# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-10-07

- Signal as-of date: 2026-10-06
- Target trading date: 2026-10-07
- AUM: $15,000.00
- Gross stock weight: 50.80%
- Single-name stock weight cap: 5.00%
- Net stock weight: -8.80%
- Gross hedge weight: 33.62%
- Total net weight after hedges: 12.94%
- Estimated turnover from current positions: 11.41%
- Full eligible order turnover: 8.92%
- Today's total child-order turnover: 9.60%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $3.60
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.21 | 0.21 | 3150 | 3150 | 8 |
| stock_short_without_hedge | 0.298 | -0.298 | 4470 | -4470 | 10 |
| total_hedge | 0.336205 | 0.217432 | 5043.08 | 3261.48 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.045 | 17.8 | 37.93 | 2026-10-06 | 37.84 | 38.02 | 0.4 | 1.1 |  |  | 2026-10-12 | fixed_hold active from 2026-09-28 to before 2026-10-12 (initial signal 2026-09-25, last same-direction signal 2026-10-06) |
| bwt | TECK | 0.015 | 3.4 | 67.1 | 2026-10-06 | 66.93 | 67.27 | 0.9 | 0.7 |  |  | 2026-10-12 | fixed_hold active from 2026-09-28 to before 2026-10-12 (initial signal 2026-09-25, last same-direction signal 2026-10-06) |
| chemical | DOW | -0.05 | -26.6 | 28.16 | 2026-10-06 | 28.09 | 28.23 | 0.3 | 1.2 |  |  | 2026-11-05 | fixed_hold active from 2026-04-20 to before 2026-11-05 (initial signal 2026-04-17, last same-direction signal 2026-10-06) |
| chemical | LYB | -0.05 | -12.7 | 58.93 | 2026-10-06 | 58.78 | 59.08 | -0 | 1.2 |  |  | 2026-11-05 | fixed_hold active from 2026-04-20 to before 2026-11-05 (initial signal 2026-04-17, last same-direction signal 2026-10-06) |
| chemical | WLK | -0.05 | -11.8 | 63.39 | 2026-10-06 | 63.23 | 63.55 | 0.8 | 0.7 |  |  | 2026-11-05 | fixed_hold active from 2026-04-20 to before 2026-11-05 (initial signal 2026-04-17, last same-direction signal 2026-10-06) |
| chemical | CE | -0.028 | -9.4 | 44.85 | 2026-10-06 | 44.74 | 44.96 | 0.9 | 1 |  |  | 2026-11-05 | fixed_hold active from 2026-04-20 to before 2026-11-05 (initial signal 2026-04-17, last same-direction signal 2026-10-06) |
| chemical | EMN | -0.028 | -6.6 | 64.11 | 2026-10-06 | 63.95 | 64.27 | 1 | 0.2 |  |  | 2026-11-05 | fixed_hold active from 2026-04-20 to before 2026-11-05 (initial signal 2026-04-17, last same-direction signal 2026-10-06) |
| chemical | HUN | -0.028 | -47.9 | 8.77 | 2026-10-06 | 8.75 | 8.79 | 1.4 | 0.7 |  |  | 2026-11-05 | fixed_hold active from 2026-04-20 to before 2026-11-05 (initial signal 2026-04-17, last same-direction signal 2026-10-06) |
| chemical | AVNT | -0.014 | -5.1 | 41.49 | 2026-10-06 | 41.39 | 41.59 | 1.1 | -0 |  |  | 2026-11-05 | fixed_hold active from 2026-04-20 to before 2026-11-05 (initial signal 2026-04-17, last same-direction signal 2026-10-06) |
| cro | MPC | 0.02 | 0.7 | 432.36 | 2026-10-06 | 431.28 | 433.44 | -0.1 | 0 |  |  |  | continuous hysteresis sign active |
| cro | PSX | 0.015 | 0.8 | 269.79 | 2026-10-06 | 269.12 | 270.46 | -0.2 | 0 |  |  |  | continuous hysteresis sign active |
| cro | VLO | 0.015 | 0.5 | 419.22 | 2026-10-06 | 418.17 | 420.27 | -0.3 | 0 |  |  |  | continuous hysteresis sign active |
| refiner | DK | 0.05 | 9.9 | 75.67 | 2026-10-06 | 75.48 | 75.86 | 0.2 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | PBF | 0.03 | 5.4 | 82.88 | 2026-10-06 | 82.67 | 83.09 | 0 | 1.7 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | DINO | 0.02 | 2.6 | 114.6 | 2026-10-06 | 114.31 | 114.89 | 0.1 | 1 |  |  |  | 5d rolling-mean band_hysteresis active |
| services | FTI | -0.02 | -4.3 | 69.89 | 2026-10-06 | 69.72 | 70.06 | 0.6 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -6 | 50 | 2026-10-06 | 49.88 | 50.12 | 1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4.6 | 32.72 | 2026-10-06 | 32.64 | 32.8 | 0.6 | 1.2 |  |  |  | continuous hysteresis sign active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.162 | 3.11903 | 779.09 | 2026-10-06 | 777.142 | 781.038 |
| XLE | 0.114818 | 27.0161 | 63.75 | 2026-10-06 | 63.5906 | 63.9094 |
| XME | -0.0593868 | -8.22988 | 108.24 | 2026-10-06 | 107.969 | 108.511 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | cro | PSX | BUY | 2 | 1 | 0.017986 | True |  | 269.79 | 2026-10-06 | 269.116 | 270.464 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | cro | MPC | BUY | 1 | 1 | 0.028824 | False |  | 432.36 | 2026-10-06 | 431.279 | 433.441 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | cro | VLO | BUY | 1 | 1 | 0.027948 | False |  | 419.22 | 2026-10-06 | 418.172 | 420.268 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XLE | SELL | -5 | -5 | -0.02125 | False |  | 63.75 | 2026-10-06 | 63.5906 | 63.9094 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |


## Strategy changes and allocation notes

- CRO (crack refiner-only) added effective 2026-10-06: 10% allocation from unused CL capacity. CL AUM remains $15,000; existing sleeve weights are NOT reduced or renormalized.
- CRO stocks: VLO/MPC/PSX = 30/40/30%; crack_03; signal lookback 30 sessions; volatility lookback 30 (minimum 20); no signal smoothing; balance=0.5 (maximum CRO stock gross 5% of CL AUM).
- CRO explicit hedge is SPY ONLY, not XLE. Preserve component hedge ownership when PSX overlaps existing sleeves; net single-name cap and execution constraints still apply.
- This addition is refiner-only CRO, NOT the refiner-producer CRP, refiner-VLCC CRV, or refiner-chemical CRC research strategies.
- CRO stock target state for this package: active. Flat CRO must not create reallocation trades under identical inputs.
- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.
- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.
- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.