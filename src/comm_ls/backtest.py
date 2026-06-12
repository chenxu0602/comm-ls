from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from comm_ls.equity import load_price_directory
from comm_ls.portfolio import (
    build_long_index_hedge_weights,
    build_long_short_weights,
    load_scores,
    load_shortability,
    write_weights,
)


def _prepare_daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    price_col = "close" if "close" in prices.columns else "adj_close"
    required = {"ticker", "date", price_col}
    missing = required.difference(prices.columns)
    if missing:
        raise ValueError(f"Price data is missing required columns: {sorted(missing)}")

    frames: list[pd.DataFrame] = []
    for ticker, group in prices.groupby("ticker", sort=True):
        g = group.sort_values("date").copy()
        frames.append(
            pd.DataFrame(
                {
                    "ticker": str(ticker).upper().strip(),
                    "date": g["date"],
                    "daily_return": pd.to_numeric(g[price_col], errors="coerce").pct_change(),
                }
            )
        )
    return pd.concat(frames, ignore_index=True).dropna(subset=["daily_return"])


def _max_drawdown(equity: pd.Series) -> float:
    if equity.empty:
        return np.nan
    peak = equity.cummax()
    drawdown = equity / peak - 1.0
    return float(drawdown.min())


def _portfolio_weights_for_scores(
    score_slice: pd.DataFrame,
    mode: str,
    shortability: pd.DataFrame | None,
    long_count: int,
    short_count: int,
    gross_long: float,
    gross_short: float,
    hedge_symbol: str,
    hedge_weight: float,
    shortability_max_staleness_days: int,
) -> pd.DataFrame:
    if mode == "long-short":
        return build_long_short_weights(
            scores=score_slice,
            shortability=shortability,
            long_count=long_count,
            short_count=short_count,
            gross_long=gross_long,
            gross_short=gross_short,
            shortability_max_staleness_days=shortability_max_staleness_days,
        )
    if mode == "index-hedge":
        return build_long_index_hedge_weights(
            scores=score_slice,
            long_count=long_count,
            gross_long=gross_long,
            hedge_symbol=hedge_symbol,
            hedge_weight=hedge_weight,
        )
    raise ValueError("mode must be 'long-short' or 'index-hedge'")


