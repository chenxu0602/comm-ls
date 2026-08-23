# Metals Daily Targets: 2026-08-21

- Signal as-of date: 2026-08-20
- Target trading date: 2026-08-21
- AUM: $5,000.00
- Gross stock weight: 57.32%
- Single-name cap after sleeve aggregation: 10.00%
- Net stock weight: 57.32%
- Gross hedge weight: 66.33%
- Total net weight after hedges: -9.02%
- Turnover from Metals-attributed current positions: 123.65%
- Full eligible order turnover: 123.65%
- Today's child-order turnover: 39.32%
- Daily turnover cap: 40.00%
- Estimated execution cost: $4.92

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
| stock_long_without_hedge | 0.573182 | 0.573182 | 2865.91 | 2865.91 | 8 |
| stock_short_without_hedge | 0 | 0 | 0 | 0 | 0 |
| total_hedge | 0.663341 | -0.663341 | 3316.71 | -3316.71 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | sco_specialty_alloys | ATI | 0.08 | 1.9 | 209.22 | 1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-1.69298;drawdown_63d=-1.14922;realized_vol_63d=-0.651494 |
| stock | sco_vol_gc_hg_accel_miners|miners | BHP | 0.1 | 5.3 | 93.63 | 0.6 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.24957;q_short_entry=2.24957;q_short_exit=1.44343;vol_diff=-0.16;accel=2.84809; aggregate BHP capped at 10.0%|persistent_binary active; feature=-0.0349941; aggregate BHP capped at 10.0% |
| stock | sco_specialty_alloys | CRS | 0.08 | 0.8 | 489.08 | 1.1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-1.69298;drawdown_63d=-1.14922;realized_vol_63d=-0.651494 |
| stock | miners | FSUGY | 0.040909 | 8 | 25.53 | 0.6 | 0.3 | persistent_binary active; feature=-0.0349941 |
| stock | sco_specialty_alloys | HWM | 0.04 | 0.7 | 273.64 | 0.9 | 0.1 | sco_specialty_alloys_hysteresis active; ret_63d=-1.69298;drawdown_63d=-1.14922;realized_vol_63d=-0.651494 |
| stock | sco_vol_gc_hg_accel_miners|miners | RIO | 0.1 | 4.9 | 102.17 | 0.3 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.24957;q_short_entry=2.24957;q_short_exit=1.44343;vol_diff=-0.16;accel=2.84809; aggregate RIO capped at 10.0%|persistent_binary active; feature=-0.0349941; aggregate RIO capped at 10.0% |
| stock | sco_vol_gc_hg_accel_miners|miners | SCCO | 0.083636 | 2.1 | 198.73 | 0.8 | 0.9 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.24957;q_short_entry=2.24957;q_short_exit=1.44343;vol_diff=-0.16;accel=2.84809|persistent_binary active; feature=-0.0349941 |
| stock | sco_vol_gc_hg_accel_miners|miners | VALE | 0.048636 | 17.1 | 14.23 | 0.3 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.24957;q_short_entry=2.24957;q_short_exit=1.44343;vol_diff=-0.16;accel=2.84809|persistent_binary active; feature=-0.0349941 |
| hedge | hedge | SPY | -0.404378 | -2.7 | 762.6 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | -0.258963 | -11.3 | 114.7 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | miners | FSUGY | BUY | 8 | 3 | 0.015318 | False | 25.53 | 25.47 | 25.59 | execute once; no same-day reversal or duplicate order |
| stock | sco_specialty_alloys | ATI | BUY | 2 | 1 | 0.041844 | False | 209.22 | 208.7 | 209.74 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners|miners | BHP | BUY | 5 | 2 | 0.037452 | False | 93.63 | 93.4 | 93.86 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners|miners | RIO | BUY | 5 | 1 | 0.020434 | False | 102.17 | 101.91 | 102.43 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners|miners | SCCO | BUY | 2 | 1 | 0.039746 | False | 198.73 | 198.23 | 199.23 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners|miners | VALE | BUY | 17 | 6 | 0.017076 | False | 14.23 | 14.19 | 14.27 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | SPY | SELL | -3 | -1 | -0.15252 | False | 762.6 | 760.69 | 764.51 | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XME | SELL | -11 | -3 | -0.06882 | False | 114.7 | 114.41 | 114.99 | single aggregate hedge order after confirming stock fills |
