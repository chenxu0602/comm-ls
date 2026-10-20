# Metals Daily Targets: 2026-10-16

- Signal as-of date: 2026-10-15
- Target trading date: 2026-10-16
- AUM: $5,000.00
- Effective 2026-10-12: gap/accel/SCO-vol/copper/miners live weights = 15%/20%/25%/10%/25%; alloys remains suspended (5% cash). Earlier target sessions retain previous weights.
- This reweight is operator approved; signal rules, 12% name cap and legacy beta method are unchanged. Migration turnover must be separated from signal turnover.
- Gross stock weight: 30.00%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: -30.00%
- Gross hedge weight: 33.93%
- Total net weight after hedges: 3.93%
- Turnover from Metals-attributed current positions: 20.10%
- Full eligible order turnover: 18.15%
- Today's total child-order turnover: 17.13%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $2.14

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
| total_hedge | 0.339261 | 0.339261 | 1696.31 | 1696.31 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | miners | BHP | -0.075 | -4.5 | 82.9 | 0.5 | 0.5 | persistent_binary active; feature=0.0500696 |
| stock | miners | FSUGY | -0.05 | -11.9 | 20.99 | 0.5 | 0.3 | persistent_binary active; feature=0.0500696 |
| stock | miners | RIO | -0.05 | -2.8 | 90.21 | 0.3 | 0.5 | persistent_binary active; feature=0.0500696 |
| stock | copper_miner\|miners | SCCO | -0.1 | -2.5 | 201.69 | 0.7 | 0.9 | copper_energy_terms_of_trade active; hg_cl_ratio=0.719151;ho_ret=-0.0204785;hg_mv_5=0.7444;hg_mv_200=0.82471;hg_mv_diff=-0.08031;hg_threshold=0.00915922;ho_momentum_20d=-0.0166512;ho_threshold=0.0278831\|persistent_binary active; feature=0.0500696 |
| stock | miners | VALE | -0.025 | -9.6 | 13.02 | 0.2 | 0.5 | persistent_binary active; feature=0.0500696 |
| hedge | hedge | SPY | 0.154138 | 1 | 771.79 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | 0.185123 | 9.1 | 101.34 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | miners | BHP | BUY | 2 | 2 | 0.03316 | False | 82.9 | 82.69 | 83.11 | execute once; no same-day reversal or duplicate order |
| stock | miners | FSUGY | BUY | 3 | 3 | 0.012594 | False | 20.99 | 20.94 | 21.04 | execute once; no same-day reversal or duplicate order |
| stock | miners | RIO | BUY | 2 | 2 | 0.036084 | False | 90.21 | 89.98 | 90.44 | execute once; no same-day reversal or duplicate order |
| stock | miners | VALE | BUY | 11 | 11 | 0.028644 | False | 13.02 | 12.99 | 13.05 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XME | SELL | -3 | -3 | -0.060804 | False | 101.34 | 101.09 | 101.59 | single aggregate hedge order after confirming stock fills |

## Beta method for 2026-10-16 — as-of 2026-10-15

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-10-16-afm7wpl7/cached/targets-metals/2026-10-16. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
