# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-09-14

- Signal as-of date: 2026-09-11
- Target trading date: 2026-09-14
- AUM: $15,000.00
- Gross stock weight: 59.80%
- Single-name stock weight cap: 5.00%
- Net stock weight: -29.80%
- Gross hedge weight: 67.96%
- Total net weight after hedges: 24.15%
- Estimated turnover from current positions: 8.24%
- Full eligible order turnover: 0.81%
- Today's total child-order turnover: 0.91%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $0.34
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.15 | 0.15 | 2250 | 2250 | 7 |
| stock_short_without_hedge | 0.448 | -0.448 | 6720 | -6720 | 14 |
| total_hedge | 0.679624 | 0.539522 | 10194.4 | 8092.83 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.045 | 19 | 35.47 | 2026-09-11 | 35.38 | 35.56 | 0.5 | 1.1 |  |  | 2026-09-17 | fixed_hold active from 2026-08-04 to before 2026-09-17 (initial signal 2026-08-03, last same-direction signal 2026-09-11) |
| bwt | TECK | 0.015 | 3.4 | 66.44 | 2026-09-11 | 66.27 | 66.61 | 0.9 | 0.7 |  |  | 2026-09-17 | fixed_hold active from 2026-08-04 to before 2026-09-17 (initial signal 2026-08-03, last same-direction signal 2026-09-11) |
| chemical | DOW | -0.05 | -25.8 | 29.03 | 2026-09-11 | 28.96 | 29.1 | 0.3 | 1.2 |  |  | 2026-10-13 | fixed_hold active from 2026-04-20 to before 2026-10-13 (initial signal 2026-04-17, last same-direction signal 2026-09-11) |
| chemical | LYB | -0.05 | -11.8 | 63.69 | 2026-09-11 | 63.53 | 63.85 | 0 | 1.2 |  |  | 2026-10-13 | fixed_hold active from 2026-04-20 to before 2026-10-13 (initial signal 2026-04-17, last same-direction signal 2026-09-11) |
| chemical | WLK | -0.05 | -10.6 | 70.81 | 2026-09-11 | 70.63 | 70.99 | 0.9 | 0.7 |  |  | 2026-10-13 | fixed_hold active from 2026-04-20 to before 2026-10-13 (initial signal 2026-04-17, last same-direction signal 2026-09-11) |
| chemical | CE | -0.028 | -9.1 | 46.09 | 2026-09-11 | 45.97 | 46.21 | 1 | 1 |  |  | 2026-10-13 | fixed_hold active from 2026-04-20 to before 2026-10-13 (initial signal 2026-04-17, last same-direction signal 2026-09-11) |
| chemical | EMN | -0.028 | -6.2 | 68.11 | 2026-09-11 | 67.94 | 68.28 | 1 | 0.2 |  |  | 2026-10-13 | fixed_hold active from 2026-04-20 to before 2026-10-13 (initial signal 2026-04-17, last same-direction signal 2026-09-11) |
| chemical | HUN | -0.028 | -44 | 9.54 | 2026-09-11 | 9.52 | 9.56 | 1.5 | 0.7 |  |  | 2026-10-13 | fixed_hold active from 2026-04-20 to before 2026-10-13 (initial signal 2026-04-17, last same-direction signal 2026-09-11) |
| chemical | AVNT | -0.014 | -5.1 | 41.41 | 2026-09-11 | 41.31 | 41.51 | 1.2 | -0 |  |  | 2026-10-13 | fixed_hold active from 2026-04-20 to before 2026-10-13 (initial signal 2026-04-17, last same-direction signal 2026-09-11) |
| fuel | CASY | 0.024 | 0.6 | 615.47 | 2026-09-11 | 613.93 | 617.01 | -0 | 0 |  |  | 2026-09-21 | fixed_hold active from 2026-03-04 to before 2026-09-21 (initial signal 2026-03-03, last same-direction signal 2026-09-11) |
| fuel | MUSA | 0.016 | 0.5 | 523.58 | 2026-09-11 | 522.27 | 524.89 | -0.6 | 0 |  |  | 2026-09-21 | fixed_hold active from 2026-03-04 to before 2026-09-21 (initial signal 2026-03-03, last same-direction signal 2026-09-11) |
| metals | ATI | 0.02 | 1.5 | 198.77 | 2026-09-11 | 198.27 | 199.27 | 1 | 0.3 |  |  | 2026-09-28 | fixed_hold active from 2026-01-12 to before 2026-09-28 (initial signal 2026-01-09, last same-direction signal 2026-09-11) |
| metals | CRS | 0.015 | 0.5 | 443.19 | 2026-09-11 | 442.08 | 444.3 | 1.1 | 0.3 |  |  | 2026-09-28 | fixed_hold active from 2026-01-12 to before 2026-09-28 (initial signal 2026-01-09, last same-direction signal 2026-09-11) |
| metals | HWM | 0.015 | 1 | 229.61 | 2026-09-11 | 229.04 | 230.18 | 1 | 0.1 |  |  | 2026-09-28 | fixed_hold active from 2026-01-12 to before 2026-09-28 (initial signal 2026-01-09, last same-direction signal 2026-09-11) |
| psx_ref | PSX | -0.05 | -2.9 | 259.47 | 2026-09-11 | 258.82 | 260.12 | 0.1 | 1.1 |  |  | 2026-09-17 | fixed_hold active from 2026-09-09 to before 2026-09-17 (initial signal 2026-09-08, last same-direction signal 2026-09-11) |
| refiner | DK | -0.05 | -9.9 | 76.1 | 2026-09-11 | 75.91 | 76.29 | 0.2 | 1.4 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | PBF | -0.03 | -5.7 | 78.3 | 2026-09-11 | 78.1 | 78.5 | 0 | 1.8 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | DINO | -0.02 | -2.8 | 107.84 | 2026-09-11 | 107.57 | 108.11 | 0.2 | 1 |  |  |  | 5d rolling-mean band_hysteresis active |
| services | FTI | -0.02 | -3.9 | 76.34 | 2026-09-11 | 76.15 | 76.53 | 0.6 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -5.4 | 56.06 | 2026-09-11 | 55.92 | 56.2 | 1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4.2 | 35.84 | 2026-09-11 | 35.75 | 35.93 | 0.6 | 1.2 |  |  |  | continuous hysteresis sign active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.156984 | 3.08098 | 764.29 | 2026-09-11 | 762.379 | 766.201 |
| XLE | 0.452589 | 104.219 | 65.14 | 2026-09-11 | 64.9771 | 65.3028 |
| XME | -0.0700509 | -9.24723 | 113.63 | 2026-09-11 | 113.346 | 113.914 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | chemical | WLK | SELL | -1 | -1 | -0.00472067 | False |  | 70.81 | 2026-09-11 | 70.633 | 70.987 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XLE | BUY | 1 | 1 | 0.00434267 | False |  | 65.14 | 2026-09-11 | 64.9771 | 65.3028 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
