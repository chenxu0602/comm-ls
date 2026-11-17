# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-11-10

- Signal as-of date: 2026-11-09
- Target trading date: 2026-11-10
- AUM: $15,000.00
- Gross stock weight: 56.00%
- Single-name stock weight cap: 5.00%
- Net stock weight: -18.00%
- Gross hedge weight: 17.60%
- Total net weight after hedges: -4.37%
- Estimated turnover from current positions: 18.33%
- Full eligible order turnover: 14.28%
- Today's total child-order turnover: 13.53%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $5.07
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.19 | 0.19 | 2850 | 2850 | 10 |
| stock_short_without_hedge | 0.37 | -0.37 | 5550 | -5550 | 10 |
| total_hedge | 0.175987 | 0.136325 | 2639.8 | 2044.88 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.015 | 7.18391 | 31.32 | 2026-11-09 | 31.24 | 31.4 | 0.6 | 1.1 |  |  | 2026-11-13 | fixed_hold active from 2026-09-28 to before 2026-11-13 (initial signal 2026-09-25, last same-direction signal 2026-11-09) |
| bwt | TECK | 0.005 | 1.15973 | 64.67 | 2026-11-09 | 64.51 | 64.83 | 0.9 | 0.7 |  |  | 2026-11-13 | fixed_hold active from 2026-09-28 to before 2026-11-13 (initial signal 2026-09-25, last same-direction signal 2026-11-09) |
| chemical | CE | -0.045 | -13.8462 | 48.75 | 2026-11-09 | 48.63 | 48.87 | 0.7 | 0.9 |  |  | 2026-11-12 | fixed_hold active from 2026-11-06 to before 2026-11-12 (initial signal 2026-11-05, last same-direction signal 2026-11-09) |
| chemical | DOW | -0.045 | -21.8023 | 30.96 | 2026-11-09 | 30.88 | 31.04 | -0.1 | 1 |  |  | 2026-11-12 | fixed_hold active from 2026-11-06 to before 2026-11-12 (initial signal 2026-11-05, last same-direction signal 2026-11-09) |
| chemical | LYB | -0.045 | -11.3445 | 59.5 | 2026-11-09 | 59.35 | 59.65 | -0.3 | 1.1 |  |  | 2026-11-12 | fixed_hold active from 2026-11-06 to before 2026-11-12 (initial signal 2026-11-05, last same-direction signal 2026-11-09) |
| chemical | WLK | -0.015 | -3.5085 | 64.13 | 2026-11-09 | 63.97 | 64.29 | 0.5 | 0.6 |  |  | 2026-11-12 | fixed_hold active from 2026-11-06 to before 2026-11-12 (initial signal 2026-11-05, last same-direction signal 2026-11-09) |
| cro | PSX | -0.02 | -1.18568 | 253.02 | 2026-11-09 | 252.39 | 253.65 | -0.2 | -0 |  |  |  | continuous hysteresis sign active |
| re_c03\|cro | MPC | -0.05 | -1.92367 | 389.88 | 2026-11-09 | 388.91 | 390.85 | 0.1 | 0.7 |  |  |  | continuous hysteresis sign active |
| re_c03\|cro | VLO | -0.05 | -2.10231 | 356.75 | 2026-11-09 | 355.86 | 357.64 | -0 | 0.7 |  |  |  | continuous hysteresis sign active |
| refiner\|refiner_slow | DK | 0.041 | 9.46154 | 65 | 2026-11-09 | 64.84 | 65.16 | 0.2 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| refiner\|refiner_slow\|cro | PBF | 0.013 | 2.80374 | 69.55 | 2026-11-09 | 69.38 | 69.72 | 1 | 4.2 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| refiner\|refiner_slow\|re_c03 | DINO | 0.016 | 2.40577 | 99.76 | 2026-11-09 | 99.51 | 100.01 | 0.2 | 1.1 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| services | FTI | -0.04 | -9.37793 | 63.98 | 2026-11-09 | 63.82 | 64.14 | 0.7 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.04 | -11.9095 | 50.38 | 2026-11-09 | 50.25 | 50.51 | 1 | 0.9 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.02 | -9.41029 | 31.88 | 2026-11-09 | 31.8 | 31.96 | 0.5 | 1.1 |  |  |  | continuous hysteresis sign active |
| shipping | DHT | 0.03 | 21.8872 | 20.56 | 2026-11-09 | 20.51 | 20.61 | 0.4 | 0.3 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | FRO | 0.03 | 10.1603 | 44.29 | 2026-11-09 | 44.18 | 44.4 | 0.6 | 0.4 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | INSW | 0.02 | 3.11042 | 96.45 | 2026-11-09 | 96.21 | 96.69 | 0.4 | 0.3 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | TNK | 0.015 | 2.64333 | 85.12 | 2026-11-09 | 84.91 | 85.33 | 0.4 | 0.4 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | STNG | 0.005 | 0.941974 | 79.62 | 2026-11-09 | 79.42 | 79.82 | 0.4 | 0.4 |  |  |  | 2d rolling-mean shipping_sticky_accel active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.0130708 | 0.260482 | 752.69 | 2026-11-09 | 750.808 | 754.572 |
| XLE | 0.143085 | 34.6509 | 61.94 | 2026-11-09 | 61.7851 | 62.0948 |
| XME | -0.0198306 | -3.01743 | 98.58 | 2026-11-09 | 98.3336 | 98.8265 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | shipping | DHT | SELL | -12 | -12 | -0.016448 | False |  | 20.56 | 2026-11-09 | 20.5086 | 20.6114 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | chemical | CE | BUY | 1 | 1 | 0.00325 | False |  | 48.75 | 2026-11-09 | 48.6281 | 48.8719 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XLE | BUY | 30 | 28 | 0.115621 | False |  | 61.94 | 2026-11-09 | 61.7851 | 62.0948 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |


## Strategy changes and allocation notes

- CL operator risk reduction effective target session 2026-10-23: chemical allocation reduced from 28% to 14%; psx_ref allocation reduced from 5% to 0% (suspended). At that decision, released 19 percentage points remained cash; no renormalization. Later dated decisions below supersede allocation details.
- At that decision other sleeves were unchanged. CL AUM $15,000 and legacy daily beta remain unchanged. CRO retains its own PSX leg and SPY-only hedge: clearing psx_ref does NOT mean flattening all account PSX. Recompute net stocks and component hedges.
- Chemical is halved BEFORE the existing 5% net single-name cap; previously capped names need not fall by exactly half. Allocation migration turnover is not a signal change.
- Chemical decision rationale: operator questioned the economic clarity of asymmetric exits plus renewing hold-21 and potential historical overfitting, not only recent losses. Rules are deterministic and unchanged; overfitting is a concern, not an established finding. Review parameter robustness, simpler exits, hedge/cost attribution and a 28% counterfactual before any restoration. See docs/cl_risk_reduction_2026-10-23.md.
- CURRENT FINAL CL from 2026-11-09: operator chemical20->15%, services20->10%, shipping STAYS10% (initial20% package superseded before execution); refiner3/slow8/bwt2/CRO20/re_c03 10% unchanged. Nominal budget78%, no normalization. AUM and legacy DAILY beta unchanged.
- Rules unchanged: chemical hold2 and L/PP exits; slow HO m1 gate carry_data_2; CRO half-balance SPY-only, re_c03 SPY+XLE. Track allocation migration separately from signal changes. See docs/cl_reweight_2026-11-09.md.
- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.
- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.
- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.
## Beta method for 2026-11-10 — as-of 2026-11-09

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-11-10-y3z13i_u/cached/targets-cl/2026-11-10. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
