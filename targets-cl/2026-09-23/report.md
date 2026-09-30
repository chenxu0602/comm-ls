# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-09-23

- Signal as-of date: 2026-09-22
- Target trading date: 2026-09-23
- AUM: $15,000.00
- Gross stock weight: 70.80%
- Single-name stock weight cap: 5.00%
- Net stock weight: -30.80%
- Gross hedge weight: 65.41%
- Total net weight after hedges: 34.61%
- Estimated turnover from current positions: 5.66%
- Full eligible order turnover: 1.17%
- Today's total child-order turnover: 1.32%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $0.49
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.2 | 0.2 | 3000 | 3000 | 5 |
| stock_short_without_hedge | 0.508 | -0.508 | 7620 | -7620 | 16 |
| total_hedge | 0.654136 | 0.654136 | 9812.04 | 9812.04 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | -0.045 | -18.1 | 37.28 | 2026-09-22 | 37.19 | 37.37 | 0.5 | 1.1 |  |  | 2026-09-25 | fixed_hold active from 2026-09-18 to before 2026-09-25 (initial signal 2026-09-17, last same-direction signal 2026-09-21) |
| bwt | TECK | -0.015 | -3.3 | 68.86 | 2026-09-22 | 68.69 | 69.03 | 0.9 | 0.7 |  |  | 2026-09-25 | fixed_hold active from 2026-09-18 to before 2026-09-25 (initial signal 2026-09-17, last same-direction signal 2026-09-21) |
| chemical | DOW | -0.05 | -26.6 | 28.19 | 2026-09-22 | 28.12 | 28.26 | 0.3 | 1.1 |  |  | 2026-10-22 | fixed_hold active from 2026-04-20 to before 2026-10-22 (initial signal 2026-04-17, last same-direction signal 2026-09-22) |
| chemical | LYB | -0.05 | -12.7 | 59.24 | 2026-09-22 | 59.09 | 59.39 | -0 | 1.2 |  |  | 2026-10-22 | fixed_hold active from 2026-04-20 to before 2026-10-22 (initial signal 2026-04-17, last same-direction signal 2026-09-22) |
| chemical | WLK | -0.05 | -10.9 | 68.77 | 2026-09-22 | 68.6 | 68.94 | 0.8 | 0.7 |  |  | 2026-10-22 | fixed_hold active from 2026-04-20 to before 2026-10-22 (initial signal 2026-04-17, last same-direction signal 2026-09-22) |
| chemical | CE | -0.028 | -8.8 | 47.46 | 2026-09-22 | 47.34 | 47.58 | 0.9 | 0.9 |  |  | 2026-10-22 | fixed_hold active from 2026-04-20 to before 2026-10-22 (initial signal 2026-04-17, last same-direction signal 2026-09-22) |
| chemical | EMN | -0.028 | -6.3 | 67.04 | 2026-09-22 | 66.87 | 67.21 | 1 | 0.2 |  |  | 2026-10-22 | fixed_hold active from 2026-04-20 to before 2026-10-22 (initial signal 2026-04-17, last same-direction signal 2026-09-22) |
| chemical | HUN | -0.028 | -46.4 | 9.06 | 2026-09-22 | 9.04 | 9.08 | 1.4 | 0.7 |  |  | 2026-10-22 | fixed_hold active from 2026-04-20 to before 2026-10-22 (initial signal 2026-04-17, last same-direction signal 2026-09-22) |
| chemical | AVNT | -0.014 | -5.1 | 41.26 | 2026-09-22 | 41.16 | 41.36 | 1.1 | -0 |  |  | 2026-10-22 | fixed_hold active from 2026-04-20 to before 2026-10-22 (initial signal 2026-04-17, last same-direction signal 2026-09-22) |
| psx_ref | PSX | -0.05 | -2.9 | 256.76 | 2026-09-22 | 256.12 | 257.4 | 0.1 | 1.1 |  |  | 2026-09-28 | fixed_hold active from 2026-09-09 to before 2026-09-28 (initial signal 2026-09-08, last same-direction signal 2026-09-22) |
| refiner | DK | -0.05 | -10.2 | 73.37 | 2026-09-22 | 73.19 | 73.55 | 0.2 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | PBF | -0.03 | -6.3 | 71.42 | 2026-09-22 | 71.24 | 71.6 | 0 | 1.7 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | DINO | -0.02 | -2.8 | 106.73 | 2026-09-22 | 106.46 | 107 | 0.1 | 1 |  |  |  | 5d rolling-mean band_hysteresis active |
| services | FTI | -0.02 | -4.2 | 70.82 | 2026-09-22 | 70.64 | 71 | 0.6 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -5.8 | 52.14 | 2026-09-22 | 52.01 | 52.27 | 1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4.6 | 32.84 | 2026-09-22 | 32.76 | 32.92 | 0.6 | 1.2 |  |  |  | continuous hysteresis sign active |
| shipping | DHT | 0.05 | 35.1 | 21.39 | 2026-09-22 | 21.34 | 21.44 | 0.3 | 0 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | FRO | 0.05 | 15.7 | 47.91 | 2026-09-22 | 47.79 | 48.03 | 0.5 | 0.2 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | INSW | 0.05 | 7.2 | 103.87 | 2026-09-22 | 103.61 | 104.13 | 0.3 | 0.2 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | TNK | 0.0375 | 5.9 | 95.63 | 2026-09-22 | 95.39 | 95.87 | 0.3 | 0.2 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | STNG | 0.0125 | 2.3 | 82.35 | 2026-09-22 | 82.14 | 82.56 | 0.3 | 0.3 |  |  |  | 2d rolling-mean shipping_sticky_accel active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.181749 | 3.53417 | 771.393 | 2026-09-22 | 769.465 | 773.322 |
| XLE | 0.413274 | 99.3473 | 62.3983 | 2026-09-22 | 62.2423 | 62.5543 |
| XME | 0.0591135 | 8.07501 | 109.808 | 2026-09-22 | 109.534 | 110.083 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | bwt | ERO | BUY | 2 | 2 | 0.00497067 | False |  | 37.28 | 2026-09-22 | 37.1868 | 37.3732 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | DHT | BUY | 3 | 3 | 0.004278 | False |  | 21.39 | 2026-09-22 | 21.3365 | 21.4435 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | chemical | LYB | SELL | -1 | -1 | -0.00394933 | False |  | 59.24 | 2026-09-22 | 59.0919 | 59.3881 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
