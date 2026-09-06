# Metals Daily Targets: 2026-08-31

- Signal as-of date: 2026-08-28
- Target trading date: 2026-08-31
- AUM: $5,000.00
- Gross stock weight: 54.00%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: 54.00%
- Gross hedge weight: 61.29%
- Total net weight after hedges: -7.29%
- Turnover from Metals-attributed current positions: 24.64%
- Full eligible order turnover: 14.13%
- Today's total child-order turnover: 15.87%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $1.98

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
| stock_long_without_hedge | 0.54 | 0.54 | 2700 | 2700 | 8 |
| stock_short_without_hedge | 0 | 0 | 0 | 0 | 0 |
| total_hedge | 0.612898 | -0.612898 | 3064.49 | -3064.49 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | sco_specialty_alloys | ATI | 0.04 | 0.9 | 213.06 | 1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-1.26327;drawdown_63d=-0.070783;realized_vol_63d=-0.44433 |
| stock | sco_vol_gc_hg_accel_miners|miners | BHP | 0.12 | 6.2 | 96.35 | 0.6 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.20186;q_short_entry=2.20186;q_short_exit=1.42143;vol_diff=-0.0771428;accel=0.765555; aggregate BHP capped at 12.0%|persistent_binary active; feature=-0.0464257; aggregate BHP capped at 12.0% |
| stock | sco_specialty_alloys | CRS | 0.04 | 0.4 | 484.93 | 1.1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-1.26327;drawdown_63d=-0.070783;realized_vol_63d=-0.44433 |
| stock | miners | FSUGY | 0.05 | 9.7 | 25.79 | 0.7 | 0.3 | persistent_binary active; feature=-0.0464257 |
| stock | sco_specialty_alloys | HWM | 0.02 | 0.4 | 265.8 | 0.9 | 0.1 | sco_specialty_alloys_hysteresis active; ret_63d=-1.26327;drawdown_63d=-0.070783;realized_vol_63d=-0.44433 |
| stock | sco_vol_gc_hg_accel_miners|miners | RIO | 0.12 | 5.7 | 104.42 | 0.3 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.20186;q_short_entry=2.20186;q_short_exit=1.42143;vol_diff=-0.0771428;accel=0.765555; aggregate RIO capped at 12.0%|persistent_binary active; feature=-0.0464257; aggregate RIO capped at 12.0% |
| stock | sco_vol_gc_hg_accel_miners|miners | SCCO | 0.1 | 2.3 | 214.88 | 0.8 | 0.9 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.20186;q_short_entry=2.20186;q_short_exit=1.42143;vol_diff=-0.0771428;accel=0.765555|persistent_binary active; feature=-0.0464257 |
| stock | sco_vol_gc_hg_accel_miners|miners | VALE | 0.05 | 16.5 | 15.16 | 0.3 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.20186;q_short_entry=2.20186;q_short_exit=1.42143;vol_diff=-0.0771428;accel=0.765555|persistent_binary active; feature=-0.0464257 |
| hedge | hedge | SPY | -0.341463 | -2.2 | 771.79 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | -0.271435 | -11.1 | 121.82 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | miners | FSUGY | SELL | -3 | -3 | -0.015474 | False | 25.79 | 25.73 | 25.85 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners|miners | SCCO | SELL | -1 | -1 | -0.042975 | False | 214.88 | 214.34 | 215.41 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners|miners | VALE | SELL | -17 | -17 | -0.051538 | False | 15.16 | 15.12 | 15.2 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XME | BUY | 2 | 2 | 0.048726 | False | 121.82 | 121.51 | 122.12 | single aggregate hedge order after confirming stock fills |
