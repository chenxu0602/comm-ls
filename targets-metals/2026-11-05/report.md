# Metals Daily Targets: 2026-11-05

- Signal as-of date: 2026-11-04
- Target trading date: 2026-11-05
- AUM: $5,000.00
- Effective 2026-10-12: gap/accel/SCO-vol/copper/miners live weights = 15%/20%/25%/10%/25%; alloys remains suspended (5% cash). Earlier target sessions retain previous weights.
- This reweight is operator approved; signal rules, 12% name cap and legacy beta method are unchanged. Migration turnover must be separated from signal turnover.
- Gross stock weight: 27.50%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: -27.50%
- Gross hedge weight: 30.15%
- Total net weight after hedges: 2.65%
- Turnover from Metals-attributed current positions: 10.27%
- Full eligible order turnover: 7.05%
- Today's total child-order turnover: 7.37%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $0.92

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
| stock_short_without_hedge | 0.275 | -0.275 | 1375 | -1375 | 5 |
| total_hedge | 0.301456 | 0.301456 | 1507.28 | 1507.28 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | miners | BHP | -0.075 | -4.67931 | 80.14 | 0.5 | 0.6 | persistent_binary active; feature=0.0376234 |
| stock | miners | FSUGY | -0.05 | -12.4008 | 20.16 | 0.5 | 0.3 | persistent_binary active; feature=0.0376234 |
| stock | miners | RIO | -0.05 | -2.95648 | 84.56 | 0.3 | 0.5 | persistent_binary active; feature=0.0376234 |
| stock | copper_miner\|miners | SCCO | -0.075 | -2.12056 | 176.84 | 0.7 | 1 | copper_energy_terms_of_trade active; hg_cl_ratio=0.762905;ho_ret=-0.0744612;hg_mv_5=0.696124;hg_mv_200=0.799077;hg_mv_diff=-0.102953;hg_threshold=0.0106543;ho_momentum_20d=-0.0652818;ho_threshold=0.0269856\|persistent_binary active; feature=0.0376234 |
| stock | miners | VALE | -0.025 | -10.9361 | 11.43 | 0.1 | 0.5 | persistent_binary active; feature=0.0376234 |
| hedge | hedge | SPY | 0.128993 | 0.841102 | 766.81 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | 0.172463 | 9.0031 | 95.78 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | copper_miner\|miners | SCCO | BUY | 1 | 1 | 0.035368 | False | 176.84 | 176.4 | 177.28 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XME | SELL | -2 | -2 | -0.038312 | False | 95.78 | 95.54 | 96.02 | single aggregate hedge order after confirming stock fills |

## Beta method for 2026-11-05 — as-of 2026-11-04

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-11-05-4_s52ks6/cached/targets-metals/2026-11-05. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
