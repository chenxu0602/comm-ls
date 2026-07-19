from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from comm_ls.reaction import load_frame
from comm_ls.sensitivity import _feature_z_scores, build_stock_sensitivity_registry
from comm_ls.universe import load_seed_universe


def feature_family(feature: str) -> str:
    if "ratio_ma_gap" in feature:
        return "relative_price_momentum"
    if feature.startswith(("price_volume", "price_oi", "volume", "oi")):
        return "participation"
    if (
        "realized_vol" in feature
        or feature.startswith("vol_")
        or "atr" in feature
        or "abs_ret" in feature
        or "large_move" in feature
    ):
        return "volatility_shock"
    if "regime" in feature or "backwardation" in feature or "contango" in feature:
        return "curve_regime"
    if (
        "calendar_dec_log_ret" in feature
        or "next_jun_log_ret" in feature
        or "liquid_deferred_log_ret" in feature
    ):
        return "fixed_contract_return"
    if "carry" in feature or "spread" in feature:
        return "curve_carry"
    if "ret" in feature or "breakout" in feature or "drawdown" in feature or "up_days" in feature:
        return "price_momentum"
    return "other"


def feature_hypothesis_family(feature: str) -> str:
    """Group related feature variants into one research hypothesis family."""
    name = str(feature).removeprefix("feature_z__").strip().lower()

    def _curve_anchor(value: str) -> str:
        for anchor in [
            "front_second",
            "front_third",
            "calendar_dec",
            "next_jun",
            "liquid_deferred",
            "activity_deferred",
        ]:
            if value.startswith(anchor):
                return anchor
        return "generic"

    def _change_bucket(value: str) -> str:
        return "change" if "_chg_" in value or value.endswith("_chg") else "level"

    if "ratio_ma_gap" in name:
        construction = "chained" if name.endswith("_chained") else "raw"
        return f"cross_commodity_ratio_momentum:hg_gc:{construction}"
    if "annualized_carry" in name or "backwardation_steepness" in name:
        return f"curve_slope:{_curve_anchor(name)}:{_change_bucket(name)}"
    if name in {"carry", "carry_chg_5d", "carry_chg_21d", "carry_pctile_252d"}:
        return f"curve_slope:custom:{_change_bucket(name)}"
    if name in {"front_second_spread", "front_third_spread"} or name.endswith("_spread"):
        return f"curve_spread:{_curve_anchor(name)}:level"
    if "log_ret" in name:
        return f"deferred_contract_return:{_curve_anchor(name)}:{_change_bucket(name)}"
    if name.startswith(("front_price_high_", "front_price_low_")):
        state = "high" if name.startswith("front_price_high_") else "low"
        return f"front_price_regime:{state}"
    if name.startswith(("realized_vol_", "vol_chg_", "m0_atr_", "abs_ret_")):
        return "volatility_state"
    if name.startswith(("volume_surge", "oi_surge", "price_volume", "price_oi")):
        return "participation_confirmation"
    if name.startswith("ret_accel"):
        return "price_momentum:acceleration"
    if name.startswith(("ret_", "m0_ret", "m1_ret", "m2_ret")):
        return "price_momentum:return"
    if name.startswith(("breakout", "drawdown", "up_days")):
        return "price_momentum:regime"
    return f"{feature_family(name)}:{name}"


def state_hypothesis(feature: str) -> str:
    """Map an observed feature to a deterministic state hypothesis.

    This is intentionally a coarse research label, not a latent model. The goal
    is to group redundant feature projections before promotion review.
    """
    name = str(feature).removeprefix("feature_z__").strip().lower()

    if "ratio_ma_gap" in name:
        return "cross_commodity_relative_value_momentum"
    if name == "days_in_backwardation":
        return "curve_tightness_persistence"
    if name in {"backwardation_regime_change", "term_structure_regime_change"}:
        return "curve_state_transition"
    if "annualized_carry" in name or "backwardation_steepness" in name:
        return "curve_tightness_change" if "_chg_" in name or name.endswith("_chg") else "curve_tightness"
    if "spread" in name or name in {"carry", "carry_pctile_252d"}:
        return "curve_tightness"
    if name.startswith("carry_chg"):
        return "curve_tightness_change"
    if "log_ret" in name:
        return "deferred_contract_momentum"
    if name.startswith("front_price_high_"):
        return "price_pressure_high"
    if name.startswith("front_price_low_"):
        return "price_pressure_low"
    if name.startswith("ret_accel"):
        return "momentum_acceleration"
    if name.startswith("drawdown"):
        return "price_drawdown_state"
    if name.startswith("breakout") or name.startswith("up_days"):
        return "price_breakout_state"
    if name.startswith(("ret_", "m0_ret", "m1_ret", "m2_ret")):
        return "price_momentum_state"
    if name.startswith(("realized_vol_", "vol_chg_", "m0_atr_", "abs_ret_", "large_move")):
        return "volatility_state"
    if name.startswith(("volume_", "volume_surge", "oi_", "oi_surge", "price_volume", "price_oi")):
        return "participation_flow_state"
    return f"observed_feature_state:{feature_family(name)}"


def load_reviewed_features(path: Path) -> pd.DataFrame:
    reviewed = pd.read_csv(path)
    required = {"commodity", "feature", "feature_family", "review_status", "default_enabled"}
    missing = required.difference(reviewed.columns)
    if missing:
        raise ValueError(f"{path} is missing required columns: {sorted(missing)}")
    reviewed = reviewed.copy()
    reviewed["commodity"] = reviewed["commodity"].astype(str).str.upper().str.strip()
    reviewed["feature"] = reviewed["feature"].astype(str).str.strip()
    reviewed["feature_family"] = reviewed["feature_family"].astype(str).str.strip()
    reviewed["default_enabled"] = reviewed["default_enabled"].astype(str).str.lower().isin(
        {"true", "1", "yes", "y"}
    )
    return reviewed


def reviewed_feature_list(
    reviewed: pd.DataFrame,
    commodity: str | None = None,
    enabled_only: bool = True,
) -> list[str]:
    df = reviewed.copy()
    if enabled_only:
        df = df[df["default_enabled"]]
    if commodity is not None:
        keep = commodity.upper().strip()
        df = df[df["commodity"].isin(["ALL", keep])]
    return sorted(df["feature"].dropna().astype(str).unique())


def _read_many(paths: list[Path]) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for path in paths:
        df = load_frame(path)
        df["source_file"] = str(path)
        frames.append(df)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def _sample_priority(samples: pd.Series) -> str:
    sample_names = set(samples.dropna().astype(str))
    for name in ["last_10y", "last_8y", "last_5y", "full_available"]:
        if name in sample_names:
            return name
    non_annual = sorted(name for name in sample_names if "_year_" not in name)
    return non_annual[0] if non_annual else sorted(sample_names)[0]


