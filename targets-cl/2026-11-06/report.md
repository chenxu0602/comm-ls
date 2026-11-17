# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-11-06

- Signal as-of date: 2026-11-05
- Target trading date: 2026-11-06
- AUM: $15,000.00
- Gross stock weight: 62.00%
- Single-name stock weight cap: 5.00%
- Net stock weight: -24.00%
- Gross hedge weight: 26.30%
- Total net weight after hedges: -1.72%
- Estimated turnover from current positions: 48.26%
- Full eligible order turnover: 46.65%
- Today's total child-order turnover: 46.69%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $17.51
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.19 | 0.19 | 2850 | 2850 | 10 |
| stock_short_without_hedge | 0.43 | -0.43 | 6450 | -6450 | 10 |
| total_hedge | 0.26298 | 0.222782 | 3944.7 | 3341.73 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.015 | 8.00997 | 28.09 | 2026-11-05 | 28.02 | 28.16 | 0.5 | 1.1 |  |  | 2026-11-11 | fixed_hold active from 2026-09-28 to before 2026-11-11 (initial signal 2026-09-25, last same-direction signal 2026-11-05) |
| bwt | TECK | 0.005 | 1.25188 | 59.91 | 2026-11-05 | 59.76 | 60.06 | 0.9 | 0.7 |  |  | 2026-11-11 | fixed_hold active from 2026-09-28 to before 2026-11-11 (initial signal 2026-09-25, last same-direction signal 2026-11-05) |
| chemical | CE | -0.05 | -15.6773 | 47.84 | 2026-11-05 | 47.72 | 47.96 | 0.7 | 0.9 |  |  | 2026-11-10 | fixed_hold active from 2026-11-06 to before 2026-11-10 (initial signal 2026-11-05, last same-direction signal 2026-11-05) |
| chemical | DOW | -0.05 | -23.4522 | 31.98 | 2026-11-05 | 31.9 | 32.06 | -0 | 1 |  |  | 2026-11-10 | fixed_hold active from 2026-11-06 to before 2026-11-10 (initial signal 2026-11-05, last same-direction signal 2026-11-05) |
| chemical | LYB | -0.05 | -12.1694 | 61.63 | 2026-11-05 | 61.48 | 61.78 | -0.3 | 1.1 |  |  | 2026-11-10 | fixed_hold active from 2026-11-06 to before 2026-11-10 (initial signal 2026-11-05, last same-direction signal 2026-11-05) |
| chemical | WLK | -0.02 | -4.52625 | 66.28 | 2026-11-05 | 66.11 | 66.45 | 0.5 | 0.6 |  |  | 2026-11-10 | fixed_hold active from 2026-11-06 to before 2026-11-10 (initial signal 2026-11-05, last same-direction signal 2026-11-05) |
| cro | PSX | -0.02 | -1.21438 | 247.04 | 2026-11-05 | 246.42 | 247.66 | -0.3 | -0 |  |  |  | continuous hysteresis sign active |
| re_c03\|cro | MPC | -0.05 | -1.9877 | 377.32 | 2026-11-05 | 376.38 | 378.26 | -0 | 0.7 |  |  |  | continuous hysteresis sign active |
| re_c03\|cro | VLO | -0.05 | -2.13535 | 351.23 | 2026-11-05 | 350.35 | 352.11 | -0.1 | 0.7 |  |  |  | continuous hysteresis sign active |
| refiner\|refiner_slow | DK | 0.041 | 9.84157 | 62.49 | 2026-11-05 | 62.33 | 62.65 | 0.1 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| refiner\|refiner_slow\|cro | PBF | 0.013 | 2.85213 | 68.37 | 2026-11-05 | 68.2 | 68.54 | 1 | 4.2 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| refiner\|refiner_slow\|re_c03 | DINO | 0.016 | 2.45474 | 97.77 | 2026-11-05 | 97.53 | 98.01 | 0.2 | 1.1 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| services | FTI | -0.05 | -12.1773 | 61.59 | 2026-11-05 | 61.44 | 61.74 | 0.7 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.05 | -15.1088 | 49.64 | 2026-11-05 | 49.52 | 49.76 | 1 | 0.9 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.04 | -18.797 | 31.92 | 2026-11-05 | 31.84 | 32 | 0.5 | 1.1 |  |  |  | continuous hysteresis sign active |
| shipping | DHT | 0.03 | 21.9727 | 20.48 | 2026-11-05 | 20.43 | 20.53 | 0.4 | 0.3 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | FRO | 0.03 | 10.0671 | 44.7 | 2026-11-05 | 44.59 | 44.81 | 0.7 | 0.4 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | INSW | 0.02 | 3.17561 | 94.47 | 2026-11-05 | 94.23 | 94.71 | 0.4 | 0.3 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | TNK | 0.015 | 2.74491 | 81.97 | 2026-11-05 | 81.77 | 82.17 | 0.4 | 0.4 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | STNG | 0.005 | 0.928908 | 80.74 | 2026-11-05 | 80.54 | 80.94 | 0.4 | 0.4 |  |  |  | 2d rolling-mean shipping_sticky_accel active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.0439749 | 0.899896 | 733 | 2026-11-05 | 731.168 | 734.832 |
| XLE | 0.198906 | 48.4113 | 61.63 | 2026-11-05 | 61.4759 | 61.7841 |
| XME | -0.0200991 | -3.33429 | 90.42 | 2026-11-05 | 90.1939 | 90.646 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | chemical | CE | SELL | -16 | -16 | -0.0510293 | False |  | 47.84 | 2026-11-05 | 47.7204 | 47.9596 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | chemical | DOW | SELL | -23 | -23 | -0.049036 | False |  | 31.98 | 2026-11-05 | 31.9 | 32.0599 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | chemical | LYB | SELL | -12 | -12 | -0.049304 | False |  | 61.63 | 2026-11-05 | 61.4759 | 61.7841 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | chemical | WLK | SELL | -5 | -5 | -0.0220933 | False |  | 66.28 | 2026-11-05 | 66.1143 | 66.4457 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | INSW | SELL | -3 | -3 | -0.018894 | False |  | 94.47 | 2026-11-05 | 94.2338 | 94.7062 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | DHT | SELL | -12 | -12 | -0.016384 | False |  | 20.48 | 2026-11-05 | 20.4288 | 20.5312 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | FRO | SELL | -5 | -5 | -0.0149 | False |  | 44.7 | 2026-11-05 | 44.5883 | 44.8118 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | TNK | SELL | -2 | -2 | -0.0109293 | False |  | 81.97 | 2026-11-05 | 81.7651 | 82.1749 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | STNG | SELL | -1 | -1 | -0.00538267 | False |  | 80.74 | 2026-11-05 | 80.5381 | 80.9418 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | services | SLB | SELL | -1 | -1 | -0.00330933 | False |  | 49.64 | 2026-11-05 | 49.5159 | 49.7641 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner\|refiner_slow | DK | BUY | 1 | 1 | 0.004166 | False |  | 62.49 | 2026-11-05 | 62.3338 | 62.6462 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XLE | BUY | 43 | 42 | 0.172564 | False |  | 61.63 | 2026-11-05 | 61.4759 | 61.7841 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
| hedge | hedge | SPY | BUY | 1 | 1 | 0.0488667 | False |  | 733 | 2026-11-05 | 731.168 | 734.832 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |


