from __future__ import annotations

from pathlib import Path
import re

import numpy as np
import pandas as pd

from comm_ls.reaction import load_frame
from comm_ls.research_quality import feature_hypothesis_family


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


def _decay_summary(
    detail: pd.DataFrame,
    min_event_count: int,
    min_sign_stability: float,
) -> dict[str, object]:
    usable = detail[detail["event_count"] >= min_event_count].copy()
    if usable.empty:
        return {
            "usable_horizon_count": 0,
            "positive_horizon_count": 0,
            "sign_stability_share": np.nan,
            "peak_horizon_days": np.nan,
            "peak_mean_signed_return": np.nan,
            "half_life_horizon_days": np.nan,
            "half_life_bucket": "insufficient",
            "delayed_peak": False,
            "decay_slope_corr": np.nan,
            "decay_verdict": "insufficient_events",
            "decay_flags": "insufficient_events",
        }

    usable = usable.sort_values("horizon_days")
    positive = usable["mean_signed_return"] > 0
    sign_stability = float(positive.mean())
    peak_idx = usable["mean_signed_return"].idxmax()
    peak = usable.loc[peak_idx]
    peak_horizon = int(peak["horizon_days"])
    peak_mean = float(peak["mean_signed_return"])
    first_horizon = int(usable["horizon_days"].min())
    first_mean = float(usable.iloc[0]["mean_signed_return"])

    if len(usable) >= 2 and usable["mean_signed_return"].std(ddof=0) > 0:
        decay_slope_corr = float(np.corrcoef(np.log(usable["horizon_days"]), usable["mean_signed_return"])[0, 1])
    else:
        decay_slope_corr = np.nan

    half_life_horizon = np.nan
    half_life_bucket = "invalid"
    if peak_mean > 0:
        after_peak = usable[usable["horizon_days"] >= peak_horizon].copy()
        half = after_peak[after_peak["mean_signed_return"] <= 0.5 * peak_mean]
        if not half.empty:
            half_life_horizon = int(half.iloc[0]["horizon_days"])
            if half_life_horizon <= 5:
                half_life_bucket = "fast"
            elif half_life_horizon <= 21:
                half_life_bucket = "medium"
            else:
                half_life_bucket = "slow"
        else:
            half_life_bucket = "persistent"

    delayed_peak = bool(
        peak_mean > 0
        and peak_horizon > first_horizon
        and (first_mean <= 0 or peak_mean >= 1.25 * max(first_mean, 1e-12))
    )

    flags: list[str] = []
    if sign_stability < min_sign_stability:
        flags.append("unstable_sign_by_horizon")
    if peak_mean <= 0:
        flags.append("no_positive_decay_peak")
    if delayed_peak:
        flags.append("delayed_peak")
    if half_life_bucket == "fast":
        flags.append("fast_decay")
    if pd.notna(decay_slope_corr) and decay_slope_corr > 0.25:
        flags.append("rising_with_horizon")

    if "unstable_sign_by_horizon" in flags or "no_positive_decay_peak" in flags:
        verdict = "unstable"
    elif delayed_peak:
        verdict = "delayed"
    elif half_life_bucket == "fast":
        verdict = "fast_decay"
    else:
        verdict = "stable"

    return {
        "usable_horizon_count": int(len(usable)),
        "positive_horizon_count": int(positive.sum()),
        "sign_stability_share": sign_stability,
        "peak_horizon_days": peak_horizon,
        "peak_mean_signed_return": peak_mean,
        "first_horizon_days": first_horizon,
        "first_mean_signed_return": first_mean,
        "half_life_horizon_days": half_life_horizon,
        "half_life_bucket": half_life_bucket,
        "delayed_peak": delayed_peak,
        "decay_slope_corr": decay_slope_corr,
        "decay_verdict": verdict,
        "decay_flags": ",".join(flags),
    }


