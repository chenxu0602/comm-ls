# Metals Daily Targets: 2026-08-26

- Signal as-of date: 2026-08-25
- Target trading date: 2026-08-26
- AUM: $5,000.00
- Gross stock weight: 58.00%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: 58.00%
- Gross hedge weight: 66.31%
- Total net weight after hedges: -8.31%
- Turnover from Metals-attributed current positions: 16.13%
- Full eligible order turnover: 1.64%
- Today's total child-order turnover: 2.42%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $0.30

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
| stock_long_without_hedge | 0.58 | 0.58 | 2900 | 2900 | 8 |
| stock_short_without_hedge | 0 | 0 | 0 | 0 | 0 |
| total_hedge | 0.663085 | -0.663085 | 3315.42 | -3315.42 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | sco_specialty_alloys | ATI | 0.04 | 0.9 | 215.23 | 1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-1.33134;drawdown_63d=-0.524735;realized_vol_63d=-0.502412 |
| stock | sco_vol_gc_hg_accel_miners|sco_vol_miners|miners | BHP | 0.12 | 6.1 | 98.69 | 0.6 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.22529;q_short_entry=2.22529;q_short_exit=1.43357;vol_diff=0.0228572;accel=1.4866; aggregate BHP capped at 12.0%|sco_vol_regime_pulse active; sco_vol=0.0107118;vol_quantile=0.0120845;vol_diff=0.00251208; aggregate BHP capped at 12.0%|persistent_binary active; feature=-0.0606331; aggregate BHP capped at 12.0% |
| stock | sco_specialty_alloys | CRS | 0.04 | 0.4 | 486.09 | 1.1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-1.33134;drawdown_63d=-0.524735;realized_vol_63d=-0.502412 |
| stock | miners | FSUGY | 0.05 | 9.8 | 25.49 | 0.7 | 0.3 | persistent_binary active; feature=-0.0606331 |
| stock | sco_specialty_alloys | HWM | 0.02 | 0.4 | 264.04 | 0.9 | 0.1 | sco_specialty_alloys_hysteresis active; ret_63d=-1.33134;drawdown_63d=-0.524735;realized_vol_63d=-0.502412 |
| stock | sco_vol_gc_hg_accel_miners|sco_vol_miners|miners | RIO | 0.12 | 5.6 | 106.81 | 0.3 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.22529;q_short_entry=2.22529;q_short_exit=1.43357;vol_diff=0.0228572;accel=1.4866; aggregate RIO capped at 12.0%|sco_vol_regime_pulse active; sco_vol=0.0107118;vol_quantile=0.0120845;vol_diff=0.00251208; aggregate RIO capped at 12.0%|persistent_binary active; feature=-0.0606331; aggregate RIO capped at 12.0% |
| stock | sco_vol_gc_hg_accel_miners|sco_vol_miners|miners | SCCO | 0.12 | 2.7 | 219.7 | 0.8 | 0.9 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.22529;q_short_entry=2.22529;q_short_exit=1.43357;vol_diff=0.0228572;accel=1.4866|sco_vol_regime_pulse active; sco_vol=0.0107118;vol_quantile=0.0120845;vol_diff=0.00251208|persistent_binary active; feature=-0.0606331 |
| stock | sco_vol_gc_hg_accel_miners|sco_vol_miners|miners | VALE | 0.07 | 22.8 | 15.33 | 0.3 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.22529;q_short_entry=2.22529;q_short_exit=1.43357;vol_diff=0.0228572;accel=1.4866|sco_vol_regime_pulse active; sco_vol=0.0107118;vol_quantile=0.0120845;vol_diff=0.00251208|persistent_binary active; feature=-0.0606331 |
| hedge | hedge | SPY | -0.365079 | -2.4 | 765.91 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | -0.298006 | -12.3 | 120.94 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | hedge | XME | BUY | 1 | 1 | 0.024188 | False | 120.94 | 120.64 | 121.24 | single aggregate hedge order after confirming stock fills |
