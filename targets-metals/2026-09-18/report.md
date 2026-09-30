# Metals Daily Targets: 2026-09-18

- Signal as-of date: 2026-09-17
- Target trading date: 2026-09-18
- AUM: $5,000.00
- Gross stock weight: 39.00%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: 39.00%
- Gross hedge weight: 39.65%
- Total net weight after hedges: -0.65%
- Turnover from Metals-attributed current positions: 14.99%
- Full eligible order turnover: 13.11%
- Today's total child-order turnover: 17.48%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $2.18

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
| stock_long_without_hedge | 0.39 | 0.39 | 1950 | 1950 | 5 |
| stock_short_without_hedge | 0 | 0 | 0 | 0 | 0 |
| total_hedge | 0.396536 | -0.396536 | 1982.68 | -1982.68 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | sco_vol_gc_hg_accel_miners\|miners | BHP | 0.12 | 6.9 | 86.56 | 0.6 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.34286;q_long_exit=2.17143;q_short_entry=2.17143;q_short_exit=1.41586;vol_diff=-0.0735714;accel=-0.105792; aggregate BHP capped at 12.0%\|persistent_binary active; feature=-0.0144259; aggregate BHP capped at 12.0% |
| stock | miners | FSUGY | 0.05 | 10.5 | 23.81 | 0.6 | 0.3 | persistent_binary active; feature=-0.0144259 |
| stock | sco_vol_gc_hg_accel_miners\|miners | RIO | 0.12 | 6.1 | 98.04 | 0.3 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.34286;q_long_exit=2.17143;q_short_entry=2.17143;q_short_exit=1.41586;vol_diff=-0.0735714;accel=-0.105792; aggregate RIO capped at 12.0%\|persistent_binary active; feature=-0.0144259; aggregate RIO capped at 12.0% |
| stock | sco_vol_gc_hg_accel_miners\|copper_miner\|miners | SCCO | 0.05 | 1.3 | 196.11 | 0.7 | 0.9 | sco_vol_gc_hg_combo active; sco_vol=1.34286;q_long_exit=2.17143;q_short_entry=2.17143;q_short_exit=1.41586;vol_diff=-0.0735714;accel=-0.105792\|copper_energy_terms_of_trade active; hg_cl_ratio=0.80095;ho_ret=-0.0225101;hg_mv_5=0.783127;hg_mv_200=0.846985;hg_mv_diff=-0.0638585;hg_threshold=0.00772558;ho_momentum_20d=0.162382;ho_threshold=0.0300924\|persistent_binary active; feature=-0.0144259 |
| stock | sco_vol_gc_hg_accel_miners\|miners | VALE | 0.05 | 17.3 | 14.47 | 0.2 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.34286;q_long_exit=2.17143;q_short_entry=2.17143;q_short_exit=1.41586;vol_diff=-0.0735714;accel=-0.105792\|persistent_binary active; feature=-0.0144259 |
| hedge | hedge | SPY | -0.18957 | -1.2 | 762.6 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | -0.206966 | -9.3 | 111.32 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | hedge | SPY | BUY | 1 | 1 | 0.15252 | False | 762.6 | 760.69 | 764.51 | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XME | BUY | 1 | 1 | 0.022264 | False | 111.32 | 111.04 | 111.6 | single aggregate hedge order after confirming stock fills |