def build_forecast_audit(
    forecast: pd.DataFrame,
    exposure_map: pd.DataFrame | None = None,
    reviewed_features: pd.DataFrame | None = None,
    aggregate_sample: str | None = None,
    high_abs_t: float = 8.0,
    min_same_direction_share: float = 0.6,
    min_peer_direction_share: float = 0.6,
) -> pd.DataFrame:
    df = forecast.copy()
    if df.empty:
        return df
    df["ticker"] = df["ticker"].astype(str).str.upper().str.strip()
    df["commodity"] = df["commodity"].astype(str).str.upper().str.strip()
    df["feature"] = df["feature"].astype(str).str.strip()
    df["sample"] = df["sample"].astype(str)
    df["t_stat"] = pd.to_numeric(df["t_stat"], errors="coerce")
    df["abs_t_stat"] = df["t_stat"].abs()

    aggregate_sample = aggregate_sample or _sample_priority(df["sample"])
    aggregate = df[df["sample"] == aggregate_sample].copy()
    annual = df[df["sample"].str.contains("_year_", na=False)].copy()
    if aggregate.empty:
        raise ValueError(f"No aggregate rows found for sample={aggregate_sample}")

    family_map: dict[str, str] = {}
    if reviewed_features is not None and not reviewed_features.empty:
        family_map = (
            reviewed_features.drop_duplicates("feature")
            .set_index("feature")["feature_family"]
            .astype(str)
            .to_dict()
        )
    aggregate["feature_family"] = aggregate["feature"].map(family_map).fillna(
        aggregate["feature"].map(feature_family)
    )
    aggregate["feature_hypothesis_family"] = aggregate["feature"].map(feature_hypothesis_family)

    peer_cols = ["ticker", "commodity", "exposure_role", "prior_weight"]
    if exposure_map is not None and not exposure_map.empty:
        exp = exposure_map.copy()
        exp["ticker"] = exp["ticker"].astype(str).str.upper().str.strip()
        exp["commodity"] = exp["commodity"].astype(str).str.upper().str.strip()
        aggregate = aggregate.merge(
            exp[[col for col in peer_cols if col in exp.columns]].drop_duplicates(["ticker", "commodity"]),
            on=["ticker", "commodity"],
            how="left",
        )
    if "exposure_role" not in aggregate.columns:
        aggregate["exposure_role"] = np.nan
    aggregate["peer_group"] = aggregate["exposure_role"].fillna(aggregate.get("role", "unknown")).fillna("unknown")

    keys = ["source_file", "ticker", "commodity", "feature", "horizon_days"]
    annual_summary = pd.DataFrame(columns=keys)
    if not annual.empty:
        annual["year"] = annual["sample"].str.extract(r"year_(\d{4})", expand=False)
        annual["year"] = pd.to_numeric(annual["year"], errors="coerce")
        records: list[dict[str, object]] = []
        for key, group in annual.groupby(keys, dropna=False, sort=False):
            direction = np.sign(group["t_stat"].median())
            if direction == 0:
                direction = np.sign(group["t_stat"].sum())
            records.append(
                {
                    **dict(zip(keys, key, strict=False)),
                    "annual_years": int(group["year"].nunique()),
                    "annual_pos_years": int((group["t_stat"] > 0).sum()),
                    "annual_neg_years": int((group["t_stat"] < 0).sum()),
                    "annual_sig15_pos_years": int((group["t_stat"] >= 1.5).sum()),
                    "annual_sig15_neg_years": int((group["t_stat"] <= -1.5).sum()),
                    "annual_median_t": group["t_stat"].median(),
                    "annual_max_abs_t": group["t_stat"].abs().max(),
                    "annual_direction": direction,
                }
            )
        annual_summary = pd.DataFrame(records)

    out = aggregate.merge(annual_summary, on=keys, how="left")
    agg_direction = np.sign(out["t_stat"]).replace(0, np.nan)
    out["same_direction_years"] = np.where(
        agg_direction >= 0,
        out["annual_pos_years"],
        out["annual_neg_years"],
    )
    out["same_direction_sig15_years"] = np.where(
        agg_direction >= 0,
        out["annual_sig15_pos_years"],
        out["annual_sig15_neg_years"],
    )
    out["same_direction_share"] = out["same_direction_years"] / out["annual_years"]

    horizon_keys = ["source_file", "ticker", "commodity", "feature"]
    horizon = (
        aggregate.assign(direction=np.sign(aggregate["t_stat"]))
        .groupby(horizon_keys, dropna=False)
        .agg(
            horizon_count=("horizon_days", "nunique"),
            horizon_pos=("direction", lambda s: int((s > 0).sum())),
            horizon_neg=("direction", lambda s: int((s < 0).sum())),
            horizon_max_abs_t=("abs_t_stat", "max"),
        )
        .reset_index()
    )
    horizon["horizon_direction_share"] = horizon[["horizon_pos", "horizon_neg"]].max(axis=1) / horizon[
        "horizon_count"
    ]
    out = out.merge(horizon, on=horizon_keys, how="left")

    peer = (
        aggregate.assign(direction=np.sign(aggregate["t_stat"]))
        .groupby(["source_file", "commodity", "feature", "horizon_days", "peer_group"], dropna=False)
        .agg(
            peer_tickers=("ticker", "nunique"),
            peer_pos=("direction", lambda s: int((s > 0).sum())),
            peer_neg=("direction", lambda s: int((s < 0).sum())),
            peer_median_t=("t_stat", "median"),
        )
        .reset_index()
    )
    peer["peer_direction_share"] = peer[["peer_pos", "peer_neg"]].max(axis=1) / peer["peer_tickers"]
    out = out.merge(
        peer,
        on=["source_file", "commodity", "feature", "horizon_days", "peer_group"],
        how="left",
    )

    out["flag_high_t"] = out["abs_t_stat"] >= high_abs_t
    out["flag_weak_annual"] = out["same_direction_share"].fillna(0) < min_same_direction_share
    out["flag_exact_horizon"] = out["horizon_direction_share"].fillna(0) < 2 / 3
    out["flag_weak_peer"] = (out["peer_tickers"].fillna(0) >= 3) & (
        out["peer_direction_share"].fillna(0) < min_peer_direction_share
    )
    out["audit_flags"] = (
        out[["flag_high_t", "flag_weak_annual", "flag_exact_horizon", "flag_weak_peer"]]
        .rename(
            columns={
                "flag_high_t": "high_t",
                "flag_weak_annual": "weak_annual",
                "flag_exact_horizon": "exact_horizon",
                "flag_weak_peer": "weak_peer",
            }
        )
        .apply(lambda row: ",".join([col for col, value in row.items() if bool(value)]), axis=1)
    )
    out["audit_verdict"] = np.select(
        [
            out["flag_weak_annual"] | out["flag_exact_horizon"] | out["flag_weak_peer"],
            out["flag_high_t"],
        ],
        ["review", "high_t_needs_manual_check"],
        default="candidate",
    )

    cols = [
        "source_file",
        "sample",
        "ticker",
        "commodity",
        "peer_group",
        "feature",
        "feature_family",
        "feature_hypothesis_family",
        "horizon_days",
        "observations",
        "t_stat",
        "abs_t_stat",
        "beta_per_1z",
        "hit_rate",
        "top_bottom_quintile_spread",
        "annual_years",
        "same_direction_share",
        "same_direction_sig15_years",
        "horizon_direction_share",
        "peer_tickers",
        "peer_direction_share",
        "peer_median_t",
        "audit_flags",
        "audit_verdict",
    ]
    return out[[col for col in cols if col in out.columns]].sort_values(
        ["audit_verdict", "abs_t_stat"], ascending=[False, False]
    )


def _feature_commodity_direction(feature: str) -> float:
    """Return the commodity-price/tightness direction implied by higher feature values."""
    name = str(feature)
    if name.startswith(("realized_vol_", "vol_chg_", "m0_atr_", "abs_ret_", "large_move")):
        return 1.0
    if "backwardation_steepness" in name:
        return 1.0
    if name == "days_in_backwardation":
        return 1.0
    if name in {"front_second_spread", "front_third_spread"} or name.endswith("_spread"):
        return 1.0
    if "annualized_carry" in name:
        return -1.0
    if name in {"carry", "carry_chg_5d", "carry_chg_21d", "carry_pctile_252d"}:
        return -1.0
    if name.startswith("drawdown"):
        return -1.0
    if (
        "log_ret" in name
        or name.startswith("ret_")
        or name.startswith("m0_ret")
        or name.startswith("m1_ret")
        or name.startswith("m2_ret")
        or name.startswith("breakout")
        or name.startswith("up_days")
    ):
        return 1.0
    return 0.0


