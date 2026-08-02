from __future__ import annotations

from pathlib import Path

import pandas as pd


FUNDAMENTAL_EXPOSURE_COLUMNS = (
    "ticker",
    "effective_start_date",
    "effective_end_date",
    "known_date",
    "primary_commodity",
    "revenue_share_range",
    "profit_share_range",
    "upstream_downstream_integrated",
    "production_region",
    "pricing_benchmark",
    "pricing_lag",
    "hedge_ratio_range",
    "hedge_tenor",
    "cost_curve_bucket",
    "cost_currency",
    "byproduct_exposure",
    "freight_terms",
    "structural_break",
    "source_filing",
    "confidence",
)

SHARE_RANGE_VALUES = {
    "none",
    "<25%",
    "25-50%",
    "50-75%",
    "75-100%",
    "unknown",
    "not_disclosed",
}
BUSINESS_MODEL_VALUES = {
    "upstream",
    "downstream",
    "integrated",
    "mixed",
    "service",
    "consumer",
    "unknown",
}
PRICING_LAG_VALUES = {
    "spot",
    "0-1m",
    "1-3m",
    "3-12m",
    ">12m",
    "mixed",
    "unknown",
}
HEDGE_TENOR_VALUES = {
    "none",
    "<3m",
    "3-12m",
    "1-3y",
    ">3y",
    "mixed",
    "unknown",
}
COST_CURVE_VALUES = {"low", "mid", "high", "mixed", "not_applicable", "unknown"}
FREIGHT_TERM_VALUES = {
    "seller",
    "buyer",
    "mixed",
    "not_applicable",
    "unknown",
}
CONFIDENCE_VALUES = {"low", "medium", "high"}

EXPOSURE_PURITY_BY_SHARE_RANGE = {
    "none": "none",
    "<25%": "secondary",
    "25-50%": "diversified",
    "50-75%": "concentrated",
    "75-100%": "pure_play",
    "unknown": "unknown",
    "not_disclosed": "unknown",
}

HOLDING_PERIOD_PRIOR_BY_PRICING_LAG = {
    "spot": "short",
    "0-1m": "short",
    "1-3m": "medium",
    "3-12m": "long",
    ">12m": "long",
    "mixed": "unspecified",
    "unknown": "unspecified",
}


def _normalize_text(frame: pd.DataFrame) -> pd.DataFrame:
    out = frame.copy()
    for column in FUNDAMENTAL_EXPOSURE_COLUMNS:
        if column not in out.columns:
            continue
        if column in {"effective_start_date", "effective_end_date", "known_date"}:
            continue
        out[column] = out[column].fillna("").astype(str).str.strip()
    out["ticker"] = out["ticker"].str.upper()
    out["primary_commodity"] = out["primary_commodity"].str.upper()
    for column in (
        "revenue_share_range",
        "profit_share_range",
        "upstream_downstream_integrated",
        "pricing_lag",
        "hedge_ratio_range",
        "hedge_tenor",
        "cost_curve_bucket",
        "freight_terms",
        "confidence",
    ):
        out[column] = out[column].str.lower()
    return out


def _validate_allowed(frame: pd.DataFrame, column: str, allowed: set[str]) -> None:
    invalid = sorted(set(frame[column]).difference(allowed))
    if invalid:
        raise ValueError(
            f"fundamental exposure registry has invalid {column} values: {invalid}; "
            f"allowed={sorted(allowed)}"
        )


def _validate_no_overlaps(frame: pd.DataFrame) -> None:
    far_future = pd.Timestamp.max.normalize()
    for ticker, group in frame.groupby("ticker", sort=True):
        ordered = group.sort_values(["effective_start_date", "known_date"])
        previous_end: pd.Timestamp | None = None
        for row in ordered.itertuples(index=False):
            start = row.effective_start_date
            end = row.effective_end_date if pd.notna(row.effective_end_date) else far_future
            if previous_end is not None and start <= previous_end:
                raise ValueError(
                    f"fundamental exposure registry has overlapping effective periods for {ticker}: "
                    f"{start.date()} starts on or before prior end {previous_end.date()}"
                )
            previous_end = end


