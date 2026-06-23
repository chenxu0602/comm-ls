from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from comm_ls.commodity import load_carry_directory, load_carry_file
from comm_ls.equity import load_price_file
from comm_ls.sensitivity import _feature_z_scores
from comm_ls.universe import get_exposure_universe


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_QUARTERLY_UNIVERSE = PROJECT_ROOT / "data/processed/quarterly_universe.csv"
DEFAULT_EQUITY_DIR = PROJECT_ROOT / "data/equity/yfinance"
DEFAULT_COMMODITY_DIR = PROJECT_ROOT / "data/comm"
DEFAULT_CARRY_DIR = PROJECT_ROOT / "data/comm/carry_data"
DEFAULT_COMMODITY_SIGNALS = PROJECT_ROOT / "data/processed/commodity_signals.parquet"
DEFAULT_SEED_UNIVERSE = PROJECT_ROOT / "config/us_commodity_equity_seed.csv"
DEFAULT_COMMODITY_EXPOSURE_MAP = PROJECT_ROOT / "config/commodity_exposure_map.csv"
DEFAULT_THEME_HEDGES = PROJECT_ROOT / "config/theme_sector_hedges.csv"
DEFAULT_EQUITY_BETA_RETURNS = PROJECT_ROOT / "data/processed/equity_beta_returns.parquet"
DEFAULT_EQUITY_PROCESSED = PROJECT_ROOT / "data/processed/equity_processed.parquet"
DEFAULT_STOCK_FEATURE_MATRIX = PROJECT_ROOT / "data/processed/stock_feature_matrix.csv"
DEFAULT_QUARTERLY_FEATURE_MATRIX_DIR = PROJECT_ROOT / "data/matrix"
DEFAULT_FUNDAMENTAL_SNAPSHOT = PROJECT_ROOT / "data/processed/fundamental_snapshot.csv"
DEFAULT_FUNDAMENTAL_FACTORS = PROJECT_ROOT / "data/processed/fundamental_factors.csv"
DEFAULT_AGRICULTURE_FUNDAMENTAL_EVENTS = PROJECT_ROOT / "data/processed/agriculture_fundamental_events.csv"
DEFAULT_CL_COMMODITY_CONFIRMATION_EVENTS = PROJECT_ROOT / "data/processed/cl_commodity_confirmation_events.csv"


def _read_frame(path: Path) -> pd.DataFrame:
    if path.suffix == ".parquet":
        return pd.read_parquet(path)
    return pd.read_csv(path)


def _sort_and_maybe_index_by_date(df: pd.DataFrame, date_as_index: bool) -> pd.DataFrame:
    out = df.sort_values("date").reset_index(drop=True)
    if date_as_index:
        out = out.set_index("date")
        out.index.name = "date"
    return out


def get_tradeable_securities(
    as_of_date: str,
    period: str = "day",
    quarterly_universe_path: Path | str = DEFAULT_QUARTERLY_UNIVERSE,
) -> pd.DataFrame:
    """Return the tradeable securities for a date or month.

    For `period="day"`, this returns the latest quarterly universe with
    `rebalance_date <= as_of_date`.

    For `period="month"`, this returns the union of active securities across
    every available trading date in the input month.
    """

    path = Path(quarterly_universe_path)
    universe = _read_frame(path)
    if universe.empty:
        return universe

    universe = universe.copy()
    universe["rebalance_date"] = pd.to_datetime(universe["rebalance_date"], utc=False)
    target = pd.Timestamp(as_of_date)

    if period == "day":
        available = universe[universe["rebalance_date"] <= target]
        if available.empty:
            return universe.iloc[0:0].copy()
        active_date = available["rebalance_date"].max()
        out = available[available["rebalance_date"] == active_date].copy()
        out.insert(0, "as_of_date", target)
        return out.sort_values(["theme", "ticker"]).reset_index(drop=True)

    if period == "month":
        month_start = target.to_period("M").start_time
        month_end = target.to_period("M").end_time
        month_rebalances = universe[
            (universe["rebalance_date"] >= month_start) & (universe["rebalance_date"] <= month_end)
        ]

        before_month = universe[universe["rebalance_date"] < month_start]
        frames: list[pd.DataFrame] = []
        if not before_month.empty:
            active_date = before_month["rebalance_date"].max()
            frames.append(before_month[before_month["rebalance_date"] == active_date])
        if not month_rebalances.empty:
            frames.append(month_rebalances)
        if not frames:
            return universe.iloc[0:0].copy()

        out = pd.concat(frames, ignore_index=True).drop_duplicates("ticker")
        out.insert(0, "month", month_start.date().isoformat())
        return out.sort_values(["theme", "ticker"]).reset_index(drop=True)

    raise ValueError("period must be 'day' or 'month'")


