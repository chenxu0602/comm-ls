# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-10-02

- Signal as-of date: 2026-10-01
- Target trading date: 2026-10-02
- AUM: $15,000.00
- Gross stock weight: 46.80%
- Single-name stock weight cap: 5.00%
- Net stock weight: -14.80%
- Gross hedge weight: 33.56%
- Total net weight after hedges: 6.92%
- Estimated turnover from current positions: 7.07%
- Full eligible order turnover: 5.44%
- Today's total child-order turnover: 4.06%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $1.52
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.16 | 0.16 | 2400 | 2400 | 5 |
| stock_short_without_hedge | 0.308 | -0.308 | 4620 | -4620 | 11 |
| total_hedge | 0.335628 | 0.217165 | 5034.42 | 3257.47 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.045 | 18.9 | 35.75 | 2026-10-01 | 35.66 | 35.84 | 0.4 | 1.1 |  |  | 2026-10-07 | fixed_hold active from 2026-09-28 to before 2026-10-07 (initial signal 2026-09-25, last same-direction signal 2026-10-01) |
| bwt | TECK | 0.015 | 3.4 | 65.22 | 2026-10-01 | 65.06 | 65.38 | 0.9 | 0.7 |  |  | 2026-10-07 | fixed_hold active from 2026-09-28 to before 2026-10-07 (initial signal 2026-09-25, last same-direction signal 2026-10-01) |
| chemical | DOW | -0.05 | -27.2 | 27.59 | 2026-10-01 | 27.52 | 27.66 | 0.3 | 1.2 |  |  | 2026-11-02 | fixed_hold active from 2026-04-20 to before 2026-11-02 (initial signal 2026-04-17, last same-direction signal 2026-10-01) |
| chemical | LYB | -0.05 | -13 | 57.78 | 2026-10-01 | 57.64 | 57.92 | -0 | 1.2 |  |  | 2026-11-02 | fixed_hold active from 2026-04-20 to before 2026-11-02 (initial signal 2026-04-17, last same-direction signal 2026-10-01) |
| chemical | WLK | -0.05 | -12 | 62.47 | 2026-10-01 | 62.31 | 62.63 | 0.8 | 0.7 |  |  | 2026-11-02 | fixed_hold active from 2026-04-20 to before 2026-11-02 (initial signal 2026-04-17, last same-direction signal 2026-10-01) |
| chemical | CE | -0.028 | -9.5 | 44.2 | 2026-10-01 | 44.09 | 44.31 | 0.9 | 1 |  |  | 2026-11-02 | fixed_hold active from 2026-04-20 to before 2026-11-02 (initial signal 2026-04-17, last same-direction signal 2026-10-01) |
| chemical | EMN | -0.028 | -6.6 | 64.05 | 2026-10-01 | 63.89 | 64.21 | 1 | 0.2 |  |  | 2026-11-02 | fixed_hold active from 2026-04-20 to before 2026-11-02 (initial signal 2026-04-17, last same-direction signal 2026-10-01) |
| chemical | HUN | -0.028 | -48.4 | 8.67 | 2026-10-01 | 8.65 | 8.69 | 1.4 | 0.7 |  |  | 2026-11-02 | fixed_hold active from 2026-04-20 to before 2026-11-02 (initial signal 2026-04-17, last same-direction signal 2026-10-01) |
| chemical | AVNT | -0.014 | -5.2 | 40.54 | 2026-10-01 | 40.44 | 40.64 | 1.1 | -0 |  |  | 2026-11-02 | fixed_hold active from 2026-04-20 to before 2026-11-02 (initial signal 2026-04-17, last same-direction signal 2026-10-01) |
| psx_ref | PSX | -0.01 | -0.6 | 264.23 | 2026-10-01 | 263.57 | 264.89 | 0.1 | 1.1 |  |  | 2026-10-07 | fixed_hold active from 2026-09-09 to before 2026-10-07 (initial signal 2026-09-08, last same-direction signal 2026-10-01) |
| refiner | DK | 0.05 | 10.1 | 74.34 | 2026-10-01 | 74.15 | 74.53 | 0.2 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | PBF | 0.03 | 5.5 | 82.34 | 2026-10-01 | 82.13 | 82.55 | 0 | 1.7 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | DINO | 0.02 | 2.7 | 112.7 | 2026-10-01 | 112.42 | 112.98 | 0.1 | 1 |  |  |  | 5d rolling-mean band_hysteresis active |
| services | FTI | -0.02 | -4.4 | 68.85 | 2026-10-01 | 68.68 | 69.02 | 0.6 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -6.2 | 48.66 | 2026-10-01 | 48.54 | 48.78 | 1.1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4.7 | 31.88 | 2026-10-01 | 31.8 | 31.96 | 0.6 | 1.2 |  |  |  | continuous hysteresis sign active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.152419 | 2.99255 | 763.99 | 2026-10-01 | 762.08 | 765.9 |
| XLE | 0.123978 | 29.6598 | 62.7 | 2026-10-01 | 62.5433 | 62.8568 |
| XME | -0.0592316 | -8.51927 | 104.29 | 2026-10-01 | 104.029 | 104.551 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | psx_ref | PSX | BUY | 1 | 1 | 0.0176153 | False |  | 264.23 | 2026-10-01 | 263.569 | 264.891 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | DK | SELL | -1 | -1 | -0.004956 | False |  | 74.34 | 2026-10-01 | 74.1541 | 74.5258 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | PBF | SELL | -1 | -1 | -0.00548933 | False |  | 82.34 | 2026-10-01 | 82.1341 | 82.5458 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XLE | SELL | -4 | -3 | -0.01254 | False |  | 62.7 | 2026-10-01 | 62.5433 | 62.8568 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
