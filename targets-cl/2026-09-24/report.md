# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-09-24

- Signal as-of date: 2026-09-23
- Target trading date: 2026-09-24
- AUM: $15,000.00
- Gross stock weight: 66.80%
- Single-name stock weight cap: 5.00%
- Net stock weight: -26.80%
- Gross hedge weight: 59.22%
- Total net weight after hedges: 32.42%
- Estimated turnover from current positions: 14.23%
- Full eligible order turnover: 12.06%
- Today's total child-order turnover: 8.56%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $3.21
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.2 | 0.2 | 3000 | 3000 | 5 |
| stock_short_without_hedge | 0.468 | -0.468 | 7020 | -7020 | 16 |
| total_hedge | 0.59216 | 0.59216 | 8882.39 | 8882.39 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | -0.045 | -18.5 | 36.48 | 2026-09-23 | 36.39 | 36.57 | 0.5 | 1.1 |  |  | 2026-09-25 | fixed_hold active from 2026-09-18 to before 2026-09-25 (initial signal 2026-09-17, last same-direction signal 2026-09-21) |
| bwt | TECK | -0.015 | -3.4 | 66.8 | 2026-09-23 | 66.63 | 66.97 | 0.9 | 0.7 |  |  | 2026-09-25 | fixed_hold active from 2026-09-18 to before 2026-09-25 (initial signal 2026-09-17, last same-direction signal 2026-09-21) |
| chemical | DOW | -0.05 | -26.2 | 28.65 | 2026-09-23 | 28.58 | 28.72 | 0.3 | 1.1 |  |  | 2026-10-23 | fixed_hold active from 2026-04-20 to before 2026-10-23 (initial signal 2026-04-17, last same-direction signal 2026-09-23) |
| chemical | LYB | -0.05 | -12.5 | 59.97 | 2026-09-23 | 59.82 | 60.12 | -0 | 1.2 |  |  | 2026-10-23 | fixed_hold active from 2026-04-20 to before 2026-10-23 (initial signal 2026-04-17, last same-direction signal 2026-09-23) |
| chemical | WLK | -0.05 | -11 | 68.42 | 2026-09-23 | 68.25 | 68.59 | 0.8 | 0.7 |  |  | 2026-10-23 | fixed_hold active from 2026-04-20 to before 2026-10-23 (initial signal 2026-04-17, last same-direction signal 2026-09-23) |
| chemical | CE | -0.028 | -8.7 | 48.49 | 2026-09-23 | 48.37 | 48.61 | 0.9 | 0.9 |  |  | 2026-10-23 | fixed_hold active from 2026-04-20 to before 2026-10-23 (initial signal 2026-04-17, last same-direction signal 2026-09-23) |
| chemical | EMN | -0.028 | -6.3 | 66.8 | 2026-09-23 | 66.63 | 66.97 | 1 | 0.2 |  |  | 2026-10-23 | fixed_hold active from 2026-04-20 to before 2026-10-23 (initial signal 2026-04-17, last same-direction signal 2026-09-23) |
| chemical | HUN | -0.028 | -46.2 | 9.1 | 2026-09-23 | 9.08 | 9.12 | 1.4 | 0.7 |  |  | 2026-10-23 | fixed_hold active from 2026-04-20 to before 2026-10-23 (initial signal 2026-04-17, last same-direction signal 2026-09-23) |
| chemical | AVNT | -0.014 | -5.1 | 40.97 | 2026-09-23 | 40.87 | 41.07 | 1.1 | -0 |  |  | 2026-10-23 | fixed_hold active from 2026-04-20 to before 2026-10-23 (initial signal 2026-04-17, last same-direction signal 2026-09-23) |
| psx_ref | PSX | -0.05 | -2.9 | 256.48 | 2026-09-23 | 255.84 | 257.12 | 0.1 | 1.1 |  |  | 2026-09-29 | fixed_hold active from 2026-09-09 to before 2026-09-29 (initial signal 2026-09-08, last same-direction signal 2026-09-23) |
| refiner | DK | -0.03 | -6.2 | 72.26 | 2026-09-23 | 72.08 | 72.44 | 0.2 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | PBF | -0.018 | -3.8 | 70.47 | 2026-09-23 | 70.29 | 70.65 | 0 | 1.7 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | DINO | -0.012 | -1.7 | 106.14 | 2026-09-23 | 105.87 | 106.41 | 0.1 | 1 |  |  |  | 5d rolling-mean band_hysteresis active |
| services | FTI | -0.02 | -4.2 | 71.24 | 2026-09-23 | 71.06 | 71.42 | 0.6 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -5.8 | 51.87 | 2026-09-23 | 51.74 | 52 | 1.1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4.5 | 33.01 | 2026-09-23 | 32.93 | 33.09 | 0.6 | 1.2 |  |  |  | continuous hysteresis sign active |
| shipping | DHT | 0.05 | 35.2 | 21.28 | 2026-09-23 | 21.23 | 21.33 | 0.3 | 0 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | FRO | 0.05 | 15.8 | 47.56 | 2026-09-23 | 47.44 | 47.68 | 0.5 | 0.2 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | INSW | 0.05 | 7.4 | 101.96 | 2026-09-23 | 101.71 | 102.21 | 0.3 | 0.2 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | TNK | 0.0375 | 5.9 | 94.54 | 2026-09-23 | 94.3 | 94.78 | 0.3 | 0.2 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | STNG | 0.0125 | 2.3 | 81.25 | 2026-09-23 | 81.05 | 81.45 | 0.3 | 0.3 |  |  |  | 2d rolling-mean shipping_sticky_accel active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.178791 | 3.49288 | 767.81 | 2026-09-23 | 765.89 | 769.73 |
| XLE | 0.354547 | 85.2687 | 62.37 | 2026-09-23 | 62.2141 | 62.5259 |
| XME | 0.0588211 | 8.05181 | 109.58 | 2026-09-23 | 109.306 | 109.854 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | refiner | DK | BUY | 4 | 4 | 0.0192693 | False |  | 72.26 | 2026-09-23 | 72.0794 | 72.4407 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | PBF | BUY | 2 | 2 | 0.009396 | False |  | 70.47 | 2026-09-23 | 70.2938 | 70.6462 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | DINO | BUY | 1 | 1 | 0.007076 | False |  | 106.14 | 2026-09-23 | 105.875 | 106.405 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XLE | SELL | -14 | -12 | -0.049896 | False |  | 62.37 | 2026-09-23 | 62.2141 | 62.5259 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
