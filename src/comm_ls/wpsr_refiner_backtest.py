from __future__ import annotations

from pathlib import Path
from typing import Mapping, Sequence

import numpy as np
import pandas as pd


DEFAULT_WPSR_VINTAGE_PATH = Path("data/processed/eia/observations_vintage.csv")

# Capacity series are deliberately excluded. Weekly changes in operable capacity
# are structural metadata, not refinery operating pressure.
DEFAULT_REFINER_SERIES: dict[str, str] = {
    "WGIRIUS2": "refinery_input_us",
    "WPULEUS3": "refinery_utilization_us",
    "WGIRIP22": "refinery_input_padd2",
    "W_NA_YUP_R20_PER": "refinery_utilization_padd2",
    "WGIRIP32": "refinery_input_padd3",
    "W_NA_YUP_R30_PER": "refinery_utilization_padd3",
    "WGIRIP42": "refinery_input_padd4",
    "W_NA_YUP_R40_PER": "refinery_utilization_padd4",
    "WGFUPUS2": "gasoline_product_demand",
    "WDIUPUS2": "distillate_product_demand",
    "WKJUPUS2": "jet_product_demand",
    "W_EPC0_SAX_YCUOK_MBBL": "cushing_crude_tightness",
    "WCESTP31": "padd3_crude_tightness",
}

REFINERY_PRESSURE_COLUMNS = (
    "refinery_input_us",
    "refinery_utilization_us",
    "refinery_input_padd2",
    "refinery_utilization_padd2",
    "refinery_input_padd3",
    "refinery_utilization_padd3",
    "refinery_input_padd4",
    "refinery_utilization_padd4",
)
PRODUCT_DEMAND_COLUMNS = (
    "gasoline_product_demand",
    "distillate_product_demand",
)
CRUDE_TIGHTNESS_COLUMNS = (
    "cushing_crude_tightness",
    "padd3_crude_tightness",
)


def _row_mean_with_min_count(
    frame: pd.DataFrame,
    columns: Sequence[str],
    min_count: int,
) -> pd.Series:
    available = [column for column in columns if column in frame.columns]
    if not available:
        return pd.Series(np.nan, index=frame.index, dtype=float)
    values = frame[available].apply(pd.to_numeric, errors="coerce")
    result = values.mean(axis=1)
    return result.where(values.notna().sum(axis=1) >= min_count)


def _release_seasonal_state(
    group: pd.DataFrame,
    min_seasonal_observations: int,
) -> pd.DataFrame:
    """Calculate expanding, prior-year seasonal z-scores for one WPSR series."""
    out = group.sort_values(["source_vintage", "observation_period"]).copy()
    iso = out["observation_period"].dt.isocalendar()
    out["iso_year"] = iso.year.astype(int)
    out["iso_week"] = iso.week.astype(int)
    out["change_1_release"] = out["value"].diff()

    seasonal_z = pd.Series(np.nan, index=out.index, dtype=float)
    for idx, row in out.iterrows():
        week_distance = (out["iso_week"] - int(row["iso_week"])).abs()
        week_distance = np.minimum(week_distance, 53 - week_distance)
        prior = out.loc[
            (out["iso_year"] < int(row["iso_year"])) & (week_distance <= 2),
            "value",
        ].dropna()
        if len(prior) < min_seasonal_observations:
            continue
        std = prior.std(ddof=1)
        if pd.notna(std) and std > 0:
            seasonal_z.loc[idx] = (float(row["value"]) - prior.mean()) / std

    out["seasonal_z"] = seasonal_z
    out["physical_state_value"] = out["seasonal_z"]
    inventory = out["state_family"].eq("inventory_tightness")
    out.loc[inventory, "physical_state_value"] *= -1.0
    return out


