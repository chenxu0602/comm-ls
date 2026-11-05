# Combined CL v4.3 + Metals + Agriculture targets: 2026-10-28

- Combined AUM: $22,000.00
- Total child turnover: 24.45% ($5,380.08)
- Stock child turnover (40% cap applies): 19.26%
- Hedge child turnover (uncapped): 5.20%
- Orders: 18
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

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
- Agriculture v4.3 joined the main account effective 2026-10-02: $2,000 allocated AUM. Idle allocation remains cash and still counts in account AUM.
- Agriculture uses component-specific hedges: crush_vol/crush_vol2/adm_bg2 use SPY + MOO; adm_bg/adm_tsn/bg_tsn use SPY only. Keep its virtual book separate.
- Agriculture stock target state for this package: active. This is not a permanent suspension.
- CRO (crack refiner-only) added effective 2026-10-06: 10% allocation from unused CL capacity. CL AUM remains $15,000; existing sleeve weights are NOT reduced or renormalized.
- CRO stocks: VLO/MPC/PSX = 30/40/30%; crack_03; signal lookback 30 sessions; volatility lookback 30 (minimum 20); no signal smoothing; balance=0.5 (maximum CRO stock gross 5% of CL AUM).
- CRO explicit hedge is SPY ONLY, not XLE. Preserve component hedge ownership when PSX overlaps existing sleeves; net single-name cap and execution constraints still apply.
- This addition is refiner-only CRO, NOT the refiner-producer CRP, refiner-VLCC CRV, or refiner-chemical CRC research strategies.
- CRO stock target state for this package: active. Flat CRO must not create reallocation trades under identical inputs.
- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.
- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.
- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | MOO | -2 | -0.73% | -2 | 0 | -2 | 0 | 80.83 |
| hedge | SPY | 1 | 3.50% | 2 | -1 | 1 | 0 | 769.66 |
| hedge | XLE | 0 | 0.00% | 4 | -4 | 0 | 0 | 68.21 |
| hedge | XME | 2 | 0.91% | 1 | 1 | 2 | 0 | 100.50 |
| stock | ADM | 10 | 3.55% | 10 | 0 | 10 | 0 | 78.20 |
| stock | AVNT | 0 | 0.00% | -3 | 3 | 0 | 0 | 42.43 |
| stock | BG | -5 | -2.30% | -4 | -1 | -5 | 0 | 101.36 |
| stock | BHP | -5 | -1.88% | -5 | 0 | -5 | 0 | 82.60 |
| stock | CE | 0 | 0.00% | -4 | 4 | 0 | 0 | 48.63 |
| stock | DINO | 2 | 1.04% | 3 | -1 | 2 | 0 | 114.21 |
| stock | DK | 3 | 0.96% | 9 | -6 | 3 | 0 | 70.30 |
| stock | DOW | 0 | 0.00% | -13 | 13 | 0 | 0 | 33.78 |
| stock | EMN | 0 | 0.00% | -3 | 3 | 0 | 0 | 66.12 |
| stock | ERO | 21 | 3.10% | 22 | -1 | 21 | 0 | 32.52 |
| stock | FSUGY | -12 | -1.12% | -12 | 0 | -12 | 0 | 20.45 |
| stock | FTI | -4 | -1.30% | -4 | 0 | -4 | 0 | 71.38 |
| stock | HAL | -4 | -0.65% | -4 | 0 | -4 | 0 | 35.62 |
| stock | HUN | 0 | 0.00% | -24 | 24 | 0 | 0 | 9.12 |
| stock | LYB | 0 | 0.00% | -8 | 8 | 0 | 0 | 67.43 |
| stock | MPC | -1 | -1.98% | 0 | -1 | -1 | 0 | 435.98 |
| stock | PBF | 2 | 0.67% | 6 | -4 | 2 | 0 | 73.63 |
| stock | PSX | 0 | 0.00% | 1 | -1 | 0 | 0 | 268.53 |
| stock | RIO | -3 | -1.17% | -3 | 0 | -3 | 0 | 85.74 |
| stock | SCCO | -3 | -2.65% | -3 | 0 | -3 | 0 | 194.43 |
| stock | SLB | -6 | -1.47% | -6 | 0 | -6 | 0 | 54.08 |
| stock | TECK | 4 | 1.13% | 4 | 0 | 4 | 0 | 62.28 |
| stock | VALE | -11 | -0.59% | -9.8 | 0 | -9.8 | -1.2 | 11.84 |
| stock | VLO | -1 | -1.76% | 0 | -1 | -1 | 0 | 387.34 |
| stock | WLK | 0 | 0.00% | -7 | 7 | 0 | 0 | 66.17 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AVNT | BUY | 3.0 | -3.0 | 0.0 | 42.32 | 42.54 | 1 |
| BG | SELL | -1.0 | -4.0 | -5.0 | 101.61 | 101.11 | 1 |
| CE | BUY | 4.0 | -4.0 | 0.0 | 48.51 | 48.75 | 1 |
| DINO | SELL | -1.0 | 3.0 | 2.0 | 114.5 | 113.92 | 1 |
| DK | SELL | -6.0 | 9.0 | 3.0 | 70.48 | 70.12 | 1 |
| DOW | BUY | 13.0 | -13.0 | 0.0 | 33.7 | 33.86 | 1 |
| EMN | BUY | 3.0 | -3.0 | 0.0 | 65.95 | 66.29 | 1 |
| ERO | SELL | -1.0 | 22.0 | 21.0 | 32.6 | 32.44 | 1 |
| HUN | BUY | 24.0 | -24.0 | 0.0 | 9.1 | 9.14 | 1 |
| LYB | BUY | 8.0 | -8.0 | 0.0 | 67.26 | 67.6 | 1 |
| MPC | SELL | -1.0 | 0.0 | -1.0 | 437.07 | 434.89 | 1 |
| PBF | SELL | -4.0 | 6.0 | 2.0 | 73.81 | 73.45 | 1 |
| PSX | SELL | -1.0 | 1.0 | 0.0 | 269.2 | 267.86 | 1 |
| VLO | SELL | -1.0 | 0.0 | -1.0 | 388.31 | 386.37 | 1 |
| WLK | BUY | 7.0 | -7.0 | 0.0 | 66.0 | 66.34 | 1 |
| SPY | SELL | -1.0 | 2.0 | 1.0 | 771.58 | 767.74 | 2 |
| XLE | SELL | -4.0 | 4.0 | 0.0 | 68.38 | 68.04 | 2 |
| XME | BUY | 1.0 | 1.0 | 2.0 | 100.25 | 100.75 | 2 |

## Beta method for 2026-10-28 — as-of 2026-10-27

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-10-28-m68fj3vk/cached/targets/2026-10-28. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
