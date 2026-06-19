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



def _extract_signed_returns(
    cache: pd.DataFrame,
    ticker: str,
    commodity: str,
    feature: str,
    direction_sign: float,
    return_column: str,
    horizon: int,
    activation_z: float,
) -> pd.DataFrame:
    data = cache[
        (cache["ticker"].astype(str).eq(ticker))
        & (cache["commodity"].astype(str).eq(commodity))
    ].copy()
    if data.empty:
        return pd.DataFrame()

    feature_col = f"feature_z__{feature}"
    if feature_col not in data.columns:
        return pd.DataFrame()

    available = _available_horizons(cache, return_column)
    if horizon not in available:
        return pd.DataFrame()
    target_col = available[horizon]

    data["date"] = pd.to_datetime(data["date"], utc=False)
    data[feature_col] = pd.to_numeric(data[feature_col], errors="coerce")
    data[target_col] = pd.to_numeric(data[target_col], errors="coerce")

    triggered = data[data[feature_col].abs() >= activation_z].copy()
    if triggered.empty:
        return pd.DataFrame()

    side = np.sign(triggered[feature_col]) * direction_sign
    triggered["signed_return"] = side * triggered[target_col]
    triggered = triggered.replace([np.inf, -np.inf], np.nan).dropna(subset=["signed_return"])
    triggered["year"] = pd.to_datetime(triggered["date"], utc=False).dt.year

    triggered = triggered.sort_values("date").reset_index(drop=True)
    keep = []
    last_end = pd.Timestamp.min
    target_end_col = f"target_end_{horizon}d"
    target_end = (
        pd.to_datetime(triggered[target_end_col], utc=False)
        if target_end_col in triggered.columns
        else triggered["date"] + pd.Timedelta(days=horizon)
    )
    for i, (_, row) in enumerate(triggered.iterrows()):
        if row["date"] <= last_end:
            continue
        keep.append(i)
        last_end = target_end.iloc[i] if target_end_col in triggered.columns else row["date"] + pd.Timedelta(days=horizon)

    return triggered.iloc[keep].reset_index(drop=True)


