# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-11-12

- Signal as-of date: 2026-11-11
- Target trading date: 2026-11-12
- AUM: $15,000.00
- Gross stock weight: 48.00%
- Single-name stock weight cap: 5.00%
- Net stock weight: -2.00%
- Gross hedge weight: 8.89%
- Total net weight after hedges: 2.89%
- Estimated turnover from current positions: 29.87%
- Full eligible order turnover: 26.38%
- Today's total child-order turnover: 25.92%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $9.72
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.23 | 0.23 | 3450 | 3450 | 10 |
| stock_short_without_hedge | 0.25 | -0.25 | 3750 | -3750 | 7 |
| total_hedge | 0.088942 | 0.048864 | 1334.13 | 732.96 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.015 | 7.27684 | 30.92 | 2026-11-11 | 30.84 | 31 | 0.6 | 1.1 |  |  | 2026-11-17 | fixed_hold active from 2026-09-28 to before 2026-11-17 (initial signal 2026-09-25, last same-direction signal 2026-11-11) |
| bwt | TECK | 0.005 | 1.17795 | 63.67 | 2026-11-11 | 63.51 | 63.83 | 0.9 | 0.7 |  |  | 2026-11-17 | fixed_hold active from 2026-09-28 to before 2026-11-17 (initial signal 2026-09-25, last same-direction signal 2026-11-11) |
| chemical | CE | -0.045 | -13.1195 | 51.45 | 2026-11-11 | 51.32 | 51.58 | 0.7 | 0.9 |  |  | 2026-11-16 | fixed_hold active from 2026-11-06 to before 2026-11-16 (initial signal 2026-11-05, last same-direction signal 2026-11-11) |
| chemical | DOW | -0.045 | -20.7437 | 32.54 | 2026-11-11 | 32.46 | 32.62 | -0 | 1 |  |  | 2026-11-16 | fixed_hold active from 2026-11-06 to before 2026-11-16 (initial signal 2026-11-05, last same-direction signal 2026-11-11) |
| chemical | LYB | -0.045 | -10.7862 | 62.58 | 2026-11-11 | 62.42 | 62.74 | -0.3 | 1.1 |  |  | 2026-11-16 | fixed_hold active from 2026-11-06 to before 2026-11-16 (initial signal 2026-11-05, last same-direction signal 2026-11-11) |
| chemical | WLK | -0.015 | -3.52223 | 63.88 | 2026-11-11 | 63.72 | 64.04 | 0.5 | 0.6 |  |  | 2026-11-16 | fixed_hold active from 2026-11-06 to before 2026-11-16 (initial signal 2026-11-05, last same-direction signal 2026-11-11) |
| refiner\|refiner_slow | DK | 0.041 | 9.15724 | 67.16 | 2026-11-11 | 66.99 | 67.33 | 0.2 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| refiner\|refiner_slow | DINO | 0.036 | 5.30817 | 101.73 | 2026-11-11 | 101.48 | 101.98 | 0.2 | 1.1 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| refiner\|refiner_slow | PBF | 0.033 | 7.09881 | 69.73 | 2026-11-11 | 69.56 | 69.9 | 0.1 | 1.7 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| services | FTI | -0.04 | -9.17572 | 65.39 | 2026-11-11 | 65.23 | 65.55 | 0.7 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.04 | -11.7739 | 50.96 | 2026-11-11 | 50.83 | 51.09 | 1 | 0.9 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.02 | -9.11023 | 32.93 | 2026-11-11 | 32.85 | 33.01 | 0.5 | 1.1 |  |  |  | continuous hysteresis sign active |
| shipping | DHT | 0.03 | 20.8623 | 21.57 | 2026-11-11 | 21.52 | 21.62 | 0.4 | 0.3 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | FRO | 0.03 | 9.88142 | 45.54 | 2026-11-11 | 45.43 | 45.65 | 0.6 | 0.4 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | INSW | 0.02 | 2.96238 | 101.27 | 2026-11-11 | 101.02 | 101.52 | 0.4 | 0.3 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | TNK | 0.015 | 2.52923 | 88.96 | 2026-11-11 | 88.74 | 89.18 | 0.4 | 0.4 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | STNG | 0.005 | 0.913854 | 82.07 | 2026-11-11 | 81.86 | 82.28 | 0.4 | 0.4 |  |  |  | 2d rolling-mean shipping_sticky_accel active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.0212999 | 0.420498 | 759.81 | 2026-11-11 | 757.91 | 761.71 |
| XLE | 0.0476032 | 11.2679 | 63.37 | 2026-11-11 | 63.2116 | 63.5284 |
| XME | -0.0200391 | -3.09149 | 97.23 | 2026-11-11 | 96.9869 | 97.4731 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | re_c03\|cro | MPC | BUY | 2 | 2 | 0.053712 | False |  | 402.84 | 2026-11-11 | 401.833 | 403.847 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | re_c03\|cro | VLO | BUY | 2 | 2 | 0.0484947 | False |  | 363.71 | 2026-11-11 | 362.801 | 364.619 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner\|refiner_slow | DINO | BUY | 3 | 3 | 0.020346 | False |  | 101.73 | 2026-11-11 | 101.476 | 101.984 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner\|refiner_slow | PBF | BUY | 4 | 4 | 0.0185947 | False |  | 69.73 | 2026-11-11 | 69.5557 | 69.9043 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | psx_ref\|cro | PSX | BUY | 1 | 1 | 0.0172453 | False |  | 258.68 | 2026-11-11 | 258.033 | 259.327 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner\|refiner_slow | DK | SELL | -1 | -1 | -0.00447733 | False |  | 67.16 | 2026-11-11 | 66.9921 | 67.3279 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | chemical | CE | BUY | 1 | 1 | 0.00343 | False |  | 51.45 | 2026-11-11 | 51.3214 | 51.5786 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XLE | SELL | -23 | -22 | -0.0929427 | False |  | 63.37 | 2026-11-11 | 63.2116 | 63.5284 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |


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
## Beta method for 2026-11-12 — as-of 2026-11-11

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-11-12-hs1sx7im/cached/targets-cl/2026-11-12. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
