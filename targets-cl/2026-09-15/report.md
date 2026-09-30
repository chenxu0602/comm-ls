# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-09-15

- Signal as-of date: 2026-09-14
- Target trading date: 2026-09-15
- AUM: $15,000.00
- Gross stock weight: 59.80%
- Single-name stock weight cap: 5.00%
- Net stock weight: -29.80%
- Gross hedge weight: 68.16%
- Total net weight after hedges: 24.25%
- Estimated turnover from current positions: 8.67%
- Full eligible order turnover: 1.11%
- Today's total child-order turnover: 1.59%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $0.60
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.15 | 0.15 | 2250 | 2250 | 7 |
| stock_short_without_hedge | 0.448 | -0.448 | 6720 | -6720 | 14 |
| total_hedge | 0.681625 | 0.540548 | 10224.4 | 8108.22 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.045 | 20 | 33.68 | 2026-09-14 | 33.6 | 33.76 | 0.4 | 1.1 |  |  | 2026-09-17 | fixed_hold active from 2026-08-04 to before 2026-09-17 (initial signal 2026-08-03, last same-direction signal 2026-09-11) |
| bwt | TECK | 0.015 | 3.4 | 66.25 | 2026-09-14 | 66.08 | 66.42 | 0.9 | 0.7 |  |  | 2026-09-17 | fixed_hold active from 2026-08-04 to before 2026-09-17 (initial signal 2026-08-03, last same-direction signal 2026-09-11) |
| chemical | DOW | -0.05 | -26 | 28.9 | 2026-09-14 | 28.83 | 28.97 | 0.3 | 1.2 |  |  | 2026-10-14 | fixed_hold active from 2026-04-20 to before 2026-10-14 (initial signal 2026-04-17, last same-direction signal 2026-09-14) |
| chemical | LYB | -0.05 | -12 | 62.75 | 2026-09-14 | 62.59 | 62.91 | 0 | 1.2 |  |  | 2026-10-14 | fixed_hold active from 2026-04-20 to before 2026-10-14 (initial signal 2026-04-17, last same-direction signal 2026-09-14) |
| chemical | WLK | -0.05 | -10.9 | 68.96 | 2026-09-14 | 68.79 | 69.13 | 0.9 | 0.7 |  |  | 2026-10-14 | fixed_hold active from 2026-04-20 to before 2026-10-14 (initial signal 2026-04-17, last same-direction signal 2026-09-14) |
| chemical | CE | -0.028 | -9.4 | 44.78 | 2026-09-14 | 44.67 | 44.89 | 0.9 | 1 |  |  | 2026-10-14 | fixed_hold active from 2026-04-20 to before 2026-10-14 (initial signal 2026-04-17, last same-direction signal 2026-09-14) |
| chemical | EMN | -0.028 | -6.3 | 67 | 2026-09-14 | 66.83 | 67.17 | 1 | 0.2 |  |  | 2026-10-14 | fixed_hold active from 2026-04-20 to before 2026-10-14 (initial signal 2026-04-17, last same-direction signal 2026-09-14) |
| chemical | HUN | -0.028 | -45.2 | 9.3 | 2026-09-14 | 9.28 | 9.32 | 1.5 | 0.7 |  |  | 2026-10-14 | fixed_hold active from 2026-04-20 to before 2026-10-14 (initial signal 2026-04-17, last same-direction signal 2026-09-14) |
| chemical | AVNT | -0.014 | -5.1 | 41.16 | 2026-09-14 | 41.06 | 41.26 | 1.2 | -0 |  |  | 2026-10-14 | fixed_hold active from 2026-04-20 to before 2026-10-14 (initial signal 2026-04-17, last same-direction signal 2026-09-14) |
| fuel | CASY | 0.024 | 0.6 | 621.61 | 2026-09-14 | 620.06 | 623.16 | -0.1 | 0 |  |  | 2026-09-22 | fixed_hold active from 2026-03-04 to before 2026-09-22 (initial signal 2026-03-03, last same-direction signal 2026-09-14) |
| fuel | MUSA | 0.016 | 0.5 | 527.17 | 2026-09-14 | 525.85 | 528.49 | -0.7 | 0 |  |  | 2026-09-22 | fixed_hold active from 2026-03-04 to before 2026-09-22 (initial signal 2026-03-03, last same-direction signal 2026-09-14) |
| metals | ATI | 0.02 | 1.6 | 188.15 | 2026-09-14 | 187.68 | 188.62 | 1.1 | 0.3 |  |  | 2026-09-29 | fixed_hold active from 2026-01-12 to before 2026-09-29 (initial signal 2026-01-09, last same-direction signal 2026-09-14) |
| metals | CRS | 0.015 | 0.5 | 420.38 | 2026-09-14 | 419.33 | 421.43 | 1.1 | 0.3 |  |  | 2026-09-29 | fixed_hold active from 2026-01-12 to before 2026-09-29 (initial signal 2026-01-09, last same-direction signal 2026-09-14) |
| metals | HWM | 0.015 | 1 | 227.13 | 2026-09-14 | 226.56 | 227.7 | 1 | 0.1 |  |  | 2026-09-29 | fixed_hold active from 2026-01-12 to before 2026-09-29 (initial signal 2026-01-09, last same-direction signal 2026-09-14) |
| psx_ref | PSX | -0.05 | -2.9 | 257.06 | 2026-09-14 | 256.42 | 257.7 | 0.1 | 1.1 |  |  | 2026-09-18 | fixed_hold active from 2026-09-09 to before 2026-09-18 (initial signal 2026-09-08, last same-direction signal 2026-09-14) |
| refiner | DK | -0.05 | -10.1 | 74.47 | 2026-09-14 | 74.28 | 74.66 | 0.2 | 1.4 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | PBF | -0.03 | -6.4 | 70.4 | 2026-09-14 | 70.22 | 70.58 | 0.1 | 1.8 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | DINO | -0.02 | -2.8 | 106.91 | 2026-09-14 | 106.64 | 107.18 | 0.2 | 1 |  |  |  | 5d rolling-mean band_hysteresis active |
| services | FTI | -0.02 | -4.1 | 72.87 | 2026-09-14 | 72.69 | 73.05 | 0.6 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -5.6 | 53.32 | 2026-09-14 | 53.19 | 53.45 | 1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4.3 | 35.01 | 2026-09-14 | 34.92 | 35.1 | 0.6 | 1.2 |  |  |  | continuous hysteresis sign active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.156995 | 3.09499 | 760.88 | 2026-09-14 | 758.978 | 762.782 |
| XLE | 0.454092 | 105.554 | 64.53 | 2026-09-14 | 64.3687 | 64.6913 |
| XME | -0.0705387 | -9.60407 | 110.17 | 2026-09-14 | 109.895 | 110.445 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | hedge | XLE | BUY | 2 | 2 | 0.008604 | False |  | 64.53 | 2026-09-14 | 64.3687 | 64.6913 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XME | SELL | -1 | -1 | -0.00734467 | False |  | 110.17 | 2026-09-14 | 109.895 | 110.445 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
