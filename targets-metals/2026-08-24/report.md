# Metals Daily Targets: 2026-08-24

- Signal as-of date: 2026-08-21
- Target trading date: 2026-08-24
- AUM: $5,000.00
- Gross stock weight: 58.00%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: 58.00%
- Gross hedge weight: 66.05%
- Total net weight after hedges: -8.05%
- Turnover from Metals-attributed current positions: 124.05%
- Full eligible order turnover: 118.05%
- Today's total child-order turnover: 115.18%
- Stock daily turnover cap: 100.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $14.40

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
| total_hedge | 0.660503 | -0.660503 | 3302.52 | -3302.52 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | sco_specialty_alloys | ATI | 0.04 | 1 | 207.01 | 1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-1.79106;drawdown_63d=-0.948206;realized_vol_63d=-0.683102 |
| stock | sco_vol_gc_hg_accel_miners|sco_vol_miners|miners | BHP | 0.12 | 6.2 | 97.03 | 0.6 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.24043;q_short_entry=2.24043;q_short_exit=1.44014;vol_diff=-0.127857;accel=2.39431; aggregate BHP capped at 12.0%|sco_vol_regime_pulse active; sco_vol=0.00970996;vol_quantile=0.0120982;vol_diff=0.00125408; aggregate BHP capped at 12.0%|persistent_binary active; feature=-0.0459931; aggregate BHP capped at 12.0% |
| stock | sco_specialty_alloys | CRS | 0.04 | 0.4 | 492.38 | 1.1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-1.79106;drawdown_63d=-0.948206;realized_vol_63d=-0.683102 |
| stock | miners | FSUGY | 0.05 | 9.7 | 25.69 | 0.6 | 0.3 | persistent_binary active; feature=-0.0459931 |
| stock | sco_specialty_alloys | HWM | 0.02 | 0.4 | 271.68 | 0.9 | 0.1 | sco_specialty_alloys_hysteresis active; ret_63d=-1.79106;drawdown_63d=-0.948206;realized_vol_63d=-0.683102 |
| stock | sco_vol_gc_hg_accel_miners|sco_vol_miners|miners | RIO | 0.12 | 5.7 | 105.3 | 0.3 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.24043;q_short_entry=2.24043;q_short_exit=1.44014;vol_diff=-0.127857;accel=2.39431; aggregate RIO capped at 12.0%|sco_vol_regime_pulse active; sco_vol=0.00970996;vol_quantile=0.0120982;vol_diff=0.00125408; aggregate RIO capped at 12.0%|persistent_binary active; feature=-0.0459931; aggregate RIO capped at 12.0% |
| stock | sco_vol_gc_hg_accel_miners|sco_vol_miners|miners | SCCO | 0.12 | 2.8 | 216 | 0.8 | 0.9 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.24043;q_short_entry=2.24043;q_short_exit=1.44014;vol_diff=-0.127857;accel=2.39431|sco_vol_regime_pulse active; sco_vol=0.00970996;vol_quantile=0.0120982;vol_diff=0.00125408|persistent_binary active; feature=-0.0459931 |
| stock | sco_vol_gc_hg_accel_miners|sco_vol_miners|miners | VALE | 0.07 | 24 | 14.59 | 0.3 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.24043;q_short_entry=2.24043;q_short_exit=1.44014;vol_diff=-0.127857;accel=2.39431|sco_vol_regime_pulse active; sco_vol=0.00970996;vol_quantile=0.0120982;vol_diff=0.00125408|persistent_binary active; feature=-0.0459931 |
| hedge | hedge | SPY | -0.361871 | -2.4 | 765.72 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | -0.298632 | -12.5 | 119.34 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | miners | FSUGY | BUY | 10 | 10 | 0.05138 | False | 25.69 | 25.63 | 25.75 | execute once; no same-day reversal or duplicate order |
| stock | sco_specialty_alloys | ATI | BUY | 1 | 1 | 0.041402 | False | 207.01 | 206.49 | 207.53 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners|sco_vol_miners|miners | BHP | BUY | 6 | 6 | 0.116436 | False | 97.03 | 96.79 | 97.27 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners|sco_vol_miners|miners | RIO | BUY | 6 | 6 | 0.12636 | False | 105.3 | 105.04 | 105.56 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners|sco_vol_miners|miners | SCCO | BUY | 3 | 3 | 0.1296 | False | 216 | 215.46 | 216.54 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners|sco_vol_miners|miners | VALE | BUY | 24 | 24 | 0.070032 | False | 14.59 | 14.55 | 14.63 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | SPY | SELL | -2 | -2 | -0.306288 | False | 765.72 | 763.81 | 767.63 | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XME | SELL | -13 | -13 | -0.310284 | False | 119.34 | 119.04 | 119.64 | single aggregate hedge order after confirming stock fills |
