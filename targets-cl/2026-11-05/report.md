# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-11-05

- Signal as-of date: 2026-11-04
- Target trading date: 2026-11-05
- AUM: $15,000.00
- Gross stock weight: 53.00%
- Single-name stock weight cap: 5.00%
- Net stock weight: 1.00%
- Gross hedge weight: 4.67%
- Total net weight after hedges: 1.09%
- Estimated turnover from current positions: 3.85%
- Full eligible order turnover: 1.71%
- Today's total child-order turnover: 1.41%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $0.53
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.27 | 0.27 | 4050 | 4050 | 10 |
| stock_short_without_hedge | 0.26 | -0.26 | 3900 | -3900 | 6 |
| total_hedge | 0.04668 | 0.000867 | 700.2 | 13.01 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.015 | 7.30045 | 30.82 | 2026-11-04 | 30.74 | 30.9 | 0.5 | 1.1 |  |  | 2026-11-10 | fixed_hold active from 2026-09-28 to before 2026-11-10 (initial signal 2026-09-25, last same-direction signal 2026-11-04) |
| bwt | TECK | 0.005 | 1.16351 | 64.46 | 2026-11-04 | 64.3 | 64.62 | 0.9 | 0.7 |  |  | 2026-11-10 | fixed_hold active from 2026-09-28 to before 2026-11-10 (initial signal 2026-09-25, last same-direction signal 2026-11-04) |
| cro | PSX | -0.02 | -1.15549 | 259.63 | 2026-11-04 | 258.98 | 260.28 | -0.4 | -0 |  |  |  | continuous hysteresis sign active |
| re_c03\|cro | MPC | -0.05 | -1.90995 | 392.68 | 2026-11-04 | 391.7 | 393.66 | -0 | 0.7 |  |  |  | continuous hysteresis sign active |
| re_c03\|cro | VLO | -0.05 | -2.05288 | 365.34 | 2026-11-04 | 364.43 | 366.25 | -0.1 | 0.7 |  |  |  | continuous hysteresis sign active |
| refiner\|refiner_slow | DK | 0.041 | 9.39505 | 65.46 | 2026-11-04 | 65.3 | 65.62 | 0.1 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| refiner\|refiner_slow\|cro | PBF | 0.013 | 2.68521 | 72.62 | 2026-11-04 | 72.44 | 72.8 | 1.2 | 4.2 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| refiner\|refiner_slow\|re_c03 | DINO | 0.016 | 2.29511 | 104.57 | 2026-11-04 | 104.31 | 104.83 | 0.1 | 1.1 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| services | FTI | -0.05 | -11.6279 | 64.5 | 2026-11-04 | 64.34 | 64.66 | 0.7 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.05 | -14.5462 | 51.56 | 2026-11-04 | 51.43 | 51.69 | 1.1 | 0.9 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.04 | -18.1818 | 33 | 2026-11-04 | 32.92 | 33.08 | 0.6 | 1.1 |  |  |  | continuous hysteresis sign active |
| shipping | DHT | 0.05 | 34.0136 | 22.05 | 2026-11-04 | 21.99 | 22.11 | 0.3 | 0.2 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | FRO | 0.05 | 15.4703 | 48.48 | 2026-11-04 | 48.36 | 48.6 | 0.6 | 0.4 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | INSW | 0.04 | 6.03865 | 99.36 | 2026-11-04 | 99.11 | 99.61 | 0.4 | 0.3 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | TNK | 0.03 | 5.06301 | 88.88 | 2026-11-04 | 88.66 | 89.1 | 0.3 | 0.3 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | STNG | 0.01 | 1.76367 | 85.05 | 2026-11-04 | 84.84 | 85.26 | 0.4 | 0.4 |  |  |  | 2d rolling-mean shipping_sticky_accel active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | -0.00292161 | -0.0571513 | 766.81 | 2026-11-04 | 764.893 | 768.727 |
| XLE | 0.0237736 | 5.61404 | 63.52 | 2026-11-04 | 63.3612 | 63.6788 |
| XME | -0.0199848 | -3.12979 | 95.78 | 2026-11-04 | 95.5405 | 96.0194 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | shipping | FRO | BUY | 1 | 1 | 0.003232 | False |  | 48.48 | 2026-11-04 | 48.3588 | 48.6012 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | DHT | BUY | 3 | 3 | 0.00441 | False |  | 22.05 | 2026-11-04 | 21.9949 | 22.1051 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | services | FTI | SELL | -1 | -1 | -0.0043 | False |  | 64.5 | 2026-11-04 | 64.3388 | 64.6612 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | services | HAL | SELL | -1 | -1 | -0.0022 | False |  | 33 | 2026-11-04 | 32.9175 | 33.0825 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |


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
## Beta method for 2026-11-05 — as-of 2026-11-04

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-11-05-4_s52ks6/cached/targets-cl/2026-11-05. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
