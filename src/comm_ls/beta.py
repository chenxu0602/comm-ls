from __future__ import annotations

from pathlib import Path
from time import perf_counter

import numpy as np
import pandas as pd

from comm_ls.equity import load_price_directory
from comm_ls.universe import load_seed_universe

DEFAULT_PROCESSED_BETA_VARIATIONS = {
    "mktsec_w6m": {
        "mode": "market_sector",
        "beta_return_frequency": "weekly",
        "beta_update_frequency": "monthly",
        "beta_lookback_months": 6,
        "min_beta_observations": 13,
        "beta_weighting": "exponential",
        "beta_half_life_months": 3.0,
        "beta_smoothing": 0.0,
        "hedge_ratio_scale": 1.0,
    },
    "mktsec_w12m": {
        "mode": "market_sector",
        "beta_return_frequency": "weekly",
        "beta_update_frequency": "monthly",
        "beta_lookback_months": 12,
        "min_beta_observations": 26,
        "beta_weighting": "exponential",
        "beta_half_life_months": 3.0,
        "beta_smoothing": 0.0,
        "hedge_ratio_scale": 1.0,
    },
    "mktsec_w24m": {
        "mode": "market_sector",
        "beta_return_frequency": "weekly",
        "beta_update_frequency": "monthly",
        "beta_lookback_months": 24,
        "min_beta_observations": 52,
        "beta_weighting": "exponential",
        "beta_half_life_months": 6.0,
        "beta_smoothing": 0.0,
        "hedge_ratio_scale": 1.0,
    },
    "mkt_w12m": {
        "mode": "market_only",
        "beta_return_frequency": "weekly",
        "beta_update_frequency": "monthly",
        "beta_lookback_months": 12,
        "min_beta_observations": 26,
        "beta_weighting": "exponential",
        "beta_half_life_months": 3.0,
        "beta_smoothing": 0.0,
        "hedge_ratio_scale": 1.0,
    },
}
DEFAULT_PRIMARY_PROCESSED_BETA_VARIATION = "mktsec_w12m"
DEFAULT_COMMODITY_BETA_SYMBOLS = ["CL", "HG", "GC", "SI", "LC", "IS", "PS", "PD", "PT"]
DEFAULT_COMMODITY_BETA_RETURN_COLUMN = "front_log_ret_1d"


def _read_frame(path: Path) -> pd.DataFrame:
    if path.suffix == ".parquet":
        return pd.read_parquet(path)
    return pd.read_csv(path)


def _load_theme_hedges(path: Path) -> dict[str, str]:
    df = pd.read_csv(path)
    required = {"theme", "sector_ticker"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"{path} is missing required columns: {sorted(missing)}")
    return {
        str(row.theme).strip(): str(row.sector_ticker).upper().strip()
        for row in df.itertuples(index=False)
        if pd.notna(row.theme) and pd.notna(row.sector_ticker)
    }


def _price_matrix(prices: pd.DataFrame) -> pd.DataFrame:
    required = {"ticker", "date", "close"}
    missing = required.difference(prices.columns)
    if missing:
        raise ValueError(f"Price data is missing required columns: {sorted(missing)}")

    df = prices.copy()
    df["date"] = pd.to_datetime(df["date"], utc=False)
    df["close"] = pd.to_numeric(df["close"], errors="coerce")
    if "adj_close" in df.columns:
        df["adj_close"] = pd.to_numeric(df["adj_close"], errors="coerce")
        df["_return_price"] = df["adj_close"].fillna(df["close"])
    else:
        df["_return_price"] = df["close"]
    df = df.dropna(subset=["_return_price"])
    matrix = df.pivot_table(index="date", columns="ticker", values="_return_price", aggfunc="last")
    return matrix.sort_index()


def _return_matrix(matrix: pd.DataFrame, frequency: str) -> pd.DataFrame:
    if frequency == "daily":
        prices = matrix
    elif frequency == "weekly":
        prices = matrix.resample("W-FRI").last()
    else:
        raise ValueError("beta_return_frequency must be 'daily' or 'weekly'")
    return np.log(prices).diff()


def _price_column(prices: pd.DataFrame) -> str:
    return "adj_close" if "adj_close" in prices.columns else "close"


def _month_start_update_dates(index: pd.DatetimeIndex) -> list[pd.Timestamp]:
    if len(index) == 0:
        return []
    dates = pd.Series(index, index=index)
    return [pd.Timestamp(value) for value in dates.groupby(dates.dt.to_period("M")).min().tolist()]


def _update_dates(index: pd.DatetimeIndex, update_frequency: str) -> list[pd.Timestamp]:
    if update_frequency == "daily":
        return [pd.Timestamp(date) for date in index]
    if update_frequency == "monthly":
        return _month_start_update_dates(index)
    raise ValueError("beta_update_frequency must be 'daily' or 'monthly'")


def _lookback_observations(
    beta_return_frequency: str,
    beta_lookback_months: int,
    beta_lookback_days: int,
) -> int:
    if beta_return_frequency == "weekly":
        return max(1, int(round(beta_lookback_months * 52 / 12)))
    return beta_lookback_days


def _half_life_observations(beta_return_frequency: str, beta_half_life_months: float) -> float:
    if beta_return_frequency == "weekly":
        return max(1.0, beta_half_life_months * 52 / 12)
    return max(1.0, beta_half_life_months * 21)