def validate_fundamental_exposure_registry(frame: pd.DataFrame) -> pd.DataFrame:
    missing = sorted(set(FUNDAMENTAL_EXPOSURE_COLUMNS).difference(frame.columns))
    if missing:
        raise ValueError(f"fundamental exposure registry is missing columns: {missing}")

    out = _normalize_text(frame[list(FUNDAMENTAL_EXPOSURE_COLUMNS)])
    for column in ("effective_start_date", "effective_end_date", "known_date"):
        out[column] = pd.to_datetime(out[column], errors="coerce").dt.normalize()

    required_text = (
        "ticker",
        "primary_commodity",
        "production_region",
        "pricing_benchmark",
        "cost_currency",
        "byproduct_exposure",
        "structural_break",
        "source_filing",
    )
    for column in required_text:
        if out[column].eq("").any():
            rows = out.index[out[column].eq("")].tolist()
            raise ValueError(f"fundamental exposure registry requires {column}; rows={rows}")

    for column in ("effective_start_date", "known_date"):
        if out[column].isna().any():
            rows = out.index[out[column].isna()].tolist()
            raise ValueError(f"fundamental exposure registry requires valid {column}; rows={rows}")

    invalid_period = out["effective_end_date"].notna() & out["effective_start_date"].gt(
        out["effective_end_date"]
    )
    if invalid_period.any():
        raise ValueError(
            "fundamental exposure registry has effective_start_date after "
            f"effective_end_date; rows={out.index[invalid_period].tolist()}"
        )
    unusable = out["effective_end_date"].notna() & out["known_date"].gt(
        out["effective_end_date"]
    )
    if unusable.any():
        raise ValueError(
            "fundamental exposure registry rows become known only after their effective "
            f"period ended; rows={out.index[unusable].tolist()}"
        )

    _validate_allowed(out, "revenue_share_range", SHARE_RANGE_VALUES)
    _validate_allowed(out, "profit_share_range", SHARE_RANGE_VALUES)
    _validate_allowed(out, "upstream_downstream_integrated", BUSINESS_MODEL_VALUES)
    _validate_allowed(out, "pricing_lag", PRICING_LAG_VALUES)
    _validate_allowed(out, "hedge_ratio_range", SHARE_RANGE_VALUES)
    _validate_allowed(out, "hedge_tenor", HEDGE_TENOR_VALUES)
    _validate_allowed(out, "cost_curve_bucket", COST_CURVE_VALUES)
    _validate_allowed(out, "freight_terms", FREIGHT_TERM_VALUES)
    _validate_allowed(out, "confidence", CONFIDENCE_VALUES)

    if out.duplicated(["ticker", "effective_start_date", "known_date"]).any():
        raise ValueError("fundamental exposure registry contains duplicate profile rows")
    _validate_no_overlaps(out)
    return out.sort_values(["ticker", "effective_start_date", "known_date"]).reset_index(
        drop=True
    )


def load_fundamental_exposure_registry(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return validate_fundamental_exposure_registry(pd.read_csv(path, dtype=str))


def active_fundamental_exposure_as_of(
    registry: pd.DataFrame,
    as_of_date: str | pd.Timestamp,
) -> pd.DataFrame:
    validated = validate_fundamental_exposure_registry(registry)
    as_of = pd.Timestamp(as_of_date).normalize()
    active = validated[
        validated["known_date"].le(as_of)
        & validated["effective_start_date"].le(as_of)
        & (
            validated["effective_end_date"].isna()
            | validated["effective_end_date"].ge(as_of)
        )
    ].copy()
    return active.sort_values(["ticker", "known_date"]).drop_duplicates(
        "ticker", keep="last"
    ).reset_index(drop=True)


def derive_fundamental_exposure_diagnostics(
    active_registry: pd.DataFrame,
) -> pd.DataFrame:
    """Derive non-alpha grouping and review priors from active profiles."""
    active = validate_fundamental_exposure_registry(active_registry)
    out = active.copy()
    out["exposure_purity_bucket"] = out["revenue_share_range"].map(
        EXPOSURE_PURITY_BY_SHARE_RANGE
    )
    out["structural_peer_group"] = (
        out["primary_commodity"].str.lower()
        + "_"
        + out["exposure_purity_bucket"]
        + "_"
        + out["upstream_downstream_integrated"]
    )
    currency_signature = (
        out["cost_currency"]
        .str.lower()
        .str.replace(";", "_", regex=False)
        .str.replace(" ", "_", regex=False)
    )
    out["regional_cost_peer_group"] = (
        out["structural_peer_group"] + "__" + currency_signature
    )
    out["holding_period_prior"] = out["pricing_lag"].map(
        HOLDING_PERIOD_PRIOR_BY_PRICING_LAG
    )
    uncertain = (
        out["confidence"].eq("low")
        | out["exposure_purity_bucket"].eq("unknown")
        | out["profit_share_range"].isin({"unknown", "not_disclosed"})
    )
    out["profile_gate"] = "eligible_structural_prior"
    out.loc[uncertain, "profile_gate"] = "review_only"
    return out


def audit_fundamental_exposure_registry_from_paths(
    registry_path: Path,
    output_path: Path,
    active_output_path: Path,
    diagnostics_output_path: Path,
    as_of_date: str | pd.Timestamp,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    registry = load_fundamental_exposure_registry(registry_path)
    active = active_fundamental_exposure_as_of(registry, as_of_date)
    diagnostics = derive_fundamental_exposure_diagnostics(active)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    active_output_path.parent.mkdir(parents=True, exist_ok=True)
    diagnostics_output_path.parent.mkdir(parents=True, exist_ok=True)
    registry.to_csv(output_path, index=False)
    active.to_csv(active_output_path, index=False)
    diagnostics.to_csv(diagnostics_output_path, index=False)
    return registry, active, diagnostics
