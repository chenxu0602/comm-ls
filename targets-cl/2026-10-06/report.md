# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-10-06

策略变更和当前信号状态见 [strategy_notes.md](strategy_notes.md)。

- Signal as-of date: 2026-10-05
- Target trading date: 2026-10-06
- AUM: $15,000.00
- Gross stock weight: 46.80%
- Single-name stock weight cap: 5.00%
- Net stock weight: -14.80%
- Gross hedge weight: 33.96%
- Total net weight after hedges: 7.28%
- Estimated turnover from current positions: 3.29%
- Full eligible order turnover: 0.53%
- Today's total child-order turnover: 1.56%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $0.59
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.16 | 0.16 | 2400 | 2400 | 5 |
| stock_short_without_hedge | 0.308 | -0.308 | 4620 | -4620 | 11 |
| total_hedge | 0.33957 | 0.220821 | 5093.55 | 3312.32 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.045 | 17.6 | 38.44 | 2026-10-05 | 38.34 | 38.54 | 0.4 | 1.1 |  |  | 2026-10-09 | fixed_hold active from 2026-09-28 to before 2026-10-09 (initial signal 2026-09-25, last same-direction signal 2026-10-05) |
| bwt | TECK | 0.015 | 3.3 | 67.87 | 2026-10-05 | 67.7 | 68.04 | 0.9 | 0.7 |  |  | 2026-10-09 | fixed_hold active from 2026-09-28 to before 2026-10-09 (initial signal 2026-09-25, last same-direction signal 2026-10-05) |
| chemical | DOW | -0.05 | -26.3 | 28.51 | 2026-10-05 | 28.44 | 28.58 | 0.3 | 1.2 |  |  | 2026-11-04 | fixed_hold active from 2026-04-20 to before 2026-11-04 (initial signal 2026-04-17, last same-direction signal 2026-10-05) |
| chemical | LYB | -0.05 | -12.7 | 59.22 | 2026-10-05 | 59.07 | 59.37 | -0 | 1.2 |  |  | 2026-11-04 | fixed_hold active from 2026-04-20 to before 2026-11-04 (initial signal 2026-04-17, last same-direction signal 2026-10-05) |
| chemical | WLK | -0.05 | -11.6 | 64.61 | 2026-10-05 | 64.45 | 64.77 | 0.8 | 0.7 |  |  | 2026-11-04 | fixed_hold active from 2026-04-20 to before 2026-11-04 (initial signal 2026-04-17, last same-direction signal 2026-10-05) |
| chemical | CE | -0.028 | -9.2 | 45.53 | 2026-10-05 | 45.42 | 45.64 | 0.9 | 1 |  |  | 2026-11-04 | fixed_hold active from 2026-04-20 to before 2026-11-04 (initial signal 2026-04-17, last same-direction signal 2026-10-05) |
| chemical | EMN | -0.028 | -6.5 | 64.94 | 2026-10-05 | 64.78 | 65.1 | 1 | 0.2 |  |  | 2026-11-04 | fixed_hold active from 2026-04-20 to before 2026-11-04 (initial signal 2026-04-17, last same-direction signal 2026-10-05) |
| chemical | HUN | -0.028 | -47.5 | 8.84 | 2026-10-05 | 8.82 | 8.86 | 1.4 | 0.7 |  |  | 2026-11-04 | fixed_hold active from 2026-04-20 to before 2026-11-04 (initial signal 2026-04-17, last same-direction signal 2026-10-05) |
| chemical | AVNT | -0.014 | -5 | 41.6 | 2026-10-05 | 41.5 | 41.7 | 1.1 | -0 |  |  | 2026-11-04 | fixed_hold active from 2026-04-20 to before 2026-11-04 (initial signal 2026-04-17, last same-direction signal 2026-10-05) |
| psx_ref | PSX | -0.01 | -0.6 | 269.72 | 2026-10-05 | 269.05 | 270.39 | 0.1 | 1.1 |  |  | 2026-10-07 | fixed_hold active from 2026-09-09 to before 2026-10-07 (initial signal 2026-09-08, last same-direction signal 2026-10-01) |
| refiner | DK | 0.05 | 9.9 | 75.4 | 2026-10-05 | 75.21 | 75.59 | 0.2 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | PBF | 0.03 | 5.3 | 84.16 | 2026-10-05 | 83.95 | 84.37 | 0 | 1.7 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | DINO | 0.02 | 2.6 | 115.22 | 2026-10-05 | 114.93 | 115.51 | 0.1 | 1 |  |  |  | 5d rolling-mean band_hysteresis active |
| services | FTI | -0.02 | -4.3 | 70.25 | 2026-10-05 | 70.07 | 70.43 | 0.6 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -6 | 50.28 | 2026-10-05 | 50.15 | 50.41 | 1.1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4.6 | 32.78 | 2026-10-05 | 32.7 | 32.86 | 0.6 | 1.2 |  |  |  | continuous hysteresis sign active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.153761 | 2.97666 | 774.83 | 2026-10-05 | 772.893 | 776.767 |
| XLE | 0.126435 | 29.8901 | 63.45 | 2026-10-05 | 63.2914 | 63.6086 |
| XME | -0.0593744 | -8.26481 | 107.76 | 2026-10-05 | 107.491 | 108.029 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | hedge | XME | BUY | 1 | 1 | 0.007184 | False |  | 107.76 | 2026-10-05 | 107.491 | 108.029 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XLE | BUY | 0 | 2 | 0.00846 | False |  | 63.45 | 2026-10-05 | 63.2914 | 63.6086 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
