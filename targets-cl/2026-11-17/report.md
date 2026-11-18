# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-11-17

- Signal as-of date: 2026-11-16
- Target trading date: 2026-11-17
- AUM: $15,000.00
- Gross stock weight: 46.00%
- Single-name stock weight cap: 5.00%
- Net stock weight: -28.00%
- Gross hedge weight: 27.80%
- Total net weight after hedges: -4.26%
- Estimated turnover from current positions: 5.89%
- Full eligible order turnover: 3.76%
- Today's total child-order turnover: 5.94%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $2.23
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.09 | 0.09 | 1350 | 1350 | 5 |
| stock_short_without_hedge | 0.37 | -0.37 | 5550 | -5550 | 10 |
| total_hedge | 0.277956 | 0.237427 | 4169.35 | 3561.4 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.015 | 8.23271 | 27.33 | 2026-11-16 | 27.26 | 27.4 | 0.6 | 1.1 |  |  | 2026-11-20 | fixed_hold active from 2026-09-28 to before 2026-11-20 (initial signal 2026-09-25, last same-direction signal 2026-11-16) |
| bwt | TECK | 0.005 | 1.31211 | 57.16 | 2026-11-16 | 57.02 | 57.3 | 0.9 | 0.7 |  |  | 2026-11-20 | fixed_hold active from 2026-09-28 to before 2026-11-20 (initial signal 2026-09-25, last same-direction signal 2026-11-16) |
| chemical | CE | -0.045 | -13.7868 | 48.96 | 2026-11-16 | 48.84 | 49.08 | 0.8 | 0.9 |  |  | 2026-11-19 | fixed_hold active from 2026-11-06 to before 2026-11-19 (initial signal 2026-11-05, last same-direction signal 2026-11-16) |
| chemical | DOW | -0.045 | -21.1202 | 31.96 | 2026-11-16 | 31.88 | 32.04 | 0 | 1 |  |  | 2026-11-19 | fixed_hold active from 2026-11-06 to before 2026-11-19 (initial signal 2026-11-05, last same-direction signal 2026-11-16) |
| chemical | LYB | -0.045 | -10.9454 | 61.67 | 2026-11-16 | 61.52 | 61.82 | -0.2 | 1.1 |  |  | 2026-11-19 | fixed_hold active from 2026-11-06 to before 2026-11-19 (initial signal 2026-11-05, last same-direction signal 2026-11-16) |
| chemical | WLK | -0.015 | -3.65082 | 61.63 | 2026-11-16 | 61.48 | 61.78 | 0.5 | 0.6 |  |  | 2026-11-19 | fixed_hold active from 2026-11-06 to before 2026-11-19 (initial signal 2026-11-05, last same-direction signal 2026-11-16) |
| cro | PSX | -0.02 | -1.1511 | 260.62 | 2026-11-16 | 259.97 | 261.27 | -0.2 | -0 |  |  |  | continuous hysteresis sign active |
| re_c03\|cro | MPC | -0.05 | -1.86479 | 402.19 | 2026-11-16 | 401.18 | 403.2 | 0.1 | 0.7 |  |  |  | continuous hysteresis sign active |
| re_c03\|cro | VLO | -0.05 | -2.02851 | 369.73 | 2026-11-16 | 368.81 | 370.65 | -0 | 0.8 |  |  |  | continuous hysteresis sign active |
| refiner\|refiner_slow | DK | 0.041 | 9.06812 | 67.82 | 2026-11-16 | 67.65 | 67.99 | 0.1 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| refiner\|refiner_slow\|cro | PBF | 0.013 | 2.84132 | 68.63 | 2026-11-16 | 68.46 | 68.8 | 0.9 | 4.2 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| refiner\|refiner_slow\|re_c03 | DINO | 0.016 | 2.42302 | 99.05 | 2026-11-16 | 98.8 | 99.3 | 0.2 | 1.1 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| services | FTI | -0.04 | -9.40291 | 63.81 | 2026-11-16 | 63.65 | 63.97 | 0.7 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.04 | -11.9808 | 50.08 | 2026-11-16 | 49.95 | 50.21 | 1 | 0.9 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.02 | -9.23077 | 32.5 | 2026-11-16 | 32.42 | 32.58 | 0.5 | 1.1 |  |  |  | continuous hysteresis sign active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.0775261 | 1.57158 | 739.95 | 2026-11-16 | 738.1 | 741.8 |
| XLE | 0.180165 | 42.4318 | 63.69 | 2026-11-16 | 63.5308 | 63.8492 |
| XME | -0.0202648 | -3.38085 | 89.91 | 2026-11-16 | 89.6852 | 90.1348 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | shipping | INSW | SELL | -1 | -1 | -0.006808 | False |  | 102.12 | 2026-11-16 | 101.865 | 102.375 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | chemical | CE | SELL | -1 | -1 | -0.003264 | False |  | 48.96 | 2026-11-16 | 48.8376 | 49.0824 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | SPY | BUY | 1 | 1 | 0.04933 | False |  | 739.95 | 2026-11-16 | 738.1 | 741.8 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |


## Strategy changes and allocation notes

- Metals operator risk reduction from target2026-11-17: gap7.5/accel10/SCO-vol12.5/copper7.5/miners12.5%; all other sleeves0. Each Nov16 sleeve allocation halved before the unchanged12% name cap; nominal50%, released50% stays cash, no normalization or automatic restoration. AUM5000, signal rules, legacy DAILY SPY+XME hedges and execution controls unchanged. Recompute hedges from reduced stock targets and distinguish allocation migration from signal turnover. See docs/metals_risk_reduction_2026-11-17.md.
- CL operator risk reduction effective target session 2026-10-23: chemical allocation reduced from 28% to 14%; psx_ref allocation reduced from 5% to 0% (suspended). At that decision, released 19 percentage points remained cash; no renormalization. Later dated decisions below supersede allocation details.
- At that decision other sleeves were unchanged. CL AUM $15,000 and legacy daily beta remain unchanged. CRO retains its own PSX leg and SPY-only hedge: clearing psx_ref does NOT mean flattening all account PSX. Recompute net stocks and component hedges.
- Chemical is halved BEFORE the existing 5% net single-name cap; previously capped names need not fall by exactly half. Allocation migration turnover is not a signal change.
- Chemical decision rationale: operator questioned the economic clarity of asymmetric exits plus renewing hold-21 and potential historical overfitting, not only recent losses. Rules are deterministic and unchanged; overfitting is a concern, not an established finding. Review parameter robustness, simpler exits, hedge/cost attribution and a 28% counterfactual before any restoration. See docs/cl_risk_reduction_2026-10-23.md.
- CURRENT FINAL CL from 2026-11-09: operator chemical20->15%, services20->10%, shipping STAYS10% (initial20% package superseded before execution); refiner3/slow8/bwt2/CRO20/re_c03 10% unchanged. Nominal budget78%, no normalization. AUM and legacy DAILY beta unchanged.
- Rules unchanged: chemical hold2 and L/PP exits; slow HO m1 gate carry_data_2; CRO half-balance SPY-only, re_c03 SPY+XLE. Track allocation migration separately from signal changes. See docs/cl_reweight_2026-11-09.md.
- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.
- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.
- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.
## Beta method for 2026-11-17 — as-of 2026-11-16

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-11-17-p0gussny/cached/targets-cl/2026-11-17. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
