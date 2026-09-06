# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-09-03

- Signal as-of date: 2026-09-02
- Target trading date: 2026-09-03
- AUM: $15,000.00
- Gross stock weight: 47.80%
- Single-name stock weight cap: 5.00%
- Net stock weight: -15.80%
- Gross hedge weight: 47.82%
- Total net weight after hedges: 18.12%
- Estimated turnover from current positions: 19.46%
- Full eligible order turnover: 10.12%
- Today's total child-order turnover: 8.05%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $3.02
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.16 | 0.16 | 2400 | 2400 | 8 |
| stock_short_without_hedge | 0.318 | -0.318 | 4770 | -4770 | 13 |
| total_hedge | 0.478193 | 0.339156 | 7172.9 | 5087.34 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.045 | 19.4 | 34.76 | 2026-09-02 | 34.67 | 34.85 | 0.5 | 1.1 |  |  | 2026-09-08 | fixed_hold active from 2026-08-04 to before 2026-09-08 (initial signal 2026-08-03, last same-direction signal 2026-09-02) |
| bwt | TECK | 0.015 | 3.4 | 67.07 | 2026-09-02 | 66.9 | 67.24 | 0.9 | 0.7 |  |  | 2026-09-08 | fixed_hold active from 2026-08-04 to before 2026-09-08 (initial signal 2026-08-03, last same-direction signal 2026-09-02) |
| chemical | DOW | -0.05 | -24 | 31.28 | 2026-09-02 | 31.2 | 31.36 | 0.3 | 1.1 |  |  | 2026-10-02 | fixed_hold active from 2026-04-20 to before 2026-10-02 (initial signal 2026-04-17, last same-direction signal 2026-09-02) |
| chemical | LYB | -0.05 | -11.3 | 66.57 | 2026-09-02 | 66.4 | 66.74 | 0 | 1.1 |  |  | 2026-10-02 | fixed_hold active from 2026-04-20 to before 2026-10-02 (initial signal 2026-04-17, last same-direction signal 2026-09-02) |
| chemical | WLK | -0.05 | -9.8 | 76.27 | 2026-09-02 | 76.08 | 76.46 | 0.9 | 0.7 |  |  | 2026-10-02 | fixed_hold active from 2026-04-20 to before 2026-10-02 (initial signal 2026-04-17, last same-direction signal 2026-09-02) |
| chemical | CE | -0.028 | -9 | 46.66 | 2026-09-02 | 46.54 | 46.78 | 1 | 0.9 |  |  | 2026-10-02 | fixed_hold active from 2026-04-20 to before 2026-10-02 (initial signal 2026-04-17, last same-direction signal 2026-09-02) |
| chemical | EMN | -0.028 | -5.8 | 72.16 | 2026-09-02 | 71.98 | 72.34 | 1 | 0.2 |  |  | 2026-10-02 | fixed_hold active from 2026-04-20 to before 2026-10-02 (initial signal 2026-04-17, last same-direction signal 2026-09-02) |
| chemical | HUN | -0.028 | -43.3 | 9.71 | 2026-09-02 | 9.69 | 9.73 | 1.5 | 0.7 |  |  | 2026-10-02 | fixed_hold active from 2026-04-20 to before 2026-10-02 (initial signal 2026-04-17, last same-direction signal 2026-09-02) |
| chemical | AVNT | -0.014 | -4.8 | 43.59 | 2026-09-02 | 43.48 | 43.7 | 1.2 | -0 |  |  | 2026-10-02 | fixed_hold active from 2026-04-20 to before 2026-10-02 (initial signal 2026-04-17, last same-direction signal 2026-09-02) |
| fuel | CASY | 0.024 | 0.5 | 753.59 | 2026-09-02 | 751.71 | 755.47 | -0.1 | 0 |  |  | 2026-09-10 | fixed_hold active from 2026-03-04 to before 2026-09-10 (initial signal 2026-03-03, last same-direction signal 2026-09-02) |
| fuel | MUSA | 0.016 | 0.5 | 520.47 | 2026-09-02 | 519.17 | 521.77 | -0.7 | 0 |  |  | 2026-09-10 | fixed_hold active from 2026-03-04 to before 2026-09-10 (initial signal 2026-03-03, last same-direction signal 2026-09-02) |
| metals | ATI | 0.02 | 1.5 | 201.69 | 2026-09-02 | 201.19 | 202.19 | 1 | 0.3 |  |  | 2026-09-17 | fixed_hold active from 2026-01-12 to before 2026-09-17 (initial signal 2026-01-09, last same-direction signal 2026-09-02) |
| metals | CRS | 0.015 | 0.5 | 460.97 | 2026-09-02 | 459.82 | 462.12 | 1.1 | 0.3 |  |  | 2026-09-17 | fixed_hold active from 2026-01-12 to before 2026-09-17 (initial signal 2026-01-09, last same-direction signal 2026-09-02) |
| metals | HWM | 0.015 | 0.9 | 252.96 | 2026-09-02 | 252.33 | 253.59 | 0.9 | 0.1 |  |  | 2026-09-17 | fixed_hold active from 2026-01-12 to before 2026-09-17 (initial signal 2026-01-09, last same-direction signal 2026-09-02) |
| psx_ref | PSX | 0.01 | 0.6 | 256.09 | 2026-09-02 | 255.45 | 256.73 | 0.1 | 1.1 |  |  | 2026-09-07 | fixed_hold active from 2026-08-28 to before 2026-09-07 (initial signal 2026-08-27, last same-direction signal 2026-09-01) |
| refiner | DK | -0.01 | -2.1 | 71.45 | 2026-09-02 | 71.27 | 71.63 | 0.2 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | PBF | -0.006 | -1.2 | 75.48 | 2026-09-02 | 75.29 | 75.67 | 0 | 1.7 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | DINO | -0.004 | -0.6 | 106.06 | 2026-09-02 | 105.79 | 106.33 | 0.2 | 1 |  |  |  | 5d rolling-mean band_hysteresis active |
| services | FTI | -0.02 | -3.8 | 79.67 | 2026-09-02 | 79.47 | 79.87 | 0.6 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -5.2 | 58.13 | 2026-09-02 | 57.98 | 58.28 | 1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4 | 37.63 | 2026-09-02 | 37.54 | 37.72 | 0.6 | 1.2 |  |  |  | continuous hysteresis sign active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.14299 | 2.80314 | 765.16 | 2026-09-02 | 763.247 | 767.073 |
| XLE | 0.265685 | 61.2176 | 65.1 | 2026-09-02 | 64.9372 | 65.2627 |
| XME | -0.0695185 | -8.72909 | 119.46 | 2026-09-02 | 119.161 | 119.759 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | refiner | DK | SELL | -4 | -2 | -0.00952667 | True |  | 71.45 | 2026-09-02 | 71.2714 | 71.6286 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | DINO | SELL | -2 | -1 | -0.00707067 | True |  | 106.06 | 2026-09-02 | 105.795 | 106.325 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | PBF | SELL | -2 | -1 | -0.005032 | True |  | 75.48 | 2026-09-02 | 75.2913 | 75.6687 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | bwt | ERO | BUY | 1 | 1 | 0.00231733 | False |  | 34.76 | 2026-09-02 | 34.6731 | 34.8469 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | chemical | LYB | BUY | 1 | 1 | 0.004438 | False |  | 66.57 | 2026-09-02 | 66.4036 | 66.7364 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XLE | BUY | 12 | 12 | 0.05208 | False |  | 65.1 | 2026-09-02 | 64.9372 | 65.2627 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