def _weighted_beta(
    data: pd.DataFrame,
    min_observations: int,
    weighting: str,
    half_life_observations: float,
    sector_equals_market: bool,
) -> tuple[float, float, int]:
    cols = ["stock", "market"] if sector_equals_market else ["stock", "market", "sector"]
    sample = data[cols].replace([np.inf, -np.inf], np.nan).dropna()
    observations = len(sample)
    if observations < min_observations:
        return np.nan, np.nan, observations

    y = sample["stock"].to_numpy(dtype=float)
    x_cols = ["market"] if sector_equals_market else ["market", "sector"]
    x = sample[x_cols].to_numpy(dtype=float)
    x = np.column_stack([np.ones(len(x)), x])

    if weighting == "equal":
        weights = np.ones(len(sample), dtype=float)
    elif weighting == "exponential":
        age = np.arange(len(sample) - 1, -1, -1, dtype=float)
        weights = np.power(0.5, age / half_life_observations)
    else:
        raise ValueError("beta_weighting must be 'equal' or 'exponential'")

    sqrt_w = np.sqrt(weights / weights.mean())
    coef, *_ = np.linalg.lstsq(x * sqrt_w[:, None], y * sqrt_w, rcond=None)
    if sector_equals_market:
        return float(coef[1]), 0.0, observations
    return float(coef[1]), float(coef[2]), observations


def _weighted_three_beta(
    data: pd.DataFrame,
    min_observations: int,
    weighting: str,
    half_life_observations: float,
    sector_equals_market: bool,
) -> tuple[float, float, float, int]:
    cols = ["stock", "market", "commodity"] if sector_equals_market else ["stock", "market", "sector", "commodity"]
    sample = data[cols].replace([np.inf, -np.inf], np.nan).dropna()
    observations = len(sample)
    if observations < min_observations:
        return np.nan, np.nan, np.nan, observations

    y = sample["stock"].to_numpy(dtype=float)
    x_cols = ["market", "commodity"] if sector_equals_market else ["market", "sector", "commodity"]
    x = sample[x_cols].to_numpy(dtype=float)
    x = np.column_stack([np.ones(len(x)), x])

    if weighting == "equal":
        weights = np.ones(len(sample), dtype=float)
    elif weighting == "exponential":
        age = np.arange(len(sample) - 1, -1, -1, dtype=float)
        weights = np.power(0.5, age / half_life_observations)
    else:
        raise ValueError("beta_weighting must be 'equal' or 'exponential'")

    sqrt_w = np.sqrt(weights / weights.mean())
    coef, *_ = np.linalg.lstsq(x * sqrt_w[:, None], y * sqrt_w, rcond=None)
    if sector_equals_market:
        return float(coef[1]), 0.0, float(coef[2]), observations
    return float(coef[1]), float(coef[2]), float(coef[3]), observations


def _monthly_or_daily_beta_pair(
    daily_stock_ret: pd.Series,
    daily_market_ret: pd.Series,
    daily_sector_ret: pd.Series,
    beta_stock_ret: pd.Series,
    beta_market_ret: pd.Series,
    beta_sector_ret: pd.Series,
    lookback_observations: int,
    min_observations: int,
    beta_lag_days: int,
    beta_update_frequency: str,
    beta_return_frequency: str,
    beta_weighting: str,
    beta_half_life_months: float,
    beta_smoothing: float,
    hedge_ratio_scale: float,
) -> pd.DataFrame:
    beta_data = pd.concat(
        {"stock": beta_stock_ret, "market": beta_market_ret, "sector": beta_sector_ret},
        axis=1,
    )
    sector_equals_market = beta_market_ret.equals(beta_sector_ret)
    update_dates = _update_dates(daily_stock_ret.index, beta_update_frequency)
    half_life_obs = _half_life_observations(beta_return_frequency, beta_half_life_months)

    beta_rows: list[dict[str, object]] = []
    last_market_beta = np.nan
    last_sector_beta = np.nan
    for update_date in update_dates:
        daily_pos = daily_stock_ret.index.searchsorted(update_date)
        cutoff_pos = daily_pos - beta_lag_days
        if cutoff_pos < 0:
            cutoff_date = update_date - pd.Timedelta(days=1)
        else:
            cutoff_date = pd.Timestamp(daily_stock_ret.index[cutoff_pos])

        sample = beta_data[beta_data.index <= cutoff_date].tail(lookback_observations)
        market_beta, sector_beta, observations = _weighted_beta(
            data=sample,
            min_observations=min_observations,
            weighting=beta_weighting,
            half_life_observations=half_life_obs,
            sector_equals_market=sector_equals_market,
        )
        if beta_smoothing > 0 and np.isfinite(market_beta) and np.isfinite(last_market_beta):
            market_beta = beta_smoothing * last_market_beta + (1.0 - beta_smoothing) * market_beta
            sector_beta = beta_smoothing * last_sector_beta + (1.0 - beta_smoothing) * sector_beta
        if np.isfinite(market_beta):
            last_market_beta = market_beta
            last_sector_beta = sector_beta

        beta_rows.append(
            {
                "date": update_date,
                "market_beta": market_beta * hedge_ratio_scale if np.isfinite(market_beta) else np.nan,
                "sector_beta": sector_beta * hedge_ratio_scale if np.isfinite(sector_beta) else np.nan,
                "beta_observations": observations,
                "beta_estimation_end": cutoff_date,
            }
        )

    beta_frame = pd.DataFrame(beta_rows).set_index("date") if beta_rows else pd.DataFrame(index=daily_stock_ret.index)
    betas = beta_frame[["market_beta", "sector_beta", "beta_observations", "beta_estimation_end"]].reindex(
        daily_stock_ret.index
    ).ffill()
    out = pd.DataFrame(
        {
            "raw_return": daily_stock_ret,
            "market_return": daily_market_ret,
            "sector_return": daily_sector_ret,
            "market_beta": pd.to_numeric(betas["market_beta"], errors="coerce"),
            "sector_beta": pd.to_numeric(betas["sector_beta"], errors="coerce"),
            "beta_observations": pd.to_numeric(betas["beta_observations"], errors="coerce"),
            "beta_estimation_end": betas["beta_estimation_end"],
        }
    )
    out["residual_return"] = (
        out["raw_return"]
        - out["market_beta"] * out["market_return"]
        - out["sector_beta"] * out["sector_return"]
    )
    out.loc[out["beta_observations"] < min_observations, ["market_beta", "sector_beta", "residual_return"]] = np.nan
    return out


