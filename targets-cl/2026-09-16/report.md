# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-09-16

- Signal as-of date: 2026-09-15
- Target trading date: 2026-09-16
- AUM: $15,000.00
- Gross stock weight: 59.80%
- Single-name stock weight cap: 5.00%
- Net stock weight: -29.80%
- Gross hedge weight: 68.04%
- Total net weight after hedges: 24.14%
- Estimated turnover from current positions: 8.85%
- Full eligible order turnover: 1.43%
- Today's total child-order turnover: 1.31%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $0.49
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.15 | 0.15 | 2250 | 2250 | 7 |
| stock_short_without_hedge | 0.448 | -0.448 | 6720 | -6720 | 14 |
| total_hedge | 0.680436 | 0.53939 | 10206.5 | 8090.85 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.045 | 20.8 | 32.53 | 2026-09-15 | 32.45 | 32.61 | 0.5 | 1.1 |  |  | 2026-09-17 | fixed_hold active from 2026-08-04 to before 2026-09-17 (initial signal 2026-08-03, last same-direction signal 2026-09-11) |
| bwt | TECK | 0.015 | 3.5 | 64.65 | 2026-09-15 | 64.49 | 64.81 | 0.9 | 0.7 |  |  | 2026-09-17 | fixed_hold active from 2026-08-04 to before 2026-09-17 (initial signal 2026-08-03, last same-direction signal 2026-09-11) |
| chemical | DOW | -0.05 | -25.1 | 29.85 | 2026-09-15 | 29.78 | 29.92 | 0.3 | 1.2 |  |  | 2026-10-15 | fixed_hold active from 2026-04-20 to before 2026-10-15 (initial signal 2026-04-17, last same-direction signal 2026-09-15) |
| chemical | LYB | -0.05 | -11.5 | 65.43 | 2026-09-15 | 65.27 | 65.59 | 0 | 1.2 |  |  | 2026-10-15 | fixed_hold active from 2026-04-20 to before 2026-10-15 (initial signal 2026-04-17, last same-direction signal 2026-09-15) |
| chemical | WLK | -0.05 | -10.7 | 70.02 | 2026-09-15 | 69.84 | 70.2 | 0.9 | 0.7 |  |  | 2026-10-15 | fixed_hold active from 2026-04-20 to before 2026-10-15 (initial signal 2026-04-17, last same-direction signal 2026-09-15) |
| chemical | CE | -0.028 | -8.9 | 47.22 | 2026-09-15 | 47.1 | 47.34 | 0.9 | 1 |  |  | 2026-10-15 | fixed_hold active from 2026-04-20 to before 2026-10-15 (initial signal 2026-04-17, last same-direction signal 2026-09-15) |
| chemical | EMN | -0.028 | -6.4 | 65.88 | 2026-09-15 | 65.72 | 66.04 | 1 | 0.2 |  |  | 2026-10-15 | fixed_hold active from 2026-04-20 to before 2026-10-15 (initial signal 2026-04-17, last same-direction signal 2026-09-15) |
| chemical | HUN | -0.028 | -45.6 | 9.22 | 2026-09-15 | 9.2 | 9.24 | 1.5 | 0.7 |  |  | 2026-10-15 | fixed_hold active from 2026-04-20 to before 2026-10-15 (initial signal 2026-04-17, last same-direction signal 2026-09-15) |
| chemical | AVNT | -0.014 | -5.1 | 40.97 | 2026-09-15 | 40.87 | 41.07 | 1.2 | -0 |  |  | 2026-10-15 | fixed_hold active from 2026-04-20 to before 2026-10-15 (initial signal 2026-04-17, last same-direction signal 2026-09-15) |
| fuel | CASY | 0.024 | 0.6 | 587.14 | 2026-09-15 | 585.67 | 588.61 | -0 | 0 |  |  | 2026-09-23 | fixed_hold active from 2026-03-04 to before 2026-09-23 (initial signal 2026-03-03, last same-direction signal 2026-09-15) |
| fuel | MUSA | 0.016 | 0.5 | 526.32 | 2026-09-15 | 525 | 527.64 | -0.7 | 0 |  |  | 2026-09-23 | fixed_hold active from 2026-03-04 to before 2026-09-23 (initial signal 2026-03-03, last same-direction signal 2026-09-15) |
| metals | ATI | 0.02 | 1.6 | 186.69 | 2026-09-15 | 186.22 | 187.16 | 1.1 | 0.3 |  |  | 2026-09-30 | fixed_hold active from 2026-01-12 to before 2026-09-30 (initial signal 2026-01-09, last same-direction signal 2026-09-15) |
| metals | CRS | 0.015 | 0.5 | 415.32 | 2026-09-15 | 414.28 | 416.36 | 1.1 | 0.3 |  |  | 2026-09-30 | fixed_hold active from 2026-01-12 to before 2026-09-30 (initial signal 2026-01-09, last same-direction signal 2026-09-15) |
| metals | HWM | 0.015 | 1 | 224.67 | 2026-09-15 | 224.11 | 225.23 | 1 | 0.1 |  |  | 2026-09-30 | fixed_hold active from 2026-01-12 to before 2026-09-30 (initial signal 2026-01-09, last same-direction signal 2026-09-15) |
| psx_ref | PSX | -0.05 | -2.8 | 264.93 | 2026-09-15 | 264.27 | 265.59 | 0.1 | 1.1 |  |  | 2026-09-21 | fixed_hold active from 2026-09-09 to before 2026-09-21 (initial signal 2026-09-08, last same-direction signal 2026-09-15) |
| refiner | DK | -0.05 | -9.6 | 78.14 | 2026-09-15 | 77.94 | 78.34 | 0.2 | 1.4 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | PBF | -0.03 | -6 | 74.72 | 2026-09-15 | 74.53 | 74.91 | 0.1 | 1.8 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | DINO | -0.02 | -2.7 | 112.25 | 2026-09-15 | 111.97 | 112.53 | 0.2 | 1 |  |  |  | 5d rolling-mean band_hysteresis active |
| services | FTI | -0.02 | -4 | 74.97 | 2026-09-15 | 74.78 | 75.16 | 0.6 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -5.5 | 54.2 | 2026-09-15 | 54.06 | 54.34 | 1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4.2 | 35.67 | 2026-09-15 | 35.58 | 35.76 | 0.6 | 1.2 |  |  |  | continuous hysteresis sign active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.154505 | 3.05994 | 757.39 | 2026-09-15 | 755.497 | 759.283 |
| XLE | 0.455409 | 103.612 | 65.93 | 2026-09-15 | 65.7652 | 66.0948 |
| XME | -0.0705231 | -9.66599 | 109.44 | 2026-09-15 | 109.166 | 109.714 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | bwt | ERO | BUY | 2 | 2 | 0.00433733 | False |  | 32.53 | 2026-09-15 | 32.4487 | 32.6113 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XLE | SELL | -2 | -2 | -0.00879067 | False |  | 65.93 | 2026-09-15 | 65.7652 | 66.0948 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
