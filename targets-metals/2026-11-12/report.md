# Metals Daily Targets: 2026-11-12

- Signal as-of date: 2026-11-11
- Target trading date: 2026-11-12
- AUM: $5,000.00
- Effective 2026-10-12: gap/accel/SCO-vol/copper/miners live weights = 15%/20%/25%/10%/25%; alloys remains suspended (5% cash). Earlier target sessions retain previous weights.
- This reweight is operator approved; signal rules, 12% name cap and legacy beta method are unchanged. Migration turnover must be separated from signal turnover.
- Gross stock weight: 54.50%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: 54.50%
- Gross hedge weight: 49.88%
- Total net weight after hedges: 4.62%
- Turnover from Metals-attributed current positions: 10.27%
- Full eligible order turnover: 8.31%
- Today's total child-order turnover: 11.69%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $1.46

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
| stock_long_without_hedge | 0.545 | 0.545 | 2725 | 2725 | 5 |
| stock_short_without_hedge | 0 | 0 | 0 | 0 | 0 |
| total_hedge | 0.498792 | -0.498792 | 2493.96 | -2493.96 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | hg_gc_gap_gc_carry_iron\|sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | BHP | 0.12 | 7.31172 | 82.06 | 0.4 | 0.6 | dual_feature_hysteresis active; hg_gap=-0.00848041;gc_carry=-0.155093; aggregate BHP capped at 12.0%\|sco_vol_gc_hg_combo active; sco_vol=1.20357;q_long_exit=2.05643;q_short_entry=2.05643;q_short_exit=1.37143;vol_diff=-0.00928571;accel=1.0805; aggregate BHP capped at 12.0%\|sco_vol_regime_pulse active; sco_vol=1.20357;vol_quantile=1.83807;vol_diff=-0.00928571; aggregate BHP capped at 12.0%\|persistent_binary active; feature=-0.00848041; aggregate BHP capped at 12.0% |
| stock | hg_gc_gap_gc_carry_iron\|miners | FSUGY | 0.065 | 15.4983 | 20.97 | 0.3 | 0.3 | dual_feature_hysteresis active; hg_gap=-0.00848041;gc_carry=-0.155093\|persistent_binary active; feature=-0.00848041 |
| stock | hg_gc_gap_gc_carry_iron\|sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | RIO | 0.12 | 7.06132 | 84.97 | 0.2 | 0.5 | dual_feature_hysteresis active; hg_gap=-0.00848041;gc_carry=-0.155093; aggregate RIO capped at 12.0%\|sco_vol_gc_hg_combo active; sco_vol=1.20357;q_long_exit=2.05643;q_short_entry=2.05643;q_short_exit=1.37143;vol_diff=-0.00928571;accel=1.0805; aggregate RIO capped at 12.0%\|sco_vol_regime_pulse active; sco_vol=1.20357;vol_quantile=1.83807;vol_diff=-0.00928571; aggregate RIO capped at 12.0%\|persistent_binary active; feature=-0.00848041; aggregate RIO capped at 12.0% |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | SCCO | 0.12 | 3.47604 | 172.61 | 0.6 | 1 | sco_vol_gc_hg_combo active; sco_vol=1.20357;q_long_exit=2.05643;q_short_entry=2.05643;q_short_exit=1.37143;vol_diff=-0.00928571;accel=1.0805; aggregate SCCO capped at 12.0%\|sco_vol_regime_pulse active; sco_vol=1.20357;vol_quantile=1.83807;vol_diff=-0.00928571; aggregate SCCO capped at 12.0%\|persistent_binary active; feature=-0.00848041; aggregate SCCO capped at 12.0% |
| stock | hg_gc_gap_gc_carry_iron\|sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | VALE | 0.12 | 51.8135 | 11.58 | -0 | 0.6 | dual_feature_hysteresis active; hg_gap=-0.00848041;gc_carry=-0.155093; aggregate VALE capped at 12.0%\|sco_vol_gc_hg_combo active; sco_vol=1.20357;q_long_exit=2.05643;q_short_entry=2.05643;q_short_exit=1.37143;vol_diff=-0.00928571;accel=1.0805; aggregate VALE capped at 12.0%\|sco_vol_regime_pulse active; sco_vol=1.20357;vol_quantile=1.83807;vol_diff=-0.00928571; aggregate VALE capped at 12.0%\|persistent_binary active; feature=-0.00848041; aggregate VALE capped at 12.0% |
| hedge | hedge | SPY | -0.156888 | -1.03242 | 759.81 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | -0.341904 | -17.5822 | 97.23 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | hg_gc_gap_gc_carry_iron\|miners | FSUGY | BUY | 15 | 15 | 0.06291 | False | 20.97 | 20.92 | 21.02 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | SCCO | SELL | -1 | -1 | -0.034522 | False | 172.61 | 172.18 | 173.04 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XME | BUY | 0 | 1 | 0.019446 | False | 97.23 | 96.99 | 97.47 | single aggregate hedge order after confirming stock fills |

## Beta method for 2026-11-12 — as-of 2026-11-11

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-11-12-hs1sx7im/cached/targets-metals/2026-11-12. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
