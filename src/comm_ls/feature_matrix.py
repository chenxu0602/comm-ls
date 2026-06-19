from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from comm_ls.candidates import build_candidate_signals
from comm_ls.reaction import load_frame
from comm_ls.research_quality import (
    consolidate_candidate_signals,
    feature_family,
    feature_hypothesis_family,
    load_reviewed_features,
)
from comm_ls.universe import load_seed_universe


def _direction_sign(direction: pd.Series) -> pd.Series:
    return np.where(direction.astype(str).str.lower().eq("positive"), 1.0, -1.0)


def build_stock_feature_matrix(
    signals: pd.DataFrame,
    source: str = "consolidated_candidate_signals",
) -> pd.DataFrame:
    if signals.empty:
        return signals.copy()

    df = signals.copy()
    df["ticker"] = df["ticker"].astype(str).str.upper().str.strip()
    df["commodity"] = df["commodity"].astype(str).str.upper().str.strip()
    df["feature"] = df["feature"].astype(str).str.strip()
    df["direction"] = df["direction"].astype(str).str.lower().str.strip()
    df["direction_sign"] = _direction_sign(df["direction"])

    if "feature_family" not in df.columns:
        df["feature_family"] = df["feature"].map(feature_family)
    if "feature_hypothesis_family" not in df.columns:
        df["feature_hypothesis_family"] = df["feature"].map(feature_hypothesis_family)
    if "score_weight" not in df.columns:
        sensitivity = pd.to_numeric(df["preferred_mean_signed_return"], errors="coerce").abs()
        t_weight = pd.to_numeric(df["max_abs_tstat"], errors="coerce").clip(upper=5.0)
        df["score_weight"] = df["direction_sign"] * sensitivity * t_weight
    if "signed_sensitivity" not in df.columns:
        df["signed_sensitivity"] = df["direction_sign"] * pd.to_numeric(
            df["preferred_mean_signed_return"], errors="coerce"
        ).abs()
    if "preferred_horizon" not in df.columns and "preferred_horizon_days" in df.columns:
        df["preferred_horizon"] = df["preferred_horizon_days"]

    df["default_rebalance"] = np.select(
        [
            df["feature_family"].isin(["participation", "volatility_shock"]),
            df["feature_family"].isin(["price_momentum", "fixed_contract_return"]),
            df["feature_family"].isin(["curve_carry", "curve_regime"]),
        ],
        ["daily_check", "weekly", "monthly"],
        default="weekly",
    )
    df["matrix_source"] = source
    if "as_of_date" in df.columns:
        df["matrix_date"] = pd.to_datetime(df["as_of_date"], utc=False)

    cols = [
        "matrix_date",
        "as_of_date",
        "ticker",
        "theme",
        "role",
        "region",
        "commodity",
        "feature",
        "feature_family",
        "feature_hypothesis_family",
        "direction",
        "direction_sign",
        "score_weight",
        "signed_sensitivity",
        "preferred_horizon",
        "preferred_event_count",
        "preferred_mean_signed_return",
        "preferred_hit_rate",
        "preferred_feature_return_corr",
        "max_abs_tstat",
        "same_direction_horizons",
        "confidence",
        "quality_score",
        "audit_verdict",
        "audit_flags",
        "same_direction_share",
        "peer_tickers",
        "peer_direction_share",
        "economic_label",
        "selection_reason",
        "default_rebalance",
        "matrix_source",
    ]
    keep = [col for col in cols if col in df.columns]
    return df[keep].sort_values(["ticker", "commodity", "feature"]).reset_index(drop=True)


