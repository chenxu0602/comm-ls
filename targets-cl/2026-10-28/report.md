# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-10-28

- Signal as-of date: 2026-10-27
- Target trading date: 2026-10-28
- AUM: $15,000.00
- Gross stock weight: 18.50%
- Single-name stock weight cap: 5.00%
- Net stock weight: 0.50%
- Gross hedge weight: 8.10%
- Total net weight after hedges: -7.60%
- Estimated turnover from current positions: 36.55%
- Full eligible order turnover: 36.08%
- Today's total child-order turnover: 35.19%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $13.20
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.095 | 0.095 | 1425 | 1425 | 5 |
| stock_short_without_hedge | 0.09 | -0.09 | 1350 | -1350 | 6 |
| total_hedge | 0.080997 | -0.080997 | 1214.96 | -1214.96 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.045 | 20.8 | 32.52 | 2026-10-27 | 32.44 | 32.6 | 0.4 | 1.1 |  |  | 2026-11-02 | fixed_hold active from 2026-09-28 to before 2026-11-02 (initial signal 2026-09-25, last same-direction signal 2026-10-27) |
| bwt | TECK | 0.015 | 3.6 | 62.28 | 2026-10-27 | 62.12 | 62.44 | 0.9 | 0.7 |  |  | 2026-11-02 | fixed_hold active from 2026-09-28 to before 2026-11-02 (initial signal 2026-09-25, last same-direction signal 2026-10-27) |
| cro | MPC | -0.02 | -0.7 | 435.98 | 2026-10-27 | 434.89 | 437.07 | -0.3 | -0 |  |  |  | continuous hysteresis sign active |
| cro | VLO | -0.015 | -0.6 | 387.34 | 2026-10-27 | 386.37 | 388.31 | -0.4 | -0 |  |  |  | continuous hysteresis sign active |
| refiner_slow\|cro | PSX | -0.005 | -0.3 | 268.53 | 2026-10-27 | 267.86 | 269.2 | -1.3 | -2.3 |  |  |  | continuous hysteresis sign active |
| refiner\|refiner_slow | DK | 0.0125 | 2.7 | 70.3 | 2026-10-27 | 70.12 | 70.48 | 0.1 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| refiner\|refiner_slow | DINO | 0.0115 | 1.5 | 114.21 | 2026-10-27 | 113.92 | 114.5 | 0.1 | 1 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| refiner\|refiner_slow | PBF | 0.011 | 2.2 | 73.63 | 2026-10-27 | 73.45 | 73.81 | 0 | 1.7 |  |  |  | 5d rolling-mean band_hysteresis active\|continuous hysteresis sign active |
| services | FTI | -0.02 | -4.2 | 71.38 | 2026-10-27 | 71.2 | 71.56 | 0.7 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -5.5 | 54.08 | 2026-10-27 | 53.94 | 54.22 | 1.1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4.2 | 35.62 | 2026-10-27 | 35.53 | 35.71 | 0.6 | 1.1 |  |  |  | continuous hysteresis sign active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | -0.00920633 | -0.179423 | 769.66 | 2026-10-27 | 767.736 | 771.584 |
| XLE | -0.0107263 | -2.35881 | 68.21 | 2026-10-27 | 68.0395 | 68.3805 |
| XME | -0.0610645 | -9.1141 | 100.5 | 2026-10-27 | 100.249 | 100.751 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | chemical | LYB | BUY | 8 | 8 | 0.0359627 | False |  | 67.43 | 2026-10-27 | 67.2614 | 67.5986 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | chemical | WLK | BUY | 7 | 7 | 0.0308793 | False |  | 66.17 | 2026-10-27 | 66.0046 | 66.3354 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner\|refiner_slow | DK | SELL | -6 | -6 | -0.02812 | False |  | 70.3 | 2026-10-27 | 70.1243 | 70.4758 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | chemical | DOW | BUY | 13 | 13 | 0.029276 | False |  | 33.78 | 2026-10-27 | 33.6955 | 33.8644 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner_slow\|cro | PSX | SELL | -1 | -1 | -0.017902 | False |  | 268.53 | 2026-10-27 | 267.859 | 269.201 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | cro | MPC | SELL | -1 | -1 | -0.0290653 | False |  | 435.98 | 2026-10-27 | 434.89 | 437.07 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner\|refiner_slow | PBF | SELL | -4 | -4 | -0.0196347 | False |  | 73.63 | 2026-10-27 | 73.4459 | 73.8141 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | cro | VLO | SELL | -1 | -1 | -0.0258227 | False |  | 387.34 | 2026-10-27 | 386.372 | 388.308 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | chemical | HUN | BUY | 24 | 24 | 0.014592 | False |  | 9.12 | 2026-10-27 | 9.0972 | 9.1428 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | chemical | EMN | BUY | 3 | 3 | 0.013224 | False |  | 66.12 | 2026-10-27 | 65.9547 | 66.2853 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | chemical | CE | BUY | 4 | 4 | 0.012968 | False |  | 48.63 | 2026-10-27 | 48.5084 | 48.7516 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner\|refiner_slow | DINO | SELL | -1 | -1 | -0.007614 | False |  | 114.21 | 2026-10-27 | 113.924 | 114.496 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | chemical | AVNT | BUY | 3 | 3 | 0.008486 | False |  | 42.43 | 2026-10-27 | 42.3239 | 42.5361 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | bwt | ERO | SELL | -1 | -1 | -0.002168 | False |  | 32.52 | 2026-10-27 | 32.4387 | 32.6013 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | SPY | SELL | -1 | -1 | -0.0513107 | False |  | 769.66 | 2026-10-27 | 767.736 | 771.584 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XLE | SELL | -6 | -4 | -0.0181893 | True |  | 68.21 | 2026-10-27 | 68.0395 | 68.3805 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XME | BUY | 1 | 1 | 0.0067 | False |  | 100.5 | 2026-10-27 | 100.249 | 100.751 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |


