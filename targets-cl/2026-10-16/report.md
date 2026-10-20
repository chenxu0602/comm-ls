# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-10-16

- Signal as-of date: 2026-10-15
- Target trading date: 2026-10-16
- AUM: $15,000.00
- Gross stock weight: 50.80%
- Single-name stock weight cap: 5.00%
- Net stock weight: -8.80%
- Gross hedge weight: 25.23%
- Total net weight after hedges: 4.37%
- Estimated turnover from current positions: 8.24%
- Full eligible order turnover: 4.40%
- Today's total child-order turnover: 5.02%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $1.88
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.21 | 0.21 | 3150 | 3150 | 6 |
| stock_short_without_hedge | 0.298 | -0.298 | 4470 | -4470 | 10 |
| total_hedge | 0.252251 | 0.131677 | 3783.77 | 1975.16 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.045 | 19.4 | 34.75 | 2026-10-15 | 34.66 | 34.84 | 0.4 | 1.1 |  |  | 2026-10-21 | fixed_hold active from 2026-09-28 to before 2026-10-21 (initial signal 2026-09-25, last same-direction signal 2026-10-15) |
| bwt | TECK | 0.015 | 3.4 | 65.74 | 2026-10-15 | 65.58 | 65.9 | 0.9 | 0.7 |  |  | 2026-10-21 | fixed_hold active from 2026-09-28 to before 2026-10-21 (initial signal 2026-09-25, last same-direction signal 2026-10-15) |
| chemical | DOW | -0.05 | -25.3 | 29.66 | 2026-10-15 | 29.59 | 29.73 | 0.2 | 1.1 |  |  | 2026-11-16 | fixed_hold active from 2026-04-20 to before 2026-11-16 (initial signal 2026-04-17, last same-direction signal 2026-10-15) |
| chemical | LYB | -0.05 | -12 | 62.67 | 2026-10-15 | 62.51 | 62.83 | -0.1 | 1.1 |  |  | 2026-11-16 | fixed_hold active from 2026-04-20 to before 2026-11-16 (initial signal 2026-04-17, last same-direction signal 2026-10-15) |
| chemical | WLK | -0.05 | -11.8 | 63.61 | 2026-10-15 | 63.45 | 63.77 | 0.8 | 0.7 |  |  | 2026-11-16 | fixed_hold active from 2026-04-20 to before 2026-11-16 (initial signal 2026-04-17, last same-direction signal 2026-10-15) |
| chemical | CE | -0.028 | -9 | 46.44 | 2026-10-15 | 46.32 | 46.56 | 0.8 | 1 |  |  | 2026-11-16 | fixed_hold active from 2026-04-20 to before 2026-11-16 (initial signal 2026-04-17, last same-direction signal 2026-10-15) |
| chemical | EMN | -0.028 | -6.6 | 63.87 | 2026-10-15 | 63.71 | 64.03 | 0.9 | 0.2 |  |  | 2026-11-16 | fixed_hold active from 2026-04-20 to before 2026-11-16 (initial signal 2026-04-17, last same-direction signal 2026-10-15) |
| chemical | HUN | -0.028 | -49.1 | 8.56 | 2026-10-15 | 8.54 | 8.58 | 1.4 | 0.7 |  |  | 2026-11-16 | fixed_hold active from 2026-04-20 to before 2026-11-16 (initial signal 2026-04-17, last same-direction signal 2026-10-15) |
| chemical | AVNT | -0.014 | -5.4 | 39 | 2026-10-15 | 38.9 | 39.1 | 1.1 | -0 |  |  | 2026-11-16 | fixed_hold active from 2026-04-20 to before 2026-11-16 (initial signal 2026-04-17, last same-direction signal 2026-10-15) |
| psx_ref | PSX | 0.05 | 2.6 | 289.2 | 2026-10-15 | 288.48 | 289.92 | 0.1 | 1.1 |  |  | 2026-10-21 | fixed_hold active from 2026-10-08 to before 2026-10-21 (initial signal 2026-10-07, last same-direction signal 2026-10-15) |
| refiner | DK | 0.05 | 9.8 | 76.88 | 2026-10-15 | 76.69 | 77.07 | 0.1 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | PBF | 0.03 | 5.2 | 86.99 | 2026-10-15 | 86.77 | 87.21 | -0 | 1.7 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | DINO | 0.02 | 2.4 | 124.7 | 2026-10-15 | 124.39 | 125.01 | 0.1 | 1.1 |  |  |  | 5d rolling-mean band_hysteresis active |
| services | FTI | -0.02 | -4.4 | 68.23 | 2026-10-15 | 68.06 | 68.4 | 0.7 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -6.2 | 48.37 | 2026-10-15 | 48.25 | 48.49 | 1.1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4.6 | 32.89 | 2026-10-15 | 32.81 | 32.97 | 0.6 | 1.1 |  |  |  | continuous hysteresis sign active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.14264 | 2.77225 | 771.79 | 2026-10-15 | 769.861 | 773.719 |
| XLE | 0.0493246 | 11.1158 | 66.56 | 2026-10-15 | 66.3936 | 66.7264 |
| XME | -0.0602869 | -8.92347 | 101.34 | 2026-10-15 | 101.087 | 101.593 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | cro | MPC | SELL | -1 | -1 | -0.0317947 | False |  | 476.92 | 2026-10-15 | 475.728 | 478.112 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | DK | BUY | 1 | 1 | 0.00512533 | False |  | 76.88 | 2026-10-15 | 76.6878 | 77.0722 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XLE | SELL | -2 | -3 | -0.013312 | False |  | 66.56 | 2026-10-15 | 66.3936 | 66.7264 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |


## Strategy changes and allocation notes

- CRO (crack refiner-only) added effective 2026-10-06: 10% allocation from unused CL capacity. CL AUM remains $15,000; existing sleeve weights are NOT reduced or renormalized.
- CRO stocks: VLO/MPC/PSX = 30/40/30%; crack_03; signal lookback 30 sessions; volatility lookback 30 (minimum 20); no signal smoothing; balance=0.5 (maximum CRO stock gross 5% of CL AUM).
- CRO explicit hedge is SPY ONLY, not XLE. Preserve component hedge ownership when PSX overlaps existing sleeves; net single-name cap and execution constraints still apply.
- This addition is refiner-only CRO, NOT the refiner-producer CRP, refiner-VLCC CRV, or refiner-chemical CRC research strategies.
- CRO stock target state for this package: flat. Flat CRO must not create reallocation trades under identical inputs.
- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.
- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.
- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.
## Beta method for 2026-10-16 — as-of 2026-10-15

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-10-16-afm7wpl7/cached/targets-cl/2026-10-16. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
