# Metals Daily Targets: 2026-08-25

- Signal as-of date: 2026-08-24
- Target trading date: 2026-08-25
- AUM: $5,000.00
- Gross stock weight: 58.00%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: 58.00%
- Gross hedge weight: 66.17%
- Total net weight after hedges: -8.17%
- Turnover from Metals-attributed current positions: 24.80%
- Full eligible order turnover: 10.85%
- Today's total child-order turnover: 11.63%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $1.45

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
| total_hedge | 0.661749 | -0.661749 | 3308.74 | -3308.74 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | sco_specialty_alloys | ATI | 0.04 | 1 | 209.81 | 1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-1.56723;drawdown_63d=-0.941959;realized_vol_63d=-0.863375 |
| stock | sco_vol_gc_hg_accel_miners|sco_vol_miners|miners | BHP | 0.12 | 6.2 | 97.13 | 0.6 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.23;q_short_entry=2.23;q_short_exit=1.43629;vol_diff=-0.0885714;accel=2.41951; aggregate BHP capped at 12.0%|sco_vol_regime_pulse active; sco_vol=0.0107019;vol_quantile=0.0120905;vol_diff=0.00222488; aggregate BHP capped at 12.0%|persistent_binary active; feature=-0.0564247; aggregate BHP capped at 12.0% |
| stock | sco_specialty_alloys | CRS | 0.04 | 0.4 | 477.1 | 1.1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-1.56723;drawdown_63d=-0.941959;realized_vol_63d=-0.863375 |
| stock | miners | FSUGY | 0.05 | 9.8 | 25.64 | 0.7 | 0.3 | persistent_binary active; feature=-0.0564247 |
| stock | sco_specialty_alloys | HWM | 0.02 | 0.4 | 263.29 | 0.9 | 0.1 | sco_specialty_alloys_hysteresis active; ret_63d=-1.56723;drawdown_63d=-0.941959;realized_vol_63d=-0.863375 |
| stock | sco_vol_gc_hg_accel_miners|sco_vol_miners|miners | RIO | 0.12 | 5.7 | 104.8 | 0.3 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.23;q_short_entry=2.23;q_short_exit=1.43629;vol_diff=-0.0885714;accel=2.41951; aggregate RIO capped at 12.0%|sco_vol_regime_pulse active; sco_vol=0.0107019;vol_quantile=0.0120905;vol_diff=0.00222488; aggregate RIO capped at 12.0%|persistent_binary active; feature=-0.0564247; aggregate RIO capped at 12.0% |
| stock | sco_vol_gc_hg_accel_miners|sco_vol_miners|miners | SCCO | 0.12 | 2.8 | 214.25 | 0.8 | 0.9 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.23;q_short_entry=2.23;q_short_exit=1.43629;vol_diff=-0.0885714;accel=2.41951|sco_vol_regime_pulse active; sco_vol=0.0107019;vol_quantile=0.0120905;vol_diff=0.00222488|persistent_binary active; feature=-0.0564247 |
| stock | sco_vol_gc_hg_accel_miners|sco_vol_miners|miners | VALE | 0.07 | 23.3 | 15.04 | 0.3 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.23;q_short_entry=2.23;q_short_exit=1.43629;vol_diff=-0.0885714;accel=2.41951|sco_vol_regime_pulse active; sco_vol=0.0107019;vol_quantile=0.0120905;vol_diff=0.00222488|persistent_binary active; feature=-0.0564247 |
| hedge | hedge | SPY | -0.363983 | -2.4 | 763.47 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | -0.297765 | -12.6 | 117.87 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | sco_vol_gc_hg_accel_miners|sco_vol_miners|miners | VALE | BUY | 23 | 23 | 0.069184 | False | 15.04 | 15 | 15.08 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XME | SELL | -2 | -2 | -0.047148 | False | 117.87 | 117.58 | 118.16 | single aggregate hedge order after confirming stock fills |
