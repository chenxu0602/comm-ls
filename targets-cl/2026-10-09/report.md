# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-10-09

- Signal as-of date: 2026-10-08
- Target trading date: 2026-10-09
- AUM: $15,000.00
- Gross stock weight: 49.80%
- Single-name stock weight cap: 5.00%
- Net stock weight: -9.80%
- Gross hedge weight: 27.98%
- Total net weight after hedges: 6.32%
- Estimated turnover from current positions: 10.79%
- Full eligible order turnover: 8.45%
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
| stock_long_without_hedge | 0.2 | 0.2 | 3000 | 3000 | 6 |
| stock_short_without_hedge | 0.298 | -0.298 | 4470 | -4470 | 10 |
| total_hedge | 0.279812 | 0.161153 | 4197.17 | 2417.3 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.045 | 18.8 | 35.98 | 2026-10-08 | 35.89 | 36.07 | 0.5 | 1.1 |  |  | 2026-10-14 | fixed_hold active from 2026-09-28 to before 2026-10-14 (initial signal 2026-09-25, last same-direction signal 2026-10-08) |
| bwt | TECK | 0.015 | 3.5 | 64.82 | 2026-10-08 | 64.66 | 64.98 | 0.9 | 0.7 |  |  | 2026-10-14 | fixed_hold active from 2026-09-28 to before 2026-10-14 (initial signal 2026-09-25, last same-direction signal 2026-10-08) |
| chemical | DOW | -0.05 | -26.2 | 28.59 | 2026-10-08 | 28.52 | 28.66 | 0.3 | 1.2 |  |  | 2026-11-09 | fixed_hold active from 2026-04-20 to before 2026-11-09 (initial signal 2026-04-17, last same-direction signal 2026-10-08) |
| chemical | LYB | -0.05 | -12.4 | 60.34 | 2026-10-08 | 60.19 | 60.49 | -0 | 1.2 |  |  | 2026-11-09 | fixed_hold active from 2026-04-20 to before 2026-11-09 (initial signal 2026-04-17, last same-direction signal 2026-10-08) |
| chemical | WLK | -0.05 | -12 | 62.31 | 2026-10-08 | 62.15 | 62.47 | 0.8 | 0.7 |  |  | 2026-11-09 | fixed_hold active from 2026-04-20 to before 2026-11-09 (initial signal 2026-04-17, last same-direction signal 2026-10-08) |
| chemical | CE | -0.028 | -9.4 | 44.81 | 2026-10-08 | 44.7 | 44.92 | 0.9 | 1 |  |  | 2026-11-09 | fixed_hold active from 2026-04-20 to before 2026-11-09 (initial signal 2026-04-17, last same-direction signal 2026-10-08) |
| chemical | EMN | -0.028 | -6.6 | 63.76 | 2026-10-08 | 63.6 | 63.92 | 1 | 0.2 |  |  | 2026-11-09 | fixed_hold active from 2026-04-20 to before 2026-11-09 (initial signal 2026-04-17, last same-direction signal 2026-10-08) |
| chemical | HUN | -0.028 | -49.4 | 8.5 | 2026-10-08 | 8.48 | 8.52 | 1.4 | 0.7 |  |  | 2026-11-09 | fixed_hold active from 2026-04-20 to before 2026-11-09 (initial signal 2026-04-17, last same-direction signal 2026-10-08) |
| chemical | AVNT | -0.014 | -5.1 | 40.98 | 2026-10-08 | 40.88 | 41.08 | 1.1 | -0 |  |  | 2026-11-09 | fixed_hold active from 2026-04-20 to before 2026-11-09 (initial signal 2026-04-17, last same-direction signal 2026-10-08) |
| psx_ref | PSX | 0.04 | 2.1 | 281.6 | 2026-10-08 | 280.9 | 282.3 | 0.1 | 1.1 |  |  | 2026-10-14 | fixed_hold active from 2026-10-08 to before 2026-10-14 (initial signal 2026-10-07, last same-direction signal 2026-10-08) |
| refiner | DK | 0.05 | 9.8 | 76.6 | 2026-10-08 | 76.41 | 76.79 | 0.2 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | PBF | 0.03 | 5 | 89.34 | 2026-10-08 | 89.12 | 89.56 | 0 | 1.7 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | DINO | 0.02 | 2.5 | 120.72 | 2026-10-08 | 120.42 | 121.02 | 0.1 | 1 |  |  |  | 5d rolling-mean band_hysteresis active |
| services | FTI | -0.02 | -4.3 | 69.63 | 2026-10-08 | 69.46 | 69.8 | 0.6 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -6.1 | 48.98 | 2026-10-08 | 48.86 | 49.1 | 1.1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4.6 | 32.57 | 2026-10-08 | 32.49 | 32.65 | 0.6 | 1.2 |  |  |  | continuous hysteresis sign active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.149521 | 2.89796 | 773.93 | 2026-10-08 | 771.995 | 775.865 |
| XLE | 0.0709613 | 16.3154 | 65.24 | 2026-10-08 | 65.0769 | 65.4031 |
| XME | -0.0593291 | -8.50719 | 104.61 | 2026-10-08 | 104.348 | 104.872 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | cro | MPC | SELL | -1 | -1 | -0.0308893 | False |  | 463.34 | 2026-10-08 | 462.182 | 464.498 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | cro | VLO | SELL | -1 | -1 | -0.0295867 | False |  | 443.8 | 2026-10-08 | 442.69 | 444.909 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | psx_ref | PSX | SELL | -1 | -1 | -0.0187733 | False |  | 281.6 | 2026-10-08 | 280.896 | 282.304 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | DINO | SELL | -1 | -1 | -0.008048 | False |  | 120.72 | 2026-10-08 | 120.418 | 121.022 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XLE | BUY | 0 | 2 | 0.00869867 | False |  | 65.24 | 2026-10-08 | 65.0769 | 65.4031 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |


## Strategy changes and allocation notes

- CRO (crack refiner-only) added effective 2026-10-06: 10% allocation from unused CL capacity. CL AUM remains $15,000; existing sleeve weights are NOT reduced or renormalized.
- CRO stocks: VLO/MPC/PSX = 30/40/30%; crack_03; signal lookback 30 sessions; volatility lookback 30 (minimum 20); no signal smoothing; balance=0.5 (maximum CRO stock gross 5% of CL AUM).
- CRO explicit hedge is SPY ONLY, not XLE. Preserve component hedge ownership when PSX overlaps existing sleeves; net single-name cap and execution constraints still apply.
- This addition is refiner-only CRO, NOT the refiner-producer CRP, refiner-VLCC CRV, or refiner-chemical CRC research strategies.
- CRO stock target state for this package: flat. Flat CRO must not create reallocation trades under identical inputs.
- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.
- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.
- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.
## Operator beta decision — 2026-10-09

Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-10-09-31i2mpxo/cached/targets-cl/2026-10-09. Agriculture's existing component-specific cached beta is unchanged.