def build_wpsr_refiner_release_states(
    vintage_path: Path | str = DEFAULT_WPSR_VINTAGE_PATH,
    *,
    series_map: Mapping[str, str] | None = None,
    min_seasonal_observations: int = 3,
) -> pd.DataFrame:
    """Build point-in-time WPSR refiner states, indexed by first tradable session.

    The function reads the append-only vintage table. For each series and
    release it selects that release's newest observation, then calculates the
    seasonal score using only prior release years. It intentionally does not
    read ``observations_latest.csv``.
    """
    mapping = dict(series_map or DEFAULT_REFINER_SERIES)
    required = [
        "series_id",
        "state_family",
        "observation_period",
        "source_vintage",
        "tradable_after",
        "value",
        "point_in_time_available",
    ]
    frame = pd.read_csv(vintage_path, usecols=required, low_memory=False)
    frame = frame[frame["series_id"].isin(mapping)].copy()
    missing_series = sorted(set(mapping).difference(frame["series_id"].unique()))
    if missing_series:
        raise ValueError(f"WPSR vintage data is missing series: {missing_series}")

    point_in_time = (
        frame["point_in_time_available"]
        .astype(str)
        .str.strip()
        .str.lower()
        .isin({"true", "1"})
    )
    if not point_in_time.all():
        bad = sorted(frame.loc[~point_in_time, "series_id"].unique())
        raise ValueError(f"Non-point-in-time WPSR rows are not allowed: {bad}")

    frame["value"] = pd.to_numeric(frame["value"], errors="coerce")
    frame["observation_period"] = pd.to_datetime(
        frame["observation_period"], errors="coerce"
    )
    frame["source_vintage"] = pd.to_datetime(frame["source_vintage"], errors="coerce")
    frame["tradable_after_utc"] = pd.to_datetime(
        frame["tradable_after"], errors="coerce", utc=True
    )
    frame = frame.dropna(
        subset=[
            "value",
            "observation_period",
            "source_vintage",
            "tradable_after_utc",
        ]
    )

    # A release contains the new current week and the previous week's revised
    # value. Use the current week to recreate what that release newly reported.
    release_rows = (
        frame.sort_values(["series_id", "source_vintage", "observation_period"])
        .groupby(["series_id", "source_vintage"], sort=False, as_index=False)
        .tail(1)
        .copy()
    )
    release_rows = pd.concat(
        [
            _release_seasonal_state(group, min_seasonal_observations)
            for _, group in release_rows.groupby("series_id", sort=False)
        ],
        ignore_index=True,
    )
    release_rows["state_name"] = release_rows["series_id"].map(mapping)
    release_rows["tradable_session"] = (
        release_rows["tradable_after_utc"]
        .dt.tz_convert("America/New_York")
        .dt.tz_localize(None)
        .dt.normalize()
    )

    states = release_rows.pivot_table(
        index="tradable_session",
        columns="state_name",
        values="physical_state_value",
        aggfunc="last",
    ).sort_index()
    states.columns.name = None
    release_dates = release_rows.groupby("tradable_session")["source_vintage"].max()
    states.insert(0, "wpsr_release_date", release_dates.reindex(states.index))
    states["refinery_pressure"] = _row_mean_with_min_count(
        states,
        REFINERY_PRESSURE_COLUMNS,
        min_count=4,
    )
    states["product_demand"] = _row_mean_with_min_count(
        states,
        PRODUCT_DEMAND_COLUMNS,
        min_count=2,
    )
    states["crude_tightness"] = _row_mean_with_min_count(
        states,
        CRUDE_TIGHTNESS_COLUMNS,
        min_count=2,
    )
    states.index.name = "date"
    return states


def align_wpsr_states_to_sessions(
    release_states: pd.DataFrame,
    sessions: Sequence[pd.Timestamp] | pd.Index,
    *,
    max_age_days: int = 10,
) -> pd.DataFrame:
    """Backward as-of join WPSR states to equity sessions with a freshness cap."""
    session_index = pd.DatetimeIndex(pd.to_datetime(sessions)).tz_localize(None)
    session_index = session_index.normalize().sort_values().unique()
    left = pd.DataFrame({"date": session_index})
    right = release_states.copy().reset_index().rename(columns={"date": "wpsr_state_date"})
    right["wpsr_state_date"] = pd.to_datetime(right["wpsr_state_date"]).dt.normalize()
    aligned = pd.merge_asof(
        left.sort_values("date"),
        right.sort_values("wpsr_state_date"),
        left_on="date",
        right_on="wpsr_state_date",
        direction="backward",
        tolerance=pd.Timedelta(days=max_age_days),
    )
    aligned["wpsr_age_days"] = (
        aligned["date"] - aligned["wpsr_state_date"]
    ).dt.days
    return aligned.set_index("date")