def _monthly_or_daily_beta_triplet(
    daily_stock_ret: pd.Series,
    daily_market_ret: pd.Series,
    daily_sector_ret: pd.Series,
    daily_commodity_ret: pd.Series,
    beta_stock_ret: pd.Series,
    beta_market_ret: pd.Series,
    beta_sector_ret: pd.Series,
    beta_commodity_ret: pd.Series,
    lookback_observations: int,
    min_observations: int,
    beta_lag_days: int,
    beta_update_frequency: str,
    beta_return_frequency: str,
    beta_weighting: str,
    beta_half_life_months: float,
    beta_smoothing: float,
    hedge_ratio_scale: float,
) -> pd.DataFrame:
    beta_data = pd.concat(
        {"stock": beta_stock_ret, "market": beta_market_ret, "sector": beta_sector_ret, "commodity": beta_commodity_ret},
        axis=1,
    )
    sector_equals_market = beta_market_ret.equals(beta_sector_ret)
    update_dates = _update_dates(daily_stock_ret.index, beta_update_frequency)
    half_life_obs = _half_life_observations(beta_return_frequency, beta_half_life_months)

    beta_rows: list[dict[str, object]] = []
    last_market_beta = np.nan
    last_sector_beta = np.nan
    last_commodity_beta = np.nan
    for update_date in update_dates:
        daily_pos = daily_stock_ret.index.searchsorted(update_date)
        cutoff_pos = daily_pos - beta_lag_days
        if cutoff_pos < 0:
            cutoff_date = update_date - pd.Timedelta(days=1)
        else:
            cutoff_date = pd.Timestamp(daily_stock_ret.index[cutoff_pos])

        sample = beta_data[beta_data.index <= cutoff_date].tail(lookback_observations)
        market_beta, sector_beta, commodity_beta, observations = _weighted_three_beta(
            data=sample,
            min_observations=min_observations,
            weighting=beta_weighting,
            half_life_observations=half_life_obs,
            sector_equals_market=sector_equals_market,
        )
        if beta_smoothing > 0 and np.isfinite(market_beta) and np.isfinite(last_market_beta):
            market_beta = beta_smoothing * last_market_beta + (1.0 - beta_smoothing) * market_beta
            sector_beta = beta_smoothing * last_sector_beta + (1.0 - beta_smoothing) * sector_beta
            commodity_beta = beta_smoothing * last_commodity_beta + (1.0 - beta_smoothing) * commodity_beta
        if np.isfinite(market_beta):
            last_market_beta = market_beta
            last_sector_beta = sector_beta
            last_commodity_beta = commodity_beta

        beta_rows.append(
            {
                "date": update_date,
                "market_beta": market_beta * hedge_ratio_scale if np.isfinite(market_beta) else np.nan,
                "sector_beta": sector_beta * hedge_ratio_scale if np.isfinite(sector_beta) else np.nan,
                "commodity_beta": commodity_beta * hedge_ratio_scale if np.isfinite(commodity_beta) else np.nan,
                "beta_observations": observations,
                "beta_estimation_end": cutoff_date,
            }
        )

    beta_frame = pd.DataFrame(beta_rows).set_index("date") if beta_rows else pd.DataFrame(index=daily_stock_ret.index)
    betas = beta_frame[
        ["market_beta", "sector_beta", "commodity_beta", "beta_observations", "beta_estimation_end"]
    ].reindex(daily_stock_ret.index).ffill()
    out = pd.DataFrame(
        {
            "raw_return": daily_stock_ret,
            "market_return": daily_market_ret,
            "sector_return": daily_sector_ret,
            "commodity_return": daily_commodity_ret,
            "market_beta": pd.to_numeric(betas["market_beta"], errors="coerce"),
            "sector_beta": pd.to_numeric(betas["sector_beta"], errors="coerce"),
            "commodity_beta": pd.to_numeric(betas["commodity_beta"], errors="coerce"),
            "beta_observations": pd.to_numeric(betas["beta_observations"], errors="coerce"),
            "beta_estimation_end": betas["beta_estimation_end"],
        }
    )
    out["residual_return"] = (
        out["raw_return"]
        - out["market_beta"] * out["market_return"]
        - out["sector_beta"] * out["sector_return"]
        - out["commodity_beta"] * out["commodity_return"]
    )
    out.loc[
        out["beta_observations"] < min_observations,
        ["market_beta", "sector_beta", "commodity_beta", "residual_return"],
    ] = np.nan
    return out


