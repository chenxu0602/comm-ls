# Metals Daily Targets: 2026-09-21

- Signal as-of date: 2026-09-18
- Target trading date: 2026-09-21
- AUM: $5,000.00
- Gross stock weight: 45.00%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: 45.00%
- Gross hedge weight: 46.76%
- Total net weight after hedges: -1.76%
- Turnover from Metals-attributed current positions: 19.53%
- Full eligible order turnover: 12.18%
- Today's total child-order turnover: 11.10%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $1.39

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
| total_hedge | 0.467642 | -0.467642 | 2338.21 | -2338.21 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | BHP | 0.12 | 7 | 86.27 | 0.6 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.37571;q_long_exit=2.16929;q_short_entry=2.16929;q_short_exit=1.41471;vol_diff=0.0664286;accel=-0.216246; aggregate BHP capped at 12.0%\|sco_vol_regime_pulse active; sco_vol=1.37571;vol_quantile=1.991;vol_diff=0.0664286; aggregate BHP capped at 12.0%\|persistent_binary active; feature=-0.00897309; aggregate BHP capped at 12.0% |
| stock | miners | FSUGY | 0.05 | 10.6 | 23.65 | 0.6 | 0.3 | persistent_binary active; feature=-0.00897309 |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | RIO | 0.12 | 6.2 | 97.37 | 0.3 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.37571;q_long_exit=2.16929;q_short_entry=2.16929;q_short_exit=1.41471;vol_diff=0.0664286;accel=-0.216246; aggregate RIO capped at 12.0%\|sco_vol_regime_pulse active; sco_vol=1.37571;vol_quantile=1.991;vol_diff=0.0664286; aggregate RIO capped at 12.0%\|persistent_binary active; feature=-0.00897309; aggregate RIO capped at 12.0% |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|copper_miner\|miners | SCCO | 0.08 | 2 | 195.7 | 0.7 | 0.9 | sco_vol_gc_hg_combo active; sco_vol=1.37571;q_long_exit=2.16929;q_short_entry=2.16929;q_short_exit=1.41471;vol_diff=0.0664286;accel=-0.216246\|sco_vol_regime_pulse active; sco_vol=1.37571;vol_quantile=1.991;vol_diff=0.0664286\|copper_energy_terms_of_trade active; hg_cl_ratio=0.798508;ho_ret=-0.00916438;hg_mv_5=0.78351;hg_mv_200=0.846472;hg_mv_diff=-0.0629618;hg_threshold=0.00779115;ho_momentum_20d=0.141535;ho_threshold=0.0301613\|persistent_binary active; feature=-0.00897309 |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | VALE | 0.08 | 28.1 | 14.21 | 0.2 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.37571;q_long_exit=2.16929;q_short_entry=2.16929;q_short_exit=1.41471;vol_diff=0.0664286;accel=-0.216246\|sco_vol_regime_pulse active; sco_vol=1.37571;vol_quantile=1.991;vol_diff=0.0664286\|persistent_binary active; feature=-0.00897309 |
| hedge | hedge | SPY | -0.219917 | -1.4 | 761.69 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | -0.247725 | -11.4 | 108.68 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|copper_miner\|miners | SCCO | BUY | 1 | 1 | 0.03914 | False | 195.7 | 195.21 | 196.19 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | VALE | BUY | 10 | 10 | 0.02842 | False | 14.21 | 14.17 | 14.25 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XME | SELL | -2 | -2 | -0.043472 | False | 108.68 | 108.41 | 108.95 | single aggregate hedge order after confirming stock fills |
