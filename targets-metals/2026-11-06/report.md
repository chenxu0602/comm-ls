# Metals Daily Targets: 2026-11-06

- Signal as-of date: 2026-11-05
- Target trading date: 2026-11-06
- AUM: $5,000.00
- Effective 2026-10-12: gap/accel/SCO-vol/copper/miners live weights = 15%/20%/25%/10%/25%; alloys remains suspended (5% cash). Earlier target sessions retain previous weights.
- This reweight is operator approved; signal rules, 12% name cap and legacy beta method are unchanged. Migration turnover must be separated from signal turnover.
- Gross stock weight: 30.00%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: 20.00%
- Gross hedge weight: 19.59%
- Total net weight after hedges: 0.41%
- Turnover from Metals-attributed current positions: 101.26%
- Full eligible order turnover: 101.18%
- Today's total child-order turnover: 54.73%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $6.84

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
| stock_long_without_hedge | 0.25 | 0.25 | 1250 | 1250 | 4 |
| stock_short_without_hedge | 0.05 | -0.05 | 250 | -250 | 1 |
| total_hedge | 0.195887 | -0.195887 | 979.43 | -979.43 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | BHP | 0.06 | 3.81777 | 78.58 | 0.4 | 0.6 | sco_vol_gc_hg_combo active; sco_vol=1.23929;q_long_exit=2.06929;q_short_entry=2.06929;q_short_exit=1.374;vol_diff=0.00571428;accel=1.00886\|sco_vol_regime_pulse active; sco_vol=1.23929;vol_quantile=1.85493;vol_diff=0.00571428\|persistent_binary active; feature=0.00937651 |
| stock | miners | FSUGY | -0.05 | -11.8259 | 21.14 | 0.3 | 0.3 | persistent_binary active; feature=0.00937651 |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | RIO | 0.105 | 6.31313 | 83.16 | 0.2 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.23929;q_long_exit=2.06929;q_short_entry=2.06929;q_short_exit=1.374;vol_diff=0.00571428;accel=1.00886\|sco_vol_regime_pulse active; sco_vol=1.23929;vol_quantile=1.85493;vol_diff=0.00571428\|persistent_binary active; feature=0.00937651 |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | SCCO | 0.04 | 1.20934 | 165.38 | 0.6 | 1 | sco_vol_gc_hg_combo active; sco_vol=1.23929;q_long_exit=2.06929;q_short_entry=2.06929;q_short_exit=1.374;vol_diff=0.00571428;accel=1.00886\|sco_vol_regime_pulse active; sco_vol=1.23929;vol_quantile=1.85493;vol_diff=0.00571428\|persistent_binary active; feature=0.00937651 |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | VALE | 0.045 | 19.6507 | 11.45 | -0 | 0.6 | sco_vol_gc_hg_combo active; sco_vol=1.23929;q_long_exit=2.06929;q_short_entry=2.06929;q_short_exit=1.374;vol_diff=0.00571428;accel=1.00886\|sco_vol_regime_pulse active; sco_vol=1.23929;vol_quantile=1.85493;vol_diff=0.00571428\|persistent_binary active; feature=0.00937651 |
| hedge | hedge | SPY | -0.056709 | -0.386825 | 733 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | -0.139178 | -7.69619 | 90.42 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | BHP | BUY | 9 | 5 | 0.07858 | True | 78.58 | 78.38 | 78.78 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | RIO | BUY | 9 | 3 | 0.049896 | True | 83.16 | 82.95 | 83.37 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | SCCO | BUY | 3 | 2 | 0.066152 | True | 165.38 | 164.97 | 165.79 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | VALE | BUY | 31 | 11 | 0.02519 | True | 11.45 | 11.42 | 11.48 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | SPY | SELL | -1 | -1 | -0.1466 | False | 733 | 731.17 | 734.83 | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XME | SELL | -19 | -10 | -0.18084 | False | 90.42 | 90.19 | 90.65 | single aggregate hedge order after confirming stock fills |

## Beta method for 2026-11-06 — as-of 2026-11-05

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-11-06-lajdlroc/cached/targets-metals/2026-11-06. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
