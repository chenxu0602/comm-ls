from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from comm_ls.equity import load_price_directory


DEFAULT_FEATURES = [
    "m0_ret_1d",
    "ret_5d",
    "ret_21d",
    "ret_42d",
    "ret_63d",
    "ret_accel_21d_vs_63d",
    "up_days_21d",
    "drawdown_63d",
    "breakout_252d",
    "front_price_high_share_63d_q80_3y",
    "front_price_high_share_100d_q80_3y",
    "front_price_high_share_126d_q80_3y",
    "front_price_high_days_100d_q80_3y",
    "front_price_high_excess_100d_q80_3y",
    "front_price_high_consecutive_days_q80_3y",
    "front_price_high_share_63d_q90_3y",
    "front_price_high_share_100d_q90_3y",
    "front_price_high_share_126d_q90_3y",
    "front_price_high_days_100d_q90_3y",
    "front_price_high_excess_100d_q90_3y",
    "front_price_high_consecutive_days_q90_3y",
    "front_price_low_share_63d_q20_3y",
    "front_price_low_share_100d_q20_3y",
    "front_price_low_share_126d_q20_3y",
    "front_price_low_days_100d_q20_3y",
    "front_price_low_shortfall_100d_q20_3y",
    "front_price_low_consecutive_days_q20_3y",
    "front_price_low_share_63d_q10_3y",
    "front_price_low_share_100d_q10_3y",
    "front_price_low_share_126d_q10_3y",
    "front_price_low_days_100d_q10_3y",
    "front_price_low_shortfall_100d_q10_3y",
    "front_price_low_consecutive_days_q10_3y",
    "front_second_spread",
    "front_third_spread",
    "front_second_annualized_carry",
    "front_third_annualized_carry",
    "front_second_backwardation_steepness",
    "front_third_backwardation_steepness",
    "calendar_dec_annualized_carry",
    "next_jun_annualized_carry",
    "liquid_deferred_annualized_carry",
    "activity_deferred_annualized_carry",
    "calendar_dec_backwardation_steepness",
    "liquid_deferred_backwardation_steepness",
    "activity_deferred_backwardation_steepness",
    "calendar_dec_log_ret_1d",
    "calendar_dec_log_ret_5d",
    "calendar_dec_log_ret_21d",
    "next_jun_log_ret_1d",
    "next_jun_log_ret_5d",
    "next_jun_log_ret_21d",
    "liquid_deferred_log_ret_1d",
    "liquid_deferred_log_ret_5d",
    "liquid_deferred_log_ret_21d",
    "activity_deferred_log_ret_1d",
    "activity_deferred_log_ret_5d",
    "activity_deferred_log_ret_21d",
    "front_second_spread_chg_21d",
    "front_third_spread_chg_21d",
    "front_second_annualized_carry_chg_21d",
    "front_third_annualized_carry_chg_21d",
    "front_second_backwardation_steepness_chg_21d",
    "front_third_backwardation_steepness_chg_21d",
    "calendar_dec_annualized_carry_chg_21d",
    "next_jun_annualized_carry_chg_21d",
    "liquid_deferred_annualized_carry_chg_21d",
    "activity_deferred_annualized_carry_chg_21d",
    "calendar_dec_backwardation_steepness_chg_21d",
    "liquid_deferred_backwardation_steepness_chg_21d",
    "activity_deferred_backwardation_steepness_chg_21d",
    "carry",
    "carry_chg_21d",
    "ng_forward_summer_strip_annualized_carry",
    "ng_forward_winter_strip_annualized_carry",
    "ng_forward_summer_strip_backwardation_steepness",
    "ng_forward_winter_strip_backwardation_steepness",
    "ng_forward_summer_strip_annualized_carry_chg_21d",
    "ng_forward_winter_strip_annualized_carry_chg_21d",
    "ng_forward_summer_strip_backwardation_steepness_chg_21d",
    "ng_forward_winter_strip_backwardation_steepness_chg_21d",
    "ng_winter_summer_strip_log_spread",
    "ng_winter_summer_strip_log_spread_chg_21d",
    "ng_winter_summer_strip_spread",
    "ng_winter_summer_strip_spread_chg_21d",
    "ng_front_settle_month_z_5y",
    "ng_front_settle_month_pctile_5y",
    "term_structure_regime_change",
    "backwardation_regime_change",
    "days_in_backwardation",
    "realized_vol_20d",
    "vol_chg_20d",
    "abs_ret_1d",
    "m0_atr_14_pct",
    "volume_surge_63d",
    "oi_surge_63d",
    "price_volume_confirm_21d",
    "price_oi_confirm_21d",
    "volume_shock_63d",
    "oi_shock_63d",
    "carry_pctile_252d",
]


