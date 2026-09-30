# Metals Daily Targets: 2026-09-25

- Signal as-of date: 2026-09-24
- Target trading date: 2026-09-25
- AUM: $5,000.00
- Gross stock weight: 46.50%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: -46.50%
- Gross hedge weight: 49.96%
- Total net weight after hedges: 3.46%
- Turnover from Metals-attributed current positions: 92.43%
- Full eligible order turnover: 92.43%
- Today's total child-order turnover: 78.21%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $9.78

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
| total_hedge | 0.499634 | 0.499634 | 2498.17 | 2498.17 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | hg_gc_gap_gc_carry_iron\|miners | BHP | -0.12 | -7.1 | 85.09 | 0.6 | 0.5 | dual_feature_hysteresis active; gc_carry=2.18489; aggregate BHP capped at 12.0%\|persistent_binary active; ; aggregate BHP capped at 12.0% |
| stock | hg_gc_gap_gc_carry_iron\|miners | FSUGY | -0.07 | -14.9 | 23.44 | 0.6 | 0.3 | dual_feature_hysteresis active; gc_carry=2.18489\|persistent_binary active;  |
| stock | hg_gc_gap_gc_carry_iron\|miners | RIO | -0.11 | -5.8 | 94.47 | 0.3 | 0.5 | dual_feature_hysteresis active; gc_carry=2.18489\|persistent_binary active;  |
| stock | copper_miner\|miners | SCCO | -0.1 | -2.5 | 201.58 | 0.7 | 0.9 | copper_energy_terms_of_trade active; ho_ret=-0.0230538;hg_mv_5=0.816665;hg_mv_200=0.844742;hg_mv_diff=-0.0280764;hg_threshold=0.00750297;ho_momentum_20d=0.12758;ho_threshold=0.0304182\|persistent_binary active;  |
| stock | hg_gc_gap_gc_carry_iron\|miners | VALE | -0.065 | -24 | 13.56 | 0.2 | 0.5 | dual_feature_hysteresis active; gc_carry=2.18489\|persistent_binary active;  |
| hedge | hedge | SPY | 0.239612 | 1.6 | 767.18 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | 0.260023 | 12 | 107.96 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | copper_miner\|miners | SCCO | SELL | -1 | -1 | -0.040316 | False | 201.58 | 201.08 | 202.08 | execute once; no same-day reversal or duplicate order |
| stock | hg_gc_gap_gc_carry_iron\|miners | BHP | SELL | -7 | -6 | -0.102108 | False | 85.09 | 84.88 | 85.3 | execute once; no same-day reversal or duplicate order |
| stock | hg_gc_gap_gc_carry_iron\|miners | FSUGY | SELL | -15 | -15 | -0.07032 | False | 23.44 | 23.38 | 23.5 | execute once; no same-day reversal or duplicate order |
| stock | hg_gc_gap_gc_carry_iron\|miners | RIO | SELL | -6 | -6 | -0.113364 | False | 94.47 | 94.23 | 94.71 | execute once; no same-day reversal or duplicate order |
| stock | hg_gc_gap_gc_carry_iron\|miners | VALE | SELL | -24 | -24 | -0.065088 | False | 13.56 | 13.53 | 13.59 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | SPY | BUY | 2 | 1 | 0.153436 | False | 767.18 | 765.26 | 769.1 | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XME | BUY | 12 | 11 | 0.237512 | False | 107.96 | 107.69 | 108.23 | single aggregate hedge order after confirming stock fills |
