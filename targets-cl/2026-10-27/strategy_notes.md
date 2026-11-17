## Strategy changes and allocation notes

- CL operator risk reduction effective target session 2026-10-23: chemical allocation reduced from 28% to 14%; psx_ref allocation reduced from 5% to 0% (suspended). At that decision, released 19 percentage points remained cash; no renormalization. Later dated decisions below supersede allocation details.
- At that decision other sleeves were unchanged. CL AUM $15,000 and legacy daily beta remain unchanged. CRO retains its own PSX leg and SPY-only hedge: clearing psx_ref does NOT mean flattening all account PSX. Recompute net stocks and component hedges.
- Chemical is halved BEFORE the existing 5% net single-name cap; previously capped names need not fall by exactly half. Allocation migration turnover is not a signal change.
- Chemical decision rationale: operator questioned the economic clarity of asymmetric exits plus renewing hold-21 and potential historical overfitting, not only recent losses. Rules are deterministic and unchanged; overfitting is a concern, not an established finding. Review parameter robustness, simpler exits, hedge/cost attribution and a 28% counterfactual before any restoration. See docs/cl_risk_reduction_2026-10-23.md.
- APPROVED refiner blend effective target session 2026-10-26: refiner_slow 10% + refiner 5%; psx_ref remains suspended at 0%. This raises live combined refiner allocation from 10% to 15%, using 5 percentage points of idle capacity, not a change in CL AUM or automatic renormalization.
- refiner_slow basket DK/DINO/PBF/PSX = 30/20/30/20%; existing refiner DK/DINO/PBF = 50/20/30%. Both hedge with SPY + XLE using retained legacy DAILY beta. CRO remains separate and SPY-only; preserve component ownership before account netting.
- Slow rule: HO front_third_annualized_carry change over 50 stock observations; carry-level std 60/min30; entry 1.25 std, exit 0.95 std; CL m1 10-session return gate versus 0.5 times daily 20/min10 std. No fixed 10-day hold, no rolling-5 smoothing. Current input lookbacks and arrivals fail closed.
- Chemical remains TEMPORARILY 14% in production as an operator stop-loss-like risk-budget override; notebook/research remains 28%. Restoration requires a new operator decision after a clear risk reduction; no numeric trigger, date or automatic restoration is authorized. Do not return it to 28% as part of this refiner change.
- Full aligned refiner stock gross can reach 14.5% after the DK 5% net-name cap, before separate CRO. Size reduction or new sleeve orders caused by this change are allocation migration, not a new commodity signal. See docs/cl_refiner_blend_production_2026-10-26.md.
- CRO (crack refiner-only) added effective 2026-10-06: 10% allocation from unused CL capacity. CL AUM remains $15,000; existing sleeve weights are NOT reduced or renormalized.
- CRO stocks: VLO/MPC/PSX = 30/40/30%; crack_03; signal lookback 30 sessions; volatility lookback 30 (minimum 20); no signal smoothing; balance=0.5 (maximum CRO stock gross 5% of CL AUM).
- CRO explicit hedge is SPY ONLY, not XLE. Preserve component hedge ownership when PSX overlaps existing sleeves; net single-name cap and execution constraints still apply.
- This addition is refiner-only CRO, NOT the refiner-producer CRP, refiner-VLCC CRV, or refiner-chemical CRC research strategies.
- CRO stock target state for this package: flat. Flat CRO must not create reallocation trades under identical inputs.
- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.
- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.
- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.

## Beta method for 2026-10-27 — as-of 2026-10-26

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-10-27-1qtch3xl/cached/targets-cl/2026-10-27. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
