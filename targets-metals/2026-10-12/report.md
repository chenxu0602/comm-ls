# Metals Daily Targets: 2026-10-12

- Signal as-of date: 2026-10-09
- Target trading date: 2026-10-12
- AUM: $5,000.00
- Effective 2026-10-12: gap/accel/SCO-vol/copper/miners live weights = 15%/20%/25%/10%/25%; alloys remains suspended (5% cash). Earlier target sessions retain previous weights.
- This reweight is operator approved; signal rules, 12% name cap and legacy beta method are unchanged. Migration turnover must be separated from signal turnover.
- Gross stock weight: 43.50%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: -43.50%
- Gross hedge weight: 47.16%
- Total net weight after hedges: 3.66%
- Turnover from Metals-attributed current positions: 17.28%
- Full eligible order turnover: 17.04%
- Today's total child-order turnover: 26.99%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $3.37

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
| total_hedge | 0.471645 | 0.471645 | 2358.22 | 2358.22 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | hg_gc_gap_gc_carry_iron\|miners | BHP | -0.12 | -6.9 | 86.74 | 0.6 | 0.5 | dual_feature_hysteresis active; hg_gap=0.0440818;gc_carry=0.720587; aggregate BHP capped at 12.0%\|persistent_binary active; feature=0.0440818; aggregate BHP capped at 12.0% |
| stock | hg_gc_gap_gc_carry_iron\|miners | FSUGY | -0.065 | -14.8 | 22 | 0.6 | 0.3 | dual_feature_hysteresis active; hg_gap=0.0440818;gc_carry=0.720587\|persistent_binary active; feature=0.0440818 |
| stock | hg_gc_gap_gc_carry_iron\|miners | RIO | -0.095 | -5 | 94.78 | 0.3 | 0.5 | dual_feature_hysteresis active; hg_gap=0.0440818;gc_carry=0.720587\|persistent_binary active; feature=0.0440818 |
| stock | copper_miner\|miners | SCCO | -0.1 | -2.4 | 209.21 | 0.7 | 0.9 | copper_energy_terms_of_trade active; hg_cl_ratio=0.763665;ho_ret=-0.0300398;hg_mv_5=0.771653;hg_mv_200=0.829525;hg_mv_diff=-0.057872;hg_threshold=0.00935862;ho_momentum_20d=-0.00629031;ho_threshold=0.0272167\|persistent_binary active; feature=0.0440818 |
| stock | hg_gc_gap_gc_carry_iron\|miners | VALE | -0.055 | -20.2 | 13.62 | 0.2 | 0.5 | dual_feature_hysteresis active; hg_gap=0.0440818;gc_carry=0.720587\|persistent_binary active; feature=0.0440818 |
| hedge | hedge | SPY | 0.222485 | 1.4 | 778.57 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | 0.24916 | 11.7 | 106.35 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | copper_miner\|miners | SCCO | BUY | 1 | 1 | 0.041842 | False | 209.21 | 208.69 | 209.73 | execute once; no same-day reversal or duplicate order |
| stock | hg_gc_gap_gc_carry_iron\|miners | RIO | BUY | 1 | 1 | 0.018956 | False | 94.78 | 94.54 | 95.02 | execute once; no same-day reversal or duplicate order |
| stock | hg_gc_gap_gc_carry_iron\|miners | VALE | BUY | 4 | 4 | 0.010896 | False | 13.62 | 13.59 | 13.65 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | SPY | SELL | -1 | -1 | -0.155714 | False | 778.57 | 776.62 | 780.52 | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XME | SELL | -1 | -2 | -0.04254 | False | 106.35 | 106.08 | 106.62 | single aggregate hedge order after confirming stock fills |

## Operator beta decision — 2026-10-09

Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Cached research comparison FAILED and is not validated; no stock-invariance comparison is available. Legacy generation completed its normal validation independently. Research failure: Command '['uv', 'run', 'python', '/Users/chenxu/Work/comm-ls/scripts/generate_metals_cached_beta_daily_targets.py', '--aum', '5000', '--as-of', '2026-10-09', '--target-date', '2026-10-12', '--current-positions', '/Users/chenxu/Work/comm-ls/stats/2026-10-09/metals_positions_attributed.csv', '--output-dir', '/var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-10-12-rn3jt1yc/cached/targets-metals']' returned non-zero exit status 1.. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-10-12-rn3jt1yc/cached/targets-metals/2026-10-12. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