def get_equity_history(
    ticker: str,
    prices_dir: Path | str = DEFAULT_EQUITY_DIR,
    drop_missing_close: bool = True,
    include_beta_returns: bool = True,
    beta_returns_path: Path | str = DEFAULT_EQUITY_BETA_RETURNS,
    date_as_index: bool = True,
) -> pd.DataFrame:
    """Return a ticker's local yfinance history.

    The project downloader now defaults to raw OHLCV plus `adj_close` when
    yfinance provides it. Research returns should prefer `adj_close`; live
    share sizing and execution price bands should use raw `close`. Older files
    may have been downloaded with adjusted OHLC only, so refresh live target
    tickers before producing orders.
    """

    safe_ticker = ticker.upper().replace("/", "-")
    path = Path(prices_dir) / f"{safe_ticker}.csv"
    if not path.exists():
        raise FileNotFoundError(f"No local equity history found for {ticker}: {path}")

    df = load_price_file(path)
    if "close" in df.columns and "adj_close" not in df.columns:
        df["adj_close"] = df["close"]
    if drop_missing_close and "close" in df.columns:
        df = df.dropna(subset=["close"])

    beta_path = Path(beta_returns_path)
    if include_beta_returns and beta_path.exists():
        beta = get_equity_beta_returns(ticker, beta_returns_path=beta_path, date_as_index=False)
        beta_cols = [
            "date",
            "raw_return",
            "market_ticker",
            "sector_ticker",
            "market_return",
            "sector_return",
            "market_beta",
            "sector_beta",
            "beta_observations",
            "residual_return",
        ]
        df = df.merge(beta[[col for col in beta_cols if col in beta.columns]], on="date", how="left")
    return _sort_and_maybe_index_by_date(df, date_as_index=date_as_index)


def get_equity_beta_returns(
    ticker: str,
    beta_returns_path: Path | str = DEFAULT_EQUITY_BETA_RETURNS,
    date_as_index: bool = True,
) -> pd.DataFrame:
    """Return precomputed raw returns, market/sector betas, and residual returns for one ticker.

    By default the returned frame is indexed by `date`; pass
    `date_as_index=False` to keep `date` as a regular column.
    """

    path = Path(beta_returns_path)
    if not path.exists():
        raise FileNotFoundError(f"No precomputed beta/return file found: {path}")

    df = _read_frame(path)
    df["date"] = pd.to_datetime(df["date"], utc=False)
    df["ticker"] = df["ticker"].astype(str).str.upper().str.strip()
    out = df[df["ticker"] == ticker.upper().strip()].copy()
    if out.empty:
        raise KeyError(f"{ticker} was not found in {path}")
    return _sort_and_maybe_index_by_date(out, date_as_index=date_as_index)


def get_equity_processed_history(
    ticker: str,
    processed_path: Path | str = DEFAULT_EQUITY_PROCESSED,
    date_as_index: bool = True,
) -> pd.DataFrame:
    """Return one ticker from the processed equity panel.

    This is the preferred notebook source for stock returns. It contains raw
    log returns, market/sector log returns, beta variations, and residual log
    returns from `data/processed/equity_processed.parquet`.
    """

    path = Path(processed_path)
    if not path.exists():
        raise FileNotFoundError(f"No processed equity dataset found: {path}")

    df = _read_frame(path)
    df["date"] = pd.to_datetime(df["date"], utc=False)
    df["ticker"] = df["ticker"].astype(str).str.upper().str.strip()
    out = df[df["ticker"] == ticker.upper().strip()].copy()
    if out.empty:
        raise KeyError(f"{ticker} was not found in {path}")
    return _sort_and_maybe_index_by_date(out, date_as_index=date_as_index)


def get_commodity_carry(
    symbol: str,
    carry_dir: Path | str = DEFAULT_CARRY_DIR,
    date_as_index: bool = True,
) -> pd.DataFrame:
    """Return one commodity's chained carry-data file.

    By default the returned frame is indexed by `date`; pass
    `date_as_index=False` to keep `date` as a regular column for
    `pd.merge(..., on="date")`.
    """

    safe_symbol = symbol.upper().strip()
    path = Path(carry_dir) / f"{safe_symbol}.csv"
    if not path.exists():
        raise FileNotFoundError(f"No local carry-data file found for {symbol}: {path}")

    return _sort_and_maybe_index_by_date(load_carry_file(path), date_as_index=date_as_index)