## Strategy changes and allocation notes

- CL operator risk reduction effective target session 2026-10-23: chemical allocation reduced from 28% to 14%; psx_ref allocation reduced from 5% to 0% (suspended). At that decision, released 19 percentage points remained cash; no renormalization. Later dated decisions below supersede allocation details.
- At that decision other sleeves were unchanged. CL AUM $15,000 and legacy daily beta remain unchanged. CRO retains its own PSX leg and SPY-only hedge: clearing psx_ref does NOT mean flattening all account PSX. Recompute net stocks and component hedges.
- Chemical is halved BEFORE the existing 5% net single-name cap; previously capped names need not fall by exactly half. Allocation migration turnover is not a signal change.
- Chemical decision rationale: operator questioned the economic clarity of asymmetric exits plus renewing hold-21 and potential historical overfitting, not only recent losses. Rules are deterministic and unchanged; overfitting is a concern, not an established finding. Review parameter robustness, simpler exits, hedge/cost attribution and a 28% counterfactual before any restoration. See docs/cl_risk_reduction_2026-10-23.md.
- CURRENT CL risk override effective target session 2026-10-28 supersedes earlier allocations: chemical 14% -> 0% (suspended), refiner 5% -> 2.5%, refiner_slow 10% -> 5%. Released 21.5 percentage points stay cash; no renormalization. CL AUM remains $15,000.
- Chemical suspension reflects unresolved exit-rule economics pending chemical input/output commodity research; refiner reduction limits drawdown risk. Neither is proof of alpha failure or an optimized historical improvement. Notebook/research chemical remains 28%; no signal rules changed. Restoration requires renewed operator approval; no automatic restoration.
- psx_ref remains 0%; CRO remains 10% allocation with SPY-only hedging. Old/slow refiner retain SPY/XLE legacy DAILY beta; the slow basket sync is recorded below. Other books and AUM are unchanged. Do not flatten all PSX or remove shared ETF hedges independently of component targets.
- Refiner_slow notebook sync effective 2026-10-28: DK/DINO/PBF/PSX = 30/25/25/20%; CL momentum/vol gate uses carry_data CL m0_ret, not m1_ret; carry change uses ffill then diff(50). Slow allocation remains 5%, old refiner 2.5%; no fixed hold or smoothing. Earlier basket descriptions are superseded.
- Recompute component hedges and account-netted orders from actual inventories; allocation migration is separate from signal turnover. Stock execution caps may leave remaining positions for later sessions. See docs/cl_risk_reduction_2026-10-28.md.
- CRO (crack refiner-only) added effective 2026-10-06: 10% allocation from unused CL capacity. CL AUM remains $15,000; existing sleeve weights are NOT reduced or renormalized.
- CRO stocks: VLO/MPC/PSX = 30/40/30%; crack_03; signal lookback 30 sessions; volatility lookback 30 (minimum 20); no signal smoothing; balance=0.5 (maximum CRO stock gross 5% of CL AUM).
- CRO explicit hedge is SPY ONLY, not XLE. Preserve component hedge ownership when PSX overlaps existing sleeves; net single-name cap and execution constraints still apply.
- This addition is refiner-only CRO, NOT the refiner-producer CRP, refiner-VLCC CRV, or refiner-chemical CRC research strategies.
- CRO stock target state for this package: active. Flat CRO must not create reallocation trades under identical inputs.
- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.
- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.
- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.
## Beta method for 2026-10-28 — as-of 2026-10-27

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-10-28-m68fj3vk/cached/targets-cl/2026-10-28. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
