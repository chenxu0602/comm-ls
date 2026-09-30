# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-09-21

- Signal as-of date: 2026-09-18
- Target trading date: 2026-09-21
- AUM: $15,000.00
- Gross stock weight: 70.80%
- Single-name stock weight cap: 5.00%
- Net stock weight: -30.80%
- Gross hedge weight: 65.76%
- Total net weight after hedges: 34.96%
- Estimated turnover from current positions: 13.26%
- Full eligible order turnover: 9.23%
- Today's total child-order turnover: 9.74%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $3.65
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.2 | 0.2 | 3000 | 3000 | 5 |
| stock_short_without_hedge | 0.508 | -0.508 | 7620 | -7620 | 16 |
| total_hedge | 0.657629 | 0.657629 | 9864.44 | 9864.44 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | -0.045 | -19.8 | 34.17 | 2026-09-18 | 34.08 | 34.26 | 0.5 | 1.1 |  |  | 2026-09-24 | fixed_hold active from 2026-09-18 to before 2026-09-24 (initial signal 2026-09-17, last same-direction signal 2026-09-18) |
| bwt | TECK | -0.015 | -3.4 | 65.52 | 2026-09-18 | 65.36 | 65.68 | 0.9 | 0.7 |  |  | 2026-09-24 | fixed_hold active from 2026-09-18 to before 2026-09-24 (initial signal 2026-09-17, last same-direction signal 2026-09-18) |
| chemical | DOW | -0.05 | -26.1 | 28.73 | 2026-09-18 | 28.66 | 28.8 | 0.3 | 1.2 |  |  | 2026-10-20 | fixed_hold active from 2026-04-20 to before 2026-10-20 (initial signal 2026-04-17, last same-direction signal 2026-09-18) |
| chemical | LYB | -0.05 | -12.1 | 61.93 | 2026-09-18 | 61.78 | 62.08 | -0 | 1.2 |  |  | 2026-10-20 | fixed_hold active from 2026-04-20 to before 2026-10-20 (initial signal 2026-04-17, last same-direction signal 2026-09-18) |
| chemical | WLK | -0.05 | -10.9 | 69.07 | 2026-09-18 | 68.9 | 69.24 | 0.8 | 0.7 |  |  | 2026-10-20 | fixed_hold active from 2026-04-20 to before 2026-10-20 (initial signal 2026-04-17, last same-direction signal 2026-09-18) |
| chemical | CE | -0.028 | -9.2 | 45.41 | 2026-09-18 | 45.3 | 45.52 | 0.9 | 0.9 |  |  | 2026-10-20 | fixed_hold active from 2026-04-20 to before 2026-10-20 (initial signal 2026-04-17, last same-direction signal 2026-09-18) |
| chemical | EMN | -0.028 | -6.4 | 65.69 | 2026-09-18 | 65.53 | 65.85 | 1 | 0.2 |  |  | 2026-10-20 | fixed_hold active from 2026-04-20 to before 2026-10-20 (initial signal 2026-04-17, last same-direction signal 2026-09-18) |
| chemical | HUN | -0.028 | -46.2 | 9.09 | 2026-09-18 | 9.07 | 9.11 | 1.4 | 0.7 |  |  | 2026-10-20 | fixed_hold active from 2026-04-20 to before 2026-10-20 (initial signal 2026-04-17, last same-direction signal 2026-09-18) |
| chemical | AVNT | -0.014 | -5.2 | 40.36 | 2026-09-18 | 40.26 | 40.46 | 1.2 | -0 |  |  | 2026-10-20 | fixed_hold active from 2026-04-20 to before 2026-10-20 (initial signal 2026-04-17, last same-direction signal 2026-09-18) |
| psx_ref | PSX | -0.05 | -2.7 | 273.13 | 2026-09-18 | 272.45 | 273.81 | 0.1 | 1.1 |  |  | 2026-09-24 | fixed_hold active from 2026-09-09 to before 2026-09-24 (initial signal 2026-09-08, last same-direction signal 2026-09-18) |
| refiner | DK | -0.05 | -9.6 | 78.12 | 2026-09-18 | 77.92 | 78.32 | 0.2 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | PBF | -0.03 | -5.8 | 77.19 | 2026-09-18 | 77 | 77.38 | 0 | 1.7 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | DINO | -0.02 | -2.6 | 115.9 | 2026-09-18 | 115.61 | 116.19 | 0.2 | 1 |  |  |  | 5d rolling-mean band_hysteresis active |
| services | FTI | -0.02 | -4.2 | 72.02 | 2026-09-18 | 71.84 | 72.2 | 0.6 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -5.9 | 51.12 | 2026-09-18 | 50.99 | 51.25 | 1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4.5 | 33.64 | 2026-09-18 | 33.56 | 33.72 | 0.6 | 1.2 |  |  |  | continuous hysteresis sign active |
| shipping | DHT | 0.05 | 32.2 | 23.27 | 2026-09-18 | 23.21 | 23.33 | 0.3 | 0 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | FRO | 0.05 | 14.6 | 51.42 | 2026-09-18 | 51.29 | 51.55 | 0.5 | 0.2 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | INSW | 0.05 | 6.7 | 111.15 | 2026-09-18 | 110.87 | 111.43 | 0.3 | 0.2 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | TNK | 0.0375 | 5.6 | 100.92 | 2026-09-18 | 100.67 | 101.17 | 0.3 | 0.2 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | STNG | 0.0125 | 2.2 | 87.16 | 2026-09-18 | 86.94 | 87.38 | 0.3 | 0.3 |  |  |  | 2d rolling-mean shipping_sticky_accel active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.185092 | 3.64502 | 761.69 | 2026-09-18 | 759.786 | 763.594 |
| XLE | 0.413943 | 96.5502 | 64.31 | 2026-09-18 | 64.1492 | 64.4708 |
| XME | 0.0585949 | 8.08726 | 108.68 | 2026-09-18 | 108.408 | 108.952 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | shipping | INSW | BUY | 4 | 4 | 0.02964 | False |  | 111.15 | 2026-09-18 | 110.872 | 111.428 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | TNK | BUY | 3 | 3 | 0.020184 | False |  | 100.92 | 2026-09-18 | 100.668 | 101.172 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | FRO | BUY | 5 | 5 | 0.01714 | False |  | 51.42 | 2026-09-18 | 51.2914 | 51.5485 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | DHT | BUY | 7 | 7 | 0.0108593 | False |  | 23.27 | 2026-09-18 | 23.2118 | 23.3282 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | STNG | BUY | 1 | 1 | 0.00581067 | False |  | 87.16 | 2026-09-18 | 86.9421 | 87.3779 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | DK | SELL | -1 | -1 | -0.005208 | False |  | 78.12 | 2026-09-18 | 77.9247 | 78.3153 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XLE | SELL | -2 | -2 | -0.00857467 | False |  | 64.31 | 2026-09-18 | 64.1492 | 64.4708 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