def get_commodity_carry_history(
    carry_dir: Path | str = DEFAULT_CARRY_DIR,
    symbols: list[str] | None = None,
    date_as_index: bool = True,
) -> pd.DataFrame:
    """Return chained carry-data files for all or selected commodities."""

    carry = load_carry_directory(Path(carry_dir))
    if symbols is not None:
        keep = {symbol.upper().strip() for symbol in symbols}
        carry = carry[carry["symbol"].astype(str).str.upper().str.strip().isin(keep)].copy()
    return _sort_and_maybe_index_by_date(carry, date_as_index=date_as_index)


def get_commodity_features(
    symbol: str | None = None,
    commodity_signals_path: Path | str = DEFAULT_COMMODITY_SIGNALS,
    date_as_index: bool = True,
) -> pd.DataFrame:
    """Return the processed daily commodity feature table."""

    path = Path(commodity_signals_path)
    if not path.exists():
        raise FileNotFoundError(f"No processed commodity feature file found: {path}")

    features = _read_frame(path)
    features["date"] = pd.to_datetime(features["date"], utc=False)
    if "arrival" in features.columns:
        features["arrival"] = pd.to_datetime(features["arrival"], utc=False)
    if symbol is not None:
        keep = symbol.upper().strip()
        features = features[features["symbol"].astype(str).str.upper().str.strip() == keep].copy()
    return _sort_and_maybe_index_by_date(features, date_as_index=date_as_index)


def get_fundamental_snapshot(
    symbol: str | None = None,
    snapshot_path: Path | str = DEFAULT_FUNDAMENTAL_SNAPSHOT,
) -> pd.DataFrame:
    """Return the normalized ticker fundamental snapshot."""

    path = Path(snapshot_path)
    if not path.exists():
        raise FileNotFoundError(f"No fundamental snapshot found: {path}")

    snapshot = _read_frame(path)
    if snapshot.empty:
        return snapshot
    snapshot["symbol"] = snapshot["symbol"].astype(str).str.upper().str.strip()
    for col in ["snapshot_date", "tradable_after"]:
        if col in snapshot.columns:
            snapshot[col] = pd.to_datetime(snapshot[col], errors="coerce", format="mixed", utc=False)
    if symbol is not None:
        snapshot = snapshot[snapshot["symbol"] == symbol.upper().strip()].copy()
    return snapshot.sort_values("symbol").reset_index(drop=True)


def get_fundamental_factors(
    symbol: str | None = None,
    metric: str | None = None,
    factors_path: Path | str = DEFAULT_FUNDAMENTAL_FACTORS,
) -> pd.DataFrame:
    """Return normalized long-form fundamental factor observations."""

    path = Path(factors_path)
    if not path.exists():
        raise FileNotFoundError(f"No fundamental factors found: {path}")

    factors = _read_frame(path)
    if factors.empty:
        return factors
    factors["symbol"] = factors["symbol"].astype(str).str.upper().str.strip()
    for col in ["date", "tradable_after"]:
        if col in factors.columns:
            factors[col] = pd.to_datetime(factors[col], errors="coerce", format="mixed", utc=False)
    if symbol is not None:
        factors = factors[factors["symbol"] == symbol.upper().strip()].copy()
    if metric is not None:
        factors = factors[factors["metric"].astype(str) == metric].copy()
    return factors.sort_values(["symbol", "metric", "tradable_after"]).reset_index(drop=True)


def get_agriculture_fundamental_events(
    commodity: str | None = None,
    events_path: Path | str = DEFAULT_AGRICULTURE_FUNDAMENTAL_EVENTS,
) -> pd.DataFrame:
    """Return normalized NASS/USDA agriculture fundamental confirmation events."""

    path = Path(events_path)
    if not path.exists():
        raise FileNotFoundError(f"No agriculture fundamental events found: {path}")

    events = _read_frame(path)
    if events.empty:
        return events
    events["commodity"] = events["commodity"].astype(str).str.upper().str.strip()
    for col in ["event_date", "tradable_after"]:
        if col in events.columns:
            events[col] = pd.to_datetime(events[col], errors="coerce", format="mixed", utc=False)
    if commodity is not None:
        events = events[events["commodity"] == commodity.upper().strip()].copy()
    return events.sort_values(["commodity", "tradable_after", "source_type", "metric"]).reset_index(drop=True)


