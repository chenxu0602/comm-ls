# Metals Daily Targets: 2026-09-24

- Signal as-of date: 2026-09-23
- Target trading date: 2026-09-24
- AUM: $5,000.00
- Gross stock weight: 30.00%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: -30.00%
- Gross hedge weight: 35.28%
- Total net weight after hedges: 5.28%
- Turnover from Metals-attributed current positions: 118.31%
- Full eligible order turnover: 118.31%
- Today's total child-order turnover: 57.07%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $7.13

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
| stock_short_without_hedge | 0.3 | -0.3 | 1500 | -1500 | 5 |
| total_hedge | 0.352809 | 0.352809 | 1764.05 | 1764.05 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | miners | BHP | -0.075 | -4.4 | 84.95 | 0.6 | 0.5 | persistent_binary active; feature=0.0250978 |
| stock | miners | FSUGY | -0.05 | -10.7 | 23.39 | 0.6 | 0.3 | persistent_binary active; feature=0.0250978 |
| stock | miners | RIO | -0.05 | -2.6 | 95.25 | 0.3 | 0.5 | persistent_binary active; feature=0.0250978 |
| stock | copper_miner\|miners | SCCO | -0.1 | -2.5 | 201.94 | 0.7 | 0.9 | copper_energy_terms_of_trade active; hg_cl_ratio=0.812598;ho_ret=-0.0273546;hg_mv_5=0.813522;hg_mv_200=0.84512;hg_mv_diff=-0.0315981;hg_threshold=0.00757702;ho_momentum_20d=0.151696;ho_threshold=0.0301663\|persistent_binary active; feature=0.0250978 |
| stock | miners | VALE | -0.025 | -9 | 13.82 | 0.2 | 0.5 | persistent_binary active; feature=0.0250978 |
| hedge | hedge | SPY | 0.171887 | 1.1 | 767.81 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | 0.180922 | 8.3 | 109.58 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | copper_miner\|miners | SCCO | SELL | -2 | -1 | -0.040388 | False | 201.94 | 201.44 | 202.44 | execute once; no same-day reversal or duplicate order |
| stock | miners | BHP | SELL | -8 | -4 | -0.06796 | True | 84.95 | 84.74 | 85.16 | execute once; no same-day reversal or duplicate order |
| stock | miners | FSUGY | SELL | -22 | -11 | -0.051458 | True | 23.39 | 23.33 | 23.45 | execute once; no same-day reversal or duplicate order |
| stock | miners | RIO | SELL | -6 | -3 | -0.05715 | True | 95.25 | 95.01 | 95.49 | execute once; no same-day reversal or duplicate order |
| stock | miners | VALE | SELL | -18 | -9 | -0.024876 | True | 13.82 | 13.79 | 13.85 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | SPY | BUY | 2 | 1 | 0.153562 | False | 767.81 | 765.89 | 769.73 | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XME | BUY | 16 | 8 | 0.175328 | True | 109.58 | 109.31 | 109.85 | single aggregate hedge order after confirming stock fills |
