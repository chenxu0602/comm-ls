for hedge in xme copx; do
   uv run comm-ls build-equity-processed-dataset \
   --prices-dir data/equity/yfinance \
   --universe config/copper_miners_copx_universe.csv \
   --theme-hedges config/theme_sector_hedges.csv \
   --ticker-hedges "config/copper_miners_${hedge}_hedges.csv" \
   --commodity-signals data/processed/commodity_signals.parquet \
   --exposure-map config/commodity_exposure_map.csv \
   --output "data/processed/equity_processed_copper_miners_${hedge}.parquet" \
   --start 2010-01-01

   uv run comm-ls build-equity-processed-dataset \
   --prices-dir data/equity/yfinance \
   --universe config/diversified_miners_hedge_universe.csv \
   --theme-hedges config/theme_sector_hedges.csv \
   --ticker-hedges "config/diversified_miners_${hedge}_hedges.csv" \
   --commodity-signals data/processed/commodity_signals.parquet \
   --exposure-map config/commodity_exposure_map.csv \
   --output "data/processed/equity_processed_diversified_miners_${hedge}.parquet" \
   --start 2010-01-01

   uv run comm-ls build-daily-feature-return-cache \
   --commodity METALS \
   --commodity-signals data/processed/metals_complex_signals.parquet \
   --beta-returns "data/processed/equity_processed_copper_miners_${hedge}.parquet" \
   --feature-preset metals_complex \
   --return-column raw_return \
   --return-column residual_return_mktsec_w12m \
   --return-column residual_return_mktseccomm_w12m \
   --output "data/cache/feature_return/METALS-copper-miners-${hedge}-multi_return.parquet"

   uv run comm-ls build-daily-feature-return-cache \
   --commodity METALS \
   --commodity-signals data/processed/metals_complex_signals.parquet \
   --beta-returns "data/processed/equity_processed_diversified_miners_${hedge}.parquet" \
   --feature-preset metals_complex \
   --return-column raw_return \
   --return-column residual_return_mktsec_w12m \
   --return-column residual_return_mktseccomm_w12m \
   --output "data/cache/feature_return/METALS-diversified-miners-${hedge}-multi_return.parquet"
done

