# Metals Daily Targets: 2026-10-06

- Signal as-of date: 2026-10-05
- Target trading date: 2026-10-06
- AUM: $5,000.00
- Gross stock weight: 46.50%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: -46.50%
- Gross hedge weight: 49.89%
- Total net weight after hedges: 3.39%
- Turnover from Metals-attributed current positions: 10.20%
- Full eligible order turnover: 0.29%
- Today's total child-order turnover: 17.93%
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
| stock_long_without_hedge | 0 | 0 | 0 | 0 | 0 |
| stock_short_without_hedge | 0.465 | -0.465 | 2325 | -2325 | 5 |
| total_hedge | 0.498902 | 0.498902 | 2494.51 | 2494.51 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | hg_gc_gap_gc_carry_iron\|miners | BHP | -0.12 | -6.9 | 86.83 | 0.6 | 0.5 | dual_feature_hysteresis active; hg_gap=0.0359531;gc_carry=1.21863; aggregate BHP capped at 12.0%\|persistent_binary active; feature=0.0359531; aggregate BHP capped at 12.0% |
| stock | hg_gc_gap_gc_carry_iron\|miners | FSUGY | -0.07 | -15.5 | 22.64 | 0.6 | 0.3 | dual_feature_hysteresis active; hg_gap=0.0359531;gc_carry=1.21863\|persistent_binary active; feature=0.0359531 |
| stock | hg_gc_gap_gc_carry_iron\|miners | RIO | -0.11 | -5.8 | 95.65 | 0.3 | 0.5 | dual_feature_hysteresis active; hg_gap=0.0359531;gc_carry=1.21863\|persistent_binary active; feature=0.0359531 |
| stock | copper_miner\|miners | SCCO | -0.1 | -2.4 | 205.29 | 0.7 | 0.9 | copper_energy_terms_of_trade active; hg_cl_ratio=0.78157;ho_ret=0.00974992;hg_mv_5=0.767982;hg_mv_200=0.833534;hg_mv_diff=-0.0655517;hg_threshold=0.0100982;ho_momentum_20d=0.04384;ho_threshold=0.0279348\|persistent_binary active; feature=0.0359531 |
| stock | hg_gc_gap_gc_carry_iron\|miners | VALE | -0.065 | -23 | 14.15 | 0.2 | 0.5 | dual_feature_hysteresis active; hg_gap=0.0359531;gc_carry=1.21863\|persistent_binary active; feature=0.0359531 |
| hedge | hedge | SPY | 0.238708 | 1.5 | 774.83 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | 0.260194 | 12.1 | 107.76 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | hg_gc_gap_gc_carry_iron\|miners | VALE | BUY | 1 | 1 | 0.00283 | False | 14.15 | 14.11 | 14.19 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | SPY | SELL | 0 | -1 | -0.154966 | False | 774.83 | 772.89 | 776.77 | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XME | SELL | 0 | -1 | -0.021552 | False | 107.76 | 107.49 | 108.03 | single aggregate hedge order after confirming stock fills |
