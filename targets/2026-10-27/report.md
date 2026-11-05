# Combined CL v4.3 + Metals + Agriculture targets: 2026-10-27

- Combined AUM: $22,000.00
- Total child turnover: 7.99% ($1,758.46)
- Stock child turnover (40% cap applies): 4.81%
- Hedge child turnover (uncapped): 3.18%
- Orders: 8
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

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
- Agriculture v4.3 joined the main account effective 2026-10-02: $2,000 allocated AUM. Idle allocation remains cash and still counts in account AUM.
- Agriculture uses component-specific hedges: crush_vol/crush_vol2/adm_bg2 use SPY + MOO; adm_bg/adm_tsn/bg_tsn use SPY only. Keep its virtual book separate.
- Agriculture stock target state for this package: active. This is not a permanent suspension.
- CRO (crack refiner-only) added effective 2026-10-06: 10% allocation from unused CL capacity. CL AUM remains $15,000; existing sleeve weights are NOT reduced or renormalized.
- CRO stocks: VLO/MPC/PSX = 30/40/30%; crack_03; signal lookback 30 sessions; volatility lookback 30 (minimum 20); no signal smoothing; balance=0.5 (maximum CRO stock gross 5% of CL AUM).
- CRO explicit hedge is SPY ONLY, not XLE. Preserve component hedge ownership when PSX overlaps existing sleeves; net single-name cap and execution constraints still apply.
- This addition is refiner-only CRO, NOT the refiner-producer CRP, refiner-VLCC CRV, or refiner-chemical CRC research strategies.
- CRO stock target state for this package: flat. Flat CRO must not create reallocation trades under identical inputs.
- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.
- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.
- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | MOO | -2 | -0.74% | -6 | 4 | -2 | 0 | 81.24 |
| hedge | SPY | 2 | 6.96% | 2 | 0 | 2 | 0 | 765.37 |
| hedge | XLE | 4 | 1.27% | 0 | 4 | 4 | 0 | 69.64 |
| hedge | XME | 1 | 0.44% | 2 | -1 | 1 | 0 | 96.01 |
| stock | ADM | 10 | 3.59% | 9 | 1 | 10 | 0 | 79.01 |
| stock | AVNT | -3 | -0.56% | -3 | 0 | -3 | 0 | 41.28 |
| stock | BG | -4 | -1.86% | 0 | -4 | -4 | 0 | 102.22 |
| stock | BHP | -5 | -1.80% | -5 | 0 | -5 | 0 | 79.13 |
| stock | CE | -4 | -0.87% | -4 | 0 | -4 | 0 | 48.08 |
| stock | DINO | 3 | 1.71% | 2 | 1 | 3 | 0 | 125.25 |
| stock | DK | 7 | 2.50% | 9 | -2 | 7 | 0 | 78.47 |
| stock | DOW | -12 | -1.85% | -13 | 0 | -13 | 1 | 33.99 |
| stock | EMN | -3 | -0.90% | -3 | 0 | -3 | 0 | 65.73 |
| stock | ERO | 22 | 3.12% | 22 | 0 | 22 | 0 | 31.21 |
| stock | FSUGY | -12 | -1.11% | -12 | 0 | -12 | 0 | 20.42 |
| stock | FTI | -4 | -1.28% | -4 | 0 | -4 | 0 | 70.41 |
| stock | HAL | -4 | -0.64% | -4 | 0 | -4 | 0 | 35.44 |
| stock | HUN | -24 | -0.97% | -24 | 0 | -24 | 0 | 8.89 |
| stock | LYB | -8 | -2.45% | -8 | 0 | -8 | 0 | 67.35 |
| stock | PBF | 6 | 2.20% | 6 | 0 | 6 | 0 | 80.55 |
| stock | PSX | 1 | 1.31% | 0 | 1 | 1 | 0 | 288.85 |
| stock | RIO | -3 | -1.14% | -3 | 0 | -3 | 0 | 83.72 |
| stock | SCCO | -3 | -2.54% | -3 | 0 | -3 | 0 | 186.01 |
| stock | SLB | -6 | -1.45% | -6 | 0 | -6 | 0 | 53.08 |
| stock | TECK | 4 | 1.10% | 4 | 0 | 4 | 0 | 60.26 |
| stock | VALE | -10 | -0.55% | -9.8 | 0 | -9.8 | -0.2 | 12.00 |
| stock | WLK | -6 | -1.78% | -7 | 0 | -7 | 1 | 65.31 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ADM | BUY | 1.0 | 9.0 | 10.0 | 78.81 | 79.21 | 1 |
| BG | SELL | -4.0 | 0.0 | -4.0 | 102.48 | 101.96 | 1 |
| DINO | BUY | 1.0 | 2.0 | 3.0 | 124.94 | 125.56 | 1 |
| DK | SELL | -2.0 | 9.0 | 7.0 | 78.67 | 78.27 | 1 |
| PSX | BUY | 1.0 | 0.0 | 1.0 | 288.13 | 289.57 | 1 |
| MOO | BUY | 4.0 | -6.0 | -2.0 | 81.04 | 81.44 | 2 |
| XLE | BUY | 4.0 | 0.0 | 4.0 | 69.47 | 69.81 | 2 |
| XME | SELL | -1.0 | 2.0 | 1.0 | 96.25 | 95.77 | 2 |

## Beta method for 2026-10-27 — as-of 2026-10-26

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-10-27-1qtch3xl/cached/targets/2026-10-27. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
