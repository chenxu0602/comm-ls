# Metals Daily Targets: 2026-10-14

- Signal as-of date: 2026-10-13
- Target trading date: 2026-10-14
- AUM: $5,000.00
- Effective 2026-10-12: gap/accel/SCO-vol/copper/miners live weights = 15%/20%/25%/10%/25%; alloys remains suspended (5% cash). Earlier target sessions retain previous weights.
- This reweight is operator approved; signal rules, 12% name cap and legacy beta method are unchanged. Migration turnover must be separated from signal turnover.
- Gross stock weight: 43.50%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: -43.50%
- Gross hedge weight: 45.78%
- Total net weight after hedges: 2.28%
- Turnover from Metals-attributed current positions: 9.70%
- Full eligible order turnover: 2.35%
- Today's total child-order turnover: 0.00%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $0.00

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
| stock_short_without_hedge | 0.435 | -0.435 | 2175 | -2175 | 5 |
| total_hedge | 0.457786 | 0.457786 | 2288.93 | 2288.93 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | hg_gc_gap_gc_carry_iron\|miners | BHP | -0.12 | -7.1 | 84.95 | 0.5 | 0.5 | dual_feature_hysteresis active; hg_gap=0.0509086;gc_carry=0.547391; aggregate BHP capped at 12.0%\|persistent_binary active; feature=0.0509086; aggregate BHP capped at 12.0% |
| stock | hg_gc_gap_gc_carry_iron\|miners | FSUGY | -0.065 | -15.2 | 21.35 | 0.5 | 0.3 | dual_feature_hysteresis active; hg_gap=0.0509086;gc_carry=0.547391\|persistent_binary active; feature=0.0509086 |
| stock | hg_gc_gap_gc_carry_iron\|miners | RIO | -0.095 | -5.1 | 93.06 | 0.3 | 0.5 | dual_feature_hysteresis active; hg_gap=0.0509086;gc_carry=0.547391\|persistent_binary active; feature=0.0509086 |
| stock | copper_miner\|miners | SCCO | -0.1 | -2.4 | 207.42 | 0.7 | 0.9 | copper_energy_terms_of_trade active; hg_cl_ratio=0.746918;ho_ret=0.0437446;hg_mv_5=0.759149;hg_mv_200=0.827422;hg_mv_diff=-0.0682734;hg_threshold=0.00919037;ho_momentum_20d=-0.0152048;ho_threshold=0.0276781\|persistent_binary active; feature=0.0509086 |
| stock | hg_gc_gap_gc_carry_iron\|miners | VALE | -0.055 | -20.6 | 13.37 | 0.2 | 0.5 | dual_feature_hysteresis active; hg_gap=0.0509086;gc_carry=0.547391\|persistent_binary active; feature=0.0509086 |
| hedge | hedge | SPY | 0.206013 | 1.3 | 778.01 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | 0.251772 | 12.1 | 103.76 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

No trades above buffer.

## Beta method for 2026-10-14 — as-of 2026-10-13

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-10-14-kibydwm3/cached/targets-metals/2026-10-14. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
