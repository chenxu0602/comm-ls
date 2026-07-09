from __future__ import annotations

import math
from collections.abc import Mapping

import numpy as np
import pandas as pd


def estimate_dollar_volume_liquidity(
    frame: pd.DataFrame,
    *,
    adv_window: int = 63,
    adv_min_periods: int = 40,
    stress_lookback: int = 252,
    stress_quantile: float = 0.25,
) -> pd.Series:
    """Estimate current and stressed trailing median dollar volume."""
    required = {"date", "close", "volume"}
    missing = sorted(required - set(frame.columns))
    if missing:
        raise ValueError(f"price frame is missing required columns: {missing}")
    if adv_window <= 0 or adv_min_periods <= 0 or stress_lookback <= 0:
        raise ValueError("ADV windows and minimum periods must be positive")
    if not 0.0 <= stress_quantile <= 1.0:
        raise ValueError("stress_quantile must be between 0 and 1")

    data = frame[["date", "close", "volume"]].copy()
    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    data["close"] = pd.to_numeric(data["close"], errors="coerce")
    data["volume"] = pd.to_numeric(data["volume"], errors="coerce")
    data = data.dropna(subset=["date"]).sort_values("date").drop_duplicates("date", keep="last")
    dollar_volume = data["close"].where(data["close"] > 0) * data["volume"].where(data["volume"] >= 0)
    adv = dollar_volume.rolling(adv_window, min_periods=adv_min_periods).median().shift(1)
    valid = adv.dropna()
    if valid.empty:
        raise ValueError("price frame does not contain enough valid observations for ADV")

    latest_position = valid.index[-1]
    trailing = valid.loc[:latest_position].tail(stress_lookback)
    return pd.Series(
        {
            "price_date": data.loc[latest_position, "date"],
            "latest_close": data.loc[latest_position, "close"],
            "latest_adv_usd": valid.loc[latest_position],
            "stressed_adv_usd": trailing.quantile(stress_quantile),
            "stress_observations": int(trailing.count()),
        }
    )


def capacity_metrics(
    *,
    target_weight: float,
    adv_usd: float,
    aum_usd: float,
    participation_limit: float,
    execution_days: int,
    weight_change_multiplier: float,
    max_weight: float | None = None,
) -> Mapping[str, float]:
    """Calculate participation, capacity, and liquidity-constrained weight."""
    weight = abs(float(target_weight))
    adv = float(adv_usd)
    aum = float(aum_usd)
    limit = float(participation_limit)
    days = int(execution_days)
    multiplier = float(weight_change_multiplier)
    if adv <= 0 or aum <= 0 or days <= 0 or multiplier <= 0:
        raise ValueError("ADV, AUM, execution_days, and multiplier must be positive")
    if not 0 < limit <= 1:
        raise ValueError("participation_limit must be in (0, 1]")

    weight_change = weight * multiplier
    daily_trade_usd = aum * weight_change / days
    daily_participation = daily_trade_usd / adv
    capacity_aum = np.inf if weight_change == 0 else limit * adv * days / weight_change
    liquidity_weight_cap = limit * adv * days / (aum * multiplier)
    if max_weight is not None:
        liquidity_weight_cap = min(liquidity_weight_cap, float(max_weight))
    required_days = 0 if weight_change == 0 else math.ceil(aum * weight_change / (limit * adv))
    return {
        "weight_change": weight_change,
        "daily_trade_usd": daily_trade_usd,
        "daily_participation": daily_participation,
        "capacity_aum_usd": capacity_aum,
        "liquidity_weight_cap": liquidity_weight_cap,
        "required_execution_days": float(required_days),
    }
