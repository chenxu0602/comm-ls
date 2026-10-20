# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-10-15

- Signal as-of date: 2026-10-14
- Target trading date: 2026-10-15
- AUM: $15,000.00
- Gross stock weight: 54.30%
- Single-name stock weight cap: 5.00%
- Net stock weight: -5.30%
- Gross hedge weight: 28.43%
- Total net weight after hedges: 11.05%
- Estimated turnover from current positions: 7.48%
- Full eligible order turnover: 1.90%
- Today's total child-order turnover: 2.18%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $0.82
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.245 | 0.245 | 3675 | 3675 | 8 |
| stock_short_without_hedge | 0.298 | -0.298 | 4470 | -4470 | 10 |
| total_hedge | 0.284308 | 0.163454 | 4264.62 | 2451.81 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.045 | 19.6 | 34.46 | 2026-10-14 | 34.37 | 34.55 | 0.4 | 1.1 |  |  | 2026-10-20 | fixed_hold active from 2026-09-28 to before 2026-10-20 (initial signal 2026-09-25, last same-direction signal 2026-10-14) |
| bwt | TECK | 0.015 | 3.5 | 64.8 | 2026-10-14 | 64.64 | 64.96 | 0.9 | 0.7 |  |  | 2026-10-20 | fixed_hold active from 2026-09-28 to before 2026-10-20 (initial signal 2026-09-25, last same-direction signal 2026-10-14) |
| chemical | DOW | -0.05 | -25.7 | 29.19 | 2026-10-14 | 29.12 | 29.26 | 0.2 | 1.1 |  |  | 2026-11-13 | fixed_hold active from 2026-04-20 to before 2026-11-13 (initial signal 2026-04-17, last same-direction signal 2026-10-14) |
| chemical | LYB | -0.05 | -12.3 | 61.17 | 2026-10-14 | 61.02 | 61.32 | -0.1 | 1.2 |  |  | 2026-11-13 | fixed_hold active from 2026-04-20 to before 2026-11-13 (initial signal 2026-04-17, last same-direction signal 2026-10-14) |
| chemical | WLK | -0.05 | -12.1 | 62.21 | 2026-10-14 | 62.05 | 62.37 | 0.8 | 0.7 |  |  | 2026-11-13 | fixed_hold active from 2026-04-20 to before 2026-11-13 (initial signal 2026-04-17, last same-direction signal 2026-10-14) |
| chemical | CE | -0.028 | -9.2 | 45.82 | 2026-10-14 | 45.71 | 45.93 | 0.8 | 1 |  |  | 2026-11-13 | fixed_hold active from 2026-04-20 to before 2026-11-13 (initial signal 2026-04-17, last same-direction signal 2026-10-14) |
| chemical | EMN | -0.028 | -6.7 | 62.88 | 2026-10-14 | 62.72 | 63.04 | 0.9 | 0.2 |  |  | 2026-11-13 | fixed_hold active from 2026-04-20 to before 2026-11-13 (initial signal 2026-04-17, last same-direction signal 2026-10-14) |
| chemical | HUN | -0.028 | -51 | 8.24 | 2026-10-14 | 8.22 | 8.26 | 1.4 | 0.7 |  |  | 2026-11-13 | fixed_hold active from 2026-04-20 to before 2026-11-13 (initial signal 2026-04-17, last same-direction signal 2026-10-14) |
| chemical | AVNT | -0.014 | -5.4 | 38.85 | 2026-10-14 | 38.75 | 38.95 | 1.1 | -0 |  |  | 2026-11-13 | fixed_hold active from 2026-04-20 to before 2026-11-13 (initial signal 2026-04-17, last same-direction signal 2026-10-14) |
| cro | MPC | 0.02 | 0.6 | 484.92 | 2026-10-14 | 483.71 | 486.13 | -0.2 | 0 |  |  |  | continuous hysteresis sign active |
| cro | VLO | 0.015 | 0.5 | 459.78 | 2026-10-14 | 458.63 | 460.93 | -0.4 | 0 |  |  |  | continuous hysteresis sign active |
| psx_ref\|cro | PSX | 0.05 | 2.5 | 297.29 | 2026-10-14 | 296.55 | 298.03 | -0 | 0.9 |  |  | 2026-10-20 | fixed_hold active from 2026-10-08 to before 2026-10-20 (initial signal 2026-10-07, last same-direction signal 2026-10-14)\|continuous hysteresis sign active |
| refiner | DK | 0.05 | 9.5 | 78.97 | 2026-10-14 | 78.77 | 79.17 | 0.1 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | PBF | 0.03 | 5 | 89.51 | 2026-10-14 | 89.29 | 89.73 | -0 | 1.7 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | DINO | 0.02 | 2.3 | 127.69 | 2026-10-14 | 127.37 | 128.01 | 0.1 | 1 |  |  |  | 5d rolling-mean band_hysteresis active |
| services | FTI | -0.02 | -4.3 | 69.5 | 2026-10-14 | 69.33 | 69.67 | 0.7 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -6.2 | 48.51 | 2026-10-14 | 48.39 | 48.63 | 1.1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4.6 | 32.83 | 2026-10-14 | 32.75 | 32.91 | 0.6 | 1.1 |  |  |  | continuous hysteresis sign active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.15816 | 3.08264 | 769.6 | 2026-10-14 | 767.676 | 771.524 |
| XLE | 0.0657213 | 14.5767 | 67.63 | 2026-10-14 | 67.4609 | 67.7991 |
| XME | -0.0604269 | -9.07675 | 99.86 | 2026-10-14 | 99.6104 | 100.11 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | bwt | ERO | BUY | 2 | 2 | 0.00459467 | False |  | 34.46 | 2026-10-14 | 34.3738 | 34.5461 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | chemical | LYB | BUY | 1 | 1 | 0.004078 | False |  | 61.17 | 2026-10-14 | 61.0171 | 61.3229 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | chemical | DOW | BUY | 1 | 1 | 0.001946 | False |  | 29.19 | 2026-10-14 | 29.117 | 29.263 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XME | SELL | -1 | -1 | -0.00665733 | False |  | 99.86 | 2026-10-14 | 99.6104 | 100.11 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XLE | SELL | 1 | -1 | -0.00450867 | False |  | 67.63 | 2026-10-14 | 67.4609 | 67.7991 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |


## Strategy changes and allocation notes

- CRO (crack refiner-only) added effective 2026-10-06: 10% allocation from unused CL capacity. CL AUM remains $15,000; existing sleeve weights are NOT reduced or renormalized.
- CRO stocks: VLO/MPC/PSX = 30/40/30%; crack_03; signal lookback 30 sessions; volatility lookback 30 (minimum 20); no signal smoothing; balance=0.5 (maximum CRO stock gross 5% of CL AUM).
- CRO explicit hedge is SPY ONLY, not XLE. Preserve component hedge ownership when PSX overlaps existing sleeves; net single-name cap and execution constraints still apply.
- This addition is refiner-only CRO, NOT the refiner-producer CRP, refiner-VLCC CRV, or refiner-chemical CRC research strategies.
- CRO stock target state for this package: active. Flat CRO must not create reallocation trades under identical inputs.
- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.
- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.
- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.
## Beta method for 2026-10-15 — as-of 2026-10-14

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-10-15-fe4cg33a/cached/targets-cl/2026-10-15. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