def get_commodity_confirmation_events(
    commodity: str | None = None,
    events_path: Path | str = DEFAULT_CL_COMMODITY_CONFIRMATION_EVENTS,
) -> pd.DataFrame:
    """Return normalized EIA/CFTC commodity confirmation events."""

    path = Path(events_path)
    if not path.exists():
        raise FileNotFoundError(f"No commodity confirmation events found: {path}")

    events = _read_frame(path)
    if events.empty:
        return events
    events["commodity"] = events["commodity"].astype(str).str.upper().str.strip()
    for col in ["date", "tradable_after"]:
        if col in events.columns:
            events[col] = pd.to_datetime(events[col], errors="coerce", format="mixed", utc=False)
    if commodity is not None:
        events = events[events["commodity"] == commodity.upper().strip()].copy()
    return events.sort_values(["commodity", "tradable_after", "source_type", "metric"]).reset_index(drop=True)


def get_quarterly_stock_feature_matrix(
    commodity: str,
    quarter: str,
    lookback_years: int,
    matrix_dir: Path | str = DEFAULT_QUARTERLY_FEATURE_MATRIX_DIR,
    ticker: str | None = None,
    feature: str | None = None,
    horizon_days: int | None = None,
) -> pd.DataFrame:
    """Load a frozen quarterly `commodity x quarter x lookback` feature matrix."""

    commodity = commodity.upper().strip()
    path = Path(matrix_dir) / commodity / f"{commodity}-Features-{quarter}-{lookback_years}Y.csv"
    if not path.exists():
        raise FileNotFoundError(f"No quarterly stock-feature matrix found: {path}")

    matrix = pd.read_csv(path)
    if matrix.empty:
        return matrix
    matrix["ticker"] = matrix["ticker"].astype(str).str.upper().str.strip()
    matrix["commodity"] = matrix["commodity"].astype(str).str.upper().str.strip()
    matrix["feature"] = matrix["feature"].astype(str).str.strip()
    for col in ["quarter_start", "asof_date", "sample_start", "sample_end", "target_end_date_max"]:
        if col in matrix.columns:
            matrix[col] = pd.to_datetime(matrix[col], utc=False)
    if ticker is not None:
        matrix = matrix[matrix["ticker"] == ticker.upper().strip()].copy()
    if feature is not None:
        matrix = matrix[matrix["feature"] == feature.strip()].copy()
    if horizon_days is not None:
        matrix = matrix[matrix["horizon_days"] == horizon_days].copy()
    return matrix.sort_values(["ticker", "feature", "horizon_days"]).reset_index(drop=True)


def get_stock_commodity_feature_frame(
    ticker: str,
    commodity: str,
    feature: str,
    processed_path: Path | str = DEFAULT_EQUITY_PROCESSED,
    commodity_signals_path: Path | str = DEFAULT_COMMODITY_SIGNALS,
    return_column: str = "residual_return",
    feature_z_window: int = 252,
    min_feature_observations: int = 126,
    start: str | None = None,
    end: str | None = None,
    date_as_index: bool = True,
) -> pd.DataFrame:
    """Align one stock's daily log return with one commodity feature.

    The returned frame includes both raw `feature_value` and standardized
    `feature_z`. Commodity rows are aligned by `arrival` using backward
    as-of merge, so stock date `T` only sees features whose arrival date is on
    or before `T`.
    """

    ticker = ticker.upper().strip()
    commodity = commodity.upper().strip()
    feature = feature.strip()

    returns = get_equity_processed_history(ticker, processed_path=processed_path, date_as_index=False)
    if return_column not in returns.columns:
        raise ValueError(f"{return_column} is not available in {processed_path}")
    keep_cols = [
        "date",
        "ticker",
        "theme",
        "role",
        "region",
        "close",
        "adj_close",
        "raw_return",
        "market_ticker",
        "sector_ticker",
        "market_return",
        "sector_return",
        return_column,
    ]
    keep_cols = list(dict.fromkeys(keep_cols))
    returns = returns[[col for col in keep_cols if col in returns.columns]].copy()
    returns = returns.rename(columns={return_column: "ret"})
    returns["ret"] = pd.to_numeric(returns["ret"], errors="coerce")
    if start is not None:
        returns = returns[returns["date"] >= pd.Timestamp(start)]
    if end is not None:
        returns = returns[returns["date"] <= pd.Timestamp(end)]
    returns = returns.dropna(subset=["ret"]).sort_values("date")
    if returns.empty:
        return returns

    commodity_features = get_commodity_features(
        symbol=commodity,
        commodity_signals_path=commodity_signals_path,
        date_as_index=False,
    )
    z = _feature_z_scores(
        commodity_signals=commodity_features,
        features=[feature],
        feature_z_window=feature_z_window,
        min_feature_observations=min_feature_observations,
    )
    z = z[z["commodity"] == commodity].copy()
    if z.empty:
        raise KeyError(f"No feature history for {commodity} {feature}")
    z["known_date"] = pd.to_datetime(z["arrival"], utc=False).dt.normalize()
    z = z.rename(columns={"date": "feature_date"})

    aligned = pd.merge_asof(
        returns.sort_values("date"),
        z[["known_date", "feature_date", "arrival", "feature_value", "feature_z"]].sort_values("known_date"),
        left_on="date",
        right_on="known_date",
        direction="backward",
    )
    aligned["commodity"] = commodity
    aligned["feature"] = feature
    aligned = aligned.rename(
        columns={
            "feature_value": feature,
            "feature_z": f"{feature}_z",
        }
    )
    cols = [
        "date",
        "ticker",
        "commodity",
        "feature",
        "feature_date",
        "arrival",
        "known_date",
        "ret",
        "raw_return",
        "market_ticker",
        "sector_ticker",
        "market_return",
        "sector_return",
        feature,
        f"{feature}_z",
    ]
    out = aligned[[col for col in cols if col in aligned.columns]].copy()
    return _sort_and_maybe_index_by_date(out, date_as_index=date_as_index)


