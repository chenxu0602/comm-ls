# Metals Daily Targets: 2026-08-17

- Signal as-of date: 2026-08-14
- Target trading date: 2026-08-17
- AUM: $10,000.00
- Gross stock weight: 48.18%
- Single-name cap after sleeve aggregation: 10.00%
- Net stock weight: 40.00%
- Gross hedge weight: 48.49%
- Total net weight after hedges: -8.49%
- Turnover from Metals-attributed current positions: 96.67%
- Full eligible order turnover: 96.67%
- Today's child-order turnover: 39.27%
- Daily turnover cap: 40.00%
- Estimated execution cost: $9.82

## Isolation and Execution Notes

- Signal construction is fail-closed on the `_2` cache/carry pipeline; it does not read the current non-`_2` signal cache.
- Required feature observations must be no more than 3 calendar days old.
- Current positions must be Metals-attributed, not a full shared IB account export.
- Execute stock orders once in the first 30 minutes; aggregate SPY/XME hedge orders only after confirming stock fills.
- Direct same-day reversals are flattened first by the child-order policy.

## Pinned Signal Inputs

- metals_cache: `data/cache/feature_return/METALS-multi_return_2.parquet`; latest n/a
- gc_cache: `data/cache/feature_return/GC-multi_return_2.parquet`; latest n/a
- sco_cache: `data/cache/feature_return/SCO-multi_return_2.parquet`; latest n/a
- carry_dir: `data/comm/carry_data_2`; latest n/a
- commodity_dir: `data/comm`; latest n/a

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.440909 | 0.440909 | 4409.09 | 4409.09 | 7 |
| stock_short_without_hedge | 0.040909 | -0.040909 | 409.09 | -409.09 | 1 |
| total_hedge | 0.48488 | -0.48488 | 4848.8 | -4848.8 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | sco_specialty_alloys | ATI | 0.08 | 3.5 | 228.48 | 1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-2.0867;drawdown_63d=-1.51193;realized_vol_63d=-0.623795 |
| stock | sco_vol_gc_hg_accel_miners|miners | BHP | 0.064091 | 7.4 | 86.78 | 0.6 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.266;q_short_entry=2.266;q_short_exit=1.45357;vol_diff=-0.310714;accel=1.031|persistent_binary active; feature=-0.0152341 |
| stock | sco_specialty_alloys | CRS | 0.08 | 1.5 | 544.59 | 1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-2.0867;drawdown_63d=-1.51193;realized_vol_63d=-0.623795 |
| stock | miners | FSUGY | -0.040909 | -16.5 | 24.85 | 0.7 | 0.3 | persistent_binary active; feature=-0.0152341 |
| stock | sco_specialty_alloys | HWM | 0.04 | 1.4 | 289.18 | 0.8 | 0.1 | sco_specialty_alloys_hysteresis active; ret_63d=-2.0867;drawdown_63d=-1.51193;realized_vol_63d=-0.623795 |
| stock | sco_vol_gc_hg_accel_miners|miners | RIO | 0.099091 | 10.4 | 95.68 | 0.3 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.266;q_short_entry=2.266;q_short_exit=1.45357;vol_diff=-0.310714;accel=1.031|persistent_binary active; feature=-0.0152341 |
| stock | sco_vol_gc_hg_accel_miners|miners | SCCO | 0.056364 | 3.1 | 184.61 | 0.9 | 0.9 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.266;q_short_entry=2.266;q_short_exit=1.45357;vol_diff=-0.310714;accel=1.031|persistent_binary active; feature=-0.0152341 |
| stock | sco_vol_gc_hg_accel_miners|miners | VALE | 0.021364 | 15.7 | 13.63 | 0.3 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.266;q_short_entry=2.266;q_short_exit=1.45357;vol_diff=-0.310714;accel=1.031|persistent_binary active; feature=-0.0152341 |
| hedge | hedge | SPY | -0.2988 | -3.8 | 776.34 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | -0.18608 | -15.9 | 117.14 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | miners | FSUGY | SELL | -16 | -7 | -0.017395 | False | 24.85 | 24.79 | 24.91 | execute once; no same-day reversal or duplicate order |
| stock | sco_specialty_alloys | ATI | BUY | 4 | 2 | 0.045696 | False | 228.48 | 227.91 | 229.05 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners|miners | BHP | BUY | 7 | 3 | 0.026034 | False | 86.78 | 86.56 | 87 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners|miners | RIO | BUY | 10 | 4 | 0.038272 | False | 95.68 | 95.44 | 95.92 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners|miners | SCCO | BUY | 3 | 1 | 0.018461 | False | 184.61 | 184.15 | 185.07 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners|miners | VALE | BUY | 16 | 7 | 0.009541 | False | 13.63 | 13.6 | 13.66 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | SPY | SELL | -4 | -2 | -0.155268 | False | 776.34 | 774.4 | 778.28 | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XME | SELL | -16 | -7 | -0.081998 | False | 117.14 | 116.85 | 117.43 | single aggregate hedge order after confirming stock fills |
