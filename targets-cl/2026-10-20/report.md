# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-10-20

- Signal as-of date: 2026-10-19
- Target trading date: 2026-10-20
- AUM: $15,000.00
- Gross stock weight: 50.80%
- Single-name stock weight cap: 5.00%
- Net stock weight: -8.80%
- Gross hedge weight: 25.47%
- Total net weight after hedges: 4.57%
- Estimated turnover from current positions: 4.02%
- Full eligible order turnover: 0.29%
- Today's total child-order turnover: 0.99%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $0.37
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.21 | 0.21 | 3150 | 3150 | 6 |
| stock_short_without_hedge | 0.298 | -0.298 | 4470 | -4470 | 10 |
| total_hedge | 0.25471 | 0.133693 | 3820.66 | 2005.4 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.045 | 19.6 | 34.43 | 2026-10-19 | 34.34 | 34.52 | 0.4 | 1.1 |  |  | 2026-10-23 | fixed_hold active from 2026-09-28 to before 2026-10-23 (initial signal 2026-09-25, last same-direction signal 2026-10-19) |
| bwt | TECK | 0.015 | 3.5 | 63.48 | 2026-10-19 | 63.32 | 63.64 | 0.9 | 0.7 |  |  | 2026-10-23 | fixed_hold active from 2026-09-28 to before 2026-10-23 (initial signal 2026-09-25, last same-direction signal 2026-10-19) |
| chemical | DOW | -0.05 | -24.9 | 30.08 | 2026-10-19 | 30 | 30.16 | 0.2 | 1.1 |  |  | 2026-11-18 | fixed_hold active from 2026-04-20 to before 2026-11-18 (initial signal 2026-04-17, last same-direction signal 2026-10-19) |
| chemical | LYB | -0.05 | -11.8 | 63.71 | 2026-10-19 | 63.55 | 63.87 | -0.1 | 1.1 |  |  | 2026-11-18 | fixed_hold active from 2026-04-20 to before 2026-11-18 (initial signal 2026-04-17, last same-direction signal 2026-10-19) |
| chemical | WLK | -0.05 | -12 | 62.29 | 2026-10-19 | 62.13 | 62.45 | 0.8 | 0.7 |  |  | 2026-11-18 | fixed_hold active from 2026-04-20 to before 2026-11-18 (initial signal 2026-04-17, last same-direction signal 2026-10-19) |
| chemical | CE | -0.028 | -8.8 | 47.88 | 2026-10-19 | 47.76 | 48 | 0.8 | 1 |  |  | 2026-11-18 | fixed_hold active from 2026-04-20 to before 2026-11-18 (initial signal 2026-04-17, last same-direction signal 2026-10-19) |
| chemical | EMN | -0.028 | -6.7 | 62.48 | 2026-10-19 | 62.32 | 62.64 | 0.9 | 0.2 |  |  | 2026-11-18 | fixed_hold active from 2026-04-20 to before 2026-11-18 (initial signal 2026-04-17, last same-direction signal 2026-10-19) |
| chemical | HUN | -0.028 | -50.4 | 8.33 | 2026-10-19 | 8.31 | 8.35 | 1.4 | 0.7 |  |  | 2026-11-18 | fixed_hold active from 2026-04-20 to before 2026-11-18 (initial signal 2026-04-17, last same-direction signal 2026-10-19) |
| chemical | AVNT | -0.014 | -5.3 | 39.51 | 2026-10-19 | 39.41 | 39.61 | 1.1 | -0 |  |  | 2026-11-18 | fixed_hold active from 2026-04-20 to before 2026-11-18 (initial signal 2026-04-17, last same-direction signal 2026-10-19) |
| psx_ref | PSX | 0.05 | 2.6 | 290.55 | 2026-10-19 | 289.82 | 291.28 | 0.1 | 1.1 |  |  | 2026-10-23 | fixed_hold active from 2026-10-08 to before 2026-10-23 (initial signal 2026-10-07, last same-direction signal 2026-10-19) |
| refiner | DK | 0.05 | 10 | 75.08 | 2026-10-19 | 74.89 | 75.27 | 0.1 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | PBF | 0.03 | 5.5 | 81.26 | 2026-10-19 | 81.06 | 81.46 | 0.1 | 1.7 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | DINO | 0.02 | 2.4 | 124.42 | 2026-10-19 | 124.11 | 124.73 | 0.1 | 1 |  |  |  | 5d rolling-mean band_hysteresis active |
| services | FTI | -0.02 | -4.3 | 69.86 | 2026-10-19 | 69.69 | 70.03 | 0.7 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -6.1 | 49.09 | 2026-10-19 | 48.97 | 49.21 | 1.1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4.5 | 32.98 | 2026-10-19 | 32.9 | 33.06 | 0.6 | 1.1 |  |  |  | continuous hysteresis sign active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.142717 | 2.79296 | 766.48 | 2026-10-19 | 764.564 | 768.396 |
| XLE | 0.0514851 | 11.3905 | 67.8 | 2026-10-19 | 67.6305 | 67.9695 |
| XME | -0.0605087 | -8.95365 | 101.37 | 2026-10-19 | 101.117 | 101.623 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | refiner | PBF | BUY | 1 | 1 | 0.00541733 | False |  | 81.26 | 2026-10-19 | 81.0569 | 81.4632 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XLE | SELL | 0 | -1 | -0.00452 | False |  | 67.8 | 2026-10-19 | 67.6305 | 67.9695 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |


## Strategy changes and allocation notes

- CRO (crack refiner-only) added effective 2026-10-06: 10% allocation from unused CL capacity. CL AUM remains $15,000; existing sleeve weights are NOT reduced or renormalized.
- CRO stocks: VLO/MPC/PSX = 30/40/30%; crack_03; signal lookback 30 sessions; volatility lookback 30 (minimum 20); no signal smoothing; balance=0.5 (maximum CRO stock gross 5% of CL AUM).
- CRO explicit hedge is SPY ONLY, not XLE. Preserve component hedge ownership when PSX overlaps existing sleeves; net single-name cap and execution constraints still apply.
- This addition is refiner-only CRO, NOT the refiner-producer CRP, refiner-VLCC CRV, or refiner-chemical CRC research strategies.
- CRO stock target state for this package: flat. Flat CRO must not create reallocation trades under identical inputs.
- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.
- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.
- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.
## Beta method for 2026-10-20 — as-of 2026-10-19

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-10-20-4i1_am1h/cached/targets-cl/2026-10-20. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