def add_one_day_feature_pnl(
    frame: pd.DataFrame,
    feature_column: str,
    return_column: str = "ret",
    signal_lag_days: int = 1,
    signal_scale: float = 1.0,
    output_column: str = "pnl",
) -> pd.DataFrame:
    """Add a simple lagged feature-times-log-return diagnostic PnL column."""

    out = frame.copy()
    out[output_column] = (
        pd.to_numeric(out[feature_column], errors="coerce").shift(signal_lag_days)
        * pd.to_numeric(out[return_column], errors="coerce")
        * signal_scale
    )
    out[f"{output_column}_cum_log"] = out[output_column].fillna(0.0).cumsum()
    out[f"{output_column}_index"] = np.exp(out[f"{output_column}_cum_log"])
    return out


def run_feature_trigger_hold_backtest(
    frame: pd.DataFrame,
    feature_column: str,
    return_column: str = "ret",
    beta_per_1z: float | None = None,
    activation_z: float = 1.0,
    hold_days: int = 10,
    execution_lag_days: int = 1,
    capital_per_event: float | None = None,
    transaction_cost_bps: float = 0.0,
) -> pd.DataFrame:
    """Backtest a single feature trigger with overlapping fixed-hold sleeves.

    `feature_column` is usually a z-score column such as
    `front_second_annualized_carry_z`. A trigger starts when
    `abs(feature_column) >= activation_z`; the event enters after
    `execution_lag_days` stock-return observations and holds for `hold_days`.

    If `beta_per_1z` is supplied from the matrix, event direction is
    `sign(beta_per_1z * feature_value)`. Otherwise it is `sign(feature_value)`.
    Returns are log returns, and `equity_curve = exp(cumsum(strategy_return))`.
    """

    if hold_days <= 0:
        raise ValueError("hold_days must be positive")
    if execution_lag_days < 0:
        raise ValueError("execution_lag_days must be non-negative")

    out = frame.copy().sort_values("date").reset_index(drop=True)
    feature_values = pd.to_numeric(out[feature_column], errors="coerce")
    returns = pd.to_numeric(out[return_column], errors="coerce")
    active = feature_values.abs() >= activation_z
    beta_sign = 1.0 if beta_per_1z is None else float(np.sign(beta_per_1z))
    event_direction = np.sign(feature_values * beta_sign)
    event_weight = 1.0 / hold_days if capital_per_event is None else float(capital_per_event)

    position = np.zeros(len(out), dtype=float)
    event_ids = np.full(len(out), np.nan)
    event_count = 0
    for event_idx in np.flatnonzero(active.to_numpy()):
        direction = event_direction.iloc[event_idx]
        if not np.isfinite(direction) or direction == 0:
            continue
        start_idx = event_idx + execution_lag_days
        end_idx = start_idx + hold_days
        if start_idx >= len(out):
            continue
        event_count += 1
        hold_slice = slice(start_idx, min(end_idx, len(out)))
        position[hold_slice] += direction * event_weight
        event_ids[hold_slice] = event_count

    out["trigger"] = active
    out["event_signal"] = event_direction.where(active, 0.0)
    out["position"] = position
    out["active_event_id"] = event_ids
    out["position_change"] = pd.Series(position).diff().abs().fillna(abs(position[0]))
    out["transaction_cost"] = out["position_change"] * transaction_cost_bps / 10_000.0
    out["strategy_return_gross"] = out["position"] * returns
    out["strategy_return"] = out["strategy_return_gross"] - out["transaction_cost"]
    out["cum_log_return"] = out["strategy_return"].fillna(0.0).cumsum()
    out["equity_curve"] = np.exp(out["cum_log_return"])
    return out