def build_wpsr_refiner_transition_signal(
    release_states: pd.DataFrame,
    sessions: Sequence[pd.Timestamp] | pd.Index,
    *,
    lookback_sessions: int = 30,
    max_age_days: int = 10,
    short_entry_pressure_change: float = 0.10,
    short_entry_tightness_change_floor: float = -0.02,
    short_exit_pressure_change: float = -0.05,
    short_exit_pressure_level: float = 1.0,
    long_entry_pressure_change: float = -0.10,
    long_entry_tightness_change_ceiling: float = 0.02,
    long_exit_pressure_change: float = 0.05,
    long_exit_pressure_level: float = -1.0,
) -> pd.DataFrame:
    """Build the research-only WPSR refinery transition signal.

    This reproduces the entry/reset rules first explored in ``eia2_data`` but
    applies them to point-in-time release states with a finite freshness cap.
    Exit/reset conditions have priority over entries when both occur on the
    same session, matching the original notebook assignment order.
    """
    if lookback_sessions <= 0:
        raise ValueError("lookback_sessions must be positive")

    out = align_wpsr_states_to_sessions(
        release_states,
        sessions,
        max_age_days=max_age_days,
    )
    required = ["refinery_pressure", "crude_tightness"]
    missing = sorted(set(required).difference(out.columns))
    if missing:
        raise ValueError(f"WPSR release states are missing columns: {missing}")

    out["refinery_pressure_change"] = out["refinery_pressure"].diff(
        lookback_sessions
    )
    out["crude_tightness_change"] = out["crude_tightness"].diff(
        lookback_sessions
    )

    short_entry = (
        out["refinery_pressure_change"].gt(short_entry_pressure_change)
        & out["crude_tightness_change"].gt(short_entry_tightness_change_floor)
    )
    short_exit = (
        out["refinery_pressure_change"].lt(short_exit_pressure_change)
        | out["refinery_pressure"].gt(short_exit_pressure_level)
    )
    long_entry = (
        out["refinery_pressure_change"].lt(long_entry_pressure_change)
        & out["crude_tightness_change"].lt(long_entry_tightness_change_ceiling)
    )
    long_exit = (
        out["refinery_pressure_change"].gt(long_exit_pressure_change)
        | out["refinery_pressure"].lt(long_exit_pressure_level)
    )
    invalid = out[required].isna().any(axis=1) | out[
        ["refinery_pressure_change", "crude_tightness_change"]
    ].isna().any(axis=1)

    short_update = pd.Series(np.nan, index=out.index, dtype=float)
    short_update.loc[short_entry] = -1.0
    short_update.loc[short_exit] = 0.0
    short_update.loc[invalid] = 0.0

    long_update = pd.Series(np.nan, index=out.index, dtype=float)
    long_update.loc[long_entry] = 1.0
    long_update.loc[long_exit] = 0.0
    long_update.loc[invalid] = 0.0

    out["sig_S"] = short_update.ffill().fillna(0.0)
    out["sig_L"] = long_update.ffill().fillna(0.0)
    out["signal"] = out["sig_S"] + out["sig_L"]
    out["short_entry"] = short_entry & ~short_exit & ~invalid
    out["short_exit"] = short_exit & ~invalid
    out["long_entry"] = long_entry & ~long_exit & ~invalid
    out["long_exit"] = long_exit & ~invalid
    out["signal_valid"] = ~invalid
    return out


