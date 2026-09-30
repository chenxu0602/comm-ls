# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-09-29

- Signal as-of date: 2026-09-28
- Target trading date: 2026-09-29
- AUM: $15,000.00
- Gross stock weight: 66.80%
- Single-name stock weight cap: 5.00%
- Net stock weight: -2.80%
- Gross hedge weight: 34.35%
- Total net weight after hedges: 19.63%
- Estimated turnover from current positions: 17.12%
- Full eligible order turnover: 14.19%
- Today's total child-order turnover: 15.66%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $5.87
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.32 | 0.32 | 4800 | 4800 | 10 |
| stock_short_without_hedge | 0.348 | -0.348 | 5220 | -5220 | 11 |
| total_hedge | 0.343453 | 0.224267 | 5151.79 | 3364.01 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.045 | 18 | 37.41 | 2026-09-28 | 37.32 | 37.5 | 0.4 | 1.1 |  |  | 2026-10-02 | fixed_hold active from 2026-09-28 to before 2026-10-02 (initial signal 2026-09-25, last same-direction signal 2026-09-28) |
| bwt | TECK | 0.015 | 3.5 | 65.16 | 2026-09-28 | 65 | 65.32 | 0.9 | 0.7 |  |  | 2026-10-02 | fixed_hold active from 2026-09-28 to before 2026-10-02 (initial signal 2026-09-25, last same-direction signal 2026-09-28) |
| chemical | DOW | -0.05 | -26.9 | 27.89 | 2026-09-28 | 27.82 | 27.96 | 0.3 | 1.2 |  |  | 2026-10-28 | fixed_hold active from 2026-04-20 to before 2026-10-28 (initial signal 2026-04-17, last same-direction signal 2026-09-28) |
| chemical | LYB | -0.05 | -12.9 | 58.27 | 2026-09-28 | 58.12 | 58.42 | -0 | 1.2 |  |  | 2026-10-28 | fixed_hold active from 2026-04-20 to before 2026-10-28 (initial signal 2026-04-17, last same-direction signal 2026-09-28) |
| chemical | WLK | -0.05 | -11.2 | 66.84 | 2026-09-28 | 66.67 | 67.01 | 0.8 | 0.7 |  |  | 2026-10-28 | fixed_hold active from 2026-04-20 to before 2026-10-28 (initial signal 2026-04-17, last same-direction signal 2026-09-28) |
| chemical | CE | -0.028 | -9.1 | 45.92 | 2026-09-28 | 45.81 | 46.03 | 0.9 | 1 |  |  | 2026-10-28 | fixed_hold active from 2026-04-20 to before 2026-10-28 (initial signal 2026-04-17, last same-direction signal 2026-09-28) |
| chemical | EMN | -0.028 | -6.3 | 66.47 | 2026-09-28 | 66.3 | 66.64 | 1 | 0.2 |  |  | 2026-10-28 | fixed_hold active from 2026-04-20 to before 2026-10-28 (initial signal 2026-04-17, last same-direction signal 2026-09-28) |
| chemical | HUN | -0.028 | -48.7 | 8.63 | 2026-09-28 | 8.61 | 8.65 | 1.4 | 0.7 |  |  | 2026-10-28 | fixed_hold active from 2026-04-20 to before 2026-10-28 (initial signal 2026-04-17, last same-direction signal 2026-09-28) |
| chemical | AVNT | -0.014 | -5.1 | 41.19 | 2026-09-28 | 41.09 | 41.29 | 1.1 | -0 |  |  | 2026-10-28 | fixed_hold active from 2026-04-20 to before 2026-10-28 (initial signal 2026-04-17, last same-direction signal 2026-09-28) |
| psx_ref | PSX | -0.05 | -3 | 253.55 | 2026-09-28 | 252.92 | 254.18 | 0.1 | 1.1 |  |  | 2026-10-02 | fixed_hold active from 2026-09-09 to before 2026-10-02 (initial signal 2026-09-08, last same-direction signal 2026-09-28) |
| refiner | DK | 0.03 | 6.7 | 67.47 | 2026-09-28 | 67.3 | 67.64 | 0.2 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | PBF | 0.018 | 3.6 | 74.39 | 2026-09-28 | 74.2 | 74.58 | 0 | 1.7 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | DINO | 0.012 | 1.7 | 106.19 | 2026-09-28 | 105.92 | 106.46 | 0.1 | 1 |  |  |  | 5d rolling-mean band_hysteresis active |
| services | FTI | -0.02 | -4.2 | 70.62 | 2026-09-28 | 70.44 | 70.8 | 0.6 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -5.8 | 51.49 | 2026-09-28 | 51.36 | 51.62 | 1.1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4.6 | 32.43 | 2026-09-28 | 32.35 | 32.51 | 0.6 | 1.2 |  |  |  | continuous hysteresis sign active |
| shipping | DHT | 0.05 | 34.2 | 21.9 | 2026-09-28 | 21.85 | 21.95 | 0.3 | 0 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | FRO | 0.05 | 15.6 | 48.1 | 2026-09-28 | 47.98 | 48.22 | 0.5 | 0.2 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | INSW | 0.05 | 6.9 | 108.31 | 2026-09-28 | 108.04 | 108.58 | 0.3 | 0.2 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | TNK | 0.0375 | 5.9 | 95.71 | 2026-09-28 | 95.47 | 95.95 | 0.3 | 0.2 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | STNG | 0.0125 | 2.3 | 83.19 | 2026-09-28 | 82.98 | 83.4 | 0.3 | 0.3 |  |  |  | 2d rolling-mean shipping_sticky_accel active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.0925024 | 1.81233 | 765.61 | 2026-09-28 | 763.696 | 767.524 |
| XLE | 0.191357 | 46.2216 | 62.1 | 2026-09-28 | 61.9447 | 62.2552 |
| XME | -0.0595927 | -8.47933 | 105.42 | 2026-09-28 | 105.156 | 105.684 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | refiner | DK | BUY | 7 | 7 | 0.031486 | False |  | 67.47 | 2026-09-28 | 67.3013 | 67.6387 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | PBF | BUY | 4 | 4 | 0.0198373 | False |  | 74.39 | 2026-09-28 | 74.204 | 74.576 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | DINO | BUY | 2 | 2 | 0.0141587 | False |  | 106.19 | 2026-09-28 | 105.925 | 106.455 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XLE | SELL | -20 | -22 | -0.09108 | False |  | 62.1 | 2026-09-28 | 61.9447 | 62.2552 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