def get_stock_feature_matrix(
    ticker: str | None = None,
    commodity: str | None = None,
    feature: str | None = None,
    matrix_path: Path | str = DEFAULT_STOCK_FEATURE_MATRIX,
    as_of_date: str | None = None,
    allow_prior: bool = True,
) -> pd.DataFrame:
    """Return the stock-feature trading matrix, optionally filtered."""

    path = Path(matrix_path)
    if not path.exists():
        raise FileNotFoundError(f"No stock-feature matrix found: {path}")

    matrix = _read_frame(path)
    if matrix.empty:
        return matrix
    matrix = matrix.copy()
    matrix["ticker"] = matrix["ticker"].astype(str).str.upper().str.strip()
    matrix["commodity"] = matrix["commodity"].astype(str).str.upper().str.strip()
    matrix["feature"] = matrix["feature"].astype(str).str.strip()
    date_col = "matrix_date" if "matrix_date" in matrix.columns else "as_of_date" if "as_of_date" in matrix.columns else None
    if date_col is not None:
        matrix[date_col] = pd.to_datetime(matrix[date_col], utc=False)
    if "as_of_date" in matrix.columns:
        matrix["as_of_date"] = pd.to_datetime(matrix["as_of_date"], utc=False)

    if as_of_date is not None:
        if date_col is None:
            raise ValueError(f"{path} has no matrix_date/as_of_date column for as-of lookup")
        target = pd.Timestamp(as_of_date)
        if allow_prior:
            available = matrix[matrix[date_col] <= target]
            if available.empty:
                return matrix.iloc[0:0].copy()
            matrix = available[available[date_col] == available[date_col].max()].copy()
        else:
            matrix = matrix[matrix[date_col] == target].copy()

    if ticker is not None:
        matrix = matrix[matrix["ticker"] == ticker.upper().strip()].copy()
    if commodity is not None:
        matrix = matrix[matrix["commodity"] == commodity.upper().strip()].copy()
    if feature is not None:
        matrix = matrix[matrix["feature"] == feature.strip()].copy()
    return matrix.sort_values(["ticker", "commodity", "feature"]).reset_index(drop=True)


