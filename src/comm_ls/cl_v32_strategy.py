from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


# These features are mathematically undefined during part of their calendar
# cycle. An explicit NaN is therefore a state boundary, not a missing quote to
# carry forward. Dates absent from the commodity calendar may still inherit the
# latest valid observation.
RESET_ON_EXPLICIT_NAN_FEATURES = frozenset(
    {
        "calendar_dec_annualized_carry",
        "next_dec_annualized_carry_gap_le_9m_v2",
    }
)
CL_V32_MAX_SINGLE_NAME_WEIGHT = 0.05
CHEMICAL_INFLECTION_LOOKBACK_DAYS = 30
CHEMICAL_LONG_EXIT_LEVEL = -0.01
CHEMICAL_SHORT_EXIT_LEVEL = -0.05
SHIPPING_CARRY_CHANGE_LOOKBACK_DAYS = 20
SHIPPING_CARRY_CHANGE_RESET_LEVEL = 0.01
SHIPPING_MOMENTUM_FEATURE = "front_log_ret_5d_v2"
SERVICE_VOL_LOOKBACK_DAYS = 60
SERVICE_VOL_MIN_PERIODS = 30
SERVICE_ENTRY_VOL_MULTIPLE = 2.0
SERVICE_EXIT_VOL_MULTIPLE = 1.0


@dataclass(frozen=True)
class SleeveConfig:
    weight: float
    tickers: tuple[str, ...]
    feature_symbol: str
    feature: str
    threshold: float
    side_mult: int
    position_mode: str
    hold_days: int | None
    rolling_days: int | None
    sector_hedge: str | None
    internal_weights: dict[str, float]
    signal_rule: str = "hysteresis"
    auxiliary_features: tuple[str, ...] = ()


# Source of truth: notebooks/backtest_cl.ipynb, cells 1 and 4-11.
# The position modes below intentionally reflect the notebook's executed code,
# which is not always the same as the descriptive mode stored in cell 1.
CL_V32_SLEEVE_CONFIG: dict[str, SleeveConfig] = {
    "psx_ref": SleeveConfig(
        weight=0.05,
        tickers=("PSX",),
        feature_symbol="CL",
        feature="activity_deferred_annualized_carry_chg_21d",
        threshold=0.01,
        side_mult=1,
        position_mode="rolling_mean",
        hold_days=None,
        rolling_days=5,
        sector_hedge="XLE",
        internal_weights={"PSX": 1.00},
    ),
    "refiner": SleeveConfig(
        weight=0.10,
        tickers=("DINO", "DK", "PBF"),
        feature_symbol="HO",
        feature="front_third_annualized_carry_chg_21d",
        threshold=0.01,
        side_mult=1,
        position_mode="rolling_mean",
        hold_days=None,
        rolling_days=5,
        sector_hedge="XLE",
        internal_weights={"DK": 0.40, "DINO": 0.30, "PBF": 0.30},
    ),
    "fuel": SleeveConfig(
        weight=0.04,
        tickers=("MUSA", "CASY"),
        feature_symbol="XB",
        feature="front_third_annualized_carry",
        threshold=0.06,
        side_mult=-1,
        position_mode="fixed_hold",
        hold_days=10,
        rolling_days=None,
        sector_hedge=None,
        internal_weights={"MUSA": 0.40, "CASY": 0.60},
    ),
    "services": SleeveConfig(
        weight=0.10,
        tickers=("FTI", "OII", "SLB", "HAL"),
        feature_symbol="CL",
        feature="carry_chg_21d",
        threshold=0.10,
        side_mult=-1,
        position_mode="rolling_mean",
        hold_days=None,
        rolling_days=2,
        sector_hedge="XLE",
        internal_weights={"FTI": 0.25, "OII": 0.25, "SLB": 0.25, "HAL": 0.25},
        signal_rule="service_volatility_hysteresis",
    ),
    "shipping": SleeveConfig(
        weight=0.25,
        tickers=("DHT", "FRO", "TNK", "STNG", "INSW"),
        feature_symbol="CL",
        feature="carry",
        threshold=0.01,
        side_mult=-1,
        position_mode="rolling_mean",
        hold_days=None,
        rolling_days=5,
        sector_hedge="XLE",
        internal_weights={
            "DHT": 0.30,
            "FRO": 0.30,
            "TNK": 0.15,
            "STNG": 0.05,
            "INSW": 0.20,
        },
        signal_rule="shipping_sticky",
        auxiliary_features=(SHIPPING_MOMENTUM_FEATURE,),
    ),
    "chemical": SleeveConfig(
        weight=0.28,
        tickers=("AVNT", "CE", "DOW", "EMN", "HUN", "LYB", "WLK"),
        feature_symbol="CL",
        feature="carry",
        threshold=0.02,
        side_mult=1,
        position_mode="fixed_hold",
        hold_days=21,
        rolling_days=None,
        sector_hedge="XLE",
        internal_weights={
            "AVNT": 0.05,
            "CE": 0.10,
            "DOW": 0.20,
            "EMN": 0.10,
            "HUN": 0.10,
            "LYB": 0.25,
            "WLK": 0.20,
        },
        signal_rule="chemical_inflection",
    ),
    "metals": SleeveConfig(
        weight=0.10,
        tickers=("ATI", "CRS"),
        feature_symbol="CL",
        feature="next_dec_annualized_carry_gap_le_9m_v2",
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
        tickers=("ERO", "TECK"),
        feature_symbol="CL",
        feature="brent_wti_carry_spread",
        threshold=0.02,
        side_mult=-1,
        position_mode="fixed_hold",
        hold_days=21,
        rolling_days=None,
        sector_hedge="XME",
        internal_weights={"ERO": 0.50, "TECK": 0.50},
    ),
}


