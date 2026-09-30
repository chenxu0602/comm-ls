# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-09-25

- Signal as-of date: 2026-09-24
- Target trading date: 2026-09-25
- AUM: $15,000.00
- Gross stock weight: 56.80%
- Single-name stock weight cap: 5.00%
- Net stock weight: -16.80%
- Gross hedge weight: 43.78%
- Total net weight after hedges: 26.98%
- Estimated turnover from current positions: 30.25%
- Full eligible order turnover: 28.54%
- Today's total child-order turnover: 26.43%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $9.91
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.2 | 0.2 | 3000 | 3000 | 5 |
| stock_short_without_hedge | 0.368 | -0.368 | 5520 | -5520 | 14 |
| total_hedge | 0.437757 | 0.437757 | 6566.35 | 6566.35 | 2 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| chemical | DOW | -0.05 | -26.3 | 28.56 | 2026-09-24 | 28.49 | 28.63 | 0.3 | 1.2 |  |  | 2026-10-26 | fixed_hold active from 2026-04-20 to before 2026-10-26 (initial signal 2026-04-17, last same-direction signal 2026-09-24) |
| chemical | LYB | -0.05 | -12.5 | 60.18 | 2026-09-24 | 60.03 | 60.33 | -0 | 1.2 |  |  | 2026-10-26 | fixed_hold active from 2026-04-20 to before 2026-10-26 (initial signal 2026-04-17, last same-direction signal 2026-09-24) |
| chemical | WLK | -0.05 | -11.2 | 66.76 | 2026-09-24 | 66.59 | 66.93 | 0.8 | 0.7 |  |  | 2026-10-26 | fixed_hold active from 2026-04-20 to before 2026-10-26 (initial signal 2026-04-17, last same-direction signal 2026-09-24) |
| chemical | CE | -0.028 | -8.8 | 47.56 | 2026-09-24 | 47.44 | 47.68 | 0.9 | 0.9 |  |  | 2026-10-26 | fixed_hold active from 2026-04-20 to before 2026-10-26 (initial signal 2026-04-17, last same-direction signal 2026-09-24) |
| chemical | EMN | -0.028 | -6.3 | 66.19 | 2026-09-24 | 66.02 | 66.36 | 1 | 0.2 |  |  | 2026-10-26 | fixed_hold active from 2026-04-20 to before 2026-10-26 (initial signal 2026-04-17, last same-direction signal 2026-09-24) |
| chemical | HUN | -0.028 | -47.8 | 8.79 | 2026-09-24 | 8.77 | 8.81 | 1.4 | 0.7 |  |  | 2026-10-26 | fixed_hold active from 2026-04-20 to before 2026-10-26 (initial signal 2026-04-17, last same-direction signal 2026-09-24) |
| chemical | AVNT | -0.014 | -5.1 | 40.78 | 2026-09-24 | 40.68 | 40.88 | 1.1 | -0 |  |  | 2026-10-26 | fixed_hold active from 2026-04-20 to before 2026-10-26 (initial signal 2026-04-17, last same-direction signal 2026-09-24) |
| psx_ref | PSX | -0.05 | -2.9 | 255.87 | 2026-09-24 | 255.23 | 256.51 | 0.1 | 1.1 |  |  | 2026-09-30 | fixed_hold active from 2026-09-09 to before 2026-09-30 (initial signal 2026-09-08, last same-direction signal 2026-09-24) |
| refiner | DK | -0.01 | -2.2 | 66.91 | 2026-09-24 | 66.74 | 67.08 | 0.2 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | PBF | -0.006 | -1.3 | 71.9 | 2026-09-24 | 71.72 | 72.08 | 0 | 1.7 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | DINO | -0.004 | -0.6 | 105.79 | 2026-09-24 | 105.53 | 106.05 | 0.1 | 1 |  |  |  | 5d rolling-mean band_hysteresis active |
| services | FTI | -0.02 | -4.2 | 70.95 | 2026-09-24 | 70.77 | 71.13 | 0.6 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -5.8 | 51.43 | 2026-09-24 | 51.3 | 51.56 | 1.1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4.6 | 32.76 | 2026-09-24 | 32.68 | 32.84 | 0.6 | 1.2 |  |  |  | continuous hysteresis sign active |
| shipping | DHT | 0.05 | 34.6 | 21.68 | 2026-09-24 | 21.63 | 21.73 | 0.3 | 0 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | FRO | 0.05 | 15.6 | 47.97 | 2026-09-24 | 47.85 | 48.09 | 0.5 | 0.2 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | INSW | 0.05 | 7.2 | 104.85 | 2026-09-24 | 104.59 | 105.11 | 0.3 | 0.2 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | TNK | 0.0375 | 6 | 94.08 | 2026-09-24 | 93.84 | 94.32 | 0.3 | 0.2 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | STNG | 0.0125 | 2.3 | 80.96 | 2026-09-24 | 80.76 | 81.16 | 0.3 | 0.3 |  |  |  | 2d rolling-mean shipping_sticky_accel active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.135974 | 2.65859 | 767.18 | 2026-09-24 | 765.262 | 769.098 |
| XLE | 0.301782 | 72.312 | 62.6 | 2026-09-24 | 62.4435 | 62.7565 |
| XME | 0 | 0 | 107.96 | 2026-09-24 | 107.69 | 108.23 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | bwt | ERO | BUY | 18 | 18 | 0.044532 | False |  | 37.11 | 2026-09-24 | 37.0172 | 37.2028 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | DK | BUY | 4 | 4 | 0.0178427 | False |  | 66.91 | 2026-09-24 | 66.7427 | 67.0773 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | bwt | TECK | BUY | 3 | 3 | 0.013302 | False |  | 66.51 | 2026-09-24 | 66.3437 | 66.6763 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | PBF | BUY | 3 | 3 | 0.01438 | False |  | 71.9 | 2026-09-24 | 71.7203 | 72.0798 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | DINO | BUY | 1 | 1 | 0.00705267 | False |  | 105.79 | 2026-09-24 | 105.526 | 106.054 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | SPY | SELL | -1 | -1 | -0.0511453 | False |  | 767.18 | 2026-09-24 | 765.262 | 769.098 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XLE | SELL | -15 | -14 | -0.0584267 | False |  | 62.6 | 2026-09-24 | 62.4435 | 62.7565 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XME | SELL | -8 | -8 | -0.0575787 | False |  | 107.96 | 2026-09-24 | 107.69 | 108.23 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
