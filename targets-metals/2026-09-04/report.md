# Metals Daily Targets: 2026-09-04

- Signal as-of date: 2026-09-03
- Target trading date: 2026-09-04
- AUM: $5,000.00
- Gross stock weight: 44.00%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: 44.00%
- Gross hedge weight: 46.10%
- Total net weight after hedges: -2.10%
- Turnover from Metals-attributed current positions: 13.65%
- Full eligible order turnover: 0.00%
- Today's total child-order turnover: 0.00%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $0.00

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
| total_hedge | 0.46103 | -0.46103 | 2305.15 | -2305.15 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | sco_specialty_alloys | ATI | 0.02 | 0.5 | 204.54 | 1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-0.360596;drawdown_63d=0.584602;realized_vol_63d=-0.351897 |
| stock | sco_vol_gc_hg_accel_miners\|miners | BHP | 0.12 | 6.5 | 92.71 | 0.6 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.36571;q_long_exit=2.19429;q_short_entry=2.19429;q_short_exit=1.43357;vol_diff=-0.0971428;accel=-0.0565848; aggregate BHP capped at 12.0%\|persistent_binary active; feature=-0.022762; aggregate BHP capped at 12.0% |
| stock | sco_specialty_alloys | CRS | 0.02 | 0.2 | 467.48 | 1.1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-0.360596;drawdown_63d=0.584602;realized_vol_63d=-0.351897 |
| stock | miners | FSUGY | 0.05 | 10.2 | 24.54 | 0.7 | 0.2 | persistent_binary active; feature=-0.022762 |
| stock | sco_specialty_alloys | HWM | 0.01 | 0.2 | 260.49 | 0.9 | 0.1 | sco_specialty_alloys_hysteresis active; ret_63d=-0.360596;drawdown_63d=0.584602;realized_vol_63d=-0.351897 |
| stock | sco_vol_gc_hg_accel_miners\|miners | RIO | 0.12 | 5.8 | 102.84 | 0.3 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.36571;q_long_exit=2.19429;q_short_entry=2.19429;q_short_exit=1.43357;vol_diff=-0.0971428;accel=-0.0565848; aggregate RIO capped at 12.0%\|persistent_binary active; feature=-0.022762; aggregate RIO capped at 12.0% |
| stock | sco_vol_gc_hg_accel_miners\|copper_miner\|miners | SCCO | 0.05 | 1.3 | 199.53 | 0.8 | 0.9 | sco_vol_gc_hg_combo active; sco_vol=1.36571;q_long_exit=2.19429;q_short_entry=2.19429;q_short_exit=1.43357;vol_diff=-0.0971428;accel=-0.0565848\|copper_energy_terms_of_trade active; hg_cl_ratio=0.850929;ho_ret=-0.0191041;hg_mv_5=0.840415;hg_mv_200=0.851052;hg_mv_diff=-0.0106373;hg_threshold=0.00703003;ho_momentum_20d=0.197858;ho_threshold=0.0301265\|persistent_binary active; feature=-0.022762 |
| stock | sco_vol_gc_hg_accel_miners\|miners | VALE | 0.05 | 16.3 | 15.31 | 0.2 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.36571;q_long_exit=2.19429;q_short_entry=2.19429;q_short_exit=1.43357;vol_diff=-0.0971428;accel=-0.0565848\|persistent_binary active; feature=-0.022762 |
| hedge | hedge | SPY | -0.247437 | -1.6 | 773.17 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | -0.213593 | -9 | 118.38 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

No trades above buffer.