def build_signal_decay_audit(
    candidates: pd.DataFrame,
    cache: pd.DataFrame,
    commodity: str | None = None,
    return_column: str = "residual_return_mktsec_w12m",
    horizons: list[int] | tuple[int, ...] | None = None,
    activation_z: float = 1.5,
    min_event_count: int = 20,
    min_sign_stability: float = 0.67,
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
    missing_horizons = [h for h in requested if h not in available]
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
        ticker, commodity, feature = key
        direction_sign = float(group["_direction_sign"].dropna().iloc[0])
        feature_col = f"feature_z__{feature}"
        base_record: dict[str, object] = {
            "ticker": ticker,
            "commodity": commodity,
            "feature": feature,
            "direction_sign": direction_sign,
            "activation_z": activation_z,
            "return_column": return_column,
            "available_horizons": ",".join(str(h) for h in sorted(available)),
            "missing_horizons": ",".join(str(h) for h in missing_horizons),
        }
        for col in meta_cols:
            if col in group.columns:
                values = group[col].dropna()
                base_record[col] = values.iloc[0] if not values.empty else np.nan

        data = cache[(cache["ticker"].eq(ticker)) & (cache["commodity"].eq(commodity))].copy()
        if data.empty or feature_col not in data.columns:
            record = {**base_record, "decay_verdict": "missing_cache_feature", "decay_flags": "missing_cache_feature"}
            summary_rows.append(record)
            continue
        data[feature_col] = pd.to_numeric(data[feature_col], errors="coerce")
        triggered = data[data[feature_col].abs() >= activation_z].copy()
        if triggered.empty:
            record = {**base_record, "decay_verdict": "no_triggers", "decay_flags": "no_triggers"}
            summary_rows.append(record)
            continue

        candidate_detail: list[dict[str, object]] = []
        for horizon in usable_horizons:
            target_col = available[horizon]
            target = pd.to_numeric(triggered[target_col], errors="coerce")
            side = np.sign(triggered[feature_col]) * direction_sign
            signed_return = side * target
            valid = pd.DataFrame(
                {
                    "date": triggered["date"],
                    "feature_z": triggered[feature_col],
                    "signed_return": signed_return,
                }
            ).replace([np.inf, -np.inf], np.nan).dropna(subset=["signed_return", "feature_z"])
            event_count = int(len(valid))
            non = _nonoverlap(valid["signed_return"], horizon)
            candidate_detail.append(
                {
                    **base_record,
                    "horizon_days": horizon,
                    "target_column": target_col,
                    "event_count": event_count,
                    "nonoverlap_event_count": int(len(non)),
                    "sample_start": valid["date"].min() if event_count else pd.NaT,
                    "sample_end": valid["date"].max() if event_count else pd.NaT,
                    "mean_signed_return": float(valid["signed_return"].mean()) if event_count else np.nan,
                    "median_signed_return": float(valid["signed_return"].median()) if event_count else np.nan,
                    "hit_rate": float((valid["signed_return"] > 0).mean()) if event_count else np.nan,
                    "t_stat": _t_stat(valid["signed_return"]),
                    "nonoverlap_mean_signed_return": float(non.mean()) if len(non) else np.nan,
                    "nonoverlap_hit_rate": float((non > 0).mean()) if len(non) else np.nan,
                    "nonoverlap_t_stat": _t_stat(non),
                }
            )

        detail = pd.DataFrame(candidate_detail)
        detail_rows.extend(candidate_detail)
        summary_rows.append({**base_record, **_decay_summary(detail, min_event_count, min_sign_stability)})

    summary = pd.DataFrame(summary_rows)
    detail = pd.DataFrame(detail_rows)
    if not summary.empty:
        front = [
            "decay_verdict",
            "decay_flags",
            "ticker",
            "commodity",
            "feature",
            "feature_hypothesis_family",
            "direction_sign",
            "peak_horizon_days",
            "half_life_bucket",
            "half_life_horizon_days",
            "delayed_peak",
            "sign_stability_share",
            "peak_mean_signed_return",
            "activation_z",
            "return_column",
            "available_horizons",
            "missing_horizons",
        ]
        cols = [col for col in front if col in summary.columns] + [col for col in summary.columns if col not in front]
        summary = summary[cols].sort_values(["decay_verdict", "ticker", "commodity", "feature"]).reset_index(drop=True)
    return summary, detail


def build_signal_decay_audit_from_paths(
    candidates_path: Path,
    cache_path: Path,
    output_path: Path,
    detail_output_path: Path | None = None,
    commodity: str | None = None,
    return_column: str = "residual_return_mktsec_w12m",
    horizons: list[int] | tuple[int, ...] | None = None,
    activation_z: float = 1.5,
    min_event_count: int = 20,
    min_sign_stability: float = 0.67,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    summary, detail = build_signal_decay_audit(
        candidates=load_frame(candidates_path),
        cache=load_frame(cache_path),
        commodity=commodity,
        return_column=return_column,
        horizons=horizons,
        activation_z=activation_z,
        min_event_count=min_event_count,
        min_sign_stability=min_sign_stability,
    )
    _write_frame(summary, output_path)
    if detail_output_path is not None:
        _write_frame(detail, detail_output_path)
    return summary, detail