def _rolling_beta_pair(
    stock_ret: pd.Series,
    market_ret: pd.Series,
    sector_ret: pd.Series,
    lookback_days: int,
    min_observations: int,
    beta_lag_days: int,
) -> pd.DataFrame:
    data = pd.concat(
        {"stock": stock_ret, "market": market_ret, "sector": sector_ret},
        axis=1,
    )

    valid_count = data.notna().all(axis=1).rolling(lookback_days).sum().shift(beta_lag_days)
    market = data["market"]
    sector = data["sector"]
    stock = data["stock"]

    if market.equals(sector):
        var_market = market.rolling(lookback_days, min_periods=min_observations).var().shift(beta_lag_days)
        cov_stock_market = stock.rolling(lookback_days, min_periods=min_observations).cov(market).shift(beta_lag_days)
        beta_market = cov_stock_market / var_market.replace(0, np.nan)
        beta_sector = pd.Series(0.0, index=data.index)
    else:
        var_market = market.rolling(lookback_days, min_periods=min_observations).var().shift(beta_lag_days)
        var_sector = sector.rolling(lookback_days, min_periods=min_observations).var().shift(beta_lag_days)
        cov_market_sector = market.rolling(lookback_days, min_periods=min_observations).cov(sector).shift(
            beta_lag_days
        )
        cov_stock_market = stock.rolling(lookback_days, min_periods=min_observations).cov(market).shift(
            beta_lag_days
        )
        cov_stock_sector = stock.rolling(lookback_days, min_periods=min_observations).cov(sector).shift(
            beta_lag_days
        )

        denominator = var_market * var_sector - cov_market_sector * cov_market_sector
        denominator = denominator.replace(0, np.nan)
        beta_market = (cov_stock_market * var_sector - cov_stock_sector * cov_market_sector) / denominator
        beta_sector = (cov_stock_sector * var_market - cov_stock_market * cov_market_sector) / denominator

    out = pd.DataFrame(
        {
            "raw_return": stock,
            "market_return": market,
            "sector_return": sector,
            "market_beta": beta_market,
            "sector_beta": beta_sector,
            "beta_observations": valid_count,
        }
    )
    out["residual_return"] = (
        out["raw_return"]
        - out["market_beta"] * out["market_return"]
        - out["sector_beta"] * out["sector_return"]
    )
    out.loc[out["beta_observations"] < min_observations, ["market_beta", "sector_beta", "residual_return"]] = np.nan
    return out


def build_equity_beta_returns(
    prices_dir: Path,
    universe_path: Path,
    theme_hedges_path: Path,
    market_ticker: str = "SPY",
    beta_lookback_days: int = 252,
    beta_lookback_months: int = 12,
    min_beta_observations: int = 126,
    beta_lag_days: int = 1,
    beta_return_frequency: str = "weekly",
    beta_update_frequency: str = "monthly",
    beta_weighting: str = "exponential",
    beta_half_life_months: float = 3.0,
    beta_smoothing: float = 0.0,
    hedge_ratio_scale: float = 1.0,
) -> pd.DataFrame:
    seed = load_seed_universe(universe_path)
    theme_hedges = _load_theme_hedges(theme_hedges_path)
    prices = load_price_directory(prices_dir)
    matrix = _price_matrix(prices)
    returns = np.log(matrix).diff()
    beta_returns = _return_matrix(matrix, beta_return_frequency)
    lookback_observations = _lookback_observations(
        beta_return_frequency=beta_return_frequency,
        beta_lookback_months=beta_lookback_months,
        beta_lookback_days=beta_lookback_days,
    )

    market_ticker = market_ticker.upper()
    required_hedges = {market_ticker, *theme_hedges.values()}
    missing = sorted(ticker for ticker in required_hedges if ticker not in returns.columns or ticker not in beta_returns.columns)
    if missing:
        raise ValueError(f"Missing hedge ticker price data: {missing}")

    rows: list[pd.DataFrame] = []
    for stock in seed.itertuples(index=False):
        ticker = str(stock.ticker).upper()
        if ticker not in returns.columns:
            continue

        theme = str(stock.theme)
        sector_ticker = theme_hedges.get(theme, market_ticker)
        if sector_ticker not in returns.columns:
            continue

        calc = _monthly_or_daily_beta_pair(
            daily_stock_ret=returns[ticker],
            daily_market_ret=returns[market_ticker],
            daily_sector_ret=returns[sector_ticker],
            beta_stock_ret=beta_returns[ticker],
            beta_market_ret=beta_returns[market_ticker],
            beta_sector_ret=beta_returns[sector_ticker],
            lookback_observations=lookback_observations,
            min_observations=min_beta_observations,
            beta_lag_days=beta_lag_days,
            beta_update_frequency=beta_update_frequency,
            beta_return_frequency=beta_return_frequency,
            beta_weighting=beta_weighting,
            beta_half_life_months=beta_half_life_months,
            beta_smoothing=beta_smoothing,
            hedge_ratio_scale=hedge_ratio_scale,
        )
        calc = calc.reset_index().rename(columns={"index": "date"})
        calc.insert(0, "ticker", ticker)
        calc["theme"] = theme
        calc["role"] = getattr(stock, "role", None)
        calc["region"] = getattr(stock, "region", None)
        calc["market_ticker"] = market_ticker
        calc["sector_ticker"] = sector_ticker
        calc["adj_close"] = matrix[ticker].reindex(calc["date"]).to_numpy()
        calc["beta_return_frequency"] = beta_return_frequency
        calc["beta_update_frequency"] = beta_update_frequency
        calc["beta_weighting"] = beta_weighting
        calc["beta_lookback_observations"] = lookback_observations
        calc["beta_half_life_months"] = beta_half_life_months
        calc["beta_smoothing"] = beta_smoothing
        calc["hedge_ratio_scale"] = hedge_ratio_scale
        rows.append(calc)

    if not rows:
        return pd.DataFrame()

    out = pd.concat(rows, ignore_index=True)
    cols = [
        "date",
        "ticker",
        "theme",
        "role",
        "region",
        "adj_close",
        "raw_return",
        "market_ticker",
        "sector_ticker",
        "market_return",
        "sector_return",
        "market_beta",
        "sector_beta",
        "beta_observations",
        "beta_estimation_end",
        "beta_return_frequency",
        "beta_update_frequency",
        "beta_weighting",
        "beta_lookback_observations",
        "beta_half_life_months",
        "beta_smoothing",
        "hedge_ratio_scale",
        "residual_return",
    ]
    return out[cols].sort_values(["ticker", "date"]).reset_index(drop=True)


