# Metals Daily Targets: 2026-09-01

- Signal as-of date: 2026-08-31
- Target trading date: 2026-09-01
- AUM: $5,000.00
- Gross stock weight: 51.00%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: 51.00%
- Gross hedge weight: 52.45%
- Total net weight after hedges: -1.45%
- Turnover from Metals-attributed current positions: 26.01%
- Full eligible order turnover: 18.42%
- Today's total child-order turnover: 17.91%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $2.24

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
| stock_long_without_hedge | 0.51 | 0.51 | 2550 | 2550 | 8 |
| stock_short_without_hedge | 0 | 0 | 0 | 0 | 0 |
| total_hedge | 0.524496 | -0.524496 | 2622.48 | -2622.48 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | sco_specialty_alloys | ATI | 0.04 | 1 | 204.2 | 1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-0.816861;drawdown_63d=0.631022;realized_vol_63d=-0.459994 |
| stock | hg_gc_gap_gc_carry_iron\|sco_vol_gc_hg_accel_miners\|miners | BHP | 0.12 | 6.4 | 93.92 | 0.6 | 0.5 | dual_feature_hysteresis active; hg_gap=-0.034833;gc_carry=-3.06876; aggregate BHP capped at 12.0%\|sco_vol_gc_hg_combo active; sco_vol=1.18714;q_long_exit=2.20029;q_short_entry=2.20029;q_short_exit=1.43829;vol_diff=-0.130714;accel=0.425975; aggregate BHP capped at 12.0%\|persistent_binary active; feature=-0.034833; aggregate BHP capped at 12.0% |
| stock | sco_specialty_alloys | CRS | 0.04 | 0.4 | 476.42 | 1.1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-0.816861;drawdown_63d=0.631022;realized_vol_63d=-0.459994 |
| stock | hg_gc_gap_gc_carry_iron\|miners | FSUGY | 0.065 | 12.9 | 25.16 | 0.7 | 0.2 | dual_feature_hysteresis active; hg_gap=-0.034833;gc_carry=-3.06876\|persistent_binary active; feature=-0.034833 |
| stock | sco_specialty_alloys | HWM | 0.02 | 0.4 | 244.95 | 0.9 | 0.1 | sco_specialty_alloys_hysteresis active; ret_63d=-0.816861;drawdown_63d=0.631022;realized_vol_63d=-0.459994 |
| stock | hg_gc_gap_gc_carry_iron\|sco_vol_gc_hg_accel_miners\|miners | RIO | 0.12 | 5.9 | 102.5 | 0.3 | 0.5 | dual_feature_hysteresis active; hg_gap=-0.034833;gc_carry=-3.06876; aggregate RIO capped at 12.0%\|sco_vol_gc_hg_combo active; sco_vol=1.18714;q_long_exit=2.20029;q_short_entry=2.20029;q_short_exit=1.43829;vol_diff=-0.130714;accel=0.425975; aggregate RIO capped at 12.0%\|persistent_binary active; feature=-0.034833; aggregate RIO capped at 12.0% |
| stock | sco_vol_gc_hg_accel_miners\|copper_miner\|miners | SCCO | 0.025 | 0.6 | 208.87 | 0.8 | 0.9 | sco_vol_gc_hg_combo active; sco_vol=1.18714;q_long_exit=2.20029;q_short_entry=2.20029;q_short_exit=1.43829;vol_diff=-0.130714;accel=0.425975\|copper_energy_terms_of_trade active; hg_cl_ratio=0.832375;ho_ret=0.0300682;hg_mv_5=0.836105;hg_mv_200=0.851344;hg_mv_diff=-0.0152394;hg_threshold=0.00706808;ho_momentum_20d=0.151183;ho_threshold=0.0293656\|persistent_binary active; feature=-0.034833 |
| stock | hg_gc_gap_gc_carry_iron\|sco_vol_gc_hg_accel_miners\|miners | VALE | 0.08 | 26.5 | 15.09 | 0.3 | 0.5 | dual_feature_hysteresis active; hg_gap=-0.034833;gc_carry=-3.06876\|sco_vol_gc_hg_combo active; sco_vol=1.18714;q_long_exit=2.20029;q_short_entry=2.20029;q_short_exit=1.43829;vol_diff=-0.130714;accel=0.425975\|persistent_binary active; feature=-0.034833 |
| hedge | hedge | SPY | -0.302119 | -2 | 767.05 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | -0.222377 | -9.4 | 118.13 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | hg_gc_gap_gc_carry_iron\|miners | FSUGY | BUY | 3 | 3 | 0.015096 | False | 25.16 | 25.1 | 25.22 | execute once; no same-day reversal or duplicate order |
| stock | hg_gc_gap_gc_carry_iron\|sco_vol_gc_hg_accel_miners\|miners | VALE | BUY | 11 | 11 | 0.033198 | False | 15.09 | 15.05 | 15.13 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners\|copper_miner\|miners | SCCO | SELL | -2 | -2 | -0.083548 | False | 208.87 | 208.35 | 209.39 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XME | BUY | 2 | 2 | 0.047252 | False | 118.13 | 117.83 | 118.43 | single aggregate hedge order after confirming stock fills |