def get_stock_feature_equity_curve(
    ticker: str,
    commodity: str,
    feature: str,
    matrix_path: Path | str = DEFAULT_STOCK_FEATURE_MATRIX,
    commodity_signals_path: Path | str = DEFAULT_COMMODITY_SIGNALS,
    beta_returns_path: Path | str = DEFAULT_EQUITY_BETA_RETURNS,
    as_of_date: str | None = None,
    return_column: str = "residual_return",
    activation_z: float = 1.0,
    position_mode: str = "sign",
    position_lag_days: int = 1,
    transaction_cost_bps: float = 0.0,
    feature_z_window: int = 252,
    min_feature_observations: int = 126,
    start: str | None = None,
    end: str | None = None,
    date_as_index: bool = True,
) -> pd.DataFrame:
    """Return a notebook-friendly equity curve for one ticker/commodity/feature cell.

    The curve uses the stock-feature matrix to infer the expected direction,
    computes the commodity feature z-score through time, lags the position by
    one stock-return observation by default, then compounds the selected return
    column. `return_column="residual_return"` uses the precomputed residual
    trading unit.
    """

    ticker = ticker.upper().strip()
    commodity = commodity.upper().strip()
    feature = feature.strip()
    matrix = get_stock_feature_matrix(
        ticker=ticker,
        commodity=commodity,
        feature=feature,
        matrix_path=matrix_path,
        as_of_date=as_of_date,
        allow_prior=True,
    )
    if matrix.empty:
        raise KeyError(f"No stock-feature matrix row for {ticker} {commodity} {feature}")

    if "quality_score" in matrix.columns:
        row = matrix.sort_values("quality_score", ascending=False).iloc[0]
    else:
        row = matrix.iloc[-1]

    direction_sign = float(row.get("direction_sign", 1.0))
    score_weight = float(row.get("score_weight", direction_sign))
    commodity_features = get_commodity_features(
        symbol=commodity,
        commodity_signals_path=commodity_signals_path,
        date_as_index=False,
    )
    z = _feature_z_scores(
        commodity_signals=commodity_features,
        features=[feature],
        feature_z_window=feature_z_window,
        min_feature_observations=min_feature_observations,
    )
    z = z[z["commodity"] == commodity].copy()
    if z.empty:
        raise KeyError(f"No z-score history for {commodity} {feature}")
    z["known_date"] = pd.to_datetime(z["arrival"], utc=False).dt.normalize()

    returns = get_equity_beta_returns(ticker, beta_returns_path=beta_returns_path, date_as_index=False)
    if return_column not in returns.columns:
        raise ValueError(f"{return_column} is not available in {beta_returns_path}")
    returns = returns[["date", "ticker", "theme", "role", "region", return_column]].copy()
    returns[return_column] = pd.to_numeric(returns[return_column], errors="coerce")
    returns = returns.dropna(subset=[return_column]).sort_values("date")
    if start is not None:
        returns = returns[returns["date"] >= pd.Timestamp(start)]
    if end is not None:
        returns = returns[returns["date"] <= pd.Timestamp(end)]
    if returns.empty:
        return returns

    aligned = pd.merge_asof(
        returns.sort_values("date"),
        z[["known_date", "date", "arrival", "feature_value", "feature_z"]]
        .rename(columns={"date": "feature_date"})
        .sort_values("known_date"),
        left_on="date",
        right_on="known_date",
        direction="backward",
    )
    aligned["raw_signal"] = aligned["feature_z"] * score_weight
    aligned["active"] = aligned["feature_z"].abs() >= activation_z

    if position_mode == "sign":
        desired = np.where(aligned["active"], np.sign(aligned["raw_signal"]), 0.0)
    elif position_mode == "continuous":
        desired = np.where(
            aligned["active"],
            np.clip(aligned["feature_z"] * direction_sign / activation_z, -1.0, 1.0),
            0.0,
        )
    else:
        raise ValueError("position_mode must be 'sign' or 'continuous'")

    aligned["desired_position"] = desired
    aligned["position"] = pd.Series(desired, index=aligned.index).shift(position_lag_days).fillna(0.0)
    aligned["position_change"] = aligned["position"].diff().abs().fillna(aligned["position"].abs())
    aligned["transaction_cost"] = aligned["position_change"] * transaction_cost_bps / 10_000.0
    aligned["strategy_return_gross"] = aligned["position"] * aligned[return_column]
    aligned["strategy_return"] = aligned["strategy_return_gross"] - aligned["transaction_cost"]
    aligned["cum_log_return"] = aligned["strategy_return"].fillna(0.0).cumsum()
    aligned["equity_curve"] = np.exp(aligned["cum_log_return"])
    aligned["ticker"] = ticker
    aligned["commodity"] = commodity
    aligned["feature"] = feature
    aligned["direction"] = row.get("direction")
    aligned["direction_sign"] = direction_sign
    aligned["score_weight"] = score_weight
    aligned["matrix_as_of_date"] = row.get("as_of_date")

    cols = [
        "date",
        "ticker",
        "commodity",
        "feature",
        "matrix_as_of_date",
        "direction",
        "direction_sign",
        "score_weight",
        "feature_date",
        "arrival",
        "feature_value",
        "feature_z",
        "active",
        "raw_signal",
        "desired_position",
        "position",
        return_column,
        "strategy_return_gross",
        "transaction_cost",
        "strategy_return",
        "cum_log_return",
        "equity_curve",
    ]
    out = aligned[[col for col in cols if col in aligned.columns]].copy()
    return _sort_and_maybe_index_by_date(out, date_as_index=date_as_index)


def get_commodity_exposure_universe(
    commodity: str | None = None,
    exposure_map_path: Path | str = DEFAULT_COMMODITY_EXPOSURE_MAP,
    min_abs_prior_weight: float = 0.0,
) -> pd.DataFrame:
    """Return ticker-commodity exposure priors."""

    return get_exposure_universe(
        exposure_map_path=Path(exposure_map_path),
        commodity=commodity,
        min_abs_prior_weight=min_abs_prior_weight,
    )


