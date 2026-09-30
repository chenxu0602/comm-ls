# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-09-30

- Signal as-of date: 2026-09-29
- Target trading date: 2026-09-30
- AUM: $15,000.00
- Gross stock weight: 63.30%
- Single-name stock weight cap: 5.00%
- Net stock weight: -6.30%
- Gross hedge weight: 32.11%
- Total net weight after hedges: 13.90%
- Estimated turnover from current positions: 17.12%
- Full eligible order turnover: 14.96%
- Today's total child-order turnover: 15.89%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $5.96
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.285 | 0.285 | 4275 | 4275 | 10 |
| stock_short_without_hedge | 0.348 | -0.348 | 5220 | -5220 | 11 |
| total_hedge | 0.32111 | 0.201965 | 4816.65 | 3029.48 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.045 | 18.2 | 37.14 | 2026-09-29 | 37.05 | 37.23 | 0.4 | 1.1 |  |  | 2026-10-05 | fixed_hold active from 2026-09-28 to before 2026-10-05 (initial signal 2026-09-25, last same-direction signal 2026-09-29) |
| bwt | TECK | 0.015 | 3.5 | 64.85 | 2026-09-29 | 64.69 | 65.01 | 0.9 | 0.7 |  |  | 2026-10-05 | fixed_hold active from 2026-09-28 to before 2026-10-05 (initial signal 2026-09-25, last same-direction signal 2026-09-29) |
| chemical | DOW | -0.05 | -27.2 | 27.61 | 2026-09-29 | 27.54 | 27.68 | 0.3 | 1.2 |  |  | 2026-10-29 | fixed_hold active from 2026-04-20 to before 2026-10-29 (initial signal 2026-04-17, last same-direction signal 2026-09-29) |
| chemical | LYB | -0.05 | -12.9 | 58.18 | 2026-09-29 | 58.03 | 58.33 | -0 | 1.2 |  |  | 2026-10-29 | fixed_hold active from 2026-04-20 to before 2026-10-29 (initial signal 2026-04-17, last same-direction signal 2026-09-29) |
| chemical | WLK | -0.05 | -11.8 | 63.39 | 2026-09-29 | 63.23 | 63.55 | 0.8 | 0.7 |  |  | 2026-10-29 | fixed_hold active from 2026-04-20 to before 2026-10-29 (initial signal 2026-04-17, last same-direction signal 2026-09-29) |
| chemical | CE | -0.028 | -9.4 | 44.84 | 2026-09-29 | 44.73 | 44.95 | 0.9 | 1 |  |  | 2026-10-29 | fixed_hold active from 2026-04-20 to before 2026-10-29 (initial signal 2026-04-17, last same-direction signal 2026-09-29) |
| chemical | EMN | -0.028 | -6.4 | 65.75 | 2026-09-29 | 65.59 | 65.91 | 1 | 0.2 |  |  | 2026-10-29 | fixed_hold active from 2026-04-20 to before 2026-10-29 (initial signal 2026-04-17, last same-direction signal 2026-09-29) |
| chemical | HUN | -0.028 | -50.1 | 8.38 | 2026-09-29 | 8.36 | 8.4 | 1.4 | 0.7 |  |  | 2026-10-29 | fixed_hold active from 2026-04-20 to before 2026-10-29 (initial signal 2026-04-17, last same-direction signal 2026-09-29) |
| chemical | AVNT | -0.014 | -5.1 | 40.78 | 2026-09-29 | 40.68 | 40.88 | 1.1 | -0 |  |  | 2026-10-29 | fixed_hold active from 2026-04-20 to before 2026-10-29 (initial signal 2026-04-17, last same-direction signal 2026-09-29) |
| psx_ref | PSX | -0.05 | -3 | 252.25 | 2026-09-29 | 251.62 | 252.88 | 0.1 | 1.1 |  |  | 2026-10-05 | fixed_hold active from 2026-09-09 to before 2026-10-05 (initial signal 2026-09-08, last same-direction signal 2026-09-29) |
| refiner | DK | 0.05 | 10.9 | 68.73 | 2026-09-29 | 68.56 | 68.9 | 0.2 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | PBF | 0.03 | 6 | 75.23 | 2026-09-29 | 75.04 | 75.42 | 0 | 1.7 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | DINO | 0.02 | 2.8 | 105.59 | 2026-09-29 | 105.33 | 105.85 | 0.1 | 1 |  |  |  | 5d rolling-mean band_hysteresis active |
| services | FTI | -0.02 | -4.4 | 68.85 | 2026-09-29 | 68.68 | 69.02 | 0.6 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -6 | 49.87 | 2026-09-29 | 49.75 | 49.99 | 1.1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4.8 | 31.54 | 2026-09-29 | 31.46 | 31.62 | 0.6 | 1.2 |  |  |  | continuous hysteresis sign active |
| shipping | DHT | 0.0375 | 25.1 | 22.42 | 2026-09-29 | 22.36 | 22.48 | 0.3 | 0 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | FRO | 0.0375 | 11.5 | 48.93 | 2026-09-29 | 48.81 | 49.05 | 0.5 | 0.2 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | INSW | 0.025 | 3.4 | 110.24 | 2026-09-29 | 109.96 | 110.52 | 0.3 | 0.2 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | TNK | 0.01875 | 2.9 | 96.81 | 2026-09-29 | 96.57 | 97.05 | 0.3 | 0.2 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | STNG | 0.00625 | 1.1 | 83.57 | 2026-09-29 | 83.36 | 83.78 | 0.3 | 0.3 |  |  |  | 2d rolling-mean shipping_sticky_accel active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.111608 | 2.19069 | 764.2 | 2026-09-29 | 762.29 | 766.111 |
| XLE | 0.149929 | 36.5443 | 61.54 | 2026-09-29 | 61.3862 | 61.6939 |
| XME | -0.0595721 | -8.6004 | 103.9 | 2026-09-29 | 103.64 | 104.16 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | shipping | INSW | SELL | -4 | -4 | -0.0293973 | False |  | 110.24 | 2026-09-29 | 109.964 | 110.516 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | TNK | SELL | -3 | -3 | -0.019362 | False |  | 96.81 | 2026-09-29 | 96.568 | 97.052 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | DK | BUY | 4 | 4 | 0.018328 | False |  | 68.73 | 2026-09-29 | 68.5582 | 68.9018 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | DHT | SELL | -10 | -10 | -0.0149467 | False |  | 22.42 | 2026-09-29 | 22.364 | 22.4761 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | FRO | SELL | -4 | -4 | -0.013048 | False |  | 48.93 | 2026-09-29 | 48.8077 | 49.0523 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | PBF | BUY | 2 | 2 | 0.0100307 | False |  | 75.23 | 2026-09-29 | 75.0419 | 75.4181 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | DINO | BUY | 1 | 1 | 0.00703933 | False |  | 105.59 | 2026-09-29 | 105.326 | 105.854 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | STNG | SELL | -1 | -1 | -0.00557133 | False |  | 83.57 | 2026-09-29 | 83.3611 | 83.7789 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | chemical | WLK | SELL | -1 | -1 | -0.004226 | False |  | 63.39 | 2026-09-29 | 63.2315 | 63.5485 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XLE | SELL | -7 | -9 | -0.036924 | False |  | 61.54 | 2026-09-29 | 61.3862 | 61.6939 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