def build_sensitivity_falsification_audit(
    matrix: pd.DataFrame,
    exposure_map: pd.DataFrame | None = None,
    min_abs_t: float = 2.0,
    min_nonoverlap_abs_t: float = 1.0,
    min_effective_observations: int = 20,
    max_overlap_inflation: float = 3.0,
    min_hit_rate_edge: float = 0.03,
) -> pd.DataFrame:
    if matrix.empty:
        return matrix.copy()
    out = matrix.copy()
    original_cols = set(out.columns)
    out["ticker"] = out["ticker"].astype(str).str.upper().str.strip()
    out["commodity"] = out["commodity"].astype(str).str.upper().str.strip()
    out["feature"] = out["feature"].astype(str).str.strip()
    if "abs_t_stat" not in out.columns and "max_abs_tstat" in out.columns:
        out["abs_t_stat"] = out["max_abs_tstat"]
    if "hit_rate" not in out.columns and "preferred_hit_rate" in out.columns:
        out["hit_rate"] = out["preferred_hit_rate"]
    if "horizon_days" not in out.columns and "preferred_horizon" in out.columns:
        out["horizon_days"] = out["preferred_horizon"]
    has_nonoverlap = "nonoverlap_abs_t_stat" in original_cols
    has_effective_observations = "effective_observations" in original_cols
    for col in [
        "abs_t_stat",
        "nonoverlap_abs_t_stat",
        "effective_observations",
        "hit_rate",
        "nonoverlap_hit_rate",
        "beta_per_1z",
        "nonoverlap_beta_per_1z",
    ]:
        if col not in out.columns:
            out[col] = np.nan
        out[col] = pd.to_numeric(out[col], errors="coerce")

    if exposure_map is not None and not exposure_map.empty:
        exposure = exposure_map.copy()
        exposure["ticker"] = exposure["ticker"].astype(str).str.upper().str.strip()
        exposure["commodity"] = exposure["commodity"].astype(str).str.upper().str.strip()
        exposure_cols = ["ticker", "commodity", "exposure_role", "prior_weight"]
        exposure = exposure[[col for col in exposure_cols if col in exposure.columns]].drop_duplicates(
            ["ticker", "commodity"]
        )
        out = out.merge(exposure, on=["ticker", "commodity"], how="left")
    if "exposure_role" not in out.columns:
        out["exposure_role"] = np.nan
    if "prior_weight" not in out.columns:
        out["prior_weight"] = np.nan
    out["prior_weight"] = pd.to_numeric(out["prior_weight"], errors="coerce")

    denominator = out["nonoverlap_abs_t_stat"].where(out["nonoverlap_abs_t_stat"] > 0)
    out["overlap_inflation_ratio"] = out["abs_t_stat"] / denominator
    out["feature_commodity_direction"] = out["feature"].map(_feature_commodity_direction)
    if "feature_family" not in out.columns:
        out["feature_family"] = out["feature"].map(feature_family)
    if "feature_hypothesis_family" not in out.columns:
        out["feature_hypothesis_family"] = out["feature"].map(feature_hypothesis_family)
    out["expected_beta_sign"] = np.sign(out["prior_weight"] * out["feature_commodity_direction"])
    out["observed_beta_sign"] = np.sign(out["beta_per_1z"])

    mapped = out[
        out["exposure_role"].notna()
        & out["observed_beta_sign"].ne(0)
        & (out["abs_t_stat"].fillna(0) >= min_abs_t)
        & (out["nonoverlap_abs_t_stat"].fillna(0) >= min_nonoverlap_abs_t)
    ].copy()
    if not mapped.empty:
        breadth = (
            mapped.groupby(["commodity", "exposure_role", "feature_hypothesis_family", "horizon_days"], dropna=False)
            .agg(
                peer_breadth_count=("ticker", "nunique"),
                peer_positive_count=("observed_beta_sign", lambda s: int((s > 0).sum())),
                peer_negative_count=("observed_beta_sign", lambda s: int((s < 0).sum())),
                peer_median_nonoverlap_abs_t=("nonoverlap_abs_t_stat", "median"),
                peer_median_hit_rate=("hit_rate", "median"),
            )
            .reset_index()
        )
        breadth["peer_same_direction_share"] = breadth[["peer_positive_count", "peer_negative_count"]].max(
            axis=1
        ) / breadth["peer_breadth_count"]
        breadth["peer_breadth_multiplier"] = np.select(
            [
                (breadth["peer_breadth_count"] >= 5) & (breadth["peer_same_direction_share"] >= 0.8),
                (breadth["peer_breadth_count"] >= 3) & (breadth["peer_same_direction_share"] >= 0.7),
                (breadth["peer_breadth_count"] >= 3) & (breadth["peer_same_direction_share"] >= 0.6),
            ],
            [1.50, 1.30, 1.15],
            default=1.0,
        )
        out = out.merge(
            breadth,
            on=["commodity", "exposure_role", "feature_hypothesis_family", "horizon_days"],
            how="left",
        )
    else:
        out["peer_breadth_count"] = np.nan
        out["peer_positive_count"] = np.nan
        out["peer_negative_count"] = np.nan
        out["peer_median_nonoverlap_abs_t"] = np.nan
        out["peer_median_hit_rate"] = np.nan
        out["peer_same_direction_share"] = np.nan
        out["peer_breadth_multiplier"] = np.nan

    out["flag_unmapped_exposure"] = out["prior_weight"].isna()
    out["flag_missing_nonoverlap_stats"] = not has_nonoverlap
    out["flag_low_effective_observations"] = has_effective_observations & (
        out["effective_observations"].fillna(0) < min_effective_observations
    )
    out["flag_weak_nonoverlap"] = has_nonoverlap & (out["abs_t_stat"].fillna(0) >= min_abs_t) & (
        out["nonoverlap_abs_t_stat"].fillna(0) < min_nonoverlap_abs_t
    )
    out["flag_overlap_inflation"] = has_nonoverlap & (
        out["overlap_inflation_ratio"].fillna(np.inf) >= max_overlap_inflation
    )
    out["flag_weak_hit_rate"] = (out["hit_rate"] - 0.5).abs().fillna(0) < min_hit_rate_edge
    out["flag_direction_review"] = (
        out["expected_beta_sign"].ne(0)
        & out["observed_beta_sign"].ne(0)
        & out["expected_beta_sign"].ne(out["observed_beta_sign"])
    )

    flag_cols = [
        "flag_unmapped_exposure",
        "flag_missing_nonoverlap_stats",
        "flag_low_effective_observations",
        "flag_weak_nonoverlap",
        "flag_overlap_inflation",
        "flag_weak_hit_rate",
        "flag_direction_review",
    ]
    out["falsification_flags"] = (
        out[flag_cols]
        .rename(columns={col: col.removeprefix("flag_") for col in flag_cols})
        .apply(lambda row: ",".join([col for col, value in row.items() if bool(value)]), axis=1)
    )
    out["falsification_issue_count"] = out[flag_cols].sum(axis=1).astype(int)
    out["falsification_verdict"] = np.select(
        [
            out["flag_weak_nonoverlap"] | out["flag_overlap_inflation"] | out["flag_low_effective_observations"],
            out["flag_unmapped_exposure"]
            | out["flag_missing_nonoverlap_stats"]
            | out["flag_weak_hit_rate"]
            | out["flag_direction_review"],
        ],
        ["reject_or_retest", "review"],
        default="pass",
    )

    preferred_cols = [
        "falsification_verdict",
        "falsification_flags",
        "falsification_issue_count",
        "ticker",
        "commodity",
        "exposure_role",
        "prior_weight",
        "feature",
        "feature_family",
        "feature_hypothesis_family",
        "horizon_days",
        "lookback_years",
        "observations",
        "effective_observations",
        "abs_t_stat",
        "nonoverlap_abs_t_stat",
        "overlap_inflation_ratio",
        "hit_rate",
        "nonoverlap_hit_rate",
        "beta_per_1z",
        "nonoverlap_beta_per_1z",
        "expected_beta_sign",
        "observed_beta_sign",
        "peer_breadth_count",
        "peer_same_direction_share",
        "peer_breadth_multiplier",
        "peer_median_nonoverlap_abs_t",
        "peer_median_hit_rate",
        "as_of_date",
        "sample_start",
        "sample_end",
    ]
    cols = [col for col in preferred_cols if col in out.columns] + [
        col for col in out.columns if col not in preferred_cols
    ]
    return out[cols].sort_values(
        ["falsification_verdict", "falsification_issue_count", "abs_t_stat"],
        ascending=[False, False, False],
    )