def load_frame(path: Path) -> pd.DataFrame:
    if path.suffix == ".parquet":
        return pd.read_parquet(path)
    return pd.read_csv(path)


def _prepare_commodity_events(
    commodity_signals: pd.DataFrame,
    features: list[str],
    shock_z_threshold: float,
    feature_z_window: int,
    min_feature_observations: int,
) -> pd.DataFrame:
    signals = commodity_signals.copy()
    signals["date"] = pd.to_datetime(signals["date"], utc=False)
    signals["arrival"] = pd.to_datetime(signals["arrival"], utc=False)

    missing = set(features).difference(signals.columns)
    if missing:
        raise ValueError(f"Commodity signals are missing features: {sorted(missing)}")

    events: list[pd.DataFrame] = []
    for symbol, group in signals.groupby("symbol", sort=True):
        g = group.sort_values("date").copy()
        for feature in features:
            value = pd.to_numeric(g[feature], errors="coerce")
            mean = value.rolling(feature_z_window, min_periods=min_feature_observations).mean()
            std = value.rolling(feature_z_window, min_periods=min_feature_observations).std()
            z = (value - mean) / std
            event = pd.DataFrame(
                {
                    "event_date": g["date"],
                    "arrival": g["arrival"],
                    "commodity": symbol,
                    "feature": feature,
                    "feature_value": value,
                    "feature_z": z,
                }
            )
            event = event[event["feature_z"].abs() >= shock_z_threshold]
            events.append(event)

    if not events:
        return pd.DataFrame(
            columns=["event_date", "arrival", "commodity", "feature", "feature_value", "feature_z"]
        )
    return pd.concat(events, ignore_index=True).dropna(subset=["feature_z"])


def _prepare_forward_returns(prices: pd.DataFrame, horizons: list[int]) -> pd.DataFrame:
    price_col = "close" if "close" in prices.columns else "adj_close"
    required = {"ticker", "date", price_col}
    missing = required.difference(prices.columns)
    if missing:
        raise ValueError(f"Price data is missing required columns: {sorted(missing)}")

    frames: list[pd.DataFrame] = []
    for ticker, group in prices.groupby("ticker", sort=True):
        g = group.sort_values("date").copy()
        out = g[["ticker", "date", price_col]].copy()
        for horizon in horizons:
            out[f"fwd_ret_{horizon}d"] = out[price_col].shift(-horizon) / out[price_col] - 1.0
        frames.append(out.drop(columns=[price_col]))

    return pd.concat(frames, ignore_index=True).sort_values(["ticker", "date"]).reset_index(drop=True)


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
                    "ticker": ticker,
                    "date": g["date"],
                    "daily_ret": g[price_col].pct_change(),
                }
            )
        )
    return pd.concat(frames, ignore_index=True).dropna(subset=["daily_ret"])


def _load_sector_map(path: Path | None) -> dict[str, str]:
    if path is None:
        return {}
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


