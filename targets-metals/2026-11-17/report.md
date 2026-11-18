# Metals Daily Targets: 2026-11-17

- Signal as-of date: 2026-11-16
- Target trading date: 2026-11-17
- AUM: $5,000.00
- Effective dated sleeve weights (unused capacity stays cash; no normalization): hg_gc_gap_gc_carry_iron=7.50%; sco_vol_gc_hg_accel_miners=10.00%; sco_specialty_alloys=0.00%; sco_vol_miners=12.50%; copper_miner=7.50%; miners=12.50%
- This reweight is operator approved; signal rules, 12% name cap and legacy beta method are unchanged. Migration turnover must be separated from signal turnover.
- Gross stock weight: 35.00%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: 35.00%
- Gross hedge weight: 34.14%
- Total net weight after hedges: 0.86%
- Turnover from Metals-attributed current positions: 28.60%
- Full eligible order turnover: 25.50%
- Today's total child-order turnover: 27.89%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $3.49

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
| stock_long_without_hedge | 0.35 | 0.35 | 1750 | 1750 | 5 |
| stock_short_without_hedge | 0 | 0 | 0 | 0 | 0 |
| total_hedge | 0.341389 | -0.341389 | 1706.94 | -1706.94 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | BHP | 0.105 | 6.94904 | 75.55 | 0.4 | 0.6 | sco_vol_gc_hg_combo active; sco_vol=1.42143;q_long_exit=2.02857;q_short_entry=2.02857;q_short_exit=1.36843;vol_diff=0.165714;accel=1.83278\|sco_vol_regime_pulse active; sco_vol=1.42143;vol_quantile=1.83579;vol_diff=0.165714\|persistent_binary active; feature=0.000875368 |
| stock | miners | FSUGY | 0.025 | 6.47333 | 19.31 | 0.3 | 0.3 | persistent_binary active; feature=0.000875368 |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | RIO | 0.1025 | 6.40225 | 80.05 | 0.2 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.42143;q_long_exit=2.02857;q_short_entry=2.02857;q_short_exit=1.36843;vol_diff=0.165714;accel=1.83278\|sco_vol_regime_pulse active; sco_vol=1.42143;vol_quantile=1.83579;vol_diff=0.165714\|persistent_binary active; feature=0.000875368 |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | SCCO | 0.07 | 2.27465 | 153.87 | 0.6 | 1 | sco_vol_gc_hg_combo active; sco_vol=1.42143;q_long_exit=2.02857;q_short_entry=2.02857;q_short_exit=1.36843;vol_diff=0.165714;accel=1.83278\|sco_vol_regime_pulse active; sco_vol=1.42143;vol_quantile=1.83579;vol_diff=0.165714\|persistent_binary active; feature=0.000875368 |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | VALE | 0.0475 | 22.7055 | 10.46 | 0 | 0.6 | sco_vol_gc_hg_combo active; sco_vol=1.42143;q_long_exit=2.02857;q_short_entry=2.02857;q_short_exit=1.36843;vol_diff=0.165714;accel=1.83278\|sco_vol_regime_pulse active; sco_vol=1.42143;vol_quantile=1.83579;vol_diff=0.165714\|persistent_binary active; feature=0.000875368 |
| hedge | hedge | SPY | -0.116975 | -0.790425 | 739.95 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | -0.224414 | -12.4799 | 89.91 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | miners | FSUGY | SELL | -10 | -10 | -0.03862 | False | 19.31 | 19.26 | 19.36 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | BHP | SELL | -1 | -1 | -0.01511 | False | 75.55 | 75.36 | 75.74 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | RIO | SELL | -1 | -1 | -0.01601 | False | 80.05 | 79.85 | 80.25 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | SCCO | SELL | -2 | -2 | -0.061548 | False | 153.87 | 153.49 | 154.25 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners\|sco_vol_miners\|miners | VALE | SELL | -19 | -19 | -0.039748 | False | 10.46 | 10.43 | 10.49 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XME | BUY | 6 | 6 | 0.107892 | False | 89.91 | 89.69 | 90.13 | single aggregate hedge order after confirming stock fills |

## Beta method for 2026-11-17 — as-of 2026-11-16

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-11-17-p0gussny/cached/targets-metals/2026-11-17. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
