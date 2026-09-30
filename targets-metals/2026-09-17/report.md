# Metals Daily Targets: 2026-09-17

- Signal as-of date: 2026-09-16
- Target trading date: 2026-09-17
- AUM: $5,000.00
- Gross stock weight: 44.00%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: 44.00%
- Gross hedge weight: 46.07%
- Total net weight after hedges: -2.07%
- Turnover from Metals-attributed current positions: 20.78%
- Full eligible order turnover: 15.76%
- Today's total child-order turnover: 23.31%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $2.91

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
| stock_long_without_hedge | 0.44 | 0.44 | 2200 | 2200 | 8 |
| stock_short_without_hedge | 0 | 0 | 0 | 0 | 0 |
| total_hedge | 0.460673 | -0.460673 | 2303.36 | -2303.36 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | sco_specialty_alloys | ATI | 0.02 | 0.5 | 189.65 | 1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-0.573388;drawdown_63d=0.08265;realized_vol_63d=-0.106362 |
| stock | sco_vol_gc_hg_accel_miners\|miners | BHP | 0.12 | 7.1 | 84.14 | 0.6 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.36071;q_long_exit=2.17257;q_short_entry=2.17257;q_short_exit=1.41643;vol_diff=-0.0557143;accel=0.144362; aggregate BHP capped at 12.0%\|persistent_binary active; feature=-0.0235556; aggregate BHP capped at 12.0% |
| stock | sco_specialty_alloys | CRS | 0.02 | 0.2 | 411.8 | 1.1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-0.573388;drawdown_63d=0.08265;realized_vol_63d=-0.106362 |
| stock | miners | FSUGY | 0.05 | 10.8 | 23.16 | 0.6 | 0.3 | persistent_binary active; feature=-0.0235556 |
| stock | sco_specialty_alloys | HWM | 0.01 | 0.2 | 227.73 | 1 | 0.1 | sco_specialty_alloys_hysteresis active; ret_63d=-0.573388;drawdown_63d=0.08265;realized_vol_63d=-0.106362 |
| stock | sco_vol_gc_hg_accel_miners\|miners | RIO | 0.12 | 6.3 | 95.79 | 0.3 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.36071;q_long_exit=2.17257;q_short_entry=2.17257;q_short_exit=1.41643;vol_diff=-0.0557143;accel=0.144362; aggregate RIO capped at 12.0%\|persistent_binary active; feature=-0.0235556; aggregate RIO capped at 12.0% |
| stock | sco_vol_gc_hg_accel_miners\|copper_miner\|miners | SCCO | 0.05 | 1.3 | 189.88 | 0.7 | 0.9 | sco_vol_gc_hg_combo active; sco_vol=1.36071;q_long_exit=2.17257;q_short_entry=2.17257;q_short_exit=1.41643;vol_diff=-0.0557143;accel=0.144362\|copper_energy_terms_of_trade active; hg_cl_ratio=0.78252;ho_ret=-0.001938;hg_mv_5=0.779276;hg_mv_200=0.847521;hg_mv_diff=-0.0682443;hg_threshold=0.00759558;ho_momentum_20d=0.184869;ho_threshold=0.0298251\|persistent_binary active; feature=-0.0235556 |
| stock | sco_vol_gc_hg_accel_miners\|miners | VALE | 0.05 | 17.7 | 14.13 | 0.2 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.36071;q_long_exit=2.17257;q_short_entry=2.17257;q_short_exit=1.41643;vol_diff=-0.0557143;accel=0.144362\|persistent_binary active; feature=-0.0235556 |
| hedge | hedge | SPY | -0.240823 | -1.6 | 754.05 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | -0.21985 | -10.1 | 108.77 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | sco_specialty_alloys | ATI | BUY | 1 | 1 | 0.03793 | False | 189.65 | 189.18 | 190.12 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners\|miners | VALE | SELL | -8 | -8 | -0.022608 | False | 14.13 | 14.09 | 14.17 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | SPY | SELL | -1 | -1 | -0.15081 | False | 754.05 | 752.16 | 755.94 | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XME | SELL | -1 | -1 | -0.021754 | False | 108.77 | 108.5 | 109.04 | single aggregate hedge order after confirming stock fills |
