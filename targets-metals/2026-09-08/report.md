# Metals Daily Targets: 2026-09-08

- Signal as-of date: 2026-09-04
- Target trading date: 2026-09-08
- AUM: $5,000.00
- Gross stock weight: 50.00%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: 50.00%
- Gross hedge weight: 50.82%
- Total net weight after hedges: -0.82%
- Turnover from Metals-attributed current positions: 19.69%
- Full eligible order turnover: 9.61%
- Today's total child-order turnover: 10.14%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $1.27

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
| stock_long_without_hedge | 0.5 | 0.5 | 2500 | 2500 | 8 |
| stock_short_without_hedge | 0 | 0 | 0 | 0 | 0 |
| total_hedge | 0.508198 | -0.508198 | 2540.99 | -2540.99 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | sco_specialty_alloys | ATI | 0.02 | 0.5 | 210.65 | 1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-0.367115;drawdown_63d=0.681749;realized_vol_63d=-0.352698 |
| stock | hg_gc_gap_gc_carry_iron\|sco_vol_gc_hg_accel_miners\|miners | BHP | 0.12 | 6.6 | 90.42 | 0.6 | 0.5 | dual_feature_hysteresis active; hg_gap=-0.0211887;gc_carry=-0.0876848; aggregate BHP capped at 12.0%\|sco_vol_gc_hg_combo active; sco_vol=1.38643;q_long_exit=2.18986;q_short_entry=2.18986;q_short_exit=1.42943;vol_diff=-0.08;accel=-0.888313; aggregate BHP capped at 12.0%\|persistent_binary active; feature=-0.0211887; aggregate BHP capped at 12.0% |
| stock | sco_specialty_alloys | CRS | 0.02 | 0.2 | 475.33 | 1.1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-0.367115;drawdown_63d=0.681749;realized_vol_63d=-0.352698 |
| stock | hg_gc_gap_gc_carry_iron\|miners | FSUGY | 0.07 | 14.1 | 24.86 | 0.7 | 0.2 | dual_feature_hysteresis active; hg_gap=-0.0211887;gc_carry=-0.0876848\|persistent_binary active; feature=-0.0211887 |
| stock | sco_specialty_alloys | HWM | 0.01 | 0.2 | 259.27 | 0.9 | 0.1 | sco_specialty_alloys_hysteresis active; ret_63d=-0.367115;drawdown_63d=0.681749;realized_vol_63d=-0.352698 |
| stock | hg_gc_gap_gc_carry_iron\|sco_vol_gc_hg_accel_miners\|miners | RIO | 0.12 | 5.8 | 103.27 | 0.3 | 0.5 | dual_feature_hysteresis active; hg_gap=-0.0211887;gc_carry=-0.0876848; aggregate RIO capped at 12.0%\|sco_vol_gc_hg_combo active; sco_vol=1.38643;q_long_exit=2.18986;q_short_entry=2.18986;q_short_exit=1.42943;vol_diff=-0.08;accel=-0.888313; aggregate RIO capped at 12.0%\|persistent_binary active; feature=-0.0211887; aggregate RIO capped at 12.0% |
| stock | sco_vol_gc_hg_accel_miners\|copper_miner\|miners | SCCO | 0.05 | 1.3 | 198.76 | 0.8 | 0.9 | sco_vol_gc_hg_combo active; sco_vol=1.38643;q_long_exit=2.18986;q_short_entry=2.18986;q_short_exit=1.42943;vol_diff=-0.08;accel=-0.888313\|copper_energy_terms_of_trade active; hg_cl_ratio=0.781945;ho_ret=-0.011693;hg_mv_5=0.786595;hg_mv_200=0.84966;hg_mv_diff=-0.0630654;hg_threshold=0.00738761;ho_momentum_20d=0.180924;ho_threshold=0.0301452\|persistent_binary active; feature=-0.0211887 |
| stock | hg_gc_gap_gc_carry_iron\|sco_vol_gc_hg_accel_miners\|miners | VALE | 0.09 | 29.5 | 15.27 | 0.2 | 0.5 | dual_feature_hysteresis active; hg_gap=-0.0211887;gc_carry=-0.0876848\|sco_vol_gc_hg_combo active; sco_vol=1.38643;q_long_exit=2.18986;q_short_entry=2.18986;q_short_exit=1.42943;vol_diff=-0.08;accel=-0.888313\|persistent_binary active; feature=-0.0211887 |
| hedge | hedge | SPY | -0.271457 | -1.8 | 770.19 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | -0.236741 | -10 | 118.62 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | hg_gc_gap_gc_carry_iron\|miners | FSUGY | BUY | 4 | 4 | 0.019888 | False | 24.86 | 24.8 | 24.92 | execute once; no same-day reversal or duplicate order |
| stock | hg_gc_gap_gc_carry_iron\|sco_vol_gc_hg_accel_miners\|miners | BHP | BUY | 1 | 1 | 0.018084 | False | 90.42 | 90.19 | 90.65 | execute once; no same-day reversal or duplicate order |
| stock | hg_gc_gap_gc_carry_iron\|sco_vol_gc_hg_accel_miners\|miners | VALE | BUY | 13 | 13 | 0.039702 | False | 15.27 | 15.23 | 15.31 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XME | SELL | -1 | -1 | -0.023724 | False | 118.62 | 118.32 | 118.92 | single aggregate hedge order after confirming stock fills |