def expand_signal_to_ticker_weights(
    signal: pd.Series,
    ticker_weights: Mapping[str, float],
) -> pd.DataFrame:
    """Expand one common sleeve signal into normalized ticker-level weights."""
    if not ticker_weights:
        raise ValueError("ticker_weights cannot be empty")
    weights = pd.Series(ticker_weights, dtype=float)
    if not np.isfinite(weights).all() or (weights < 0).any():
        raise ValueError("ticker_weights must be finite and non-negative")
    total = float(weights.sum())
    if total <= 0:
        raise ValueError("ticker_weights must have positive total weight")
    weights /= total
    values = pd.to_numeric(signal, errors="coerce").fillna(0.0)
    return pd.DataFrame(
        {ticker: values * weight for ticker, weight in weights.items()},
        index=values.index,
    )


def apply_refiner_wpsr_veto(
    baseline_positions: pd.DataFrame,
    release_states: pd.DataFrame,
    *,
    score_threshold: float = 1.0,
    max_age_days: int = 10,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Apply a research-only WPSR conflict veto without reversing positions.

    The preregistered experimental score is product demand minus refinery
    operating pressure. Positive values are treated as supportive for refiners;
    negative values are treated as margin-pressure risk. This is an economic
    hypothesis for falsification, not a production-approved equity direction.
    """
    if score_threshold <= 0:
        raise ValueError("score_threshold must be positive")

    positions = baseline_positions.copy().sort_index()
    positions.index = pd.DatetimeIndex(pd.to_datetime(positions.index)).tz_localize(None)
    states = align_wpsr_states_to_sessions(
        release_states,
        positions.index,
        max_age_days=max_age_days,
    )
    states["refiner_support_score"] = (
        states["product_demand"] - states["refinery_pressure"]
    )
    score = states["refiner_support_score"]
    states["eia_refiner_direction"] = np.select(
        [score >= score_threshold, score <= -score_threshold],
        [1.0, -1.0],
        default=0.0,
    )
    states.loc[score.isna(), "eia_refiner_direction"] = np.nan

    baseline_side = np.sign(positions.sum(axis=1)).rename("baseline_side")
    states["baseline_side"] = baseline_side.reindex(states.index).fillna(0.0)
    active = states["baseline_side"].ne(0)
    direction = states["eia_refiner_direction"]
    confirmed = active & direction.notna() & direction.eq(states["baseline_side"])
    conflicted = active & direction.notna() & direction.eq(-states["baseline_side"])
    missing = active & direction.isna()

    states["overlay_label"] = np.select(
        [~active, missing, confirmed, conflicted, active & direction.eq(0)],
        ["inactive", "missing", "confirmed", "conflicted", "neutral"],
        default="neutral",
    )
    veto_positions = positions.copy()
    veto_positions.loc[conflicted, :] = 0.0
    return veto_positions, states


def calculate_weighted_pnl(
    positions: pd.DataFrame,
    returns: pd.DataFrame,
    *,
    cost_bps: float = 25.0,
) -> pd.DataFrame:
    """Calculate portfolio daily PnL using the project's position convention."""
    pos, ret = positions.align(returns, join="inner", axis=0)
    pos, ret = pos.align(ret, join="inner", axis=1)
    gross_by_ticker = pos.shift(1).fillna(0.0).mul(ret)
    cost_by_ticker = pos.fillna(0.0).diff().fillna(0.0).abs() * cost_bps / 10_000.0
    return pd.DataFrame(
        {
            "gross_pnl": gross_by_ticker.sum(axis=1),
            "cost": cost_by_ticker.sum(axis=1),
            "net_pnl": (gross_by_ticker - cost_by_ticker).sum(axis=1),
            "turnover": pos.fillna(0.0).diff().fillna(0.0).abs().sum(axis=1),
        }
    )


def summarize_pnl(pnl: pd.Series) -> pd.Series:
    """Return compact additive-log-return statistics used by the notebook."""
    values = pd.to_numeric(pnl, errors="coerce").dropna()
    volatility = values.std(ddof=1)
    cumulative = values.cumsum()
    max_drawdown = (cumulative.cummax() - cumulative).max()
    return pd.Series(
        {
            "observations": len(values),
            "total_return": values.sum(),
            "annualized_return": values.mean() * 252,
            "annualized_vol": volatility * np.sqrt(252),
            "sharpe": values.mean() / volatility * np.sqrt(252)
            if volatility > 0
            else np.nan,
            "max_drawdown": max_drawdown,
        }
    )
