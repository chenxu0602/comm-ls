# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-11-09

- Signal as-of date: 2026-11-06
- Target trading date: 2026-11-09
- AUM: $15,000.00
- Gross stock weight: 56.00%
- Single-name stock weight cap: 5.00%
- Net stock weight: -18.00%
- Gross hedge weight: 17.34%
- Total net weight after hedges: -4.66%
- Estimated turnover from current positions: 34.28%
- Full eligible order turnover: 32.41%
- Today's total child-order turnover: 33.38%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $12.52
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.19 | 0.19 | 2850 | 2850 | 10 |
| stock_short_without_hedge | 0.37 | -0.37 | 5550 | -5550 | 10 |
| total_hedge | 0.173365 | 0.133371 | 2600.48 | 2000.57 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.015 | 7.79626 | 28.86 | 2026-11-06 | 28.79 | 28.93 | 0.5 | 1.1 |  |  | 2026-11-12 | fixed_hold active from 2026-09-28 to before 2026-11-12 (initial signal 2026-09-25, last same-direction signal 2026-11-06) |
| bwt | TECK | 0.005 | 1.24049 | 60.46 | 2026-11-06 | 60.31 | 60.61 | 0.9 | 0.7 |  |  | 2026-11-12 | fixed_hold active from 2026-09-28 to before 2026-11-12 (initial signal 2026-09-25, last same-direction signal 2026-11-06) |
| chemical | CE | -0.045 | -14.5193 | 46.49 | 2026-11-06 | 46.37 | 46.61 | 0.7 | 0.9 |  |  | 2026-11-11 | fixed_hold active from 2026-11-06 to before 2026-11-11 (initial signal 2026-11-05, last same-direction signal 2026-11-06) |
| chemical | DOW | -0.045 | -21.4968 | 31.4 | 2026-11-06 | 31.32 | 31.48 | -0 | 1 |  |  | 2026-11-11 | fixed_hold active from 2026-11-06 to before 2026-11-11 (initial signal 2026-11-05, last same-direction signal 2026-11-06) |
| chemical | LYB | -0.045 | -11.1166 | 60.72 | 2026-11-06 | 60.57 | 60.87 | -0.3 | 1.1 |  |  | 2026-11-11 | fixed_hold active from 2026-11-06 to before 2026-11-11 (initial signal 2026-11-05, last same-direction signal 2026-11-06) |
| chemical | WLK | -0.015 | -3.54387 | 63.49 | 2026-11-06 | 63.33 | 63.65 | 0.5 | 0.6 |  |  | 2026-11-11 | fixed_hold active from 2026-11-06 to before 2026-11-11 (initial signal 2026-11-05, last same-direction signal 2026-11-06) |
| cro | PSX | -0.02 | -1.2209 | 245.72 | 2026-11-06 | 245.11 | 246.33 | -0.3 | -0 |  |  |  | continuous hysteresis sign active |
| re_c03\|cro | MPC | -0.05 | -2.01213 | 372.74 | 2026-11-06 | 371.81 | 373.67 | -0 | 0.7 |  |  |  | continuous hysteresis sign active |
| re_c03\|cro | VLO | -0.05 | -2.16481 | 346.45 | 2026-11-06 | 345.58 | 347.32 | -0.1 | 0.7 |  |  |  | continuous hysteresis sign active |
| refiner\|refiner_slow | DK | 0.041 | 9.61689 | 63.95 | 2026-11-06 | 63.79 | 64.11 | 0.1 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| refiner\|refiner_slow\|cro | PBF | 0.013 | 2.89877 | 67.27 | 2026-11-06 | 67.1 | 67.44 | 1 | 4.2 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| refiner\|refiner_slow\|re_c03 | DINO | 0.016 | 2.46964 | 97.18 | 2026-11-06 | 96.94 | 97.42 | 0.2 | 1.1 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| services | FTI | -0.04 | -9.44584 | 63.52 | 2026-11-06 | 63.36 | 63.68 | 0.7 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.04 | -12.0192 | 49.92 | 2026-11-06 | 49.8 | 50.04 | 1 | 0.9 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.02 | -9.42211 | 31.84 | 2026-11-06 | 31.76 | 31.92 | 0.5 | 1.1 |  |  |  | continuous hysteresis sign active |
| shipping | DHT | 0.03 | 21.7602 | 20.68 | 2026-11-06 | 20.63 | 20.73 | 0.4 | 0.3 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | FRO | 0.03 | 9.90753 | 45.42 | 2026-11-06 | 45.31 | 45.53 | 0.7 | 0.4 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | INSW | 0.02 | 3.0606 | 98.02 | 2026-11-06 | 97.77 | 98.27 | 0.4 | 0.3 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | TNK | 0.015 | 2.62513 | 85.71 | 2026-11-06 | 85.5 | 85.92 | 0.4 | 0.4 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | STNG | 0.005 | 0.928678 | 80.76 | 2026-11-06 | 80.56 | 80.96 | 0.4 | 0.4 |  |  |  | 2d rolling-mean shipping_sticky_accel active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.0110902 | 0.226241 | 735.29 | 2026-11-06 | 733.452 | 737.128 |
| XLE | 0.142278 | 34.6344 | 61.62 | 2026-11-06 | 61.4659 | 61.774 |
| XME | -0.019997 | -3.20979 | 93.45 | 2026-11-06 | 93.2164 | 93.6836 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | chemical | CE | SELL | -15 | -15 | -0.04649 | False |  | 46.49 | 2026-11-06 | 46.3738 | 46.6062 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | chemical | DOW | SELL | -21 | -21 | -0.04396 | False |  | 31.4 | 2026-11-06 | 31.3215 | 31.4785 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | services | HAL | BUY | 9 | 9 | 0.019104 | False |  | 31.84 | 2026-11-06 | 31.7604 | 31.9196 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | DHT | SELL | -12 | -12 | -0.016544 | False |  | 20.68 | 2026-11-06 | 20.6283 | 20.7317 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | chemical | WLK | SELL | -4 | -4 | -0.0169307 | False |  | 63.49 | 2026-11-06 | 63.3313 | 63.6487 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | services | FTI | BUY | 3 | 3 | 0.012704 | False |  | 63.52 | 2026-11-06 | 63.3612 | 63.6788 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | services | SLB | BUY | 3 | 3 | 0.009984 | False |  | 49.92 | 2026-11-06 | 49.7952 | 50.0448 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | chemical | LYB | BUY | 1 | 1 | 0.004048 | False |  | 60.72 | 2026-11-06 | 60.5682 | 60.8718 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XLE | BUY | 30 | 28 | 0.115024 | False |  | 61.62 | 2026-11-06 | 61.4659 | 61.774 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
| hedge | hedge | SPY | SELL | -1 | -1 | -0.0490193 | False |  | 735.29 | 2026-11-06 | 733.452 | 737.128 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |


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
## Beta method for 2026-11-09 — as-of 2026-11-06

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-11-09-t7cxj9rr/cached/targets-cl/2026-11-09. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
