# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-11-13

- Signal as-of date: 2026-11-12
- Target trading date: 2026-11-13
- AUM: $15,000.00
- Gross stock weight: 51.00%
- Single-name stock weight cap: 5.00%
- Net stock weight: -23.00%
- Gross hedge weight: 21.91%
- Total net weight after hedges: -5.13%
- Estimated turnover from current positions: 14.85%
- Full eligible order turnover: 12.92%
- Today's total child-order turnover: 15.71%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $5.89
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.14 | 0.14 | 2100 | 2100 | 10 |
| stock_short_without_hedge | 0.37 | -0.37 | 5550 | -5550 | 10 |
| total_hedge | 0.219058 | 0.178719 | 3285.87 | 2680.79 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.015 | 7.56048 | 29.76 | 2026-11-12 | 29.69 | 29.83 | 0.6 | 1.1 |  |  | 2026-11-18 | fixed_hold active from 2026-09-28 to before 2026-11-18 (initial signal 2026-09-25, last same-direction signal 2026-11-12) |
| bwt | TECK | 0.005 | 1.22569 | 61.19 | 2026-11-12 | 61.04 | 61.34 | 0.9 | 0.7 |  |  | 2026-11-18 | fixed_hold active from 2026-09-28 to before 2026-11-18 (initial signal 2026-09-25, last same-direction signal 2026-11-12) |
| chemical | CE | -0.045 | -13.1682 | 51.26 | 2026-11-12 | 51.13 | 51.39 | 0.7 | 0.9 |  |  | 2026-11-17 | fixed_hold active from 2026-11-06 to before 2026-11-17 (initial signal 2026-11-05, last same-direction signal 2026-11-12) |
| chemical | DOW | -0.045 | -20.362 | 33.15 | 2026-11-12 | 33.07 | 33.23 | -0 | 1 |  |  | 2026-11-17 | fixed_hold active from 2026-11-06 to before 2026-11-17 (initial signal 2026-11-05, last same-direction signal 2026-11-12) |
| chemical | LYB | -0.045 | -10.5667 | 63.88 | 2026-11-12 | 63.72 | 64.04 | -0.3 | 1.1 |  |  | 2026-11-17 | fixed_hold active from 2026-11-06 to before 2026-11-17 (initial signal 2026-11-05, last same-direction signal 2026-11-12) |
| chemical | WLK | -0.015 | -3.58394 | 62.78 | 2026-11-12 | 62.62 | 62.94 | 0.5 | 0.6 |  |  | 2026-11-17 | fixed_hold active from 2026-11-06 to before 2026-11-17 (initial signal 2026-11-05, last same-direction signal 2026-11-12) |
| cro | PSX | -0.02 | -1.14107 | 262.91 | 2026-11-12 | 262.25 | 263.57 | -0.2 | -0 |  |  |  | continuous hysteresis sign active |
| re_c03\|cro | MPC | -0.05 | -1.81664 | 412.85 | 2026-11-12 | 411.82 | 413.88 | 0.1 | 0.7 |  |  |  | continuous hysteresis sign active |
| re_c03\|cro | VLO | -0.05 | -2.00027 | 374.95 | 2026-11-12 | 374.01 | 375.89 | -0 | 0.8 |  |  |  | continuous hysteresis sign active |
| refiner\|refiner_slow | DK | 0.041 | 8.98991 | 68.41 | 2026-11-12 | 68.24 | 68.58 | 0.2 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| refiner\|refiner_slow\|cro | PBF | 0.013 | 2.74803 | 70.96 | 2026-11-12 | 70.78 | 71.14 | 1 | 4.2 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| refiner\|refiner_slow\|re_c03 | DINO | 0.016 | 2.34949 | 102.15 | 2026-11-12 | 101.89 | 102.41 | 0.2 | 1.1 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| services | FTI | -0.04 | -9.24214 | 64.92 | 2026-11-12 | 64.76 | 65.08 | 0.7 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.04 | -11.7855 | 50.91 | 2026-11-12 | 50.78 | 51.04 | 1 | 0.9 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.02 | -9.15751 | 32.76 | 2026-11-12 | 32.68 | 32.84 | 0.5 | 1.1 |  |  |  | continuous hysteresis sign active |
| shipping | DHT | 0.015 | 10.0987 | 22.28 | 2026-11-12 | 22.22 | 22.34 | 0.4 | 0.3 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | FRO | 0.015 | 4.81181 | 46.76 | 2026-11-12 | 46.64 | 46.88 | 0.6 | 0.4 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | INSW | 0.01 | 1.43335 | 104.65 | 2026-11-12 | 104.39 | 104.91 | 0.4 | 0.3 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | TNK | 0.0075 | 1.27119 | 88.5 | 2026-11-12 | 88.28 | 88.72 | 0.4 | 0.4 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | STNG | 0.0025 | 0.449425 | 83.44 | 2026-11-12 | 83.23 | 83.65 | 0.4 | 0.4 |  |  |  | 2d rolling-mean shipping_sticky_accel active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.0391018 | 0.774681 | 757.12 | 2026-11-12 | 755.227 | 759.013 |
| XLE | 0.159787 | 37.2579 | 64.33 | 2026-11-12 | 64.1692 | 64.4908 |
| XME | -0.0201695 | -3.17629 | 95.25 | 2026-11-12 | 95.0119 | 95.4881 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | refiner\|refiner_slow\|re_c03 | DINO | SELL | -3 | -3 | -0.02043 | False |  | 102.15 | 2026-11-12 | 101.895 | 102.405 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | DHT | SELL | -12 | -12 | -0.017824 | False |  | 22.28 | 2026-11-12 | 22.2243 | 22.3357 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | FRO | SELL | -5 | -5 | -0.0155867 | False |  | 46.76 | 2026-11-12 | 46.6431 | 46.8769 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | INSW | SELL | -2 | -2 | -0.0139533 | False |  | 104.65 | 2026-11-12 | 104.388 | 104.912 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | TNK | SELL | -2 | -2 | -0.0118 | False |  | 88.5 | 2026-11-12 | 88.2788 | 88.7212 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | STNG | SELL | -1 | -1 | -0.00556267 | False |  | 83.44 | 2026-11-12 | 83.2314 | 83.6486 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | SPY | BUY | 1 | 1 | 0.0504747 | False |  | 757.12 | 2026-11-12 | 755.227 | 759.013 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XLE | BUY | 3 | 5 | 0.0214433 | False |  | 64.33 | 2026-11-12 | 64.1692 | 64.4908 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |


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
## Beta method for 2026-11-13 — as-of 2026-11-12

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-11-13-i3tt0ifh/cached/targets-cl/2026-11-13. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
