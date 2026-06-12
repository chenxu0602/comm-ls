from __future__ import annotations

from pathlib import Path

import pandas as pd

from comm_ls.equity import load_price_directory, load_price_file


def load_seed_universe(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"ticker", "theme", "role"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"{path} is missing required columns: {sorted(missing)}")
    df["ticker"] = df["ticker"].astype(str).str.upper().str.strip()
    return df.drop_duplicates("ticker").reset_index(drop=True)


def load_commodity_exposure_map(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"ticker", "commodity", "exposure_role", "prior_weight"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"{path} is missing required columns: {sorted(missing)}")

    df = df.copy()
    df["ticker"] = df["ticker"].astype(str).str.upper().str.strip()
    df["commodity"] = df["commodity"].astype(str).str.upper().str.strip()
    df["exposure_role"] = df["exposure_role"].astype(str).str.strip()
    df["prior_weight"] = pd.to_numeric(df["prior_weight"], errors="coerce")
    return df.dropna(subset=["ticker", "commodity", "prior_weight"]).drop_duplicates(
        ["ticker", "commodity"]
    ).reset_index(drop=True)


def get_exposure_universe(
    exposure_map_path: Path,
    commodity: str | None = None,
    min_abs_prior_weight: float = 0.0,
) -> pd.DataFrame:
    exposure = load_commodity_exposure_map(exposure_map_path)
    if commodity is not None:
        exposure = exposure[exposure["commodity"] == commodity.upper().strip()].copy()
    exposure = exposure[exposure["prior_weight"].abs() >= min_abs_prior_weight].copy()
    return exposure.sort_values(["commodity", "ticker"]).reset_index(drop=True)


