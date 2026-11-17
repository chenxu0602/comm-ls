# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-10-26

- Signal as-of date: 2026-10-23
- Target trading date: 2026-10-26
- AUM: $15,000.00
- Gross stock weight: 38.00%
- Single-name stock weight cap: 5.00%
- Net stock weight: -0.00%
- Gross hedge weight: 13.84%
- Total net weight after hedges: -0.27%
- Estimated turnover from current positions: 16.12%
- Full eligible order turnover: 13.26%
- Today's total child-order turnover: 11.90%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $4.46
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.19 | 0.19 | 2850 | 2850 | 6 |
| stock_short_without_hedge | 0.19 | -0.19 | 2850 | -2850 | 10 |
| total_hedge | 0.138372 | -0.002728 | 2075.58 | -40.92 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.045 | 22.5 | 29.95 | 2026-10-23 | 29.88 | 30.02 | 0.3 | 1.1 |  |  | 2026-10-29 | fixed_hold active from 2026-09-28 to before 2026-10-29 (initial signal 2026-09-25, last same-direction signal 2026-10-23) |
| bwt | TECK | 0.015 | 3.8 | 59.05 | 2026-10-23 | 58.9 | 59.2 | 0.8 | 0.7 |  |  | 2026-10-29 | fixed_hold active from 2026-09-28 to before 2026-10-29 (initial signal 2026-09-25, last same-direction signal 2026-10-23) |
| chemical | LYB | -0.035 | -7.9 | 66.45 | 2026-10-23 | 66.28 | 66.62 | -0.1 | 1.1 |  |  | 2026-11-24 | fixed_hold active from 2026-04-20 to before 2026-11-24 (initial signal 2026-04-17, last same-direction signal 2026-10-23) |
| chemical | DOW | -0.028 | -12.9 | 32.61 | 2026-10-23 | 32.53 | 32.69 | 0.1 | 1.1 |  |  | 2026-11-24 | fixed_hold active from 2026-04-20 to before 2026-11-24 (initial signal 2026-04-17, last same-direction signal 2026-10-23) |
| chemical | WLK | -0.028 | -6.5 | 64.56 | 2026-10-23 | 64.4 | 64.72 | 0.7 | 0.7 |  |  | 2026-11-24 | fixed_hold active from 2026-04-20 to before 2026-11-24 (initial signal 2026-04-17, last same-direction signal 2026-10-23) |
| chemical | CE | -0.014 | -4.4 | 47.71 | 2026-10-23 | 47.59 | 47.83 | 0.8 | 1 |  |  | 2026-11-24 | fixed_hold active from 2026-04-20 to before 2026-11-24 (initial signal 2026-04-17, last same-direction signal 2026-10-23) |
| chemical | EMN | -0.014 | -3.2 | 64.93 | 2026-10-23 | 64.77 | 65.09 | 0.9 | 0.2 |  |  | 2026-11-24 | fixed_hold active from 2026-04-20 to before 2026-11-24 (initial signal 2026-04-17, last same-direction signal 2026-10-23) |
| chemical | HUN | -0.014 | -23.9 | 8.8 | 2026-10-23 | 8.78 | 8.82 | 1.3 | 0.7 |  |  | 2026-11-24 | fixed_hold active from 2026-04-20 to before 2026-11-24 (initial signal 2026-04-17, last same-direction signal 2026-10-23) |
| chemical | AVNT | -0.007 | -2.6 | 41.03 | 2026-10-23 | 40.93 | 41.13 | 1.1 | -0 |  |  | 2026-11-24 | fixed_hold active from 2026-04-20 to before 2026-11-24 (initial signal 2026-04-17, last same-direction signal 2026-10-23) |
| refiner_slow | PSX | 0.02 | 1.1 | 283.18 | 2026-10-23 | 282.47 | 283.89 | 0.1 | 1.1 |  |  |  | continuous hysteresis sign active |
| refiner\|refiner_slow | DK | 0.045 | 9.1 | 74.41 | 2026-10-23 | 74.22 | 74.6 | 0.2 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| refiner\|refiner_slow | PBF | 0.039 | 7.7 | 76.17 | 2026-10-23 | 75.98 | 76.36 | 0.1 | 1.7 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| refiner\|refiner_slow | DINO | 0.026 | 3.2 | 121.66 | 2026-10-23 | 121.36 | 121.96 | 0.2 | 1 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| services | FTI | -0.02 | -4.3 | 69.89 | 2026-10-23 | 69.72 | 70.06 | 0.7 | 0.9 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -5.7 | 53.06 | 2026-10-23 | 52.93 | 53.19 | 1.1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4.3 | 34.92 | 2026-10-23 | 34.83 | 35.01 | 0.6 | 1.2 |  |  |  | continuous hysteresis sign active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.0678219 | 1.33864 | 759.97 | 2026-10-23 | 758.07 | 761.87 |
| XLE | -0.00885994 | -1.91691 | 69.33 | 2026-10-23 | 69.1567 | 69.5033 |
| XME | -0.0616901 | -9.60207 | 96.37 | 2026-10-23 | 96.1291 | 96.6109 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | cro | MPC | BUY | 1 | 1 | 0.0304813 | False |  | 457.22 | 2026-10-23 | 456.077 | 458.363 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | cro | VLO | BUY | 1 | 1 | 0.027952 | False |  | 419.28 | 2026-10-23 | 418.232 | 420.328 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner_slow | PSX | BUY | 1 | 1 | 0.0188787 | False |  | 283.18 | 2026-10-23 | 282.472 | 283.888 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner\|refiner_slow | DINO | BUY | 1 | 1 | 0.00811067 | False |  | 121.66 | 2026-10-23 | 121.356 | 121.964 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner\|refiner_slow | PBF | BUY | 2 | 2 | 0.010156 | False |  | 76.17 | 2026-10-23 | 75.9796 | 76.3604 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner\|refiner_slow | DK | SELL | -1 | -1 | -0.00496067 | False |  | 74.41 | 2026-10-23 | 74.224 | 74.596 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XLE | SELL | -6 | -4 | -0.018488 | True |  | 69.33 | 2026-10-23 | 69.1567 | 69.5033 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |


