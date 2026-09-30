# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-09-22

- Signal as-of date: 2026-09-21
- Target trading date: 2026-09-22
- AUM: $15,000.00
- Gross stock weight: 70.80%
- Single-name stock weight cap: 5.00%
- Net stock weight: -30.80%
- Gross hedge weight: 65.80%
- Total net weight after hedges: 35.00%
- Estimated turnover from current positions: 5.98%
- Full eligible order turnover: 1.52%
- Today's total child-order turnover: 1.45%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $0.54
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.2 | 0.2 | 3000 | 3000 | 5 |
| stock_short_without_hedge | 0.508 | -0.508 | 7620 | -7620 | 16 |
| total_hedge | 0.658018 | 0.658018 | 9870.28 | 9870.28 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | -0.045 | -19.5 | 34.7 | 2026-09-21 | 34.61 | 34.79 | 0.5 | 1.1 |  |  | 2026-09-25 | fixed_hold active from 2026-09-18 to before 2026-09-25 (initial signal 2026-09-17, last same-direction signal 2026-09-21) |
| bwt | TECK | -0.015 | -3.4 | 66.76 | 2026-09-21 | 66.59 | 66.93 | 0.9 | 0.7 |  |  | 2026-09-25 | fixed_hold active from 2026-09-18 to before 2026-09-25 (initial signal 2026-09-17, last same-direction signal 2026-09-21) |
| chemical | DOW | -0.05 | -26.5 | 28.27 | 2026-09-21 | 28.2 | 28.34 | 0.3 | 1.1 |  |  | 2026-10-21 | fixed_hold active from 2026-04-20 to before 2026-10-21 (initial signal 2026-04-17, last same-direction signal 2026-09-21) |
| chemical | LYB | -0.05 | -12.5 | 60.24 | 2026-09-21 | 60.09 | 60.39 | -0 | 1.2 |  |  | 2026-10-21 | fixed_hold active from 2026-04-20 to before 2026-10-21 (initial signal 2026-04-17, last same-direction signal 2026-09-21) |
| chemical | WLK | -0.05 | -11.1 | 67.77 | 2026-09-21 | 67.6 | 67.94 | 0.8 | 0.7 |  |  | 2026-10-21 | fixed_hold active from 2026-04-20 to before 2026-10-21 (initial signal 2026-04-17, last same-direction signal 2026-09-21) |
| chemical | CE | -0.028 | -9.5 | 44.38 | 2026-09-21 | 44.27 | 44.49 | 0.9 | 1 |  |  | 2026-10-21 | fixed_hold active from 2026-04-20 to before 2026-10-21 (initial signal 2026-04-17, last same-direction signal 2026-09-21) |
| chemical | EMN | -0.028 | -6.5 | 65.09 | 2026-09-21 | 64.93 | 65.25 | 1 | 0.2 |  |  | 2026-10-21 | fixed_hold active from 2026-04-20 to before 2026-10-21 (initial signal 2026-04-17, last same-direction signal 2026-09-21) |
| chemical | HUN | -0.028 | -47.4 | 8.86 | 2026-09-21 | 8.84 | 8.88 | 1.4 | 0.7 |  |  | 2026-10-21 | fixed_hold active from 2026-04-20 to before 2026-10-21 (initial signal 2026-04-17, last same-direction signal 2026-09-21) |
| chemical | AVNT | -0.014 | -5.2 | 40.44 | 2026-09-21 | 40.34 | 40.54 | 1.1 | -0 |  |  | 2026-10-21 | fixed_hold active from 2026-04-20 to before 2026-10-21 (initial signal 2026-04-17, last same-direction signal 2026-09-21) |
| psx_ref | PSX | -0.05 | -2.9 | 261.75 | 2026-09-21 | 261.1 | 262.4 | 0.1 | 1.1 |  |  | 2026-09-25 | fixed_hold active from 2026-09-09 to before 2026-09-25 (initial signal 2026-09-08, last same-direction signal 2026-09-21) |
| refiner | DK | -0.05 | -10.1 | 74.37 | 2026-09-21 | 74.18 | 74.56 | 0.2 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | PBF | -0.03 | -6.2 | 72.48 | 2026-09-21 | 72.3 | 72.66 | 0 | 1.7 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | DINO | -0.02 | -2.7 | 109.29 | 2026-09-21 | 109.02 | 109.56 | 0.1 | 1 |  |  |  | 5d rolling-mean band_hysteresis active |
| services | FTI | -0.02 | -4.2 | 71.31 | 2026-09-21 | 71.13 | 71.49 | 0.6 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -5.8 | 51.76 | 2026-09-21 | 51.63 | 51.89 | 1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4.5 | 33.39 | 2026-09-21 | 33.31 | 33.47 | 0.6 | 1.2 |  |  |  | continuous hysteresis sign active |
| shipping | DHT | 0.05 | 33.4 | 22.45 | 2026-09-21 | 22.39 | 22.51 | 0.3 | 0 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | FRO | 0.05 | 15.1 | 49.81 | 2026-09-21 | 49.69 | 49.93 | 0.5 | 0.2 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | INSW | 0.05 | 6.9 | 109.1 | 2026-09-21 | 108.83 | 109.37 | 0.3 | 0.2 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | TNK | 0.0375 | 5.7 | 98.76 | 2026-09-21 | 98.51 | 99.01 | 0.3 | 0.2 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | STNG | 0.0125 | 2.2 | 86.21 | 2026-09-21 | 85.99 | 86.43 | 0.3 | 0.3 |  |  |  | 2d rolling-mean shipping_sticky_accel active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.185711 | 3.60139 | 773.5 | 2026-09-21 | 771.566 | 775.434 |
| XLE | 0.413668 | 99.3439 | 62.46 | 2026-09-21 | 62.3038 | 62.6161 |
| XME | 0.0586391 | 8.06961 | 109 | 2026-09-21 | 108.728 | 109.272 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | chemical | DOW | SELL | -2 | -2 | -0.00376933 | False |  | 28.27 | 2026-09-21 | 28.1993 | 28.3407 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | chemical | HUN | SELL | -4 | -4 | -0.00236267 | False |  | 8.86 | 2026-09-21 | 8.83785 | 8.88215 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XLE | BUY | 2 | 2 | 0.008328 | False |  | 62.46 | 2026-09-21 | 62.3038 | 62.6161 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