def build_stock_feature_matrix_cache(
    reactions: pd.DataFrame,
    seed_universe: pd.DataFrame,
    forecast_audit: pd.DataFrame | None = None,
    reviewed_features: pd.DataFrame | None = None,
    min_events: int = 30,
    min_abs_t: float = 3.0,
    min_same_direction_horizons: int = 2,
    min_confidence: str = "medium",
    require_audit_candidate: bool = False,
    min_same_direction_share: float = 0.6,
    min_peer_direction_share: float = 0.0,
    max_per_ticker: int = 3,
    source: str = "rolling_feature_reactions",
) -> pd.DataFrame:
    if reactions.empty:
        return pd.DataFrame()

    df = reactions.copy()
    if "as_of_date" not in df.columns:
        raise ValueError("reactions must include as_of_date to build a matrix cache")
    df["as_of_date"] = pd.to_datetime(df["as_of_date"], utc=False)

    frames: list[pd.DataFrame] = []
    for as_of_date, group in df.groupby("as_of_date", sort=True):
        candidates = build_candidate_signals(
            reactions=group,
            seed_universe=seed_universe,
            min_events=min_events,
            min_abs_t=min_abs_t,
            min_same_direction_horizons=min_same_direction_horizons,
        )
        if candidates.empty:
            continue

        audit_slice = forecast_audit
        if forecast_audit is not None and not forecast_audit.empty and "as_of_date" in forecast_audit.columns:
            audit = forecast_audit.copy()
            audit["as_of_date"] = pd.to_datetime(audit["as_of_date"], utc=False)
            audit_slice = audit[audit["as_of_date"] <= pd.Timestamp(as_of_date)].copy()

        consolidated = consolidate_candidate_signals(
            candidates=candidates,
            forecast_audit=audit_slice,
            reviewed_features=reviewed_features,
            min_confidence=min_confidence,
            require_audit_candidate=require_audit_candidate,
            min_same_direction_share=min_same_direction_share,
            min_peer_direction_share=min_peer_direction_share,
            max_per_ticker=max_per_ticker,
        )
        if consolidated.empty:
            continue

        matrix = build_stock_feature_matrix(consolidated, source=source)
        matrix["matrix_date"] = pd.Timestamp(as_of_date)
        matrix["as_of_date"] = pd.Timestamp(as_of_date)
        frames.append(matrix)

    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True).sort_values(
        ["matrix_date", "ticker", "commodity", "feature"]
    ).reset_index(drop=True)


def build_stock_feature_matrix_from_paths(
    signals_path: Path,
    output_path: Path,
    source: str = "consolidated_candidate_signals",
) -> pd.DataFrame:
    signals = load_frame(signals_path)
    matrix = build_stock_feature_matrix(signals=signals, source=source)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix == ".parquet":
        matrix.to_parquet(output_path, index=False)
    elif output_path.suffix == ".csv":
        matrix.to_csv(output_path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")
    return matrix


def build_stock_feature_matrix_cache_from_paths(
    reactions_path: Path,
    universe_path: Path,
    output_path: Path,
    forecast_audit_path: Path | None = None,
    reviewed_features_path: Path | None = None,
    min_events: int = 30,
    min_abs_t: float = 3.0,
    min_same_direction_horizons: int = 2,
    min_confidence: str = "medium",
    require_audit_candidate: bool = False,
    min_same_direction_share: float = 0.6,
    min_peer_direction_share: float = 0.0,
    max_per_ticker: int = 3,
    source: str = "rolling_feature_reactions",
) -> pd.DataFrame:
    reactions = load_frame(reactions_path)
    seed = load_seed_universe(universe_path)
    forecast_audit = load_frame(forecast_audit_path) if forecast_audit_path and forecast_audit_path.exists() else None
    reviewed = (
        load_reviewed_features(reviewed_features_path)
        if reviewed_features_path and reviewed_features_path.exists()
        else None
    )
    matrix = build_stock_feature_matrix_cache(
        reactions=reactions,
        seed_universe=seed,
        forecast_audit=forecast_audit,
        reviewed_features=reviewed,
        min_events=min_events,
        min_abs_t=min_abs_t,
        min_same_direction_horizons=min_same_direction_horizons,
        min_confidence=min_confidence,
        require_audit_candidate=require_audit_candidate,
        min_same_direction_share=min_same_direction_share,
        min_peer_direction_share=min_peer_direction_share,
        max_per_ticker=max_per_ticker,
        source=source,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix == ".parquet":
        matrix.to_parquet(output_path, index=False)
    elif output_path.suffix == ".csv":
        matrix.to_csv(output_path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")
    return matrix
