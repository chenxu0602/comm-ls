# Combined CL v4.3 (notebook cached beta) + Metals + Agriculture targets: 2026-10-08

- Combined AUM: $22,000.00
- Total child turnover: 21.87% ($4,811.41)
- Stock child turnover (40% cap applies): 4.96%
- Hedge child turnover (uncapped): 16.91%
- Orders: 7
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Strategy changes and allocation notes

- Agriculture v4.3 joined the main account effective 2026-10-02: $2,000 allocated AUM. Idle allocation remains cash and still counts in account AUM.
- Agriculture uses component-specific hedges: crush_vol/crush_vol2/adm_bg2 use SPY + MOO; adm_bg/adm_tsn/bg_tsn use SPY only. Keep its virtual book separate.
- Agriculture stock target state for this package: flat. This is not a permanent suspension.
- CRO (crack refiner-only) added effective 2026-10-06: 10% allocation from unused CL capacity. CL AUM remains $15,000; existing sleeve weights are NOT reduced or renormalized.
- CRO stocks: VLO/MPC/PSX = 30/40/30%; crack_03; signal lookback 30 sessions; volatility lookback 30 (minimum 20); no signal smoothing; balance=0.5 (maximum CRO stock gross 5% of CL AUM).
- CRO explicit hedge is SPY ONLY, not XLE. Preserve component hedge ownership when PSX overlaps existing sleeves; net single-name cap and execution constraints still apply.
- This addition is refiner-only CRO, NOT the refiner-producer CRP, refiner-VLCC CRV, or refiner-chemical CRC research strategies.
- CRO stock target state for this package: active. Flat CRO must not create reallocation trades under identical inputs.
- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.
- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.
- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | SPY | 8 | 28.26% | 4 | 4 | 8 | 0 | 777.22 |
| hedge | XLE | 19 | 5.47% | 27 | -8 | 19 | 0 | 63.36 |
| hedge | XME | 2 | 0.95% | 3 | -1 | 2 | 0 | 104.84 |
| stock | AVNT | -5 | -0.93% | -5 | 0 | -5 | 0 | 41.00 |
| stock | BHP | -7 | -2.71% | -7 | 0 | -7 | 0 | 85.22 |
| stock | CE | -10 | -1.99% | -9 | 0 | -9 | -1 | 43.86 |
| stock | DINO | 3 | 1.58% | 3 | 0 | 3 | 0 | 115.63 |
| stock | DK | 10 | 3.43% | 10 | 0 | 10 | 0 | 75.46 |
| stock | DOW | -27 | -3.41% | -27 | 0 | -27 | 0 | 27.77 |
| stock | EMN | -7 | -2.01% | -6 | -1 | -7 | 0 | 63.25 |
| stock | ERO | 18 | 3.01% | 18 | 0 | 18 | 0 | 36.78 |
| stock | FSUGY | -16 | -1.61% | -15 | -1 | -16 | 0 | 22.16 |
| stock | FTI | -4 | -1.24% | -4 | 0 | -4 | 0 | 68.40 |
| stock | HAL | -5 | -0.72% | -4 | 0 | -4 | -1 | 31.75 |
| stock | HUN | -49 | -1.92% | -47 | 0 | -47 | -2 | 8.63 |
| stock | LYB | -13 | -3.46% | -13 | 0 | -13 | 0 | 58.49 |
| stock | MPC | 1 | 2.01% | 1 | 0 | 1 | 0 | 442.26 |
| stock | PBF | 5 | 1.90% | 5 | 0 | 5 | 0 | 83.68 |
| stock | PSX | 3 | 3.70% | 0 | 3 | 3 | 0 | 271.62 |
| stock | RIO | -6 | -2.54% | -6 | 0 | -6 | 0 | 93.16 |
| stock | SCCO | -2 | -1.82% | -2 | 0 | -2 | 0 | 200.57 |
| stock | SLB | -6 | -1.31% | -6 | 0 | -6 | 0 | 47.96 |
| stock | TECK | 3 | 0.89% | 3 | 0 | 3 | 0 | 65.39 |
| stock | VALE | -24 | -1.48% | -9.8 | -14 | -23.8 | -0.2 | 13.61 |
| stock | VLO | 1 | 1.93% | 1 | 0 | 1 | 0 | 424.10 |
| stock | WLK | -12 | -3.36% | -12 | 0 | -12 | 0 | 61.52 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| EMN | SELL | -1.0 | -6.0 | -7.0 | 63.41 | 63.09 | 1 |
| FSUGY | SELL | -1.0 | -15.0 | -16.0 | 22.22 | 22.1 | 1 |
| PSX | BUY | 3.0 | 0.0 | 3.0 | 270.94 | 272.3 | 1 |
| VALE | SELL | -14.0 | -9.8 | -23.8 | 13.64 | 13.58 | 1 |
| SPY | BUY | 4.0 | 4.0 | 8.0 | 775.28 | 779.16 | 2 |
| XLE | SELL | -8.0 | 27.0 | 19.0 | 63.52 | 63.2 | 2 |
| XME | SELL | -1.0 | 3.0 | 2.0 | 105.1 | 104.58 | 2 |

