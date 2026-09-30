# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-09-18

- Signal as-of date: 2026-09-17
- Target trading date: 2026-09-18
- AUM: $15,000.00
- Gross stock weight: 63.30%
- Single-name stock weight cap: 5.00%
- Net stock weight: -38.30%
- Gross hedge weight: 69.53%
- Total net weight after hedges: 31.23%
- Estimated turnover from current positions: 29.26%
- Full eligible order turnover: 26.55%
- Today's total child-order turnover: 26.05%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $9.77
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.125 | 0.125 | 1875 | 1875 | 5 |
| stock_short_without_hedge | 0.508 | -0.508 | 7620 | -7620 | 16 |
| total_hedge | 0.695326 | 0.695326 | 10429.9 | 10429.9 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | -0.045 | -20.3 | 33.28 | 2026-09-17 | 33.2 | 33.36 | 0.4 | 1.1 |  |  | 2026-09-23 | fixed_hold active from 2026-09-18 to before 2026-09-23 (initial signal 2026-09-17, last same-direction signal 2026-09-17) |
| bwt | TECK | -0.015 | -3.4 | 65.22 | 2026-09-17 | 65.06 | 65.38 | 0.9 | 0.7 |  |  | 2026-09-23 | fixed_hold active from 2026-09-18 to before 2026-09-23 (initial signal 2026-09-17, last same-direction signal 2026-09-17) |
| chemical | DOW | -0.05 | -25.4 | 29.49 | 2026-09-17 | 29.42 | 29.56 | 0.3 | 1.2 |  |  | 2026-10-19 | fixed_hold active from 2026-04-20 to before 2026-10-19 (initial signal 2026-04-17, last same-direction signal 2026-09-17) |
| chemical | LYB | -0.05 | -11.7 | 64.25 | 2026-09-17 | 64.09 | 64.41 | -0 | 1.2 |  |  | 2026-10-19 | fixed_hold active from 2026-04-20 to before 2026-10-19 (initial signal 2026-04-17, last same-direction signal 2026-09-17) |
| chemical | WLK | -0.05 | -10.6 | 70.57 | 2026-09-17 | 70.39 | 70.75 | 0.8 | 0.7 |  |  | 2026-10-19 | fixed_hold active from 2026-04-20 to before 2026-10-19 (initial signal 2026-04-17, last same-direction signal 2026-09-17) |
| chemical | CE | -0.028 | -9 | 46.81 | 2026-09-17 | 46.69 | 46.93 | 0.9 | 0.9 |  |  | 2026-10-19 | fixed_hold active from 2026-04-20 to before 2026-10-19 (initial signal 2026-04-17, last same-direction signal 2026-09-17) |
| chemical | EMN | -0.028 | -6.3 | 66.24 | 2026-09-17 | 66.07 | 66.41 | 1 | 0.2 |  |  | 2026-10-19 | fixed_hold active from 2026-04-20 to before 2026-10-19 (initial signal 2026-04-17, last same-direction signal 2026-09-17) |
| chemical | HUN | -0.028 | -46.1 | 9.12 | 2026-09-17 | 9.1 | 9.14 | 1.5 | 0.7 |  |  | 2026-10-19 | fixed_hold active from 2026-04-20 to before 2026-10-19 (initial signal 2026-04-17, last same-direction signal 2026-09-17) |
| chemical | AVNT | -0.014 | -5.2 | 40.58 | 2026-09-17 | 40.48 | 40.68 | 1.2 | -0 |  |  | 2026-10-19 | fixed_hold active from 2026-04-20 to before 2026-10-19 (initial signal 2026-04-17, last same-direction signal 2026-09-17) |
| psx_ref | PSX | -0.05 | -2.7 | 274.21 | 2026-09-17 | 273.52 | 274.9 | 0.1 | 1.1 |  |  | 2026-09-23 | fixed_hold active from 2026-09-09 to before 2026-09-23 (initial signal 2026-09-08, last same-direction signal 2026-09-17) |
| refiner | DK | -0.05 | -9.2 | 81.55 | 2026-09-17 | 81.35 | 81.75 | 0.2 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | PBF | -0.03 | -5.8 | 77.16 | 2026-09-17 | 76.97 | 77.35 | 0 | 1.7 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | DINO | -0.02 | -2.6 | 116.62 | 2026-09-17 | 116.33 | 116.91 | 0.2 | 1 |  |  |  | 5d rolling-mean band_hysteresis active |
| services | FTI | -0.02 | -4.1 | 72.74 | 2026-09-17 | 72.56 | 72.92 | 0.6 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -5.8 | 52.08 | 2026-09-17 | 51.95 | 52.21 | 1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4.4 | 34.03 | 2026-09-17 | 33.94 | 34.12 | 0.6 | 1.2 |  |  |  | continuous hysteresis sign active |
| shipping | DHT | 0.0375 | 24.6 | 22.82 | 2026-09-17 | 22.76 | 22.88 | 0.3 | 0 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | FRO | 0.0375 | 10.4 | 54.03 | 2026-09-17 | 53.89 | 54.17 | 0.5 | 0.2 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | INSW | 0.025 | 3.4 | 110.53 | 2026-09-17 | 110.25 | 110.81 | 0.3 | 0.2 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | TNK | 0.01875 | 2.8 | 100.82 | 2026-09-17 | 100.57 | 101.07 | 0.3 | 0.2 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | STNG | 0.00625 | 1.1 | 87.85 | 2026-09-17 | 87.63 | 88.07 | 0.3 | 0.3 |  |  |  | 2d rolling-mean shipping_sticky_accel active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.210107 | 4.1327 | 762.6 | 2026-09-17 | 760.693 | 764.506 |
| XLE | 0.425898 | 99.0768 | 64.48 | 2026-09-17 | 64.3188 | 64.6412 |
| XME | 0.0593209 | 7.9933 | 111.32 | 2026-09-17 | 111.042 | 111.598 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | bwt | ERO | SELL | -20 | -20 | -0.0443733 | False |  | 33.28 | 2026-09-17 | 33.1968 | 33.3632 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | DHT | BUY | 25 | 25 | 0.0380333 | False |  | 22.82 | 2026-09-17 | 22.7629 | 22.877 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | FRO | BUY | 10 | 10 | 0.03602 | False |  | 54.03 | 2026-09-17 | 53.8949 | 54.1651 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | INSW | BUY | 3 | 3 | 0.022106 | False |  | 110.53 | 2026-09-17 | 110.254 | 110.806 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | TNK | BUY | 3 | 3 | 0.020164 | False |  | 100.82 | 2026-09-17 | 100.568 | 101.072 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | bwt | TECK | SELL | -3 | -3 | -0.013044 | False |  | 65.22 | 2026-09-17 | 65.057 | 65.3831 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | STNG | BUY | 1 | 1 | 0.00585667 | False |  | 87.85 | 2026-09-17 | 87.6304 | 88.0696 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XME | BUY | 8 | 8 | 0.0593707 | False |  | 111.32 | 2026-09-17 | 111.042 | 111.598 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XLE | SELL | -5 | -5 | -0.0214933 | False |  | 64.48 | 2026-09-17 | 64.3188 | 64.6412 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