def validate_config(config: dict[str, SleeveConfig]) -> None:
    for sleeve, cfg in config.items():
        if not cfg.feature_symbol.strip():
            raise ValueError(f"{sleeve} feature_symbol is empty")
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
        if cfg.signal_rule not in {
            "hysteresis",
            "chemical_inflection",
            "shipping_sticky",
            "service_volatility_hysteresis",
        }:
            raise ValueError(f"{sleeve} has unknown signal rule {cfg.signal_rule}")
        if cfg.signal_rule == "shipping_sticky" and SHIPPING_MOMENTUM_FEATURE not in cfg.auxiliary_features:
            raise ValueError(f"{sleeve} shipping_sticky rule requires {SHIPPING_MOMENTUM_FEATURE}")


def normalize_index(index: pd.Index) -> pd.DatetimeIndex:
    out = pd.to_datetime(index, errors="coerce")
    if getattr(out, "tz", None) is not None:
        out = out.tz_convert(None)
    return out.normalize()


def index_features_by_arrival(frame: pd.DataFrame, features: list[str]) -> pd.DataFrame:
    """Index commodity features by their first known date, not settlement date."""
    required = {"date", "arrival", *features}
    missing = sorted(required - set(frame.columns))
    if missing:
        raise KeyError(f"Missing commodity signal columns: {missing}")

    out = frame[["date", "arrival", *features]].copy()
    out["date"] = pd.to_datetime(out["date"], errors="coerce")
    out["arrival"] = pd.to_datetime(out["arrival"], errors="coerce")
    out["known_date"] = out["arrival"].dt.normalize()
    out = out.dropna(subset=["date", "arrival", "known_date"])
    out = out.sort_values(["known_date", "arrival", "date"]).drop_duplicates("known_date", keep="last")
    return out.set_index("known_date")[features].sort_index()


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


