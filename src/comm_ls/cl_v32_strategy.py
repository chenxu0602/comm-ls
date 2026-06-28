from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


# These features are mathematically undefined during part of their calendar
# cycle. An explicit NaN is therefore a state boundary, not a missing quote to
# carry forward. Dates absent from the commodity calendar may still inherit the
# latest valid observation.
RESET_ON_EXPLICIT_NAN_FEATURES = frozenset({"calendar_dec_annualized_carry"})


@dataclass(frozen=True)
class SleeveConfig:
    weight: float
    tickers: tuple[str, ...]
    feature: str
    threshold: float
    side_mult: int
    position_mode: str
    hold_days: int | None
    rolling_days: int | None
    sector_hedge: str | None
    internal_weights: dict[str, float]


# Source of truth: notebooks/backtest_cl.ipynb, cells 1 and 4-11.
# The position modes below intentionally reflect the notebook's executed code,
# which is not always the same as the descriptive mode stored in cell 1.
CL_V32_SLEEVE_CONFIG: dict[str, SleeveConfig] = {
    "refiner": SleeveConfig(
        weight=0.24,
        tickers=("PSX", "DK", "DINO"),
        feature="liquid_deferred_annualized_carry_chg_21d",
        threshold=0.01,
        side_mult=1,
        position_mode="rolling_mean",
        hold_days=None,
        rolling_days=5,
        sector_hedge="XLE",
        internal_weights={"PSX": 0.40, "DK": 0.30, "DINO": 0.30},
    ),
    "fuel": SleeveConfig(
        weight=0.03,
        tickers=("MUSA", "CASY"),
        feature="front_third_spread",
        threshold=0.01,
        side_mult=1,
        position_mode="fixed_hold",
        hold_days=21,
        rolling_days=None,
        sector_hedge=None,
        internal_weights={"MUSA": 0.60, "CASY": 0.40},
    ),
    "services": SleeveConfig(
        weight=0.09,
        tickers=("FTI", "OII"),
        feature="carry_chg_21d",
        threshold=0.01,
        side_mult=-1,
        position_mode="rolling_mean",
        hold_days=None,
        rolling_days=2,
        sector_hedge="XLE",
        internal_weights={"FTI": 0.60, "OII": 0.40},
    ),
    "shipping": SleeveConfig(
        weight=0.23,
        tickers=("DHT", "FRO", "TNK", "STNG", "INSW"),
        feature="calendar_dec_annualized_carry",
        threshold=0.01,
        side_mult=-1,
        position_mode="sign",
        hold_days=None,
        rolling_days=None,
        sector_hedge="XLE",
        internal_weights={
            "DHT": 0.20,
            "FRO": 0.20,
            "TNK": 0.20,
            "STNG": 0.20,
            "INSW": 0.20,
        },
    ),
    "chemical": SleeveConfig(
        weight=0.22,
        tickers=("AVNT", "ASH", "CE", "DOW", "EMN", "HUN", "LYB", "WLK"),
        feature="carry",
        threshold=0.02,
        side_mult=1,
        position_mode="sign",
        hold_days=None,
        rolling_days=None,
        sector_hedge="XLE",
        internal_weights={
            "AVNT": 0.125,
            "ASH": 0.125,
            "CE": 0.125,
            "DOW": 0.125,
            "EMN": 0.125,
            "HUN": 0.125,
            "LYB": 0.125,
            "WLK": 0.125,
        },
    ),
    "metals": SleeveConfig(
        weight=0.11,
        tickers=("ATI", "CRS"),
        feature="calendar_dec_annualized_carry",
        threshold=0.015,
        side_mult=-1,
        position_mode="sign",
        hold_days=None,
        rolling_days=None,
        sector_hedge="XME",
        internal_weights={"ATI": 0.55, "CRS": 0.45},
    ),
    "bwt": SleeveConfig(
        weight=0.06,
        tickers=("ERO", "TECK", "NEXA"),
        feature="brent_wti_carry_spread",
        threshold=0.02,
        side_mult=-1,
        position_mode="fixed_hold",
        hold_days=21,
        rolling_days=None,
        sector_hedge="XME",
        internal_weights={"ERO": 0.33, "TECK": 0.33, "NEXA": 0.34},
    ),
}


def validate_config(config: dict[str, SleeveConfig]) -> None:
    for sleeve, cfg in config.items():
        if set(cfg.internal_weights) != set(cfg.tickers):
            raise ValueError(f"{sleeve} internal weights do not match its ticker list")
        if not np.isclose(sum(cfg.internal_weights.values()), 1.0):
            raise ValueError(f"{sleeve} internal weights must sum to 1")
        if cfg.position_mode == "fixed_hold" and not cfg.hold_days:
            raise ValueError(f"{sleeve} fixed_hold mode requires hold_days")
        if cfg.position_mode == "rolling_mean" and not cfg.rolling_days:
            raise ValueError(f"{sleeve} rolling_mean mode requires rolling_days")
        if cfg.position_mode not in {"sign", "fixed_hold", "rolling_mean"}:
            raise ValueError(f"{sleeve} has unknown position mode {cfg.position_mode}")


