# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-10-19

- Signal as-of date: 2026-10-16
- Target trading date: 2026-10-19
- AUM: $15,000.00
- Gross stock weight: 50.80%
- Single-name stock weight cap: 5.00%
- Net stock weight: -8.80%
- Gross hedge weight: 25.16%
- Total net weight after hedges: 4.27%
- Estimated turnover from current positions: 4.61%
- Full eligible order turnover: 0.54%
- Today's total child-order turnover: 0.45%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $0.17
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.21 | 0.21 | 3150 | 3150 | 6 |
| stock_short_without_hedge | 0.298 | -0.298 | 4470 | -4470 | 10 |
| total_hedge | 0.251638 | 0.130686 | 3774.58 | 1960.29 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.045 | 19.8 | 34.16 | 2026-10-16 | 34.07 | 34.25 | 0.4 | 1.1 |  |  | 2026-10-22 | fixed_hold active from 2026-09-28 to before 2026-10-22 (initial signal 2026-09-25, last same-direction signal 2026-10-16) |
| bwt | TECK | 0.015 | 3.5 | 64.62 | 2026-10-16 | 64.46 | 64.78 | 0.9 | 0.7 |  |  | 2026-10-22 | fixed_hold active from 2026-09-28 to before 2026-10-22 (initial signal 2026-09-25, last same-direction signal 2026-10-16) |
| chemical | DOW | -0.05 | -25.1 | 29.93 | 2026-10-16 | 29.86 | 30 | 0.2 | 1.1 |  |  | 2026-11-17 | fixed_hold active from 2026-04-20 to before 2026-11-17 (initial signal 2026-04-17, last same-direction signal 2026-10-16) |
| chemical | LYB | -0.05 | -11.7 | 64.01 | 2026-10-16 | 63.85 | 64.17 | -0.1 | 1.1 |  |  | 2026-11-17 | fixed_hold active from 2026-04-20 to before 2026-11-17 (initial signal 2026-04-17, last same-direction signal 2026-10-16) |
| chemical | WLK | -0.05 | -11.8 | 63.33 | 2026-10-16 | 63.17 | 63.49 | 0.8 | 0.7 |  |  | 2026-11-17 | fixed_hold active from 2026-04-20 to before 2026-11-17 (initial signal 2026-04-17, last same-direction signal 2026-10-16) |
| chemical | CE | -0.028 | -8.8 | 47.49 | 2026-10-16 | 47.37 | 47.61 | 0.8 | 1 |  |  | 2026-11-17 | fixed_hold active from 2026-04-20 to before 2026-11-17 (initial signal 2026-04-17, last same-direction signal 2026-10-16) |
| chemical | EMN | -0.028 | -6.7 | 62.33 | 2026-10-16 | 62.17 | 62.49 | 0.9 | 0.2 |  |  | 2026-11-17 | fixed_hold active from 2026-04-20 to before 2026-11-17 (initial signal 2026-04-17, last same-direction signal 2026-10-16) |
| chemical | HUN | -0.028 | -49 | 8.58 | 2026-10-16 | 8.56 | 8.6 | 1.4 | 0.7 |  |  | 2026-11-17 | fixed_hold active from 2026-04-20 to before 2026-11-17 (initial signal 2026-04-17, last same-direction signal 2026-10-16) |
| chemical | AVNT | -0.014 | -5.4 | 38.98 | 2026-10-16 | 38.88 | 39.08 | 1.1 | -0 |  |  | 2026-11-17 | fixed_hold active from 2026-04-20 to before 2026-11-17 (initial signal 2026-04-17, last same-direction signal 2026-10-16) |
| psx_ref | PSX | 0.05 | 2.6 | 293.17 | 2026-10-16 | 292.44 | 293.9 | 0.1 | 1.1 |  |  | 2026-10-22 | fixed_hold active from 2026-10-08 to before 2026-10-22 (initial signal 2026-10-07, last same-direction signal 2026-10-16) |
| refiner | DK | 0.05 | 9.8 | 76.59 | 2026-10-16 | 76.4 | 76.78 | 0.1 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | PBF | 0.03 | 5.3 | 84.52 | 2026-10-16 | 84.31 | 84.73 | 0 | 1.7 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | DINO | 0.02 | 2.4 | 125.29 | 2026-10-16 | 124.98 | 125.6 | 0.1 | 1 |  |  |  | 5d rolling-mean band_hysteresis active |
| services | FTI | -0.02 | -4.3 | 69.67 | 2026-10-16 | 69.5 | 69.84 | 0.7 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -6.1 | 49.5 | 2026-10-16 | 49.38 | 49.62 | 1.1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4.5 | 33.5 | 2026-10-16 | 33.42 | 33.58 | 0.6 | 1.1 |  |  |  | continuous hysteresis sign active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.140262 | 2.75655 | 763.25 | 2026-10-16 | 761.342 | 765.158 |
| XLE | 0.0508999 | 11.1884 | 68.24 | 2026-10-16 | 68.0694 | 68.4106 |
| XME | -0.0604761 | -8.98871 | 100.92 | 2026-10-16 | 100.668 | 101.172 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | hedge | XLE | BUY | 1 | 1 | 0.00454933 | False |  | 68.24 | 2026-10-16 | 68.0694 | 68.4106 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |


## Strategy changes and allocation notes

- CRO (crack refiner-only) added effective 2026-10-06: 10% allocation from unused CL capacity. CL AUM remains $15,000; existing sleeve weights are NOT reduced or renormalized.
- CRO stocks: VLO/MPC/PSX = 30/40/30%; crack_03; signal lookback 30 sessions; volatility lookback 30 (minimum 20); no signal smoothing; balance=0.5 (maximum CRO stock gross 5% of CL AUM).
- CRO explicit hedge is SPY ONLY, not XLE. Preserve component hedge ownership when PSX overlaps existing sleeves; net single-name cap and execution constraints still apply.
- This addition is refiner-only CRO, NOT the refiner-producer CRP, refiner-VLCC CRV, or refiner-chemical CRC research strategies.
- CRO stock target state for this package: flat. Flat CRO must not create reallocation trades under identical inputs.
- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.
- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.
- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.
## Beta method for 2026-10-19 — as-of 2026-10-16

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-10-19-yth0x4tp/cached/targets-cl/2026-10-19. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
