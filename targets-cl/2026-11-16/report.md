# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-11-16

- Signal as-of date: 2026-11-13
- Target trading date: 2026-11-16
- AUM: $15,000.00
- Gross stock weight: 46.00%
- Single-name stock weight cap: 5.00%
- Net stock weight: -28.00%
- Gross hedge weight: 26.04%
- Total net weight after hedges: -6.00%
- Estimated turnover from current positions: 8.72%
- Full eligible order turnover: 5.20%
- Today's total child-order turnover: 6.08%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $2.28
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.09 | 0.09 | 1350 | 1350 | 5 |
| stock_short_without_hedge | 0.37 | -0.37 | 5550 | -5550 | 10 |
| total_hedge | 0.260413 | 0.219993 | 3906.2 | 3299.89 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.015 | 7.7426 | 29.06 | 2026-11-13 | 28.99 | 29.13 | 0.6 | 1.1 |  |  | 2026-11-19 | fixed_hold active from 2026-09-28 to before 2026-11-19 (initial signal 2026-09-25, last same-direction signal 2026-11-13) |
| bwt | TECK | 0.005 | 1.24605 | 60.19 | 2026-11-13 | 60.04 | 60.34 | 0.9 | 0.7 |  |  | 2026-11-19 | fixed_hold active from 2026-09-28 to before 2026-11-19 (initial signal 2026-09-25, last same-direction signal 2026-11-13) |
| chemical | CE | -0.045 | -13.1297 | 51.41 | 2026-11-13 | 51.28 | 51.54 | 0.7 | 0.8 |  |  | 2026-11-18 | fixed_hold active from 2026-11-06 to before 2026-11-18 (initial signal 2026-11-05, last same-direction signal 2026-11-13) |
| chemical | DOW | -0.045 | -20.4298 | 33.04 | 2026-11-13 | 32.96 | 33.12 | -0 | 1 |  |  | 2026-11-18 | fixed_hold active from 2026-11-06 to before 2026-11-18 (initial signal 2026-11-05, last same-direction signal 2026-11-13) |
| chemical | LYB | -0.045 | -10.4765 | 64.43 | 2026-11-13 | 64.27 | 64.59 | -0.3 | 1.1 |  |  | 2026-11-18 | fixed_hold active from 2026-11-06 to before 2026-11-18 (initial signal 2026-11-05, last same-direction signal 2026-11-13) |
| chemical | WLK | -0.015 | -3.53718 | 63.61 | 2026-11-13 | 63.45 | 63.77 | 0.5 | 0.6 |  |  | 2026-11-18 | fixed_hold active from 2026-11-06 to before 2026-11-18 (initial signal 2026-11-05, last same-direction signal 2026-11-13) |
| cro | PSX | -0.02 | -1.1325 | 264.9 | 2026-11-13 | 264.24 | 265.56 | -0.2 | -0 |  |  |  | continuous hysteresis sign active |
| re_c03\|cro | MPC | -0.05 | -1.80875 | 414.65 | 2026-11-13 | 413.61 | 415.69 | 0.1 | 0.7 |  |  |  | continuous hysteresis sign active |
| re_c03\|cro | VLO | -0.05 | -1.97457 | 379.83 | 2026-11-13 | 378.88 | 380.78 | -0 | 0.7 |  |  |  | continuous hysteresis sign active |
| refiner\|refiner_slow | DK | 0.041 | 8.9781 | 68.5 | 2026-11-13 | 68.33 | 68.67 | 0.2 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| refiner\|refiner_slow\|cro | PBF | 0.013 | 2.73569 | 71.28 | 2026-11-13 | 71.1 | 71.46 | 1 | 4.2 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| refiner\|refiner_slow\|re_c03 | DINO | 0.016 | 2.3488 | 102.18 | 2026-11-13 | 101.92 | 102.44 | 0.2 | 1.1 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| services | FTI | -0.04 | -9.05524 | 66.26 | 2026-11-13 | 66.09 | 66.43 | 0.7 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.04 | -11.6122 | 51.67 | 2026-11-13 | 51.54 | 51.8 | 1 | 0.9 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.02 | -8.88099 | 33.78 | 2026-11-13 | 33.7 | 33.86 | 0.5 | 1.1 |  |  |  | continuous hysteresis sign active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.0627998 | 1.24872 | 754.37 | 2026-11-13 | 752.484 | 756.256 |
| XLE | 0.177403 | 40.9644 | 64.96 | 2026-11-13 | 64.7976 | 65.1224 |
| XME | -0.0202101 | -3.23396 | 93.74 | 2026-11-13 | 93.5056 | 93.9743 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | shipping | FRO | SELL | -5 | -5 | -0.0156567 | False |  | 46.97 | 2026-11-13 | 46.8526 | 47.0874 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | DHT | SELL | -10 | -10 | -0.0148333 | False |  | 22.25 | 2026-11-13 | 22.1944 | 22.3056 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | INSW | SELL | -1 | -1 | -0.00701533 | False |  | 105.23 | 2026-11-13 | 104.967 | 105.493 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | TNK | SELL | -1 | -1 | -0.005962 | False |  | 89.43 | 2026-11-13 | 89.2064 | 89.6536 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XLE | BUY | 2 | 4 | 0.0173227 | False |  | 64.96 | 2026-11-13 | 64.7976 | 65.1224 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |


## Strategy changes and allocation notes

- Metals reweight from target2026-11-16: hg_gc_gap15/accel20/SCO-vol25/copper15/miners25%; alloys0 and notebook-only hg_gc_gap_gc_carry_iron_2=0. Nominal100%, no normalization; copper10->15 uses the previously idle5pp. AUM5000, legacy DAILY SPY+XME hedges, signal rules,12% name cap and execution controls unchanged. See docs/metals_reweight_2026-11-16.md.
- CL operator risk reduction effective target session 2026-10-23: chemical allocation reduced from 28% to 14%; psx_ref allocation reduced from 5% to 0% (suspended). At that decision, released 19 percentage points remained cash; no renormalization. Later dated decisions below supersede allocation details.
- At that decision other sleeves were unchanged. CL AUM $15,000 and legacy daily beta remain unchanged. CRO retains its own PSX leg and SPY-only hedge: clearing psx_ref does NOT mean flattening all account PSX. Recompute net stocks and component hedges.
- Chemical is halved BEFORE the existing 5% net single-name cap; previously capped names need not fall by exactly half. Allocation migration turnover is not a signal change.
- Chemical decision rationale: operator questioned the economic clarity of asymmetric exits plus renewing hold-21 and potential historical overfitting, not only recent losses. Rules are deterministic and unchanged; overfitting is a concern, not an established finding. Review parameter robustness, simpler exits, hedge/cost attribution and a 28% counterfactual before any restoration. See docs/cl_risk_reduction_2026-10-23.md.
- CURRENT FINAL CL from 2026-11-09: operator chemical20->15%, services20->10%, shipping STAYS10% (initial20% package superseded before execution); refiner3/slow8/bwt2/CRO20/re_c03 10% unchanged. Nominal budget78%, no normalization. AUM and legacy DAILY beta unchanged.
- Rules unchanged: chemical hold2 and L/PP exits; slow HO m1 gate carry_data_2; CRO half-balance SPY-only, re_c03 SPY+XLE. Track allocation migration separately from signal changes. See docs/cl_reweight_2026-11-09.md.
- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.
- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.
- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.
## Beta method for 2026-11-16 — as-of 2026-11-13

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-11-16-unv2y3l0/cached/targets-cl/2026-11-16. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
