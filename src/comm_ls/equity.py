from __future__ import annotations

from pathlib import Path
from time import perf_counter

import numpy as np
import pandas as pd


DEFAULT_SECURITY_LIFECYCLE_PATH = (
    Path(__file__).resolve().parents[2] / "config/equity_security_lifecycle.csv"
)
DEFAULT_TICKER_LINEAGE_PATH = (
    Path(__file__).resolve().parents[2] / "config/equity_ticker_lineage.csv"
)


def load_security_lifecycle(path: Path = DEFAULT_SECURITY_LIFECYCLE_PATH) -> pd.DataFrame:
    """Load dated security boundaries used to prevent post-event return leakage."""
    if not path.exists():
        return pd.DataFrame(
            columns=[
                "ticker",
                "effective_start_date",
                "effective_end_date",
                "continuity_policy",
            ]
        )

    lifecycle = pd.read_csv(path)
    required = {"ticker", "effective_start_date", "effective_end_date", "continuity_policy"}
    missing = required.difference(lifecycle.columns)
    if missing:
        raise ValueError(f"{path} is missing required columns: {sorted(missing)}")

    lifecycle = lifecycle.copy()
    lifecycle["ticker"] = lifecycle["ticker"].astype(str).str.upper().str.strip()
    for column in ["effective_start_date", "effective_end_date"]:
        lifecycle[column] = pd.to_datetime(lifecycle[column], errors="coerce")
    lifecycle["continuity_policy"] = lifecycle["continuity_policy"].astype(str).str.strip()
    unsupported = sorted(
        set(lifecycle["continuity_policy"]).difference({"stop_no_splice"})
    )
    if unsupported:
        raise ValueError(f"{path} has unsupported continuity policies: {unsupported}")
    invalid_dates = (
        lifecycle["effective_start_date"].notna()
        & lifecycle["effective_end_date"].notna()
        & lifecycle["effective_start_date"].gt(lifecycle["effective_end_date"])
    )
    if invalid_dates.any():
        tickers = sorted(lifecycle.loc[invalid_dates, "ticker"].unique())
        raise ValueError(f"{path} has start dates after end dates for: {tickers}")
    duplicate_tickers = lifecycle.loc[lifecycle["ticker"].duplicated(), "ticker"].unique()
    if len(duplicate_tickers):
        raise ValueError(
            f"{path} has duplicate security lifecycle rows for: {sorted(duplicate_tickers)}"
        )
    return lifecycle.reset_index(drop=True)


def apply_security_lifecycle(
    frame: pd.DataFrame,
    lifecycle: pd.DataFrame,
) -> pd.DataFrame:
    """Clip each ticker to its own listed-security identity without successor splicing."""
    if frame.empty or lifecycle.empty:
        return frame
    if not {"ticker", "date"}.issubset(frame.columns):
        raise ValueError("Price frame must contain ticker and date columns")

    out = frame.copy()
    out["ticker"] = out["ticker"].astype(str).str.upper().str.strip()
    out["date"] = pd.to_datetime(out["date"], utc=False)
    boundaries = lifecycle.set_index("ticker")

    keep = pd.Series(True, index=out.index)
    for ticker, rows in out.groupby("ticker", sort=False).groups.items():
        if ticker not in boundaries.index:
            continue
        boundary = boundaries.loc[ticker]
        start_date = boundary["effective_start_date"]
        end_date = boundary["effective_end_date"]
        if pd.notna(start_date):
            keep.loc[rows] &= out.loc[rows, "date"].ge(start_date)
        if pd.notna(end_date):
            keep.loc[rows] &= out.loc[rows, "date"].le(end_date)

    return out.loc[keep].sort_values(["ticker", "date"]).reset_index(drop=True)


