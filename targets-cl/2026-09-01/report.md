# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-09-01

- Signal as-of date: 2026-08-31
- Target trading date: 2026-09-01
- AUM: $15,000.00
- Gross stock weight: 53.80%
- Single-name stock weight cap: 5.00%
- Net stock weight: -5.80%
- Gross hedge weight: 33.69%
- Total net weight after hedges: 13.82%
- Estimated turnover from current positions: 20.40%
- Full eligible order turnover: 10.52%
- Today's total child-order turnover: 10.32%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $3.87
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.24 | 0.24 | 3600 | 3600 | 11 |
| stock_short_without_hedge | 0.298 | -0.298 | 4470 | -4470 | 10 |
| total_hedge | 0.336931 | 0.196193 | 5053.96 | 2942.89 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.045 | 18.2 | 37.13 | 2026-08-31 | 37.04 | 37.22 | 0.4 | 1.1 |  |  | 2026-09-04 | fixed_hold active from 2026-08-04 to before 2026-09-04 (initial signal 2026-08-03, last same-direction signal 2026-08-31) |
| bwt | TECK | 0.015 | 3.3 | 68.12 | 2026-08-31 | 67.95 | 68.29 | 0.9 | 0.7 |  |  | 2026-09-04 | fixed_hold active from 2026-08-04 to before 2026-09-04 (initial signal 2026-08-03, last same-direction signal 2026-08-31) |
| chemical | DOW | -0.05 | -24.6 | 30.52 | 2026-08-31 | 30.44 | 30.6 | 0.3 | 1.2 |  |  | 2026-09-30 | fixed_hold active from 2026-04-20 to before 2026-09-30 (initial signal 2026-04-17, last same-direction signal 2026-08-31) |
| chemical | LYB | -0.05 | -11.5 | 65.08 | 2026-08-31 | 64.92 | 65.24 | 0 | 1.1 |  |  | 2026-09-30 | fixed_hold active from 2026-04-20 to before 2026-09-30 (initial signal 2026-04-17, last same-direction signal 2026-08-31) |
| chemical | WLK | -0.05 | -10 | 75.07 | 2026-08-31 | 74.88 | 75.26 | 0.9 | 0.7 |  |  | 2026-09-30 | fixed_hold active from 2026-04-20 to before 2026-09-30 (initial signal 2026-04-17, last same-direction signal 2026-08-31) |
| chemical | CE | -0.028 | -9.2 | 45.48 | 2026-08-31 | 45.37 | 45.59 | 0.9 | 0.9 |  |  | 2026-09-30 | fixed_hold active from 2026-04-20 to before 2026-09-30 (initial signal 2026-04-17, last same-direction signal 2026-08-31) |
| chemical | EMN | -0.028 | -5.8 | 72.44 | 2026-08-31 | 72.26 | 72.62 | 1 | 0.2 |  |  | 2026-09-30 | fixed_hold active from 2026-04-20 to before 2026-09-30 (initial signal 2026-04-17, last same-direction signal 2026-08-31) |
| chemical | HUN | -0.028 | -43.8 | 9.58 | 2026-08-31 | 9.56 | 9.6 | 1.5 | 0.7 |  |  | 2026-09-30 | fixed_hold active from 2026-04-20 to before 2026-09-30 (initial signal 2026-04-17, last same-direction signal 2026-08-31) |
| chemical | AVNT | -0.014 | -4.8 | 44.06 | 2026-08-31 | 43.95 | 44.17 | 1.2 | -0 |  |  | 2026-09-30 | fixed_hold active from 2026-04-20 to before 2026-09-30 (initial signal 2026-04-17, last same-direction signal 2026-08-31) |
| fuel | CASY | 0.024 | 0.5 | 752.21 | 2026-08-31 | 750.33 | 754.09 | -0.1 | 0 |  |  | 2026-09-08 | fixed_hold active from 2026-03-04 to before 2026-09-08 (initial signal 2026-03-03, last same-direction signal 2026-08-31) |
| fuel | MUSA | 0.016 | 0.5 | 515.39 | 2026-08-31 | 514.1 | 516.68 | -0.6 | 0 |  |  | 2026-09-08 | fixed_hold active from 2026-03-04 to before 2026-09-08 (initial signal 2026-03-03, last same-direction signal 2026-08-31) |
| metals | ATI | 0.02 | 1.5 | 204.2 | 2026-08-31 | 203.69 | 204.71 | 1 | 0.3 |  |  | 2026-09-15 | fixed_hold active from 2026-01-12 to before 2026-09-15 (initial signal 2026-01-09, last same-direction signal 2026-08-31) |
| metals | CRS | 0.015 | 0.5 | 476.42 | 2026-08-31 | 475.23 | 477.61 | 1.1 | 0.3 |  |  | 2026-09-15 | fixed_hold active from 2026-01-12 to before 2026-09-15 (initial signal 2026-01-09, last same-direction signal 2026-08-31) |
| metals | HWM | 0.015 | 0.9 | 244.95 | 2026-08-31 | 244.34 | 245.56 | 0.9 | 0.1 |  |  | 2026-09-15 | fixed_hold active from 2026-01-12 to before 2026-09-15 (initial signal 2026-01-09, last same-direction signal 2026-08-31) |
| psx_ref | PSX | 0.03 | 1.8 | 246.58 | 2026-08-31 | 245.96 | 247.2 | 0.1 | 1.1 |  |  | 2026-09-04 | fixed_hold active from 2026-08-28 to before 2026-09-04 (initial signal 2026-08-27, last same-direction signal 2026-08-31) |
| refiner | DK | 0.03 | 6.1 | 74.34 | 2026-08-31 | 74.15 | 74.53 | 0.1 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | PBF | 0.018 | 3.7 | 72.99 | 2026-08-31 | 72.81 | 73.17 | -0 | 1.7 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | DINO | 0.012 | 1.8 | 101.61 | 2026-08-31 | 101.36 | 101.86 | 0.2 | 1 |  |  |  | 5d rolling-mean band_hysteresis active |
| services | FTI | -0.02 | -3.8 | 78.15 | 2026-08-31 | 77.95 | 78.35 | 0.6 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -5 | 60.1 | 2026-08-31 | 59.95 | 60.25 | 1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4.1 | 36.85 | 2026-08-31 | 36.76 | 36.94 | 0.6 | 1.2 |  |  |  | continuous hysteresis sign active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.131334 | 2.56829 | 767.05 | 2026-08-31 | 765.132 | 768.968 |
| XLE | 0.135228 | 31.7138 | 63.96 | 2026-08-31 | 63.8001 | 64.1199 |
| XME | -0.070369 | -8.93537 | 118.13 | 2026-08-31 | 117.835 | 118.425 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | refiner | DK | SELL | -5 | -5 | -0.02478 | False |  | 74.34 | 2026-08-31 | 74.1541 | 74.5258 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | PBF | SELL | -2 | -2 | -0.009732 | False |  | 72.99 | 2026-08-31 | 72.8075 | 73.1725 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | DINO | SELL | -1 | -1 | -0.006774 | False |  | 101.61 | 2026-08-31 | 101.356 | 101.864 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | services | SLB | BUY | 1 | 1 | 0.00400667 | False |  | 60.1 | 2026-08-31 | 59.9497 | 60.2502 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | bwt | ERO | BUY | 1 | 1 | 0.00247533 | False |  | 37.13 | 2026-08-31 | 37.0372 | 37.2228 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XLE | BUY | 13 | 13 | 0.055432 | False |  | 63.96 | 2026-08-31 | 63.8001 | 64.1199 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
