# Combined CL v4.3 + Metals + Agriculture targets: 2026-11-02

- Combined AUM: $22,000.00
- Total child turnover: 27.12% ($5,966.24)
- Stock child turnover (40% cap applies): 17.26%
- Hedge child turnover (uncapped): 9.86%
- Orders: 13
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Strategy changes and allocation notes

- CL operator risk reduction effective target session 2026-10-23: chemical allocation reduced from 28% to 14%; psx_ref allocation reduced from 5% to 0% (suspended). At that decision, released 19 percentage points remained cash; no renormalization. Later dated decisions below supersede allocation details.
- At that decision other sleeves were unchanged. CL AUM $15,000 and legacy daily beta remain unchanged. CRO retains its own PSX leg and SPY-only hedge: clearing psx_ref does NOT mean flattening all account PSX. Recompute net stocks and component hedges.
- Chemical is halved BEFORE the existing 5% net single-name cap; previously capped names need not fall by exactly half. Allocation migration turnover is not a signal change.
- Chemical decision rationale: operator questioned the economic clarity of asymmetric exits plus renewing hold-21 and potential historical overfitting, not only recent losses. Rules are deterministic and unchanged; overfitting is a concern, not an established finding. Review parameter robustness, simpler exits, hedge/cost attribution and a 28% counterfactual before any restoration. See docs/cl_risk_reduction_2026-10-23.md.
- Agriculture v4.3 joined the main account effective 2026-10-02: $2,000 allocated AUM. Idle allocation remains cash and still counts in account AUM.
- Agriculture uses component-specific hedges: crush_vol/crush_vol2/adm_bg2 use SPY + MOO; adm_bg/adm_tsn/bg_tsn use SPY only. Keep its virtual book separate.
- Agriculture stock target state for this package: active. This is not a permanent suspension.
- CURRENT CL from 2026-11-02: chemical 0% (25% research dummy is NOT live), shipping 20%, refiner 3%, refiner_slow/re_slow 10%, services 20%, bwt 2%, re_c03 20%, others including CRO 0%. Budget 75%; no renormalization; all book AUMs unchanged.
- re_c03 replaces CRO: DINO/MPC/VLO 20/30/50%, full balance, quarterly near MA3-MA30 entry, far change5 exit, far std30 thresholds. SPY + XLE legacy DAILY hedges; old CRO half-balance/SPY-only retired.
- Refiner DK/DINO/PBF 30/40/30%; slow DK/DINO/PBF 40/30/30%, HO m1 momentum gate and carry ffill.diff50. Other algorithms unchanged. Track allocation/hedge migration separately. See docs/cl_reallocation_2026-11-02.md.
- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.
- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.
- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | MOO | -2 | -0.75% | -2 | 0 | -2 | 0 | 81.98 |
| hedge | SPY | 3 | 10.31% | 1 | 2 | 3 | 0 | 755.72 |
| hedge | XLE | 0 | 0.00% | -1 | 1 | 0 | 0 | 70.02 |
| hedge | XME | 8 | 3.56% | 2 | 6 | 8 | 0 | 97.82 |
| stock | ADM | 10 | 3.50% | 10 | 0 | 10 | 0 | 76.91 |
| stock | BG | -5 | -2.20% | -5 | 0 | -5 | 0 | 96.64 |
| stock | BHP | -5 | -1.80% | -5 | 0 | -5 | 0 | 79.16 |
| stock | DINO | -1 | -0.52% | 2 | -2 | 0 | -1 | 115.00 |
| stock | DK | 9 | 3.01% | 3 | 6 | 9 | 0 | 73.57 |
| stock | ERO | 8 | 1.06% | 22 | -14 | 8 | 0 | 29.05 |
| stock | FSUGY | -12 | -1.09% | -12 | 0 | -12 | 0 | 20.02 |
| stock | FTI | -11 | -3.44% | -4 | -7 | -11 | 0 | 68.77 |
| stock | HAL | -17 | -2.79% | -4 | -13 | -17 | 0 | 36.17 |
| stock | MPC | -2 | -4.04% | -1 | -1 | -2 | 0 | 444.73 |
| stock | PBF | 6 | 2.13% | 2 | 4 | 6 | 0 | 78.00 |
| stock | RIO | -3 | -1.12% | -3 | 0 | -3 | 0 | 81.89 |
| stock | SCCO | -3 | -2.42% | -3 | 0 | -3 | 0 | 177.53 |
| stock | SLB | -14 | -3.42% | -6 | -8 | -14 | 0 | 53.74 |
| stock | TECK | 1 | 0.28% | 4 | -3 | 1 | 0 | 60.61 |
| stock | VALE | -11 | -0.57% | -10.8 | 0 | -10.8 | -0.2 | 11.39 |
| stock | VLO | -2 | -3.63% | -1 | -1 | -2 | 0 | 399.66 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DINO | SELL | -2.0 | 2.0 | 0.0 | 115.29 | 114.71 | 1 |
| DK | BUY | 6.0 | 3.0 | 9.0 | 73.39 | 73.75 | 1 |
| ERO | SELL | -14.0 | 22.0 | 8.0 | 29.12 | 28.98 | 1 |
| FTI | SELL | -7.0 | -4.0 | -11.0 | 68.94 | 68.6 | 1 |
| HAL | SELL | -13.0 | -4.0 | -17.0 | 36.26 | 36.08 | 1 |
| MPC | SELL | -1.0 | -1.0 | -2.0 | 445.84 | 443.62 | 1 |
| PBF | BUY | 4.0 | 2.0 | 6.0 | 77.81 | 78.19 | 1 |
| SLB | SELL | -8.0 | -6.0 | -14.0 | 53.87 | 53.61 | 1 |
| TECK | SELL | -3.0 | 4.0 | 1.0 | 60.76 | 60.46 | 1 |
| VLO | SELL | -1.0 | -1.0 | -2.0 | 400.66 | 398.66 | 1 |
| SPY | BUY | 2.0 | 1.0 | 3.0 | 753.83 | 757.61 | 2 |
| XLE | BUY | 1.0 | -1.0 | 0.0 | 69.84 | 70.2 | 2 |
| XME | BUY | 6.0 | 2.0 | 8.0 | 97.58 | 98.06 | 2 |

## Beta method for 2026-11-02 — as-of 2026-10-30

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-11-02-w9zewr1_/cached/targets/2026-11-02. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