def build_exposure_taxonomy_audit(
    exposure_map: pd.DataFrame,
    role_taxonomy: pd.DataFrame | None = None,
    candidates: pd.DataFrame | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if exposure_map.empty:
        return exposure_map.copy(), pd.DataFrame()
    exposure = exposure_map.copy()
    exposure["ticker"] = exposure["ticker"].astype(str).str.upper().str.strip()
    exposure["commodity"] = exposure["commodity"].astype(str).str.upper().str.strip()
    exposure["exposure_role"] = exposure["exposure_role"].astype(str).str.strip()
    exposure["prior_weight"] = pd.to_numeric(exposure["prior_weight"], errors="coerce")

    taxonomy_cols = [
        "commodity",
        "exposure_role",
        "taxonomy_bucket",
        "economic_channel",
        "expected_prior_sign",
        "alpha_priority",
        "deployable_default",
        "notes",
    ]
    if role_taxonomy is not None and not role_taxonomy.empty:
        taxonomy = role_taxonomy.copy()
        taxonomy["commodity"] = taxonomy["commodity"].astype(str).str.upper().str.strip()
        taxonomy["exposure_role"] = taxonomy["exposure_role"].astype(str).str.strip()
        taxonomy["expected_prior_sign"] = pd.to_numeric(taxonomy["expected_prior_sign"], errors="coerce")
        taxonomy["deployable_default"] = taxonomy["deployable_default"].astype(str).str.lower().isin(
            {"true", "1", "yes", "y"}
        )
        exposure = exposure.merge(
            taxonomy[[col for col in taxonomy_cols if col in taxonomy.columns]],
            on=["commodity", "exposure_role"],
            how="left",
        )
    else:
        exposure["taxonomy_bucket"] = pd.NA
        exposure["economic_channel"] = pd.NA
        exposure["expected_prior_sign"] = np.nan
        exposure["alpha_priority"] = pd.NA
        exposure["deployable_default"] = pd.NA

    exposure["role_taxonomy_status"] = np.where(exposure["taxonomy_bucket"].notna(), "mapped_role", "missing_role")
    exposure["prior_sign"] = np.sign(exposure["prior_weight"])
    exposure["prior_sign_matches_taxonomy"] = np.where(
        exposure["expected_prior_sign"].fillna(0).eq(0),
        np.nan,
        exposure["prior_sign"].eq(np.sign(exposure["expected_prior_sign"])),
    )

    summary = (
        exposure.groupby(["commodity", "exposure_role"], dropna=False)
        .agg(
            ticker_count=("ticker", "nunique"),
            avg_prior_weight=("prior_weight", "mean"),
            avg_abs_prior_weight=("prior_weight", lambda s: float(pd.to_numeric(s, errors="coerce").abs().mean())),
            taxonomy_bucket=("taxonomy_bucket", "first"),
            economic_channel=("economic_channel", "first"),
            expected_prior_sign=("expected_prior_sign", "first"),
            alpha_priority=("alpha_priority", "first"),
            deployable_default=("deployable_default", "first"),
            role_taxonomy_status=("role_taxonomy_status", "first"),
            sign_match_share=("prior_sign_matches_taxonomy", "mean"),
        )
        .reset_index()
    )
    priority_rank = {"high": 0, "medium": 1, "low": 2}
    summary["alpha_priority_rank"] = summary["alpha_priority"].map(priority_rank).fillna(99).astype(int)
    summary = summary.sort_values(
        ["commodity", "alpha_priority_rank", "ticker_count"],
        ascending=[True, True, False],
    ).drop(columns=["alpha_priority_rank"])

    unmapped = pd.DataFrame()
    if candidates is not None and not candidates.empty:
        cand = candidates.copy()
        cand["ticker"] = cand["ticker"].astype(str).str.upper().str.strip()
        cand["commodity"] = cand["commodity"].astype(str).str.upper().str.strip()
        candidate_cols = [
            "ticker",
            "commodity",
            "feature",
            "feature_family",
            "direction",
            "preferred_horizon",
            "max_abs_tstat",
            "quality_score",
            "confidence",
            "theme",
            "role",
        ]
        cand = cand[[col for col in candidate_cols if col in cand.columns]].drop_duplicates()
        mapped_pairs = exposure[["ticker", "commodity", "exposure_role", "prior_weight", "taxonomy_bucket"]]
        unmapped = cand.merge(mapped_pairs, on=["ticker", "commodity"], how="left")
        unmapped = unmapped[unmapped["exposure_role"].isna()].copy()
        if not unmapped.empty:
            sort_cols = [col for col in ["commodity", "max_abs_tstat", "quality_score", "ticker"] if col in unmapped.columns]
            ascending = [True, False, False, True][: len(sort_cols)]
            unmapped = unmapped.sort_values(sort_cols, ascending=ascending).reset_index(drop=True)

    return summary.reset_index(drop=True), unmapped.reset_index(drop=True)


def build_candidate_taxonomy_review(
    candidates: pd.DataFrame,
    exposure_map: pd.DataFrame,
    role_taxonomy: pd.DataFrame | None = None,
    mechanism_alignment: pd.DataFrame | None = None,
    min_mechanism_alignment_probability: float = 0.67,
    mechanism_review_band: float = 0.55,
) -> pd.DataFrame:
    if candidates.empty:
        return candidates.copy()

    cand = candidates.copy()
    cand["ticker"] = cand["ticker"].astype(str).str.upper().str.strip()
    cand["commodity"] = cand["commodity"].astype(str).str.upper().str.strip()
    if "feature" in cand.columns:
        cand["feature"] = cand["feature"].astype(str).str.strip()
        cand["feature_family"] = cand.get("feature_family", cand["feature"].map(feature_family))
        cand["feature_hypothesis_family"] = cand.get(
            "feature_hypothesis_family",
            cand["feature"].map(feature_hypothesis_family),
        )
    else:
        cand["feature"] = pd.NA
        cand["feature_family"] = pd.NA
        cand["feature_hypothesis_family"] = pd.NA
    canonical_review_cols = [
        "exposure_role",
        "prior_weight",
        "exposure_notes",
        "taxonomy_bucket",
        "economic_channel",
        "expected_prior_sign",
        "alpha_priority",
        "deployable_default",
        "taxonomy_notes",
    ]
    cand = cand.drop(columns=[col for col in canonical_review_cols if col in cand.columns])

    exposure = exposure_map.copy()
    exposure["ticker"] = exposure["ticker"].astype(str).str.upper().str.strip()
    exposure["commodity"] = exposure["commodity"].astype(str).str.upper().str.strip()
    exposure["exposure_role"] = exposure["exposure_role"].astype(str).str.strip()
    exposure["prior_weight"] = pd.to_numeric(exposure["prior_weight"], errors="coerce")

    out = cand.merge(
        exposure[["ticker", "commodity", "exposure_role", "prior_weight", "notes"]].drop_duplicates(
            ["ticker", "commodity"]
        ).rename(columns={"notes": "exposure_notes"}),
        on=["ticker", "commodity"],
        how="left",
    )

    if role_taxonomy is not None and not role_taxonomy.empty:
        taxonomy = role_taxonomy.copy()
        taxonomy["commodity"] = taxonomy["commodity"].astype(str).str.upper().str.strip()
        taxonomy["exposure_role"] = taxonomy["exposure_role"].astype(str).str.strip()
        taxonomy["expected_prior_sign"] = pd.to_numeric(taxonomy["expected_prior_sign"], errors="coerce")
        taxonomy["deployable_default"] = taxonomy["deployable_default"].astype(str).str.lower().isin(
            {"true", "1", "yes", "y"}
        )
        out = out.merge(
            taxonomy[
                [
                    "commodity",
                    "exposure_role",
                    "taxonomy_bucket",
                    "economic_channel",
                    "expected_prior_sign",
                    "alpha_priority",
                    "deployable_default",
                    "notes",
                ]
            ].drop_duplicates(["commodity", "exposure_role"]),
            on=["commodity", "exposure_role"],
            how="left",
            suffixes=("", "_taxonomy"),
        )
        out = out.rename(columns={"notes": "taxonomy_notes"})
    else:
        out["taxonomy_bucket"] = pd.NA
        out["economic_channel"] = pd.NA
        out["expected_prior_sign"] = np.nan
        out["alpha_priority"] = pd.NA
        out["deployable_default"] = pd.NA

    out["feature_commodity_direction"] = out["feature"].map(_feature_commodity_direction)
    out["expected_beta_sign"] = np.sign(
        pd.to_numeric(out["prior_weight"], errors="coerce") * out["feature_commodity_direction"]
    )
    if "direction" in out.columns:
        out["candidate_direction_sign"] = np.sign(pd.to_numeric(out["direction"], errors="coerce"))
    else:
        out["candidate_direction_sign"] = np.nan

    out["flag_missing_exposure"] = out["exposure_role"].isna()
    out["flag_missing_role_taxonomy"] = out["exposure_role"].notna() & out["taxonomy_bucket"].isna()
    out["flag_no_economic_channel"] = out["economic_channel"].isna() | out["economic_channel"].astype(str).str.strip().eq("")
    out["flag_low_priority_role"] = out["alpha_priority"].astype(str).str.lower().eq("low")
    out["flag_macro_proxy_role"] = out["taxonomy_bucket"].astype(str).str.contains("macro_proxy", na=False)
    out["flag_not_deployable_default"] = out["deployable_default"].eq(False)
    out["flag_direction_mismatch"] = (
        out["candidate_direction_sign"].ne(0)
        & out["expected_beta_sign"].ne(0)
        & out["candidate_direction_sign"].notna()
        & out["expected_beta_sign"].notna()
        & out["candidate_direction_sign"].ne(out["expected_beta_sign"])
    )

    flag_cols = [
        "flag_missing_exposure",
        "flag_missing_role_taxonomy",
        "flag_no_economic_channel",
        "flag_low_priority_role",
        "flag_macro_proxy_role",
        "flag_not_deployable_default",
        "flag_direction_mismatch",
    ]
    out["taxonomy_flags"] = (
        out[flag_cols]
        .rename(columns={col: col.removeprefix("flag_") for col in flag_cols})
        .apply(lambda row: ",".join([col for col, value in row.items() if bool(value)]), axis=1)
    )
    out["taxonomy_issue_count"] = out[flag_cols].sum(axis=1).astype(int)
    out["taxonomy_verdict"] = np.select(
        [
            out["flag_missing_exposure"],
            out[
                [
                    "flag_missing_role_taxonomy",
                    "flag_no_economic_channel",
                    "flag_low_priority_role",
                    "flag_macro_proxy_role",
                    "flag_not_deployable_default",
                    "flag_direction_mismatch",
                ]
            ].any(axis=1),
        ],
        ["block", "review"],
        default="pass",
    )

    if mechanism_alignment is not None and not mechanism_alignment.empty:
        if "preferred_horizon" in out.columns:
            out["preferred_horizon"] = pd.to_numeric(out["preferred_horizon"], errors="coerce").astype("Int64")
        else:
            out["preferred_horizon"] = pd.Series(pd.array([pd.NA] * len(out), dtype="Int64"), index=out.index)
        alignment = _candidate_mechanism_gate(
            mechanism_alignment=mechanism_alignment,
            min_alignment_probability=min_mechanism_alignment_probability,
            review_band=mechanism_review_band,
        )
        out = out.merge(alignment, on=["ticker", "commodity", "feature", "preferred_horizon"], how="left")
        missing_alignment = out["mechanism_gate_verdict"].isna()
        out["mechanism_gate_verdict"] = out["mechanism_gate_verdict"].fillna("review")
        out.loc[missing_alignment, "mechanism_gate_flags"] = "missing_mechanism_alignment"
    else:
        out["mechanism_gate_verdict"] = "missing"
        out["mechanism_gate_flags"] = "missing_mechanism_alignment"
        out["mechanism_alignment_probability"] = np.nan
        out["mechanism_alignment_aligned_share"] = np.nan
        out["mechanism_alignment_conflict_share"] = np.nan
        out["mechanism_alignment_observation_count"] = 0

    out["candidate_gate_verdict"] = np.select(
        [
            out["taxonomy_verdict"].eq("block"),
            out["taxonomy_verdict"].eq("review") | out["mechanism_gate_verdict"].ne("pass"),
        ],
        ["block", "review"],
        default="pass",
    )
    out["candidate_gate_flags"] = (
        out[["taxonomy_flags", "mechanism_gate_flags"]]
        .fillna("")
        .apply(lambda row: ",".join([value for value in row if str(value).strip()]), axis=1)
    )
    front = [
        "candidate_gate_verdict",
        "candidate_gate_flags",
        "taxonomy_verdict",
        "taxonomy_flags",
        "taxonomy_issue_count",
        "mechanism_gate_verdict",
        "mechanism_gate_flags",
        "mechanism_alignment_probability",
        "mechanism_alignment_aligned_share",
        "mechanism_alignment_conflict_share",
        "mechanism_alignment_observation_count",
        "ticker",
        "commodity",
        "feature",
        "feature_family",
        "feature_hypothesis_family",
        "direction",
        "exposure_role",
        "prior_weight",
        "taxonomy_bucket",
        "economic_channel",
        "alpha_priority",
        "deployable_default",
        "expected_beta_sign",
        "candidate_direction_sign",
    ]
    cols = [col for col in front if col in out.columns] + [col for col in out.columns if col not in front]
    return out[cols].sort_values(
        ["candidate_gate_verdict", "taxonomy_issue_count", "ticker", "commodity"],
        ascending=[True, False, True, True],
    ).reset_index(drop=True)


def _candidate_mechanism_gate(
    mechanism_alignment: pd.DataFrame,
    min_alignment_probability: float,
    review_band: float,
) -> pd.DataFrame:
    alignment = mechanism_alignment.copy()
    required = {"ticker", "commodity", "feature", "horizon_days", "mechanism_alignment_probability"}
    missing = required.difference(alignment.columns)
    if missing:
        raise ValueError(f"mechanism alignment is missing required columns: {sorted(missing)}")
    alignment["ticker"] = alignment["ticker"].astype(str).str.upper().str.strip()
    alignment["commodity"] = alignment["commodity"].astype(str).str.upper().str.strip()
    alignment["feature"] = alignment["feature"].astype(str).str.strip()
    alignment["preferred_horizon"] = pd.to_numeric(alignment["horizon_days"], errors="coerce").astype("Int64")
    alignment["mechanism_alignment_probability"] = pd.to_numeric(
        alignment["mechanism_alignment_probability"],
        errors="coerce",
    )
    if "mechanism_alignment_sign" not in alignment.columns:
        alignment["mechanism_alignment_sign"] = np.nan
    alignment["mechanism_alignment_sign"] = pd.to_numeric(alignment["mechanism_alignment_sign"], errors="coerce")
    if "mechanism_state" not in alignment.columns:
        alignment["mechanism_state"] = pd.NA
    if "mechanism_verdict" not in alignment.columns:
        alignment["mechanism_verdict"] = pd.NA

    grouped = (
        alignment.groupby(["ticker", "commodity", "feature", "preferred_horizon"], dropna=False)
        .agg(
            mechanism_alignment_probability=("mechanism_alignment_probability", "mean"),
            mechanism_alignment_min_probability=("mechanism_alignment_probability", "min"),
            mechanism_alignment_aligned_share=("mechanism_alignment_sign", lambda s: float((s > 0).mean())),
            mechanism_alignment_conflict_share=("mechanism_alignment_sign", lambda s: float((s < 0).mean())),
            mechanism_alignment_observation_count=("mechanism_alignment_probability", "count"),
            mechanism_alignment_states=(
                "mechanism_state",
                lambda s: ",".join(sorted(set(s.dropna().astype(str)))),
            ),
            mechanism_alignment_source_verdicts=(
                "mechanism_verdict",
                lambda s: ",".join(sorted(set(s.dropna().astype(str)))),
            ),
        )
        .reset_index()
    )
    grouped["mechanism_gate_verdict"] = np.select(
        [
            grouped["mechanism_alignment_observation_count"].eq(0),
            grouped["mechanism_alignment_probability"].ge(min_alignment_probability),
            grouped["mechanism_alignment_probability"].ge(review_band),
        ],
        ["review", "pass", "review"],
        default="conflict",
    )
    grouped["mechanism_gate_flags"] = ""
    grouped.loc[grouped["mechanism_alignment_observation_count"].eq(0), "mechanism_gate_flags"] += (
        "missing_mechanism_alignment,"
    )
    grouped.loc[grouped["mechanism_gate_verdict"].eq("conflict"), "mechanism_gate_flags"] += (
        "mechanism_alignment_conflict,"
    )
    grouped.loc[
        grouped["mechanism_gate_verdict"].eq("review")
        & grouped["mechanism_alignment_observation_count"].gt(0)
        & grouped["mechanism_alignment_probability"].lt(min_alignment_probability),
        "mechanism_gate_flags",
    ] += "weak_mechanism_alignment,"
    grouped.loc[grouped["mechanism_alignment_conflict_share"].gt(0.5), "mechanism_gate_flags"] += (
        "mostly_conflicting_mechanism_signs,"
    )
    grouped.loc[
        grouped["mechanism_alignment_source_verdicts"].astype(str).str.contains("review|block", regex=True, na=False),
        "mechanism_gate_flags",
    ] += "mechanism_state_not_pass,"
    grouped["mechanism_gate_flags"] = grouped["mechanism_gate_flags"].str.rstrip(",").replace("", np.nan)
    return grouped


def _corr_beta_stats(
    x: pd.Series,
    y: pd.Series,
    min_observations: int,
) -> dict[str, float | int]:
    sample = pd.DataFrame({"x": x, "y": y}).replace([np.inf, -np.inf], np.nan).dropna()
    observations = int(len(sample))
    if observations < min_observations:
        return {"observations": observations, "corr": np.nan, "beta": np.nan}
    variance = float(sample["x"].var(ddof=0))
    beta = np.nan if variance == 0 else float(sample["x"].cov(sample["y"]) / sample["x"].var())
    return {
        "observations": observations,
        "corr": float(sample["x"].corr(sample["y"])),
        "beta": beta,
    }


def build_nonlinear_commodity_beta_audit(
    candidates: pd.DataFrame,
    equity_processed: pd.DataFrame,
    commodity_signals: pd.DataFrame | None = None,
    exposure_map: pd.DataFrame | None = None,
    return_column: str = "residual_return_mktsec_w12m",
    commodity_return_column: str = "commodity_return_mktseccomm",
    commodity_signal_return_column: str = "front_log_ret_1d",
    lag_days: list[int] | tuple[int, ...] = (0, 1, 5, 10, 21),
    min_observations: int = 126,
    large_move_quantile: float = 0.80,
    volatility_window: int = 21,
    max_abs_lag_corr_threshold: float = 0.15,
    asymmetry_corr_diff_threshold: float = 0.15,
) -> pd.DataFrame:
    if candidates.empty:
        return candidates.copy()
    required_candidate_cols = {"ticker", "commodity"}
    missing_candidate_cols = required_candidate_cols.difference(candidates.columns)
    if missing_candidate_cols:
        raise ValueError(f"candidates is missing required columns: {sorted(missing_candidate_cols)}")
    required_equity_cols = {"ticker", "date", return_column, commodity_return_column}
    if commodity_signals is not None and not commodity_signals.empty:
        required_equity_cols = {"ticker", "date", return_column}
    missing_equity_cols = required_equity_cols.difference(equity_processed.columns)
    if missing_equity_cols:
        raise ValueError(f"equity_processed is missing required columns: {sorted(missing_equity_cols)}")

    cand = candidates.copy()
    cand["ticker"] = cand["ticker"].astype(str).str.upper().str.strip()
    cand["commodity"] = cand["commodity"].astype(str).str.upper().str.strip()
    if "feature" in cand.columns:
        cand["feature"] = cand["feature"].astype(str).str.strip()
    else:
        cand["feature"] = pd.NA
    if "feature_hypothesis_family" not in cand.columns:
        cand["feature_hypothesis_family"] = cand["feature"].map(feature_hypothesis_family)

    if exposure_map is not None and not exposure_map.empty:
        exposure = exposure_map.copy()
        exposure["ticker"] = exposure["ticker"].astype(str).str.upper().str.strip()
        exposure["commodity"] = exposure["commodity"].astype(str).str.upper().str.strip()
        exposure_cols = ["ticker", "commodity", "exposure_role", "prior_weight"]
        cand = cand.merge(
            exposure[[col for col in exposure_cols if col in exposure.columns]].drop_duplicates(
                ["ticker", "commodity"]
            ),
            on=["ticker", "commodity"],
            how="left",
        )

    panel = equity_processed.copy()
    panel["ticker"] = panel["ticker"].astype(str).str.upper().str.strip()
    panel["date"] = pd.to_datetime(panel["date"], utc=False)
    panel[return_column] = pd.to_numeric(panel[return_column], errors="coerce")
    if commodity_return_column in panel.columns:
        panel[commodity_return_column] = pd.to_numeric(panel[commodity_return_column], errors="coerce")
    if "commodity_symbol_mktseccomm" in panel.columns:
        panel["commodity_symbol_mktseccomm"] = panel["commodity_symbol_mktseccomm"].astype(str).str.upper().str.strip()

    signal_returns = pd.DataFrame()
    if commodity_signals is not None and not commodity_signals.empty:
        signal_col = "symbol" if "symbol" in commodity_signals.columns else "commodity"
        required_signal_cols = {"date", signal_col, commodity_signal_return_column}
        missing_signal_cols = required_signal_cols.difference(commodity_signals.columns)
        if missing_signal_cols:
            raise ValueError(f"commodity_signals is missing required columns: {sorted(missing_signal_cols)}")
        signal_returns = commodity_signals[["date", signal_col, commodity_signal_return_column]].copy()
        signal_returns = signal_returns.rename(
            columns={signal_col: "commodity", commodity_signal_return_column: "_commodity_return"}
        )
        signal_returns["commodity"] = signal_returns["commodity"].astype(str).str.upper().str.strip()
        signal_returns["date"] = pd.to_datetime(signal_returns["date"], utc=False)
        signal_returns["_commodity_return"] = pd.to_numeric(signal_returns["_commodity_return"], errors="coerce")

    key_cols = ["ticker", "commodity", "feature", "feature_hypothesis_family"]
    extra_cols = [col for col in ["exposure_role", "prior_weight"] if col in cand.columns]
    rows: list[dict[str, object]] = []
    for key, group in cand.groupby(key_cols, dropna=False, sort=True):
        ticker, commodity, feature, hypothesis_family = key
        data = panel[panel["ticker"].eq(ticker)].copy()
        if signal_returns.empty and "commodity_symbol_mktseccomm" in data.columns:
            data = data[data["commodity_symbol_mktseccomm"].eq(commodity)].copy()
        data = data.sort_values("date").reset_index(drop=True)
        if data.empty:
            rows.append(
                {
                    "ticker": ticker,
                    "commodity": commodity,
                    "feature": feature,
                    "feature_hypothesis_family": hypothesis_family,
                    "nonlinear_beta_verdict": "review",
                    "nonlinear_beta_flags": "missing_return_panel",
                }
            )
            continue

        y = data[return_column]
        if not signal_returns.empty:
            commodity_returns = signal_returns[signal_returns["commodity"].eq(commodity)][
                ["date", "_commodity_return"]
            ]
            data = data.merge(commodity_returns, on="date", how="left")
            c = data["_commodity_return"]
            active_commodity_return_column = commodity_signal_return_column
        else:
            c = data[commodity_return_column]
            active_commodity_return_column = commodity_return_column
        record: dict[str, object] = {
            "ticker": ticker,
            "commodity": commodity,
            "feature": feature,
            "feature_hypothesis_family": hypothesis_family,
            "sample_start": data["date"].min(),
            "sample_end": data["date"].max(),
            "return_column": return_column,
            "commodity_return_column": active_commodity_return_column,
        }
        for col in extra_cols:
            record[col] = group[col].dropna().iloc[0] if group[col].notna().any() else np.nan

        lag_records: list[tuple[int, dict[str, float | int]]] = []
        for lag in lag_days:
            stats = _corr_beta_stats(c.shift(lag), y, min_observations=min_observations)
            lag_records.append((int(lag), stats))
            record[f"lag_{int(lag)}d_observations"] = stats["observations"]
            record[f"lag_{int(lag)}d_corr"] = stats["corr"]
            record[f"lag_{int(lag)}d_beta"] = stats["beta"]

        valid_lags = [(lag, stats) for lag, stats in lag_records if pd.notna(stats["corr"])]
        if valid_lags:
            max_lag, max_stats = max(valid_lags, key=lambda item: abs(float(item[1]["corr"])))
            record["max_abs_lag_days"] = max_lag
            record["max_abs_lag_corr"] = abs(float(max_stats["corr"]))
            record["max_abs_lag_beta"] = max_stats["beta"]
        else:
            record["max_abs_lag_days"] = np.nan
            record["max_abs_lag_corr"] = np.nan
            record["max_abs_lag_beta"] = np.nan

        up_stats = _corr_beta_stats(c.where(c > 0), y, min_observations=min_observations)
        down_stats = _corr_beta_stats(c.where(c < 0), y, min_observations=min_observations)
        record["commodity_up_observations"] = up_stats["observations"]
        record["commodity_up_corr"] = up_stats["corr"]
        record["commodity_up_beta"] = up_stats["beta"]
        record["commodity_down_observations"] = down_stats["observations"]
        record["commodity_down_corr"] = down_stats["corr"]
        record["commodity_down_beta"] = down_stats["beta"]
        record["up_down_corr_diff"] = (
            abs(float(up_stats["corr"] - down_stats["corr"]))
            if pd.notna(up_stats["corr"]) and pd.notna(down_stats["corr"])
            else np.nan
        )

        abs_c = c.abs()
        large_threshold = abs_c.quantile(large_move_quantile)
        large_stats = _corr_beta_stats(c.where(abs_c >= large_threshold), y, min_observations=min_observations)
        normal_stats = _corr_beta_stats(c.where(abs_c < large_threshold), y, min_observations=min_observations)
        record["large_move_threshold"] = float(large_threshold) if pd.notna(large_threshold) else np.nan
        record["large_move_observations"] = large_stats["observations"]
        record["large_move_corr"] = large_stats["corr"]
        record["large_move_beta"] = large_stats["beta"]
        record["normal_move_observations"] = normal_stats["observations"]
        record["normal_move_corr"] = normal_stats["corr"]
        record["normal_move_beta"] = normal_stats["beta"]

        realized_vol = c.rolling(volatility_window, min_periods=max(5, volatility_window // 2)).std()
        vol_median = realized_vol.median()
        high_vol_stats = _corr_beta_stats(c.where(realized_vol >= vol_median), y, min_observations=min_observations)
        low_vol_stats = _corr_beta_stats(c.where(realized_vol < vol_median), y, min_observations=min_observations)
        record["volatility_window"] = volatility_window
        record["high_vol_observations"] = high_vol_stats["observations"]
        record["high_vol_corr"] = high_vol_stats["corr"]
        record["high_vol_beta"] = high_vol_stats["beta"]
        record["low_vol_observations"] = low_vol_stats["observations"]
        record["low_vol_corr"] = low_vol_stats["corr"]
        record["low_vol_beta"] = low_vol_stats["beta"]

        flags = {
            "lagged_exposure": pd.notna(record["max_abs_lag_corr"])
            and float(record["max_abs_lag_corr"]) >= max_abs_lag_corr_threshold,
            "up_down_asymmetry": pd.notna(record["up_down_corr_diff"])
            and float(record["up_down_corr_diff"]) >= asymmetry_corr_diff_threshold,
            "large_move_exposure": pd.notna(record["large_move_corr"])
            and abs(float(record["large_move_corr"])) >= max_abs_lag_corr_threshold,
            "high_vol_exposure": pd.notna(record["high_vol_corr"])
            and abs(float(record["high_vol_corr"])) >= max_abs_lag_corr_threshold,
            "low_observations": max(int(stats["observations"]) for _, stats in lag_records) < min_observations,
        }
        record["nonlinear_beta_flags"] = ",".join([name for name, value in flags.items() if bool(value)])
        record["nonlinear_beta_issue_count"] = int(sum(bool(value) for value in flags.values()))
        record["nonlinear_beta_verdict"] = "review" if record["nonlinear_beta_issue_count"] else "pass"
        rows.append(record)

    out = pd.DataFrame(rows)
    if out.empty:
        return out
    front = [
        "nonlinear_beta_verdict",
        "nonlinear_beta_flags",
        "nonlinear_beta_issue_count",
        "ticker",
        "commodity",
        "exposure_role",
        "prior_weight",
        "feature",
        "feature_hypothesis_family",
        "sample_start",
        "sample_end",
        "return_column",
        "commodity_return_column",
        "max_abs_lag_days",
        "max_abs_lag_corr",
        "max_abs_lag_beta",
        "up_down_corr_diff",
        "large_move_corr",
        "high_vol_corr",
    ]
    cols = [col for col in front if col in out.columns] + [col for col in out.columns if col not in front]
    return out[cols].sort_values(
        ["nonlinear_beta_verdict", "nonlinear_beta_issue_count", "max_abs_lag_corr"],
        ascending=[False, False, False],
    ).reset_index(drop=True)


def build_registry_turnover(
    snapshots: pd.DataFrame,
    min_prior_snapshots: int = 1,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if snapshots.empty:
        return snapshots.copy(), snapshots.copy()
    df = snapshots.copy()
    df["as_of_date"] = pd.to_datetime(df["as_of_date"], utc=False)
    df["ticker"] = df["ticker"].astype(str).str.upper().str.strip()
    df["commodity"] = df["commodity"].astype(str).str.upper().str.strip()
    df["feature"] = df["feature"].astype(str).str.strip()
    df["feature_family"] = df["feature"].map(feature_family)

    key_cols = ["ticker", "commodity", "feature"]
    signal_cols = key_cols + ["direction"]
    dates = sorted(df["as_of_date"].dropna().unique())
    summary_rows: list[dict[str, object]] = []
    detail_rows: list[dict[str, object]] = []
    previous: pd.DataFrame | None = None

    for date in dates:
        current = df[df["as_of_date"] == date].copy()
        current_keys = current[signal_cols].drop_duplicates()
        if previous is None:
            summary_rows.append(
                {
                    "as_of_date": pd.Timestamp(date),
                    "signal_count": len(current_keys),
                    "added_count": len(current_keys),
                    "removed_count": 0,
                    "kept_count": 0,
                    "retention_rate": np.nan,
                    "direction_flip_count": 0,
                }
            )
            previous = current_keys
            continue

        prev_keys = previous[signal_cols].drop_duplicates()
        kept = current_keys.merge(prev_keys, on=signal_cols, how="inner")
        added = current_keys.merge(prev_keys, on=signal_cols, how="left", indicator=True)
        added = added[added["_merge"] == "left_only"].drop(columns=["_merge"])
        removed = prev_keys.merge(current_keys, on=signal_cols, how="left", indicator=True)
        removed = removed[removed["_merge"] == "left_only"].drop(columns=["_merge"])

        direction_compare = current_keys.merge(prev_keys, on=key_cols, suffixes=("_current", "_previous"))
        flips = direction_compare[direction_compare["direction_current"] != direction_compare["direction_previous"]]
        prev_count = max(len(prev_keys), min_prior_snapshots)
        summary_rows.append(
            {
                "as_of_date": pd.Timestamp(date),
                "signal_count": len(current_keys),
                "added_count": len(added),
                "removed_count": len(removed),
                "kept_count": len(kept),
                "retention_rate": len(kept) / prev_count,
                "direction_flip_count": len(flips),
            }
        )
        for state, frame in [("added", added), ("removed", removed), ("kept", kept)]:
            if frame.empty:
                continue
            d = frame.copy()
            d["as_of_date"] = pd.Timestamp(date)
            d["state"] = state
            detail_rows.append(d)
        if not flips.empty:
            f = flips.copy()
            f["as_of_date"] = pd.Timestamp(date)
            f["state"] = "direction_flip"
            detail_rows.append(f)
        previous = current_keys

    summary = pd.DataFrame(summary_rows)
    detail = pd.concat(detail_rows, ignore_index=True) if detail_rows else pd.DataFrame()
    return summary, detail


def build_registry_snapshots_from_reactions(
    reactions: pd.DataFrame,
    seed_universe: pd.DataFrame,
    min_events: int,
    min_abs_t: float,
    min_same_direction_horizons: int,
) -> pd.DataFrame:
    if reactions.empty:
        return reactions.copy()
    df = reactions.copy()
    df["as_of_date"] = pd.to_datetime(df["as_of_date"], utc=False)
    rows: list[pd.DataFrame] = []
    for as_of_date, group in df.groupby("as_of_date", sort=True):
        registry = build_stock_sensitivity_registry(
            reactions=group,
            seed_universe=seed_universe,
            min_events=min_events,
            min_abs_t=min_abs_t,
            min_same_direction_horizons=min_same_direction_horizons,
        )
        if not registry.empty:
            registry["as_of_date"] = pd.Timestamp(as_of_date)
            rows.append(registry)
    return pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()


def build_group_activation_scores(
    registry: pd.DataFrame,
    commodity_signals: pd.DataFrame,
    exposure_map: pd.DataFrame,
    as_of_date: str | None = None,
    activation_z: float = 1.0,
    feature_z_window: int = 252,
    min_feature_observations: int = 126,
    require_exposure: bool = True,
) -> pd.DataFrame:
    if registry.empty:
        return registry.copy()
    reg = registry.copy()
    reg["ticker"] = reg["ticker"].astype(str).str.upper().str.strip()
    reg["commodity"] = reg["commodity"].astype(str).str.upper().str.strip()
    reg["feature"] = reg["feature"].astype(str).str.strip()
    reg["feature_family"] = reg["feature"].map(feature_family)

    features = sorted(reg["feature"].unique())
    z = _feature_z_scores(
        commodity_signals=commodity_signals,
        features=features,
        feature_z_window=feature_z_window,
        min_feature_observations=min_feature_observations,
    )
    if as_of_date:
        target = pd.Timestamp(as_of_date)
        z = z[z["arrival"] <= target]
    if z.empty:
        return pd.DataFrame()

    latest = z.groupby(["commodity", "feature"])["date"].max().reset_index()
    z = z.merge(latest, on=["commodity", "feature", "date"], how="inner")
    components = reg.merge(z, on=["commodity", "feature"], how="inner")
    if components.empty:
        return pd.DataFrame()

    exp = exposure_map.copy()
    exp["ticker"] = exp["ticker"].astype(str).str.upper().str.strip()
    exp["commodity"] = exp["commodity"].astype(str).str.upper().str.strip()
    components = components.merge(
        exp[["ticker", "commodity", "exposure_role", "prior_weight"]].drop_duplicates(["ticker", "commodity"]),
        on=["ticker", "commodity"],
        how="left",
    )
    if require_exposure:
        components = components[components["exposure_role"].notna()].copy()
        if components.empty:
            return pd.DataFrame()
    components["peer_group"] = components["exposure_role"].fillna(components.get("role", "unknown")).fillna(
        "unknown"
    )
    components["component_score"] = components["feature_z"] * components["score_weight"]
    components["component_abs_score"] = components["component_score"].abs()
    components["active"] = components["feature_z"].abs() >= activation_z
    active = components[components["active"]].copy()
    if active.empty:
        return pd.DataFrame()

    active["score_date"] = pd.Timestamp(as_of_date) if as_of_date else active["date"].max()
    grouped = (
        active.groupby(["score_date", "commodity", "peer_group", "feature_family"], dropna=False)
        .agg(
            arrival=("arrival", "max"),
            group_score=("component_score", "sum"),
            group_abs_score=("component_abs_score", "sum"),
            mean_feature_z=("feature_z", "mean"),
            max_abs_feature_z=("feature_z", lambda s: s.abs().max()),
            active_components=("component_score", "count"),
            active_tickers=("ticker", "nunique"),
            mean_component_score=("component_score", "mean"),
            component_score_std=("component_score", "std"),
            tickers=("ticker", lambda s: ",".join(sorted(set(s.astype(str))))),
            features=("feature", lambda s: ",".join(sorted(set(s.astype(str))))),
        )
        .reset_index()
        .rename(columns={"score_date": "date"})
    )
    grouped["score_direction"] = np.where(grouped["group_score"] >= 0, "positive", "negative")
    return grouped.sort_values("group_abs_score", ascending=False).reset_index(drop=True)


def consolidate_candidate_signals(
    candidates: pd.DataFrame,
    forecast_audit: pd.DataFrame | None = None,
    reviewed_features: pd.DataFrame | None = None,
    mechanism_alignment: pd.DataFrame | None = None,
    min_confidence: str = "medium",
    require_audit_candidate: bool = False,
    require_mechanism_pass: bool = False,
    block_mechanism_conflicts: bool = False,
    min_mechanism_alignment_probability: float = 0.67,
    mechanism_review_band: float = 0.55,
    min_same_direction_share: float = 0.6,
    min_peer_direction_share: float = 0.0,
    max_per_ticker: int = 3,
) -> pd.DataFrame:
    if candidates.empty:
        return candidates.copy()

    confidence_rank = {"low": 1, "medium": 2, "high": 3}
    min_rank = confidence_rank.get(min_confidence, 2)

    out = candidates.copy()
    out["ticker"] = out["ticker"].astype(str).str.upper().str.strip()
    out["commodity"] = out["commodity"].astype(str).str.upper().str.strip()
    out["feature"] = out["feature"].astype(str).str.strip()
    out["confidence"] = out["confidence"].astype(str).str.lower().str.strip()
    out["confidence_rank"] = out["confidence"].map(confidence_rank).fillna(0)
    out = out[out["confidence_rank"] >= min_rank].copy()
    if out.empty:
        return out
    audit_generated_cols = [
        "audit_verdict",
        "audit_flags",
        "audit_candidate",
        "same_direction_share",
        "same_direction_sig15_years",
        "peer_tickers",
        "peer_direction_share",
        "peer_median_t",
        "horizon_days",
    ]
    out = out.drop(columns=[col for col in audit_generated_cols if col in out.columns], errors="ignore")

    family_map: dict[str, str] = {}
    if reviewed_features is not None and not reviewed_features.empty:
        family_map = (
            reviewed_features.drop_duplicates("feature")
            .set_index("feature")["feature_family"]
            .astype(str)
            .to_dict()
        )
    out["feature_family"] = out["feature"].map(family_map).fillna(out["feature"].map(feature_family))

    if forecast_audit is not None and not forecast_audit.empty:
        audit = forecast_audit.copy()
        audit["ticker"] = audit["ticker"].astype(str).str.upper().str.strip()
        audit["commodity"] = audit["commodity"].astype(str).str.upper().str.strip()
        audit["feature"] = audit["feature"].astype(str).str.strip()
        audit["horizon_days"] = pd.to_numeric(audit["horizon_days"], errors="coerce")
        audit["audit_candidate"] = audit["audit_verdict"].astype(str).eq("candidate")
        audit_cols = [
            "ticker",
            "commodity",
            "feature",
            "horizon_days",
            "audit_verdict",
            "audit_flags",
            "same_direction_share",
            "same_direction_sig15_years",
            "peer_tickers",
            "peer_direction_share",
            "peer_median_t",
        ]
        audit = audit[[col for col in audit_cols if col in audit.columns]].copy()
        audit["same_direction_share"] = pd.to_numeric(audit.get("same_direction_share"), errors="coerce")
        audit["peer_direction_share"] = pd.to_numeric(audit.get("peer_direction_share"), errors="coerce")
        audit = audit.sort_values(
            ["ticker", "commodity", "feature", "horizon_days", "same_direction_share", "peer_direction_share"],
            ascending=[True, True, True, True, False, False],
        ).drop_duplicates(["ticker", "commodity", "feature", "horizon_days"])
        out = out.merge(
            audit,
            left_on=["ticker", "commodity", "feature", "preferred_horizon"],
            right_on=["ticker", "commodity", "feature", "horizon_days"],
            how="left",
        )
        out["audit_verdict"] = out["audit_verdict"].fillna("missing")
        out["audit_candidate"] = out["audit_verdict"].eq("candidate")
        out["same_direction_share"] = pd.to_numeric(out["same_direction_share"], errors="coerce")
        out["peer_direction_share"] = pd.to_numeric(out["peer_direction_share"], errors="coerce")
    else:
        out["audit_verdict"] = "missing"
        out["audit_flags"] = pd.NA
        out["audit_candidate"] = False
        out["same_direction_share"] = np.nan
        out["peer_direction_share"] = np.nan
        out["peer_tickers"] = np.nan
        out["peer_median_t"] = np.nan

    if require_audit_candidate:
        out = out[out["audit_candidate"]].copy()
    out = out[out["same_direction_share"].fillna(1.0) >= min_same_direction_share].copy()
    out = out[out["peer_direction_share"].fillna(1.0) >= min_peer_direction_share].copy()
    if out.empty:
        return out

    if mechanism_alignment is not None and not mechanism_alignment.empty:
        if "preferred_horizon" in out.columns:
            out["preferred_horizon"] = pd.to_numeric(out["preferred_horizon"], errors="coerce").astype("Int64")
        else:
            out["preferred_horizon"] = pd.Series(pd.array([pd.NA] * len(out), dtype="Int64"), index=out.index)
        alignment = _candidate_mechanism_gate(
            mechanism_alignment=mechanism_alignment,
            min_alignment_probability=min_mechanism_alignment_probability,
            review_band=mechanism_review_band,
        )
        out = out.merge(alignment, on=["ticker", "commodity", "feature", "preferred_horizon"], how="left")
        missing_alignment = out["mechanism_gate_verdict"].isna()
        out["mechanism_gate_verdict"] = out["mechanism_gate_verdict"].fillna("review")
        out.loc[missing_alignment, "mechanism_gate_flags"] = "missing_mechanism_alignment"
        if require_mechanism_pass:
            out = out[out["mechanism_gate_verdict"].eq("pass")].copy()
        elif block_mechanism_conflicts:
            out = out[out["mechanism_gate_verdict"].ne("conflict")].copy()
    else:
        out["mechanism_gate_verdict"] = "missing"
        out["mechanism_gate_flags"] = "missing_mechanism_alignment"

    if out.empty:
        return out

    out["audit_rank"] = np.select(
        [out["audit_verdict"].eq("candidate"), out["audit_verdict"].eq("high_t_needs_manual_check")],
        [3, 2],
        default=1,
    )
    out["quality_score"] = (
        out["confidence_rank"] * 100.0
        + out["audit_rank"] * 20.0
        + pd.to_numeric(out["same_direction_share"], errors="coerce").fillna(0.5) * 10.0
        + pd.to_numeric(out["peer_direction_share"], errors="coerce").fillna(0.5) * 5.0
        + pd.to_numeric(out["max_abs_tstat"], errors="coerce").clip(upper=8.0)
        + pd.to_numeric(out["preferred_hit_rate"], errors="coerce").fillna(0.0)
        + np.select(
            [
                out["mechanism_gate_verdict"].eq("pass"),
                out["mechanism_gate_verdict"].eq("review"),
                out["mechanism_gate_verdict"].eq("conflict"),
            ],
            [10.0, 0.0, -25.0],
            default=0.0,
        )
    )
    out = out.sort_values(
        ["quality_score", "confidence_rank", "max_abs_tstat", "preferred_hit_rate"],
        ascending=[False, False, False, False],
    )
    out = out.drop_duplicates(["ticker", "commodity", "feature_family", "direction"], keep="first")
    if max_per_ticker > 0:
        out = out.groupby("ticker", group_keys=False, sort=False).head(max_per_ticker)

    out["selection_reason"] = np.where(
        out["audit_candidate"],
        "best_family_candidate_with_audit_support",
        "best_family_candidate_without_full_audit_support",
    )
    return out.sort_values(["quality_score", "ticker", "commodity"], ascending=[False, True, True]).reset_index(
        drop=True
    )


def write_frame(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix == ".parquet":
        df.to_parquet(output_path, index=False)
    elif output_path.suffix == ".csv":
        df.to_csv(output_path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")


def audit_forecast_from_paths(
    forecast_paths: list[Path],
    exposure_map_path: Path,
    reviewed_features_path: Path,
    output_path: Path,
    aggregate_sample: str | None = None,
    high_abs_t: float = 8.0,
    min_same_direction_share: float = 0.6,
    min_peer_direction_share: float = 0.6,
) -> pd.DataFrame:
    forecast = _read_many(forecast_paths)
    exposure = pd.read_csv(exposure_map_path) if exposure_map_path.exists() else pd.DataFrame()
    reviewed = load_reviewed_features(reviewed_features_path) if reviewed_features_path.exists() else pd.DataFrame()
    audit = build_forecast_audit(
        forecast=forecast,
        exposure_map=exposure,
        reviewed_features=reviewed,
        aggregate_sample=aggregate_sample,
        high_abs_t=high_abs_t,
        min_same_direction_share=min_same_direction_share,
        min_peer_direction_share=min_peer_direction_share,
    )
    write_frame(audit, output_path)
    return audit


def audit_sensitivity_falsification_from_paths(
    matrix_path: Path,
    output_path: Path,
    exposure_map_path: Path | None = None,
    min_abs_t: float = 2.0,
    min_nonoverlap_abs_t: float = 1.0,
    min_effective_observations: int = 20,
    max_overlap_inflation: float = 3.0,
    min_hit_rate_edge: float = 0.03,
) -> pd.DataFrame:
    matrix = load_frame(matrix_path)
    exposure = (
        pd.read_csv(exposure_map_path)
        if exposure_map_path is not None and exposure_map_path.exists()
        else pd.DataFrame()
    )
    audit = build_sensitivity_falsification_audit(
        matrix=matrix,
        exposure_map=exposure,
        min_abs_t=min_abs_t,
        min_nonoverlap_abs_t=min_nonoverlap_abs_t,
        min_effective_observations=min_effective_observations,
        max_overlap_inflation=max_overlap_inflation,
        min_hit_rate_edge=min_hit_rate_edge,
    )
    write_frame(audit, output_path)
    return audit


def audit_nonlinear_commodity_beta_from_paths(
    candidates_path: Path,
    equity_processed_path: Path,
    commodity_signals_path: Path | None,
    output_path: Path,
    exposure_map_path: Path | None = None,
    return_column: str = "residual_return_mktsec_w12m",
    commodity_return_column: str = "commodity_return_mktseccomm",
    commodity_signal_return_column: str = "front_log_ret_1d",
    lag_days: list[int] | tuple[int, ...] = (0, 1, 5, 10, 21),
    min_observations: int = 126,
    large_move_quantile: float = 0.80,
    volatility_window: int = 21,
    max_abs_lag_corr_threshold: float = 0.15,
    asymmetry_corr_diff_threshold: float = 0.15,
) -> pd.DataFrame:
    candidates = load_frame(candidates_path)
    equity_processed = load_frame(equity_processed_path)
    commodity_signals = (
        load_frame(commodity_signals_path)
        if commodity_signals_path is not None and commodity_signals_path.exists()
        else pd.DataFrame()
    )
    exposure = (
        pd.read_csv(exposure_map_path)
        if exposure_map_path is not None and exposure_map_path.exists()
        else pd.DataFrame()
    )
    audit = build_nonlinear_commodity_beta_audit(
        candidates=candidates,
        equity_processed=equity_processed,
        commodity_signals=commodity_signals,
        exposure_map=exposure,
        return_column=return_column,
        commodity_return_column=commodity_return_column,
        commodity_signal_return_column=commodity_signal_return_column,
        lag_days=lag_days,
        min_observations=min_observations,
        large_move_quantile=large_move_quantile,
        volatility_window=volatility_window,
        max_abs_lag_corr_threshold=max_abs_lag_corr_threshold,
        asymmetry_corr_diff_threshold=asymmetry_corr_diff_threshold,
    )
    write_frame(audit, output_path)
    return audit


def audit_exposure_taxonomy_from_paths(
    exposure_map_path: Path,
    role_taxonomy_path: Path,
    output_path: Path,
    candidates_path: Path | None = None,
    unmapped_output_path: Path | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    exposure = pd.read_csv(exposure_map_path)
    taxonomy = pd.read_csv(role_taxonomy_path) if role_taxonomy_path.exists() else pd.DataFrame()
    candidates = load_frame(candidates_path) if candidates_path is not None and candidates_path.exists() else None
    summary, unmapped = build_exposure_taxonomy_audit(
        exposure_map=exposure,
        role_taxonomy=taxonomy,
        candidates=candidates,
    )
    write_frame(summary, output_path)
    if unmapped_output_path is not None:
        write_frame(unmapped, unmapped_output_path)
    return summary, unmapped


def review_candidate_taxonomy_from_paths(
    candidates_path: Path,
    exposure_map_path: Path,
    role_taxonomy_path: Path,
    output_path: Path,
    mechanism_alignment_path: Path | None = None,
    min_mechanism_alignment_probability: float = 0.67,
    mechanism_review_band: float = 0.55,
) -> pd.DataFrame:
    candidates = load_frame(candidates_path)
    exposure = pd.read_csv(exposure_map_path)
    taxonomy = pd.read_csv(role_taxonomy_path) if role_taxonomy_path.exists() else pd.DataFrame()
    mechanism_alignment = (
        load_frame(mechanism_alignment_path)
        if mechanism_alignment_path is not None and mechanism_alignment_path.exists()
        else None
    )
    review = build_candidate_taxonomy_review(
        candidates=candidates,
        exposure_map=exposure,
        role_taxonomy=taxonomy,
        mechanism_alignment=mechanism_alignment,
        min_mechanism_alignment_probability=min_mechanism_alignment_probability,
        mechanism_review_band=mechanism_review_band,
    )
    write_frame(review, output_path)
    return review


def registry_turnover_from_paths(
    output_path: Path,
    detail_output_path: Path,
    registry_paths: list[Path] | None = None,
    reactions_path: Path | None = None,
    universe_path: Path | None = None,
    min_events: int = 30,
    min_abs_t: float = 3.0,
    min_same_direction_horizons: int = 2,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if registry_paths:
        snapshots = _read_many(registry_paths)
    elif reactions_path and universe_path:
        reactions = load_frame(reactions_path)
        seed = load_seed_universe(universe_path)
        snapshots = build_registry_snapshots_from_reactions(
            reactions=reactions,
            seed_universe=seed,
            min_events=min_events,
            min_abs_t=min_abs_t,
            min_same_direction_horizons=min_same_direction_horizons,
        )
    else:
        raise ValueError("Provide --registry at least once, or provide --reactions and --universe")
    summary, detail = build_registry_turnover(snapshots)
    write_frame(summary, output_path)
    write_frame(detail, detail_output_path)
    return summary, detail


def group_activation_scores_from_paths(
    registry_path: Path,
    commodity_signals_path: Path,
    exposure_map_path: Path,
    output_path: Path,
    as_of_date: str | None = None,
    activation_z: float = 1.0,
    feature_z_window: int = 252,
    min_feature_observations: int = 126,
    require_exposure: bool = True,
) -> pd.DataFrame:
    registry = load_frame(registry_path)
    commodity_signals = load_frame(commodity_signals_path)
    exposure = pd.read_csv(exposure_map_path)
    scores = build_group_activation_scores(
        registry=registry,
        commodity_signals=commodity_signals,
        exposure_map=exposure,
        as_of_date=as_of_date,
        activation_z=activation_z,
        feature_z_window=feature_z_window,
        min_feature_observations=min_feature_observations,
        require_exposure=require_exposure,
    )
    write_frame(scores, output_path)
    return scores


def consolidate_candidate_signals_from_paths(
    candidates_path: Path,
    output_path: Path,
    forecast_audit_path: Path | None = None,
    reviewed_features_path: Path | None = None,
    mechanism_alignment_path: Path | None = None,
    min_confidence: str = "medium",
    require_audit_candidate: bool = False,
    require_mechanism_pass: bool = False,
    block_mechanism_conflicts: bool = False,
    min_mechanism_alignment_probability: float = 0.67,
    mechanism_review_band: float = 0.55,
    min_same_direction_share: float = 0.6,
    min_peer_direction_share: float = 0.0,
    max_per_ticker: int = 3,
) -> pd.DataFrame:
    candidates = load_frame(candidates_path)
    forecast_audit = load_frame(forecast_audit_path) if forecast_audit_path and forecast_audit_path.exists() else None
    reviewed = (
        load_reviewed_features(reviewed_features_path)
        if reviewed_features_path and reviewed_features_path.exists()
        else None
    )
    mechanism_alignment = (
        load_frame(mechanism_alignment_path)
        if mechanism_alignment_path is not None and mechanism_alignment_path.exists()
        else None
    )
    consolidated = consolidate_candidate_signals(
        candidates=candidates,
        forecast_audit=forecast_audit,
        reviewed_features=reviewed,
        mechanism_alignment=mechanism_alignment,
        min_confidence=min_confidence,
        require_audit_candidate=require_audit_candidate,
        require_mechanism_pass=require_mechanism_pass,
        block_mechanism_conflicts=block_mechanism_conflicts,
        min_mechanism_alignment_probability=min_mechanism_alignment_probability,
        mechanism_review_band=mechanism_review_band,
        min_same_direction_share=min_same_direction_share,
        min_peer_direction_share=min_peer_direction_share,
        max_per_ticker=max_per_ticker,
    )
    write_frame(consolidated, output_path)
    return consolidated
