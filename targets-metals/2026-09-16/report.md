# Metals Daily Targets: 2026-09-16

- Signal as-of date: 2026-09-15
- Target trading date: 2026-09-16
- AUM: $5,000.00
- Gross stock weight: 39.00%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: 39.00%
- Gross hedge weight: 39.39%
- Total net weight after hedges: -0.39%
- Turnover from Metals-attributed current positions: 12.72%
- Full eligible order turnover: 8.54%
- Today's total child-order turnover: 10.77%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $1.35

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
| total_hedge | 0.3939 | -0.3939 | 1969.5 | -1969.5 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | sco_vol_gc_hg_accel_miners\|miners | BHP | 0.12 | 7.1 | 84.77 | 0.6 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.38214;q_long_exit=2.176;q_short_entry=2.176;q_short_exit=1.41943;vol_diff=-0.148571;accel=-0.23783; aggregate BHP capped at 12.0%\|persistent_binary active; feature=-0.0232328; aggregate BHP capped at 12.0% |
| stock | miners | FSUGY | 0.05 | 10.8 | 23.22 | 0.6 | 0.3 | persistent_binary active; feature=-0.0232328 |
| stock | sco_vol_gc_hg_accel_miners\|miners | RIO | 0.12 | 6.2 | 97.26 | 0.3 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.38214;q_long_exit=2.176;q_short_entry=2.176;q_short_exit=1.41943;vol_diff=-0.148571;accel=-0.23783; aggregate RIO capped at 12.0%\|persistent_binary active; feature=-0.0232328; aggregate RIO capped at 12.0% |
| stock | sco_vol_gc_hg_accel_miners\|copper_miner\|miners | SCCO | 0.05 | 1.3 | 189.39 | 0.7 | 0.9 | sco_vol_gc_hg_combo active; sco_vol=1.38214;q_long_exit=2.176;q_short_entry=2.176;q_short_exit=1.41943;vol_diff=-0.148571;accel=-0.23783\|copper_energy_terms_of_trade active; hg_cl_ratio=0.762454;ho_ret=0.0521761;hg_mv_5=0.79221;hg_mv_200=0.848063;hg_mv_diff=-0.0558523;hg_threshold=0.00741782;ho_momentum_20d=0.190423;ho_threshold=0.0298888\|persistent_binary active; feature=-0.0232328 |
| stock | sco_vol_gc_hg_accel_miners\|miners | VALE | 0.05 | 17.3 | 14.47 | 0.2 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.38214;q_long_exit=2.176;q_short_entry=2.176;q_short_exit=1.41943;vol_diff=-0.148571;accel=-0.23783\|persistent_binary active; feature=-0.0232328 |
| hedge | hedge | SPY | -0.187562 | -1.2 | 757.39 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | -0.206338 | -9.4 | 109.44 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | sco_vol_gc_hg_accel_miners\|copper_miner\|miners | SCCO | SELL | -1 | -1 | -0.037878 | False | 189.39 | 188.92 | 189.86 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners\|miners | VALE | SELL | -9 | -9 | -0.026046 | False | 14.47 | 14.43 | 14.51 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XME | BUY | 2 | 2 | 0.043776 | False | 109.44 | 109.17 | 109.71 | single aggregate hedge order after confirming stock fills |
