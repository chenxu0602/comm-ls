# Metals Daily Targets: 2026-10-05

- Signal as-of date: 2026-10-02
- Target trading date: 2026-10-05
- AUM: $5,000.00
- Gross stock weight: 46.50%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: -46.50%
- Gross hedge weight: 49.98%
- Total net weight after hedges: 3.48%
- Turnover from Metals-attributed current positions: 10.44%
- Full eligible order turnover: 2.33%
- Today's total child-order turnover: 19.50%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $2.44

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
| total_hedge | 0.499832 | 0.499832 | 2499.16 | 2499.16 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | hg_gc_gap_gc_carry_iron\|miners | BHP | -0.12 | -7 | 86.07 | 0.6 | 0.5 | dual_feature_hysteresis active; hg_gap=0.0331615;gc_carry=1.4214; aggregate BHP capped at 12.0%\|persistent_binary active; feature=0.0331615; aggregate BHP capped at 12.0% |
| stock | hg_gc_gap_gc_carry_iron\|miners | FSUGY | -0.07 | -15.5 | 22.61 | 0.6 | 0.3 | dual_feature_hysteresis active; hg_gap=0.0331615;gc_carry=1.4214\|persistent_binary active; feature=0.0331615 |
| stock | hg_gc_gap_gc_carry_iron\|miners | RIO | -0.11 | -5.8 | 94.21 | 0.3 | 0.5 | dual_feature_hysteresis active; hg_gap=0.0331615;gc_carry=1.4214\|persistent_binary active; feature=0.0331615 |
| stock | copper_miner\|miners | SCCO | -0.1 | -2.4 | 205.54 | 0.7 | 0.9 | copper_energy_terms_of_trade active; hg_cl_ratio=0.773291;ho_ret=-0.0308235;hg_mv_5=0.760719;hg_mv_200=0.834475;hg_mv_diff=-0.0737561;hg_threshold=0.0103564;ho_momentum_20d=0.0223971;ho_threshold=0.0279644\|persistent_binary active; feature=0.0331615 |
| stock | hg_gc_gap_gc_carry_iron\|miners | VALE | -0.065 | -23.6 | 13.76 | 0.2 | 0.5 | dual_feature_hysteresis active; hg_gap=0.0331615;gc_carry=1.4214\|persistent_binary active; feature=0.0331615 |
| hedge | hedge | SPY | 0.239796 | 1.6 | 769.64 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | 0.260036 | 12.3 | 105.74 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | copper_miner\|miners | SCCO | BUY | 1 | 1 | 0.041108 | False | 205.54 | 205.03 | 206.05 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | SPY | SELL | 0 | -1 | -0.153928 | False | 769.64 | 767.72 | 771.56 | single aggregate hedge order after confirming stock fills |
