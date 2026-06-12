from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from comm_ls.equity import load_price_directory


SHORTABILITY_COLUMNS = [
    "date",
    "arrival",
    "ticker",
    "ssr_triggered",
    "ssr_active",
    "threshold_security",
    "ibkr_shortable_score",
    "ibkr_shortable_shares",
    "borrow_fee_rate",
    "hard_to_borrow",
    "can_short",
    "short_entry_price_test_constrained",
    "price",
    "adv_63d",
    "source",
]


def build_shortability_frame(
    prices: pd.DataFrame,
    min_price: float = 5.0,
    min_adv: float = 10_000_000.0,
    lookback_days: int = 63,
) -> pd.DataFrame:
    price_col = "close" if "close" in prices.columns else "adj_close"
    required = {"ticker", "date", "low", price_col, "volume"}
    missing = required.difference(prices.columns)
    if missing:
        raise ValueError(f"Price data is missing required columns: {sorted(missing)}")

    frames: list[pd.DataFrame] = []
    for ticker, group in prices.groupby("ticker", sort=True):
        g = group.sort_values("date").copy()
        prev_close = g[price_col].shift(1)
        dollar_volume = g[price_col] * g["volume"]

        ssr_triggered = g["low"] <= prev_close * 0.90
        ssr_active = ssr_triggered | ssr_triggered.shift(1, fill_value=False)
        adv = dollar_volume.rolling(lookback_days, min_periods=max(20, lookback_days // 2)).mean()
        price = g[price_col]

        can_short = (price >= min_price) & (adv >= min_adv)
        hard_to_borrow = np.where(can_short, False, pd.NA)

        out = pd.DataFrame(
            {
                "date": g["date"],
                "arrival": g["date"],
                "ticker": ticker,
                "ssr_triggered": ssr_triggered.fillna(False),
                "ssr_active": ssr_active.fillna(False),
                "threshold_security": pd.NA,
                "ibkr_shortable_score": np.nan,
                "ibkr_shortable_shares": np.nan,
                "borrow_fee_rate": np.nan,
                "hard_to_borrow": hard_to_borrow,
                "can_short": can_short.fillna(False),
                "short_entry_price_test_constrained": ssr_active.fillna(False),
                "price": price,
                "adv_63d": adv,
                "source": "yfinance_price_proxy",
            }
        )
        frames.append(out)

    if not frames:
        return pd.DataFrame(columns=SHORTABILITY_COLUMNS)

    result = pd.concat(frames, ignore_index=True)
    return result[SHORTABILITY_COLUMNS].sort_values(["date", "ticker"]).reset_index(drop=True)


def build_shortability_from_price_directory(
    prices_dir: Path,
    min_price: float = 5.0,
    min_adv: float = 10_000_000.0,
    lookback_days: int = 63,
) -> pd.DataFrame:
    prices = load_price_directory(prices_dir)
    return build_shortability_frame(
        prices=prices,
        min_price=min_price,
        min_adv=min_adv,
        lookback_days=lookback_days,
    )
