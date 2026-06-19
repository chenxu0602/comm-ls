from __future__ import annotations

from pathlib import Path
import re

import numpy as np
import pandas as pd

from comm_ls.curve_diagnostics import covid_time_regime
from comm_ls.reaction import load_frame
from comm_ls.research_quality import feature_hypothesis_family


DEFAULT_REGIME_DIMENSIONS = [
    "time_regime",
    "curve_state",
    "price_regime",
    "vol_regime",
    "momentum_regime",
    "vix_regime",
    "dxy_regime",
    "ovx_regime",
]


def _write_frame(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix == ".parquet":
        df.to_parquet(output_path, index=False)
    elif output_path.suffix == ".csv":
        df.to_csv(output_path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")


def _direction_sign(row: pd.Series) -> float:
    if "direction_sign" in row.index and pd.notna(row["direction_sign"]):
        value = float(pd.to_numeric(row["direction_sign"], errors="coerce"))
        if value != 0:
            return float(np.sign(value))
    direction = str(row.get("direction", "")).lower().strip()
    if direction == "positive":
        return 1.0
    if direction == "negative":
        return -1.0
    for col in [
        "observed_beta_sign",
        "median_nonoverlap_beta_per_1z",
        "median_beta_per_1z",
        "signed_sensitivity",
        "preferred_mean_signed_return",
    ]:
        if col in row.index and pd.notna(row[col]):
            value = float(pd.to_numeric(row[col], errors="coerce"))
            if value != 0:
                return float(np.sign(value))
    return 0.0


def _available_horizons(cache: pd.DataFrame, return_column: str) -> dict[int, str]:
    escaped = re.escape(return_column)
    multi_pattern = re.compile(rf"^fwd_return__{escaped}_(\d+)d$")
    simple_pattern = re.compile(r"^fwd_residual_return_(\d+)d$")
    out: dict[int, str] = {}
    for col in cache.columns:
        match = multi_pattern.match(col)
        if match:
            out[int(match.group(1))] = col
    if not out and return_column in {"residual_return", "residual_return_mktsec_w12m"}:
        for col in cache.columns:
            match = simple_pattern.match(col)
            if match:
                out[int(match.group(1))] = col
    return dict(sorted(out.items()))


def _t_stat(values: pd.Series) -> float:
    clean = pd.to_numeric(values, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    if len(clean) < 3:
        return np.nan
    std = clean.std(ddof=1)
    if pd.isna(std) or std == 0:
        return np.nan
    return float(clean.mean() / std * np.sqrt(len(clean)))


def _nonoverlap(values: pd.Series, horizon: int) -> pd.Series:
    clean = pd.to_numeric(values, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    if clean.empty:
        return clean
    return clean.iloc[np.arange(0, len(clean), max(1, horizon), dtype=int)]


def _beta_per_1z(feature_z: pd.Series, target: pd.Series) -> float:
    sample = pd.DataFrame({"x": feature_z, "y": target}).replace([np.inf, -np.inf], np.nan).dropna()
    if len(sample) < 3:
        return np.nan
    variance = float(sample["x"].var(ddof=1))
    if not np.isfinite(variance) or variance == 0:
        return np.nan
    return float(sample["x"].cov(sample["y"]) / variance)


def _classify_curve_state(row: pd.Series, curve_z_threshold: float) -> str:
    spread = pd.to_numeric(row.get("front_third_spread"), errors="coerce")
    spread_z = pd.to_numeric(row.get("front_third_spread_z_252d"), errors="coerce")
    if pd.notna(spread) and pd.notna(spread_z):
        if spread > 0 and spread_z >= curve_z_threshold:
            return "curve_tight"
        if spread < 0 and spread_z <= -curve_z_threshold:
            return "curve_loose"
    return "curve_neutral"


def _classify_price_regime(row: pd.Series, price_share_threshold: float) -> str:
    high_share = pd.to_numeric(row.get("front_price_high_share_100d_q80_3y"), errors="coerce")
    low_share = pd.to_numeric(row.get("front_price_low_share_100d_q20_3y"), errors="coerce")
    if pd.notna(high_share) and high_share >= price_share_threshold:
        return "high_price"
    if pd.notna(low_share) and low_share >= price_share_threshold:
        return "low_price"
    return "normal_price"


def _classify_vol_regime(row: pd.Series, vol_z_threshold: float) -> str:
    vol_z = pd.to_numeric(row.get("realized_vol_20d_z_252d"), errors="coerce")
    if pd.notna(vol_z) and vol_z >= vol_z_threshold:
        return "high_vol"
    if pd.notna(vol_z) and vol_z <= -vol_z_threshold:
        return "low_vol"
    return "normal_vol"


def _classify_momentum_regime(row: pd.Series, momentum_z_threshold: float) -> str:
    momentum_z = pd.to_numeric(row.get("ret_63d_z_252d"), errors="coerce")
    if pd.notna(momentum_z) and momentum_z >= momentum_z_threshold:
        return "momentum_up"
    if pd.notna(momentum_z) and momentum_z <= -momentum_z_threshold:
        return "momentum_down"
    return "momentum_neutral"


def _commodity_regimes(
    commodity_signals: pd.DataFrame,
    curve_z_threshold: float,
    price_share_threshold: float,
    vol_z_threshold: float,
    momentum_z_threshold: float,
    macro_regime: pd.DataFrame | None = None,
) -> pd.DataFrame:
    signals = commodity_signals.copy()
    required = {"date", "symbol"}
    missing = required.difference(signals.columns)
    if missing:
        raise ValueError(f"commodity signals is missing required columns: {sorted(missing)}")
    signals["commodity"] = signals["symbol"].astype(str).str.upper().str.strip()
    signals["date"] = pd.to_datetime(signals["date"], utc=False)
    keep_cols = [
        "date",
        "commodity",
        "front_third_spread",
        "front_third_spread_z_252d",
        "ret_63d_z_252d",
        "realized_vol_20d_z_252d",
        "front_price_high_share_100d_q80_3y",
        "front_price_low_share_100d_q20_3y",
    ]
    out = signals[[col for col in keep_cols if col in signals.columns]].copy()
    out["time_regime"] = out["date"].map(covid_time_regime)
    out["curve_state"] = out.apply(_classify_curve_state, axis=1, curve_z_threshold=curve_z_threshold)
    out["price_regime"] = out.apply(_classify_price_regime, axis=1, price_share_threshold=price_share_threshold)
    out["vol_regime"] = out.apply(_classify_vol_regime, axis=1, vol_z_threshold=vol_z_threshold)
    out["momentum_regime"] = out.apply(
        _classify_momentum_regime,
        axis=1,
        momentum_z_threshold=momentum_z_threshold,
    )

    if macro_regime is not None and not macro_regime.empty:
        mr = macro_regime.copy()
        mr["date"] = pd.to_datetime(mr["date"], utc=False)
        for col in ["vix_regime", "dxy_regime", "ovx_regime"]:
            if col in mr.columns:
                out = out.merge(mr[["date", col]], on="date", how="left")
                out[col] = out[col].fillna("unknown")

    return out


def _regime_stats(
    frame: pd.DataFrame,
    horizon: int,
    direction_sign: float,
) -> dict[str, object]:
    target = pd.to_numeric(frame["target_return"], errors="coerce")
    feature_z = pd.to_numeric(frame["feature_z"], errors="coerce")
    side = np.sign(feature_z) * direction_sign
    signed_return = side * target
    valid = pd.DataFrame({"signed_return": signed_return, "target": target, "feature_z": feature_z}).replace(
        [np.inf, -np.inf],
        np.nan,
    ).dropna()
    event_count = int(len(valid))
    nonoverlap = _nonoverlap(valid["signed_return"], horizon)
    beta = _beta_per_1z(valid["feature_z"], valid["target"])
    signed_beta = float(direction_sign * beta) if pd.notna(beta) else np.nan
    return {
        "event_count": event_count,
        "nonoverlap_event_count": int(len(nonoverlap)),
        "mean_signed_return": float(valid["signed_return"].mean()) if event_count else np.nan,
        "median_signed_return": float(valid["signed_return"].median()) if event_count else np.nan,
        "hit_rate": float((valid["signed_return"] > 0).mean()) if event_count else np.nan,
        "t_stat": _t_stat(valid["signed_return"]),
        "nonoverlap_t_stat": _t_stat(nonoverlap),
        "mean_target_return": float(valid["target"].mean()) if event_count else np.nan,
        "beta_per_1z": beta,
        "signed_beta_per_1z": signed_beta,
        "mean_abs_feature_z": float(valid["feature_z"].abs().mean()) if event_count else np.nan,
    }


def _validity_summary(
    detail: pd.DataFrame,
    min_regime_event_count: int,
    min_positive_regime_share: float,
    max_dominant_regime_event_share: float,
    min_effective_regime_count: float,
) -> dict[str, object]:
    usable = detail[detail["event_count"] >= min_regime_event_count].copy()
    total_events = int(detail["event_count"].sum()) if not detail.empty else 0
    if usable.empty:
        return {
            "total_event_count": total_events,
            "usable_regime_count": 0,
            "positive_regime_share": np.nan,
            "dominant_regime_event_share": np.nan,
            "effective_regime_count": 0.0,
            "worst_regime_mean_signed_return": np.nan,
            "worst_regime_nonoverlap_t_stat": np.nan,
            "best_regime_mean_signed_return": np.nan,
            "regime_validity_verdict": "insufficient_regime_events",
            "regime_validity_flags": "insufficient_regime_events",
        }

    positive_share = float((usable["mean_signed_return"] > 0).mean())
    weights = pd.to_numeric(usable["event_count"], errors="coerce").fillna(0.0)
    total_weight = float(weights.sum())
    shares = weights / total_weight if total_weight > 0 else weights
    dominant_share = float(shares.max()) if total_weight > 0 else np.nan
    hhi = float((shares * shares).sum()) if total_weight > 0 else np.nan
    effective_count = float(1.0 / hhi) if pd.notna(hhi) and hhi > 0 else 0.0

    flags: list[str] = []
    if positive_share < min_positive_regime_share:
        flags.append("unstable_across_regimes")
    if pd.notna(dominant_share) and dominant_share > max_dominant_regime_event_share:
        flags.append("dominant_regime_concentration")
    if effective_count < min_effective_regime_count:
        flags.append("low_effective_regime_count")
    if (usable["mean_signed_return"] <= 0).any():
        flags.append("negative_regime_bucket")

    if "unstable_across_regimes" in flags or "negative_regime_bucket" in flags:
        verdict = "unstable"
    elif "dominant_regime_concentration" in flags or "low_effective_regime_count" in flags:
        verdict = "concentrated"
    else:
        verdict = "stable"

    return {
        "total_event_count": total_events,
        "usable_regime_count": int(len(usable)),
        "positive_regime_share": positive_share,
        "dominant_regime_event_share": dominant_share,
        "effective_regime_count": effective_count,
        "worst_regime_mean_signed_return": float(usable["mean_signed_return"].min()),
        "worst_regime_nonoverlap_t_stat": float(usable["nonoverlap_t_stat"].min()),
        "best_regime_mean_signed_return": float(usable["mean_signed_return"].max()),
        "regime_validity_verdict": verdict,
        "regime_validity_flags": ",".join(flags),
    }


def build_regime_conditioned_validity_audit(
    candidates: pd.DataFrame,
    cache: pd.DataFrame,
    commodity_signals: pd.DataFrame,
    commodity: str | None = None,
    return_column: str = "residual_return_mktsec_w12m",
    horizons: list[int] | tuple[int, ...] | None = None,
    activation_z: float = 1.5,
    regime_dimensions: list[str] | tuple[str, ...] | None = None,
    min_regime_event_count: int = 20,
    min_positive_regime_share: float = 0.67,
    max_dominant_regime_event_share: float = 0.70,
    min_effective_regime_count: float = 1.5,
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
        raise ValueError(
            f"Cache has no forward return columns for return_column={return_column}. "
            "Rebuild with build-daily-feature-return-cache and the desired --horizon values."
        )

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
        commodity_signals=commodity_signals,
        curve_z_threshold=curve_z_threshold,
        price_share_threshold=price_share_threshold,
        vol_z_threshold=vol_z_threshold,
        momentum_z_threshold=momentum_z_threshold,
        macro_regime=macro_regime,
    )
    cache = cache.merge(
        regimes[["date", "commodity", *regime_dimensions]].drop_duplicates(["date", "commodity"]),
        on=["date", "commodity"],
        how="left",
    )

    detail_rows: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []
    meta_cols = [
        "theme",
        "role",
        "region",
        "feature_family",
        "feature_hypothesis_family",
        "preferred_horizon",
        "confidence",
        "selection_reason",
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
                {
                    **base_record,
                    "regime_validity_verdict": "missing_cache_feature",
                    "regime_validity_flags": "missing_cache_feature",
                }
            )
            continue
        data[feature_col] = pd.to_numeric(data[feature_col], errors="coerce")
        triggered = data[data[feature_col].abs() >= activation_z].copy()
        if triggered.empty:
            summary_rows.append(
                {**base_record, "regime_validity_verdict": "no_triggers", "regime_validity_flags": "no_triggers"}
            )
            continue

        candidate_detail: list[dict[str, object]] = []
        for horizon in usable_horizons:
            target_col = available[horizon]
            frame = triggered.copy()
            frame["feature_z"] = frame[feature_col]
            frame["target_return"] = pd.to_numeric(frame[target_col], errors="coerce")
            for dimension in regime_dimensions:
                if dimension not in frame.columns:
                    continue
                for bucket, bucket_frame in frame.groupby(dimension, dropna=False, sort=True):
                    stats = _regime_stats(bucket_frame, horizon=horizon, direction_sign=direction_sign)
                    row = {
                        **base_record,
                        "horizon_days": horizon,
                        "regime_dimension": dimension,
                        "regime_bucket": str(bucket),
                        **stats,
                    }
                    candidate_detail.append(row)
                    detail_rows.append(row)

        if not candidate_detail:
            summary_rows.append(
                {
                    **base_record,
                    "regime_validity_verdict": "missing_regime_detail",
                    "regime_validity_flags": "missing_regime_detail",
                }
            )
            continue

        detail_df = pd.DataFrame(candidate_detail)
        for (horizon, dimension), detail_group in detail_df.groupby(["horizon_days", "regime_dimension"], sort=True):
            summary = _validity_summary(
                detail_group,
                min_regime_event_count=min_regime_event_count,
                min_positive_regime_share=min_positive_regime_share,
                max_dominant_regime_event_share=max_dominant_regime_event_share,
                min_effective_regime_count=min_effective_regime_count,
            )
            summary_rows.append(
                {
                    **base_record,
                    "horizon_days": horizon,
                    "regime_dimension": dimension,
                    **summary,
                    "min_regime_event_count": min_regime_event_count,
                    "min_positive_regime_share": min_positive_regime_share,
                    "max_dominant_regime_event_share": max_dominant_regime_event_share,
                    "min_effective_regime_count": min_effective_regime_count,
                }
            )

    summary = pd.DataFrame(summary_rows)
    detail = pd.DataFrame(detail_rows)
    if not summary.empty:
        front = [
            "regime_validity_verdict",
            "regime_validity_flags",
            "ticker",
            "commodity",
            "feature",
            "horizon_days",
            "regime_dimension",
            "total_event_count",
            "usable_regime_count",
            "positive_regime_share",
            "dominant_regime_event_share",
            "effective_regime_count",
            "worst_regime_mean_signed_return",
            "worst_regime_nonoverlap_t_stat",
            "best_regime_mean_signed_return",
        ]
        summary = summary[
            [col for col in front if col in summary.columns] + [col for col in summary.columns if col not in front]
        ].sort_values(["regime_validity_verdict", "ticker", "feature", "horizon_days", "regime_dimension"])
    if not detail.empty:
        front = [
            "ticker",
            "commodity",
            "feature",
            "horizon_days",
            "regime_dimension",
            "regime_bucket",
            "event_count",
            "nonoverlap_event_count",
            "mean_signed_return",
            "hit_rate",
            "t_stat",
            "nonoverlap_t_stat",
            "signed_beta_per_1z",
        ]
        detail = detail[
            [col for col in front if col in detail.columns] + [col for col in detail.columns if col not in front]
        ].sort_values(["ticker", "feature", "horizon_days", "regime_dimension", "regime_bucket"])
    return summary.reset_index(drop=True), detail.reset_index(drop=True)


def build_regime_conditioned_validity_audit_from_paths(
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
    min_regime_event_count: int = 20,
    min_positive_regime_share: float = 0.67,
    max_dominant_regime_event_share: float = 0.70,
    min_effective_regime_count: float = 1.5,
    curve_z_threshold: float = 1.0,
    price_share_threshold: float = 0.6,
    vol_z_threshold: float = 1.0,
    momentum_z_threshold: float = 1.0,
    macro_regime_path: Path | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    summary, detail = build_regime_conditioned_validity_audit(
        candidates=load_frame(candidates_path),
        cache=load_frame(cache_path),
        commodity_signals=load_frame(commodity_signals_path),
        commodity=commodity,
        return_column=return_column,
        horizons=horizons,
        activation_z=activation_z,
        regime_dimensions=regime_dimensions,
        min_regime_event_count=min_regime_event_count,
        min_positive_regime_share=min_positive_regime_share,
        max_dominant_regime_event_share=max_dominant_regime_event_share,
        min_effective_regime_count=min_effective_regime_count,
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
