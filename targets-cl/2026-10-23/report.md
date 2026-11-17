# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-10-23

- Signal as-of date: 2026-10-22
- Target trading date: 2026-10-23
- AUM: $15,000.00
- Gross stock weight: 40.00%
- Single-name stock weight cap: 5.00%
- Net stock weight: -8.00%
- Gross hedge weight: 14.24%
- Total net weight after hedges: -6.03%
- Estimated turnover from current positions: 35.91%
- Full eligible order turnover: 34.97%
- Today's total child-order turnover: 36.72%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $13.77
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.16 | 0.16 | 2400 | 2400 | 5 |
| stock_short_without_hedge | 0.24 | -0.24 | 3600 | -3600 | 13 |
| total_hedge | 0.142439 | 0.019655 | 2136.58 | 294.82 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.045 | 22.4 | 30.13 | 2026-10-22 | 30.05 | 30.21 | 0.3 | 1.1 |  |  | 2026-10-28 | fixed_hold active from 2026-09-28 to before 2026-10-28 (initial signal 2026-09-25, last same-direction signal 2026-10-22) |
| bwt | TECK | 0.015 | 3.8 | 58.9 | 2026-10-22 | 58.75 | 59.05 | 0.8 | 0.7 |  |  | 2026-10-28 | fixed_hold active from 2026-09-28 to before 2026-10-28 (initial signal 2026-09-25, last same-direction signal 2026-10-22) |
| chemical | LYB | -0.035 | -8 | 65.37 | 2026-10-22 | 65.21 | 65.53 | -0.1 | 1.1 |  |  | 2026-11-23 | fixed_hold active from 2026-04-20 to before 2026-11-23 (initial signal 2026-04-17, last same-direction signal 2026-10-22) |
| chemical | DOW | -0.028 | -13.2 | 31.81 | 2026-10-22 | 31.73 | 31.89 | 0.1 | 1.1 |  |  | 2026-11-23 | fixed_hold active from 2026-04-20 to before 2026-11-23 (initial signal 2026-04-17, last same-direction signal 2026-10-22) |
| chemical | WLK | -0.028 | -6.5 | 64.14 | 2026-10-22 | 63.98 | 64.3 | 0.7 | 0.7 |  |  | 2026-11-23 | fixed_hold active from 2026-04-20 to before 2026-11-23 (initial signal 2026-04-17, last same-direction signal 2026-10-22) |
| chemical | CE | -0.014 | -4.4 | 47.22 | 2026-10-22 | 47.1 | 47.34 | 0.8 | 1 |  |  | 2026-11-23 | fixed_hold active from 2026-04-20 to before 2026-11-23 (initial signal 2026-04-17, last same-direction signal 2026-10-22) |
| chemical | EMN | -0.014 | -3.2 | 65.31 | 2026-10-22 | 65.15 | 65.47 | 0.9 | 0.2 |  |  | 2026-11-23 | fixed_hold active from 2026-04-20 to before 2026-11-23 (initial signal 2026-04-17, last same-direction signal 2026-10-22) |
| chemical | HUN | -0.014 | -24.1 | 8.72 | 2026-10-22 | 8.7 | 8.74 | 1.3 | 0.7 |  |  | 2026-11-23 | fixed_hold active from 2026-04-20 to before 2026-11-23 (initial signal 2026-04-17, last same-direction signal 2026-10-22) |
| chemical | AVNT | -0.007 | -2.6 | 40.58 | 2026-10-22 | 40.48 | 40.68 | 1.1 | -0 |  |  | 2026-11-23 | fixed_hold active from 2026-04-20 to before 2026-11-23 (initial signal 2026-04-17, last same-direction signal 2026-10-22) |
| cro | MPC | -0.02 | -0.7 | 459.28 | 2026-10-22 | 458.13 | 460.43 | -0.3 | -0 |  |  |  | continuous hysteresis sign active |
| cro | PSX | -0.015 | -0.8 | 284.63 | 2026-10-22 | 283.92 | 285.34 | -0.4 | -0 |  |  |  | continuous hysteresis sign active |
| cro | VLO | -0.015 | -0.5 | 426.28 | 2026-10-22 | 425.21 | 427.35 | -0.4 | -0 |  |  |  | continuous hysteresis sign active |
| refiner | DK | 0.05 | 9.9 | 75.79 | 2026-10-22 | 75.6 | 75.98 | 0.1 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | PBF | 0.03 | 5.7 | 79.25 | 2026-10-22 | 79.05 | 79.45 | 0.1 | 1.7 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | DINO | 0.02 | 2.5 | 122.32 | 2026-10-22 | 122.01 | 122.63 | 0.1 | 1 |  |  |  | 5d rolling-mean band_hysteresis active |
| services | FTI | -0.02 | -4.5 | 66.82 | 2026-10-22 | 66.65 | 66.99 | 0.7 | 0.9 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -6.1 | 49.55 | 2026-10-22 | 49.43 | 49.67 | 1.1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4.5 | 33.19 | 2026-10-22 | 33.11 | 33.27 | 0.6 | 1.1 |  |  |  | continuous hysteresis sign active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.056816 | 1.11556 | 763.96 | 2026-10-22 | 762.05 | 765.87 |
| XLE | 0.0242305 | 5.37898 | 67.57 | 2026-10-22 | 67.4011 | 67.7389 |
| XME | -0.061392 | -9.53391 | 96.59 | 2026-10-22 | 96.3485 | 96.8315 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | cro | PSX | SELL | -4 | -3 | -0.056926 | True |  | 284.63 | 2026-10-22 | 283.918 | 285.342 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | chemical | WLK | BUY | 5 | 5 | 0.02138 | False |  | 64.14 | 2026-10-22 | 63.9796 | 64.3003 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | chemical | DOW | BUY | 11 | 11 | 0.0233273 | False |  | 31.81 | 2026-10-22 | 31.7305 | 31.8895 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | cro | MPC | SELL | -1 | -1 | -0.0306187 | False |  | 459.28 | 2026-10-22 | 458.132 | 460.428 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | chemical | LYB | BUY | 4 | 4 | 0.017432 | False |  | 65.37 | 2026-10-22 | 65.2066 | 65.5334 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | chemical | EMN | BUY | 4 | 4 | 0.017416 | False |  | 65.31 | 2026-10-22 | 65.1467 | 65.4733 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | chemical | HUN | BUY | 28 | 28 | 0.0162773 | False |  | 8.72 | 2026-10-22 | 8.6982 | 8.7418 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | cro | VLO | SELL | -1 | -1 | -0.0284187 | False |  | 426.28 | 2026-10-22 | 425.214 | 427.346 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | chemical | CE | BUY | 5 | 5 | 0.01574 | False |  | 47.22 | 2026-10-22 | 47.102 | 47.3381 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | chemical | AVNT | BUY | 2 | 2 | 0.00541067 | False |  | 40.58 | 2026-10-22 | 40.4786 | 40.6815 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | bwt | ERO | BUY | 2 | 2 | 0.00401733 | False |  | 30.13 | 2026-10-22 | 30.0547 | 30.2053 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | bwt | TECK | BUY | 1 | 1 | 0.00392667 | False |  | 58.9 | 2026-10-22 | 58.7528 | 59.0473 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | SPY | SELL | -2 | -2 | -0.101861 | False |  | 763.96 | 2026-10-22 | 762.05 | 765.87 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XLE | SELL | -3 | -4 | -0.0180187 | False |  | 67.57 | 2026-10-22 | 67.4011 | 67.7389 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XME | SELL | -2 | -1 | -0.00643933 | False |  | 96.59 | 2026-10-22 | 96.3485 | 96.8315 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |


