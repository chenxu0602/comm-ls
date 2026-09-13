# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-09-11

- Signal as-of date: 2026-09-10
- Target trading date: 2026-09-11
- AUM: $15,000.00
- Gross stock weight: 59.80%
- Single-name stock weight cap: 5.00%
- Net stock weight: -29.80%
- Gross hedge weight: 67.20%
- Total net weight after hedges: 23.33%
- Estimated turnover from current positions: 8.78%
- Full eligible order turnover: 6.78%
- Today's total child-order turnover: 12.24%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $4.59
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.15 | 0.15 | 2250 | 2250 | 7 |
| stock_short_without_hedge | 0.448 | -0.448 | 6720 | -6720 | 14 |
| total_hedge | 0.671989 | 0.531297 | 10079.8 | 7969.45 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.045 | 19.3 | 34.98 | 2026-09-10 | 34.89 | 35.07 | 0.4 | 1.1 |  |  | 2026-09-16 | fixed_hold active from 2026-08-04 to before 2026-09-16 (initial signal 2026-08-03, last same-direction signal 2026-09-10) |
| bwt | TECK | 0.015 | 3.4 | 65.9 | 2026-09-10 | 65.74 | 66.06 | 0.9 | 0.7 |  |  | 2026-09-16 | fixed_hold active from 2026-08-04 to before 2026-09-16 (initial signal 2026-08-03, last same-direction signal 2026-09-10) |
| chemical | DOW | -0.05 | -25.3 | 29.64 | 2026-09-10 | 29.57 | 29.71 | 0.4 | 1.2 |  |  | 2026-10-12 | fixed_hold active from 2026-04-20 to before 2026-10-12 (initial signal 2026-04-17, last same-direction signal 2026-09-10) |
| chemical | LYB | -0.05 | -11.7 | 64.3 | 2026-09-10 | 64.14 | 64.46 | 0 | 1.2 |  |  | 2026-10-12 | fixed_hold active from 2026-04-20 to before 2026-10-12 (initial signal 2026-04-17, last same-direction signal 2026-09-10) |
| chemical | WLK | -0.05 | -10.5 | 71.62 | 2026-09-10 | 71.44 | 71.8 | 0.9 | 0.7 |  |  | 2026-10-12 | fixed_hold active from 2026-04-20 to before 2026-10-12 (initial signal 2026-04-17, last same-direction signal 2026-09-10) |
| chemical | CE | -0.028 | -9.2 | 45.72 | 2026-09-10 | 45.61 | 45.83 | 1 | 0.9 |  |  | 2026-10-12 | fixed_hold active from 2026-04-20 to before 2026-10-12 (initial signal 2026-04-17, last same-direction signal 2026-09-10) |
| chemical | EMN | -0.028 | -6.1 | 68.38 | 2026-09-10 | 68.21 | 68.55 | 1 | 0.2 |  |  | 2026-10-12 | fixed_hold active from 2026-04-20 to before 2026-10-12 (initial signal 2026-04-17, last same-direction signal 2026-09-10) |
| chemical | HUN | -0.028 | -44.1 | 9.53 | 2026-09-10 | 9.51 | 9.55 | 1.5 | 0.7 |  |  | 2026-10-12 | fixed_hold active from 2026-04-20 to before 2026-10-12 (initial signal 2026-04-17, last same-direction signal 2026-09-10) |
| chemical | AVNT | -0.014 | -5 | 41.72 | 2026-09-10 | 41.62 | 41.82 | 1.2 | -0 |  |  | 2026-10-12 | fixed_hold active from 2026-04-20 to before 2026-10-12 (initial signal 2026-04-17, last same-direction signal 2026-09-10) |
| fuel | CASY | 0.024 | 0.6 | 627.64 | 2026-09-10 | 626.07 | 629.21 | -0 | 0 |  |  | 2026-09-18 | fixed_hold active from 2026-03-04 to before 2026-09-18 (initial signal 2026-03-03, last same-direction signal 2026-09-10) |
| fuel | MUSA | 0.016 | 0.5 | 525.78 | 2026-09-10 | 524.47 | 527.09 | -0.6 | 0 |  |  | 2026-09-18 | fixed_hold active from 2026-03-04 to before 2026-09-18 (initial signal 2026-03-03, last same-direction signal 2026-09-10) |
| metals | ATI | 0.02 | 1.5 | 199 | 2026-09-10 | 198.5 | 199.5 | 1.1 | 0.3 |  |  | 2026-09-25 | fixed_hold active from 2026-01-12 to before 2026-09-25 (initial signal 2026-01-09, last same-direction signal 2026-09-10) |
| metals | CRS | 0.015 | 0.5 | 448.25 | 2026-09-10 | 447.13 | 449.37 | 1.1 | 0.3 |  |  | 2026-09-25 | fixed_hold active from 2026-01-12 to before 2026-09-25 (initial signal 2026-01-09, last same-direction signal 2026-09-10) |
| metals | HWM | 0.015 | 1 | 227.91 | 2026-09-10 | 227.34 | 228.48 | 1 | 0.1 |  |  | 2026-09-25 | fixed_hold active from 2026-01-12 to before 2026-09-25 (initial signal 2026-01-09, last same-direction signal 2026-09-10) |
| psx_ref | PSX | -0.05 | -2.9 | 258.51 | 2026-09-10 | 257.86 | 259.16 | 0.1 | 1.1 |  |  | 2026-09-16 | fixed_hold active from 2026-09-09 to before 2026-09-16 (initial signal 2026-09-08, last same-direction signal 2026-09-10) |
| refiner | DK | -0.05 | -10 | 74.89 | 2026-09-10 | 74.7 | 75.08 | 0.2 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | PBF | -0.03 | -5.8 | 77.08 | 2026-09-10 | 76.89 | 77.27 | 0 | 1.7 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | DINO | -0.02 | -2.8 | 107.72 | 2026-09-10 | 107.45 | 107.99 | 0.2 | 1 |  |  |  | 5d rolling-mean band_hysteresis active |
| services | FTI | -0.02 | -4 | 75.58 | 2026-09-10 | 75.39 | 75.77 | 0.6 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -5.4 | 56.01 | 2026-09-10 | 55.87 | 56.15 | 1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4.2 | 36.07 | 2026-09-10 | 35.98 | 36.16 | 0.6 | 1.2 |  |  |  | continuous hysteresis sign active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.154979 | 3.06756 | 757.83 | 2026-09-10 | 755.935 | 759.725 |
| XLE | 0.446664 | 103.187 | 64.93 | 2026-09-10 | 64.7677 | 65.0923 |
| XME | -0.0703459 | -9.19394 | 114.77 | 2026-09-10 | 114.483 | 115.057 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | fuel | CASY | BUY | 1 | 1 | 0.0418427 | False |  | 627.64 | 2026-09-10 | 626.071 | 629.209 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | fuel | MUSA | SELL | -1 | -1 | -0.035052 | False |  | 525.78 | 2026-09-10 | 524.466 | 527.094 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | metals | CRS | BUY | 1 | 1 | 0.0298833 | False |  | 448.25 | 2026-09-10 | 447.129 | 449.371 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | metals | ATI | BUY | 1 | 1 | 0.0132667 | False |  | 199 | 2026-09-10 | 198.502 | 199.498 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | bwt | ERO | BUY | 1 | 1 | 0.002332 | False |  | 34.98 | 2026-09-10 | 34.8925 | 35.0674 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
