from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_NARROW = ROOT / "data/processed/equity_processed_agriculture_sector.parquet"
DEFAULT_LIQUID = ROOT / "data/processed/equity_processed_agriculture_liquid_sector.parquet"
DEFAULT_OUTPUT = ROOT / "data/processed/equity_processed_agriculture.parquet"
KEYS = ["ticker", "date"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Combine narrow- and liquid-sector Agriculture equity residual panels."
    )
    parser.add_argument("--narrow", type=Path, default=DEFAULT_NARROW)
    parser.add_argument("--liquid", type=Path, default=DEFAULT_LIQUID)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def _prepare(path: Path) -> pd.DataFrame:
    frame = pd.read_parquet(path)
    missing = set(KEYS + ["sector_ticker", "residual_return_mktsec_w12m"]).difference(
        frame.columns
    )
    if missing:
        raise ValueError(f"{path} missing columns: {sorted(missing)}")
    frame = frame.copy()
    frame["ticker"] = frame["ticker"].astype(str).str.upper()
    frame["date"] = pd.to_datetime(frame["date"]).dt.normalize()
    if frame.duplicated(KEYS).any():
        raise ValueError(f"{path} contains duplicate ticker/date rows")
    return frame.sort_values(KEYS).reset_index(drop=True)


def main() -> None:
    args = parse_args()
    narrow = _prepare(args.narrow)
    liquid = _prepare(args.liquid)
    if not narrow[KEYS].equals(liquid[KEYS]):
        raise ValueError("Narrow and liquid Agriculture panels have different ticker/date rows")

    output = narrow.copy()
    output["sector_ticker_narrow"] = output["sector_ticker"]
    output["sector_ticker_liquid"] = liquid["sector_ticker"].to_numpy()

    # Keep the project-wide canonical columns as narrow-sector aliases. Add
    # explicit names for both Agriculture alternatives so research cannot
    # silently select the better in-sample hedge.
    narrow_columns = [column for column in narrow if "mktsec_w12m" in column]
    liquid_columns = [column for column in liquid if "mktsec_w12m" in column]
    if set(narrow_columns) != set(liquid_columns):
        raise ValueError("Narrow and liquid panels expose different mktsec_w12m schemas")
    for column in narrow_columns:
        output[column.replace("mktsec_w12m", "mktsec_narrow_w12m")] = narrow[column]
        output[column.replace("mktsec_w12m", "mktsec_liquid_w12m")] = liquid[column].to_numpy()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    output.to_parquet(args.output, index=False)
    print(
        f"Wrote {len(output):,} Agriculture equity rows with canonical=narrow and "
        f"explicit narrow/liquid residuals to {args.output}"
    )


if __name__ == "__main__":
    main()