def _compute_rolling_betas(
    daily_returns: pd.DataFrame,
    quarterly_universe: pd.DataFrame,
    market_ticker: str,
    sector_map: dict[str, str],
    beta_lookback_days: int,
    min_beta_observations: int,
) -> pd.DataFrame:
    market = market_ticker.upper()
    factor_tickers = sorted({market, *sector_map.values()})
    factors = daily_returns[daily_returns["ticker"].isin(factor_tickers)].pivot(
        index="date", columns="ticker", values="daily_ret"
    )
    missing_factors = [ticker for ticker in factor_tickers if ticker not in factors.columns]
    if missing_factors:
        raise ValueError(
            f"Missing hedge ticker price data for: {missing_factors}. "
            "Download these tickers into --prices-dir before using --residualize."
        )

    quarterly = quarterly_universe[["ticker", "theme"]].drop_duplicates("ticker").copy()
    rows: list[pd.DataFrame] = []
    for row in quarterly.itertuples(index=False):
        ticker = str(row.ticker).upper()
        theme = str(row.theme)
        sector = sector_map.get(theme)
        stock = daily_returns[daily_returns["ticker"] == ticker][["date", "daily_ret"]].rename(
            columns={"daily_ret": "stock_ret"}
        )
        if stock.empty:
            continue

        data = stock.merge(factors.reset_index(), on="date", how="left")
        beta_mkt_raw = data["stock_ret"].rolling(beta_lookback_days, min_periods=min_beta_observations).cov(
            data[market]
        ) / data[market].rolling(beta_lookback_days, min_periods=min_beta_observations).var()
        beta_mkt = beta_mkt_raw.shift(1)  # lag to avoid look-ahead

        if sector and sector != market:
            residual_stock = data["stock_ret"] - beta_mkt * data[market]
            sector_mkt_beta_raw = (
                data[sector].rolling(beta_lookback_days, min_periods=min_beta_observations).cov(data[market])
                / data[market].rolling(beta_lookback_days, min_periods=min_beta_observations).var()
            ).shift(1)
            residual_sector = data[sector] - sector_mkt_beta_raw * data[market]
            beta_sector = residual_stock.rolling(beta_lookback_days, min_periods=min_beta_observations).cov(
                residual_sector
            ) / residual_sector.rolling(beta_lookback_days, min_periods=min_beta_observations).var()
            beta_sector = beta_sector.shift(1)
        else:
            beta_sector = pd.Series(0.0, index=data.index)
            sector = market

        rows.append(
            pd.DataFrame(
                {
                    "ticker": ticker,
                    "date": data["date"],
                    "theme": theme,
                    "sector_ticker": sector,
                    "market_beta": beta_mkt,
                    "sector_beta": beta_sector,
                }
            )
        )

    if not rows:
        return pd.DataFrame(columns=["ticker", "date", "theme", "sector_ticker", "market_beta", "sector_beta"])
    return pd.concat(rows, ignore_index=True)


def _apply_residual_trading_unit_adjustment(
    returns: pd.DataFrame,
    prices: pd.DataFrame,
    quarterly_universe: pd.DataFrame,
    horizons: list[int],
    market_ticker: str,
    sector_map_path: Path | None,
    beta_lookback_days: int,
    min_beta_observations: int,
) -> pd.DataFrame:
    sector_map = _load_sector_map(sector_map_path)
    daily_returns = _prepare_daily_returns(prices)
    betas = _compute_rolling_betas(
        daily_returns=daily_returns,
        quarterly_universe=quarterly_universe,
        market_ticker=market_ticker,
        sector_map=sector_map,
        beta_lookback_days=beta_lookback_days,
        min_beta_observations=min_beta_observations,
    )

    factor_forward = returns[
        returns["ticker"].isin({market_ticker.upper(), *sector_map.values()})
    ][["ticker", "date"] + [f"fwd_ret_{horizon}d" for horizon in horizons]]
    factor_forward = factor_forward.rename(columns={"ticker": "factor_ticker"})

    adjusted = returns.merge(betas, on=["ticker", "date"], how="left")
    market_fwd = factor_forward[factor_forward["factor_ticker"] == market_ticker.upper()].drop(
        columns=["factor_ticker"]
    )
    market_fwd = market_fwd.rename(columns={f"fwd_ret_{horizon}d": f"market_fwd_ret_{horizon}d" for horizon in horizons})
    adjusted = adjusted.merge(market_fwd, on="date", how="left")

    sector_fwd = factor_forward.rename(
        columns={f"fwd_ret_{horizon}d": f"sector_fwd_ret_{horizon}d" for horizon in horizons}
    )
    adjusted = adjusted.merge(
        sector_fwd,
        left_on=["sector_ticker", "date"],
        right_on=["factor_ticker", "date"],
        how="left",
    ).drop(columns=["factor_ticker"])

    for horizon in horizons:
        ret_col = f"fwd_ret_{horizon}d"
        adjusted[ret_col] = (
            adjusted[ret_col]
            - adjusted["market_beta"] * adjusted[f"market_fwd_ret_{horizon}d"]
            - adjusted["sector_beta"] * adjusted[f"sector_fwd_ret_{horizon}d"]
        )

    drop_cols = ["market_beta", "sector_beta", "theme", "sector_ticker"]
    drop_cols += [f"market_fwd_ret_{horizon}d" for horizon in horizons]
    drop_cols += [f"sector_fwd_ret_{horizon}d" for horizon in horizons]
    return adjusted.drop(columns=drop_cols)


