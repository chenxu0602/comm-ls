from __future__ import annotations

from pathlib import Path

import pandas as pd


def download_yfinance_prices(
    tickers: list[str],
    output_dir: Path,
    start: str = "2000-01-01",
    end: str | None = None,
    auto_adjust: bool = True,
) -> list[Path]:
    import yfinance as yf

    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    for ticker in sorted(set(tickers)):
        data = yf.download(
            ticker,
            start=start,
            end=end,
            auto_adjust=auto_adjust,
            progress=False,
            threads=False,
        )
        if data.empty:
            continue

        if isinstance(data.columns, pd.MultiIndex):
            data.columns = data.columns.get_level_values(0)

        data = data.reset_index()
        data.columns = [str(col).lower().replace(" ", "_") for col in data.columns]
        data.insert(0, "ticker", ticker)

        path = output_dir / f"{ticker.replace('/', '-')}.csv"
        data.to_csv(path, index=False)
        written.append(path)

    return written


def load_price_file(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "date" not in df.columns:
        raise ValueError(f"{path} has no date column")
    if "ticker" not in df.columns:
        df.insert(0, "ticker", path.stem)

    df["date"] = pd.to_datetime(df["date"], utc=False)
    for col in df.columns.difference(["ticker", "date"]):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df.sort_values("date").reset_index(drop=True)


def load_price_directory(prices_dir: Path) -> pd.DataFrame:
    frames = [load_price_file(path) for path in sorted(prices_dir.glob("*.csv"))]
    if not frames:
        raise FileNotFoundError(f"No price CSV files found in {prices_dir}")
    return pd.concat(frames, ignore_index=True)
