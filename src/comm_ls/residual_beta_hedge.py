"""Shared explicit hedge engine using the betas that built notebook residuals.

No regressions are performed here. Dates are decision dates: the beta source
and its estimation cutoff must both be known by the decision date.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

METHODS = {
    "residual_return_mkt_w12m": "mkt_w12m",
    "residual_return_mktsec_w12m": "mktsec_w12m",
}
BETA_MODE = "notebook_residual_cached_beta_v1"
DEFAULT_PANEL = Path("data/processed/equity_processed.parquet")


def return_method(strategy: str, component: str = "", sector: str | None = None) -> str:
    if strategy == "crypto" or (strategy == "cl" and component.startswith("cr")):
        return "residual_return_mkt_w12m"
    # Fuel uses the notebook mktsec residual too; sector=SPY collapses it
    # to a single SPY regression in the processed panel.
    return "residual_return_mktsec_w12m"


class ResidualBetaStore:
    def __init__(self, frame: pd.DataFrame, source: str = "in_memory"):
        self.source = source
        frame = frame.copy()
        frame["date"] = pd.to_datetime(frame["date"], errors="raise").dt.normalize()
        frame["ticker"] = frame["ticker"].astype(str)
        if frame.duplicated(["date", "ticker"]).any():
            raise ValueError("Duplicate processed equity date/ticker rows")
        self.frame = frame.sort_values(["ticker", "date"])
        self.histories = {
            ticker: group.set_index("date").sort_index()
            for ticker, group in self.frame.groupby("ticker", sort=False)
        }

    @classmethod
    def from_path(cls, path: Path, tickers: list[str] | None = None):
        columns = ["date", "ticker", "market_ticker", "sector_ticker", "raw_return",
                   "market_return", "sector_return"]
        for method, suffix in METHODS.items():
            columns += [method, f"market_beta_{suffix}", f"sector_beta_{suffix}",
                        f"beta_observations_{suffix}", f"beta_estimation_end_{suffix}"]
        frame = pd.read_parquet(path, columns=columns)
        if tickers is not None:
            frame = frame[frame.ticker.isin(tickers)]
        return cls(frame, str(path))

    def lookup(self, ticker: str, method: str, as_of, *, market="SPY", sector=None):
        if method not in METHODS:
            raise ValueError(f"Unsupported residual method: {method}")
        day = pd.Timestamp(as_of).normalize()
        if ticker not in self.histories:
            raise ValueError(f"No cached beta history for {ticker}")
        sample = self.histories[ticker].loc[:day]
        if sample.empty:
            raise ValueError(f"No cached beta for {ticker} known by {day.date()}")
        row = sample.iloc[-1]
        suffix = METHODS[method]
        cutoff = pd.Timestamp(row[f"beta_estimation_end_{suffix}"])
        bm = float(row[f"market_beta_{suffix}"])
        bs = float(row[f"sector_beta_{suffix}"]) if suffix == "mktsec_w12m" else 0.0
        source_market = str(row["market_ticker"])
        source_sector = str(row["sector_ticker"]) if suffix == "mktsec_w12m" else ""
        # When market and sector are SPY, the processed residual has bs=0.
        effective_sector = source_sector if source_sector != source_market else ""
        requested_sector = sector or ""
        if source_market != market or effective_sector != requested_sector:
            raise ValueError(
                f"{ticker}:{method} cached hedge mapping {source_market}/{effective_sector} "
                f"does not match requested {market}/{requested_sector}"
            )
        if (pd.isna(cutoff) or cutoff > day or not np.isfinite([bm, bs]).all()):
            raise ValueError(f"Invalid/future cached beta for {ticker}:{method} at {day.date()}")
        # A missing current stock row must not silently select stale/future data.
        if sample.index[-1] != day:
            raise ValueError(f"Missing beta source row for {ticker} on {day.date()}")
        return {
            "instrument": ticker, "return_method": method,
            "market_hedge": market, "sector_hedge": requested_sector,
            "market_beta": bm, "sector_beta": bs,
            "beta_observations": float(row[f"beta_observations_{suffix}"]),
            "beta_source_date": sample.index[-1], "beta_estimation_end": cutoff,
            "beta_source_path": self.source, "beta_mode": BETA_MODE,
        }

    def history(self, ticker: str, method: str, calendar: pd.DatetimeIndex):
        """Exact source-date history; do not fill missing beta or return rows."""
        if ticker not in self.histories:
            raise ValueError(f"No processed history for {ticker}")
        suffix = METHODS[method]
        frame = self.histories[ticker].reindex(calendar)
        result = pd.DataFrame(index=calendar)
        result["market_beta"] = frame[f"market_beta_{suffix}"]
        result["sector_beta"] = frame[f"sector_beta_{suffix}"] if suffix == "mktsec_w12m" else 0.0
        result["market_return"] = frame.market_return
        result["sector_return"] = frame.sector_return if suffix == "mktsec_w12m" else 0.0
        result["raw_return"] = frame.raw_return
        result["residual_return"] = frame[method]
        result["beta_estimation_end"] = pd.to_datetime(frame[f"beta_estimation_end_{suffix}"])
        if (result.beta_estimation_end > calendar).any():
            raise ValueError(f"Future beta estimation cutoff: {ticker}:{method}")
        result["market_hedge"] = frame.market_ticker
        result["sector_hedge"] = frame.sector_ticker if suffix == "mktsec_w12m" else ""
        return result


def component_hedge_weights(stock_weight, market_beta, sector_beta=0.0):
    """The same multiplication is used by historical and daily target paths."""
    return -stock_weight * market_beta, -stock_weight * sector_beta


def snapshot_hedges(legs: pd.DataFrame, store: ResidualBetaStore, as_of):
    """Per-sleeve betas first, then ETF netting, including offsetting stock legs."""
    rows = []
    totals: dict[str, float] = {}
    for leg in legs.to_dict("records"):
        weight = float(leg["target_weight"])
        if weight == 0:
            continue
        beta = store.lookup(leg["instrument"], leg["return_method"], as_of,
                            sector=leg.get("sector_hedge") or None)
        hm, hs = component_hedge_weights(weight, beta["market_beta"], beta["sector_beta"])
        totals[beta["market_hedge"]] = totals.get(beta["market_hedge"], 0.0) + hm
        if beta["sector_hedge"]:
            totals[beta["sector_hedge"]] = totals.get(beta["sector_hedge"], 0.0) + hs
        rows.append(dict(leg, **beta, market_hedge_weight=hm, sector_hedge_weight=hs))
    return pd.Series(totals, dtype=float), pd.DataFrame(rows)


def beta_notes(source: str) -> str:
    return (
        "## Beta algorithm change: notebook residual cached beta\n\n"
        f"- beta_mode: `{BETA_MODE}`. Source: `{source}`.\n"
        "- Uses the already-computed beta for each notebook residual: "
        "`market_beta_mktsec_w12m` / `sector_beta_mktsec_w12m`, or "
        "`market_beta_mkt_w12m` for SPY-only sleeves.\n"
        "- Source pipeline default: 12-month weekly returns, exponential weighting "
        "(3-month half-life), monthly updates. No new daily 252-session regression.\n"
        "- CL CRO and Crypto use SPY only; other CL sleeves and Metals keep their "
        "existing residual-specific sector mapping. Shared core: "
        "`comm_ls.residual_beta_hedge`, also used by the new explicit backtest.\n"
        "- Exact beta values, source dates and estimation cutoffs are in "
        "`beta_sources.csv`. Only observations known by the signal as-of are used.\n"
        "- The beta change can produce ETF migration orders even when the stock "
        "signal is unchanged. Compare with the legacy package before execution.\n"
        "- Prices, integer rounding, caps, trade buffers and intraday fills can "
        "still differ from implicit research PnL. At monthly beta updates the "
        "prior-close explicit hedge and the return-day residual beta can differ "
        "by one session; the new audit reports that timing gap separately.\n"
    )