## Strategy changes and allocation notes

- CL operator risk reduction effective target session 2026-10-23: chemical allocation reduced from 28% to 14%; psx_ref allocation reduced from 5% to 0% (suspended). At that decision, released 19 percentage points remained cash; no renormalization. Later dated decisions below supersede allocation details.
- At that decision other sleeves were unchanged. CL AUM $15,000 and legacy daily beta remain unchanged. CRO retains its own PSX leg and SPY-only hedge: clearing psx_ref does NOT mean flattening all account PSX. Recompute net stocks and component hedges.
- Chemical is halved BEFORE the existing 5% net single-name cap; previously capped names need not fall by exactly half. Allocation migration turnover is not a signal change.
- Chemical decision rationale: operator questioned the economic clarity of asymmetric exits plus renewing hold-21 and potential historical overfitting, not only recent losses. Rules are deterministic and unchanged; overfitting is a concern, not an established finding. Review parameter robustness, simpler exits, hedge/cost attribution and a 28% counterfactual before any restoration. See docs/cl_risk_reduction_2026-10-23.md.
- APPROVED refiner blend effective target session 2026-10-26: refiner_slow 10% + refiner 5%; psx_ref remains suspended at 0%. This raises live combined refiner allocation from 10% to 15%, using 5 percentage points of idle capacity, not a change in CL AUM or automatic renormalization.
- refiner_slow basket DK/DINO/PBF/PSX = 30/20/30/20%; existing refiner DK/DINO/PBF = 50/20/30%. Both hedge with SPY + XLE using retained legacy DAILY beta. CRO remains separate and SPY-only; preserve component ownership before account netting.
- Slow rule: HO front_third_annualized_carry change over 50 stock observations; carry-level std 60/min30; entry 1.25 std, exit 0.95 std; CL m1 10-session return gate versus 0.5 times daily 20/min10 std. No fixed 10-day hold, no rolling-5 smoothing. Current input lookbacks and arrivals fail closed.
- Chemical remains TEMPORARILY 14% in production as an operator stop-loss-like risk-budget override; notebook/research remains 28%. Restoration requires a new operator decision after a clear risk reduction; no numeric trigger, date or automatic restoration is authorized. Do not return it to 28% as part of this refiner change.
- Full aligned refiner stock gross can reach 14.5% after the DK 5% net-name cap, before separate CRO. Size reduction or new sleeve orders caused by this change are allocation migration, not a new commodity signal. See docs/cl_refiner_blend_production_2026-10-26.md.
- CRO (crack refiner-only) added effective 2026-10-06: 10% allocation from unused CL capacity. CL AUM remains $15,000; existing sleeve weights are NOT reduced or renormalized.
- CRO stocks: VLO/MPC/PSX = 30/40/30%; crack_03; signal lookback 30 sessions; volatility lookback 30 (minimum 20); no signal smoothing; balance=0.5 (maximum CRO stock gross 5% of CL AUM).
- CRO explicit hedge is SPY ONLY, not XLE. Preserve component hedge ownership when PSX overlaps existing sleeves; net single-name cap and execution constraints still apply.
- This addition is refiner-only CRO, NOT the refiner-producer CRP, refiner-VLCC CRV, or refiner-chemical CRC research strategies.
- CRO stock target state for this package: flat. Flat CRO must not create reallocation trades under identical inputs.
- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.
- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.
- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.
## Beta method for 2026-10-26 — as-of 2026-10-23

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-10-26-z0ozui6k/cached/targets-cl/2026-10-26. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
