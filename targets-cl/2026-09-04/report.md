# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-09-04

- Signal as-of date: 2026-09-03
- Target trading date: 2026-09-04
- AUM: $15,000.00
- Gross stock weight: 51.80%
- Single-name stock weight cap: 5.00%
- Net stock weight: -19.80%
- Gross hedge weight: 53.26%
- Total net weight after hedges: 19.68%
- Estimated turnover from current positions: 21.65%
- Full eligible order turnover: 12.12%
- Today's total child-order turnover: 12.78%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $4.79
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.16 | 0.16 | 2400 | 2400 | 8 |
| stock_short_without_hedge | 0.358 | -0.358 | 5370 | -5370 | 13 |
| total_hedge | 0.532633 | 0.394756 | 7989.49 | 5921.34 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.045 | 19.1 | 35.32 | 2026-09-03 | 35.23 | 35.41 | 0.5 | 1 |  |  | 2026-09-09 | fixed_hold active from 2026-08-04 to before 2026-09-09 (initial signal 2026-08-03, last same-direction signal 2026-09-03) |
| bwt | TECK | 0.015 | 3.3 | 68.82 | 2026-09-03 | 68.65 | 68.99 | 0.9 | 0.7 |  |  | 2026-09-09 | fixed_hold active from 2026-08-04 to before 2026-09-09 (initial signal 2026-08-03, last same-direction signal 2026-09-03) |
| chemical | DOW | -0.05 | -24.7 | 30.36 | 2026-09-03 | 30.28 | 30.44 | 0.3 | 1.2 |  |  | 2026-10-05 | fixed_hold active from 2026-04-20 to before 2026-10-05 (initial signal 2026-04-17, last same-direction signal 2026-09-03) |
| chemical | LYB | -0.05 | -11.6 | 64.76 | 2026-09-03 | 64.6 | 64.92 | -0 | 1.1 |  |  | 2026-10-05 | fixed_hold active from 2026-04-20 to before 2026-10-05 (initial signal 2026-04-17, last same-direction signal 2026-09-03) |
| chemical | WLK | -0.05 | -10.1 | 74.6 | 2026-09-03 | 74.41 | 74.79 | 0.9 | 0.7 |  |  | 2026-10-05 | fixed_hold active from 2026-04-20 to before 2026-10-05 (initial signal 2026-04-17, last same-direction signal 2026-09-03) |
| chemical | CE | -0.028 | -9.3 | 45.2 | 2026-09-03 | 45.09 | 45.31 | 1 | 0.9 |  |  | 2026-10-05 | fixed_hold active from 2026-04-20 to before 2026-10-05 (initial signal 2026-04-17, last same-direction signal 2026-09-03) |
| chemical | EMN | -0.028 | -5.9 | 70.77 | 2026-09-03 | 70.59 | 70.95 | 1 | 0.2 |  |  | 2026-10-05 | fixed_hold active from 2026-04-20 to before 2026-10-05 (initial signal 2026-04-17, last same-direction signal 2026-09-03) |
| chemical | HUN | -0.028 | -44.7 | 9.4 | 2026-09-03 | 9.38 | 9.42 | 1.5 | 0.7 |  |  | 2026-10-05 | fixed_hold active from 2026-04-20 to before 2026-10-05 (initial signal 2026-04-17, last same-direction signal 2026-09-03) |
| chemical | AVNT | -0.014 | -4.9 | 42.91 | 2026-09-03 | 42.8 | 43.02 | 1.2 | -0 |  |  | 2026-10-05 | fixed_hold active from 2026-04-20 to before 2026-10-05 (initial signal 2026-04-17, last same-direction signal 2026-09-03) |
| fuel | CASY | 0.024 | 0.5 | 758.42 | 2026-09-03 | 756.52 | 760.32 | -0.1 | 0 |  |  | 2026-09-11 | fixed_hold active from 2026-03-04 to before 2026-09-11 (initial signal 2026-03-03, last same-direction signal 2026-09-03) |
| fuel | MUSA | 0.016 | 0.5 | 522.3 | 2026-09-03 | 520.99 | 523.61 | -0.7 | 0 |  |  | 2026-09-11 | fixed_hold active from 2026-03-04 to before 2026-09-11 (initial signal 2026-03-03, last same-direction signal 2026-09-03) |
| metals | ATI | 0.02 | 1.5 | 204.54 | 2026-09-03 | 204.03 | 205.05 | 1 | 0.3 |  |  | 2026-09-18 | fixed_hold active from 2026-01-12 to before 2026-09-18 (initial signal 2026-01-09, last same-direction signal 2026-09-03) |
| metals | CRS | 0.015 | 0.5 | 467.48 | 2026-09-03 | 466.31 | 468.65 | 1.1 | 0.3 |  |  | 2026-09-18 | fixed_hold active from 2026-01-12 to before 2026-09-18 (initial signal 2026-01-09, last same-direction signal 2026-09-03) |
| metals | HWM | 0.015 | 0.9 | 260.49 | 2026-09-03 | 259.84 | 261.14 | 0.9 | 0.1 |  |  | 2026-09-18 | fixed_hold active from 2026-01-12 to before 2026-09-18 (initial signal 2026-01-09, last same-direction signal 2026-09-03) |
| psx_ref | PSX | 0.01 | 0.6 | 254.66 | 2026-09-03 | 254.02 | 255.3 | 0.1 | 1.1 |  |  | 2026-09-07 | fixed_hold active from 2026-08-28 to before 2026-09-07 (initial signal 2026-08-27, last same-direction signal 2026-09-01) |
| refiner | DK | -0.03 | -6.2 | 72.4 | 2026-09-03 | 72.22 | 72.58 | 0.2 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | PBF | -0.018 | -3.6 | 75.33 | 2026-09-03 | 75.14 | 75.52 | 0 | 1.7 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | DINO | -0.012 | -1.7 | 106.15 | 2026-09-03 | 105.88 | 106.42 | 0.2 | 1 |  |  |  | 5d rolling-mean band_hysteresis active |
| services | FTI | -0.02 | -3.7 | 80.08 | 2026-09-03 | 79.88 | 80.28 | 0.6 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -5.2 | 57.41 | 2026-09-03 | 57.27 | 57.55 | 1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4 | 37.29 | 2026-09-03 | 37.2 | 37.38 | 0.6 | 1.2 |  |  |  | continuous hysteresis sign active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.142177 | 2.75833 | 773.17 | 2026-09-03 | 771.237 | 775.103 |
| XLE | 0.321517 | 74.6326 | 64.62 | 2026-09-03 | 64.4585 | 64.7816 |
| XME | -0.0689382 | -8.7352 | 118.38 | 2026-09-03 | 118.084 | 118.676 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | refiner | DK | SELL | -6 | -6 | -0.02896 | False |  | 72.4 | 2026-09-03 | 72.219 | 72.581 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | PBF | SELL | -4 | -4 | -0.020088 | False |  | 75.33 | 2026-09-03 | 75.1417 | 75.5183 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | DINO | SELL | -2 | -2 | -0.0141533 | False |  | 106.15 | 2026-09-03 | 105.885 | 106.415 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | chemical | LYB | SELL | -1 | -1 | -0.00431733 | False |  | 64.76 | 2026-09-03 | 64.5981 | 64.9219 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XLE | BUY | 14 | 14 | 0.060312 | False |  | 64.62 | 2026-09-03 | 64.4585 | 64.7816 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