def _variation_config(name: str) -> dict[str, object]:
    if name not in DEFAULT_PROCESSED_BETA_VARIATIONS:
        known = ", ".join(sorted(DEFAULT_PROCESSED_BETA_VARIATIONS))
        raise ValueError(f"Unknown beta variation '{name}'. Known variations: {known}")
    return DEFAULT_PROCESSED_BETA_VARIATIONS[name]


def _price_panel_with_metadata(prices: pd.DataFrame, seed: pd.DataFrame) -> pd.DataFrame:
    price_col = _price_column(prices)
    price_cols = [
        col
        for col in ["open", "high", "low", "close", "adj_close", "volume", "dividends", "stock_splits"]
        if col in prices.columns
    ]
    if "adj_close" not in price_cols and "close" in prices.columns:
        price_cols.append("adj_close")

    panel = prices.copy()
    panel["ticker"] = panel["ticker"].astype(str).str.upper().str.strip()
    panel["date"] = pd.to_datetime(panel["date"], utc=False)
    if "adj_close" not in panel.columns:
        panel["adj_close"] = panel[price_col]
    elif "close" in panel.columns:
        panel["adj_close"] = pd.to_numeric(panel["adj_close"], errors="coerce").fillna(
            pd.to_numeric(panel["close"], errors="coerce")
        )

    seed_meta = seed.copy()
    seed_meta["ticker"] = seed_meta["ticker"].astype(str).str.upper().str.strip()
    meta_cols = [col for col in ["ticker", "theme", "role", "region", "notes"] if col in seed_meta.columns]
    panel = panel.merge(seed_meta[meta_cols], on="ticker", how="inner")
    keep_cols = ["date", "ticker", *[col for col in ["theme", "role", "region", "notes"] if col in panel.columns], *price_cols]
    return panel[keep_cols].sort_values(["ticker", "date"]).reset_index(drop=True)


def _load_commodity_return_matrix(
    commodity_signals_path: Path | None,
    symbols: list[str] | None,
    return_column: str,
    frequency: str,
) -> pd.DataFrame:
    if commodity_signals_path is None or not commodity_signals_path.exists():
        return pd.DataFrame()
    signals = _read_frame(commodity_signals_path)
    if signals.empty or not {"date", "symbol", return_column}.issubset(signals.columns):
        return pd.DataFrame()

    keep_symbols = {symbol.upper().strip() for symbol in (symbols or [])}
    out = signals.copy()
    out["date"] = pd.to_datetime(out["date"], utc=False)
    out["symbol"] = out["symbol"].astype(str).str.upper().str.strip()
    if keep_symbols:
        out = out[out["symbol"].isin(keep_symbols)].copy()
    out[return_column] = pd.to_numeric(out[return_column], errors="coerce")
    matrix = out.pivot_table(index="date", columns="symbol", values=return_column, aggfunc="last").sort_index()
    if frequency == "daily":
        return matrix
    if frequency == "weekly":
        return matrix.resample("W-FRI").sum(min_count=1)
    raise ValueError("beta_return_frequency must be 'daily' or 'weekly'")


def _ticker_commodity_map(
    exposure_map_path: Path | None,
    symbols: list[str] | None,
) -> dict[str, str]:
    if exposure_map_path is None or not exposure_map_path.exists():
        return {}
    exposure = pd.read_csv(exposure_map_path)
    if exposure.empty or not {"ticker", "commodity", "prior_weight"}.issubset(exposure.columns):
        return {}
    keep_symbols = {symbol.upper().strip() for symbol in (symbols or [])}
    exposure = exposure.copy()
    exposure["ticker"] = exposure["ticker"].astype(str).str.upper().str.strip()
    exposure["commodity"] = exposure["commodity"].astype(str).str.upper().str.strip()
    exposure["prior_weight"] = pd.to_numeric(exposure["prior_weight"], errors="coerce")
    if keep_symbols:
        exposure = exposure[exposure["commodity"].isin(keep_symbols)].copy()
    if exposure.empty:
        return {}
    exposure["abs_prior_weight"] = exposure["prior_weight"].abs()
    primary = exposure.sort_values(["ticker", "abs_prior_weight"], ascending=[True, False]).drop_duplicates(
        "ticker",
        keep="first",
    )
    return primary.set_index("ticker")["commodity"].to_dict()