def load_ticker_lineage(path: Path = DEFAULT_TICKER_LINEAGE_PATH) -> pd.DataFrame:
    """Load same-security ticker aliases with dated exchange validity."""
    if not path.exists():
        return pd.DataFrame(
            columns=[
                "security_id",
                "canonical_ticker",
                "historical_ticker",
                "effective_start_date",
                "effective_end_date",
                "continuity_policy",
            ]
        )

    lineage = pd.read_csv(path)
    required = {
        "security_id",
        "canonical_ticker",
        "historical_ticker",
        "effective_start_date",
        "effective_end_date",
        "continuity_policy",
    }
    missing = required.difference(lineage.columns)
    if missing:
        raise ValueError(f"{path} is missing required columns: {sorted(missing)}")

    lineage = lineage.copy()
    lineage["security_id"] = lineage["security_id"].astype(str).str.strip()
    for column in ["canonical_ticker", "historical_ticker"]:
        lineage[column] = lineage[column].astype(str).str.upper().str.strip()
    for column in ["effective_start_date", "effective_end_date"]:
        lineage[column] = pd.to_datetime(lineage[column], errors="coerce")
    lineage["continuity_policy"] = lineage["continuity_policy"].astype(str).str.strip()

    unsupported = sorted(
        set(lineage["continuity_policy"]).difference({"same_security_ticker_change"})
    )
    if unsupported:
        raise ValueError(f"{path} has unsupported continuity policies: {unsupported}")
    canonical_counts = lineage.groupby("security_id")["canonical_ticker"].nunique()
    if canonical_counts.gt(1).any():
        security_ids = sorted(canonical_counts[canonical_counts.gt(1)].index)
        raise ValueError(f"{path} has multiple canonical tickers for: {security_ids}")
    invalid_dates = (
        lineage["effective_start_date"].notna()
        & lineage["effective_end_date"].notna()
        & lineage["effective_start_date"].gt(lineage["effective_end_date"])
    )
    if invalid_dates.any():
        security_ids = sorted(lineage.loc[invalid_dates, "security_id"].unique())
        raise ValueError(f"{path} has start dates after end dates for: {security_ids}")
    return lineage.reset_index(drop=True)


def apply_ticker_lineage(
    frame: pd.DataFrame,
    lineage: pd.DataFrame,
) -> pd.DataFrame:
    """Map dated ticker aliases to one research identity without double counting."""
    if frame.empty or lineage.empty:
        return frame
    if not {"ticker", "date"}.issubset(frame.columns):
        raise ValueError("Price frame must contain ticker and date columns")

    out = frame.copy().reset_index(drop=True)
    out["ticker"] = out["ticker"].astype(str).str.upper().str.strip()
    out["date"] = pd.to_datetime(out["date"], utc=False)
    if "source_ticker" not in out.columns:
        out["source_ticker"] = out["ticker"]
    else:
        out["source_ticker"] = out["source_ticker"].astype(str).str.upper().str.strip()
    out["historical_ticker"] = out["source_ticker"]
    out["security_id"] = pd.NA
    out["_lineage_priority"] = 0
    out["_lineage_member"] = False
    out["_lineage_matched"] = False
    out["_lineage_valid_source"] = True
    out["_row_order"] = np.arange(len(out))

    for security_id, aliases in lineage.groupby("security_id", sort=False):
        canonical_ticker = str(aliases["canonical_ticker"].iloc[0])
        historical_tickers = set(aliases["historical_ticker"])
        member = out["source_ticker"].isin(historical_tickers | {canonical_ticker})
        out.loc[member, "_lineage_member"] = True

        for alias in aliases.itertuples(index=False):
            interval = member.copy()
            if pd.notna(alias.effective_start_date):
                interval &= out["date"].ge(alias.effective_start_date)
            if pd.notna(alias.effective_end_date):
                interval &= out["date"].le(alias.effective_end_date)
            if not interval.any():
                continue

            historical_ticker = str(alias.historical_ticker)
            valid_source = out["source_ticker"].isin(
                {historical_ticker, canonical_ticker}
            )
            out.loc[interval, "_lineage_matched"] = True
            out.loc[interval, "_lineage_valid_source"] = valid_source.loc[interval]
            out.loc[interval, "security_id"] = security_id
            out.loc[interval, "historical_ticker"] = historical_ticker
            out.loc[interval, "ticker"] = canonical_ticker
            out.loc[interval, "_lineage_priority"] = (
                2 * out.loc[interval, "source_ticker"].eq(historical_ticker).astype(int)
                + out.loc[interval, "source_ticker"].eq(canonical_ticker).astype(int)
            )

    invalid_lineage_rows = out["_lineage_member"] & (
        ~out["_lineage_matched"] | ~out["_lineage_valid_source"]
    )
    out = out.loc[~invalid_lineage_rows].copy()
    out = (
        out.sort_values(
            ["ticker", "date", "_lineage_priority", "_row_order"],
            ascending=[True, True, False, True],
        )
        .drop_duplicates(["ticker", "date"], keep="first")
        .drop(
            columns=[
                "_lineage_priority",
                "_lineage_member",
                "_lineage_matched",
                "_lineage_valid_source",
                "_row_order",
            ]
        )
    )
    return out.sort_values(["ticker", "date"]).reset_index(drop=True)


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
        preserved_gap_rows = 0
        if path.exists():
            existing = pd.read_csv(path)
            if "date" not in existing.columns:
                raise ValueError(f"{path} has no date column")

            existing_dates = pd.to_datetime(existing["date"], errors="coerce", utc=True)
            in_requested_range = existing_dates.ge(pd.Timestamp(start, tz="UTC"))
            if end is not None:
                in_requested_range &= existing_dates.lt(pd.Timestamp(end, tz="UTC"))
            existing = existing.loc[in_requested_range].copy()

            downloaded_dates = pd.to_datetime(data["date"], errors="coerce", utc=True)
            downloaded_keys = set(downloaded_dates.dropna().dt.normalize())
            existing_keys = pd.to_datetime(
                existing["date"], errors="coerce", utc=True
            ).dt.normalize()
            preserve = existing_keys.notna() & ~existing_keys.isin(downloaded_keys)
            preserved = existing.loc[preserve].copy()
            preserved_gap_rows = len(preserved)
            if preserved_gap_rows:
                column_order = list(data.columns) + [
                    column for column in preserved.columns if column not in data.columns
                ]
                data = pd.concat([data, preserved], ignore_index=True, sort=False)
                data["_sort_date"] = pd.to_datetime(
                    data["date"], errors="coerce", utc=True
                )
                data = (
                    data.sort_values("_sort_date", kind="stable")
                    .drop(columns="_sort_date")
                    .loc[:, column_order]
                    .reset_index(drop=True)
                )
        normalized_dates = pd.to_datetime(data["date"], errors="coerce", utc=True)
        valid_dates = normalized_dates.notna()
        data.loc[valid_dates, "date"] = normalized_dates.loc[valid_dates].dt.strftime(
            "%Y-%m-%d"
        )
        data.to_csv(path, index=False)
        written.append(path)
        latest_date = pd.to_datetime(data["date"], errors="coerce").max()
        latest_label = latest_date.date().isoformat() if pd.notna(latest_date) else "unknown"
        elapsed = perf_counter() - started
        proxy_rows = int(data["close_proxy_used"].sum()) if "close_proxy_used" in data.columns else 0
        print(
            f"[download-equities] FINISHED {position}/{total} ticker={ticker} "
            f"rows={len(data):,} latest={latest_label} close_proxy_rows={proxy_rows} "
            f"preserved_gap_rows={preserved_gap_rows} "
            f"elapsed={elapsed:.1f}s",
            flush=True,
        )

    return written