def get_hedging_instruments(
    ticker: str,
    seed_universe_path: Path | str = DEFAULT_SEED_UNIVERSE,
    theme_hedges_path: Path | str = DEFAULT_THEME_HEDGES,
    market_ticker: str = "SPY",
) -> pd.DataFrame:
    """Return market and sector hedge instruments for one stock ticker."""

    ticker = ticker.upper().strip()
    seed = _read_frame(Path(seed_universe_path))
    hedges = _read_frame(Path(theme_hedges_path))

    seed["ticker"] = seed["ticker"].astype(str).str.upper().str.strip()
    row = seed[seed["ticker"] == ticker]
    if row.empty:
        raise KeyError(f"{ticker} was not found in {seed_universe_path}")

    meta = row.iloc[0].to_dict()
    sector_row = hedges[hedges["theme"].astype(str) == str(meta["theme"])]
    sector_ticker = market_ticker if sector_row.empty else str(sector_row.iloc[0]["sector_ticker"]).upper()

    return pd.DataFrame(
        [
            {
                "ticker": ticker,
                "instrument_role": "stock",
                "instrument_ticker": ticker,
                "theme": meta.get("theme"),
                "stock_role": meta.get("role"),
                "region": meta.get("region"),
            },
            {
                "ticker": ticker,
                "instrument_role": "market_hedge",
                "instrument_ticker": market_ticker.upper(),
                "theme": meta.get("theme"),
                "stock_role": meta.get("role"),
                "region": meta.get("region"),
            },
            {
                "ticker": ticker,
                "instrument_role": "sector_hedge",
                "instrument_ticker": sector_ticker,
                "theme": meta.get("theme"),
                "stock_role": meta.get("role"),
                "region": meta.get("region"),
            },
        ]
    )


def get_equity_and_hedge_history(
    ticker: str,
    prices_dir: Path | str = DEFAULT_EQUITY_DIR,
    seed_universe_path: Path | str = DEFAULT_SEED_UNIVERSE,
    theme_hedges_path: Path | str = DEFAULT_THEME_HEDGES,
    market_ticker: str = "SPY",
    drop_missing_close: bool = True,
) -> pd.DataFrame:
    """Return stock, market hedge, and sector hedge histories in long format."""

    instruments = get_hedging_instruments(
        ticker=ticker,
        seed_universe_path=seed_universe_path,
        theme_hedges_path=theme_hedges_path,
        market_ticker=market_ticker,
    )

    frames: list[pd.DataFrame] = []
    for row in instruments.itertuples(index=False):
        hist = get_equity_history(
            row.instrument_ticker,
            prices_dir=prices_dir,
            drop_missing_close=drop_missing_close,
            include_beta_returns=False,
            date_as_index=False,
        )
        hist = hist.copy()
        hist["target_ticker"] = row.ticker
        hist["instrument_role"] = row.instrument_role
        hist["instrument_ticker"] = row.instrument_ticker
        hist["theme"] = row.theme
        frames.append(hist)

    out = pd.concat(frames, ignore_index=True)
    cols = ["target_ticker", "instrument_role", "instrument_ticker", "theme"]
    cols += [col for col in out.columns if col not in cols]
    return out[cols].sort_values(["instrument_role", "instrument_ticker", "date"]).reset_index(drop=True)


def get_equity_and_hedge_history_wide(
    ticker: str,
    prices_dir: Path | str = DEFAULT_EQUITY_DIR,
    seed_universe_path: Path | str = DEFAULT_SEED_UNIVERSE,
    theme_hedges_path: Path | str = DEFAULT_THEME_HEDGES,
    market_ticker: str = "SPY",
) -> pd.DataFrame:
    """Return adjusted close prices for stock, market hedge, and sector hedge in wide format."""

    long = get_equity_and_hedge_history(
        ticker=ticker,
        prices_dir=prices_dir,
        seed_universe_path=seed_universe_path,
        theme_hedges_path=theme_hedges_path,
        market_ticker=market_ticker,
    )
    wide = long.pivot_table(index="date", columns="instrument_role", values="adj_close", aggfunc="last")
    return wide.reset_index().sort_values("date").reset_index(drop=True)


def get_commodity_contracts(
    symbol: str,
    commodity_dir: Path | str = DEFAULT_COMMODITY_DIR,
) -> pd.DataFrame:
    """Return all local futures contract files for a commodity symbol.

    Example: `get_commodity_contracts("CL")` reads every CSV under
    `data/comm/CL` and adds `symbol` plus `contract` columns.
    """

    symbol = symbol.upper()
    directory = Path(commodity_dir) / symbol
    if not directory.exists():
        raise FileNotFoundError(f"No local commodity directory found for {symbol}: {directory}")

    frames: list[pd.DataFrame] = []
    for path in sorted(directory.glob("*.csv")):
        df = pd.read_csv(path)
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], utc=False)
        df.insert(0, "contract", path.stem)
        df.insert(0, "symbol", symbol)
        frames.append(df)

    if not frames:
        return pd.DataFrame()

    out = pd.concat(frames, ignore_index=True)
    return out.sort_values(["contract", "date"]).reset_index(drop=True)