def _apply_market_adjustment(
    returns: pd.DataFrame,
    benchmark_ticker: str,
    horizons: list[int],
) -> pd.DataFrame:
    benchmark = benchmark_ticker.upper()
    bench = returns[returns["ticker"] == benchmark][["date"] + [f"fwd_ret_{horizon}d" for horizon in horizons]].copy()
    if bench.empty:
        raise ValueError(
            f"Benchmark ticker {benchmark} was not found in price data. "
            "Download it into --prices-dir before using --adjust-market."
        )

    bench = bench.rename(columns={f"fwd_ret_{horizon}d": f"benchmark_fwd_ret_{horizon}d" for horizon in horizons})
    adjusted = returns.merge(bench, on="date", how="left")
    for horizon in horizons:
        ret_col = f"fwd_ret_{horizon}d"
        bench_col = f"benchmark_fwd_ret_{horizon}d"
        adjusted[ret_col] = adjusted[ret_col] - adjusted[bench_col]
    return adjusted.drop(columns=[f"benchmark_fwd_ret_{horizon}d" for horizon in horizons])


def _filter_non_overlapping_events(events: pd.DataFrame, min_gap_days: int) -> pd.DataFrame:
    if events.empty:
        return events

    kept: list[pd.DataFrame] = []
    for _, group in events.sort_values("event_date").groupby(["commodity", "feature"], sort=True):
        last_date: pd.Timestamp | None = None
        rows: list[pd.Series] = []
        for _, row in group.iterrows():
            event_date = pd.Timestamp(row["event_date"])
            if last_date is None or (event_date - last_date).days >= min_gap_days:
                rows.append(row)
                last_date = event_date
        if rows:
            kept.append(pd.DataFrame(rows))

    if not kept:
        return events.iloc[0:0]
    return pd.concat(kept, ignore_index=True)


def _active_universe_for_date(quarterly_universe: pd.DataFrame, as_of_date: pd.Timestamp) -> pd.DataFrame:
    available = quarterly_universe[quarterly_universe["rebalance_date"] <= as_of_date]
    if available.empty:
        return quarterly_universe.iloc[0:0]
    rebalance_date = available["rebalance_date"].max()
    return available[available["rebalance_date"] == rebalance_date]


def build_feature_reaction_study(
    commodity_signals: pd.DataFrame,
    prices: pd.DataFrame,
    quarterly_universe: pd.DataFrame,
    as_of_dates: list[pd.Timestamp] | None = None,
    features: list[str] | None = None,
    horizons: list[int] | None = None,
    lookback_years: float = 3.0,
    shock_z_threshold: float = 1.0,
    feature_z_window: int = 252,
    min_feature_observations: int = 126,
    min_events: int = 8,
    adjust_market: str | None = None,
    non_overlap_events: bool = False,
    residualize: bool = False,
    residual_market: str = "SPY",
    sector_map_path: Path | None = None,
    beta_lookback_days: int = 252,
    min_beta_observations: int = 126,
) -> pd.DataFrame:
    features = features or DEFAULT_FEATURES
    horizons = horizons or [5, 10, 21]

    quarterly = quarterly_universe.copy()
    quarterly["rebalance_date"] = pd.to_datetime(quarterly["rebalance_date"], utc=False)
    quarterly["ticker"] = quarterly["ticker"].astype(str).str.upper().str.strip()

    returns = _prepare_forward_returns(prices, horizons)
    returns["date"] = pd.to_datetime(returns["date"], utc=False)
    if residualize:
        returns = _apply_residual_trading_unit_adjustment(
            returns=returns,
            prices=prices,
            quarterly_universe=quarterly,
            horizons=horizons,
            market_ticker=residual_market,
            sector_map_path=sector_map_path,
            beta_lookback_days=beta_lookback_days,
            min_beta_observations=min_beta_observations,
        )
    elif adjust_market:
        returns = _apply_market_adjustment(returns, adjust_market, horizons)

    events = _prepare_commodity_events(
        commodity_signals=commodity_signals,
        features=features,
        shock_z_threshold=shock_z_threshold,
        feature_z_window=feature_z_window,
        min_feature_observations=min_feature_observations,
    )
    if events.empty:
        return pd.DataFrame()

    if as_of_dates is None:
        as_of_dates = sorted(quarterly["rebalance_date"].unique())
    else:
        as_of_dates = [pd.Timestamp(date) for date in as_of_dates]

    rows: list[dict[str, object]] = []
    lookback_days = int(round(lookback_years * 365.25))

    for as_of_date in as_of_dates:
        as_of = pd.Timestamp(as_of_date)
        active = _active_universe_for_date(quarterly, as_of)
        tickers = active["ticker"].drop_duplicates().tolist()
        if not tickers:
            continue

        start = as_of - pd.Timedelta(days=lookback_days)
        event_window = events[(events["arrival"] <= as_of) & (events["event_date"] >= start)]
        if event_window.empty:
            continue

        for horizon in horizons:
            horizon_events = (
                _filter_non_overlapping_events(event_window, horizon) if non_overlap_events else event_window
            )
            if horizon_events.empty:
                continue

            event_keys = horizon_events[
                ["event_date", "commodity", "feature", "feature_value", "feature_z"]
            ].rename(columns={"event_date": "date"})
            ticker_dates = pd.MultiIndex.from_product(
                [tickers, event_keys["date"].unique()], names=["ticker", "date"]
            ).to_frame(index=False)
            joined = ticker_dates.merge(returns, on=["ticker", "date"], how="left")
            joined = joined.merge(event_keys, on="date", how="inner")
            joined = joined.dropna(subset=["feature_z"])

            ret_col = f"fwd_ret_{horizon}d"
            sample = joined.dropna(subset=[ret_col])
            if sample.empty:
                continue

            for (commodity, feature, ticker), group in sample.groupby(["commodity", "feature", "ticker"]):
                if len(group) < min_events:
                    continue

                signed = np.sign(group["feature_z"]) * group[ret_col]
                corr = group["feature_z"].corr(group[ret_col])
                rows.append(
                    {
                        "as_of_date": as_of,
                        "commodity": commodity,
                        "feature": feature,
                        "ticker": ticker,
                        "horizon_days": horizon,
                        "event_count": int(len(group)),
                        "mean_signed_return": float(signed.mean()),
                        "median_signed_return": float(signed.median()),
                        "hit_rate": float((signed > 0).mean()),
                        "feature_return_corr": float(corr) if pd.notna(corr) else np.nan,
                        "avg_abs_feature_z": float(group["feature_z"].abs().mean()),
                        "return_adjustment": (
                            f"residual:{residual_market.upper()}+sector"
                            if residualize
                            else f"market:{adjust_market.upper()}"
                            if adjust_market
                            else "none"
                        ),
                        "non_overlap_events": non_overlap_events,
                        "reaction_tstat": float(signed.mean() / (signed.std(ddof=1) / np.sqrt(len(signed))))
                        if len(signed) > 1 and signed.std(ddof=1) > 0
                        else np.nan,
                    }
                )

    if not rows:
        return pd.DataFrame(
            columns=[
                "as_of_date",
                "commodity",
                "feature",
                "ticker",
                "horizon_days",
                "event_count",
                "mean_signed_return",
                "median_signed_return",
                "hit_rate",
                "feature_return_corr",
                "avg_abs_feature_z",
                "return_adjustment",
                "non_overlap_events",
                "reaction_tstat",
            ]
        )

    result = pd.DataFrame(rows)
    return result.sort_values(
        ["as_of_date", "commodity", "feature", "horizon_days", "reaction_tstat"],
        ascending=[True, True, True, True, False],
    ).reset_index(drop=True)