def run_score_backtest(
    scores: pd.DataFrame,
    prices: pd.DataFrame,
    mode: str = "index-hedge",
    shortability: pd.DataFrame | None = None,
    long_count: int = 20,
    short_count: int = 20,
    gross_long: float = 1.0,
    gross_short: float = 1.0,
    hedge_symbol: str = "SPY",
    hedge_weight: float = -1.0,
    hold_days: int = 21,
    execution_lag_days: int = 1,
    transaction_cost_bps: float = 0.0,
    capital_per_sleeve: float | None = None,
    shortability_max_staleness_days: int = 5,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    if hold_days <= 0:
        raise ValueError("hold_days must be positive")
    if execution_lag_days <= 0:
        raise ValueError("execution_lag_days must be positive")

    score_data = scores.copy()
    score_data["date"] = pd.to_datetime(score_data["date"], utc=False)
    score_data["ticker"] = score_data["ticker"].astype(str).str.upper().str.strip()
    score_data["score"] = pd.to_numeric(score_data["score"], errors="coerce")
    score_data = score_data.dropna(subset=["date", "ticker", "score"]).sort_values(["date", "ticker"])
    if score_data.empty:
        empty_daily = pd.DataFrame(
            columns=["date", "gross_return", "transaction_cost", "net_return", "active_sleeves", "equity"]
        )
        empty_summary = pd.DataFrame()
        empty_weights = pd.DataFrame()
        return empty_daily, empty_weights, empty_summary

    returns = _prepare_daily_returns(prices)
    calendar = pd.Index(sorted(returns["date"].dropna().unique()))
    sleeve_capital = capital_per_sleeve if capital_per_sleeve is not None else 1.0 / hold_days

    daily_rows: list[pd.DataFrame] = []
    weight_rows: list[pd.DataFrame] = []
    rebalance_count = 0

    for signal_date, score_slice in score_data.groupby("date", sort=True):
        weights = _portfolio_weights_for_scores(
            score_slice=score_slice,
            mode=mode,
            shortability=shortability,
            long_count=long_count,
            short_count=short_count,
            gross_long=gross_long,
            gross_short=gross_short,
            hedge_symbol=hedge_symbol,
            hedge_weight=hedge_weight,
            shortability_max_staleness_days=shortability_max_staleness_days,
        )
        if weights.empty:
            continue

        future_dates = calendar[calendar > signal_date]
        if len(future_dates) < execution_lag_days:
            continue
        entry_idx = execution_lag_days - 1
        holding_dates = future_dates[entry_idx : entry_idx + hold_days]
        if len(holding_dates) == 0:
            continue

        rebalance_count += 1
        sleeve_id = f"{pd.Timestamp(signal_date).date().isoformat()}#{rebalance_count}"
        weights = weights.copy()
        weights["signal_date"] = pd.Timestamp(signal_date)
        weights["entry_date"] = pd.Timestamp(holding_dates[0])
        weights["exit_date"] = pd.Timestamp(holding_dates[-1])
        weights["sleeve_id"] = sleeve_id
        weights["capital"] = sleeve_capital
        weight_rows.append(weights)

        sleeve_returns = returns[returns["date"].isin(holding_dates)].merge(
            weights[["ticker", "weight"]],
            on="ticker",
            how="inner",
        )
        if sleeve_returns.empty:
            continue
        sleeve_returns["weighted_return"] = sleeve_returns["weight"] * sleeve_returns["daily_return"] * sleeve_capital
        sleeve_daily = (
            sleeve_returns.groupby("date", sort=True)
            .agg(gross_return=("weighted_return", "sum"), active_positions=("ticker", "nunique"))
            .reset_index()
        )
        sleeve_daily["sleeve_id"] = sleeve_id
        sleeve_daily["signal_date"] = pd.Timestamp(signal_date)
        sleeve_daily["transaction_cost"] = 0.0
        entry_date = pd.Timestamp(holding_dates[0])
        entry_cost = float(weights["weight"].abs().sum()) * sleeve_capital * transaction_cost_bps / 10_000.0
        sleeve_daily.loc[sleeve_daily["date"] == entry_date, "transaction_cost"] = entry_cost
        daily_rows.append(sleeve_daily)

    weights_out = pd.concat(weight_rows, ignore_index=True) if weight_rows else pd.DataFrame()
    if not daily_rows:
        empty_daily = pd.DataFrame(
            columns=["date", "gross_return", "transaction_cost", "net_return", "active_sleeves", "equity"]
        )
        return empty_daily, weights_out, pd.DataFrame()

    sleeve_daily = pd.concat(daily_rows, ignore_index=True)
    daily = (
        sleeve_daily.groupby("date", sort=True)
        .agg(
            gross_return=("gross_return", "sum"),
            transaction_cost=("transaction_cost", "sum"),
            active_sleeves=("sleeve_id", "nunique"),
            active_positions=("active_positions", "sum"),
        )
        .reset_index()
    )
    daily["net_return"] = daily["gross_return"] - daily["transaction_cost"]
    daily["equity"] = (1.0 + daily["net_return"]).cumprod()

    n_days = len(daily)
    total_return = float(daily["equity"].iloc[-1] - 1.0) if n_days else np.nan
    ann_return = float(daily["equity"].iloc[-1] ** (252 / n_days) - 1.0) if n_days else np.nan
    ann_vol = float(daily["net_return"].std(ddof=0) * np.sqrt(252)) if n_days else np.nan
    sharpe = ann_return / ann_vol if ann_vol and not np.isnan(ann_vol) else np.nan

    summary = pd.DataFrame(
        [
            {
                "start_date": daily["date"].min(),
                "end_date": daily["date"].max(),
                "trading_days": n_days,
                "rebalance_count": rebalance_count,
                "mode": mode,
                "hold_days": hold_days,
                "execution_lag_days": execution_lag_days,
                "capital_per_sleeve": sleeve_capital,
                "transaction_cost_bps": transaction_cost_bps,
                "total_return": total_return,
                "annualized_return": ann_return,
                "annualized_volatility": ann_vol,
                "sharpe": sharpe,
                "max_drawdown": _max_drawdown(daily["equity"]),
                "average_active_sleeves": float(daily["active_sleeves"].mean()),
            }
        ]
    )
    return daily, weights_out, summary


def write_frame(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix == ".parquet":
        df.to_parquet(output_path, index=False)
    elif output_path.suffix == ".csv":
        df.to_csv(output_path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")


def run_score_backtest_from_paths(
    scores_path: Path,
    prices_dir: Path,
    output_daily_path: Path,
    output_weights_path: Path,
    output_summary_path: Path,
    mode: str = "index-hedge",
    shortability_path: Path | None = None,
    long_count: int = 20,
    short_count: int = 20,
    gross_long: float = 1.0,
    gross_short: float = 1.0,
    hedge_symbol: str = "SPY",
    hedge_weight: float = -1.0,
    hold_days: int = 21,
    execution_lag_days: int = 1,
    transaction_cost_bps: float = 0.0,
    capital_per_sleeve: float | None = None,
    shortability_max_staleness_days: int = 5,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    scores = load_scores(scores_path)
    prices = load_price_directory(prices_dir)
    shortability = load_shortability(shortability_path) if shortability_path else None
    daily, weights, summary = run_score_backtest(
        scores=scores,
        prices=prices,
        mode=mode,
        shortability=shortability,
        long_count=long_count,
        short_count=short_count,
        gross_long=gross_long,
        gross_short=gross_short,
        hedge_symbol=hedge_symbol,
        hedge_weight=hedge_weight,
        hold_days=hold_days,
        execution_lag_days=execution_lag_days,
        transaction_cost_bps=transaction_cost_bps,
        capital_per_sleeve=capital_per_sleeve,
        shortability_max_staleness_days=shortability_max_staleness_days,
    )
    write_frame(daily, output_daily_path)
    write_weights(weights, output_weights_path)
    write_frame(summary, output_summary_path)
    return daily, weights, summary
