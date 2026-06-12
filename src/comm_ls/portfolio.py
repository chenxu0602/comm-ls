from __future__ import annotations

from pathlib import Path

import pandas as pd


REQUIRED_SCORE_COLUMNS = {"date", "ticker", "score"}


def load_scores(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = REQUIRED_SCORE_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"{path} is missing required columns: {sorted(missing)}")

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], utc=False)
    df["ticker"] = df["ticker"].astype(str).str.upper().str.strip()
    df["score"] = pd.to_numeric(df["score"], errors="coerce")
    return df.dropna(subset=["score"]).sort_values(["date", "ticker"]).reset_index(drop=True)


def load_shortability(path: Path) -> pd.DataFrame:
    if path.suffix == ".parquet":
        df = pd.read_parquet(path)
    else:
        df = pd.read_csv(path)

    required = {"date", "ticker", "can_short"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"{path} is missing required columns: {sorted(missing)}")

    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], utc=False)
    df["ticker"] = df["ticker"].astype(str).str.upper().str.strip()
    df["can_short"] = df["can_short"].astype(bool)
    if "price" in df.columns:
        df = df[pd.to_numeric(df["price"], errors="coerce").notna()].copy()
    return df[["date", "ticker", "can_short"]].drop_duplicates(["date", "ticker"])


def align_shortability_asof(
    scores: pd.DataFrame,
    shortability: pd.DataFrame,
    max_staleness_days: int = 5,
) -> pd.DataFrame:
    """Attach the latest per-ticker shortability known on or before each score date."""

    if scores.empty:
        out = scores.copy()
        out["can_short"] = pd.Series(dtype=bool)
        out["shortability_date"] = pd.NaT
        return out

    if shortability.empty:
        out = scores.copy()
        out["can_short"] = False
        out["shortability_date"] = pd.NaT
        return out

    score_rows = scores.copy()
    score_rows["date"] = pd.to_datetime(score_rows["date"], utc=False)
    score_rows["ticker"] = score_rows["ticker"].astype(str).str.upper().str.strip()
    score_rows["_score_row"] = range(len(score_rows))

    borrow = shortability.copy()
    borrow["date"] = pd.to_datetime(borrow["date"], utc=False)
    borrow["ticker"] = borrow["ticker"].astype(str).str.upper().str.strip()
    borrow = borrow.rename(columns={"date": "shortability_date"})

    frames: list[pd.DataFrame] = []
    for ticker, group in score_rows.groupby("ticker", sort=False):
        ticker_borrow = borrow[borrow["ticker"] == ticker].sort_values("shortability_date")
        g = group.sort_values("date")
        if ticker_borrow.empty:
            g = g.copy()
            g["shortability_date"] = pd.NaT
            g["can_short"] = False
            frames.append(g)
            continue

        aligned = pd.merge_asof(
            g,
            ticker_borrow[["shortability_date", "can_short"]],
            left_on="date",
            right_on="shortability_date",
            direction="backward",
        )
        staleness = (aligned["date"] - aligned["shortability_date"]).dt.days
        stale = aligned["shortability_date"].isna() | (staleness > max_staleness_days)
        aligned["can_short"] = aligned["can_short"].fillna(False) & ~stale
        frames.append(aligned)

    out = pd.concat(frames, ignore_index=True).sort_values("_score_row").drop(columns=["_score_row"])
    return out.reset_index(drop=True)


def _equal_weight(rows: pd.DataFrame, gross: float) -> pd.Series:
    if rows.empty:
        return pd.Series(dtype=float)
    return pd.Series(gross / len(rows), index=rows.index)


def build_long_short_weights(
    scores: pd.DataFrame,
    shortability: pd.DataFrame | None = None,
    long_count: int = 20,
    short_count: int = 20,
    gross_long: float = 1.0,
    gross_short: float = 1.0,
    shortability_max_staleness_days: int = 5,
) -> pd.DataFrame:
    if shortability is not None:
        scores = align_shortability_asof(
            scores=scores,
            shortability=shortability,
            max_staleness_days=shortability_max_staleness_days,
        )
    else:
        scores = scores.copy()
        scores["can_short"] = True
        scores["shortability_date"] = pd.NaT

    frames: list[pd.DataFrame] = []
    for date, group in scores.groupby("date", sort=True):
        g = group.sort_values("score", ascending=False).copy()
        longs = g.head(long_count).copy()
        long_tickers = set(longs["ticker"])
        short_candidates = g[g["can_short"] & ~g["ticker"].isin(long_tickers)]
        shorts = short_candidates.tail(short_count).copy()

        longs["weight"] = _equal_weight(longs, gross_long)
        shorts["weight"] = -_equal_weight(shorts, gross_short)

        out = pd.concat([longs, shorts], ignore_index=True)
        out["date"] = date
        out["leg"] = ["long"] * len(longs) + ["short"] * len(shorts)
        out["hedge_mode"] = "single_name_short"
        extra_cols = ["shortability_date"] if "shortability_date" in out.columns else []
        frames.append(out[["date", "ticker", "score", "leg", "weight", "hedge_mode", *extra_cols]])

    if not frames:
        return pd.DataFrame(
            columns=["date", "ticker", "score", "leg", "weight", "hedge_mode", "shortability_date"]
        )
    return pd.concat(frames, ignore_index=True)


def build_long_index_hedge_weights(
    scores: pd.DataFrame,
    long_count: int = 20,
    gross_long: float = 1.0,
    hedge_symbol: str = "SPY",
    hedge_weight: float = -1.0,
) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for date, group in scores.groupby("date", sort=True):
        longs = group.sort_values("score", ascending=False).head(long_count).copy()
        longs["weight"] = _equal_weight(longs, gross_long)
        longs["leg"] = "long"
        longs["hedge_mode"] = "index_hedge"

        hedge = pd.DataFrame(
            [
                {
                    "date": date,
                    "ticker": hedge_symbol.upper(),
                    "score": pd.NA,
                    "leg": "hedge",
                    "weight": hedge_weight,
                    "hedge_mode": "index_hedge",
                }
            ]
        )
        frames.append(pd.concat([longs[["date", "ticker", "score", "leg", "weight", "hedge_mode"]], hedge]))

    if not frames:
        return pd.DataFrame(columns=["date", "ticker", "score", "leg", "weight", "hedge_mode"])
    return pd.concat(frames, ignore_index=True).reset_index(drop=True)


def write_weights(weights: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix == ".parquet":
        weights.to_parquet(output_path, index=False)
    elif output_path.suffix == ".csv":
        weights.to_csv(output_path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")
