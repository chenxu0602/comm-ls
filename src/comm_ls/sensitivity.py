from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from comm_ls.candidates import build_candidate_signals
from comm_ls.reaction import DEFAULT_FEATURES, load_frame
from comm_ls.universe import load_seed_universe


def build_stock_sensitivity_registry(
    reactions: pd.DataFrame,
    seed_universe: pd.DataFrame,
    min_events: int = 30,
    min_abs_t: float = 3.0,
    min_same_direction_horizons: int = 2,
) -> pd.DataFrame:
    candidates = build_candidate_signals(
        reactions=reactions,
        seed_universe=seed_universe,
        min_events=min_events,
        min_abs_t=min_abs_t,
        min_same_direction_horizons=min_same_direction_horizons,
    )
    if candidates.empty:
        return candidates

    registry = candidates.copy()
    registry["direction_sign"] = np.where(registry["direction"] == "positive", 1.0, -1.0)
    registry["sensitivity"] = registry["preferred_mean_signed_return"].abs()
    registry["signed_sensitivity"] = registry["direction_sign"] * registry["sensitivity"]
    registry["score_weight"] = registry["signed_sensitivity"] * registry["max_abs_tstat"].clip(upper=5.0)

    cols = [
        "as_of_date",
        "ticker",
        "theme",
        "role",
        "region",
        "commodity",
        "feature",
        "direction",
        "direction_sign",
        "preferred_horizon",
        "preferred_event_count",
        "preferred_mean_signed_return",
        "preferred_hit_rate",
        "preferred_feature_return_corr",
        "tstat_5d",
        "tstat_10d",
        "tstat_21d",
        "max_abs_tstat",
        "avg_tstat",
        "same_direction_horizons",
        "sensitivity",
        "signed_sensitivity",
        "score_weight",
        "economic_label",
        "confidence",
    ]
    return registry[[col for col in cols if col in registry.columns]].sort_values(
        ["ticker", "commodity", "feature"]
    ).reset_index(drop=True)


def _feature_z_scores(
    commodity_signals: pd.DataFrame,
    features: list[str],
    feature_z_window: int,
    min_feature_observations: int,
) -> pd.DataFrame:
    signals = commodity_signals.copy()
    signals["date"] = pd.to_datetime(signals["date"], utc=False)
    signals["arrival"] = pd.to_datetime(signals["arrival"], utc=False)

    missing = set(features).difference(signals.columns)
    if missing:
        raise ValueError(f"Commodity signals are missing features: {sorted(missing)}")

    rows: list[pd.DataFrame] = []
    for commodity, group in signals.groupby("symbol", sort=True):
        g = group.sort_values("date").copy()
        for feature in features:
            value = pd.to_numeric(g[feature], errors="coerce")
            mean = value.rolling(feature_z_window, min_periods=min_feature_observations).mean()
            std = value.rolling(feature_z_window, min_periods=min_feature_observations).std()
            rows.append(
                pd.DataFrame(
                    {
                        "date": g["date"],
                        "arrival": g["arrival"],
                        "commodity": commodity,
                        "feature": feature,
                        "feature_value": value,
                        "feature_z": (value - mean) / std,
                    }
                )
            )
    return pd.concat(rows, ignore_index=True).dropna(subset=["feature_z"])


def build_daily_scores_from_registry(
    registry: pd.DataFrame,
    commodity_signals: pd.DataFrame,
    as_of_date: str,
    features: list[str] | None = None,
    feature_z_window: int = 252,
    min_feature_observations: int = 126,
) -> pd.DataFrame:
    features = features or DEFAULT_FEATURES
    z = _feature_z_scores(
        commodity_signals=commodity_signals,
        features=features,
        feature_z_window=feature_z_window,
        min_feature_observations=min_feature_observations,
    )

    as_of = pd.Timestamp(as_of_date)
    z = z[z["arrival"] <= as_of]
    if z.empty:
        return pd.DataFrame()
    latest_dates = z.groupby(["commodity", "feature"])["date"].max().reset_index()
    z = z.merge(latest_dates, on=["commodity", "feature", "date"], how="inner")
    reg = registry.copy()
    scored = reg.merge(z, on=["commodity", "feature"], how="inner")
    if scored.empty:
        return scored

    scored["component_score"] = scored["feature_z"] * scored["score_weight"]
    scored["component_abs_score"] = scored["component_score"].abs()
    scored["score_date"] = pd.Timestamp(as_of_date)

    meta = scored.sort_values(["ticker", "theme", "role"]).drop_duplicates("ticker")[
        ["ticker", "theme", "role"]
    ]
    summary = (
        scored.groupby(["score_date", "ticker"], dropna=False)
        .agg(
            arrival=("arrival", "max"),
            score=("component_score", "sum"),
            gross_signal=("component_abs_score", "sum"),
            signal_count=("component_score", "count"),
            max_component_abs_score=("component_abs_score", "max"),
        )
        .reset_index()
        .rename(columns={"score_date": "date"})
        .merge(meta, on="ticker", how="left")
    )
    cols = ["date", "arrival", "ticker", "theme", "role", "score", "gross_signal", "signal_count", "max_component_abs_score"]
    return summary[cols].sort_values("score", ascending=False).reset_index(drop=True)


def build_stock_sensitivity_registry_from_paths(
    reactions_path: Path,
    universe_path: Path,
    output_path: Path,
    min_events: int = 30,
    min_abs_t: float = 3.0,
    min_same_direction_horizons: int = 2,
) -> pd.DataFrame:
    reactions = load_frame(reactions_path)
    seed = load_seed_universe(universe_path)
    registry = build_stock_sensitivity_registry(
        reactions=reactions,
        seed_universe=seed,
        min_events=min_events,
        min_abs_t=min_abs_t,
        min_same_direction_horizons=min_same_direction_horizons,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix == ".parquet":
        registry.to_parquet(output_path, index=False)
    elif output_path.suffix == ".csv":
        registry.to_csv(output_path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")
    return registry


def build_daily_scores_from_paths(
    registry_path: Path,
    commodity_signals_path: Path,
    output_path: Path,
    as_of_date: str,
    feature_z_window: int = 252,
    min_feature_observations: int = 126,
) -> pd.DataFrame:
    registry = load_frame(registry_path)
    commodity_signals = load_frame(commodity_signals_path)
    scores = build_daily_scores_from_registry(
        registry=registry,
        commodity_signals=commodity_signals,
        as_of_date=as_of_date,
        feature_z_window=feature_z_window,
        min_feature_observations=min_feature_observations,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix == ".parquet":
        scores.to_parquet(output_path, index=False)
    elif output_path.suffix == ".csv":
        scores.to_csv(output_path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")
    return scores