## Main-account beta algorithm change

CL and Metals use `notebook_residual_cached_beta_v1`, shared with the new explicit backtest. Agriculture already reads its sleeve-specific processed beta. CL/Metals/Crypto legacy packages and algorithms remain available for comparison. New ETF orders may include beta-method migration turnover.

### CL

## Beta algorithm change: notebook residual cached beta

- beta_mode: `notebook_residual_cached_beta_v1`. Source: `data/processed/equity_processed.parquet`.
- Uses the already-computed beta for each notebook residual: `market_beta_mktsec_w12m` / `sector_beta_mktsec_w12m`, or `market_beta_mkt_w12m` for SPY-only sleeves.
- Source pipeline default: 12-month weekly returns, exponential weighting (3-month half-life), monthly updates. No new daily 252-session regression.
- CL CRO and Crypto use SPY only; other CL sleeves and Metals keep their existing residual-specific sector mapping. Shared core: `comm_ls.residual_beta_hedge`, also used by the new explicit backtest.
- Exact beta values, source dates and estimation cutoffs are in `beta_sources.csv`. Only observations known by the signal as-of are used.
- The beta change can produce ETF migration orders even when the stock signal is unchanged. Compare with the legacy package before execution.
- Prices, integer rounding, caps, trade buffers and intraday fills can still differ from implicit research PnL. At monthly beta updates the prior-close explicit hedge and the return-day residual beta can differ by one session; the new audit reports that timing gap separately.

### Metals

## Beta algorithm change: notebook residual cached beta

- beta_mode: `notebook_residual_cached_beta_v1`. Source: `data/processed/equity_processed.parquet`.
- Uses the already-computed beta for each notebook residual: `market_beta_mktsec_w12m` / `sector_beta_mktsec_w12m`, or `market_beta_mkt_w12m` for SPY-only sleeves.
- Source pipeline default: 12-month weekly returns, exponential weighting (3-month half-life), monthly updates. No new daily 252-session regression.
- CL CRO and Crypto use SPY only; other CL sleeves and Metals keep their existing residual-specific sector mapping. Shared core: `comm_ls.residual_beta_hedge`, also used by the new explicit backtest.
- Exact beta values, source dates and estimation cutoffs are in `beta_sources.csv`. Only observations known by the signal as-of are used.
- The beta change can produce ETF migration orders even when the stock signal is unchanged. Compare with the legacy package before execution.
- Prices, integer rounding, caps, trade buffers and intraday fills can still differ from implicit research PnL. At monthly beta updates the prior-close explicit hedge and the return-day residual beta can differ by one session; the new audit reports that timing gap separately.

