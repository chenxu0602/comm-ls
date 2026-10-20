# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-10-13

- Signal as-of date: 2026-10-12
- Target trading date: 2026-10-13
- AUM: $15,000.00
- Gross stock weight: 54.30%
- Single-name stock weight cap: 5.00%
- Net stock weight: -5.30%
- Gross hedge weight: 29.16%
- Total net weight after hedges: 12.02%
- Estimated turnover from current positions: 6.20%
- Full eligible order turnover: 0.55%
- Today's total child-order turnover: 0.71%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $0.27
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.245 | 0.245 | 3675 | 3675 | 8 |
| stock_short_without_hedge | 0.298 | -0.298 | 4470 | -4470 | 10 |
| total_hedge | 0.291556 | 0.173175 | 4373.34 | 2597.62 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.045 | 18 | 37.53 | 2026-10-12 | 37.44 | 37.62 | 0.4 | 1.1 |  |  | 2026-10-16 | fixed_hold active from 2026-09-28 to before 2026-10-16 (initial signal 2026-09-25, last same-direction signal 2026-10-12) |
| bwt | TECK | 0.015 | 3.3 | 67.54 | 2026-10-12 | 67.37 | 67.71 | 0.9 | 0.7 |  |  | 2026-10-16 | fixed_hold active from 2026-09-28 to before 2026-10-16 (initial signal 2026-09-25, last same-direction signal 2026-10-12) |
| chemical | DOW | -0.05 | -26.7 | 28.12 | 2026-10-12 | 28.05 | 28.19 | 0.3 | 1.2 |  |  | 2026-11-11 | fixed_hold active from 2026-04-20 to before 2026-11-11 (initial signal 2026-04-17, last same-direction signal 2026-10-12) |
| chemical | LYB | -0.05 | -12.6 | 59.41 | 2026-10-12 | 59.26 | 59.56 | -0 | 1.2 |  |  | 2026-11-11 | fixed_hold active from 2026-04-20 to before 2026-11-11 (initial signal 2026-04-17, last same-direction signal 2026-10-12) |
| chemical | WLK | -0.05 | -12.1 | 61.85 | 2026-10-12 | 61.7 | 62 | 0.8 | 0.7 |  |  | 2026-11-11 | fixed_hold active from 2026-04-20 to before 2026-11-11 (initial signal 2026-04-17, last same-direction signal 2026-10-12) |
| chemical | CE | -0.028 | -9.4 | 44.56 | 2026-10-12 | 44.45 | 44.67 | 0.9 | 1 |  |  | 2026-11-11 | fixed_hold active from 2026-04-20 to before 2026-11-11 (initial signal 2026-04-17, last same-direction signal 2026-10-12) |
| chemical | EMN | -0.028 | -6.8 | 62.1 | 2026-10-12 | 61.94 | 62.26 | 1 | 0.2 |  |  | 2026-11-11 | fixed_hold active from 2026-04-20 to before 2026-11-11 (initial signal 2026-04-17, last same-direction signal 2026-10-12) |
| chemical | HUN | -0.028 | -52 | 8.07 | 2026-10-12 | 8.05 | 8.09 | 1.4 | 0.7 |  |  | 2026-11-11 | fixed_hold active from 2026-04-20 to before 2026-11-11 (initial signal 2026-04-17, last same-direction signal 2026-10-12) |
| chemical | AVNT | -0.014 | -5.4 | 38.96 | 2026-10-12 | 38.86 | 39.06 | 1.1 | -0 |  |  | 2026-11-11 | fixed_hold active from 2026-04-20 to before 2026-11-11 (initial signal 2026-04-17, last same-direction signal 2026-10-12) |
| cro | MPC | 0.02 | 0.7 | 458.81 | 2026-10-12 | 457.66 | 459.96 | -0.1 | 0 |  |  |  | continuous hysteresis sign active |
| cro | VLO | 0.015 | 0.5 | 436 | 2026-10-12 | 434.91 | 437.09 | -0.3 | 0 |  |  |  | continuous hysteresis sign active |
| psx_ref\|cro | PSX | 0.05 | 2.7 | 281.47 | 2026-10-12 | 280.77 | 282.17 | -0 | 0.8 |  |  | 2026-10-16 | fixed_hold active from 2026-10-08 to before 2026-10-16 (initial signal 2026-10-07, last same-direction signal 2026-10-12)\|continuous hysteresis sign active |
| refiner | DK | 0.05 | 9.7 | 77.33 | 2026-10-12 | 77.14 | 77.52 | 0.2 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | PBF | 0.03 | 5.3 | 85.02 | 2026-10-12 | 84.81 | 85.23 | 0 | 1.7 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | DINO | 0.02 | 2.4 | 122.91 | 2026-10-12 | 122.6 | 123.22 | 0.1 | 1 |  |  |  | 5d rolling-mean band_hysteresis active |
| services | FTI | -0.02 | -4.3 | 69.75 | 2026-10-12 | 69.58 | 69.92 | 0.6 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -6.2 | 48.77 | 2026-10-12 | 48.65 | 48.89 | 1.1 | 0.9 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4.6 | 32.6 | 2026-10-12 | 32.52 | 32.68 | 0.6 | 1.2 |  |  |  | continuous hysteresis sign active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.160386 | 3.09187 | 778.1 | 2026-10-12 | 776.155 | 780.045 |
| XLE | 0.0719798 | 16.3566 | 66.01 | 2026-10-12 | 65.845 | 66.175 |
| XME | -0.0591906 | -8.46789 | 104.85 | 2026-10-12 | 104.588 | 105.112 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | chemical | HUN | SELL | -5 | -5 | -0.00269 | False |  | 8.07 | 2026-10-12 | 8.04982 | 8.09017 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XLE | SELL | -1 | -1 | -0.00440067 | False |  | 66.01 | 2026-10-12 | 65.845 | 66.175 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |


## Strategy changes and allocation notes

- CRO (crack refiner-only) added effective 2026-10-06: 10% allocation from unused CL capacity. CL AUM remains $15,000; existing sleeve weights are NOT reduced or renormalized.
- CRO stocks: VLO/MPC/PSX = 30/40/30%; crack_03; signal lookback 30 sessions; volatility lookback 30 (minimum 20); no signal smoothing; balance=0.5 (maximum CRO stock gross 5% of CL AUM).
- CRO explicit hedge is SPY ONLY, not XLE. Preserve component hedge ownership when PSX overlaps existing sleeves; net single-name cap and execution constraints still apply.
- This addition is refiner-only CRO, NOT the refiner-producer CRP, refiner-VLCC CRV, or refiner-chemical CRC research strategies.
- CRO stock target state for this package: active. Flat CRO must not create reallocation trades under identical inputs.
- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.
- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.
- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.
## Beta method for 2026-10-13 — as-of 2026-10-12

Continues the operator's 2026-10-09 decision to retain legacy daily beta.

Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-10-13-p40p8pvg/cached/targets-cl/2026-10-13. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