def normalize_index(index: pd.Index) -> pd.DatetimeIndex:
    out = pd.to_datetime(index, errors="coerce")
    if getattr(out, "tz", None) is not None:
        out = out.tz_convert(None)
    return out.normalize()


def align_features_to_calendar(features: pd.DataFrame, calendar: pd.Index) -> pd.DataFrame:
    """Align features while preserving explicit feature-invalid periods."""
    calendar = normalize_index(calendar)
    source = features.copy()
    source.index = normalize_index(source.index)
    source = source.groupby(source.index).last().sort_index()
    union = source.index.union(calendar).sort_values()
    aligned = source.reindex(union).ffill()

    for feature in RESET_ON_EXPLICIT_NAN_FEATURES.intersection(source.columns):
        # True/False is carried only across dates absent from the source. An
        # explicit source NaN flips the validity state to False until a new
        # valid observation arrives.
        valid_state = source[feature].notna().reindex(union).ffill().fillna(False)
        aligned[feature] = aligned[feature].where(valid_state)

    return aligned.reindex(calendar)


def hysteresis_signal(feature: pd.Series, cfg: SleeveConfig) -> pd.Series:
    """Build the notebook's threshold-entry, zero-crossing-exit signal."""
    value = pd.to_numeric(feature, errors="coerce")
    long_state = pd.Series(np.nan, index=value.index, dtype=float)
    short_state = pd.Series(np.nan, index=value.index, dtype=float)

    long_state.loc[value > cfg.threshold] = float(cfg.side_mult)
    long_state.loc[value < 0] = 0.0
    short_state.loc[value < -cfg.threshold] = float(-cfg.side_mult)
    short_state.loc[value > 0] = 0.0

    # An explicit invalid feature observation exits the state. When the feature
    # becomes valid again it must cross an entry threshold before re-entering.
    invalid = value.isna()
    long_state.loc[invalid] = 0.0
    short_state.loc[invalid] = 0.0

    signal = long_state.ffill().fillna(0.0) + short_state.ffill().fillna(0.0)
    signal.name = feature.name
    return signal


def fixed_hold_position(sig: pd.Series, hold_days: int, execution_lag: int = 1) -> pd.Series:
    values = sig.fillna(0.0).astype(float).to_numpy()
    pos = np.zeros(len(values), dtype=float)
    active_until = -1
    active_signal = 0.0

    for i, signal in enumerate(values):
        if signal == 0 or np.isnan(signal):
            continue
        start = i + execution_lag
        end = start + hold_days
        if start >= len(values):
            continue
        if i <= active_until:
            if signal == active_signal and start == active_until + 1:
                end = min(end, len(values))
                pos[start:end] = signal
                active_until = end - 1
            continue
        end = min(end, len(values))
        pos[start:end] = signal
        active_until = end - 1
        active_signal = signal

    return pd.Series(pos, index=sig.index, name=sig.name)


def position_from_feature(feature: pd.Series, cfg: SleeveConfig) -> pd.Series:
    signal = hysteresis_signal(feature, cfg)
    if cfg.position_mode == "sign":
        return signal.shift(1).fillna(0.0)
    if cfg.position_mode == "rolling_mean":
        return signal.rolling(cfg.rolling_days).mean().shift(1).fillna(0.0)
    if cfg.position_mode == "fixed_hold":
        return fixed_hold_position(signal, hold_days=int(cfg.hold_days))
    raise ValueError(f"Unknown position mode: {cfg.position_mode}")


def build_stock_weights(
    features: pd.DataFrame,
    config: dict[str, SleeveConfig],
    availability: pd.DataFrame | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Build notebook-equivalent ticker weights on a shared market calendar."""
    validate_config(config)
    stock_weights: dict[str, pd.Series] = {}
    component_weights: dict[str, pd.Series] = {}

    for sleeve, cfg in config.items():
        sleeve_weights = []
        for ticker in cfg.tickers:
            ticker_feature = features[cfg.feature]
            present = None
            if availability is not None and ticker in availability:
                present = availability[ticker].reindex(features.index).fillna(False).astype(bool)
                present_dates = present[present].index
                if present_dates.empty:
                    ticker_pos = pd.Series(0.0, index=features.index)
                else:
                    local_feature = ticker_feature.loc[present_dates]
                    ticker_pos = position_from_feature(local_feature, cfg).reindex(features.index).fillna(0.0)
                    ticker_pos = ticker_pos.where(present, 0.0)
            else:
                ticker_pos = position_from_feature(ticker_feature, cfg)

            weight = ticker_pos * cfg.internal_weights[ticker] * cfg.weight
            stock_weights[f"{sleeve}:{ticker}"] = weight
            sleeve_weights.append(weight.abs())

        component_weights[sleeve] = pd.concat(sleeve_weights, axis=1).sum(axis=1)

    return (
        pd.DataFrame(stock_weights, index=features.index).fillna(0.0),
        pd.DataFrame(component_weights, index=features.index).fillna(0.0),
    )


validate_config(CL_V32_SLEEVE_CONFIG)
