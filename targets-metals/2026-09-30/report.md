# Metals Daily Targets: 2026-09-30

- Signal as-of date: 2026-09-29
- Target trading date: 2026-09-30
- AUM: $5,000.00
- Gross stock weight: 46.50%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: -46.50%
- Gross hedge weight: 49.94%
- Total net weight after hedges: 3.44%
- Turnover from Metals-attributed current positions: 12.38%
- Full eligible order turnover: 9.72%
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
| stock_long_without_hedge | 0 | 0 | 0 | 0 | 0 |
| stock_short_without_hedge | 0.465 | -0.465 | 2325 | -2325 | 5 |
| total_hedge | 0.499406 | 0.499406 | 2497.03 | 2497.03 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | hg_gc_gap_gc_carry_iron\|miners | BHP | -0.12 | -7.1 | 84.82 | 0.6 | 0.5 | dual_feature_hysteresis active; hg_gap=0.038787;gc_carry=1.63593; aggregate BHP capped at 12.0%\|persistent_binary active; feature=0.038787; aggregate BHP capped at 12.0% |
| stock | hg_gc_gap_gc_carry_iron\|miners | FSUGY | -0.07 | -15.5 | 22.6 | 0.6 | 0.3 | dual_feature_hysteresis active; hg_gap=0.038787;gc_carry=1.63593\|persistent_binary active; feature=0.038787 |
| stock | hg_gc_gap_gc_carry_iron\|miners | RIO | -0.11 | -5.8 | 94.16 | 0.3 | 0.5 | dual_feature_hysteresis active; hg_gap=0.038787;gc_carry=1.63593\|persistent_binary active; feature=0.038787 |
| stock | copper_miner\|miners | SCCO | -0.1 | -2.5 | 202.55 | 0.7 | 0.9 | copper_energy_terms_of_trade active; hg_cl_ratio=0.79637;ho_ret=0.00326475;hg_mv_5=0.807972;hg_mv_200=0.842778;hg_mv_diff=-0.0348059;hg_threshold=0.00714554;ho_momentum_20d=0.0615612;ho_threshold=0.0301971\|persistent_binary active; feature=0.038787 |
| stock | hg_gc_gap_gc_carry_iron\|miners | VALE | -0.065 | -24.4 | 13.3 | 0.2 | 0.5 | dual_feature_hysteresis active; hg_gap=0.038787;gc_carry=1.63593\|persistent_binary active; feature=0.038787 |
| hedge | hedge | SPY | 0.239344 | 1.6 | 764.2 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | 0.260062 | 12.5 | 103.9 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

No trades above buffer.
