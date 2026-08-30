from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
UNIVERSE_PATH = ROOT / "config/agriculture_equity_beta_universe.csv"
PANEL_CONFIGS = {
    "sector": (
        ROOT / "config/agriculture_ticker_sector_hedges.csv",
        ROOT / "data/processed/equity_processed_agriculture_sector.parquet",
    ),
    "liquid_sector": (
        ROOT / "config/agriculture_ticker_liquid_sector_hedges.csv",
        ROOT / "data/processed/equity_processed_agriculture_liquid_sector.parquet",
    ),
}
COMBINED_PATH = ROOT / "data/processed/equity_processed_agriculture.parquet"

REQUIRED_COLUMNS = {
    "ticker",
    "date",
    "raw_return",
    "market_ticker",
    "sector_ticker",
    "residual_return_mkt_w12m",
    "residual_return_mktsec_w12m",
}


def verify_panel(
    label: str,
    universe: pd.DataFrame,
    hedge_path: Path,
    panel_path: Path,
) -> pd.DataFrame:
    hedges = pd.read_csv(hedge_path)
    panel = pd.read_parquet(panel_path)

    expected = universe["ticker"].astype(str).str.upper().tolist()
    expected_hedges = dict(zip(hedges["ticker"], hedges["sector_ticker"], strict=True))
    missing_columns = REQUIRED_COLUMNS.difference(panel.columns)
    if missing_columns:
        raise ValueError(f"{panel_path} missing columns: {sorted(missing_columns)}")

    panel["ticker"] = panel["ticker"].astype(str).str.upper()
    missing_tickers = sorted(set(expected).difference(panel["ticker"].unique()))
    if missing_tickers:
        raise ValueError(f"{panel_path} missing agriculture tickers: {missing_tickers}")

    latest = panel.groupby("ticker", observed=True)["date"].max()
    mappings = (
        panel.loc[panel["ticker"].isin(expected), ["ticker", "market_ticker", "sector_ticker"]]
        .drop_duplicates()
        .sort_values("ticker")
    )
    if mappings.groupby("ticker").size().max() != 1:
        raise ValueError("Agriculture ticker hedge mapping changes unexpectedly inside the panel")
    actual_hedges = mappings.set_index("ticker")["sector_ticker"].to_dict()
    bad = {
        ticker: (actual_hedges.get(ticker), expected_hedges[ticker])
        for ticker in expected
        if actual_hedges.get(ticker) != expected_hedges[ticker]
    }
    if bad:
        raise ValueError(f"Agriculture sector hedge mismatches: {bad}")
    if set(mappings["market_ticker"]) != {"SPY"}:
        raise ValueError(f"Expected SPY market hedge, got {sorted(mappings['market_ticker'].unique())}")

    print(f"Agriculture {label} beta panel verified: rows={len(panel):,}, tickers={len(expected)}")
    print(mappings.to_string(index=False))
    print("Latest stock dates:")
    print(latest.reindex(expected).to_string())
    return panel


def main() -> None:
    universe = pd.read_csv(UNIVERSE_PATH)
    panels = {
        label: verify_panel(label, universe, hedge_path, panel_path)
        for label, (hedge_path, panel_path) in PANEL_CONFIGS.items()
    }

    identity = ["ticker", "date"]
    comparison_columns = ["raw_return", "residual_return_mkt_w12m"]
    sector_source = panels["sector"].sort_values(identity).reset_index(drop=True)
    liquid_source = panels["liquid_sector"].sort_values(identity).reset_index(drop=True)
    sector = sector_source[identity + comparison_columns]
    liquid = liquid_source[identity + comparison_columns]
    if not sector[identity].equals(liquid[identity]):
        raise ValueError("Sector and liquid-sector panels do not have identical ticker/date rows")
    for column in comparison_columns:
        left = pd.to_numeric(sector[column], errors="coerce")
        right = pd.to_numeric(liquid[column], errors="coerce")
        if not left.equals(right):
            raise ValueError(f"{column} differs between sector and liquid-sector panels")
    print("Shared raw and SPY-only return layers are identical across both panels.")

    combined = pd.read_parquet(COMBINED_PATH).sort_values(identity).reset_index(drop=True)
    required_combined = {
        "sector_ticker",
        "sector_ticker_narrow",
        "sector_ticker_liquid",
        "residual_return_mkt_w12m",
        "residual_return_mktsec_w12m",
        "residual_return_mktsec_narrow_w12m",
        "residual_return_mktsec_liquid_w12m",
    }
    missing = required_combined.difference(combined.columns)
    if missing:
        raise ValueError(f"{COMBINED_PATH} missing columns: {sorted(missing)}")
    if not combined[identity].equals(sector[identity]):
        raise ValueError("Combined Agriculture panel has different ticker/date rows")
    if not combined["sector_ticker"].equals(combined["sector_ticker_narrow"]):
        raise ValueError("sector_ticker must be the exact narrow-sector alias")
    if not combined["sector_ticker_narrow"].equals(
        sector_source["sector_ticker"]
    ):
        raise ValueError("Combined narrow-sector mapping differs from its source panel")
    if not combined["sector_ticker_liquid"].equals(
        liquid_source["sector_ticker"]
    ):
        raise ValueError("Combined liquid-sector mapping differs from its source panel")

    return_aliases = {
        "residual_return_mktsec_w12m": sector_source["residual_return_mktsec_w12m"],
        "residual_return_mktsec_narrow_w12m": sector_source[
            "residual_return_mktsec_w12m"
        ],
        "residual_return_mktsec_liquid_w12m": liquid_source[
            "residual_return_mktsec_w12m"
        ],
    }
    for column, expected in return_aliases.items():
        if not pd.to_numeric(combined[column], errors="coerce").equals(
            pd.to_numeric(expected, errors="coerce")
        ):
            raise ValueError(f"Combined Agriculture {column} differs from its source")
    print(
        "Combined Agriculture panel verified: residual_return_mktsec_w12m is the "
        "narrow alias; narrow and liquid alternatives are explicit."
    )


if __name__ == "__main__":
    main()
