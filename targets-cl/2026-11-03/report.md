# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-11-03

- Signal as-of date: 2026-11-02
- Target trading date: 2026-11-03
- AUM: $15,000.00
- Gross stock weight: 44.36%
- Single-name stock weight cap: 5.00%
- Net stock weight: -4.20%
- Gross hedge weight: 20.07%
- Total net weight after hedges: 11.80%
- Estimated turnover from current positions: 29.60%
- Full eligible order turnover: 28.07%
- Today's total child-order turnover: 30.30%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $11.36
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.2008 | 0.2008 | 3012 | 3012 | 9 |
| stock_short_without_hedge | 0.2428 | -0.2428 | 3642 | -3642 | 6 |
| total_hedge | 0.200701 | 0.16002 | 3010.51 | 2400.3 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.015 | 7.7 | 29.16 | 2026-11-02 | 29.09 | 29.23 | 0.4 | 1.1 |  |  | 2026-11-06 | fixed_hold active from 2026-09-28 to before 2026-11-06 (initial signal 2026-09-25, last same-direction signal 2026-11-02) |
| bwt | TECK | 0.005 | 1.2 | 62.74 | 2026-11-02 | 62.58 | 62.9 | 0.9 | 0.7 |  |  | 2026-11-06 | fixed_hold active from 2026-09-28 to before 2026-11-06 (initial signal 2026-09-25, last same-direction signal 2026-11-02) |
| re_c03 | MPC | -0.05 | -1.7 | 430.39 | 2026-11-02 | 429.31 | 431.47 | 0.2 | 1.2 |  |  |  | continuous hysteresis sign active |
| re_c03 | VLO | -0.05 | -2 | 381.46 | 2026-11-02 | 380.51 | 382.41 | 0.1 | 1.2 |  |  |  | continuous hysteresis sign active |
| refiner\|refiner_slow | DK | 0.0454 | 9.7 | 70.19 | 2026-11-02 | 70.01 | 70.37 | 0.1 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| refiner\|refiner_slow | PBF | 0.0354 | 7.1 | 75.08 | 2026-11-02 | 74.89 | 75.27 | 0 | 1.7 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| refiner\|refiner_slow\|re_c03 | DINO | -0.0028 | -0.4 | 111.66 | 2026-11-02 | 111.38 | 111.94 | 0.1 | 1 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| services | FTI | -0.05 | -11.2 | 66.87 | 2026-11-02 | 66.7 | 67.04 | 0.7 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.05 | -14.3 | 52.31 | 2026-11-02 | 52.18 | 52.44 | 1.1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.04 | -17.3 | 34.61 | 2026-11-02 | 34.52 | 34.7 | 0.6 | 1.1 |  |  |  | continuous hysteresis sign active |
| shipping | DHT | 0.03 | 18.9 | 23.86 | 2026-11-02 | 23.8 | 23.92 | 0.3 | 0.1 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | FRO | 0.03 | 8.6 | 52.08 | 2026-11-02 | 51.95 | 52.21 | 0.6 | 0.3 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | INSW | 0.02 | 2.8 | 105.68 | 2026-11-02 | 105.42 | 105.94 | 0.4 | 0.3 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | TNK | 0.015 | 2.4 | 95.47 | 2026-11-02 | 95.23 | 95.71 | 0.3 | 0.3 |  |  |  | 2d rolling-mean shipping_sticky_accel active |
| shipping | STNG | 0.005 | 0.9 | 86.62 | 2026-11-02 | 86.4 | 86.84 | 0.4 | 0.4 |  |  |  | 2d rolling-mean shipping_sticky_accel active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.0696964 | 1.39004 | 752.1 | 2026-11-02 | 750.22 | 753.98 |
| XLE | 0.110664 | 24.6834 | 67.25 | 2026-11-02 | 67.0819 | 67.4181 |
| XME | -0.0203404 | -3.12416 | 97.66 | 2026-11-02 | 97.4159 | 97.9042 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | services | HAL | SELL | -13 | -13 | -0.0299953 | False |  | 34.61 | 2026-11-02 | 34.5235 | 34.6965 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | DHT | BUY | 19 | 19 | 0.0302227 | False |  | 23.86 | 2026-11-02 | 23.8004 | 23.9197 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | FRO | BUY | 9 | 9 | 0.031248 | False |  | 52.08 | 2026-11-02 | 51.9498 | 52.2102 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | INSW | BUY | 3 | 3 | 0.021136 | False |  | 105.68 | 2026-11-02 | 105.416 | 105.944 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | TNK | BUY | 2 | 2 | 0.0127293 | False |  | 95.47 | 2026-11-02 | 95.2313 | 95.7087 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner\|refiner_slow | PBF | BUY | 1 | 1 | 0.00500533 | False |  | 75.08 | 2026-11-02 | 74.8923 | 75.2677 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | shipping | STNG | BUY | 1 | 1 | 0.00577467 | False |  | 86.62 | 2026-11-02 | 86.4035 | 86.8366 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner\|refiner_slow | DK | BUY | 1 | 1 | 0.00467933 | False |  | 70.19 | 2026-11-02 | 70.0145 | 70.3655 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XLE | BUY | 25 | 25 | 0.112083 | False |  | 67.25 | 2026-11-02 | 67.0819 | 67.4181 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
| hedge | hedge | SPY | SELL | -1 | -1 | -0.05014 | False |  | 752.1 | 2026-11-02 | 750.22 | 753.98 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |


## Strategy changes and allocation notes

- CL operator risk reduction effective target session 2026-10-23: chemical allocation reduced from 28% to 14%; psx_ref allocation reduced from 5% to 0% (suspended). At that decision, released 19 percentage points remained cash; no renormalization. Later dated decisions below supersede allocation details.
- At that decision other sleeves were unchanged. CL AUM $15,000 and legacy daily beta remain unchanged. CRO retains its own PSX leg and SPY-only hedge: clearing psx_ref does NOT mean flattening all account PSX. Recompute net stocks and component hedges.
- Chemical is halved BEFORE the existing 5% net single-name cap; previously capped names need not fall by exactly half. Allocation migration turnover is not a signal change.
- Chemical decision rationale: operator questioned the economic clarity of asymmetric exits plus renewing hold-21 and potential historical overfitting, not only recent losses. Rules are deterministic and unchanged; overfitting is a concern, not an established finding. Review parameter robustness, simpler exits, hedge/cost attribution and a 28% counterfactual before any restoration. See docs/cl_risk_reduction_2026-10-23.md.
- CURRENT CL from 2026-11-02: chemical 0% (25% research dummy is NOT live), shipping 20%, refiner 3%, refiner_slow/re_slow 10%, services 20%, bwt 2%, re_c03 20%, others including CRO 0%. Budget 75%; no renormalization; all book AUMs unchanged.
- re_c03 replaces CRO: DINO/MPC/VLO 20/30/50%, full balance, quarterly near MA3-MA30 entry, far change5 exit, far std30 thresholds. SPY + XLE legacy DAILY hedges; old CRO half-balance/SPY-only retired.
- Refiner DK/DINO/PBF 30/40/30%; slow DK/DINO/PBF 40/30/30%, HO m1 momentum gate and carry ffill.diff50. Other algorithms unchanged. Track allocation/hedge migration separately. See docs/cl_reallocation_2026-11-02.md.
- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.
- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.
- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.
## Beta method for 2026-11-03 — as-of 2026-11-02

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-11-03-a5qvthw9/cached/targets-cl/2026-11-03. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
