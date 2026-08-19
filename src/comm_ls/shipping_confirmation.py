from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

# ---- constants ----

SHIPPING_CONFIRMATION_COLUMNS = (
    "commodity",
    "date",
    "tradable_after",
    "source_type",
    "source_name",
    "metric",
    "value",
    "unit",
    "confirmation_pressure",
    "confirmation_strength",
    "confirmation_flag",
    "timestamp_quality",
    "source_detail",
)

DEFAULT_SHIPPING_TICKERS = ("DHT", "FRO", "TNK", "STNG", "INSW")
DEFAULT_CORRELATION_WINDOW = 63
DEFAULT_REGIME_WINDOW = 21


@dataclass(frozen=True)
class ShippingConfirmationConfig:
    commodity: str = "CL"
    carry_data_path: Path = Path("data/comm/carry_data/CL.csv")
    external_data_path: Path | None = None
    equity_prices_dir: Path = Path("data/equity/yfinance")
    shipping_tickers: tuple[str, ...] = DEFAULT_SHIPPING_TICKERS
    correlation_window: int = DEFAULT_CORRELATION_WINDOW
    regime_window: int = DEFAULT_REGIME_WINDOW
    output_path: Path = Path("data/processed/shipping_confirmation_events.csv")


# ---- external data schema ----

def _validate_external_columns(frame: pd.DataFrame, source_name: str) -> None:
    required = {"date", "value"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"{source_name} external data is missing columns: {sorted(missing)}")


def _read_external_csv(path: Path, source_name: str) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"external shipping data not found: {path}")
    frame = pd.read_csv(path, parse_dates=["date"]).sort_values("date").reset_index(drop=True)
    _validate_external_columns(frame, source_name)
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce").dt.normalize()
    frame["value"] = pd.to_numeric(frame["value"], errors="coerce")
    return frame


# ---- shipping composite proxy (used when external data unavailable) ----

def _load_shipping_stock_composite(
    prices_dir: Path,
    tickers: tuple[str, ...],
) -> pd.DataFrame:
    frames = []
    for ticker in tickers:
        path = prices_dir / f"{ticker}.csv"
        if not path.exists():
            continue
        df = pd.read_csv(path, parse_dates=["date"]).drop_duplicates(subset=["date"]).sort_values("date")
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.normalize()
        close = pd.to_numeric(df["adj_close"], errors="coerce")
        ret = np.log(close / close.shift(1))
        ret.index = df["date"]; frames.append(ret.rename(ticker))
    if not frames:
        raise FileNotFoundError(f"no shipping stock price files found under {prices_dir}")
    composite = pd.concat(frames, axis=1).ffill().mean(axis=1, skipna=True)
    equity_sessions = composite.dropna().index
    return pd.DataFrame({"date": equity_sessions, "value": composite.loc[equity_sessions].values})


# ---- core analysis ----

def compute_rolling_correlation(
    carry_series: pd.Series,
    target_series: pd.Series,
    window: int = DEFAULT_CORRELATION_WINDOW,
) -> pd.Series:
    aligned = pd.DataFrame({"carry": carry_series, "target": target_series}).dropna()
    if len(aligned) < window:
        return pd.Series(np.nan, index=aligned.index, dtype=float)
    rolling_corr = aligned["carry"].rolling(window).corr(aligned["target"])
    return rolling_corr


