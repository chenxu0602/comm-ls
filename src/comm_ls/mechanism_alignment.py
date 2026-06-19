from __future__ import annotations

from math import erf, sqrt
from pathlib import Path

import numpy as np
import pandas as pd

from comm_ls.reaction import load_frame


FEATURE_FAMILY_TO_STATE_FAMILY = {
    "curve_carry": {"curve_structure", "curve_change"},
    "term_structure_regime": {"curve_structure", "curve_change"},
    "price_momentum": {"price_momentum"},
    "price_regime": {"price_regime"},
    "volatility": {"volatility"},
    "volatility_shock": {"volatility"},
    "participation": {"participation"},
}


def _write_frame(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix == ".parquet":
        df.to_parquet(output_path, index=False)
    elif output_path.suffix == ".csv":
        df.to_csv(output_path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")


def _matrix_files(matrix_dir: Path, commodity: str) -> list[Path]:
    return sorted(matrix_dir.glob(f"{commodity.upper()}-Features-*-*.csv"))


def _quarter_for_date(value: object) -> str:
    period = pd.Timestamp(value).to_period("Q")
    return f"{period.year}-Q{period.quarter}"


def _normal_cdf(value: float) -> float:
    if not np.isfinite(value):
        return np.nan
    return 0.5 * (1.0 + erf(value / sqrt(2.0)))


def _sign_confidence(t_stat: float) -> float:
    if not np.isfinite(t_stat):
        return 0.5
    return float(_normal_cdf(abs(t_stat)))


def _load_matrix_rows(
    matrix_dir: Path,
    commodity: str,
    tickers: set[str],
    target_return_column: str,
    horizon_days: set[int] | None,
    lookback_years: set[int] | None,
    quarters: set[str] | None,
) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for path in _matrix_files(matrix_dir, commodity):
        matrix = pd.read_csv(path)
        if matrix.empty:
            continue
        rows = matrix[
            matrix["commodity"].astype(str).str.upper().str.strip().eq(commodity)
            & matrix["ticker"].astype(str).str.upper().str.strip().isin(tickers)
            & matrix["target_return_column"].astype(str).eq(target_return_column)
        ].copy()
        if horizon_days is not None:
            rows = rows[pd.to_numeric(rows["horizon_days"], errors="coerce").isin(horizon_days)].copy()
        if lookback_years is not None:
            rows = rows[pd.to_numeric(rows["lookback_years"], errors="coerce").isin(lookback_years)].copy()
        if quarters is not None:
            rows = rows[rows["quarter"].astype(str).isin(quarters)].copy()
        if rows.empty:
            continue
        rows["source_matrix_path"] = str(path)
        frames.append(rows)
    if not frames:
        return pd.DataFrame()
    out = pd.concat(frames, ignore_index=True)
    out["commodity"] = out["commodity"].astype(str).str.upper().str.strip()
    out["ticker"] = out["ticker"].astype(str).str.upper().str.strip()
    out["quarter"] = out["quarter"].astype(str)
    out["feature"] = out["feature"].astype(str).str.strip()
    out["feature_family"] = out["feature_family"].astype(str).str.strip()
    numeric_cols = [
        "horizon_days",
        "lookback_years",
        "direction_sign",
        "nonoverlap_t_stat",
        "nonoverlap_abs_t_stat",
        "nonoverlap_beta_per_1z",
        "effective_observations",
        "nonoverlap_hit_rate",
    ]
    for col in numeric_cols:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")
    return out.reset_index(drop=True)


def _feature_matches_state(feature_family: str, state_family: str) -> bool:
    allowed = FEATURE_FAMILY_TO_STATE_FAMILY.get(str(feature_family), set())
    return str(state_family) in allowed


def _feature_commodity_direction_sign(feature: object, feature_family: object) -> float:
    name = str(feature).lower().strip()
    family = str(feature_family).lower().strip()
    if "annualized_carry" in name or name in {"carry", "carry_360_perc", "carry_pctile_252d"}:
        return -1.0
    if "backwardation" in name or "spread" in name:
        return 1.0
    if name.startswith("front_price_low_"):
        return -1.0
    if name.startswith("front_price_high_"):
        return 1.0
    if family == "price_momentum" or name.startswith("ret_") or "ret_accel" in name or "breakout" in name:
        return 1.0
    if family in {"volatility", "volatility_shock", "participation"}:
        return 0.0
    return 0.0


def _alignment_verdict(row: pd.Series, min_alignment_probability: float, review_band: float) -> str:
    if row["mechanism_verdict"] == "block":
        return "block"
    if int(row["aligned_observation_count"]) == 0:
        return "block"
    if float(row["mean_mechanism_alignment_probability"]) >= min_alignment_probability:
        if row["mechanism_verdict"] == "pass":
            return "pass"
        return "review"
    if float(row["mean_mechanism_alignment_probability"]) >= review_band:
        return "review"
    return "conflict"


def build_mechanism_alignment_audit(
    mechanism_tickers: pd.DataFrame,
    matrix_dir: Path,
    commodity: str,
    target_return_column: str = "residual_return_mktsec_w12m",
    horizon_days: list[int] | tuple[int, ...] | None = None,
    lookback_years: list[int] | tuple[int, ...] | None = None,
    min_alignment_probability: float = 0.67,
    review_band: float = 0.55,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if mechanism_tickers.empty:
        return pd.DataFrame(), pd.DataFrame()
    commodity = commodity.upper().strip()
    mech = mechanism_tickers.copy()
    required = {
        "date",
        "commodity",
        "ticker",
        "mechanism_state",
        "state_family",
        "expected_ticker_response_sign",
        "mechanism_verdict",
    }
    missing = required.difference(mech.columns)
    if missing:
        raise ValueError(f"mechanism tickers is missing required columns: {sorted(missing)}")

    mech["commodity"] = mech["commodity"].astype(str).str.upper().str.strip()
    mech = mech[mech["commodity"].eq(commodity)].copy()
    mech["ticker"] = mech["ticker"].astype(str).str.upper().str.strip()
    mech = mech[mech["ticker"].notna() & mech["ticker"].ne("")]
    mech["date"] = pd.to_datetime(mech["date"], utc=False)
    mech["quarter"] = mech["date"].map(_quarter_for_date)
    mech["expected_ticker_response_sign"] = pd.to_numeric(
        mech["expected_ticker_response_sign"],
        errors="coerce",
    )
    mech = mech[mech["expected_ticker_response_sign"].notna() & mech["expected_ticker_response_sign"].ne(0)].copy()
    if mech.empty:
        return pd.DataFrame(), pd.DataFrame()

    horizons = set(horizon_days) if horizon_days is not None else None
    lookbacks = set(lookback_years) if lookback_years is not None else None
    matrix = _load_matrix_rows(
        matrix_dir=matrix_dir,
        commodity=commodity,
        tickers=set(mech["ticker"].dropna().unique()),
        target_return_column=target_return_column,
        horizon_days=horizons,
        lookback_years=lookbacks,
        quarters=set(mech["quarter"].dropna().unique()),
    )
    if matrix.empty:
        return pd.DataFrame(), pd.DataFrame()

    detail = mech.merge(
        matrix,
        on=["commodity", "ticker", "quarter"],
        how="inner",
        suffixes=("_mechanism", "_matrix"),
    )
    if detail.empty:
        return pd.DataFrame(), pd.DataFrame()
    detail["feature_state_family_match"] = detail.apply(
        lambda row: _feature_matches_state(row["feature_family"], row["state_family"]),
        axis=1,
    )
    detail = detail[detail["feature_state_family_match"]].copy()
    if detail.empty:
        return pd.DataFrame(), pd.DataFrame()

    detail["empirical_direction_sign"] = pd.to_numeric(detail["direction_sign"], errors="coerce")
    detail["feature_commodity_direction_sign"] = detail.apply(
        lambda row: _feature_commodity_direction_sign(row["feature"], row["feature_family"]),
        axis=1,
    )
    detail["expected_feature_response_sign"] = np.sign(
        detail["feature_commodity_direction_sign"] * detail["expected_prior_sign"]
    )
    detail = detail[detail["expected_feature_response_sign"].ne(0)].copy()
    if detail.empty:
        return pd.DataFrame(), pd.DataFrame()
    detail["empirical_sign_confidence"] = detail["nonoverlap_t_stat"].map(_sign_confidence)
    detail["empirical_positive_probability"] = np.where(
        detail["empirical_direction_sign"].gt(0),
        detail["empirical_sign_confidence"],
        1.0 - detail["empirical_sign_confidence"],
    )
    mechanism_positive = detail["expected_feature_response_sign"].gt(0)
    detail["mechanism_alignment_probability"] = np.where(
        mechanism_positive,
        detail["empirical_positive_probability"],
        1.0 - detail["empirical_positive_probability"],
    )
    detail["mechanism_alignment_sign"] = np.sign(
        detail["expected_feature_response_sign"] * detail["empirical_direction_sign"]
    )
    detail["mechanism_alignment_flag"] = np.select(
        [
            detail["mechanism_alignment_probability"].ge(min_alignment_probability),
            detail["mechanism_alignment_probability"].ge(review_band),
        ],
        ["aligned", "weak"],
        default="conflict",
    )

    group_cols = [
        "commodity",
        "quarter",
        "ticker",
        "mechanism_state",
        "state_family",
        "transmission_channel",
        "exposure_role",
    ]
    summary = (
        detail.groupby(group_cols, dropna=False)
        .agg(
            mechanism_verdict=("mechanism_verdict", "first"),
            expected_ticker_response_sign=("expected_ticker_response_sign", "first"),
            expected_feature_response_sign=("expected_feature_response_sign", "mean"),
            aligned_observation_count=("mechanism_alignment_probability", "count"),
            aligned_feature_count=("feature", "nunique"),
            mean_mechanism_alignment_probability=("mechanism_alignment_probability", "mean"),
            min_mechanism_alignment_probability=("mechanism_alignment_probability", "min"),
            aligned_share=("mechanism_alignment_sign", lambda s: float((s > 0).mean())),
            conflict_share=("mechanism_alignment_sign", lambda s: float((s < 0).mean())),
            mean_empirical_sign_confidence=("empirical_sign_confidence", "mean"),
            mean_effective_observations=("effective_observations", "mean"),
            strongest_abs_t=("nonoverlap_abs_t_stat", "max"),
        )
        .reset_index()
    )
    summary["mechanism_alignment_verdict"] = summary.apply(
        _alignment_verdict,
        axis=1,
        min_alignment_probability=min_alignment_probability,
        review_band=review_band,
    )
    summary["mechanism_alignment_flags"] = ""
    summary.loc[summary["aligned_observation_count"].eq(0), "mechanism_alignment_flags"] += "no_aligned_features,"
    summary.loc[summary["conflict_share"].gt(0.5), "mechanism_alignment_flags"] += "mostly_conflicting_signs,"
    summary.loc[
        summary["mean_mechanism_alignment_probability"].lt(review_band),
        "mechanism_alignment_flags",
    ] += "low_alignment_probability,"
    summary.loc[
        summary["mean_mechanism_alignment_probability"].between(review_band, min_alignment_probability, inclusive="left"),
        "mechanism_alignment_flags",
    ] += "weak_alignment_probability,"
    summary.loc[summary["mechanism_verdict"].ne("pass"), "mechanism_alignment_flags"] += "mechanism_not_pass,"
    summary["mechanism_alignment_flags"] = summary["mechanism_alignment_flags"].str.rstrip(",").replace("", np.nan)

    summary_front = [
        "mechanism_alignment_verdict",
        "mechanism_alignment_flags",
        "commodity",
        "quarter",
        "ticker",
        "mechanism_state",
        "state_family",
        "transmission_channel",
        "exposure_role",
        "expected_ticker_response_sign",
        "expected_feature_response_sign",
        "mean_mechanism_alignment_probability",
        "aligned_share",
        "conflict_share",
        "aligned_feature_count",
        "aligned_observation_count",
    ]
    detail_front = [
        "mechanism_alignment_flag",
        "mechanism_alignment_probability",
        "commodity",
        "quarter",
        "ticker",
        "mechanism_state",
        "state_family",
        "feature",
        "feature_family",
        "target_return_column",
        "horizon_days",
        "lookback_years",
        "expected_ticker_response_sign",
        "feature_commodity_direction_sign",
        "expected_feature_response_sign",
        "empirical_direction_sign",
        "empirical_positive_probability",
        "empirical_sign_confidence",
        "nonoverlap_t_stat",
        "effective_observations",
    ]
    return (
        summary[[col for col in summary_front if col in summary.columns] + [col for col in summary.columns if col not in summary_front]]
        .sort_values(["mechanism_alignment_verdict", "quarter", "ticker", "mechanism_state"])
        .reset_index(drop=True),
        detail[[col for col in detail_front if col in detail.columns] + [col for col in detail.columns if col not in detail_front]]
        .sort_values(["quarter", "ticker", "mechanism_state", "feature", "horizon_days", "lookback_years"])
        .reset_index(drop=True),
    )


def build_mechanism_alignment_audit_from_paths(
    mechanism_tickers_path: Path,
    matrix_dir: Path,
    output_path: Path,
    detail_output_path: Path | None = None,
    commodity: str = "CL",
    target_return_column: str = "residual_return_mktsec_w12m",
    horizon_days: list[int] | tuple[int, ...] | None = None,
    lookback_years: list[int] | tuple[int, ...] | None = None,
    min_alignment_probability: float = 0.67,
    review_band: float = 0.55,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    summary, detail = build_mechanism_alignment_audit(
        mechanism_tickers=load_frame(mechanism_tickers_path),
        matrix_dir=matrix_dir,
        commodity=commodity,
        target_return_column=target_return_column,
        horizon_days=horizon_days,
        lookback_years=lookback_years,
        min_alignment_probability=min_alignment_probability,
        review_band=review_band,
    )
    _write_frame(summary, output_path)
    if detail_output_path is not None:
        _write_frame(detail, detail_output_path)
    return summary, detail
