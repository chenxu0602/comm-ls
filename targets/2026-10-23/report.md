# Combined CL v4.3 + Metals + Agriculture targets: 2026-10-23

- Combined AUM: $22,000.00
- Total child turnover: 25.80% ($5,676.41)
- Stock child turnover (40% cap applies): 17.26%
- Hedge child turnover (uncapped): 8.54%
- Orders: 16
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Strategy changes and allocation notes

- Chemical decision rationale (recorded 2026-10-23): operator questioned the economic clarity of asymmetric exits plus renewing hold-21 and potential historical overfitting, not only recent losses. Rules are deterministic and unchanged; overfitting is a concern, not an established finding. Review parameter robustness, simpler exits, hedge/cost attribution and a 28% counterfactual before any restoration. See docs/cl_risk_reduction_2026-10-23.md.

- CL operator risk reduction effective target session 2026-10-23: chemical allocation reduced from 28% to 14%; psx_ref allocation reduced from 5% to 0% (suspended). Released 19 percentage points remain cash; no renormalization.
- Other sleeves, CL AUM $15,000 and legacy daily beta remain unchanged. CRO retains its own PSX leg and SPY-only hedge: clearing psx_ref does NOT mean flattening all account PSX. Recompute net stocks and component hedges.
- Chemical is halved BEFORE the existing 5% net single-name cap; previously capped names need not fall by exactly half. Allocation migration turnover is not a signal change.
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
| hedge | MOO | -6 | -2.22% | -5 | -1 | -6 | 0 | 81.26 |
| hedge | SPY | 2 | 6.95% | 4 | -2 | 2 | 0 | 763.96 |
| hedge | XLE | 4 | 1.23% | 8 | -4 | 4 | 0 | 67.57 |
| hedge | XME | 2 | 0.88% | 2 | 0 | 2 | 0 | 96.59 |
| stock | ADM | 3 | 1.09% | 3 | 0 | 3 | 0 | 79.84 |
| stock | AVNT | -3 | -0.55% | -5 | 2 | -3 | 0 | 40.58 |
| stock | BG | 2 | 0.94% | 2 | 0 | 2 | 0 | 103.15 |
| stock | BHP | -5 | -1.76% | -5 | 0 | -5 | 0 | 77.58 |
| stock | CE | -4 | -0.86% | -9 | 5 | -4 | 0 | 47.22 |
| stock | DINO | 2 | 1.11% | 2 | 0 | 2 | 0 | 122.32 |
| stock | DK | 10 | 3.45% | 10 | 0 | 10 | 0 | 75.79 |
| stock | DOW | -13 | -1.88% | -24 | 11 | -13 | 0 | 31.81 |
| stock | EMN | -3 | -0.89% | -7 | 4 | -3 | 0 | 65.31 |
| stock | ERO | 22 | 3.01% | 20 | 2 | 22 | 0 | 30.13 |
| stock | FSUGY | -12 | -1.10% | -12 | 0 | -12 | 0 | 20.21 |
| stock | FTI | -4 | -1.21% | -4 | 0 | -4 | 0 | 66.82 |
| stock | HAL | -5 | -0.75% | -4 | 0 | -4 | -1 | 33.19 |
| stock | HUN | -24 | -0.95% | -52 | 28 | -24 | 0 | 8.72 |
| stock | LYB | -8 | -2.38% | -12 | 4 | -8 | 0 | 65.37 |
| stock | MPC | -1 | -2.09% | 0 | -1 | -1 | 0 | 459.28 |
| stock | PBF | 6 | 2.16% | 6 | 0 | 6 | 0 | 79.25 |
| stock | PSX | -1 | -1.29% | 3 | -3 | 0 | -1 | 284.63 |
| stock | RIO | -3 | -1.15% | -3 | 0 | -3 | 0 | 84.14 |
| stock | SCCO | -3 | -2.50% | -2 | -1 | -3 | 0 | 183.59 |
| stock | SLB | -6 | -1.35% | -6 | 0 | -6 | 0 | 49.55 |
| stock | TECK | 4 | 1.07% | 3 | 1 | 4 | 0 | 58.90 |
| stock | VALE | -10 | -0.55% | -9.8 | 0 | -9.8 | -0.2 | 12.20 |
| stock | VLO | -1 | -1.94% | 0 | -1 | -1 | 0 | 426.28 |
| stock | WLK | -7 | -2.04% | -12 | 5 | -7 | 0 | 64.14 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AVNT | BUY | 2.0 | -5.0 | -3.0 | 40.48 | 40.68 | 1 |
| CE | BUY | 5.0 | -9.0 | -4.0 | 47.1 | 47.34 | 1 |
| DOW | BUY | 11.0 | -24.0 | -13.0 | 31.73 | 31.89 | 1 |
| EMN | BUY | 4.0 | -7.0 | -3.0 | 65.15 | 65.47 | 1 |
| ERO | BUY | 2.0 | 20.0 | 22.0 | 30.05 | 30.21 | 1 |
| HUN | BUY | 28.0 | -52.0 | -24.0 | 8.7 | 8.74 | 1 |
| LYB | BUY | 4.0 | -12.0 | -8.0 | 65.21 | 65.53 | 1 |
| MPC | SELL | -1.0 | 0.0 | -1.0 | 460.43 | 458.13 | 1 |
| PSX | SELL | -3.0 | 3.0 | 0.0 | 285.34 | 283.92 | 1 |
| SCCO | SELL | -1.0 | -2.0 | -3.0 | 184.05 | 183.13 | 1 |
| TECK | BUY | 1.0 | 3.0 | 4.0 | 58.75 | 59.05 | 1 |
| VLO | SELL | -1.0 | 0.0 | -1.0 | 427.35 | 425.21 | 1 |
| WLK | BUY | 5.0 | -12.0 | -7.0 | 63.98 | 64.3 | 1 |
| MOO | SELL | -1.0 | -5.0 | -6.0 | 81.46 | 81.06 | 2 |
| SPY | SELL | -2.0 | 4.0 | 2.0 | 765.87 | 762.05 | 2 |
| XLE | SELL | -4.0 | 8.0 | 4.0 | 67.74 | 67.4 | 2 |

## Beta method for 2026-10-23 — as-of 2026-10-22

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-10-23-syg5sij3/cached/targets/2026-10-23. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
