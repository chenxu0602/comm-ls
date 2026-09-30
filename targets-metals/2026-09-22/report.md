# Metals Daily Targets: 2026-09-22

- Signal as-of date: 2026-09-21
- Target trading date: 2026-09-22
- AUM: $5,000.00
- Gross stock weight: 45.00%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: 45.00%
- Gross hedge weight: 46.46%
- Total net weight after hedges: -1.46%
- Turnover from Metals-attributed current positions: 7.80%
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
| stock_long_without_hedge | 0.45 | 0.45 | 2250 | 2250 | 5 |
| stock_short_without_hedge | 0 | 0 | 0 | 0 | 0 |
| total_hedge | 0.46457 | -0.46457 | 2322.85 | -2322.85 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | BHP | 0.12 | 7 | 86.09 | 0.6 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.36143;q_long_exit=2.16614;q_short_entry=2.16614;q_short_exit=1.414;vol_diff=-0.0121429;accel=-0.880206; aggregate BHP capped at 12.0%\|sco_vol_regime_pulse active; sco_vol=1.36143;vol_quantile=1.98743;vol_diff=-0.0121429; aggregate BHP capped at 12.0%\|persistent_binary active; feature=0.00369094; aggregate BHP capped at 12.0% |
| stock | miners | FSUGY | 0.05 | 10.5 | 23.76 | 0.6 | 0.3 | persistent_binary active; feature=0.00369094 |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | RIO | 0.12 | 6.2 | 97.04 | 0.3 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.36143;q_long_exit=2.16614;q_short_entry=2.16614;q_short_exit=1.414;vol_diff=-0.0121429;accel=-0.880206; aggregate RIO capped at 12.0%\|sco_vol_regime_pulse active; sco_vol=1.36143;vol_quantile=1.98743;vol_diff=-0.0121429; aggregate RIO capped at 12.0%\|persistent_binary active; feature=0.00369094; aggregate RIO capped at 12.0% |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|copper_miner\|miners | SCCO | 0.08 | 2 | 198.06 | 0.7 | 0.9 | sco_vol_gc_hg_combo active; sco_vol=1.36143;q_long_exit=2.16614;q_short_entry=2.16614;q_short_exit=1.414;vol_diff=-0.0121429;accel=-0.880206\|sco_vol_regime_pulse active; sco_vol=1.36143;vol_quantile=1.98743;vol_diff=-0.0121429\|copper_energy_terms_of_trade active; hg_cl_ratio=0.821489;ho_ret=-0.0286664;hg_mv_5=0.793184;hg_mv_200=0.84607;hg_mv_diff=-0.0528858;hg_threshold=0.00775399;ho_momentum_20d=0.110288;ho_threshold=0.0304056\|persistent_binary active; feature=0.00369094 |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | VALE | 0.08 | 28.3 | 14.15 | 0.2 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.36143;q_long_exit=2.16614;q_short_entry=2.16614;q_short_exit=1.414;vol_diff=-0.0121429;accel=-0.880206\|sco_vol_regime_pulse active; sco_vol=1.36143;vol_quantile=1.98743;vol_diff=-0.0121429\|persistent_binary active; feature=0.00369094 |
| hedge | hedge | SPY | -0.215002 | -1.4 | 773.5 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | -0.249569 | -11.4 | 109 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

No trades above buffer.
