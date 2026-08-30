#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "[1/6] Download agriculture stocks and narrow SPY/sector hedges"
uv run comm-ls download-equities \
  --universe config/agriculture_equity_beta_universe.csv \
  --theme-hedges config/theme_sector_hedges.csv \
  --ticker-hedges config/agriculture_ticker_sector_hedges.csv \
  --start 2000-01-01

echo "[2/6] Download the additional liquid-sector hedge"
uv run comm-ls download-equities \
  --ticker XLP \
  --start 2000-01-01

echo "[3/6] Build narrow-sector agriculture beta panel"
uv run comm-ls build-equity-processed-dataset \
  --universe config/agriculture_equity_beta_universe.csv \
  --theme-hedges config/theme_sector_hedges.csv \
  --ticker-hedges config/agriculture_ticker_sector_hedges.csv \
  --market-ticker SPY \
  --start 2010-01-01 \
  --skip-commodity-beta-residuals \
  --output data/processed/equity_processed_agriculture_sector.parquet

echo "[4/6] Build liquid-sector agriculture beta panel"
uv run comm-ls build-equity-processed-dataset \
  --universe config/agriculture_equity_beta_universe.csv \
  --theme-hedges config/theme_sector_hedges.csv \
  --ticker-hedges config/agriculture_ticker_liquid_sector_hedges.csv \
  --market-ticker SPY \
  --start 2010-01-01 \
  --skip-commodity-beta-residuals \
  --output data/processed/equity_processed_agriculture_liquid_sector.parquet

echo "[5/6] Build canonical Agriculture panel with explicit hedge alternatives"
uv run python scripts/build_agriculture_equity_beta_panel.py

echo "[6/6] Verify mappings, aliases, and shared SPY-only layer"
uv run python scripts/verify_agriculture_equity_beta_data.py
