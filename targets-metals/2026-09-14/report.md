# Metals Daily Targets: 2026-09-14

- Signal as-of date: 2026-09-11
- Target trading date: 2026-09-14
- AUM: $5,000.00
- Gross stock weight: 50.00%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: 50.00%
- Gross hedge weight: 52.99%
- Total net weight after hedges: -2.99%
- Turnover from Metals-attributed current positions: 11.63%
- Full eligible order turnover: 1.72%
- Today's total child-order turnover: 1.92%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $0.24

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
| total_hedge | 0.529907 | -0.529907 | 2649.53 | -2649.53 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | sco_specialty_alloys | ATI | 0.02 | 0.5 | 198.77 | 1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-0.846332;drawdown_63d=0.244043;realized_vol_63d=0.168167 |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | BHP | 0.12 | 6.9 | 87.15 | 0.6 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.44143;q_long_exit=2.18229;q_short_entry=2.18229;q_short_exit=1.41943;vol_diff=0.00357143;accel=-0.650903; aggregate BHP capped at 12.0%\|sco_vol_regime_pulse active; sco_vol=1.44143;vol_quantile=2.01793;vol_diff=0.00357143; aggregate BHP capped at 12.0%\|persistent_binary active; feature=-0.00751125; aggregate BHP capped at 12.0% |
| stock | sco_specialty_alloys | CRS | 0.02 | 0.2 | 443.19 | 1.1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-0.846332;drawdown_63d=0.244043;realized_vol_63d=0.168167 |
| stock | miners | FSUGY | 0.05 | 10.4 | 24.01 | 0.6 | 0.3 | persistent_binary active; feature=-0.00751125 |
| stock | sco_specialty_alloys | HWM | 0.01 | 0.2 | 229.61 | 1 | 0.1 | sco_specialty_alloys_hysteresis active; ret_63d=-0.846332;drawdown_63d=0.244043;realized_vol_63d=0.168167 |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | RIO | 0.12 | 6 | 99.96 | 0.3 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.44143;q_long_exit=2.18229;q_short_entry=2.18229;q_short_exit=1.41943;vol_diff=0.00357143;accel=-0.650903; aggregate RIO capped at 12.0%\|sco_vol_regime_pulse active; sco_vol=1.44143;vol_quantile=2.01793;vol_diff=0.00357143; aggregate RIO capped at 12.0%\|persistent_binary active; feature=-0.00751125; aggregate RIO capped at 12.0% |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|copper_miner\|miners | SCCO | 0.08 | 2.1 | 193.49 | 0.8 | 0.9 | sco_vol_gc_hg_combo active; sco_vol=1.44143;q_long_exit=2.18229;q_short_entry=2.18229;q_short_exit=1.41943;vol_diff=0.00357143;accel=-0.650903\|sco_vol_regime_pulse active; sco_vol=1.44143;vol_quantile=2.01793;vol_diff=0.00357143\|copper_energy_terms_of_trade active; hg_cl_ratio=0.796594;ho_ret=-0.0196077;hg_mv_5=0.811902;hg_mv_200=0.849047;hg_mv_diff=-0.0371445;hg_threshold=0.00735647;ho_momentum_20d=0.182576;ho_threshold=0.0295451\|persistent_binary active; feature=-0.00751125 |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | VALE | 0.08 | 26.3 | 15.23 | 0.2 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.44143;q_long_exit=2.18229;q_short_entry=2.18229;q_short_exit=1.41943;vol_diff=0.00357143;accel=-0.650903\|sco_vol_regime_pulse active; sco_vol=1.44143;vol_quantile=2.01793;vol_diff=0.00357143\|persistent_binary active; feature=-0.00751125 |
| hedge | hedge | SPY | -0.270876 | -1.8 | 764.29 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | -0.259031 | -11.4 | 113.63 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | miners | FSUGY | SELL | -4 | -4 | -0.019208 | False | 24.01 | 23.95 | 24.07 | execute once; no same-day reversal or duplicate order |
