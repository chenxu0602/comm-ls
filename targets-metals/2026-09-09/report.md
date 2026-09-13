# Metals Daily Targets: 2026-09-09

- Signal as-of date: 2026-09-08
- Target trading date: 2026-09-09
- AUM: $5,000.00
- Gross stock weight: 41.50%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: 41.50%
- Gross hedge weight: 39.50%
- Total net weight after hedges: 2.00%
- Turnover from Metals-attributed current positions: 30.15%
- Full eligible order turnover: 25.15%
- Today's total child-order turnover: 34.20%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $4.27

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
| stock_long_without_hedge | 0.415 | 0.415 | 2075 | 2075 | 7 |
| stock_short_without_hedge | 0 | 0 | 0 | 0 | 0 |
| total_hedge | 0.395024 | -0.395024 | 1975.12 | -1975.12 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | sco_specialty_alloys | ATI | 0.02 | 0.5 | 207.32 | 1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-0.231616;drawdown_63d=1.0312;realized_vol_63d=-0.3063 |
| stock | hg_gc_gap_gc_carry_iron\|miners | BHP | 0.12 | 6.5 | 91.99 | 0.6 | 0.5 | dual_feature_hysteresis active; hg_gap=-0.011851;gc_carry=-0.0869472; aggregate BHP capped at 12.0%\|persistent_binary active; feature=-0.011851; aggregate BHP capped at 12.0% |
| stock | sco_specialty_alloys | CRS | 0.02 | 0.2 | 458.56 | 1.1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-0.231616;drawdown_63d=1.0312;realized_vol_63d=-0.3063 |
| stock | hg_gc_gap_gc_carry_iron\|miners | FSUGY | 0.07 | 13.7 | 25.46 | 0.6 | 0.3 | dual_feature_hysteresis active; hg_gap=-0.011851;gc_carry=-0.0869472\|persistent_binary active; feature=-0.011851 |
| stock | sco_specialty_alloys | HWM | 0.01 | 0.2 | 231.53 | 1 | 0.1 | sco_specialty_alloys_hysteresis active; ret_63d=-0.231616;drawdown_63d=1.0312;realized_vol_63d=-0.3063 |
| stock | hg_gc_gap_gc_carry_iron\|miners | RIO | 0.11 | 5.3 | 103.83 | 0.3 | 0.5 | dual_feature_hysteresis active; hg_gap=-0.011851;gc_carry=-0.0869472\|persistent_binary active; feature=-0.011851 |
| stock | hg_gc_gap_gc_carry_iron\|miners | VALE | 0.065 | 20.9 | 15.56 | 0.2 | 0.5 | dual_feature_hysteresis active; hg_gap=-0.011851;gc_carry=-0.0869472\|persistent_binary active; feature=-0.011851 |
| hedge | hedge | SPY | -0.216737 | -1.4 | 765.96 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | -0.178287 | -7.4 | 119.95 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | copper_miner\|miners | SCCO | SELL | -1 | -1 | -0.041712 | False | 208.56 | 208.04 | 209.08 | execute once; no same-day reversal or duplicate order |
| stock | hg_gc_gap_gc_carry_iron\|miners | BHP | BUY | 1 | 1 | 0.018398 | False | 91.99 | 91.76 | 92.22 | execute once; no same-day reversal or duplicate order |
| stock | hg_gc_gap_gc_carry_iron\|miners | FSUGY | BUY | 4 | 4 | 0.020368 | False | 25.46 | 25.4 | 25.52 | execute once; no same-day reversal or duplicate order |
| stock | hg_gc_gap_gc_carry_iron\|miners | RIO | SELL | -1 | -1 | -0.020766 | False | 103.83 | 103.57 | 104.09 | execute once; no same-day reversal or duplicate order |
| stock | hg_gc_gap_gc_carry_iron\|miners | VALE | BUY | 5 | 5 | 0.01556 | False | 15.56 | 15.52 | 15.6 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | SPY | BUY | 1 | 1 | 0.153192 | False | 765.96 | 764.05 | 767.87 | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XME | BUY | 3 | 3 | 0.07197 | False | 119.95 | 119.65 | 120.25 | single aggregate hedge order after confirming stock fills |