def load_price_file(
    path: Path,
    security_lifecycle_path: Path | None = DEFAULT_SECURITY_LIFECYCLE_PATH,
    ticker_lineage_path: Path | None = DEFAULT_TICKER_LINEAGE_PATH,
) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "date" not in df.columns:
        raise ValueError(f"{path} has no date column")
    if "ticker" not in df.columns:
        df.insert(0, "ticker", path.stem)

    df["date"] = pd.to_datetime(df["date"], utc=False)
    for col in df.columns.difference(["ticker", "date", "close_proxy_used"]):
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = fill_missing_close_from_ohl(df)
    if security_lifecycle_path is not None:
        df = apply_security_lifecycle(df, load_security_lifecycle(security_lifecycle_path))
    if ticker_lineage_path is not None:
        df = apply_ticker_lineage(df, load_ticker_lineage(ticker_lineage_path))
    return df.sort_values("date").reset_index(drop=True)


def load_price_directory(
    prices_dir: Path,
    security_lifecycle_path: Path | None = DEFAULT_SECURITY_LIFECYCLE_PATH,
    ticker_lineage_path: Path | None = DEFAULT_TICKER_LINEAGE_PATH,
) -> pd.DataFrame:
    lifecycle = (
        load_security_lifecycle(security_lifecycle_path)
        if security_lifecycle_path is not None
        else pd.DataFrame()
    )
    lineage = (
        load_ticker_lineage(ticker_lineage_path)
        if ticker_lineage_path is not None
        else pd.DataFrame()
    )
    frames = [
        load_price_file(
            path,
            security_lifecycle_path=None,
            ticker_lineage_path=None,
        )
        for path in sorted(prices_dir.glob("*.csv"))
    ]
    if not frames:
        raise FileNotFoundError(f"No price CSV files found in {prices_dir}")
    prices = apply_security_lifecycle(pd.concat(frames, ignore_index=True), lifecycle)
    return apply_ticker_lineage(prices, lineage)