## Strategy changes and allocation notes

- CL operator risk reduction effective target session 2026-10-23: chemical allocation reduced from 28% to 14%; psx_ref allocation reduced from 5% to 0% (suspended). At that decision, released 19 percentage points remained cash; no renormalization. Later dated decisions below supersede allocation details.
- At that decision other sleeves were unchanged. CL AUM $15,000 and legacy daily beta remain unchanged. CRO retains its own PSX leg and SPY-only hedge: clearing psx_ref does NOT mean flattening all account PSX. Recompute net stocks and component hedges.
- Chemical is halved BEFORE the existing 5% net single-name cap; previously capped names need not fall by exactly half. Allocation migration turnover is not a signal change.
- Chemical decision rationale: operator questioned the economic clarity of asymmetric exits plus renewing hold-21 and potential historical overfitting, not only recent losses. Rules are deterministic and unchanged; overfitting is a concern, not an established finding. Review parameter robustness, simpler exits, hedge/cost attribution and a 28% counterfactual before any restoration. See docs/cl_risk_reduction_2026-10-23.md.
- CURRENT CL from 2026-11-06: shipping20->10% operator risk reduction; chemical20/refiner3/refiner_slow8/services20/bwt2/CRO20/re_c03 10% unchanged. Nominal budget93%, no normalization; released10 percentage points stay cash. No automatic shipping restoration.
- Operator corrected notebook: chemical retains hold2 (NOT direct signal, NOT hold21). Slow HO m1 gate reads carry_data_2 from Nov06 to match notebook default loader, with strict lookback/arrival validation, no canonical fallback. L/PP exits and baskets unchanged. CRO remains half-balance SPY-only; re_c03 SPY+XLE. AUM and legacy DAILY beta unchanged. See docs/cl_shipping_reduction_2026-11-06.md.
- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.
- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.
- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.
## Beta method for 2026-11-06 — as-of 2026-11-05

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-11-06-lajdlroc/cached/targets-cl/2026-11-06. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
