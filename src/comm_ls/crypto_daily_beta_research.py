"""Additive legacy-production SPY residual research; never used by live targets."""
from pathlib import Path

import numpy as np
import pandas as pd

RETURN_COLUMN = "residual_return_mkt_d252_prod_lag1"
DEFAULT_OVERLAY = Path("data/processed/crypto_daily_beta_research.parquet")


def daily_production_residual(stock, market, *, window=252, min_obs=126):
    """Estimate after decision close, apply on next observed SPY session.

    Production drops incomplete stock/market pairs before taking the last 252
    observations. Rolling over the compressed paired history reproduces that
    rule, unlike rolling over a union calendar with missing rows.
    """
    calendar = market.dropna().index
    paired = pd.concat({"stock": stock, "market": market}, axis=1).dropna()
    beta = (paired.stock.rolling(window, min_periods=min_obs).cov(paired.market)
            / paired.market.rolling(window, min_periods=min_obs).var().replace(0, np.nan))
    decision = beta.reindex(calendar).ffill()
    cutoff = pd.Series(paired.index, index=paired.index).reindex(calendar).ffill()
    frame = pd.DataFrame(index=calendar)
    frame["raw_return_prod_daily"] = stock.reindex(calendar)
    frame["spy_return_prod_daily"] = market.reindex(calendar)
    frame["market_beta_d252_prod_asof"] = decision
    frame["market_beta_d252_prod_lag1"] = decision.shift(1)
    frame["beta_estimation_end_d252_prod_lag1"] = cutoff.shift(1)
    frame[RETURN_COLUMN] = (frame.raw_return_prod_daily
                           - frame.market_beta_d252_prod_lag1 * frame.spy_return_prod_daily)
    return frame


def add_daily_beta_research_columns(frame, ticker=None, *, overlay_path=DEFAULT_OVERLAY):
    """Overlay new columns onto a notebook cache or processed ticker history."""
    overlay = pd.read_parquet(overlay_path)
    indexed = "date" not in frame.columns
    out = frame.reset_index() if indexed else frame.copy()
    out["date"] = pd.to_datetime(out["date"]).dt.normalize()
    if "ticker" not in out:
        if ticker is None:
            raise ValueError("Provide ticker for a frame without ticker column")
        out["ticker"] = ticker
    columns = [c for c in overlay if c not in {"date", "ticker"} and c not in out]
    merged = out.merge(overlay[["date", "ticker", *columns]], on=["date", "ticker"],
                       how="left", validate="many_to_one", sort=False)
    return merged.set_index("date") if indexed else merged