def compute_rolling_regime_z(
    series: pd.Series,
    window: int = DEFAULT_REGIME_WINDOW,
    long_window: int = 252,
) -> pd.DataFrame:
    short_ma = series.rolling(window, min_periods=window // 2).mean()
    long_ma = series.rolling(long_window, min_periods=long_window // 2).mean()
    long_std = series.rolling(long_window, min_periods=long_window // 2).std()
    diffusion = short_ma - long_ma
    zscore = diffusion / long_std.where(long_std > 0)
    return pd.DataFrame(
        {"regime_diffusion": diffusion, "regime_z": zscore, "value": series},
        index=series.index,
    )


def _tradable_after(date_series: pd.Series, lag_days: int = 1) -> pd.Series:
    return date_series + pd.to_timedelta(lag_days, unit="D")


def build_shipping_confirmation_events(
    config: ShippingConfirmationConfig,
) -> pd.DataFrame:
    carry = pd.read_csv(config.carry_data_path, parse_dates=["date"])
    carry["date"] = pd.to_datetime(carry["date"], errors="coerce").dt.normalize()
    carry_series = carry.set_index("date")["carry"].sort_index()
    carry_series = pd.to_numeric(carry_series, errors="coerce")

    if config.external_data_path is not None:
        external = _read_external_csv(config.external_data_path, "external_shipping")
        target = external.set_index("date")["value"].sort_index()
        source_type = "shipping_external"
        source_name = config.external_data_path.stem
        metric = "external_rate"
        unit = "index"
        source_detail = f"external shipping data from {config.external_data_path}"
    else:
        target = _load_shipping_stock_composite(
            config.equity_prices_dir, config.shipping_tickers
        ).set_index("date")["value"].sort_index()
        target = pd.to_numeric(target, errors="coerce")
        source_type = "shipping_stock_proxy"
        source_name = "shipping_stock_composite"
        metric = "equal_weight_log_return"
        unit = "log_return"
        source_detail = (
            f"equal-weighted daily log return of "
            f"{','.join(config.shipping_tickers)}; "
            f"proxy for tanker market health — replace with Clarksons/BDTI data"
        )

    common_idx = carry_series.dropna().index.intersection(target.dropna().index)
    carry_aligned = carry_series.reindex(common_idx)
    target_aligned = target.reindex(common_idx)

    corr = compute_rolling_correlation(
        carry_aligned, target_aligned, config.correlation_window
    )
    regime = compute_rolling_regime_z(
        target_aligned, config.regime_window
    )

    events = pd.DataFrame(
        {
            "date": common_idx,
            "carry": carry_aligned.values,
            "target_value": target_aligned.values,
            "rolling_correlation": corr.reindex(common_idx).values,
            "regime_z": regime["regime_z"].reindex(common_idx).values,
            "regime_diffusion": regime["regime_diffusion"].reindex(common_idx).values,
        }
    )
    events.dropna(subset=["carry", "target_value"], inplace=True)

    events["tradable_after"] = _tradable_after(events["date"], lag_days=1)
    events["source_type"] = source_type
    events["source_name"] = source_name
    events["metric"] = metric
    events["unit"] = unit
    events["source_detail"] = source_detail

    events["confirmation_pressure"] = np.where(
        events["regime_z"] > 0, 1.0, np.where(events["regime_z"] < 0, -1.0, 0.0)
    )
    events["confirmation_strength"] = events["rolling_correlation"].abs()

    corr_available = events["rolling_correlation"].notna()
    pos_corr = events["rolling_correlation"] > 0
    neg_corr = events["rolling_correlation"] < 0
    regime_positive = events["regime_z"] > 0
    regime_negative = events["regime_z"] < 0

    events["confirmation_flag"] = "no_signal"
    events.loc[corr_available & pos_corr & regime_positive, "confirmation_flag"] = "confirm"
    events.loc[corr_available & neg_corr & regime_negative, "confirmation_flag"] = "confirm"
    events.loc[corr_available & pos_corr & regime_negative, "confirmation_flag"] = "warn"
    events.loc[corr_available & neg_corr & regime_positive, "confirmation_flag"] = "warn"
    events.loc[~corr_available, "confirmation_flag"] = "unknown"
    events.loc[events["regime_z"].abs() < 0.5, "confirmation_flag"] = "neutral"

    events["commodity"] = config.commodity.upper().strip()
    events["timestamp_quality"] = "date_plus_one_session"
    events["value"] = events["target_value"]

    extra_columns = ["rolling_correlation", "regime_z", "regime_diffusion", "carry", "target_value"]
    all_columns = list(SHIPPING_CONFIRMATION_COLUMNS) + [col for col in extra_columns if col in events.columns]
    output = events[all_columns].copy()
    return output.sort_values(["commodity", "date"]).reset_index(drop=True)


def build_shipping_confirmation_events_from_paths(
    carry_data_path: Path,
    shipping_data_path: Path | None,
    equity_prices_dir: Path,
    output_path: Path,
    commodity: str = "CL",
    correlation_window: int = DEFAULT_CORRELATION_WINDOW,
    regime_window: int = DEFAULT_REGIME_WINDOW,
) -> pd.DataFrame:
    config = ShippingConfirmationConfig(
        commodity=commodity,
        carry_data_path=carry_data_path,
        external_data_path=shipping_data_path,
        equity_prices_dir=equity_prices_dir,
        correlation_window=correlation_window,
        regime_window=regime_window,
        output_path=output_path,
    )
    events = build_shipping_confirmation_events(config)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    events.to_csv(output_path, index=False)
    return events


# ---- diagnostic summary ----

def _safe_round(value: float, decimals: int = 3) -> float:
    if pd.isna(value) or np.isinf(value):
        return float("nan")
    return round(float(value), decimals)


def summarize_shipping_confirmation(
    events: pd.DataFrame,
    lookback_months: int = 12,
) -> dict:
    if events.empty:
        return {"error": "no confirmation events available"}

    events["date"] = pd.to_datetime(events["date"], errors="coerce")
    cutoff = events["date"].max() - pd.DateOffset(months=lookback_months)
    recent = events[events["date"] >= cutoff].copy()
    if recent.empty:
        recent = events.tail(252).copy()

    flag_counts = recent["confirmation_flag"].value_counts().to_dict()
    recent_corr = recent["rolling_correlation"].dropna()
    recent_regime = recent["regime_z"].dropna()

    latest = events.iloc[-1] if len(events) > 0 else None

    return {
        "total_observations": len(events),
        "recent_window": f"{recent['date'].min().date()} to {recent['date'].max().date()}",
        "recent_observations": len(recent),
        "latest_date": str(latest["date"].date()) if latest is not None else "none",
        "latest_correlation": _safe_round(latest["rolling_correlation"]) if latest is not None else float("nan"),
        "latest_regime_z": _safe_round(latest["regime_z"]) if latest is not None else float("nan"),
        "latest_flag": str(latest["confirmation_flag"]) if latest is not None else "none",
        "recent_mean_correlation": _safe_round(recent_corr.mean()),
        "recent_std_correlation": _safe_round(recent_corr.std()),
        "recent_mean_regime_z": _safe_round(recent_regime.mean()),
        "flag_counts": {str(k): int(v) for k, v in flag_counts.items()},
        "source_type": str(events["source_type"].iloc[0]) if "source_type" in events.columns else "unknown",
    }
