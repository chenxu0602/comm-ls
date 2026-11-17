# Metals Daily Targets: 2026-11-10

- Signal as-of date: 2026-11-09
- Target trading date: 2026-11-10
- AUM: $5,000.00
- Effective 2026-10-12: gap/accel/SCO-vol/copper/miners live weights = 15%/20%/25%/10%/25%; alloys remains suspended (5% cash). Earlier target sessions retain previous weights.
- This reweight is operator approved; signal rules, 12% name cap and legacy beta method are unchanged. Migration turnover must be separated from signal turnover.
- Gross stock weight: 47.00%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: 47.00%
- Gross hedge weight: 42.86%
- Total net weight after hedges: 4.14%
- Turnover from Metals-attributed current positions: 95.10%
- Full eligible order turnover: 95.10%
- Today's total child-order turnover: 69.61%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $8.70

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
| stock_long_without_hedge | 0.47 | 0.47 | 2350 | 2350 | 5 |
| stock_short_without_hedge | 0 | 0 | 0 | 0 | 0 |
| total_hedge | 0.428613 | -0.428613 | 2143.06 | -2143.06 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | hg_gc_gap_gc_carry_iron\|sco_vol_gc_hg_accel_miners\|miners | BHP | 0.12 | 7.24113 | 82.86 | 0.4 | 0.6 | dual_feature_hysteresis active; hg_gap=-0.0207631;gc_carry=-0.726849; aggregate BHP capped at 12.0%\|sco_vol_gc_hg_combo active; sco_vol=1.21429;q_long_exit=2.06429;q_short_entry=2.06429;q_short_exit=1.37329;vol_diff=-0.00214286;accel=1.37836; aggregate BHP capped at 12.0%\|persistent_binary active; feature=-0.0207631; aggregate BHP capped at 12.0% |
| stock | hg_gc_gap_gc_carry_iron\|miners | FSUGY | 0.065 | 15.2011 | 21.38 | 0.3 | 0.3 | dual_feature_hysteresis active; hg_gap=-0.0207631;gc_carry=-0.726849\|persistent_binary active; feature=-0.0207631 |
| stock | hg_gc_gap_gc_carry_iron\|sco_vol_gc_hg_accel_miners\|miners | RIO | 0.12 | 6.94525 | 86.39 | 0.2 | 0.5 | dual_feature_hysteresis active; hg_gap=-0.0207631;gc_carry=-0.726849; aggregate RIO capped at 12.0%\|sco_vol_gc_hg_combo active; sco_vol=1.21429;q_long_exit=2.06429;q_short_entry=2.06429;q_short_exit=1.37329;vol_diff=-0.00214286;accel=1.37836; aggregate RIO capped at 12.0%\|persistent_binary active; feature=-0.0207631; aggregate RIO capped at 12.0% |
| stock | sco_vol_gc_hg_accel_miners\|miners | SCCO | 0.09 | 2.55653 | 176.02 | 0.6 | 0.9 | sco_vol_gc_hg_combo active; sco_vol=1.21429;q_long_exit=2.06429;q_short_entry=2.06429;q_short_exit=1.37329;vol_diff=-0.00214286;accel=1.37836\|persistent_binary active; feature=-0.0207631 |
| stock | hg_gc_gap_gc_carry_iron\|sco_vol_gc_hg_accel_miners\|miners | VALE | 0.075 | 31.3283 | 11.97 | -0 | 0.6 | dual_feature_hysteresis active; hg_gap=-0.0207631;gc_carry=-0.726849\|sco_vol_gc_hg_combo active; sco_vol=1.21429;q_long_exit=2.06429;q_short_entry=2.06429;q_short_exit=1.37329;vol_diff=-0.00214286;accel=1.37836\|persistent_binary active; feature=-0.0207631 |
| hedge | hedge | SPY | -0.144867 | -0.962328 | 752.69 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | -0.283746 | -14.3916 | 98.58 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | hg_gc_gap_gc_carry_iron\|miners | FSUGY | BUY | 27 | 12 | 0.051312 | True | 21.38 | 21.33 | 21.43 | execute once; no same-day reversal or duplicate order |
| stock | hg_gc_gap_gc_carry_iron\|sco_vol_gc_hg_accel_miners\|miners | BHP | BUY | 7 | 5 | 0.08286 | False | 82.86 | 82.65 | 83.07 | execute once; no same-day reversal or duplicate order |
| stock | hg_gc_gap_gc_carry_iron\|sco_vol_gc_hg_accel_miners\|miners | RIO | BUY | 7 | 5 | 0.08639 | False | 86.39 | 86.17 | 86.61 | execute once; no same-day reversal or duplicate order |
| stock | hg_gc_gap_gc_carry_iron\|sco_vol_gc_hg_accel_miners\|miners | VALE | BUY | 31 | 24 | 0.057456 | False | 11.97 | 11.94 | 12 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners\|miners | SCCO | BUY | 3 | 2 | 0.070408 | False | 176.02 | 175.58 | 176.46 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | SPY | SELL | -1 | -1 | -0.150538 | False | 752.69 | 750.81 | 754.57 | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XME | SELL | -14 | -10 | -0.19716 | False | 98.58 | 98.33 | 98.83 | single aggregate hedge order after confirming stock fills |

## Beta method for 2026-11-10 — as-of 2026-11-09

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-11-10-y3z13i_u/cached/targets-metals/2026-11-10. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
