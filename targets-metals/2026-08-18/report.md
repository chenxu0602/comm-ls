# Metals Daily Targets: 2026-08-18

- Signal as-of date: 2026-08-17
- Target trading date: 2026-08-18
- AUM: $10,000.00
- Gross stock weight: 48.18%
- Single-name cap after sleeve aggregation: 10.00%
- Net stock weight: 40.00%
- Gross hedge weight: 48.45%
- Total net weight after hedges: -8.45%
- Turnover from Metals-attributed current positions: 96.63%
- Full eligible order turnover: 96.63%
- Today's child-order turnover: 38.99%
- Daily turnover cap: 40.00%
- Estimated execution cost: $9.75

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
| total_hedge | 0.484479 | -0.484479 | 4844.79 | -4844.79 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | sco_specialty_alloys | ATI | 0.08 | 3.5 | 230.41 | 1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-2.01158;drawdown_63d=-1.39133;realized_vol_63d=-0.617969 |
| stock | sco_vol_gc_hg_accel_miners|miners | BHP | 0.064091 | 7.3 | 88.05 | 0.6 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.266;q_short_entry=2.266;q_short_exit=1.45357;vol_diff=-0.310714;accel=1.44511|persistent_binary active; feature=-0.0166219 |
| stock | sco_specialty_alloys | CRS | 0.08 | 1.5 | 543.16 | 1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-2.01158;drawdown_63d=-1.39133;realized_vol_63d=-0.617969 |
| stock | miners | FSUGY | -0.040909 | -16.3 | 25.04 | 0.7 | 0.3 | persistent_binary active; feature=-0.0166219 |
| stock | sco_specialty_alloys | HWM | 0.04 | 1.4 | 289.25 | 0.8 | 0.1 | sco_specialty_alloys_hysteresis active; ret_63d=-2.01158;drawdown_63d=-1.39133;realized_vol_63d=-0.617969 |
| stock | sco_vol_gc_hg_accel_miners|miners | RIO | 0.099091 | 10.3 | 96.42 | 0.3 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.266;q_short_entry=2.266;q_short_exit=1.45357;vol_diff=-0.310714;accel=1.44511|persistent_binary active; feature=-0.0166219 |
| stock | sco_vol_gc_hg_accel_miners|miners | SCCO | 0.056364 | 2.9 | 192.04 | 0.9 | 0.9 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.266;q_short_entry=2.266;q_short_exit=1.45357;vol_diff=-0.310714;accel=1.44511|persistent_binary active; feature=-0.0166219 |
| stock | sco_vol_gc_hg_accel_miners|miners | VALE | 0.021364 | 15.6 | 13.68 | 0.3 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.266;q_short_entry=2.266;q_short_exit=1.45357;vol_diff=-0.310714;accel=1.44511|persistent_binary active; feature=-0.0166219 |
| hedge | hedge | SPY | -0.298827 | -3.9 | 775.16 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | -0.185651 | -15.8 | 117.21 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | miners | FSUGY | SELL | -16 | -7 | -0.01753 | False | 25.04 | 24.98 | 25.11 | execute once; no same-day reversal or duplicate order |
| stock | sco_specialty_alloys | ATI | BUY | 3 | 1 | 0.023041 | False | 230.41 | 229.84 | 230.99 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners|miners | BHP | BUY | 7 | 4 | 0.03522 | False | 88.05 | 87.83 | 88.27 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners|miners | RIO | BUY | 10 | 5 | 0.048208 | False | 96.42 | 96.18 | 96.66 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners|miners | SCCO | BUY | 3 | 1 | 0.019204 | False | 192.04 | 191.56 | 192.52 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners|miners | VALE | BUY | 16 | 7 | 0.009576 | False | 13.68 | 13.65 | 13.71 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | SPY | SELL | -4 | -2 | -0.155031 | False | 775.16 | 773.22 | 777.09 | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XME | SELL | -16 | -7 | -0.082045 | False | 117.21 | 116.91 | 117.5 | single aggregate hedge order after confirming stock fills |
