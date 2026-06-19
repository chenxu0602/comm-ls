from __future__ import annotations

from pathlib import Path
from itertools import combinations

import numpy as np
import pandas as pd

from comm_ls.reaction import load_frame
from comm_ls.regime_validity import (
    DEFAULT_REGIME_DIMENSIONS,
    _available_horizons,
    _commodity_regimes,
    _direction_sign,
    _regime_stats,
    _write_frame,
)
from comm_ls.research_quality import feature_hypothesis_family


def _dependency_ratio(full_mean: float, holdout_mean: float) -> float:
    if pd.isna(full_mean) or pd.isna(holdout_mean) or full_mean == 0:
        return np.nan
    return float((full_mean - holdout_mean) / abs(full_mean))


def _detail_verdict(
    full_stats: dict[str, object],
    holdout_stats: dict[str, object],
    removed_event_share: float,
    min_holdout_event_count: int,
    max_removed_event_share: float,
    max_mean_drop_ratio: float,
) -> tuple[str, str]:
    flags: list[str] = []
    full_mean = float(full_stats.get("mean_signed_return", np.nan))
    holdout_mean = float(holdout_stats.get("mean_signed_return", np.nan))
    full_beta = float(full_stats.get("signed_beta_per_1z", np.nan))
    holdout_beta = float(holdout_stats.get("signed_beta_per_1z", np.nan))
    ratio = _dependency_ratio(full_mean, holdout_mean)

    if int(holdout_stats.get("event_count", 0)) < min_holdout_event_count:
        flags.append("insufficient_holdout_events")
    if pd.notna(removed_event_share) and removed_event_share > max_removed_event_share:
        flags.append("removed_bucket_concentration")
    if pd.notna(full_mean) and full_mean <= 0:
        flags.append("full_sample_not_positive")
    if pd.notna(holdout_mean) and holdout_mean <= 0:
        flags.append("holdout_nonpositive")
    if pd.notna(full_beta) and pd.notna(holdout_beta) and np.sign(full_beta) != np.sign(holdout_beta):
        flags.append("holdout_beta_flip")
    if pd.notna(ratio) and ratio > max_mean_drop_ratio:
        flags.append("high_regime_dependency")

    if "full_sample_not_positive" in flags or "holdout_nonpositive" in flags or "holdout_beta_flip" in flags:
        verdict = "block"
    elif flags:
        verdict = "review"
    else:
        verdict = "pass"
    return verdict, ",".join(flags)


def _summary_verdict(detail: pd.DataFrame) -> tuple[str, str]:
    if detail.empty:
        return "block", "missing_adversarial_detail"
    verdicts = set(detail["adversarial_verdict"].dropna().astype(str))
    flags = sorted(
        {
            flag
            for value in detail["adversarial_flags"].dropna().astype(str)
            for flag in value.split(",")
            if flag
        }
    )
    if "block" in verdicts:
        verdict = "block"
    elif "review" in verdicts:
        verdict = "review"
    else:
        verdict = "pass"
    return verdict, ",".join(flags)


