# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-09-17

- Signal as-of date: 2026-09-16
- Target trading date: 2026-09-17
- AUM: $15,000.00
- Gross stock weight: 44.80%
- Single-name stock weight cap: 5.00%
- Net stock weight: -44.80%
- Gross hedge weight: 66.96%
- Total net weight after hedges: 22.16%
- Estimated turnover from current positions: 33.94%
- Full eligible order turnover: 32.40%
- Today's total child-order turnover: 30.53%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $11.45
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0 | 0 | 0 | 0 | 0 |
| stock_short_without_hedge | 0.448 | -0.448 | 6720 | -6720 | 14 |
| total_hedge | 0.669613 | 0.669613 | 10044.2 | 10044.2 | 2 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| chemical | DOW | -0.05 | -24.9 | 30.08 | 2026-09-16 | 30 | 30.16 | 0.3 | 1.2 |  |  | 2026-10-16 | fixed_hold active from 2026-04-20 to before 2026-10-16 (initial signal 2026-04-17, last same-direction signal 2026-09-16) |
| chemical | LYB | -0.05 | -11.6 | 64.9 | 2026-09-16 | 64.74 | 65.06 | 0 | 1.2 |  |  | 2026-10-16 | fixed_hold active from 2026-04-20 to before 2026-10-16 (initial signal 2026-04-17, last same-direction signal 2026-09-16) |
| chemical | WLK | -0.05 | -10.6 | 70.66 | 2026-09-16 | 70.48 | 70.84 | 0.8 | 0.7 |  |  | 2026-10-16 | fixed_hold active from 2026-04-20 to before 2026-10-16 (initial signal 2026-04-17, last same-direction signal 2026-09-16) |
| chemical | CE | -0.028 | -9 | 46.87 | 2026-09-16 | 46.75 | 46.99 | 0.9 | 0.9 |  |  | 2026-10-16 | fixed_hold active from 2026-04-20 to before 2026-10-16 (initial signal 2026-04-17, last same-direction signal 2026-09-16) |
| chemical | EMN | -0.028 | -6.5 | 65.07 | 2026-09-16 | 64.91 | 65.23 | 1 | 0.2 |  |  | 2026-10-16 | fixed_hold active from 2026-04-20 to before 2026-10-16 (initial signal 2026-04-17, last same-direction signal 2026-09-16) |
| chemical | HUN | -0.028 | -45.7 | 9.19 | 2026-09-16 | 9.17 | 9.21 | 1.5 | 0.7 |  |  | 2026-10-16 | fixed_hold active from 2026-04-20 to before 2026-10-16 (initial signal 2026-04-17, last same-direction signal 2026-09-16) |
| chemical | AVNT | -0.014 | -5.1 | 40.93 | 2026-09-16 | 40.83 | 41.03 | 1.2 | -0 |  |  | 2026-10-16 | fixed_hold active from 2026-04-20 to before 2026-10-16 (initial signal 2026-04-17, last same-direction signal 2026-09-16) |
| psx_ref | PSX | -0.05 | -2.8 | 264.63 | 2026-09-16 | 263.97 | 265.29 | 0.1 | 1.1 |  |  | 2026-09-22 | fixed_hold active from 2026-09-09 to before 2026-09-22 (initial signal 2026-09-08, last same-direction signal 2026-09-16) |
| refiner | DK | -0.05 | -9.5 | 79.16 | 2026-09-16 | 78.96 | 79.36 | 0.2 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | PBF | -0.03 | -5.9 | 75.93 | 2026-09-16 | 75.74 | 76.12 | 0 | 1.8 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | DINO | -0.02 | -2.6 | 113.97 | 2026-09-16 | 113.69 | 114.25 | 0.1 | 1 |  |  |  | 5d rolling-mean band_hysteresis active |
| services | FTI | -0.02 | -4.1 | 72.78 | 2026-09-16 | 72.6 | 72.96 | 0.6 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -5.7 | 52.3 | 2026-09-16 | 52.17 | 52.43 | 1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4.3 | 34.51 | 2026-09-16 | 34.42 | 34.6 | 0.6 | 1.2 |  |  |  | continuous hysteresis sign active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.224416 | 4.46421 | 754.05 | 2026-09-16 | 752.165 | 755.935 |
| XLE | 0.445197 | 104.294 | 64.03 | 2026-09-16 | 63.8699 | 64.1901 |
| XME | 0 | 0 | 108.77 | 2026-09-16 | 108.498 | 109.042 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | bwt | ERO | SELL | -21 | -21 | -0.045192 | False |  | 32.28 | 2026-09-16 | 32.1993 | 32.3607 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | fuel | CASY | SELL | -1 | -1 | -0.0392667 | False |  | 589 | 2026-09-16 | 587.528 | 590.472 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | metals | CRS | SELL | -1 | -1 | -0.0274533 | False |  | 411.8 | 2026-09-16 | 410.77 | 412.829 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | metals | ATI | SELL | -2 | -2 | -0.0252867 | False |  | 189.65 | 2026-09-16 | 189.176 | 190.124 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | metals | HWM | SELL | -1 | -1 | -0.015182 | False |  | 227.73 | 2026-09-16 | 227.161 | 228.299 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | bwt | TECK | SELL | -3 | -3 | -0.01285 | False |  | 64.25 | 2026-09-16 | 64.0894 | 64.4106 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | DK | BUY | 1 | 1 | 0.00527733 | False |  | 79.16 | 2026-09-16 | 78.9621 | 79.3579 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | services | SLB | SELL | -1 | -1 | -0.00348667 | False |  | 52.3 | 2026-09-16 | 52.1692 | 52.4307 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | SPY | BUY | 1 | 1 | 0.05027 | False |  | 754.05 | 2026-09-16 | 752.165 | 755.935 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XME | BUY | 10 | 10 | 0.0725133 | False |  | 108.77 | 2026-09-16 | 108.498 | 109.042 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XLE | SELL | -2 | -2 | -0.00853733 | False |  | 64.03 | 2026-09-16 | 63.8699 | 64.1901 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
