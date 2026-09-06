# Metals Daily Targets: 2026-09-02

- Signal as-of date: 2026-09-01
- Target trading date: 2026-09-02
- AUM: $5,000.00
- Gross stock weight: 44.00%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: 44.00%
- Gross hedge weight: 46.36%
- Total net weight after hedges: -2.36%
- Turnover from Metals-attributed current positions: 17.91%
- Full eligible order turnover: 6.77%
- Today's total child-order turnover: 8.56%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $1.07

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
| total_hedge | 0.463597 | -0.463597 | 2317.99 | -2317.99 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | sco_specialty_alloys | ATI | 0.02 | 0.5 | 200.95 | 1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-0.51657;drawdown_63d=0.627782;realized_vol_63d=-0.861561 |
| stock | sco_vol_gc_hg_accel_miners\|miners | BHP | 0.12 | 6.5 | 92.82 | 0.6 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.18071;q_long_exit=2.19829;q_short_entry=2.19829;q_short_exit=1.43757;vol_diff=-0.155;accel=0.181838; aggregate BHP capped at 12.0%\|persistent_binary active; feature=-0.0194374; aggregate BHP capped at 12.0% |
| stock | sco_specialty_alloys | CRS | 0.02 | 0.2 | 473.06 | 1.1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-0.51657;drawdown_63d=0.627782;realized_vol_63d=-0.861561 |
| stock | miners | FSUGY | 0.05 | 9.9 | 25.35 | 0.7 | 0.2 | persistent_binary active; feature=-0.0194374 |
| stock | sco_specialty_alloys | HWM | 0.01 | 0.2 | 254.89 | 0.9 | 0.1 | sco_specialty_alloys_hysteresis active; ret_63d=-0.51657;drawdown_63d=0.627782;realized_vol_63d=-0.861561 |
| stock | sco_vol_gc_hg_accel_miners\|miners | RIO | 0.12 | 5.9 | 101.86 | 0.3 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.18071;q_long_exit=2.19829;q_short_entry=2.19829;q_short_exit=1.43757;vol_diff=-0.155;accel=0.181838; aggregate RIO capped at 12.0%\|persistent_binary active; feature=-0.0194374; aggregate RIO capped at 12.0% |
| stock | sco_vol_gc_hg_accel_miners\|copper_miner\|miners | SCCO | 0.05 | 1.2 | 201.61 | 0.8 | 0.9 | sco_vol_gc_hg_combo active; sco_vol=1.18071;q_long_exit=2.19829;q_short_entry=2.19829;q_short_exit=1.43757;vol_diff=-0.155;accel=0.181838\|copper_energy_terms_of_trade active; hg_cl_ratio=0.842545;ho_ret=0.0587103;hg_mv_5=0.834961;hg_mv_200=0.851187;hg_mv_diff=-0.016226;hg_threshold=0.00706404;ho_momentum_20d=0.245058;ho_threshold=0.0300853\|persistent_binary active; feature=-0.0194374 |
| stock | sco_vol_gc_hg_accel_miners\|miners | VALE | 0.05 | 16.5 | 15.12 | 0.3 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.18071;q_long_exit=2.19829;q_short_entry=2.19829;q_short_exit=1.43757;vol_diff=-0.155;accel=0.181838\|persistent_binary active; feature=-0.0194374 |
| hedge | hedge | SPY | -0.249561 | -1.6 | 761.78 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | -0.214036 | -9.2 | 115.77 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | miners | FSUGY | SELL | -3 | -3 | -0.01521 | False | 25.35 | 25.29 | 25.41 | execute once; no same-day reversal or duplicate order |
| stock | sco_specialty_alloys | ATI | SELL | -1 | -1 | -0.04019 | False | 200.95 | 200.45 | 201.45 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners\|miners | VALE | SELL | -10 | -10 | -0.03024 | False | 15.12 | 15.08 | 15.16 | execute once; no same-day reversal or duplicate order |
