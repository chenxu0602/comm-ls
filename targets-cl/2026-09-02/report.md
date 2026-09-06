# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-09-02

- Signal as-of date: 2026-09-01
- Target trading date: 2026-09-02
- AUM: $15,000.00
- Gross stock weight: 47.80%
- Single-name stock weight cap: 5.00%
- Net stock weight: -11.80%
- Gross hedge weight: 42.08%
- Total net weight after hedges: 16.20%
- Estimated turnover from current positions: 23.32%
- Full eligible order turnover: 14.24%
- Today's total child-order turnover: 13.40%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $5.03
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.18 | 0.18 | 2700 | 2700 | 11 |
| stock_short_without_hedge | 0.298 | -0.298 | 4470 | -4470 | 10 |
| total_hedge | 0.420793 | 0.279986 | 6311.9 | 4199.78 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.045 | 19.4 | 34.82 | 2026-09-01 | 34.73 | 34.91 | 0.5 | 1.1 |  |  | 2026-09-07 | fixed_hold active from 2026-08-04 to before 2026-09-07 (initial signal 2026-08-03, last same-direction signal 2026-09-01) |
| bwt | TECK | 0.015 | 3.4 | 66.79 | 2026-09-01 | 66.62 | 66.96 | 0.9 | 0.7 |  |  | 2026-09-07 | fixed_hold active from 2026-08-04 to before 2026-09-07 (initial signal 2026-08-03, last same-direction signal 2026-09-01) |
| chemical | DOW | -0.05 | -24.6 | 30.46 | 2026-09-01 | 30.38 | 30.54 | 0.3 | 1.1 |  |  | 2026-10-01 | fixed_hold active from 2026-04-20 to before 2026-10-01 (initial signal 2026-04-17, last same-direction signal 2026-09-01) |
| chemical | LYB | -0.05 | -11.5 | 65.17 | 2026-09-01 | 65.01 | 65.33 | 0 | 1.1 |  |  | 2026-10-01 | fixed_hold active from 2026-04-20 to before 2026-10-01 (initial signal 2026-04-17, last same-direction signal 2026-09-01) |
| chemical | WLK | -0.05 | -10.1 | 74.23 | 2026-09-01 | 74.04 | 74.42 | 0.9 | 0.7 |  |  | 2026-10-01 | fixed_hold active from 2026-04-20 to before 2026-10-01 (initial signal 2026-04-17, last same-direction signal 2026-09-01) |
| chemical | CE | -0.028 | -9.5 | 44.13 | 2026-09-01 | 44.02 | 44.24 | 1 | 0.9 |  |  | 2026-10-01 | fixed_hold active from 2026-04-20 to before 2026-10-01 (initial signal 2026-04-17, last same-direction signal 2026-09-01) |
| chemical | EMN | -0.028 | -6 | 70.14 | 2026-09-01 | 69.96 | 70.32 | 1 | 0.2 |  |  | 2026-10-01 | fixed_hold active from 2026-04-20 to before 2026-10-01 (initial signal 2026-04-17, last same-direction signal 2026-09-01) |
| chemical | HUN | -0.028 | -44.7 | 9.39 | 2026-09-01 | 9.37 | 9.41 | 1.5 | 0.7 |  |  | 2026-10-01 | fixed_hold active from 2026-04-20 to before 2026-10-01 (initial signal 2026-04-17, last same-direction signal 2026-09-01) |
| chemical | AVNT | -0.014 | -4.9 | 42.62 | 2026-09-01 | 42.51 | 42.73 | 1.2 | -0 |  |  | 2026-10-01 | fixed_hold active from 2026-04-20 to before 2026-10-01 (initial signal 2026-04-17, last same-direction signal 2026-09-01) |
| fuel | CASY | 0.024 | 0.5 | 766.91 | 2026-09-01 | 764.99 | 768.83 | -0.1 | 0 |  |  | 2026-09-09 | fixed_hold active from 2026-03-04 to before 2026-09-09 (initial signal 2026-03-03, last same-direction signal 2026-09-01) |
| fuel | MUSA | 0.016 | 0.4 | 536.45 | 2026-09-01 | 535.11 | 537.79 | -0.6 | 0 |  |  | 2026-09-09 | fixed_hold active from 2026-03-04 to before 2026-09-09 (initial signal 2026-03-03, last same-direction signal 2026-09-01) |
| metals | ATI | 0.02 | 1.5 | 200.95 | 2026-09-01 | 200.45 | 201.45 | 1 | 0.3 |  |  | 2026-09-16 | fixed_hold active from 2026-01-12 to before 2026-09-16 (initial signal 2026-01-09, last same-direction signal 2026-09-01) |
| metals | CRS | 0.015 | 0.5 | 473.06 | 2026-09-01 | 471.88 | 474.24 | 1.1 | 0.3 |  |  | 2026-09-16 | fixed_hold active from 2026-01-12 to before 2026-09-16 (initial signal 2026-01-09, last same-direction signal 2026-09-01) |
| metals | HWM | 0.015 | 0.9 | 254.89 | 2026-09-01 | 254.25 | 255.53 | 0.9 | 0.1 |  |  | 2026-09-16 | fixed_hold active from 2026-01-12 to before 2026-09-16 (initial signal 2026-01-09, last same-direction signal 2026-09-01) |
| psx_ref | PSX | 0.01 | 0.6 | 252.02 | 2026-09-01 | 251.39 | 252.65 | 0.1 | 1.1 |  |  | 2026-09-07 | fixed_hold active from 2026-08-28 to before 2026-09-07 (initial signal 2026-08-27, last same-direction signal 2026-09-01) |
| refiner | DK | 0.01 | 2 | 73.34 | 2026-09-01 | 73.16 | 73.52 | 0.1 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | PBF | 0.006 | 1.2 | 74.99 | 2026-09-01 | 74.8 | 75.18 | -0 | 1.7 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | DINO | 0.004 | 0.6 | 103.97 | 2026-09-01 | 103.71 | 104.23 | 0.2 | 1 |  |  |  | 5d rolling-mean band_hysteresis active |
| services | FTI | -0.02 | -3.8 | 78.31 | 2026-09-01 | 78.11 | 78.51 | 0.6 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -5.2 | 57.15 | 2026-09-01 | 57.01 | 57.29 | 1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4.1 | 36.8 | 2026-09-01 | 36.71 | 36.89 | 0.6 | 1.2 |  |  |  | continuous hysteresis sign active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.139812 | 2.753 | 761.78 | 2026-09-01 | 759.876 | 763.684 |
| XLE | 0.210577 | 48.7673 | 64.77 | 2026-09-01 | 64.6081 | 64.9319 |
| XME | -0.0704037 | -9.12202 | 115.77 | 2026-09-01 | 115.481 | 116.059 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | psx_ref | PSX | SELL | -1 | -1 | -0.0168013 | False |  | 252.02 | 2026-09-01 | 251.39 | 252.65 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | DK | SELL | -4 | -4 | -0.0195573 | False |  | 73.34 | 2026-09-01 | 73.1566 | 73.5233 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | PBF | SELL | -3 | -3 | -0.014998 | False |  | 74.99 | 2026-09-01 | 74.8025 | 75.1775 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | DINO | SELL | -1 | -1 | -0.00693133 | False |  | 103.97 | 2026-09-01 | 103.71 | 104.23 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | bwt | ERO | BUY | 1 | 1 | 0.00232133 | False |  | 34.82 | 2026-09-01 | 34.7329 | 34.907 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XLE | BUY | 17 | 17 | 0.073406 | False |  | 64.77 | 2026-09-01 | 64.6081 | 64.9319 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
