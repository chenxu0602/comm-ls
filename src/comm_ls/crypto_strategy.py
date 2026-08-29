from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

import numpy as np
import pandas as pd


CRYPTO_FEATURE_ALIGNMENT_MODE = "stock_observation_asof"
CRYPTO_MAX_SINGLE_NAME_WEIGHT = 0.12
CRYPTO_CACHE_DIR = Path("data/cache/feature_return_observation_v1")
CRYPTO_CACHE_SUFFIX = "_2"


@dataclass(frozen=True)
class CryptoSleeveConfig:
    weight: float
    symbol: str
    tickers: tuple[str, ...]
    internal_weights: Mapping[str, float]
    signal_builder: str
    signal_smoothing: int = 1


# Mirrors the executed portfolio cells in notebooks/backtest_btc_v43.ipynb.
CRYPTO_SLEEVE_CONFIG: dict[str, CryptoSleeveConfig] = {
    "platforms": CryptoSleeveConfig(
        weight=0.30,
        symbol="BTC",
        tickers=("COIN", "HOOD"),
        internal_weights={"COIN": 0.40, "HOOD": 0.60},
        signal_builder="platforms",
    ),
    "btc_momentum_vol_carry": CryptoSleeveConfig(
        weight=0.35,
        symbol="BTC",
        tickers=("MARA", "RIOT", "CLSK", "MSTR", "COIN", "HIVE"),
        internal_weights={
            "MARA": 0.15,
            "RIOT": 0.15,
            "CLSK": 0.20,
            "MSTR": 0.15,
            "COIN": 0.20,
            "HIVE": 0.15,
        },
        signal_builder="btc_momentum_vol_carry",
    ),
    "eth_momentum_vol_carry": CryptoSleeveConfig(
        weight=0.35,
        symbol="ETH",
        tickers=("MARA", "RIOT", "CLSK", "MSTR", "COIN", "HIVE"),
        internal_weights={
            "MARA": 0.15,
            "RIOT": 0.10,
            "CLSK": 0.20,
            "MSTR": 0.15,
            "COIN": 0.20,
            "HIVE": 0.20,
        },
        signal_builder="eth_momentum_vol_carry",
        signal_smoothing=2,
    ),
}


REQUIRED_FEATURES_BY_BUILDER: dict[str, tuple[str, ...]] = {
    "platforms": (
        "feature_value__front_log_ret_20d_v2",
        "feature_value__realized_vol_20d",
        "feature_value__carry_chg_10d",
        "feature_value__carry_chg_30d",
    ),
    "btc_momentum_vol_carry": (
        "feature_value__front_log_ret_10d_v2",
        "feature_value__realized_vol_20d",
        "feature_value__carry_chg_5d",
        "feature_value__carry_chg_10d",
    ),
    "eth_momentum_vol_carry": ("feature_value__front_log_ret_20d_v2",),
}


def validate_config() -> None:
    if not np.isclose(sum(cfg.weight for cfg in CRYPTO_SLEEVE_CONFIG.values()), 1.0):
        raise ValueError("Crypto sleeve weights must sum to 1")
    for name, cfg in CRYPTO_SLEEVE_CONFIG.items():
        if set(cfg.tickers) != set(cfg.internal_weights):
            raise ValueError(f"{name}: internal weights do not match tickers")
        if not np.isclose(sum(cfg.internal_weights.values()), 1.0):
            raise ValueError(f"{name}: internal weights must sum to 1")
        if cfg.signal_smoothing < 1:
            raise ValueError(f"{name}: signal_smoothing must be positive")


def cache_path(symbol: str, cache_dir: Path = CRYPTO_CACHE_DIR) -> Path:
    return cache_dir / f"{symbol.upper()}-multi_return{CRYPTO_CACHE_SUFFIX}.parquet"


def _load_ticker_features(
    path: Path,
    ticker: str,
    columns: tuple[str, ...],
) -> pd.DataFrame:
    required = [
        "date",
        "ticker",
        "commodity_feature_date",
        "commodity_arrival",
        "feature_alignment_mode",
        *columns,
    ]
    try:
        frame = pd.read_parquet(path, columns=required, filters=[("ticker", "=", ticker)])
    except Exception as exc:
        raise ValueError(f"Cannot load required crypto features from {path}: {exc}") from exc
    if frame.empty:
        raise ValueError(f"{ticker} is absent from {path}")
    modes = set(frame["feature_alignment_mode"].dropna().astype(str))
    if modes != {CRYPTO_FEATURE_ALIGNMENT_MODE}:
        raise ValueError(f"{path}: unexpected feature alignment modes {sorted(modes)}")
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce").dt.normalize()
    frame["commodity_feature_date"] = pd.to_datetime(
        frame["commodity_feature_date"], errors="coerce"
    ).dt.normalize()
    if frame["commodity_feature_date"].gt(frame["date"]).any():
        raise ValueError(f"{path}: commodity feature date is after stock date")
    return frame.dropna(subset=["date"]).sort_values("date").drop_duplicates("date", keep="last")