def _basket_signed_stats(frame: pd.DataFrame, horizon: int) -> dict[str, object]:
    signed = pd.to_numeric(frame["signed_return"], errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    nonoverlap = signed.iloc[np.arange(0, len(signed), max(1, horizon), dtype=int)] if not signed.empty else signed
    return {
        "event_count": int(len(signed)),
        "nonoverlap_event_count": int(len(nonoverlap)),
        "mean_signed_return": float(signed.mean()) if len(signed) else np.nan,
        "median_signed_return": float(signed.median()) if len(signed) else np.nan,
        "hit_rate": float((signed > 0).mean()) if len(signed) else np.nan,
        "t_stat": _t_stat_local(signed),
        "nonoverlap_t_stat": _t_stat_local(nonoverlap),
    }


def _t_stat_local(values: pd.Series) -> float:
    clean = pd.to_numeric(values, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    if len(clean) < 3:
        return np.nan
    std = clean.std(ddof=1)
    if pd.isna(std) or std == 0:
        return np.nan
    return float(clean.mean() / std * np.sqrt(len(clean)))


def build_regime_adversarial_audit(
    candidates: pd.DataFrame,
    cache: pd.DataFrame,
    commodity_signals: pd.DataFrame,
    commodity: str | None = None,
    return_column: str = "residual_return_mktsec_w12m",
    horizons: list[int] | tuple[int, ...] | None = None,
    activation_z: float = 1.5,
    regime_dimensions: list[str] | tuple[str, ...] | None = None,
    min_removed_event_count: int = 20,
    min_holdout_event_count: int = 40,
    max_removed_event_share: float = 0.60,
    max_mean_drop_ratio: float = 0.50,
    curve_z_threshold: float = 1.0,
    price_share_threshold: float = 0.6,
    vol_z_threshold: float = 1.0,
    momentum_z_threshold: float = 1.0,
    macro_regime: pd.DataFrame | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if candidates.empty:
        return candidates.copy(), pd.DataFrame()
    required = {"ticker", "commodity", "feature"}
    missing = required.difference(candidates.columns)
    if missing:
        raise ValueError(f"candidates is missing required columns: {sorted(missing)}")

    cache = cache.copy()
    cache["ticker"] = cache["ticker"].astype(str).str.upper().str.strip()
    cache["commodity"] = cache["commodity"].astype(str).str.upper().str.strip()
    cache["date"] = pd.to_datetime(cache["date"], utc=False)
    available = _available_horizons(cache, return_column)
    requested = sorted(set(int(h) for h in horizons)) if horizons else sorted(available)
    usable_horizons = [h for h in requested if h in available]
    if not usable_horizons:
        raise ValueError(f"Cache has no forward return columns for return_column={return_column}.")

    cand = candidates.copy()
    cand["ticker"] = cand["ticker"].astype(str).str.upper().str.strip()
    cand["commodity"] = cand["commodity"].astype(str).str.upper().str.strip()
    cand["feature"] = cand["feature"].astype(str).str.strip()
    if commodity is not None:
        keep_commodity = commodity.upper().strip()
        cand = cand[cand["commodity"].eq(keep_commodity)].copy()
        cache = cache[cache["commodity"].eq(keep_commodity)].copy()
    if "feature_hypothesis_family" not in cand.columns:
        cand["feature_hypothesis_family"] = cand["feature"].map(feature_hypothesis_family)
    cand["_direction_sign"] = cand.apply(_direction_sign, axis=1)
    cand = cand[cand["_direction_sign"].ne(0)].copy()
    regime_dimensions = list(regime_dimensions or DEFAULT_REGIME_DIMENSIONS)

    regimes = _commodity_regimes(
        macro_regime=macro_regime,
        commodity_signals=commodity_signals,
        curve_z_threshold=curve_z_threshold,
        price_share_threshold=price_share_threshold,
        vol_z_threshold=vol_z_threshold,
        momentum_z_threshold=momentum_z_threshold,
    )
    cache = cache.merge(
        regimes[["date", "commodity", *regime_dimensions]].drop_duplicates(["date", "commodity"]),
        on=["date", "commodity"],
        how="left",
    )

    summary_rows: list[dict[str, object]] = []
    detail_rows: list[dict[str, object]] = []
    meta_cols = [
        "theme",
        "role",
        "region",
        "feature_family",
        "feature_hypothesis_family",
        "exposure_role",
        "selection_verdict",
    ]

    for key, group in cand.groupby(["ticker", "commodity", "feature"], dropna=False, sort=True):
        ticker, commodity_code, feature = key
        direction_sign = float(group["_direction_sign"].dropna().iloc[0])
        feature_col = f"feature_z__{feature}"
        base_record: dict[str, object] = {
            "ticker": ticker,
            "commodity": commodity_code,
            "feature": feature,
            "direction_sign": direction_sign,
            "activation_z": activation_z,
            "return_column": return_column,
        }
        for col in meta_cols:
            if col in group.columns:
                values = group[col].dropna()
                base_record[col] = values.iloc[0] if not values.empty else np.nan

        data = cache[(cache["ticker"].eq(ticker)) & (cache["commodity"].eq(commodity_code))].copy()
        if data.empty or feature_col not in data.columns:
            summary_rows.append(
                {**base_record, "adversarial_verdict": "block", "adversarial_flags": "missing_cache_feature"}
            )
            continue
        data[feature_col] = pd.to_numeric(data[feature_col], errors="coerce")
        triggered = data[data[feature_col].abs() >= activation_z].copy()
        if triggered.empty:
            summary_rows.append({**base_record, "adversarial_verdict": "block", "adversarial_flags": "no_triggers"})
            continue

        candidate_detail: list[dict[str, object]] = []
        for horizon in usable_horizons:
            target_col = available[horizon]
            frame = triggered.copy()
            frame["feature_z"] = frame[feature_col]
            frame["target_return"] = pd.to_numeric(frame[target_col], errors="coerce")
            full_stats = _regime_stats(frame, horizon=horizon, direction_sign=direction_sign)
            full_event_count = int(full_stats["event_count"])
            for dimension in regime_dimensions:
                if dimension not in frame.columns:
                    continue
                for bucket, bucket_frame in frame.groupby(dimension, dropna=False, sort=True):
                    removed_stats = _regime_stats(bucket_frame, horizon=horizon, direction_sign=direction_sign)
                    removed_event_count = int(removed_stats["event_count"])
                    if removed_event_count < min_removed_event_count:
                        continue
                    holdout_frame = frame[frame[dimension].ne(bucket)].copy()
                    holdout_stats = _regime_stats(holdout_frame, horizon=horizon, direction_sign=direction_sign)
                    removed_share = removed_event_count / full_event_count if full_event_count else np.nan
                    verdict, flags = _detail_verdict(
                        full_stats=full_stats,
                        holdout_stats=holdout_stats,
                        removed_event_share=removed_share,
                        min_holdout_event_count=min_holdout_event_count,
                        max_removed_event_share=max_removed_event_share,
                        max_mean_drop_ratio=max_mean_drop_ratio,
                    )
                    row = {
                        **base_record,
                        "horizon_days": horizon,
                        "regime_dimension": dimension,
                        "removed_regime_bucket": str(bucket),
                        "adversarial_verdict": verdict,
                        "adversarial_flags": flags,
                        "full_event_count": full_event_count,
                        "removed_event_count": removed_event_count,
                        "holdout_event_count": int(holdout_stats["event_count"]),
                        "removed_event_share": removed_share,
                        "full_mean_signed_return": full_stats["mean_signed_return"],
                        "removed_mean_signed_return": removed_stats["mean_signed_return"],
                        "holdout_mean_signed_return": holdout_stats["mean_signed_return"],
                        "mean_signed_return_drop": float(
                            full_stats["mean_signed_return"] - holdout_stats["mean_signed_return"]
                        )
                        if pd.notna(full_stats["mean_signed_return"])
                        and pd.notna(holdout_stats["mean_signed_return"])
                        else np.nan,
                        "mean_drop_ratio": _dependency_ratio(
                            float(full_stats["mean_signed_return"]),
                            float(holdout_stats["mean_signed_return"]),
                        ),
                        "full_nonoverlap_t_stat": full_stats["nonoverlap_t_stat"],
                        "holdout_nonoverlap_t_stat": holdout_stats["nonoverlap_t_stat"],
                        "full_signed_beta_per_1z": full_stats["signed_beta_per_1z"],
                        "holdout_signed_beta_per_1z": holdout_stats["signed_beta_per_1z"],
                        "min_removed_event_count": min_removed_event_count,
                        "min_holdout_event_count": min_holdout_event_count,
                        "max_removed_event_share": max_removed_event_share,
                        "max_mean_drop_ratio": max_mean_drop_ratio,
                    }
                    candidate_detail.append(row)
                    detail_rows.append(row)

        if not candidate_detail:
            summary_rows.append(
                {**base_record, "adversarial_verdict": "block", "adversarial_flags": "missing_adversarial_detail"}
            )
            continue
        detail_df = pd.DataFrame(candidate_detail)
        for (horizon, dimension), detail_group in detail_df.groupby(["horizon_days", "regime_dimension"], sort=True):
            verdict, flags = _summary_verdict(detail_group)
            summary_rows.append(
                {
                    **base_record,
                    "horizon_days": horizon,
                    "regime_dimension": dimension,
                    "adversarial_verdict": verdict,
                    "adversarial_flags": flags,
                    "tested_removed_buckets": int(detail_group["removed_regime_bucket"].nunique()),
                    "worst_holdout_mean_signed_return": float(detail_group["holdout_mean_signed_return"].min()),
                    "worst_holdout_nonoverlap_t_stat": float(detail_group["holdout_nonoverlap_t_stat"].min()),
                    "max_mean_drop_ratio_observed": float(detail_group["mean_drop_ratio"].max()),
                    "max_removed_event_share_observed": float(detail_group["removed_event_share"].max()),
                    "min_holdout_event_count_observed": int(detail_group["holdout_event_count"].min()),
                    "full_mean_signed_return": float(detail_group["full_mean_signed_return"].iloc[0]),
                    "full_nonoverlap_t_stat": float(detail_group["full_nonoverlap_t_stat"].iloc[0]),
                    "full_signed_beta_per_1z": float(detail_group["full_signed_beta_per_1z"].iloc[0]),
                }
            )

    summary = pd.DataFrame(summary_rows)
    detail = pd.DataFrame(detail_rows)
    if not summary.empty:
        front = [
            "adversarial_verdict",
            "adversarial_flags",
            "ticker",
            "commodity",
            "feature",
            "horizon_days",
            "regime_dimension",
            "tested_removed_buckets",
            "worst_holdout_mean_signed_return",
            "worst_holdout_nonoverlap_t_stat",
            "max_mean_drop_ratio_observed",
            "max_removed_event_share_observed",
        ]
        summary = summary[
            [col for col in front if col in summary.columns] + [col for col in summary.columns if col not in front]
        ].sort_values(["adversarial_verdict", "ticker", "feature", "horizon_days", "regime_dimension"])
    if not detail.empty:
        front = [
            "adversarial_verdict",
            "adversarial_flags",
            "ticker",
            "commodity",
            "feature",
            "horizon_days",
            "regime_dimension",
            "removed_regime_bucket",
            "full_event_count",
            "removed_event_count",
            "holdout_event_count",
            "removed_event_share",
            "full_mean_signed_return",
            "removed_mean_signed_return",
            "holdout_mean_signed_return",
            "mean_drop_ratio",
        ]
        detail = detail[
            [col for col in front if col in detail.columns] + [col for col in detail.columns if col not in front]
        ].sort_values(["ticker", "feature", "horizon_days", "regime_dimension", "removed_regime_bucket"])
    return summary.reset_index(drop=True), detail.reset_index(drop=True)


def build_regime_adversarial_audit_from_paths(
    candidates_path: Path,
    cache_path: Path,
    commodity_signals_path: Path,
    output_path: Path,
    detail_output_path: Path | None = None,
    commodity: str | None = None,
    return_column: str = "residual_return_mktsec_w12m",
    horizons: list[int] | tuple[int, ...] | None = None,
    activation_z: float = 1.5,
    regime_dimensions: list[str] | tuple[str, ...] | None = None,
    min_removed_event_count: int = 20,
    min_holdout_event_count: int = 40,
    max_removed_event_share: float = 0.60,
    max_mean_drop_ratio: float = 0.50,
    curve_z_threshold: float = 1.0,
    price_share_threshold: float = 0.6,
    vol_z_threshold: float = 1.0,
    momentum_z_threshold: float = 1.0,
    macro_regime_path: Path | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    summary, detail = build_regime_adversarial_audit(
        candidates=load_frame(candidates_path),
        cache=load_frame(cache_path),
        commodity_signals=load_frame(commodity_signals_path),
        commodity=commodity,
        return_column=return_column,
        horizons=horizons,
        activation_z=activation_z,
        regime_dimensions=regime_dimensions,
        min_removed_event_count=min_removed_event_count,
        min_holdout_event_count=min_holdout_event_count,
        max_removed_event_share=max_removed_event_share,
        max_mean_drop_ratio=max_mean_drop_ratio,
        curve_z_threshold=curve_z_threshold,
        price_share_threshold=price_share_threshold,
        vol_z_threshold=vol_z_threshold,
        momentum_z_threshold=momentum_z_threshold,
        macro_regime=load_frame(macro_regime_path) if macro_regime_path else None,
    )
    _write_frame(summary, output_path)
    if detail_output_path is not None:
        _write_frame(detail, detail_output_path)
    return summary, detail


def build_basket_regime_adversarial_audit(
    candidates: pd.DataFrame,
    cache: pd.DataFrame,
    commodity_signals: pd.DataFrame,
    commodity: str | None = None,
    return_column: str = "residual_return_mktsec_w12m",
    horizon: int = 42,
    activation_z: float = 1.5,
    regime_dimensions: list[str] | tuple[str, ...] | None = None,
    min_removed_event_count: int = 20,
    min_holdout_event_count: int = 40,
    max_removed_event_share: float = 0.60,
    max_mean_drop_ratio: float = 0.50,
    curve_z_threshold: float = 1.0,
    price_share_threshold: float = 0.6,
    vol_z_threshold: float = 1.0,
    momentum_z_threshold: float = 1.0,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if candidates.empty:
        return pd.DataFrame(), pd.DataFrame()

    cache = cache.copy()
    cache["ticker"] = cache["ticker"].astype(str).str.upper().str.strip()
    cache["commodity"] = cache["commodity"].astype(str).str.upper().str.strip()
    cache["date"] = pd.to_datetime(cache["date"], utc=False)
    available = _available_horizons(cache, return_column)
    if int(horizon) not in available:
        raise ValueError(f"Cache has no forward return column for return_column={return_column}, horizon={horizon}.")

    cand = candidates.copy()
    cand["ticker"] = cand["ticker"].astype(str).str.upper().str.strip()
    cand["commodity"] = cand["commodity"].astype(str).str.upper().str.strip()
    cand["feature"] = cand["feature"].astype(str).str.strip()
    if commodity is not None:
        keep_commodity = commodity.upper().strip()
        cand = cand[cand["commodity"].eq(keep_commodity)].copy()
        cache = cache[cache["commodity"].eq(keep_commodity)].copy()
    cand["_direction_sign"] = cand.apply(_direction_sign, axis=1)
    cand = cand[cand["_direction_sign"].ne(0)].copy()
    pairs = cand[["ticker", "commodity", "feature", "_direction_sign"]].drop_duplicates()
    regime_dimensions = list(regime_dimensions or DEFAULT_REGIME_DIMENSIONS)

    regimes = _commodity_regimes(
        commodity_signals=commodity_signals,
        curve_z_threshold=curve_z_threshold,
        price_share_threshold=price_share_threshold,
        vol_z_threshold=vol_z_threshold,
        momentum_z_threshold=momentum_z_threshold,
    )
    cache = cache.merge(
        regimes[["date", "commodity", *regime_dimensions]].drop_duplicates(["date", "commodity"]),
        on=["date", "commodity"],
        how="left",
    )

    target_col = available[int(horizon)]
    event_frames: list[pd.DataFrame] = []
    for _, row in pairs.iterrows():
        ticker = row["ticker"]
        commodity_code = row["commodity"]
        feature = row["feature"]
        feature_col = f"feature_z__{feature}"
        data = cache[(cache["ticker"].eq(ticker)) & (cache["commodity"].eq(commodity_code))].copy()
        if data.empty or feature_col not in data.columns or target_col not in data.columns:
            continue
        data["feature_z"] = pd.to_numeric(data[feature_col], errors="coerce")
        data["target_return"] = pd.to_numeric(data[target_col], errors="coerce")
        data = data[data["feature_z"].abs() >= activation_z].copy()
        if data.empty:
            continue
        direction_sign = float(row["_direction_sign"])
        data["signed_return"] = np.sign(data["feature_z"]) * direction_sign * data["target_return"]
        data["source_ticker"] = ticker
        event_frames.append(
            data[
                [
                    "date",
                    "commodity",
                    "source_ticker",
                    "feature_z",
                    "target_return",
                    "signed_return",
                    *regime_dimensions,
                ]
            ]
        )

    if not event_frames:
        return pd.DataFrame(), pd.DataFrame()

    events = pd.concat(event_frames, ignore_index=True)
    daily = (
        events.groupby(["date", "commodity", *regime_dimensions], dropna=False)
        .agg(
            event_count=("signed_return", "size"),
            ticker_count=("source_ticker", "nunique"),
            signed_return=("signed_return", "mean"),
            target_return=("target_return", "mean"),
            feature_z=("feature_z", "mean"),
        )
        .reset_index()
    )
    full_stats = _basket_signed_stats(daily, horizon=int(horizon))

    rows: list[dict[str, object]] = []
    for dimension in regime_dimensions:
        if dimension not in daily.columns:
            continue
        for bucket, removed in daily.groupby(dimension, dropna=False, sort=True):
            removed_event_count = int(len(removed))
            if removed_event_count < min_removed_event_count:
                continue
            holdout = daily[daily[dimension].ne(bucket)].copy()
            removed_stats = _basket_signed_stats(removed, horizon=int(horizon))
            holdout_stats = _basket_signed_stats(holdout, horizon=int(horizon))
            removed_share = removed_event_count / len(daily) if len(daily) else np.nan
            flags: list[str] = []
            if int(holdout_stats["event_count"]) < min_holdout_event_count:
                flags.append("insufficient_holdout_events")
            if pd.notna(removed_share) and removed_share > max_removed_event_share:
                flags.append("removed_bucket_concentration")
            if pd.notna(holdout_stats["mean_signed_return"]) and holdout_stats["mean_signed_return"] <= 0:
                flags.append("holdout_nonpositive")
            ratio = _dependency_ratio(
                float(full_stats["mean_signed_return"]),
                float(holdout_stats["mean_signed_return"]),
            )
            if pd.notna(ratio) and ratio > max_mean_drop_ratio:
                flags.append("high_regime_dependency")
            verdict = "block" if "holdout_nonpositive" in flags else "review" if flags else "pass"
            rows.append(
                {
                    "adversarial_verdict": verdict,
                    "adversarial_flags": ",".join(flags),
                    "commodity": str(daily["commodity"].dropna().iloc[0]) if daily["commodity"].notna().any() else np.nan,
                    "feature_count": int(pairs["feature"].nunique()),
                    "ticker_count": int(pairs["ticker"].nunique()),
                    "horizon_days": int(horizon),
                    "return_column": return_column,
                    "activation_z": activation_z,
                    "regime_dimension": dimension,
                    "removed_regime_bucket": str(bucket),
                    "full_event_days": int(len(daily)),
                    "removed_event_days": removed_event_count,
                    "holdout_event_days": int(len(holdout)),
                    "removed_event_share": removed_share,
                    "full_mean_signed_return": full_stats["mean_signed_return"],
                    "removed_mean_signed_return": removed_stats["mean_signed_return"],
                    "holdout_mean_signed_return": holdout_stats["mean_signed_return"],
                    "mean_drop_ratio": ratio,
                    "full_nonoverlap_t_stat": full_stats["nonoverlap_t_stat"],
                    "holdout_nonoverlap_t_stat": holdout_stats["nonoverlap_t_stat"],
                    "avg_daily_ticker_count": float(daily["ticker_count"].mean()),
                    "min_removed_event_count": min_removed_event_count,
                    "min_holdout_event_count": min_holdout_event_count,
                    "max_removed_event_share": max_removed_event_share,
                    "max_mean_drop_ratio": max_mean_drop_ratio,
                }
            )

    summary = pd.DataFrame(rows)
    if not summary.empty:
        summary = summary.sort_values(["adversarial_verdict", "regime_dimension", "removed_regime_bucket"])
    return summary.reset_index(drop=True), daily.reset_index(drop=True)


def build_basket_regime_adversarial_audit_from_paths(
    candidates_path: Path,
    cache_path: Path,
    commodity_signals_path: Path,
    output_path: Path,
    events_output_path: Path | None = None,
    commodity: str | None = None,
    return_column: str = "residual_return_mktsec_w12m",
    horizon: int = 42,
    activation_z: float = 1.5,
    regime_dimensions: list[str] | tuple[str, ...] | None = None,
    min_removed_event_count: int = 20,
    min_holdout_event_count: int = 40,
    max_removed_event_share: float = 0.60,
    max_mean_drop_ratio: float = 0.50,
    curve_z_threshold: float = 1.0,
    price_share_threshold: float = 0.6,
    vol_z_threshold: float = 1.0,
    momentum_z_threshold: float = 1.0,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    summary, events = build_basket_regime_adversarial_audit(
        candidates=load_frame(candidates_path),
        cache=load_frame(cache_path),
        commodity_signals=load_frame(commodity_signals_path),
        commodity=commodity,
        return_column=return_column,
        horizon=horizon,
        activation_z=activation_z,
        regime_dimensions=regime_dimensions,
        min_removed_event_count=min_removed_event_count,
        min_holdout_event_count=min_holdout_event_count,
        max_removed_event_share=max_removed_event_share,
        max_mean_drop_ratio=max_mean_drop_ratio,
        curve_z_threshold=curve_z_threshold,
        price_share_threshold=price_share_threshold,
        vol_z_threshold=vol_z_threshold,
        momentum_z_threshold=momentum_z_threshold,
    )
    _write_frame(summary, output_path)
    if events_output_path is not None:
        _write_frame(events, events_output_path)
    return summary, events


def build_basket_state_filter_audit(
    events: pd.DataFrame,
    regime_dimension: str = "vol_regime",
    horizon: int = 42,
    min_nonoverlap_events: int = 5,
    min_nonoverlap_t_stat: float = 1.5,
) -> pd.DataFrame:
    if events.empty:
        return pd.DataFrame()
    required = {"signed_return", "ticker_count", regime_dimension}
    missing = required.difference(events.columns)
    if missing:
        raise ValueError(f"events is missing required columns: {sorted(missing)}")

    frame = events.copy()
    buckets = sorted(str(value) for value in frame[regime_dimension].dropna().astype(str).unique())
    rows: list[dict[str, object]] = []

    def add_row(filter_name: str, filter_type: str, selected_buckets: list[str], selected: pd.DataFrame) -> None:
        stats = _basket_signed_stats(selected, horizon=int(horizon))
        flags: list[str] = []
        if stats["event_count"] == 0:
            flags.append("no_events")
        if stats["nonoverlap_event_count"] < min_nonoverlap_events:
            flags.append("low_nonoverlap_events")
        if pd.notna(stats["mean_signed_return"]) and stats["mean_signed_return"] <= 0:
            flags.append("nonpositive_mean")
        if pd.notna(stats["nonoverlap_t_stat"]) and stats["nonoverlap_t_stat"] < min_nonoverlap_t_stat:
            flags.append("weak_nonoverlap_t")
        if "nonpositive_mean" in flags or "no_events" in flags:
            verdict = "block"
        elif flags:
            verdict = "review"
        else:
            verdict = "pass"
        rows.append(
            {
                "filter_verdict": verdict,
                "filter_flags": ",".join(flags),
                "regime_dimension": regime_dimension,
                "filter": filter_name,
                "filter_type": filter_type,
                "selected_buckets": ",".join(selected_buckets),
                "event_days": int(stats["event_count"]),
                "day_share": float(stats["event_count"] / len(frame)) if len(frame) else np.nan,
                "avg_daily_ticker_count": float(selected["ticker_count"].mean()) if not selected.empty else np.nan,
                "mean_signed_return": stats["mean_signed_return"],
                "median_signed_return": stats["median_signed_return"],
                "hit_rate": stats["hit_rate"],
                "nonoverlap_event_count": stats["nonoverlap_event_count"],
                "nonoverlap_t_stat": stats["nonoverlap_t_stat"],
                "horizon_days": int(horizon),
                "min_nonoverlap_events": min_nonoverlap_events,
                "min_nonoverlap_t_stat": min_nonoverlap_t_stat,
            }
        )

    add_row("all", "all", buckets, frame)
    for bucket in buckets:
        add_row(
            f"include:{bucket}",
            "include",
            [bucket],
            frame[frame[regime_dimension].astype(str).eq(bucket)].copy(),
        )
        keep = [value for value in buckets if value != bucket]
        add_row(
            f"exclude:{bucket}",
            "exclude",
            keep,
            frame[frame[regime_dimension].astype(str).ne(bucket)].copy(),
        )
    for size in range(2, len(buckets)):
        for combo in combinations(buckets, size):
            combo_list = list(combo)
            add_row(
                "include:" + "_or_".join(combo_list),
                "include_combo",
                combo_list,
                frame[frame[regime_dimension].astype(str).isin(combo_list)].copy(),
            )

    out = pd.DataFrame(rows)
    if not out.empty:
        out = out.sort_values(["filter_verdict", "nonoverlap_t_stat", "mean_signed_return"], ascending=[True, False, False])
    return out.reset_index(drop=True)


def build_basket_state_filter_audit_from_paths(
    events_path: Path,
    output_path: Path,
    regime_dimension: str = "vol_regime",
    horizon: int = 42,
    min_nonoverlap_events: int = 5,
    min_nonoverlap_t_stat: float = 1.5,
) -> pd.DataFrame:
    audit = build_basket_state_filter_audit(
        events=load_frame(events_path),
        regime_dimension=regime_dimension,
        horizon=horizon,
        min_nonoverlap_events=min_nonoverlap_events,
        min_nonoverlap_t_stat=min_nonoverlap_t_stat,
    )
    _write_frame(audit, output_path)
    return audit
