# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-10-05

- Signal as-of date: 2026-10-02
- Target trading date: 2026-10-05
- AUM: $15,000.00
- Gross stock weight: 46.80%
- Single-name stock weight cap: 5.00%
- Net stock weight: -14.80%
- Gross hedge weight: 33.59%
- Total net weight after hedges: 6.91%
- Estimated turnover from current positions: 3.35%
- Full eligible order turnover: 0.72%
- Today's total child-order turnover: 1.66%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $0.62
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.16 | 0.16 | 2400 | 2400 | 5 |
| stock_short_without_hedge | 0.308 | -0.308 | 4620 | -4620 | 11 |
| total_hedge | 0.33586 | 0.217144 | 5037.9 | 3257.17 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.045 | 17.8 | 37.91 | 2026-10-02 | 37.82 | 38 | 0.5 | 1.1 |  |  | 2026-10-08 | fixed_hold active from 2026-09-28 to before 2026-10-08 (initial signal 2026-09-25, last same-direction signal 2026-10-02) |
| bwt | TECK | 0.015 | 3.3 | 68.56 | 2026-10-02 | 68.39 | 68.73 | 0.9 | 0.7 |  |  | 2026-10-08 | fixed_hold active from 2026-09-28 to before 2026-10-08 (initial signal 2026-09-25, last same-direction signal 2026-10-02) |
| chemical | DOW | -0.05 | -26.8 | 27.97 | 2026-10-02 | 27.9 | 28.04 | 0.3 | 1.2 |  |  | 2026-11-03 | fixed_hold active from 2026-04-20 to before 2026-11-03 (initial signal 2026-04-17, last same-direction signal 2026-10-02) |
| chemical | LYB | -0.05 | -12.8 | 58.58 | 2026-10-02 | 58.43 | 58.73 | -0 | 1.2 |  |  | 2026-11-03 | fixed_hold active from 2026-04-20 to before 2026-11-03 (initial signal 2026-04-17, last same-direction signal 2026-10-02) |
| chemical | WLK | -0.05 | -11.8 | 63.5 | 2026-10-02 | 63.34 | 63.66 | 0.8 | 0.7 |  |  | 2026-11-03 | fixed_hold active from 2026-04-20 to before 2026-11-03 (initial signal 2026-04-17, last same-direction signal 2026-10-02) |
| chemical | CE | -0.028 | -9.5 | 44.19 | 2026-10-02 | 44.08 | 44.3 | 0.9 | 1 |  |  | 2026-11-03 | fixed_hold active from 2026-04-20 to before 2026-11-03 (initial signal 2026-04-17, last same-direction signal 2026-10-02) |
| chemical | EMN | -0.028 | -6.5 | 64.87 | 2026-10-02 | 64.71 | 65.03 | 1 | 0.2 |  |  | 2026-11-03 | fixed_hold active from 2026-04-20 to before 2026-11-03 (initial signal 2026-04-17, last same-direction signal 2026-10-02) |
| chemical | HUN | -0.028 | -49.2 | 8.53 | 2026-10-02 | 8.51 | 8.55 | 1.4 | 0.7 |  |  | 2026-11-03 | fixed_hold active from 2026-04-20 to before 2026-11-03 (initial signal 2026-04-17, last same-direction signal 2026-10-02) |
| chemical | AVNT | -0.014 | -5.1 | 41.17 | 2026-10-02 | 41.07 | 41.27 | 1.1 | -0 |  |  | 2026-11-03 | fixed_hold active from 2026-04-20 to before 2026-11-03 (initial signal 2026-04-17, last same-direction signal 2026-10-02) |
| psx_ref | PSX | -0.01 | -0.6 | 264.58 | 2026-10-02 | 263.92 | 265.24 | 0.1 | 1.1 |  |  | 2026-10-07 | fixed_hold active from 2026-09-09 to before 2026-10-07 (initial signal 2026-09-08, last same-direction signal 2026-10-01) |
| refiner | DK | 0.05 | 10.1 | 74.19 | 2026-10-02 | 74 | 74.38 | 0.2 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | PBF | 0.03 | 5.6 | 80.78 | 2026-10-02 | 80.58 | 80.98 | 0 | 1.7 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | DINO | 0.02 | 2.6 | 113.36 | 2026-10-02 | 113.08 | 113.64 | 0.1 | 1 |  |  |  | 5d rolling-mean band_hysteresis active |
| services | FTI | -0.02 | -4.4 | 68.82 | 2026-10-02 | 68.65 | 68.99 | 0.6 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -6.2 | 48.74 | 2026-10-02 | 48.62 | 48.86 | 1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4.7 | 31.85 | 2026-10-02 | 31.77 | 31.93 | 0.6 | 1.2 |  |  |  | continuous hysteresis sign active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.152439 | 2.97098 | 769.64 | 2026-10-02 | 767.716 | 771.564 |
| XLE | 0.124063 | 29.6235 | 62.82 | 2026-10-02 | 62.6629 | 62.977 |
| XME | -0.0593577 | -8.42033 | 105.74 | 2026-10-02 | 105.476 | 106.004 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | refiner | PBF | BUY | 1 | 1 | 0.00538533 | False |  | 80.78 | 2026-10-02 | 80.578 | 80.9819 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XME | BUY | 1 | 1 | 0.00704933 | False |  | 105.74 | 2026-10-02 | 105.476 | 106.004 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XLE | SELL | 0 | -1 | -0.004188 | False |  | 62.82 | 2026-10-02 | 62.6629 | 62.977 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