def chemical_inflection_signal(feature: pd.Series) -> pd.Series:
    """Build the notebook's asymmetric carry-inflection state for chemicals."""
    value = pd.to_numeric(feature, errors="coerce")
    change = value.diff(CHEMICAL_INFLECTION_LOOKBACK_DAYS)
    long_state = pd.Series(np.nan, index=value.index, dtype=float)
    short_state = pd.Series(np.nan, index=value.index, dtype=float)

    long_state.loc[(change < 0.0) & (value > 0.0)] = 1.0
    long_state.loc[value <= CHEMICAL_LONG_EXIT_LEVEL] = 0.0
    short_state.loc[(change > 0.0) & (value < 0.0)] = -1.0
    short_state.loc[value >= CHEMICAL_SHORT_EXIT_LEVEL] = 0.0

    invalid = value.isna()
    long_state.loc[invalid] = 0.0
    short_state.loc[invalid] = 0.0
    return long_state.ffill().fillna(0.0) + short_state.ffill().fillna(0.0)


def shipping_sticky_signal(carry: pd.Series, momentum: pd.Series) -> pd.Series:
    """Build the notebook's sticky CL carry/momentum state for tanker equities."""
    carry = pd.to_numeric(carry, errors="coerce")
    momentum = pd.to_numeric(momentum, errors="coerce")
    carry_change = carry.diff(SHIPPING_CARRY_CHANGE_LOOKBACK_DAYS)

    long_entry = (momentum < 0.0) & (carry < 0.0)
    short_entry = (momentum > 0.0) & (carry > 0.0)
    reset_state = carry_change > SHIPPING_CARRY_CHANGE_RESET_LEVEL
    invalid = carry.isna() | momentum.isna()

    # Priority matches the notebook: short entry, reset, then long entry.
    state_update = pd.Series(np.nan, index=carry.index, dtype=float)
    state_update.loc[long_entry] = 1.0
    state_update.loc[reset_state] = 0.0
    state_update.loc[short_entry] = -1.0
    state_update.loc[invalid] = 0.0
    return state_update.ffill().fillna(0.0)


def service_volatility_hysteresis_signal(feature: pd.Series, cfg: SleeveConfig) -> pd.Series:
    """Build the notebook's volatility-scaled CL carry-change state for services."""
    value = pd.to_numeric(feature, errors="coerce")
    volatility = value.rolling(
        SERVICE_VOL_LOOKBACK_DAYS,
        min_periods=SERVICE_VOL_MIN_PERIODS,
    ).std()
    long_state = pd.Series(np.nan, index=value.index, dtype=float)
    short_state = pd.Series(np.nan, index=value.index, dtype=float)

    long_state.loc[value > volatility * SERVICE_ENTRY_VOL_MULTIPLE] = float(cfg.side_mult)
    long_state.loc[value < -volatility * SERVICE_EXIT_VOL_MULTIPLE] = 0.0
    short_state.loc[value < -volatility * SERVICE_ENTRY_VOL_MULTIPLE] = float(-cfg.side_mult)
    short_state.loc[value > volatility * SERVICE_EXIT_VOL_MULTIPLE] = 0.0

    invalid = value.isna()
    long_state.loc[invalid] = 0.0
    short_state.loc[invalid] = 0.0
    return long_state.ffill().fillna(0.0) + short_state.ffill().fillna(0.0)


def sleeve_feature_names(cfg: SleeveConfig) -> tuple[str, ...]:
    return tuple(dict.fromkeys((cfg.feature, *cfg.auxiliary_features)))


def config_feature_names(config: dict[str, SleeveConfig]) -> list[str]:
    return sorted({feature for cfg in config.values() for feature in sleeve_feature_names(cfg)})


def config_feature_symbols(config: dict[str, SleeveConfig]) -> dict[str, str]:
    """Return the commodity symbol that should source each feature column.

    Feature columns are kept un-prefixed because downstream signal code expects
    notebook-equivalent names. If two sleeves later need the same feature name
    from different commodities, that ambiguity must be resolved explicitly
    before building production targets.
    """
    out: dict[str, str] = {}
    for sleeve, cfg in config.items():
        symbol = cfg.feature_symbol.upper()
        for feature in sleeve_feature_names(cfg):
            existing = out.get(feature)
            if existing is not None and existing != symbol:
                raise ValueError(
                    f"Feature {feature!r} is requested from both {existing} and {symbol}; "
                    f"cannot build un-prefixed production feature panel for sleeve {sleeve!r}"
                )
            out[feature] = symbol
    return out


