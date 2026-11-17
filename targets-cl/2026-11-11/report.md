# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-11-11

- Signal as-of date: 2026-11-10
- Target trading date: 2026-11-11
- AUM: $15,000.00
- Gross stock weight: 56.00%
- Single-name stock weight cap: 5.00%
- Net stock weight: -18.00%
- Gross hedge weight: 17.53%
- Total net weight after hedges: -4.48%
- Estimated turnover from current positions: 4.39%
- Full eligible order turnover: 0.56%
- Today's total child-order turnover: 0.41%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $0.16
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.19 | 0.19 | 2850 | 2850 | 10 |
| stock_short_without_hedge | 0.37 | -0.37 | 5550 | -5550 | 10 |
| total_hedge | 0.175275 | 0.135227 | 2629.13 | 2028.4 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.015 | 7.33616 | 30.67 | 2026-11-10 | 30.59 | 30.75 | 0.6 | 1.1 |  |  | 2026-11-16 | fixed_hold active from 2026-09-28 to before 2026-11-16 (initial signal 2026-09-25, last same-direction signal 2026-11-10) |
| bwt | TECK | 0.005 | 1.19332 | 62.85 | 2026-11-10 | 62.69 | 63.01 | 0.9 | 0.7 |  |  | 2026-11-16 | fixed_hold active from 2026-09-28 to before 2026-11-16 (initial signal 2026-09-25, last same-direction signal 2026-11-10) |
| chemical | CE | -0.045 | -13.7952 | 48.93 | 2026-11-10 | 48.81 | 49.05 | 0.7 | 0.8 |  |  | 2026-11-13 | fixed_hold active from 2026-11-06 to before 2026-11-13 (initial signal 2026-11-05, last same-direction signal 2026-11-10) |
| chemical | DOW | -0.045 | -21.4422 | 31.48 | 2026-11-10 | 31.4 | 31.56 | -0.1 | 1 |  |  | 2026-11-13 | fixed_hold active from 2026-11-06 to before 2026-11-13 (initial signal 2026-11-05, last same-direction signal 2026-11-10) |
| chemical | LYB | -0.045 | -11.1386 | 60.6 | 2026-11-10 | 60.45 | 60.75 | -0.3 | 1.1 |  |  | 2026-11-13 | fixed_hold active from 2026-11-06 to before 2026-11-13 (initial signal 2026-11-05, last same-direction signal 2026-11-10) |
| chemical | WLK | -0.015 | -3.56238 | 63.16 | 2026-11-10 | 63 | 63.32 | 0.5 | 0.6 |  |  | 2026-11-13 | fixed_hold active from 2026-11-06 to before 2026-11-13 (initial signal 2026-11-05, last same-direction signal 2026-11-10) |
| cro | PSX | -0.02 | -1.19665 | 250.7 | 2026-11-10 | 250.07 | 251.33 | -0.2 | -0 |  |  |  | continuous hysteresis sign active |
| re_c03\|cro | MPC | -0.05 | -1.9253 | 389.55 | 2026-11-10 | 388.58 | 390.52 | 0.1 | 0.7 |  |  |  | continuous hysteresis sign active |
| re_c03\|cro | VLO | -0.05 | -2.13852 | 350.71 | 2026-11-10 | 349.83 | 351.59 | -0 | 0.7 |  |  |  | continuous hysteresis sign active |
| refiner\|refiner_slow | DK | 0.041 | 9.81801 | 62.64 | 2026-11-10 | 62.48 | 62.8 | 0.2 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| refiner\|refiner_slow\|cro | PBF | 0.013 | 2.95858 | 65.91 | 2026-11-10 | 65.75 | 66.07 | 1 | 4.2 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| refiner\|refiner_slow\|re_c03 | DINO | 0.016 | 2.43013 | 98.76 | 2026-11-10 | 98.51 | 99.01 | 0.2 | 1.1 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| services | FTI | -0.04 | -9.29512 | 64.55 | 2026-11-10 | 64.39 | 64.71 | 0.7 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.04 | -12.024 | 49.9 | 2026-11-10 | 49.78 | 50.02 | 1 | 0.9 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.02 | -9.4162 | 31.86 | 2026-11-10 | 31.78 | 31.94 | 0.5 | 1.1 |  |  |  | continuous hysteresis sign active |
| shipping | DHT | 0.03 | 21.6242 | 20.81 | 2026-11-10 | 20.76 | 20.86 | 0.4 | 0.3 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | FRO | 0.03 | 10.2576 | 43.87 | 2026-11-10 | 43.76 | 43.98 | 0.6 | 0.4 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | INSW | 0.02 | 3.05344 | 98.25 | 2026-11-10 | 98 | 98.5 | 0.4 | 0.3 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | TNK | 0.015 | 2.62544 | 85.7 | 2026-11-10 | 85.49 | 85.91 | 0.4 | 0.4 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | STNG | 0.005 | 0.931099 | 80.55 | 2026-11-10 | 80.35 | 80.75 | 0.4 | 0.4 |  |  |  | 2d rolling-mean shipping_sticky_accel active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.0127966 | 0.255959 | 749.92 | 2026-11-10 | 748.045 | 751.795 |
| XLE | 0.142454 | 34.3484 | 62.21 | 2026-11-10 | 62.0545 | 62.3655 |
| XME | -0.0200244 | -3.10937 | 96.6 | 2026-11-10 | 96.3585 | 96.8415 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | hedge | XLE | BUY | 1 | 1 | 0.00414733 | False |  | 62.21 | 2026-11-10 | 62.0545 | 62.3655 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |


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
## Beta method for 2026-11-11 — as-of 2026-11-10

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-11-11-qblrlzla/cached/targets-cl/2026-11-11. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