def build_equity_processed_dataset(
    prices_dir: Path,
    universe_path: Path,
    theme_hedges_path: Path,
    commodity_signals_path: Path | None = None,
    exposure_map_path: Path | None = None,
    market_ticker: str = "SPY",
    start: str | None = "2010-01-01",
    end: str | None = None,
    beta_variations: list[str] | None = None,
    primary_variation: str = DEFAULT_PRIMARY_PROCESSED_BETA_VARIATION,
    beta_lag_days: int = 1,
    commodity_beta_symbols: list[str] | None = None,
    commodity_return_column: str = DEFAULT_COMMODITY_BETA_RETURN_COLUMN,
    include_commodity_beta_residuals: bool = True,
    progress: bool = False,
) -> pd.DataFrame:
    started = perf_counter()

    def log(message: str) -> None:
        if progress:
            elapsed = perf_counter() - started
            print(f"[build-equity-processed {elapsed:7.1f}s] {message}", flush=True)

    log(f"loading seed universe from {universe_path}")
    seed = load_seed_universe(universe_path)
    log(f"loaded {len(seed):,} seed tickers; loading theme hedges from {theme_hedges_path}")
    theme_hedges = _load_theme_hedges(theme_hedges_path)
    log(f"loaded {len(theme_hedges):,} theme hedges; loading prices from {prices_dir}")
    prices = load_price_directory(prices_dir)
    price_tickers = prices["ticker"].nunique() if "ticker" in prices.columns else 0
    log(f"loaded {len(prices):,} price rows across {price_tickers:,} tickers")
    price_col = _price_column(prices)
    matrix = _price_matrix(prices)
    daily_returns = np.log(matrix).diff()
    log(f"built price matrix {matrix.shape[0]:,} dates x {matrix.shape[1]:,} tickers using {price_col}")

    market_ticker = market_ticker.upper().strip()
    beta_variations = beta_variations or list(DEFAULT_PROCESSED_BETA_VARIATIONS)
    primary_variation = primary_variation.strip()
    if primary_variation not in beta_variations:
        beta_variations = [*beta_variations, primary_variation]
    beta_return_matrices = {
        frequency: _return_matrix(matrix, frequency)
        for frequency in sorted(
            {str(_variation_config(variation)["beta_return_frequency"]) for variation in beta_variations}
        )
    }
    log(
        "built beta return matrices for "
        + ", ".join(f"{frequency}:{frame.shape[0]:,} rows" for frequency, frame in beta_return_matrices.items())
    )
    commodity_beta_symbols = commodity_beta_symbols or DEFAULT_COMMODITY_BETA_SYMBOLS
    ticker_commodity = (
        _ticker_commodity_map(exposure_map_path, commodity_beta_symbols)
        if include_commodity_beta_residuals
        else {}
    )
    if include_commodity_beta_residuals:
        log(f"loaded commodity exposure map for {len(ticker_commodity):,} tickers")
    commodity_daily_returns = (
        _load_commodity_return_matrix(
            commodity_signals_path=commodity_signals_path,
            symbols=commodity_beta_symbols,
            return_column=commodity_return_column,
            frequency="daily",
        )
        if include_commodity_beta_residuals
        else pd.DataFrame()
    )
    if include_commodity_beta_residuals:
        log(
            "loaded daily commodity returns "
            f"{commodity_daily_returns.shape[0]:,} dates x {commodity_daily_returns.shape[1]:,} symbols"
        )
    commodity_beta_return_matrices = (
        {
            frequency: _load_commodity_return_matrix(
                commodity_signals_path=commodity_signals_path,
                symbols=commodity_beta_symbols,
                return_column=commodity_return_column,
                frequency=frequency,
            )
            for frequency in beta_return_matrices
        }
        if include_commodity_beta_residuals
        else {}
    )
    if include_commodity_beta_residuals:
        log(
            "built commodity beta matrices for "
            + ", ".join(
                f"{frequency}:{frame.shape[0]:,} rows"
                for frequency, frame in commodity_beta_return_matrices.items()
            )
        )

    required_hedges = {market_ticker, *theme_hedges.values()}
    missing = sorted(ticker for ticker in required_hedges if ticker not in daily_returns.columns)
    if missing:
        raise ValueError(f"Missing hedge ticker price data: {missing}")

    panel = _price_panel_with_metadata(prices=prices, seed=seed)
    panel["raw_return"] = panel.groupby("ticker", sort=False)[price_col].transform(lambda s: np.log(s).diff())
    panel["market_ticker"] = market_ticker
    log(f"built raw panel with {len(panel):,} rows; starting per-ticker beta/residual loop")

    rows: list[pd.DataFrame] = []
    skipped_missing_price = 0
    skipped_missing_hedge = 0
    total_seed = len(seed)
    commodity_residual_count = 0
    for idx, stock in enumerate(seed.itertuples(index=False), start=1):
        ticker = str(stock.ticker).upper().strip()
        if ticker not in daily_returns.columns:
            skipped_missing_price += 1
            continue
        theme = str(stock.theme)
        sector_ticker = theme_hedges.get(theme, market_ticker)
        if sector_ticker not in daily_returns.columns:
            skipped_missing_hedge += 1
            continue

        base = pd.DataFrame(
            {
                "date": daily_returns.index,
                "ticker": ticker,
                "market_return": daily_returns[market_ticker].to_numpy(),
                "sector_return": daily_returns[sector_ticker].to_numpy(),
                "sector_ticker": sector_ticker,
            }
        )
        for variation in beta_variations:
            cfg = _variation_config(variation)
            beta_return_frequency = str(cfg["beta_return_frequency"])
            beta_matrix = beta_return_matrices[beta_return_frequency]
            mode = str(cfg["mode"])
            beta_sector_ticker = market_ticker if mode == "market_only" else sector_ticker
            daily_sector = daily_returns[market_ticker] if mode == "market_only" else daily_returns[sector_ticker]

            calc = _monthly_or_daily_beta_pair(
                daily_stock_ret=daily_returns[ticker],
                daily_market_ret=daily_returns[market_ticker],
                daily_sector_ret=daily_sector,
                beta_stock_ret=beta_matrix[ticker],
                beta_market_ret=beta_matrix[market_ticker],
                beta_sector_ret=beta_matrix[beta_sector_ticker],
                lookback_observations=_lookback_observations(
                    beta_return_frequency=beta_return_frequency,
                    beta_lookback_months=int(cfg["beta_lookback_months"]),
                    beta_lookback_days=252,
                ),
                min_observations=int(cfg["min_beta_observations"]),
                beta_lag_days=beta_lag_days,
                beta_update_frequency=str(cfg["beta_update_frequency"]),
                beta_return_frequency=beta_return_frequency,
                beta_weighting=str(cfg["beta_weighting"]),
                beta_half_life_months=float(cfg["beta_half_life_months"]),
                beta_smoothing=float(cfg["beta_smoothing"]),
                hedge_ratio_scale=float(cfg["hedge_ratio_scale"]),
            )
            base[f"market_beta_{variation}"] = calc["market_beta"].to_numpy()
            base[f"sector_beta_{variation}"] = calc["sector_beta"].to_numpy()
            base[f"beta_observations_{variation}"] = calc["beta_observations"].to_numpy()
            base[f"beta_estimation_end_{variation}"] = calc["beta_estimation_end"].to_numpy()
            base[f"residual_return_{variation}"] = calc["residual_return"].to_numpy()

            commodity_symbol = ticker_commodity.get(ticker)
            commodity_beta_matrix = commodity_beta_return_matrices.get(beta_return_frequency, pd.DataFrame())
            if (
                include_commodity_beta_residuals
                and mode == "market_sector"
                and commodity_symbol is not None
                and commodity_symbol in commodity_daily_returns.columns
                and commodity_symbol in commodity_beta_matrix.columns
            ):
                comm_calc = _monthly_or_daily_beta_triplet(
                    daily_stock_ret=daily_returns[ticker],
                    daily_market_ret=daily_returns[market_ticker],
                    daily_sector_ret=daily_returns[sector_ticker],
                    daily_commodity_ret=commodity_daily_returns[commodity_symbol].reindex(daily_returns.index),
                    beta_stock_ret=beta_matrix[ticker],
                    beta_market_ret=beta_matrix[market_ticker],
                    beta_sector_ret=beta_matrix[beta_sector_ticker],
                    beta_commodity_ret=commodity_beta_matrix[commodity_symbol].reindex(beta_matrix.index),
                    lookback_observations=_lookback_observations(
                        beta_return_frequency=beta_return_frequency,
                        beta_lookback_months=int(cfg["beta_lookback_months"]),
                        beta_lookback_days=252,
                    ),
                    min_observations=int(cfg["min_beta_observations"]),
                    beta_lag_days=beta_lag_days,
                    beta_update_frequency=str(cfg["beta_update_frequency"]),
                    beta_return_frequency=beta_return_frequency,
                    beta_weighting=str(cfg["beta_weighting"]),
                    beta_half_life_months=float(cfg["beta_half_life_months"]),
                    beta_smoothing=float(cfg["beta_smoothing"]),
                    hedge_ratio_scale=float(cfg["hedge_ratio_scale"]),
                )
                suffix = variation.replace("mktsec_", "")
                comm_name = f"mktseccomm_{suffix}"
                base[f"commodity_symbol_{comm_name}"] = commodity_symbol
                base[f"commodity_return_{comm_name}"] = comm_calc["commodity_return"].to_numpy()
                base[f"market_beta_{comm_name}"] = comm_calc["market_beta"].to_numpy()
                base[f"sector_beta_{comm_name}"] = comm_calc["sector_beta"].to_numpy()
                base[f"commodity_beta_{comm_name}"] = comm_calc["commodity_beta"].to_numpy()
                base[f"beta_observations_{comm_name}"] = comm_calc["beta_observations"].to_numpy()
                base[f"beta_estimation_end_{comm_name}"] = comm_calc["beta_estimation_end"].to_numpy()
                base[f"residual_return_{comm_name}"] = comm_calc["residual_return"].to_numpy()
                base[f"commodity_beta_return_column_{comm_name}"] = commodity_return_column
                commodity_residual_count += 1

        rows.append(base)
        if idx == 1 or idx == total_seed or idx % 25 == 0:
            log(
                f"processed {idx:,}/{total_seed:,} seed rows; "
                f"built={len(rows):,}; skipped price={skipped_missing_price:,}; "
                f"skipped hedge={skipped_missing_hedge:,}; commodity residuals={commodity_residual_count:,}"
            )

    if not rows:
        log("no per-ticker rows built")
        return pd.DataFrame()

    log(f"concatenating {len(rows):,} per-ticker frames")
    returns = pd.concat(rows, ignore_index=True)
    log(f"merging {len(returns):,} calculated return rows into raw panel")
    out = panel.merge(returns, on=["date", "ticker"], how="left", suffixes=("", "_calc"))
    if "sector_ticker_calc" in out.columns:
        out["sector_ticker"] = out["sector_ticker_calc"].combine_first(out.get("sector_ticker"))
        out = out.drop(columns=["sector_ticker_calc"])
    if "market_ticker_calc" in out.columns:
        out = out.drop(columns=["market_ticker_calc"])

    primary_cols = {
        "market_beta": f"market_beta_{primary_variation}",
        "sector_beta": f"sector_beta_{primary_variation}",
        "beta_observations": f"beta_observations_{primary_variation}",
        "beta_estimation_end": f"beta_estimation_end_{primary_variation}",
        "residual_return": f"residual_return_{primary_variation}",
    }
    for alias, source in primary_cols.items():
        if source in out.columns:
            out[alias] = out[source]
    primary_comm_variation = f"mktseccomm_{primary_variation.replace('mktsec_', '')}"
    primary_comm_cols = {
        "commodity_symbol_mktseccomm": f"commodity_symbol_{primary_comm_variation}",
        "commodity_return_mktseccomm": f"commodity_return_{primary_comm_variation}",
        "commodity_beta_mktseccomm": f"commodity_beta_{primary_comm_variation}",
        "residual_return_mktseccomm": f"residual_return_{primary_comm_variation}",
        "commodity_beta_return_column_mktseccomm": f"commodity_beta_return_column_{primary_comm_variation}",
    }
    for alias, source in primary_comm_cols.items():
        if source in out.columns:
            out[alias] = out[source]

    if start is not None:
        out = out[out["date"] >= pd.Timestamp(start)]
    if end is not None:
        out = out[out["date"] <= pd.Timestamp(end)]
    log(f"applied date filters start={start} end={end}; output rows={len(out):,}")

    front_cols = [
        "date",
        "ticker",
        *[col for col in ["theme", "role", "region", "notes"] if col in out.columns],
        *[col for col in ["open", "high", "low", "close", "adj_close", "volume"] if col in out.columns],
        "raw_return",
        "market_ticker",
        "sector_ticker",
        "market_return",
        "sector_return",
        "market_beta",
        "sector_beta",
        "beta_observations",
        "beta_estimation_end",
        "residual_return",
        *[
            col
            for col in [
                "commodity_symbol_mktseccomm",
                "commodity_return_mktseccomm",
                "commodity_beta_mktseccomm",
                "residual_return_mktseccomm",
                "commodity_beta_return_column_mktseccomm",
            ]
            if col in out.columns
        ],
    ]
    remaining = [col for col in out.columns if col not in front_cols]
    result = out[[col for col in front_cols if col in out.columns] + remaining].sort_values(
        ["ticker", "date"]
    ).reset_index(drop=True)
    log(f"finished dataset assembly with {len(result):,} rows x {len(result.columns):,} columns")
    return result


