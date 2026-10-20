# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-10-08

- Signal as-of date: 2026-10-07
- Target trading date: 2026-10-08
- AUM: $15,000.00
- Gross stock weight: 54.30%
- Single-name stock weight cap: 5.00%
- Net stock weight: -5.30%
- Gross hedge weight: 29.52%
- Total net weight after hedges: 12.34%
- Estimated turnover from current positions: 13.93%
- Full eligible order turnover: 9.13%
- Today's total child-order turnover: 10.50%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $3.94
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.245 | 0.245 | 3675 | 3675 | 8 |
| stock_short_without_hedge | 0.298 | -0.298 | 4470 | -4470 | 10 |
| total_hedge | 0.295153 | 0.176441 | 4427.3 | 2646.61 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.045 | 18.4 | 36.78 | 2026-10-07 | 36.69 | 36.87 | 0.4 | 1.1 |  |  | 2026-10-13 | fixed_hold active from 2026-09-28 to before 2026-10-13 (initial signal 2026-09-25, last same-direction signal 2026-10-07) |
| bwt | TECK | 0.015 | 3.4 | 65.39 | 2026-10-07 | 65.23 | 65.55 | 0.9 | 0.7 |  |  | 2026-10-13 | fixed_hold active from 2026-09-28 to before 2026-10-13 (initial signal 2026-09-25, last same-direction signal 2026-10-07) |
| chemical | DOW | -0.05 | -27 | 27.77 | 2026-10-07 | 27.7 | 27.84 | 0.3 | 1.2 |  |  | 2026-11-06 | fixed_hold active from 2026-04-20 to before 2026-11-06 (initial signal 2026-04-17, last same-direction signal 2026-10-07) |
| chemical | LYB | -0.05 | -12.8 | 58.49 | 2026-10-07 | 58.34 | 58.64 | -0 | 1.2 |  |  | 2026-11-06 | fixed_hold active from 2026-04-20 to before 2026-11-06 (initial signal 2026-04-17, last same-direction signal 2026-10-07) |
| chemical | WLK | -0.05 | -12.2 | 61.52 | 2026-10-07 | 61.37 | 61.67 | 0.8 | 0.7 |  |  | 2026-11-06 | fixed_hold active from 2026-04-20 to before 2026-11-06 (initial signal 2026-04-17, last same-direction signal 2026-10-07) |
| chemical | CE | -0.028 | -9.6 | 43.86 | 2026-10-07 | 43.75 | 43.97 | 0.9 | 1 |  |  | 2026-11-06 | fixed_hold active from 2026-04-20 to before 2026-11-06 (initial signal 2026-04-17, last same-direction signal 2026-10-07) |
| chemical | EMN | -0.028 | -6.6 | 63.25 | 2026-10-07 | 63.09 | 63.41 | 1 | 0.2 |  |  | 2026-11-06 | fixed_hold active from 2026-04-20 to before 2026-11-06 (initial signal 2026-04-17, last same-direction signal 2026-10-07) |
| chemical | HUN | -0.028 | -48.7 | 8.63 | 2026-10-07 | 8.61 | 8.65 | 1.4 | 0.7 |  |  | 2026-11-06 | fixed_hold active from 2026-04-20 to before 2026-11-06 (initial signal 2026-04-17, last same-direction signal 2026-10-07) |
| chemical | AVNT | -0.014 | -5.1 | 41 | 2026-10-07 | 40.9 | 41.1 | 1.1 | -0 |  |  | 2026-11-06 | fixed_hold active from 2026-04-20 to before 2026-11-06 (initial signal 2026-04-17, last same-direction signal 2026-10-07) |
| cro | MPC | 0.02 | 0.7 | 442.26 | 2026-10-07 | 441.15 | 443.37 | -0.1 | 0 |  |  |  | continuous hysteresis sign active |
| cro | VLO | 0.015 | 0.5 | 424.1 | 2026-10-07 | 423.04 | 425.16 | -0.3 | 0 |  |  |  | continuous hysteresis sign active |
| psx_ref\|cro | PSX | 0.05 | 2.8 | 271.62 | 2026-10-07 | 270.94 | 272.3 | -0 | 0.8 |  |  | 2026-10-13 | fixed_hold active from 2026-10-08 to before 2026-10-13 (initial signal 2026-10-07, last same-direction signal 2026-10-07)\|continuous hysteresis sign active |
| refiner | DK | 0.05 | 9.9 | 75.46 | 2026-10-07 | 75.27 | 75.65 | 0.2 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | PBF | 0.03 | 5.4 | 83.68 | 2026-10-07 | 83.47 | 83.89 | 0 | 1.7 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | DINO | 0.02 | 2.6 | 115.63 | 2026-10-07 | 115.34 | 115.92 | 0.1 | 1 |  |  |  | 5d rolling-mean band_hysteresis active |
| services | FTI | -0.02 | -4.4 | 68.4 | 2026-10-07 | 68.23 | 68.57 | 0.6 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -6.3 | 47.96 | 2026-10-07 | 47.84 | 48.08 | 1.1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4.7 | 31.75 | 2026-10-07 | 31.67 | 31.83 | 0.6 | 1.2 |  |  |  | continuous hysteresis sign active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.160339 | 3.09448 | 777.22 | 2026-10-07 | 775.277 | 779.163 |
| XLE | 0.0754577 | 17.864 | 63.36 | 2026-10-07 | 63.2016 | 63.5184 |
| XME | -0.0593563 | -8.49241 | 104.84 | 2026-10-07 | 104.578 | 105.102 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | psx_ref\|cro | PSX | BUY | 3 | 3 | 0.054324 | False |  | 271.62 | 2026-10-07 | 270.941 | 272.299 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | chemical | EMN | SELL | -1 | -1 | -0.00421667 | False |  | 63.25 | 2026-10-07 | 63.0919 | 63.4081 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XLE | SELL | -9 | -11 | -0.046464 | False |  | 63.36 | 2026-10-07 | 63.2016 | 63.5184 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |


## Strategy changes and allocation notes

- CRO (crack refiner-only) added effective 2026-10-06: 10% allocation from unused CL capacity. CL AUM remains $15,000; existing sleeve weights are NOT reduced or renormalized.
- CRO stocks: VLO/MPC/PSX = 30/40/30%; crack_03; signal lookback 30 sessions; volatility lookback 30 (minimum 20); no signal smoothing; balance=0.5 (maximum CRO stock gross 5% of CL AUM).
- CRO explicit hedge is SPY ONLY, not XLE. Preserve component hedge ownership when PSX overlaps existing sleeves; net single-name cap and execution constraints still apply.
- This addition is refiner-only CRO, NOT the refiner-producer CRP, refiner-VLCC CRV, or refiner-chemical CRC research strategies.
- CRO stock target state for this package: active. Flat CRO must not create reallocation trades under identical inputs.
- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.
- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.
- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.