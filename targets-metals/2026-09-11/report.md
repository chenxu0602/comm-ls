# Metals Daily Targets: 2026-09-11

- Signal as-of date: 2026-09-10
- Target trading date: 2026-09-11
- AUM: $5,000.00
- Gross stock weight: 50.00%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: 50.00%
- Gross hedge weight: 53.08%
- Total net weight after hedges: -3.08%
- Turnover from Metals-attributed current positions: 20.98%
- Full eligible order turnover: 14.61%
- Today's total child-order turnover: 15.94%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $1.99

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
| total_hedge | 0.530813 | -0.530813 | 2654.06 | -2654.06 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | sco_specialty_alloys | ATI | 0.02 | 0.5 | 199 | 1.1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-0.74793;drawdown_63d=0.595115;realized_vol_63d=-0.00904755 |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | BHP | 0.12 | 6.9 | 87.35 | 0.6 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.47143;q_long_exit=2.18357;q_short_entry=2.18357;q_short_exit=1.41943;vol_diff=0.0692857;accel=-0.478904; aggregate BHP capped at 12.0%\|sco_vol_regime_pulse active; sco_vol=1.47143;vol_quantile=2.01871;vol_diff=0.0692857; aggregate BHP capped at 12.0%\|persistent_binary active; feature=0.00370317; aggregate BHP capped at 12.0% |
| stock | sco_specialty_alloys | CRS | 0.02 | 0.2 | 448.25 | 1.1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-0.74793;drawdown_63d=0.595115;realized_vol_63d=-0.00904755 |
| stock | miners | FSUGY | 0.05 | 10.2 | 24.43 | 0.6 | 0.3 | persistent_binary active; feature=0.00370317 |
| stock | sco_specialty_alloys | HWM | 0.01 | 0.2 | 227.91 | 1 | 0.1 | sco_specialty_alloys_hysteresis active; ret_63d=-0.74793;drawdown_63d=0.595115;realized_vol_63d=-0.00904755 |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | RIO | 0.12 | 6 | 99.39 | 0.3 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.47143;q_long_exit=2.18357;q_short_entry=2.18357;q_short_exit=1.41943;vol_diff=0.0692857;accel=-0.478904; aggregate RIO capped at 12.0%\|sco_vol_regime_pulse active; sco_vol=1.47143;vol_quantile=2.01871;vol_diff=0.0692857; aggregate RIO capped at 12.0%\|persistent_binary active; feature=0.00370317; aggregate RIO capped at 12.0% |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|copper_miner\|miners | SCCO | 0.08 | 2.1 | 194.14 | 0.8 | 0.9 | sco_vol_gc_hg_combo active; sco_vol=1.47143;q_long_exit=2.18357;q_short_entry=2.18357;q_short_exit=1.41943;vol_diff=0.0692857;accel=-0.478904\|sco_vol_regime_pulse active; sco_vol=1.47143;vol_quantile=2.01871;vol_diff=0.0692857\|copper_energy_terms_of_trade active; hg_cl_ratio=0.781698;ho_ret=0.0520481;hg_mv_5=0.809784;hg_mv_200=0.849414;hg_mv_diff=-0.0396304;hg_threshold=0.00742247;ho_momentum_20d=0.190872;ho_threshold=0.029766\|persistent_binary active; feature=0.00370317 |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | VALE | 0.08 | 26.2 | 15.28 | 0.2 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.47143;q_long_exit=2.18357;q_short_entry=2.18357;q_short_exit=1.41943;vol_diff=0.0692857;accel=-0.478904\|sco_vol_regime_pulse active; sco_vol=1.47143;vol_quantile=2.01871;vol_diff=0.0692857\|persistent_binary active; feature=0.00370317 |
| hedge | hedge | SPY | -0.272447 | -1.8 | 757.83 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | -0.258365 | -11.3 | 114.77 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | miners | FSUGY | SELL | -4 | -4 | -0.019544 | False | 24.43 | 24.37 | 24.49 | execute once; no same-day reversal or duplicate order |
| stock | sco_specialty_alloys | ATI | BUY | 1 | 1 | 0.0398 | False | 199 | 198.5 | 199.5 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|copper_miner\|miners | SCCO | BUY | 1 | 1 | 0.038828 | False | 194.14 | 193.65 | 194.63 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | VALE | SELL | -5 | -5 | -0.01528 | False | 15.28 | 15.24 | 15.32 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XME | SELL | -2 | -2 | -0.045908 | False | 114.77 | 114.48 | 115.06 | single aggregate hedge order after confirming stock fills |
