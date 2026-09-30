# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-09-28

- Signal as-of date: 2026-09-25
- Target trading date: 2026-09-28
- AUM: $15,000.00
- Gross stock weight: 62.80%
- Single-name stock weight cap: 5.00%
- Net stock weight: -6.80%
- Gross hedge weight: 40.13%
- Total net weight after hedges: 21.46%
- Estimated turnover from current positions: 28.73%
- Full eligible order turnover: 27.47%
- Today's total child-order turnover: 21.79%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $8.17
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.28 | 0.28 | 4200 | 4200 | 10 |
| stock_short_without_hedge | 0.348 | -0.348 | 5220 | -5220 | 11 |
| total_hedge | 0.401315 | 0.282599 | 6019.73 | 4238.99 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.045 | 17.8 | 37.87 | 2026-09-25 | 37.78 | 37.96 | 0.5 | 1.1 |  |  | 2026-10-01 | fixed_hold active from 2026-09-28 to before 2026-10-01 (initial signal 2026-09-25, last same-direction signal 2026-09-25) |
| bwt | TECK | 0.015 | 3.4 | 66.05 | 2026-09-25 | 65.88 | 66.22 | 0.9 | 0.7 |  |  | 2026-10-01 | fixed_hold active from 2026-09-28 to before 2026-10-01 (initial signal 2026-09-25, last same-direction signal 2026-09-25) |
| chemical | DOW | -0.05 | -26.8 | 28.02 | 2026-09-25 | 27.95 | 28.09 | 0.3 | 1.2 |  |  | 2026-10-27 | fixed_hold active from 2026-04-20 to before 2026-10-27 (initial signal 2026-04-17, last same-direction signal 2026-09-25) |
| chemical | LYB | -0.05 | -12.9 | 58.14 | 2026-09-25 | 57.99 | 58.29 | -0 | 1.2 |  |  | 2026-10-27 | fixed_hold active from 2026-04-20 to before 2026-10-27 (initial signal 2026-04-17, last same-direction signal 2026-09-25) |
| chemical | WLK | -0.05 | -11.1 | 67.71 | 2026-09-25 | 67.54 | 67.88 | 0.8 | 0.7 |  |  | 2026-10-27 | fixed_hold active from 2026-04-20 to before 2026-10-27 (initial signal 2026-04-17, last same-direction signal 2026-09-25) |
| chemical | CE | -0.028 | -8.9 | 47.09 | 2026-09-25 | 46.97 | 47.21 | 0.9 | 0.9 |  |  | 2026-10-27 | fixed_hold active from 2026-04-20 to before 2026-10-27 (initial signal 2026-04-17, last same-direction signal 2026-09-25) |
| chemical | EMN | -0.028 | -6.3 | 66.97 | 2026-09-25 | 66.8 | 67.14 | 1 | 0.2 |  |  | 2026-10-27 | fixed_hold active from 2026-04-20 to before 2026-10-27 (initial signal 2026-04-17, last same-direction signal 2026-09-25) |
| chemical | HUN | -0.028 | -47.2 | 8.9 | 2026-09-25 | 8.88 | 8.92 | 1.4 | 0.7 |  |  | 2026-10-27 | fixed_hold active from 2026-04-20 to before 2026-10-27 (initial signal 2026-04-17, last same-direction signal 2026-09-25) |
| chemical | AVNT | -0.014 | -5.1 | 41.28 | 2026-09-25 | 41.18 | 41.38 | 1.1 | -0 |  |  | 2026-10-27 | fixed_hold active from 2026-04-20 to before 2026-10-27 (initial signal 2026-04-17, last same-direction signal 2026-09-25) |
| psx_ref | PSX | -0.05 | -2.9 | 255.75 | 2026-09-25 | 255.11 | 256.39 | 0.1 | 1.1 |  |  | 2026-10-01 | fixed_hold active from 2026-09-09 to before 2026-10-01 (initial signal 2026-09-08, last same-direction signal 2026-09-25) |
| refiner | DK | 0.01 | 2.2 | 67.84 | 2026-09-25 | 67.67 | 68.01 | 0.2 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | PBF | 0.006 | 1.2 | 73.69 | 2026-09-25 | 73.51 | 73.87 | 0 | 1.7 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | DINO | 0.004 | 0.6 | 106.82 | 2026-09-25 | 106.55 | 107.09 | 0.1 | 1 |  |  |  | 5d rolling-mean band_hysteresis active |
| services | FTI | -0.02 | -4.2 | 70.99 | 2026-09-25 | 70.81 | 71.17 | 0.6 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -5.8 | 51.54 | 2026-09-25 | 51.41 | 51.67 | 1.1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4.6 | 32.76 | 2026-09-25 | 32.68 | 32.84 | 0.6 | 1.2 |  |  |  | continuous hysteresis sign active |
| shipping | DHT | 0.05 | 34.4 | 21.78 | 2026-09-25 | 21.73 | 21.83 | 0.3 | 0 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | FRO | 0.05 | 15.7 | 47.73 | 2026-09-25 | 47.61 | 47.85 | 0.5 | 0.2 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | INSW | 0.05 | 7.1 | 105.64 | 2026-09-25 | 105.38 | 105.9 | 0.3 | 0.2 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | TNK | 0.0375 | 6 | 94.07 | 2026-09-25 | 93.83 | 94.31 | 0.3 | 0.2 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | STNG | 0.0125 | 2.3 | 81.49 | 2026-09-25 | 81.29 | 81.69 | 0.3 | 0.3 |  |  |  | 2d rolling-mean shipping_sticky_accel active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.0965099 | 1.87677 | 771.35 | 2026-09-25 | 769.422 | 773.278 |
| XLE | 0.245448 | 59.3442 | 62.04 | 2026-09-25 | 61.8849 | 62.1951 |
| XME | -0.059358 | -8.21905 | 108.33 | 2026-09-25 | 108.059 | 108.601 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | bwt | ERO | BUY | 18 | 18 | 0.045444 | False |  | 37.87 | 2026-09-25 | 37.7753 | 37.9647 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | DK | BUY | 4 | 2 | 0.00904533 | True |  | 67.84 | 2026-09-25 | 67.6704 | 68.0096 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | bwt | TECK | BUY | 3 | 3 | 0.01321 | False |  | 66.05 | 2026-09-25 | 65.8849 | 66.2151 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | DINO | BUY | 2 | 1 | 0.00712133 | True |  | 106.82 | 2026-09-25 | 106.553 | 107.087 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | PBF | BUY | 2 | 1 | 0.00491267 | True |  | 73.69 | 2026-09-25 | 73.5058 | 73.8742 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XME | SELL | -8 | -8 | -0.057776 | False |  | 108.33 | 2026-09-25 | 108.059 | 108.601 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
| hedge | hedge | SPY | SELL | -1 | -1 | -0.0514233 | False |  | 771.35 | 2026-09-25 | 769.422 | 773.278 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XLE | SELL | -14 | -7 | -0.028952 | False |  | 62.04 | 2026-09-25 | 61.8849 | 62.1951 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
