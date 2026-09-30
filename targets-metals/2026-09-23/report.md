# Metals Daily Targets: 2026-09-23

- Signal as-of date: 2026-09-22
- Target trading date: 2026-09-23
- AUM: $5,000.00
- Gross stock weight: 20.00%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: 20.00%
- Gross hedge weight: 18.61%
- Total net weight after hedges: 1.39%
- Turnover from Metals-attributed current positions: 46.39%
- Full eligible order turnover: 40.18%
- Today's total child-order turnover: 40.13%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $5.02

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
| stock_long_without_hedge | 0.2 | 0.2 | 1000 | 1000 | 4 |
| stock_short_without_hedge | 0 | 0 | 0 | 0 | 0 |
| total_hedge | 0.186128 | -0.186128 | 930.64 | -930.64 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | miners | BHP | 0.075 | 4.3 | 87.81 | 0.6 | 0.5 | persistent_binary active; feature=0.0140668 |
| stock | miners | FSUGY | 0.05 | 10.5 | 23.76 | 0.6 | 0.3 | persistent_binary active; feature=0.0140668 |
| stock | miners | RIO | 0.05 | 2.6 | 97.42 | 0.3 | 0.5 | persistent_binary active; feature=0.0140668 |
| stock | miners | VALE | 0.025 | 8.8 | 14.2 | 0.2 | 0.5 | persistent_binary active; feature=0.0140668 |
| hedge | hedge | SPY | -0.094533 | -0.6 | 771.39 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | -0.091595 | -4.2 | 109.81 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | copper_miner\|miners | SCCO | SELL | -2 | -2 | -0.082472 | False | 206.18 | 205.66 | 206.7 | execute once; no same-day reversal or duplicate order |
| stock | miners | BHP | SELL | -3 | -3 | -0.052686 | False | 87.81 | 87.59 | 88.03 | execute once; no same-day reversal or duplicate order |
| stock | miners | RIO | SELL | -3 | -3 | -0.058452 | False | 97.42 | 97.18 | 97.66 | execute once; no same-day reversal or duplicate order |
| stock | miners | VALE | SELL | -19 | -19 | -0.053979 | False | 14.2 | 14.17 | 14.24 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XME | BUY | 7 | 7 | 0.153732 | False | 109.81 | 109.53 | 110.08 | single aggregate hedge order after confirming stock fills |