def signal_from_features(features: pd.DataFrame, cfg: SleeveConfig) -> pd.Series:
    required = sleeve_feature_names(cfg)
    missing = sorted(set(required) - set(features.columns))
    if missing:
        raise KeyError(f"Missing features for {cfg.signal_rule}: {missing}")
    if cfg.signal_rule == "hysteresis":
        return hysteresis_signal(features[cfg.feature], cfg)
    if cfg.signal_rule == "chemical_inflection":
        return chemical_inflection_signal(features[cfg.feature]) * float(cfg.side_mult)
    if cfg.signal_rule == "shipping_sticky":
        return shipping_sticky_signal(features[cfg.feature], features[SHIPPING_MOMENTUM_FEATURE])
    if cfg.signal_rule == "service_volatility_hysteresis":
        return service_volatility_hysteresis_signal(features[cfg.feature], cfg)
    raise ValueError(f"Unknown signal rule: {cfg.signal_rule}")


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


def position_from_signal(signal: pd.Series, cfg: SleeveConfig) -> pd.Series:
    if cfg.position_mode == "sign":
        return signal.shift(1).fillna(0.0)
    if cfg.position_mode == "rolling_mean":
        return signal.rolling(cfg.rolling_days).mean().shift(1).fillna(0.0)
    if cfg.position_mode == "fixed_hold":
        return fixed_hold_position(signal, hold_days=int(cfg.hold_days))
    raise ValueError(f"Unknown position mode: {cfg.position_mode}")


def position_from_features(features: pd.DataFrame, cfg: SleeveConfig) -> pd.Series:
    return position_from_signal(signal_from_features(features, cfg), cfg)


def position_from_feature(feature: pd.Series, cfg: SleeveConfig) -> pd.Series:
    """Compatibility helper for sleeves using one generic hysteresis feature."""
    if cfg.signal_rule != "hysteresis" or cfg.auxiliary_features:
        raise ValueError(f"{cfg.signal_rule} requires position_from_features")
    return position_from_features(feature.to_frame(name=cfg.feature), cfg)


def build_stock_weights(
    features: pd.DataFrame,
    config: dict[str, SleeveConfig],
    availability: pd.DataFrame | None = None,
    max_single_name_weight: float | None = CL_V32_MAX_SINGLE_NAME_WEIGHT,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Build capped notebook-equivalent ticker weights on a shared market calendar."""
    validate_config(config)
    if max_single_name_weight is not None and max_single_name_weight <= 0:
        raise ValueError("max_single_name_weight must be positive or None")
    stock_weights: dict[str, pd.Series] = {}

    for sleeve, cfg in config.items():
        required_features = list(sleeve_feature_names(cfg))
        missing = sorted(set(required_features) - set(features.columns))
        if missing:
            raise KeyError(f"Missing features for {sleeve}: {missing}")
        for ticker in cfg.tickers:
            present = None
            if availability is not None and ticker in availability:
                present = availability[ticker].reindex(features.index).fillna(False).astype(bool)
                present_dates = present[present].index
                if present_dates.empty:
                    ticker_pos = pd.Series(0.0, index=features.index)
                else:
                    local_features = features.loc[present_dates, required_features]
                    ticker_pos = position_from_features(local_features, cfg).reindex(features.index).fillna(0.0)
                    ticker_pos = ticker_pos.where(present, 0.0)
            else:
                ticker_pos = position_from_features(features[required_features], cfg)

            weight = ticker_pos * cfg.internal_weights[ticker] * cfg.weight
            stock_weights[f"{sleeve}:{ticker}"] = weight

    weights = pd.DataFrame(stock_weights, index=features.index).fillna(0.0)
    if max_single_name_weight is not None:
        weights = weights.clip(-max_single_name_weight, max_single_name_weight)

    component_weights = {
        sleeve: weights[[col for col in weights if col.startswith(f"{sleeve}:")]].abs().sum(axis=1)
        for sleeve in config
    }
    return weights, pd.DataFrame(component_weights, index=features.index).fillna(0.0)


validate_config(CL_V32_SLEEVE_CONFIG)