def build_feature_reaction_study_from_paths(
    commodity_signals_path: Path,
    prices_dir: Path,
    quarterly_universe_path: Path,
    output_path: Path,
    features: list[str] | None = None,
    horizons: list[int] | None = None,
    as_of_date: str | None = None,
    lookback_years: float = 3.0,
    shock_z_threshold: float = 1.0,
    feature_z_window: int = 252,
    min_feature_observations: int = 126,
    min_events: int = 8,
    adjust_market: str | None = None,
    non_overlap_events: bool = False,
    residualize: bool = False,
    residual_market: str = "SPY",
    sector_map_path: Path | None = None,
    beta_lookback_days: int = 252,
    min_beta_observations: int = 126,
) -> pd.DataFrame:
    commodity_signals = load_frame(commodity_signals_path)
    prices = load_price_directory(prices_dir)
    quarterly_universe = load_frame(quarterly_universe_path)

    as_of_dates = [pd.Timestamp(as_of_date)] if as_of_date else None
    result = build_feature_reaction_study(
        commodity_signals=commodity_signals,
        prices=prices,
        quarterly_universe=quarterly_universe,
        as_of_dates=as_of_dates,
        features=features,
        horizons=horizons,
        lookback_years=lookback_years,
        shock_z_threshold=shock_z_threshold,
        feature_z_window=feature_z_window,
        min_feature_observations=min_feature_observations,
        min_events=min_events,
        adjust_market=adjust_market,
        non_overlap_events=non_overlap_events,
        residualize=residualize,
        residual_market=residual_market,
        sector_map_path=sector_map_path,
        beta_lookback_days=beta_lookback_days,
        min_beta_observations=min_beta_observations,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix == ".parquet":
        result.to_parquet(output_path, index=False)
    elif output_path.suffix == ".csv":
        result.to_csv(output_path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")
    return result