## Strategy changes and allocation notes

- Chemical decision rationale (recorded 2026-10-23): operator questioned the economic clarity of asymmetric exits plus renewing hold-21 and potential historical overfitting, not only recent losses. Rules are deterministic and unchanged; overfitting is a concern, not an established finding. Review parameter robustness, simpler exits, hedge/cost attribution and a 28% counterfactual before any restoration. See docs/cl_risk_reduction_2026-10-23.md.

- CL operator risk reduction effective target session 2026-10-23: chemical allocation reduced from 28% to 14%; psx_ref allocation reduced from 5% to 0% (suspended). Released 19 percentage points remain cash; no renormalization.
- Other sleeves, CL AUM $15,000 and legacy daily beta remain unchanged. CRO retains its own PSX leg and SPY-only hedge: clearing psx_ref does NOT mean flattening all account PSX. Recompute net stocks and component hedges.
- Chemical is halved BEFORE the existing 5% net single-name cap; previously capped names need not fall by exactly half. Allocation migration turnover is not a signal change.
- CRO (crack refiner-only) added effective 2026-10-06: 10% allocation from unused CL capacity. CL AUM remains $15,000; existing sleeve weights are NOT reduced or renormalized.
- CRO stocks: VLO/MPC/PSX = 30/40/30%; crack_03; signal lookback 30 sessions; volatility lookback 30 (minimum 20); no signal smoothing; balance=0.5 (maximum CRO stock gross 5% of CL AUM).
- CRO explicit hedge is SPY ONLY, not XLE. Preserve component hedge ownership when PSX overlaps existing sleeves; net single-name cap and execution constraints still apply.
- This addition is refiner-only CRO, NOT the refiner-producer CRP, refiner-VLCC CRV, or refiner-chemical CRC research strategies.
- CRO stock target state for this package: active. Flat CRO must not create reallocation trades under identical inputs.
- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.
- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.
- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.
## Beta method for 2026-10-23 — as-of 2026-10-22

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-10-23-syg5sij3/cached/targets-cl/2026-10-23. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