def build_equity_processed_dataset_from_paths(
    prices_dir: Path,
    universe_path: Path,
    theme_hedges_path: Path,
    output_path: Path,
    commodity_signals_path: Path | None = None,
    exposure_map_path: Path | None = None,
    market_ticker: str = "SPY",
    start: str | None = "2010-01-01",
    end: str | None = None,
    beta_variations: list[str] | None = None,
    primary_variation: str = DEFAULT_PRIMARY_PROCESSED_BETA_VARIATION,
    beta_lag_days: int = 1,
    commodity_beta_symbols: list[str] | None = None,
    commodity_return_column: str = DEFAULT_COMMODITY_BETA_RETURN_COLUMN,
    include_commodity_beta_residuals: bool = True,
    progress: bool = False,
) -> pd.DataFrame:
    dataset = build_equity_processed_dataset(
        prices_dir=prices_dir,
        universe_path=universe_path,
        theme_hedges_path=theme_hedges_path,
        commodity_signals_path=commodity_signals_path,
        exposure_map_path=exposure_map_path,
        market_ticker=market_ticker,
        start=start,
        end=end,
        beta_variations=beta_variations,
        primary_variation=primary_variation,
        beta_lag_days=beta_lag_days,
        commodity_beta_symbols=commodity_beta_symbols,
        commodity_return_column=commodity_return_column,
        include_commodity_beta_residuals=include_commodity_beta_residuals,
        progress=progress,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if progress:
        print(f"[build-equity-processed] writing {len(dataset):,} rows to {output_path}", flush=True)
    if output_path.suffix == ".parquet":
        dataset.to_parquet(output_path, index=False)
    elif output_path.suffix == ".csv":
        dataset.to_csv(output_path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")
    return dataset


def build_equity_beta_returns_from_paths(
    prices_dir: Path,
    universe_path: Path,
    theme_hedges_path: Path,
    output_path: Path,
    market_ticker: str = "SPY",
    beta_lookback_days: int = 252,
    beta_lookback_months: int = 12,
    min_beta_observations: int = 126,
    beta_lag_days: int = 1,
    beta_return_frequency: str = "weekly",
    beta_update_frequency: str = "monthly",
    beta_weighting: str = "exponential",
    beta_half_life_months: float = 3.0,
    beta_smoothing: float = 0.0,
    hedge_ratio_scale: float = 1.0,
) -> pd.DataFrame:
    beta_returns = build_equity_beta_returns(
        prices_dir=prices_dir,
        universe_path=universe_path,
        theme_hedges_path=theme_hedges_path,
        market_ticker=market_ticker,
        beta_lookback_days=beta_lookback_days,
        beta_lookback_months=beta_lookback_months,
        min_beta_observations=min_beta_observations,
        beta_lag_days=beta_lag_days,
        beta_return_frequency=beta_return_frequency,
        beta_update_frequency=beta_update_frequency,
        beta_weighting=beta_weighting,
        beta_half_life_months=beta_half_life_months,
        beta_smoothing=beta_smoothing,
        hedge_ratio_scale=hedge_ratio_scale,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix == ".parquet":
        beta_returns.to_parquet(output_path, index=False)
    elif output_path.suffix == ".csv":
        beta_returns.to_csv(output_path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")
    return beta_returns