def _year_stability_summary(
    signed_returns: pd.DataFrame,
    horizon: int,
    min_event_count: int,
    max_concentration: float,
    min_loyo_abs_t: float,
) -> dict[str, object]:
    if signed_returns.empty:
        return {
            "total_events": 0,
            "nonoverlap_events": 0,
            "year_count": 0,
            "year_stability_verdict": "insufficient_events",
            "year_stability_flags": "insufficient_events",
        }

    years = sorted(signed_returns["year"].unique())
    if len(years) < 2:
        return {
            "total_events": int(len(signed_returns)),
            "nonoverlap_events": int(len(signed_returns)),
            "year_count": int(len(years)),
            "year_stability_verdict": "insufficient_years",
            "year_stability_flags": "insufficient_years",
        }

    non = pd.to_numeric(signed_returns["signed_return"], errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    full_nonoverlap_events = int(len(non))
    full_mean = float(non.mean())
    full_t = _t_stat(non)
    full_total = float(non.sum())

    loyo_rows: list[dict[str, object]] = []
    for year in years:
        excluded = signed_returns[signed_returns["year"] != year]
        non_ex = pd.to_numeric(excluded["signed_return"], errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
        if len(non_ex) < 3:
            loyo_rows.append(
                {
                    "excluded_year": int(year),
                    "removed_events": int((signed_returns["year"] == year).sum()),
                    "holdout_events": int(len(non_ex)),
                    "holdout_mean_return": float(non_ex.mean()),
                    "holdout_total_return": float(non_ex.sum()),
                    "holdout_t_stat": np.nan,
                    "delta_total_return_vs_full": float(non_ex.sum() - full_total),
                }
            )
        else:
            loyo_rows.append(
                {
                    "excluded_year": int(year),
                    "removed_events": int((signed_returns["year"] == year).sum()),
                    "holdout_events": int(len(non_ex)),
                    "holdout_mean_return": float(non_ex.mean()),
                    "holdout_total_return": float(non_ex.sum()),
                    "holdout_t_stat": _t_stat(non_ex),
                    "delta_total_return_vs_full": float(non_ex.sum() - full_total),
                }
            )

    loyo = pd.DataFrame(loyo_rows)
    loyo_valid = loyo[loyo["holdout_t_stat"].notna()].copy()

    yearly = signed_returns.groupby("year").apply(
        lambda g: pd.to_numeric(g["signed_return"], errors="coerce").replace([np.inf, -np.inf], np.nan).dropna().sum(), include_groups=False
    )
    yearly = yearly[yearly.notna()]
    yearly_share = (yearly / full_total) if abs(full_total) > 1e-12 else yearly * 0.0
    max_year = yearly.idxmax() if not yearly.empty else None
    min_year = yearly.idxmin() if not yearly.empty else None
    max_share = float(yearly_share.max()) if not yearly.empty else np.nan
    min_share = float(yearly_share.min()) if not yearly.empty else np.nan

    if loyo_valid.empty:
        sign_flip = False
        min_loyo_t = np.nan
        min_loyo_t_year = None
        sign_flip_year = None
    else:
        full_sign = np.sign(full_mean) if full_mean != 0 else 0
        flip_mask = np.sign(loyo_valid["holdout_mean_return"]) != full_sign
        sign_flip = bool(flip_mask.any())
        sign_flip_year = int(loyo_valid.loc[flip_mask, "excluded_year"].iloc[0]) if sign_flip else None
        min_loyo_t = float(loyo_valid["holdout_t_stat"].min())
        min_loyo_t_year = int(loyo_valid.loc[loyo_valid["holdout_t_stat"].idxmin(), "excluded_year"])

    flags: list[str] = []
    if full_nonoverlap_events < min_event_count:
        flags.append("insufficient_events")
    if len(years) < 3:
        flags.append("insufficient_years")
    if pd.notna(max_share) and max_share >= max_concentration:
        flags.append(f"concentrated_best_year_{max_share:.2f}")
    if pd.notna(min_share) and abs(min_share) >= max_concentration:
        flags.append(f"concentrated_worst_year_{min_share:.2f}")
    if sign_flip:
        flags.append(f"sign_flip_without_{sign_flip_year}")
    if pd.notna(min_loyo_t) and abs(min_loyo_t) < min_loyo_abs_t:
        flags.append(f"fragile_loyo_t_{min_loyo_t:.2f}")

    if "insufficient_events" in flags:
        verdict = "insufficient_events"
    elif "insufficient_years" in flags:
        verdict = "insufficient_years"
    elif "sign_flip_without" in ",".join(flags) or "fragile_loyo_t" in ",".join(flags):
        verdict = "fragile"
    elif "concentrated_best_year" in ",".join(flags):
        verdict = "concentrated"
    else:
        verdict = "stable"

    return {
        "total_events": int(len(signed_returns)),
        "nonoverlap_events": full_nonoverlap_events,
        "year_count": int(len(years)),
        "full_mean_return": full_mean,
        "full_total_return": full_total,
        "full_t_stat": full_t,
        "full_hit_rate": float((non > 0).mean()),
        "best_year": int(max_year) if max_year is not None else np.nan,
        "best_year_share": float(max_share) if pd.notna(max_share) else np.nan,
        "worst_year": int(min_year) if min_year is not None else np.nan,
        "worst_year_share": float(min_share) if pd.notna(min_share) else np.nan,
        "min_loyo_t_stat": min_loyo_t,
        "min_loyo_t_stat_year": min_loyo_t_year,
        "sign_flips_without_year": sign_flip,
        "sign_flip_year": sign_flip_year,
        "year_contributions": ",".join(
            f"{int(y)}:{float(s):.3f}" for y, s in zip(yearly.index, yearly_share)
        ) if not yearly.empty else "",
        "year_stability_verdict": verdict,
        "year_stability_flags": ",".join(flags) if flags else "",
    }


def build_year_stability_audit(
    candidates: pd.DataFrame,
    cache: pd.DataFrame,
    commodity: str | None = None,
    return_column: str = "residual_return_mktsec_w12m",
    horizon: int = 21,
    activation_z: float = 1.5,
    min_event_count: int = 20,
    max_concentration: float = 0.30,
    min_loyo_abs_t: float = 1.5,
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

    summary_rows: list[dict[str, object]] = []
    detail_rows: list[dict[str, object]] = []
    meta_cols = [
        "theme",
        "role",
        "region",
        "feature_family",
        "feature_hypothesis_family",
        "preferred_horizon",
        "exposure_role",
        "confidence",
        "selection_verdict",
        "selection_score",
    ]
    for key, group in cand.groupby(["ticker", "commodity", "feature"], dropna=False, sort=True):
        ticker, commodity_code, feature = key
        direction_sign = float(group["_direction_sign"].dropna().iloc[0])
        base_record: dict[str, object] = {
            "ticker": ticker,
            "commodity": commodity_code,
            "feature": feature,
            "direction_sign": direction_sign,
            "activation_z": activation_z,
            "return_column": return_column,
            "horizon": horizon,
        }
        for col in meta_cols:
            if col in group.columns:
                values = group[col].dropna()
                base_record[col] = values.iloc[0] if not values.empty else np.nan

        signed = _extract_signed_returns(
            cache=cache,
            ticker=ticker,
            commodity=commodity_code,
            feature=feature,
            direction_sign=direction_sign,
            return_column=return_column,
            horizon=horizon,
            activation_z=activation_z,
        )

        if signed.empty:
            record = {
                **base_record,
                "year_stability_verdict": "no_triggers",
                "year_stability_flags": "no_triggers",
                "total_events": 0,
                "nonoverlap_events": 0,
                "year_count": 0,
            }
            summary_rows.append(record)
            continue

        summary = _year_stability_summary(
            signed_returns=signed,
            horizon=horizon,
            min_event_count=min_event_count,
            max_concentration=max_concentration,
            min_loyo_abs_t=min_loyo_abs_t,
        )
        summary_rows.append({**base_record, **summary})

        years = sorted(signed["year"].unique())
        for year in years:
            year_data = signed[signed["year"] == year]
            non_y = pd.to_numeric(year_data["signed_return"], errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
            full_excluding = signed[signed["year"] != year]
            non_ex = pd.to_numeric(full_excluding["signed_return"], errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
            detail_rows.append(
                {
                    **base_record,
                    "year": int(year),
                    "events_in_year": int(len(year_data)),
                    "nonoverlap_events_in_year": int(len(non_y)),
                    "year_sum_return": float(non_y.sum()) if len(non_y) else np.nan,
                    "year_mean_return": float(non_y.mean()) if len(non_y) else np.nan,
                    "year_t_stat": _t_stat(non_y),
                    "loyo_nonoverlap_events": int(len(non_ex)),
                    "loyo_mean_return": float(non_ex.mean()) if len(non_ex) else np.nan,
                    "loyo_total_return": float(non_ex.sum()) if len(non_ex) else np.nan,
                    "loyo_t_stat": _t_stat(non_ex),
                }
            )

    summary = pd.DataFrame(summary_rows)
    detail = pd.DataFrame(detail_rows)
    if not summary.empty:
        front = [
            "year_stability_verdict",
            "year_stability_flags",
            "ticker",
            "commodity",
            "feature",
            "feature_hypothesis_family",
            "direction_sign",
            "horizon",
            "full_t_stat",
            "min_loyo_t_stat",
            "min_loyo_t_stat_year",
            "sign_flips_without_year",
            "best_year",
            "best_year_share",
            "worst_year",
            "worst_year_share",
            "nonoverlap_events",
            "full_mean_return",
            "full_hit_rate",
            "year_count",
            "year_contributions",
            "activation_z",
            "return_column",
        ]
        cols = [col for col in front if col in summary.columns] + [col for col in summary.columns if col not in front]
        summary = summary[cols].sort_values(
            ["year_stability_verdict", "ticker", "commodity", "feature"]
        ).reset_index(drop=True)
    if not detail.empty:
        detail_front = [
            "ticker",
            "commodity",
            "feature",
            "year",
            "events_in_year",
            "year_sum_return",
            "year_mean_return",
            "year_t_stat",
            "loyo_t_stat",
            "loyo_mean_return",
        ]
        detail = detail[detail_front + [col for col in detail.columns if col not in detail_front]].sort_values(
            ["ticker", "commodity", "feature", "year"]
        ).reset_index(drop=True)
    return summary, detail


def build_year_stability_audit_from_paths(
    candidates_path: Path,
    cache_path: Path,
    output_path: Path,
    detail_output_path: Path | None = None,
    commodity: str | None = None,
    return_column: str = "residual_return_mktsec_w12m",
    horizon: int = 21,
    activation_z: float = 1.5,
    min_event_count: int = 20,
    max_concentration: float = 0.30,
    min_loyo_abs_t: float = 1.5,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    candidates = load_frame(candidates_path)
    cache = load_frame(cache_path)
    summary, detail = build_year_stability_audit(
        candidates=candidates,
        cache=cache,
        commodity=commodity,
        return_column=return_column,
        horizon=horizon,
        activation_z=activation_z,
        min_event_count=min_event_count,
        max_concentration=max_concentration,
        min_loyo_abs_t=min_loyo_abs_t,
    )
    _write_frame(summary, output_path)
    if detail_output_path is not None:
        _write_frame(detail, detail_output_path)
    return summary, detail

