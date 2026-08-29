# Metals Daily Targets: 2026-08-27

- Signal as-of date: 2026-08-26
- Target trading date: 2026-08-27
- AUM: $5,000.00
- Gross stock weight: 62.50%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: 62.50%
- Gross hedge weight: 69.80%
- Total net weight after hedges: -7.30%
- Turnover from Metals-attributed current positions: 16.29%
- Full eligible order turnover: 7.82%
- Today's total child-order turnover: 15.32%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $1.92

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
| stock_long_without_hedge | 0.625 | 0.625 | 3125 | 3125 | 8 |
| stock_short_without_hedge | 0 | 0 | 0 | 0 | 0 |
| total_hedge | 0.698002 | -0.698002 | 3490.01 | -3490.01 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | sco_specialty_alloys | ATI | 0.04 | 0.9 | 212.86 | 1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-1.23679;drawdown_63d=-0.332554;realized_vol_63d=-0.385305 |
| stock | hg_gc_gap_gc_carry_iron|sco_vol_gc_hg_accel_miners|sco_vol_miners|miners | BHP | 0.12 | 6.2 | 96.33 | 0.6 | 0.5 | dual_feature_hysteresis active; hg_gap=-0.0533193;gc_carry=-0.243697; aggregate BHP capped at 12.0%|sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.213;q_short_entry=2.213;q_short_exit=1.42943;vol_diff=0.0442857;accel=1.14612; aggregate BHP capped at 12.0%|sco_vol_regime_pulse active; sco_vol=0.0109736;vol_quantile=0.0120665;vol_diff=0.0034501; aggregate BHP capped at 12.0%|persistent_binary active; feature=-0.0533193; aggregate BHP capped at 12.0% |
| stock | sco_specialty_alloys | CRS | 0.04 | 0.4 | 483.7 | 1.1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-1.23679;drawdown_63d=-0.332554;realized_vol_63d=-0.385305 |
| stock | hg_gc_gap_gc_carry_iron|miners | FSUGY | 0.065 | 13 | 25.02 | 0.7 | 0.3 | dual_feature_hysteresis active; hg_gap=-0.0533193;gc_carry=-0.243697|persistent_binary active; feature=-0.0533193 |
| stock | sco_specialty_alloys | HWM | 0.02 | 0.4 | 269.34 | 0.9 | 0.1 | sco_specialty_alloys_hysteresis active; ret_63d=-1.23679;drawdown_63d=-0.332554;realized_vol_63d=-0.385305 |
| stock | hg_gc_gap_gc_carry_iron|sco_vol_gc_hg_accel_miners|sco_vol_miners|miners | RIO | 0.12 | 5.7 | 104.7 | 0.3 | 0.5 | dual_feature_hysteresis active; hg_gap=-0.0533193;gc_carry=-0.243697; aggregate RIO capped at 12.0%|sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.213;q_short_entry=2.213;q_short_exit=1.42943;vol_diff=0.0442857;accel=1.14612; aggregate RIO capped at 12.0%|sco_vol_regime_pulse active; sco_vol=0.0109736;vol_quantile=0.0120665;vol_diff=0.0034501; aggregate RIO capped at 12.0%|persistent_binary active; feature=-0.0533193; aggregate RIO capped at 12.0% |
| stock | sco_vol_gc_hg_accel_miners|sco_vol_miners|miners | SCCO | 0.12 | 2.8 | 213.75 | 0.8 | 0.9 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.213;q_short_entry=2.213;q_short_exit=1.42943;vol_diff=0.0442857;accel=1.14612|sco_vol_regime_pulse active; sco_vol=0.0109736;vol_quantile=0.0120665;vol_diff=0.0034501|persistent_binary active; feature=-0.0533193 |
| stock | hg_gc_gap_gc_carry_iron|sco_vol_gc_hg_accel_miners|sco_vol_miners|miners | VALE | 0.1 | 33 | 15.16 | 0.3 | 0.5 | dual_feature_hysteresis active; hg_gap=-0.0533193;gc_carry=-0.243697|sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.213;q_short_entry=2.213;q_short_exit=1.42943;vol_diff=0.0442857;accel=1.14612|sco_vol_regime_pulse active; sco_vol=0.0109736;vol_quantile=0.0120665;vol_diff=0.0034501|persistent_binary active; feature=-0.0533193 |
| hedge | hedge | SPY | -0.381473 | -2.5 | 766.08 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | -0.31653 | -13.2 | 120.31 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | hedge | SPY | BUY | 1 | 1 | 0.153216 | False | 766.08 | 764.16 | 768 | single aggregate hedge order after confirming stock fills |
