# Metals Daily Targets: 2026-10-02

- Signal as-of date: 2026-10-01
- Target trading date: 2026-10-02
- AUM: $5,000.00
- Gross stock weight: 46.50%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: -46.50%
- Gross hedge weight: 49.88%
- Total net weight after hedges: 3.38%
- Turnover from Metals-attributed current positions: 28.35%
- Full eligible order turnover: 28.13%
- Today's total child-order turnover: 37.83%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $4.73

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
| total_hedge | 0.49878 | 0.49878 | 2493.9 | 2493.9 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | hg_gc_gap_gc_carry_iron\|miners | BHP | -0.12 | -7.1 | 84.65 | 0.6 | 0.5 | dual_feature_hysteresis active; hg_gap=0.0347738;gc_carry=0.925017; aggregate BHP capped at 12.0%\|persistent_binary active; feature=0.0347738; aggregate BHP capped at 12.0% |
| stock | hg_gc_gap_gc_carry_iron\|miners | FSUGY | -0.07 | -15.5 | 22.59 | 0.6 | 0.3 | dual_feature_hysteresis active; hg_gap=0.0347738;gc_carry=0.925017\|persistent_binary active; feature=0.0347738 |
| stock | hg_gc_gap_gc_carry_iron\|miners | RIO | -0.11 | -5.9 | 92.87 | 0.3 | 0.5 | dual_feature_hysteresis active; hg_gap=0.0347738;gc_carry=0.925017\|persistent_binary active; feature=0.0347738 |
| stock | copper_miner\|miners | SCCO | -0.1 | -2.5 | 199.22 | 0.7 | 0.9 | copper_energy_terms_of_trade active; hg_cl_ratio=0.771354;ho_ret=-0.00988208;hg_mv_5=0.758603;hg_mv_200=0.835383;hg_mv_diff=-0.07678;hg_threshold=0.0105793;ho_momentum_20d=0.0341165;ho_threshold=0.0278237\|persistent_binary active; feature=0.0347738 |
| stock | hg_gc_gap_gc_carry_iron\|miners | VALE | -0.065 | -24.2 | 13.45 | 0.2 | 0.5 | dual_feature_hysteresis active; hg_gap=0.0347738;gc_carry=0.925017\|persistent_binary active; feature=0.0347738 |
| hedge | hedge | SPY | 0.239324 | 1.6 | 763.99 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | 0.259456 | 12.4 | 104.29 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | copper_miner\|miners | SCCO | SELL | -1 | -1 | -0.039844 | False | 199.22 | 198.72 | 199.72 | execute once; no same-day reversal or duplicate order |
| stock | hg_gc_gap_gc_carry_iron\|miners | BHP | SELL | -1 | -1 | -0.01693 | False | 84.65 | 84.44 | 84.86 | execute once; no same-day reversal or duplicate order |
| stock | hg_gc_gap_gc_carry_iron\|miners | RIO | SELL | -3 | -3 | -0.055722 | False | 92.87 | 92.64 | 93.1 | execute once; no same-day reversal or duplicate order |
| stock | hg_gc_gap_gc_carry_iron\|miners | VALE | SELL | -11 | -11 | -0.02959 | False | 13.45 | 13.42 | 13.48 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | SPY | BUY | 1 | 1 | 0.152798 | False | 763.99 | 762.08 | 765.9 | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XME | BUY | 3 | 4 | 0.083432 | False | 104.29 | 104.03 | 104.55 | single aggregate hedge order after confirming stock fills |
