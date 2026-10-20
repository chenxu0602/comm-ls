# Metals Daily Targets: 2026-10-08

- Signal as-of date: 2026-10-07
- Target trading date: 2026-10-08
- AUM: $5,000.00
- Gross stock weight: 46.50%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: -46.50%
- Gross hedge weight: 30.68%
- Total net weight after hedges: -15.82%
- Turnover from Metals-attributed current positions: 20.11%
- Full eligible order turnover: 17.88%
- Today's total child-order turnover: 21.90%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $2.74

## Isolation and Execution Notes

- Signal construction is fail-closed on the `_2` cache/carry pipeline; it does not read the current non-`_2` signal cache.
- Required feature observations must be no more than 3 calendar days old.
- Current positions must be Metals-attributed, not a full shared IB account export.
- Execute stock orders once in the first 30 minutes; aggregate SPY/XME hedge orders only after confirming stock fills.
- Direct same-day reversals are flattened first by the child-order policy.

## Pinned Signal Inputs

- metals_cache: `data/cache/feature_return_observation_v1/METALS-multi_return_2.parquet`; latest n/a
- gc_cache: `data/cache/feature_return_observation_v1/GC-multi_return_2.parquet`; latest n/a
- sco_cache: `data/cache/feature_return_observation_v1/SCO-multi_return_2.parquet`; latest n/a
- carry_dir: `data/comm/carry_data_2`; latest n/a
- commodity_dir: `data/comm`; latest n/a

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0 | 0 | 0 | 0 | 0 |
| stock_short_without_hedge | 0.465 | -0.465 | 2325 | -2325 | 5 |
| total_hedge | 0.306812 | 0.306812 | 1534.06 | 1534.06 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | hg_gc_gap_gc_carry_iron\|miners | BHP | -0.12 | -7 | 85.22 | 0.1 | 0.6 | dual_feature_hysteresis active; hg_gap=0.0485523;gc_carry=1.06425; aggregate BHP capped at 12.0%\|persistent_binary active; feature=0.0485523; aggregate BHP capped at 12.0% |
| stock | hg_gc_gap_gc_carry_iron\|miners | FSUGY | -0.07 | -15.8 | 22.16 | 0.3 | 0.3 | dual_feature_hysteresis active; hg_gap=0.0485523;gc_carry=1.06425\|persistent_binary active; feature=0.0485523 |
| stock | hg_gc_gap_gc_carry_iron\|miners | RIO | -0.11 | -5.9 | 93.16 | -0.1 | 0.5 | dual_feature_hysteresis active; hg_gap=0.0485523;gc_carry=1.06425\|persistent_binary active; feature=0.0485523 |
| stock | copper_miner\|miners | SCCO | -0.1 | -2.5 | 200.57 | 0.5 | 0.8 | copper_energy_terms_of_trade active; hg_cl_ratio=0.781559;ho_ret=0.011597;hg_mv_5=0.777866;hg_mv_200=0.831623;hg_mv_diff=-0.0537569;hg_threshold=0.00968381;ho_momentum_20d=0.00489403;ho_threshold=0.0261841\|persistent_binary active; feature=0.0485523 |
| stock | hg_gc_gap_gc_carry_iron\|miners | VALE | -0.065 | -23.9 | 13.61 | -0.4 | 0.4 | dual_feature_hysteresis active; hg_gap=0.0485523;gc_carry=1.06425\|persistent_binary active; feature=0.0485523 |
| hedge | hedge | SPY | 0.047317 | 0.3 | 777.22 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | 0.259496 | 12.4 | 104.84 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | hg_gc_gap_gc_carry_iron\|miners | FSUGY | SELL | -1 | -1 | -0.004432 | False | 22.16 | 22.1 | 22.22 | execute once; no same-day reversal or duplicate order |
| stock | hg_gc_gap_gc_carry_iron\|miners | VALE | SELL | -14 | -14 | -0.038108 | False | 13.61 | 13.58 | 13.64 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | SPY | SELL | -1 | -1 | -0.155444 | False | 777.22 | 775.28 | 779.16 | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XME | BUY | 1 | 1 | 0.020968 | False | 104.84 | 104.58 | 105.1 | single aggregate hedge order after confirming stock fills |

## Beta algorithm change: notebook residual cached beta

- beta_mode: `notebook_residual_cached_beta_v1`. Source: `data/processed/equity_processed.parquet`.
- Uses the already-computed beta for each notebook residual: `market_beta_mktsec_w12m` / `sector_beta_mktsec_w12m`, or `market_beta_mkt_w12m` for SPY-only sleeves.
- Source pipeline default: 12-month weekly returns, exponential weighting (3-month half-life), monthly updates. No new daily 252-session regression.
- CL CRO and Crypto use SPY only; other CL sleeves and Metals keep their existing residual-specific sector mapping. Shared core: `comm_ls.residual_beta_hedge`, also used by the new explicit backtest.
- Exact beta values, source dates and estimation cutoffs are in `beta_sources.csv`. Only observations known by the signal as-of are used.
- The beta change can produce ETF migration orders even when the stock signal is unchanged. Compare with the legacy package before execution.
- Prices, integer rounding, caps, trade buffers and intraday fills can still differ from implicit research PnL. At monthly beta updates the prior-close explicit hedge and the return-day residual beta can differ by one session; the new audit reports that timing gap separately.
