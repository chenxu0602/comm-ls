# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-10-14

- Signal as-of date: 2026-10-13
- Target trading date: 2026-10-14
- AUM: $15,000.00
- Gross stock weight: 54.30%
- Single-name stock weight cap: 5.00%
- Net stock weight: -5.30%
- Gross hedge weight: 28.51%
- Total net weight after hedges: 11.24%
- Estimated turnover from current positions: 7.14%
- Full eligible order turnover: 3.03%
- Today's total child-order turnover: 4.48%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $1.68
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.245 | 0.245 | 3675 | 3675 | 8 |
| stock_short_without_hedge | 0.298 | -0.298 | 4470 | -4470 | 10 |
| total_hedge | 0.285076 | 0.16538 | 4276.14 | 2480.71 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.045 | 18.4 | 36.65 | 2026-10-13 | 36.56 | 36.74 | 0.4 | 1.1 |  |  | 2026-10-19 | fixed_hold active from 2026-09-28 to before 2026-10-19 (initial signal 2026-09-25, last same-direction signal 2026-10-13) |
| bwt | TECK | 0.015 | 3.3 | 67.17 | 2026-10-13 | 67 | 67.34 | 0.9 | 0.7 |  |  | 2026-10-19 | fixed_hold active from 2026-09-28 to before 2026-10-19 (initial signal 2026-09-25, last same-direction signal 2026-10-13) |
| chemical | DOW | -0.05 | -26.3 | 28.51 | 2026-10-13 | 28.44 | 28.58 | 0.2 | 1.1 |  |  | 2026-11-12 | fixed_hold active from 2026-04-20 to before 2026-11-12 (initial signal 2026-04-17, last same-direction signal 2026-10-13) |
| chemical | LYB | -0.05 | -12.5 | 60.01 | 2026-10-13 | 59.86 | 60.16 | -0.1 | 1.2 |  |  | 2026-11-12 | fixed_hold active from 2026-04-20 to before 2026-11-12 (initial signal 2026-04-17, last same-direction signal 2026-10-13) |
| chemical | WLK | -0.05 | -12.1 | 61.86 | 2026-10-13 | 61.71 | 62.01 | 0.8 | 0.7 |  |  | 2026-11-12 | fixed_hold active from 2026-04-20 to before 2026-11-12 (initial signal 2026-04-17, last same-direction signal 2026-10-13) |
| chemical | CE | -0.028 | -9.4 | 44.73 | 2026-10-13 | 44.62 | 44.84 | 0.8 | 1 |  |  | 2026-11-12 | fixed_hold active from 2026-04-20 to before 2026-11-12 (initial signal 2026-04-17, last same-direction signal 2026-10-13) |
| chemical | EMN | -0.028 | -6.7 | 63 | 2026-10-13 | 62.84 | 63.16 | 0.9 | 0.2 |  |  | 2026-11-12 | fixed_hold active from 2026-04-20 to before 2026-11-12 (initial signal 2026-04-17, last same-direction signal 2026-10-13) |
| chemical | HUN | -0.028 | -51.5 | 8.16 | 2026-10-13 | 8.14 | 8.18 | 1.4 | 0.7 |  |  | 2026-11-12 | fixed_hold active from 2026-04-20 to before 2026-11-12 (initial signal 2026-04-17, last same-direction signal 2026-10-13) |
| chemical | AVNT | -0.014 | -5.3 | 39.54 | 2026-10-13 | 39.44 | 39.64 | 1.1 | -0 |  |  | 2026-11-12 | fixed_hold active from 2026-04-20 to before 2026-11-12 (initial signal 2026-04-17, last same-direction signal 2026-10-13) |
| cro | MPC | 0.02 | 0.6 | 476.98 | 2026-10-13 | 475.79 | 478.17 | -0.2 | 0 |  |  |  | continuous hysteresis sign active |
| cro | VLO | 0.015 | 0.5 | 456.46 | 2026-10-13 | 455.32 | 457.6 | -0.4 | 0 |  |  |  | continuous hysteresis sign active |
| psx_ref\|cro | PSX | 0.05 | 2.6 | 292.73 | 2026-10-13 | 292 | 293.46 | -0 | 0.9 |  |  | 2026-10-19 | fixed_hold active from 2026-10-08 to before 2026-10-19 (initial signal 2026-10-07, last same-direction signal 2026-10-13)\|continuous hysteresis sign active |
| refiner | DK | 0.05 | 9.3 | 80.75 | 2026-10-13 | 80.55 | 80.95 | 0.1 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | PBF | 0.03 | 4.9 | 91.17 | 2026-10-13 | 90.94 | 91.4 | -0 | 1.8 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | DINO | 0.02 | 2.3 | 128.23 | 2026-10-13 | 127.91 | 128.55 | 0.1 | 1.1 |  |  |  | 5d rolling-mean band_hysteresis active |
| services | FTI | -0.02 | -4.2 | 70.72 | 2026-10-13 | 70.54 | 70.9 | 0.7 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -6.2 | 48.77 | 2026-10-13 | 48.65 | 48.89 | 1.1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4.6 | 32.79 | 2026-10-13 | 32.71 | 32.87 | 0.6 | 1.1 |  |  |  | continuous hysteresis sign active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.160095 | 3.08663 | 778.01 | 2026-10-13 | 776.065 | 779.955 |
| XLE | 0.0651327 | 14.5385 | 67.2 | 2026-10-13 | 67.032 | 67.368 |
| XME | -0.0598476 | -8.65184 | 103.76 | 2026-10-13 | 103.501 | 104.019 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | cro | VLO | SELL | -1 | -1 | -0.0304307 | False |  | 456.46 | 2026-10-13 | 455.319 | 457.601 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | DK | SELL | -1 | -1 | -0.00538333 | False |  | 80.75 | 2026-10-13 | 80.5481 | 80.9519 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XLE | SELL | -1 | -2 | -0.00896 | False |  | 67.2 | 2026-10-13 | 67.032 | 67.368 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |


## Strategy changes and allocation notes

- CRO (crack refiner-only) added effective 2026-10-06: 10% allocation from unused CL capacity. CL AUM remains $15,000; existing sleeve weights are NOT reduced or renormalized.
- CRO stocks: VLO/MPC/PSX = 30/40/30%; crack_03; signal lookback 30 sessions; volatility lookback 30 (minimum 20); no signal smoothing; balance=0.5 (maximum CRO stock gross 5% of CL AUM).
- CRO explicit hedge is SPY ONLY, not XLE. Preserve component hedge ownership when PSX overlaps existing sleeves; net single-name cap and execution constraints still apply.
- This addition is refiner-only CRO, NOT the refiner-producer CRP, refiner-VLCC CRV, or refiner-chemical CRC research strategies.
- CRO stock target state for this package: active. Flat CRO must not create reallocation trades under identical inputs.
- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.
- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.
- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.
## Beta method for 2026-10-14 — as-of 2026-10-13

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-10-14-kibydwm3/cached/targets-cl/2026-10-14. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
