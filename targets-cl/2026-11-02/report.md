# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-11-02

- Signal as-of date: 2026-10-30
- Target trading date: 2026-11-02
- AUM: $15,000.00
- Gross stock weight: 34.12%
- Single-name stock weight cap: 5.00%
- Net stock weight: -15.40%
- Gross hedge weight: 28.75%
- Total net weight after hedges: 9.28%
- Estimated turnover from current positions: 55.46%
- Full eligible order turnover: 55.46%
- Today's total child-order turnover: 39.77%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $14.92
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.0936 | 0.0936 | 1404 | 1404 | 4 |
| stock_short_without_hedge | 0.2476 | -0.2476 | 3714 | -3714 | 6 |
| total_hedge | 0.287466 | 0.246809 | 4311.99 | 3702.14 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.015 | 7.7 | 29.05 | 2026-10-30 | 28.98 | 29.12 | 0.4 | 1.1 |  |  | 2026-11-05 | fixed_hold active from 2026-09-28 to before 2026-11-05 (initial signal 2026-09-25, last same-direction signal 2026-10-30) |
| bwt | TECK | 0.005 | 1.2 | 60.61 | 2026-10-30 | 60.46 | 60.76 | 0.9 | 0.7 |  |  | 2026-11-05 | fixed_hold active from 2026-09-28 to before 2026-11-05 (initial signal 2026-09-25, last same-direction signal 2026-10-30) |
| re_c03 | MPC | -0.05 | -1.7 | 444.73 | 2026-10-30 | 443.62 | 445.84 | 0.2 | 1.2 |  |  |  | continuous hysteresis sign active |
| re_c03 | VLO | -0.05 | -1.9 | 399.66 | 2026-10-30 | 398.66 | 400.66 | 0.1 | 1.2 |  |  |  | continuous hysteresis sign active |
| refiner\|refiner_slow | DK | 0.0418 | 8.5 | 73.57 | 2026-10-30 | 73.39 | 73.75 | 0.1 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| refiner\|refiner_slow | PBF | 0.0318 | 6.1 | 78 | 2026-10-30 | 77.81 | 78.19 | 0 | 1.7 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| refiner\|refiner_slow\|re_c03 | DINO | -0.0076 | -1 | 115 | 2026-10-30 | 114.71 | 115.29 | 0.1 | 1 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| services | FTI | -0.05 | -10.9 | 68.77 | 2026-10-30 | 68.6 | 68.94 | 0.7 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.05 | -14 | 53.74 | 2026-10-30 | 53.61 | 53.87 | 1.1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.04 | -16.6 | 36.17 | 2026-10-30 | 36.08 | 36.26 | 0.6 | 1.1 |  |  |  | continuous hysteresis sign active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.1133 | 2.24886 | 755.72 | 2026-10-30 | 753.831 | 757.609 |
| XLE | 0.153837 | 32.9557 | 70.02 | 2026-10-30 | 69.8449 | 70.195 |
| XME | -0.0203284 | -3.11722 | 97.82 | 2026-10-30 | 97.5754 | 98.0645 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | services | FTI | SELL | -7 | -7 | -0.0320927 | False |  | 68.77 | 2026-10-30 | 68.5981 | 68.9419 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | services | HAL | SELL | -13 | -13 | -0.0313473 | False |  | 36.17 | 2026-10-30 | 36.0796 | 36.2604 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | services | SLB | SELL | -8 | -8 | -0.0286613 | False |  | 53.74 | 2026-10-30 | 53.6057 | 53.8744 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | bwt | ERO | SELL | -14 | -14 | -0.0271133 | False |  | 29.05 | 2026-10-30 | 28.9774 | 29.1226 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner\|refiner_slow | DK | BUY | 6 | 6 | 0.029428 | False |  | 73.57 | 2026-10-30 | 73.3861 | 73.7539 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | re_c03 | VLO | SELL | -1 | -1 | -0.026644 | False |  | 399.66 | 2026-10-30 | 398.661 | 400.659 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner\|refiner_slow\|re_c03 | DINO | SELL | -3 | -2 | -0.0153333 | True |  | 115 | 2026-10-30 | 114.713 | 115.287 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner\|refiner_slow | PBF | BUY | 4 | 4 | 0.0208 | False |  | 78 | 2026-10-30 | 77.805 | 78.195 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | re_c03 | MPC | SELL | -1 | -1 | -0.0296487 | False |  | 444.73 | 2026-10-30 | 443.618 | 445.842 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | bwt | TECK | SELL | -3 | -3 | -0.012122 | False |  | 60.61 | 2026-10-30 | 60.4585 | 60.7615 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XLE | BUY | 34 | 1 | 0.004668 | True |  | 70.02 | 2026-10-30 | 69.8449 | 70.195 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
| hedge | hedge | SPY | BUY | 2 | 2 | 0.100763 | False |  | 755.72 | 2026-10-30 | 753.831 | 757.609 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XME | BUY | 6 | 6 | 0.039128 | False |  | 97.82 | 2026-10-30 | 97.5754 | 98.0645 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |


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
## Beta method for 2026-11-02 — as-of 2026-10-30

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-11-02-w9zewr1_/cached/targets-cl/2026-11-02. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