def build_quarterly_liquidity_universe(
    seed_path: Path,
    prices_dir: Path,
    min_price: float = 5.0,
    min_adv: float = 10_000_000.0,
    lookback_days: int = 63,
) -> pd.DataFrame:
    seed = load_seed_universe(seed_path)
    prices = load_price_directory(prices_dir)

    price_col = "close" if "close" in prices.columns else "adj_close"
    required = {"ticker", "date", price_col, "volume"}
    missing = required.difference(prices.columns)
    if missing:
        raise ValueError(f"Downloaded prices are missing columns: {sorted(missing)}")

    prices = prices.merge(seed, on="ticker", how="inner")
    all_dates = pd.Series(prices["date"].unique()).sort_values()
    rebalance_dates = all_dates.groupby(all_dates.dt.to_period("Q")).max().tolist()

    rows: list[dict[str, object]] = []
    for ticker, g in prices.groupby("ticker", sort=True):
        g = g.sort_values("date").copy()
        g["dollar_volume"] = g[price_col] * g["volume"]
        meta = seed.loc[seed["ticker"] == ticker].iloc[0].to_dict()

        for rebalance_date in rebalance_dates:
            hist = g[g["date"] <= rebalance_date].tail(lookback_days)
            if len(hist) < max(20, lookback_days // 2):
                continue

            price = float(hist[price_col].iloc[-1])
            adv = float(hist["dollar_volume"].mean())
            if price < min_price or adv < min_adv:
                continue

            rows.append(
                {
                    "rebalance_date": rebalance_date,
                    "ticker": ticker,
                    "theme": meta["theme"],
                    "role": meta["role"],
                    "price": price,
                    "adv_63d": adv,
                    "lookback_observations": len(hist),
                }
            )

    out = pd.DataFrame(rows)
    if out.empty:
        return out
    return out.sort_values(["rebalance_date", "theme", "ticker"]).reset_index(drop=True)


def build_broad_quarterly_liquidity_universe(
    prices_dir: Path,
    seed_path: Path | None = None,
    start: str = "2010-01-01",
    end: str | None = None,
    min_price: float = 5.0,
    min_adv: float = 10_000_000.0,
    lookback_days: int = 63,
    min_lookback_observations: int = 42,
    min_history_observations: int = 252,
    max_staleness_days: int = 10,
    exclude_tickers: list[str] | None = None,
    max_names: int | None = None,
    universe_source: str = "local_broad_liquidity",
    constituent_pit_status: str = "local_symbol_universe_not_constituent_pit",
) -> pd.DataFrame:
    """Build a broad point-in-time liquidity universe from local price files."""

    prices = load_price_directory(prices_dir)
    price_col = "close" if "close" in prices.columns else "adj_close"
    required = {"ticker", "date", price_col, "volume"}
    missing = required.difference(prices.columns)
    if missing:
        raise ValueError(f"Downloaded prices are missing columns: {sorted(missing)}")

    excluded = {ticker.upper().strip() for ticker in (exclude_tickers or [])}
    prices = prices.copy()
    prices["ticker"] = prices["ticker"].astype(str).str.upper().str.strip()
    prices = prices[~prices["ticker"].isin(excluded)].copy()
    prices[price_col] = pd.to_numeric(prices[price_col], errors="coerce")
    prices["volume"] = pd.to_numeric(prices["volume"], errors="coerce")
    prices = prices.dropna(subset=[price_col, "volume"])
    if prices.empty:
        return pd.DataFrame()

    seed_meta = pd.DataFrame(columns=["ticker", "theme", "role", "region", "notes"])
    if seed_path is not None and seed_path.exists():
        seed_meta = load_seed_universe(seed_path)

    max_price_date = prices["date"].max()
    end_ts = pd.Timestamp(end) if end is not None else max_price_date
    periods = pd.period_range(
        start=pd.Timestamp(start).to_period("Q"),
        end=end_ts.to_period("Q"),
        freq="Q",
    )
    all_dates = pd.Series(prices["date"].unique()).sort_values()
    grouped_prices = {
        ticker: group.sort_values("date").copy()
        for ticker, group in prices.groupby("ticker", sort=True)
    }
    meta_by_ticker = {
        str(row.ticker): row._asdict()
        for row in seed_meta.itertuples(index=False)
    }

    rows: list[dict[str, object]] = []
    for period in periods:
        quarter_start = period.start_time
        asof_target = quarter_start - pd.Timedelta(days=1)
        available_dates = all_dates[all_dates <= asof_target]
        if available_dates.empty:
            continue
        asof_date = pd.Timestamp(available_dates.iloc[-1])

        for ticker, ticker_prices in grouped_prices.items():
            history = ticker_prices[ticker_prices["date"] <= asof_date].copy()
            if history.empty:
                continue

            last_price_date = pd.Timestamp(history["date"].iloc[-1])
            if last_price_date < asof_date - pd.Timedelta(days=max_staleness_days):
                continue

            hist = history.tail(lookback_days).copy()
            if len(hist) < min_lookback_observations or len(history) < min_history_observations:
                continue

            hist["dollar_volume"] = hist[price_col] * hist["volume"]
            price = float(history[price_col].iloc[-1])
            adv = float(hist["dollar_volume"].mean())
            if price < min_price or adv < min_adv:
                continue

            meta = meta_by_ticker.get(ticker, {})
            rows.append(
                {
                    "quarter": _quarter_label(period),
                    "quarter_start": quarter_start.date().isoformat(),
                    "asof_date": asof_date.date().isoformat(),
                    "pit_data_cutoff": asof_date.date().isoformat(),
                    "ticker": ticker,
                    "theme": meta.get("theme", "unknown"),
                    "role": meta.get("role", "unknown"),
                    "region": meta.get("region", "unknown"),
                    "price": price,
                    "adv_63d": adv,
                    "median_dollar_volume_63d": float(hist["dollar_volume"].median()),
                    "lookback_observations": int(len(hist)),
                    "history_observations": int(len(history)),
                    "first_price_date": pd.Timestamp(history["date"].iloc[0]).date().isoformat(),
                    "last_price_date": last_price_date.date().isoformat(),
                    "source": "local_price_directory",
                    "universe_source": universe_source,
                    "pit_status": "price_volume_pit_only",
                    "constituent_pit_status": constituent_pit_status,
                    "max_names": max_names,
                    "is_tradeable": True,
                    "inclusion_rule_version": "broad_quarterly_liquidity_v1",
                }
            )

    out = pd.DataFrame(rows)
    if out.empty:
        return out
    out["dollar_volume_rank"] = (
        out.groupby("quarter")["adv_63d"].rank(method="first", ascending=False).astype(int)
    )
    out["eligible_names_before_cap"] = out.groupby("quarter")["ticker"].transform("count")
    if max_names is not None:
        out = out[out["dollar_volume_rank"] <= max_names].copy()
    out["selected_names_after_cap"] = out.groupby("quarter")["ticker"].transform("count")
    return out.sort_values(["quarter", "dollar_volume_rank", "ticker"]).reset_index(drop=True)


def _quarter_label(period: pd.Period) -> str:
    return f"{period.year}-Q{period.quarter}"


def _candidate_price_frame(prices_dir: Path, tickers: list[str]) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for ticker in sorted(set(tickers)):
        path = prices_dir / f"{ticker.replace('/', '-')}.csv"
        if not path.exists():
            continue
        frames.append(load_price_file(path))
    if not frames:
        raise FileNotFoundError(f"No candidate price CSV files found in {prices_dir}")
    return pd.concat(frames, ignore_index=True)


def build_commodity_quarterly_universes(
    exposure_map_path: Path,
    seed_path: Path,
    prices_dir: Path,
    commodities: list[str],
    start: str = "2010-01-01",
    end: str | None = None,
    min_price: float = 5.0,
    min_adv: float = 10_000_000.0,
    lookback_days: int = 63,
    min_lookback_observations: int = 42,
    min_history_observations: int = 252,
    max_staleness_days: int = 10,
    min_abs_prior_weight: float = 0.0,
) -> pd.DataFrame:
    """Build commodity-specific, quarter-frozen tradeable universes.

    Every row is computed using price and volume data with dates less than or
    equal to the quarter's `asof_date`. The economic candidate list comes from
    `commodity_exposure_map.csv`, so this remains a prototype until that map is
    replaced with point-in-time fundamental/text snapshots.
    """

    if not commodities:
        raise ValueError("At least one commodity is required")

    keep_commodities = [commodity.upper().strip() for commodity in commodities]
    exposure = load_commodity_exposure_map(exposure_map_path)
    exposure = exposure[exposure["commodity"].isin(keep_commodities)].copy()
    exposure = exposure[exposure["prior_weight"].abs() >= min_abs_prior_weight].copy()
    if exposure.empty:
        return pd.DataFrame()

    seed = load_seed_universe(seed_path)
    exposure = exposure.merge(
        seed[["ticker", "theme", "role", "region", "notes"]].rename(
            columns={"role": "primary_role", "notes": "seed_notes"}
        ),
        on="ticker",
        how="inner",
    )
    if exposure.empty:
        return pd.DataFrame()

    prices = _candidate_price_frame(prices_dir, exposure["ticker"].tolist())
    price_col = "close" if "close" in prices.columns else "adj_close"
    required = {"ticker", "date", price_col, "volume"}
    missing = required.difference(prices.columns)
    if missing:
        raise ValueError(f"Downloaded prices are missing columns: {sorted(missing)}")

    prices = prices[prices["ticker"].isin(exposure["ticker"])].copy()
    prices[price_col] = pd.to_numeric(prices[price_col], errors="coerce")
    prices["volume"] = pd.to_numeric(prices["volume"], errors="coerce")
    valid_prices = prices.dropna(subset=[price_col, "volume"]).copy()
    if valid_prices.empty:
        return pd.DataFrame()

    max_price_date = valid_prices["date"].max()
    end_ts = pd.Timestamp(end) if end is not None else max_price_date
    start_period = pd.Timestamp(start).to_period("Q")
    end_period = end_ts.to_period("Q")
    periods = pd.period_range(start=start_period, end=end_period, freq="Q")

    all_dates = pd.Series(valid_prices["date"].unique()).sort_values()
    rows: list[dict[str, object]] = []
    rule_version = "commodity_quarterly_universe_v1"

    grouped_prices = {
        ticker: group.sort_values("date").copy()
        for ticker, group in valid_prices.groupby("ticker", sort=True)
    }

    for period in periods:
        quarter_start = period.start_time
        asof_target = quarter_start - pd.Timedelta(days=1)
        available_dates = all_dates[all_dates <= asof_target]
        if available_dates.empty:
            continue
        asof_date = pd.Timestamp(available_dates.iloc[-1])
        if asof_date > max_price_date:
            continue

        for _, meta in exposure.iterrows():
            ticker = str(meta["ticker"])
            ticker_prices = grouped_prices.get(ticker)
            if ticker_prices is None:
                continue

            history = ticker_prices[ticker_prices["date"] <= asof_date].copy()
            if history.empty:
                continue

            last_price_date = pd.Timestamp(history["date"].iloc[-1])
            if last_price_date < asof_date - pd.Timedelta(days=max_staleness_days):
                continue

            hist = history.tail(lookback_days).copy()
            if len(hist) < min_lookback_observations or len(history) < min_history_observations:
                continue

            hist["dollar_volume"] = hist[price_col] * hist["volume"]
            price = float(history[price_col].iloc[-1])
            adv = float(hist["dollar_volume"].mean())
            median_dollar_volume = float(hist["dollar_volume"].median())
            if price < min_price or adv < min_adv:
                continue

            rows.append(
                {
                    "quarter": _quarter_label(period),
                    "quarter_start": quarter_start.date().isoformat(),
                    "asof_date": asof_date.date().isoformat(),
                    "pit_data_cutoff": asof_date.date().isoformat(),
                    "commodity": str(meta["commodity"]),
                    "ticker": ticker,
                    "theme": str(meta["theme"]),
                    "primary_role": str(meta["primary_role"]),
                    "exposure_role": str(meta["exposure_role"]),
                    "region": str(meta["region"]),
                    "prior_weight": float(meta["prior_weight"]),
                    "price": price,
                    "adv_63d": adv,
                    "median_dollar_volume_63d": median_dollar_volume,
                    "lookback_observations": int(len(hist)),
                    "history_observations": int(len(history)),
                    "first_price_date": pd.Timestamp(history["date"].iloc[0]).date().isoformat(),
                    "last_price_date": last_price_date.date().isoformat(),
                    "source_reason": str(meta["notes"]),
                    "seed_notes": str(meta["seed_notes"]),
                    "is_tradeable": True,
                    "inclusion_rule_version": rule_version,
                }
            )

    out = pd.DataFrame(rows)
    if out.empty:
        return out

    out["dollar_volume_rank"] = (
        out.groupby(["commodity", "quarter"])["adv_63d"]
        .rank(method="first", ascending=False)
        .astype(int)
    )
    columns = [
        "quarter",
        "quarter_start",
        "asof_date",
        "pit_data_cutoff",
        "commodity",
        "ticker",
        "theme",
        "primary_role",
        "exposure_role",
        "region",
        "prior_weight",
        "price",
        "adv_63d",
        "median_dollar_volume_63d",
        "dollar_volume_rank",
        "lookback_observations",
        "history_observations",
        "first_price_date",
        "last_price_date",
        "source_reason",
        "seed_notes",
        "is_tradeable",
        "inclusion_rule_version",
    ]
    return out[columns].sort_values(["commodity", "quarter", "dollar_volume_rank", "ticker"]).reset_index(drop=True)


def write_commodity_quarterly_universe_files(universe: pd.DataFrame, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    if universe.empty:
        return written

    for (commodity, quarter), group in universe.groupby(["commodity", "quarter"], sort=True):
        commodity_dir = output_dir / str(commodity)
        commodity_dir.mkdir(parents=True, exist_ok=True)
        path = commodity_dir / f"{commodity}-Univ-{quarter}.csv"
        group.to_csv(path, index=False)
        written.append(path)
    return written