def _build_signal(frame: pd.DataFrame, builder: str) -> pd.Series:
    long_state = pd.Series(np.nan, index=frame.index, dtype=float)
    short_state = pd.Series(np.nan, index=frame.index, dtype=float)

    if builder == "btc_momentum_vol_carry":
        momentum = frame["feature_value__front_log_ret_10d_v2"]
        vol_change = frame["feature_value__realized_vol_20d"].diff(5)
        carry_5d = frame["feature_value__carry_chg_5d"]
        carry_10d = frame["feature_value__carry_chg_10d"]
        long_state.loc[(momentum < -0.02) & (vol_change > 0.0)] = -1.0
        long_state.loc[(carry_10d > 0.01) | (momentum > 0.01)] = 0.0
        short_state.loc[(momentum > 0.02) & (vol_change < 0.0)] = 1.0
        short_state.loc[(carry_5d < 0.01) | (momentum < -0.01)] = 0.0
    elif builder == "eth_momentum_vol_carry":
        magnitude = frame["feature_value__front_log_ret_20d_v2"].abs()
        long_state.loc[magnitude > 0.10] = -1.0
        long_state.loc[magnitude < 0.05] = 0.0
        short_state.loc[magnitude < 0.02] = 1.0
        short_state.loc[magnitude > 0.08] = 0.0
    elif builder == "platforms":
        momentum = frame["feature_value__front_log_ret_20d_v2"]
        vol = frame["feature_value__realized_vol_20d"]
        carry_10d = frame["feature_value__carry_chg_10d"]
        carry_30d = frame["feature_value__carry_chg_30d"]
        long_state.loc[(momentum > vol * 0.3) & (carry_30d > 0.01)] = 1.0
        long_state.loc[(momentum < -vol * 0.3) | (carry_10d < -0.01)] = 0.0
        short_state.loc[carry_30d < -0.01] = -0.5
        short_state.loc[carry_10d > 0.01] = 0.0
    else:
        raise ValueError(f"Unknown crypto signal builder: {builder}")

    return long_state.ffill().fillna(0.0) + short_state.ffill().fillna(0.0)


def build_component_targets(
    *,
    as_of: pd.Timestamp,
    target_date: pd.Timestamp,
    cache_dir: Path = CRYPTO_CACHE_DIR,
) -> tuple[pd.DataFrame, dict[str, pd.Timestamp], dict[str, Path]]:
    """Build next-session component weights using the notebook's one-session delay."""
    validate_config()
    as_of = pd.Timestamp(as_of).normalize()
    target_date = pd.Timestamp(target_date).normalize()
    rows: list[dict[str, object]] = []
    latest_dates: dict[str, pd.Timestamp] = {}
    source_paths: dict[str, Path] = {}

    for sleeve, cfg in CRYPTO_SLEEVE_CONFIG.items():
        path = cache_path(cfg.symbol, cache_dir)
        if not path.exists():
            raise FileNotFoundError(path)
        source_paths[cfg.symbol] = path
        required_features = REQUIRED_FEATURES_BY_BUILDER[cfg.signal_builder]
        sleeve_signals: dict[str, pd.Series] = {}
        frames: dict[str, pd.DataFrame] = {}
        for ticker in cfg.tickers:
            frame = _load_ticker_features(path, ticker, required_features)
            frame = frame.loc[frame["date"].le(as_of)].set_index("date")
            if frame.empty:
                raise ValueError(f"{sleeve}/{ticker}: no cache observation at or before {as_of.date()}")
            frames[ticker] = frame
            sleeve_signals[ticker] = _build_signal(frame, cfg.signal_builder)
            latest_dates[f"{cfg.symbol}_{ticker}"] = frame.index.max()

        signals = pd.DataFrame(sleeve_signals).sort_index()
        if cfg.signal_smoothing > 1:
            signals = signals.rolling(cfg.signal_smoothing).mean()

        for ticker in cfg.tickers:
            native = signals[ticker].dropna()
            if native.empty:
                raise ValueError(f"{sleeve}/{ticker}: no usable signal")
            # calc_pos_with_future(..., delay=1) makes the T+1 target equal to
            # the smoothed signal observed on T.
            signal = float(native.iloc[-1])
            internal_weight = float(cfg.internal_weights[ticker])
            research_weight = cfg.weight * internal_weight * signal
            frame = frames[ticker]
            rows.append(
                {
                    "as_of_date": as_of.date(),
                    "target_date": target_date.date(),
                    "component": sleeve,
                    "instrument": ticker,
                    "feature_symbol": cfg.symbol,
                    "signal_builder": cfg.signal_builder,
                    "signal_smoothing": cfg.signal_smoothing,
                    "signal": signal,
                    "sleeve_weight": cfg.weight,
                    "internal_weight": internal_weight,
                    "research_target_weight": research_weight,
                    "commodity_feature_date": frame["commodity_feature_date"].iloc[-1].date(),
                    "commodity_arrival": frame["commodity_arrival"].iloc[-1],
                    "signal_date": frame.index[-1].date(),
                }
            )

    return pd.DataFrame(rows), latest_dates, source_paths


def aggregate_and_cap_targets(component_targets: pd.DataFrame) -> pd.DataFrame:
    grouped = component_targets.groupby("instrument", sort=True)
    out = grouped.agg(
        component=("component", lambda x: "|".join(dict.fromkeys(x))),
        research_target_weight=("research_target_weight", "sum"),
        signal_date=("signal_date", "max"),
    ).reset_index()
    out["target_weight"] = out["research_target_weight"].clip(
        -CRYPTO_MAX_SINGLE_NAME_WEIGHT,
        CRYPTO_MAX_SINGLE_NAME_WEIGHT,
    )
    out["target_weight_adjustment"] = (
        out["target_weight"] - out["research_target_weight"]
    )
    return out
