# Metals Daily Targets: 2026-10-09

- Signal as-of date: 2026-10-08
- Target trading date: 2026-10-09
- AUM: $5,000.00
- Gross stock weight: 46.50%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: -46.50%
- Gross hedge weight: 49.44%
- Total net weight after hedges: 2.94%
- Turnover from Metals-attributed current positions: 11.74%
- Full eligible order turnover: 3.62%
- Today's total child-order turnover: 21.98%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $2.75

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
| total_hedge | 0.494367 | 0.494367 | 2471.83 | 2471.83 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | hg_gc_gap_gc_carry_iron\|miners | BHP | -0.12 | -7.1 | 84.83 | 0.6 | 0.5 | dual_feature_hysteresis active; hg_gap=0.0445274;gc_carry=1.07036; aggregate BHP capped at 12.0%\|persistent_binary active; feature=0.0445274; aggregate BHP capped at 12.0% |
| stock | hg_gc_gap_gc_carry_iron\|miners | FSUGY | -0.07 | -15.9 | 22 | 0.6 | 0.3 | dual_feature_hysteresis active; hg_gap=0.0445274;gc_carry=1.07036\|persistent_binary active; feature=0.0445274 |
| stock | hg_gc_gap_gc_carry_iron\|miners | RIO | -0.11 | -5.9 | 93.34 | 0.3 | 0.5 | dual_feature_hysteresis active; hg_gap=0.0445274;gc_carry=1.07036\|persistent_binary active; feature=0.0445274 |
| stock | copper_miner\|miners | SCCO | -0.1 | -2.5 | 198.66 | 0.7 | 0.9 | copper_energy_terms_of_trade active; hg_cl_ratio=0.749914;ho_ret=0.0547604;hg_mv_5=0.773578;hg_mv_200=0.830483;hg_mv_diff=-0.0569045;hg_threshold=0.00948679;ho_momentum_20d=0.00760633;ho_threshold=0.026901\|persistent_binary active; feature=0.0445274 |
| stock | hg_gc_gap_gc_carry_iron\|miners | VALE | -0.065 | -24.2 | 13.42 | 0.2 | 0.5 | dual_feature_hysteresis active; hg_gap=0.0445274;gc_carry=1.07036\|persistent_binary active; feature=0.0445274 |
| hedge | hedge | SPY | 0.231678 | 1.5 | 773.93 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | 0.262689 | 12.6 | 104.61 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | copper_miner\|miners | SCCO | SELL | -1 | -1 | -0.039732 | False | 198.66 | 198.16 | 199.16 | execute once; no same-day reversal or duplicate order |
| stock | hg_gc_gap_gc_carry_iron\|miners | FSUGY | SELL | -1 | -1 | -0.0044 | False | 22 | 21.94 | 22.06 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | SPY | BUY | 0 | 1 | 0.154786 | False | 773.93 | 772 | 775.86 | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XME | BUY | 1 | 1 | 0.020922 | False | 104.61 | 104.35 | 104.87 | single aggregate hedge order after confirming stock fills |

## Operator beta decision — 2026-10-09

Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-10-09-31i2mpxo/cached/targets-metals/2026-10-09. Agriculture's existing component-specific cached beta is unchanged.
