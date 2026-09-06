# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-09-08

- Signal as-of date: 2026-09-04
- Target trading date: 2026-09-08
- AUM: $15,000.00
- Gross stock weight: 54.80%
- Single-name stock weight cap: 5.00%
- Net stock weight: -24.80%
- Gross hedge weight: 60.14%
- Total net weight after hedges: 21.58%
- Estimated turnover from current positions: 20.59%
- Full eligible order turnover: 12.11%
- Today's total child-order turnover: 12.14%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $4.55
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.15 | 0.15 | 2250 | 2250 | 7 |
| stock_short_without_hedge | 0.398 | -0.398 | 5970 | -5970 | 13 |
| total_hedge | 0.601371 | 0.463756 | 9020.57 | 6956.34 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.045 | 19.3 | 34.9 | 2026-09-04 | 34.81 | 34.99 | 0.5 | 1 |  |  | 2026-09-11 | fixed_hold active from 2026-08-04 to before 2026-09-11 (initial signal 2026-08-03, last same-direction signal 2026-09-04) |
| bwt | TECK | 0.015 | 3.3 | 69.1 | 2026-09-04 | 68.93 | 69.27 | 1 | 0.7 |  |  | 2026-09-11 | fixed_hold active from 2026-08-04 to before 2026-09-11 (initial signal 2026-08-03, last same-direction signal 2026-09-04) |
| chemical | DOW | -0.05 | -25.5 | 29.44 | 2026-09-04 | 29.37 | 29.51 | 0.3 | 1.2 |  |  | 2026-10-07 | fixed_hold active from 2026-04-20 to before 2026-10-07 (initial signal 2026-04-17, last same-direction signal 2026-09-04) |
| chemical | LYB | -0.05 | -11.8 | 63.52 | 2026-09-04 | 63.36 | 63.68 | 0 | 1.2 |  |  | 2026-10-07 | fixed_hold active from 2026-04-20 to before 2026-10-07 (initial signal 2026-04-17, last same-direction signal 2026-09-04) |
| chemical | WLK | -0.05 | -10 | 74.79 | 2026-09-04 | 74.6 | 74.98 | 0.9 | 0.7 |  |  | 2026-10-07 | fixed_hold active from 2026-04-20 to before 2026-10-07 (initial signal 2026-04-17, last same-direction signal 2026-09-04) |
| chemical | CE | -0.028 | -9.4 | 44.67 | 2026-09-04 | 44.56 | 44.78 | 0.9 | 0.9 |  |  | 2026-10-07 | fixed_hold active from 2026-04-20 to before 2026-10-07 (initial signal 2026-04-17, last same-direction signal 2026-09-04) |
| chemical | EMN | -0.028 | -5.9 | 71.19 | 2026-09-04 | 71.01 | 71.37 | 1 | 0.2 |  |  | 2026-10-07 | fixed_hold active from 2026-04-20 to before 2026-10-07 (initial signal 2026-04-17, last same-direction signal 2026-09-04) |
| chemical | HUN | -0.028 | -43.7 | 9.62 | 2026-09-04 | 9.6 | 9.64 | 1.5 | 0.7 |  |  | 2026-10-07 | fixed_hold active from 2026-04-20 to before 2026-10-07 (initial signal 2026-04-17, last same-direction signal 2026-09-04) |
| chemical | AVNT | -0.014 | -4.8 | 43.4 | 2026-09-04 | 43.29 | 43.51 | 1.2 | -0 |  |  | 2026-10-07 | fixed_hold active from 2026-04-20 to before 2026-10-07 (initial signal 2026-04-17, last same-direction signal 2026-09-04) |
| fuel | CASY | 0.024 | 0.5 | 756.09 | 2026-09-04 | 754.2 | 757.98 | -0.1 | 0 |  |  | 2026-09-15 | fixed_hold active from 2026-03-04 to before 2026-09-15 (initial signal 2026-03-03, last same-direction signal 2026-09-04) |
| fuel | MUSA | 0.016 | 0.5 | 511.33 | 2026-09-04 | 510.05 | 512.61 | -0.6 | 0 |  |  | 2026-09-15 | fixed_hold active from 2026-03-04 to before 2026-09-15 (initial signal 2026-03-03, last same-direction signal 2026-09-04) |
| metals | ATI | 0.02 | 1.4 | 210.65 | 2026-09-04 | 210.12 | 211.18 | 1 | 0.3 |  |  | 2026-09-22 | fixed_hold active from 2026-01-12 to before 2026-09-22 (initial signal 2026-01-09, last same-direction signal 2026-09-04) |
| metals | CRS | 0.015 | 0.5 | 475.33 | 2026-09-04 | 474.14 | 476.52 | 1.1 | 0.3 |  |  | 2026-09-22 | fixed_hold active from 2026-01-12 to before 2026-09-22 (initial signal 2026-01-09, last same-direction signal 2026-09-04) |
| metals | HWM | 0.015 | 0.9 | 259.27 | 2026-09-04 | 258.62 | 259.92 | 0.9 | 0.1 |  |  | 2026-09-22 | fixed_hold active from 2026-01-12 to before 2026-09-22 (initial signal 2026-01-09, last same-direction signal 2026-09-04) |
| refiner | DK | -0.05 | -10.4 | 71.86 | 2026-09-04 | 71.68 | 72.04 | 0.2 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | PBF | -0.03 | -6.1 | 74.34 | 2026-09-04 | 74.15 | 74.53 | 0 | 1.7 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | DINO | -0.02 | -2.8 | 105.41 | 2026-09-04 | 105.15 | 105.67 | 0.2 | 1 |  |  |  | 5d rolling-mean band_hysteresis active |
| services | FTI | -0.02 | -3.8 | 79.84 | 2026-09-04 | 79.64 | 80.04 | 0.6 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -5.2 | 57.51 | 2026-09-04 | 57.37 | 57.65 | 1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4 | 37.07 | 2026-09-04 | 36.98 | 37.16 | 0.6 | 1.2 |  |  |  | continuous hysteresis sign active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.145593 | 2.83553 | 770.19 | 2026-09-04 | 768.265 | 772.115 |
| XLE | 0.386971 | 90.6113 | 64.06 | 2026-09-04 | 63.8998 | 64.2201 |
| XME | -0.0688077 | -8.70102 | 118.62 | 2026-09-04 | 118.323 | 118.917 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | refiner | DK | SELL | -4 | -4 | -0.0191627 | False |  | 71.86 | 2026-09-04 | 71.6804 | 72.0397 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | psx_ref | PSX | SELL | -1 | -1 | -0.017006 | False |  | 255.09 | 2026-09-04 | 254.452 | 255.728 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | PBF | SELL | -2 | -2 | -0.009912 | False |  | 74.34 | 2026-09-04 | 74.1541 | 74.5258 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | DINO | SELL | -1 | -1 | -0.00702733 | False |  | 105.41 | 2026-09-04 | 105.146 | 105.674 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XLE | BUY | 16 | 16 | 0.0683307 | False |  | 64.06 | 2026-09-04 | 63.8998 | 64.2201 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
