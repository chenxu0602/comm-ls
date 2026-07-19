from __future__ import annotations

from pathlib import Path
from time import perf_counter

import numpy as np
import pandas as pd


def fill_missing_close_from_ohl(frame: pd.DataFrame) -> pd.DataFrame:
    """Fill a missing Yahoo close from OHL3 while preserving adjustment scale."""
    out = frame.copy()
    required = {"open", "high", "low", "close"}
    if not required.issubset(out.columns):
        return out

    for col in ["open", "high", "low", "close", "adj_close"]:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")

    adj_missing = out["adj_close"].isna() if "adj_close" in out.columns else True
    proxy_mask = out["close"].isna() & adj_missing & out[["open", "high", "low"]].notna().all(axis=1)
    proxy_close = out[["open", "high", "low"]].mean(axis=1)

    existing_proxy = pd.Series(False, index=out.index)
    if "close_proxy_used" in out.columns:
        raw_proxy = out["close_proxy_used"]
        if pd.api.types.is_bool_dtype(raw_proxy):
            existing_proxy = raw_proxy.fillna(False)
        else:
            existing_proxy = raw_proxy.astype(str).str.lower().isin({"1", "true", "yes"})

    if "adj_close" in out.columns:
        valid_ratio = out["close"].notna() & out["adj_close"].notna() & out["close"].ne(0)
        adjustment_ratio = (out["adj_close"] / out["close"]).where(valid_ratio)
        adjustment_ratio = adjustment_ratio.replace([np.inf, -np.inf], np.nan).ffill().fillna(1.0)
        out.loc[proxy_mask, "adj_close"] = proxy_close.loc[proxy_mask] * adjustment_ratio.loc[proxy_mask]

    out.loc[proxy_mask, "close"] = proxy_close.loc[proxy_mask]
    out["close_proxy_used"] = existing_proxy | proxy_mask
    return out


def download_yfinance_prices(
    tickers: list[str],
    output_dir: Path,
    start: str = "2000-01-01",
    end: str | None = None,
    auto_adjust: bool = False,
) -> list[Path]:
    import yfinance as yf

    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    unique_tickers = sorted(set(tickers))
    total = len(unique_tickers)

    for position, ticker in enumerate(unique_tickers, start=1):
        started = perf_counter()
        print(f"[download-equities] START {position}/{total} ticker={ticker}", flush=True)
        try:
            data = yf.download(
                ticker,
                start=start,
                end=end,
                auto_adjust=auto_adjust,
                progress=False,
                threads=False,
            )
        except Exception as exc:
            elapsed = perf_counter() - started
            print(
                f"[download-equities] FAILED {position}/{total} ticker={ticker} "
                f"elapsed={elapsed:.1f}s error={exc}",
                flush=True,
            )
            raise
        if data.empty:
            elapsed = perf_counter() - started
            print(
                f"[download-equities] EMPTY {position}/{total} ticker={ticker} "
                f"elapsed={elapsed:.1f}s",
                flush=True,
            )
            continue

        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        data = data.reset_index()
        data.columns = [str(col).lower().replace(" ", "_") for col in data.columns]
        data.insert(0, "ticker", ticker)
        data = fill_missing_close_from_ohl(data)

        path = output_dir / f"{ticker.replace('/', '-')}.csv"
        data.to_csv(path, index=False)
        written.append(path)
        latest_date = pd.to_datetime(data["date"], errors="coerce").max()
        latest_label = latest_date.date().isoformat() if pd.notna(latest_date) else "unknown"
        elapsed = perf_counter() - started
        proxy_rows = int(data["close_proxy_used"].sum()) if "close_proxy_used" in data.columns else 0
        print(
            f"[download-equities] FINISHED {position}/{total} ticker={ticker} "
            f"rows={len(data):,} latest={latest_label} close_proxy_rows={proxy_rows} "
            f"elapsed={elapsed:.1f}s",
            flush=True,
        )

    return written


def load_price_file(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "date" not in df.columns:
        raise ValueError(f"{path} has no date column")
    if "ticker" not in df.columns:
        df.insert(0, "ticker", path.stem)

    df["date"] = pd.to_datetime(df["date"], utc=False)
    for col in df.columns.difference(["ticker", "date", "close_proxy_used"]):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = fill_missing_close_from_ohl(df)
    return df.sort_values("date").reset_index(drop=True)


def load_price_directory(prices_dir: Path) -> pd.DataFrame:
    frames = [load_price_file(path) for path in sorted(prices_dir.glob("*.csv"))]
    if not frames:
        raise FileNotFoundError(f"No price CSV files found in {prices_dir}")
    return pd.concat(frames, ignore_index=True)
