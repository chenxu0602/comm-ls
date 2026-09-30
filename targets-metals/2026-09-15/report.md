# Metals Daily Targets: 2026-09-15

- Signal as-of date: 2026-09-14
- Target trading date: 2026-09-15
- AUM: $5,000.00
- Gross stock weight: 45.00%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: 45.00%
- Gross hedge weight: 46.46%
- Total net weight after hedges: -1.46%
- Turnover from Metals-attributed current positions: 14.57%
- Full eligible order turnover: 13.16%
- Today's total child-order turnover: 19.75%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $2.47

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
| stock_long_without_hedge | 0.45 | 0.45 | 2250 | 2250 | 5 |
| stock_short_without_hedge | 0 | 0 | 0 | 0 | 0 |
| total_hedge | 0.464622 | -0.464622 | 2323.11 | -2323.11 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | BHP | 0.12 | 7.1 | 84.74 | 0.6 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.43571;q_long_exit=2.17971;q_short_entry=2.17971;q_short_exit=1.41943;vol_diff=-0.0271428;accel=-0.542245; aggregate BHP capped at 12.0%\|sco_vol_regime_pulse active; sco_vol=1.43571;vol_quantile=2.01143;vol_diff=-0.0271428; aggregate BHP capped at 12.0%\|persistent_binary active; feature=-0.0235506; aggregate BHP capped at 12.0% |
| stock | miners | FSUGY | 0.05 | 10.6 | 23.68 | 0.6 | 0.3 | persistent_binary active; feature=-0.0235506 |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | RIO | 0.12 | 6.1 | 97.64 | 0.3 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.43571;q_long_exit=2.17971;q_short_entry=2.17971;q_short_exit=1.41943;vol_diff=-0.0271428;accel=-0.542245; aggregate RIO capped at 12.0%\|sco_vol_regime_pulse active; sco_vol=1.43571;vol_quantile=2.01143;vol_diff=-0.0271428; aggregate RIO capped at 12.0%\|persistent_binary active; feature=-0.0235506; aggregate RIO capped at 12.0% |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|copper_miner\|miners | SCCO | 0.08 | 2.1 | 188.35 | 0.7 | 0.9 | sco_vol_gc_hg_combo active; sco_vol=1.43571;q_long_exit=2.17971;q_short_entry=2.17971;q_short_exit=1.41943;vol_diff=-0.0271428;accel=-0.542245\|sco_vol_regime_pulse active; sco_vol=1.43571;vol_quantile=2.01143;vol_diff=-0.0271428\|copper_energy_terms_of_trade active; hg_cl_ratio=0.773117;ho_ret=-0.00273006;hg_mv_5=0.810137;hg_mv_200=0.84866;hg_mv_diff=-0.0385234;hg_threshold=0.00732695;ho_momentum_20d=0.17189;ho_threshold=0.0295784\|persistent_binary active; feature=-0.0235506 |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | VALE | 0.08 | 27.4 | 14.61 | 0.2 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.43571;q_long_exit=2.17971;q_short_entry=2.17971;q_short_exit=1.41943;vol_diff=-0.0271428;accel=-0.542245\|sco_vol_regime_pulse active; sco_vol=1.43571;vol_quantile=2.01143;vol_diff=-0.0271428\|persistent_binary active; feature=-0.0235506 |
| hedge | hedge | SPY | -0.217047 | -1.4 | 760.88 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | -0.247575 | -11.2 | 110.17 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | miners | FSUGY | BUY | 1 | 1 | 0.004736 | False | 23.68 | 23.62 | 23.74 | execute once; no same-day reversal or duplicate order |
| stock | sco_specialty_alloys | ATI | SELL | -1 | -1 | -0.03763 | False | 188.15 | 187.68 | 188.62 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | VALE | BUY | 1 | 1 | 0.002922 | False | 14.61 | 14.57 | 14.65 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | SPY | BUY | 1 | 1 | 0.152176 | False | 760.88 | 758.98 | 762.78 | single aggregate hedge order after confirming stock fills |
