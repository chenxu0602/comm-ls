# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-11-04

- Signal as-of date: 2026-11-03
- Target trading date: 2026-11-04
- AUM: $15,000.00
- Gross stock weight: 53.00%
- Single-name stock weight cap: 5.00%
- Net stock weight: 1.00%
- Gross hedge weight: 5.94%
- Total net weight after hedges: 2.02%
- Estimated turnover from current positions: 28.60%
- Full eligible order turnover: 26.90%
- Today's total child-order turnover: 27.57%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $10.34
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.27 | 0.27 | 4050 | 4050 | 10 |
| stock_short_without_hedge | 0.26 | -0.26 | 3900 | -3900 | 6 |
| total_hedge | 0.059352 | 0.010225 | 890.28 | 153.37 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.015 | 7.39159 | 30.44 | 2026-11-03 | 30.36 | 30.52 | 0.5 | 1.1 |  |  | 2026-11-09 | fixed_hold active from 2026-09-28 to before 2026-11-09 (initial signal 2026-09-25, last same-direction signal 2026-11-03) |
| bwt | TECK | 0.005 | 1.2134 | 61.81 | 2026-11-03 | 61.66 | 61.96 | 0.9 | 0.7 |  |  | 2026-11-09 | fixed_hold active from 2026-09-28 to before 2026-11-09 (initial signal 2026-09-25, last same-direction signal 2026-11-03) |
| cro | PSX | -0.02 | -1.10318 | 271.94 | 2026-11-03 | 271.26 | 272.62 | -0.4 | -0 |  |  |  | continuous hysteresis sign active |
| re_c03\|cro | MPC | -0.05 | -1.75504 | 427.34 | 2026-11-03 | 426.27 | 428.41 | 0 | 0.7 |  |  |  | continuous hysteresis sign active |
| re_c03\|cro | VLO | -0.05 | -1.93473 | 387.65 | 2026-11-03 | 386.68 | 388.62 | -0.1 | 0.7 |  |  |  | continuous hysteresis sign active |
| refiner\|refiner_slow | DK | 0.041 | 8.68031 | 70.85 | 2026-11-03 | 70.67 | 71.03 | 0.1 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| refiner\|refiner_slow\|cro | PBF | 0.013 | 2.5061 | 77.81 | 2026-11-03 | 77.62 | 78 | 1.1 | 4.2 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| refiner\|refiner_slow\|re_c03 | DINO | 0.016 | 2.11715 | 113.36 | 2026-11-03 | 113.08 | 113.64 | 0.1 | 1 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| services | FTI | -0.05 | -11.2376 | 66.74 | 2026-11-03 | 66.57 | 66.91 | 0.7 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.05 | -14.3871 | 52.13 | 2026-11-03 | 52 | 52.26 | 1.1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.04 | -17.6108 | 34.07 | 2026-11-03 | 33.98 | 34.16 | 0.6 | 1.1 |  |  |  | continuous hysteresis sign active |
| shipping | DHT | 0.05 | 31.3545 | 23.92 | 2026-11-03 | 23.86 | 23.98 | 0.3 | 0.1 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | FRO | 0.05 | 14.2993 | 52.45 | 2026-11-03 | 52.32 | 52.58 | 0.6 | 0.3 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | INSW | 0.04 | 5.72792 | 104.75 | 2026-11-03 | 104.49 | 105.01 | 0.4 | 0.3 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | TNK | 0.03 | 4.7081 | 95.58 | 2026-11-03 | 95.34 | 95.82 | 0.3 | 0.3 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | STNG | 0.01 | 1.71743 | 87.34 | 2026-11-03 | 87.12 | 87.56 | 0.4 | 0.4 |  |  |  | 2d rolling-mean shipping_sticky_accel active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | -0.0043476 | -0.0864506 | 754.35 | 2026-11-03 | 752.464 | 756.236 |
| XLE | 0.0347883 | 7.82581 | 66.68 | 2026-11-03 | 66.5133 | 66.8467 |
| XME | -0.020216 | -3.13394 | 96.76 | 2026-11-03 | 96.5181 | 97.0019 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | refiner\|refiner_slow\|cro | PBF | SELL | -4 | -4 | -0.0207493 | False |  | 77.81 | 2026-11-03 | 77.6155 | 78.0045 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | cro | PSX | SELL | -1 | -1 | -0.0181293 | False |  | 271.94 | 2026-11-03 | 271.26 | 272.62 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | DHT | BUY | 12 | 12 | 0.019136 | False |  | 23.92 | 2026-11-03 | 23.8602 | 23.9798 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | INSW | BUY | 3 | 3 | 0.02095 | False |  | 104.75 | 2026-11-03 | 104.488 | 105.012 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | FRO | BUY | 5 | 5 | 0.0174833 | False |  | 52.45 | 2026-11-03 | 52.3189 | 52.5811 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | TNK | BUY | 3 | 3 | 0.019116 | False |  | 95.58 | 2026-11-03 | 95.3411 | 95.819 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner\|refiner_slow\|re_c03 | DINO | BUY | 2 | 2 | 0.0151147 | False |  | 113.36 | 2026-11-03 | 113.077 | 113.643 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | STNG | BUY | 1 | 1 | 0.00582267 | False |  | 87.34 | 2026-11-03 | 87.1216 | 87.5583 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XLE | SELL | -17 | -20 | -0.0889067 | False |  | 66.68 | 2026-11-03 | 66.5133 | 66.8467 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
| hedge | hedge | SPY | SELL | -1 | -1 | -0.05029 | False |  | 754.35 | 2026-11-03 | 752.464 | 756.236 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |


## Strategy changes and allocation notes

- CL operator risk reduction effective target session 2026-10-23: chemical allocation reduced from 28% to 14%; psx_ref allocation reduced from 5% to 0% (suspended). At that decision, released 19 percentage points remained cash; no renormalization. Later dated decisions below supersede allocation details.
- At that decision other sleeves were unchanged. CL AUM $15,000 and legacy daily beta remain unchanged. CRO retains its own PSX leg and SPY-only hedge: clearing psx_ref does NOT mean flattening all account PSX. Recompute net stocks and component hedges.
- Chemical is halved BEFORE the existing 5% net single-name cap; previously capped names need not fall by exactly half. Allocation migration turnover is not a signal change.
- Chemical decision rationale: operator questioned the economic clarity of asymmetric exits plus renewing hold-21 and potential historical overfitting, not only recent losses. Rules are deterministic and unchanged; overfitting is a concern, not an established finding. Review parameter robustness, simpler exits, hedge/cost attribution and a 28% counterfactual before any restoration. See docs/cl_risk_reduction_2026-10-23.md.
- CURRENT CL from 2026-11-04: chemical20/shipping20/refiner3/refiner_slow8/services20/bwt2/CRO20/re_c03 10%; nominal budget103%, no renormalization. AUM and legacy DAILY beta unchanged.
- CRO restored alongside re_c03, not CRP: VLO/MPC/PSX/PBF=30/20/20/20%, basket total90%, half-balance, SPY-only. Idle basket capacity is preserved. re_c03 retains SPY+XLE hedging.
- Chemical re-enabled by operator: DOW/LYB/WLK/CE 30/30/10/30%, CL carry entry, L and PP own-vol exits, hold2, SPY+XLE. Current flat signal is not a permanent pause; future signals may open positions. See docs/cl_chemical_lp_2026-11-04.md.
- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.
- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.
- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.
## Beta method for 2026-11-04 — as-of 2026-11-03

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-11-04-wvcqr0yp/cached/targets-cl/2026-11-04. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
