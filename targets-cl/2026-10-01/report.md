# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-10-01

- Signal as-of date: 2026-09-30
- Target trading date: 2026-10-01
- AUM: $15,000.00
- Gross stock weight: 48.80%
- Single-name stock weight cap: 5.00%
- Net stock weight: -16.80%
- Gross hedge weight: 36.23%
- Total net weight after hedges: 7.57%
- Estimated turnover from current positions: 28.14%
- Full eligible order turnover: 26.84%
- Today's total child-order turnover: 27.02%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $10.13
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.16 | 0.16 | 2400 | 2400 | 5 |
| stock_short_without_hedge | 0.328 | -0.328 | 4920 | -4920 | 11 |
| total_hedge | 0.362283 | 0.243739 | 5434.24 | 3656.09 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.045 | 18.4 | 36.69 | 2026-09-30 | 36.6 | 36.78 | 0.4 | 1.1 |  |  | 2026-10-06 | fixed_hold active from 2026-09-28 to before 2026-10-06 (initial signal 2026-09-25, last same-direction signal 2026-09-30) |
| bwt | TECK | 0.015 | 3.4 | 65.79 | 2026-09-30 | 65.63 | 65.95 | 0.9 | 0.7 |  |  | 2026-10-06 | fixed_hold active from 2026-09-28 to before 2026-10-06 (initial signal 2026-09-25, last same-direction signal 2026-09-30) |
| chemical | DOW | -0.05 | -27.2 | 27.54 | 2026-09-30 | 27.47 | 27.61 | 0.3 | 1.2 |  |  | 2026-10-30 | fixed_hold active from 2026-04-20 to before 2026-10-30 (initial signal 2026-04-17, last same-direction signal 2026-09-30) |
| chemical | LYB | -0.05 | -13.1 | 57.47 | 2026-09-30 | 57.33 | 57.61 | -0 | 1.2 |  |  | 2026-10-30 | fixed_hold active from 2026-04-20 to before 2026-10-30 (initial signal 2026-04-17, last same-direction signal 2026-09-30) |
| chemical | WLK | -0.05 | -12 | 62.31 | 2026-09-30 | 62.15 | 62.47 | 0.8 | 0.7 |  |  | 2026-10-30 | fixed_hold active from 2026-04-20 to before 2026-10-30 (initial signal 2026-04-17, last same-direction signal 2026-09-30) |
| chemical | CE | -0.028 | -9.5 | 44.37 | 2026-09-30 | 44.26 | 44.48 | 0.9 | 1 |  |  | 2026-10-30 | fixed_hold active from 2026-04-20 to before 2026-10-30 (initial signal 2026-04-17, last same-direction signal 2026-09-30) |
| chemical | EMN | -0.028 | -6.5 | 64.84 | 2026-09-30 | 64.68 | 65 | 1 | 0.2 |  |  | 2026-10-30 | fixed_hold active from 2026-04-20 to before 2026-10-30 (initial signal 2026-04-17, last same-direction signal 2026-09-30) |
| chemical | HUN | -0.028 | -50 | 8.4 | 2026-09-30 | 8.38 | 8.42 | 1.4 | 0.7 |  |  | 2026-10-30 | fixed_hold active from 2026-04-20 to before 2026-10-30 (initial signal 2026-04-17, last same-direction signal 2026-09-30) |
| chemical | AVNT | -0.014 | -5.2 | 40.25 | 2026-09-30 | 40.15 | 40.35 | 1.1 | -0 |  |  | 2026-10-30 | fixed_hold active from 2026-04-20 to before 2026-10-30 (initial signal 2026-04-17, last same-direction signal 2026-09-30) |
| psx_ref | PSX | -0.03 | -1.8 | 255.31 | 2026-09-30 | 254.67 | 255.95 | 0.1 | 1.1 |  |  | 2026-10-06 | fixed_hold active from 2026-09-09 to before 2026-10-06 (initial signal 2026-09-08, last same-direction signal 2026-09-30) |
| refiner | DK | 0.05 | 10.5 | 71.37 | 2026-09-30 | 71.19 | 71.55 | 0.2 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | PBF | 0.03 | 5.8 | 76.96 | 2026-09-30 | 76.77 | 77.15 | 0 | 1.7 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | DINO | 0.02 | 2.8 | 107.32 | 2026-09-30 | 107.05 | 107.59 | 0.1 | 1 |  |  |  | 5d rolling-mean band_hysteresis active |
| services | FTI | -0.02 | -4.4 | 67.92 | 2026-09-30 | 67.75 | 68.09 | 0.6 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -6.2 | 48.72 | 2026-09-30 | 48.6 | 48.84 | 1.1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4.7 | 31.8 | 2026-09-30 | 31.72 | 31.88 | 0.6 | 1.2 |  |  |  | continuous hysteresis sign active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.155311 | 3.05477 | 762.63 | 2026-09-30 | 760.723 | 764.537 |
| XLE | 0.1477 | 36.0245 | 61.5 | 2026-09-30 | 61.3463 | 61.6537 |
| XME | -0.0592719 | -8.58515 | 103.56 | 2026-09-30 | 103.301 | 103.819 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | shipping | DHT | SELL | -25 | -25 | -0.0376167 | False |  | 22.57 | 2026-09-30 | 22.5136 | 22.6264 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | FRO | SELL | -11 | -11 | -0.0361313 | False |  | 49.27 | 2026-09-30 | 49.1468 | 49.3932 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | INSW | SELL | -3 | -3 | -0.022028 | False |  | 110.14 | 2026-09-30 | 109.865 | 110.415 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | psx_ref | PSX | BUY | 1 | 1 | 0.0170207 | False |  | 255.31 | 2026-09-30 | 254.672 | 255.948 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | TNK | SELL | -3 | -3 | -0.019412 | False |  | 97.06 | 2026-09-30 | 96.8173 | 97.3026 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | DK | BUY | 4 | 4 | 0.019032 | False |  | 71.37 | 2026-09-30 | 71.1916 | 71.5484 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | PBF | BUY | 2 | 2 | 0.0102613 | False |  | 76.96 | 2026-09-30 | 76.7676 | 77.1524 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | DINO | BUY | 1 | 1 | 0.00715467 | False |  | 107.32 | 2026-09-30 | 107.052 | 107.588 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | STNG | SELL | -1 | -1 | -0.00558 | False |  | 83.7 | 2026-09-30 | 83.4907 | 83.9092 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | chemical | WLK | SELL | -1 | -1 | -0.004154 | False |  | 62.31 | 2026-09-30 | 62.1542 | 62.4658 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | SPY | BUY | 1 | 1 | 0.050842 | False |  | 762.63 | 2026-09-30 | 760.723 | 764.537 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XLE | SELL | -8 | -10 | -0.041 | False |  | 61.5 | 2026-09-30 | 61.3463 | 61.6537 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
