# Combined CL v4.3 + Metals + Agriculture targets: 2026-11-04

- Combined AUM: $22,000.00
- Total child turnover: 18.80% ($4,135.47)
- Stock child turnover (40% cap applies): 9.31%
- Hedge child turnover (uncapped): 9.49%
- Orders: 10
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
- CURRENT CL from 2026-11-04: chemical20/shipping20/refiner3/refiner_slow8/services20/bwt2/CRO20/re_c03 10%; nominal budget103%, no renormalization. AUM and legacy DAILY beta unchanged.
- CRO restored alongside re_c03, not CRP: VLO/MPC/PSX/PBF=30/20/20/20%, basket total90%, half-balance, SPY-only. Idle basket capacity is preserved. re_c03 retains SPY+XLE hedging.
- Chemical re-enabled by operator: DOW/LYB/WLK/CE 30/30/10/30%, CL carry entry, L and PP own-vol exits, hold2, SPY+XLE. Current flat signal is not a permanent pause; future signals may open positions. See docs/cl_chemical_lp_2026-11-04.md.
- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.
- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.
- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | MOO | -2 | -0.74% | -2 | 0 | -2 | 0 | 81.74 |
| hedge | SPY | 1 | 3.43% | 2 | -1 | 1 | 0 | 754.35 |
| hedge | XLE | 5 | 1.52% | 25 | -20 | 5 | 0 | 66.68 |
| hedge | XME | 8 | 3.52% | 8 | 0 | 8 | 0 | 96.76 |
| stock | ADM | 11 | 3.53% | 11 | 0 | 11 | 0 | 70.60 |
| stock | BG | -5 | -2.15% | -5 | 0 | -5 | 0 | 94.72 |
| stock | BHP | -5 | -1.78% | -5 | 0 | -5 | 0 | 78.13 |
| stock | DHT | 31 | 3.37% | 19 | 12 | 31 | 0 | 23.92 |
| stock | DINO | 2 | 1.03% | 0 | 2 | 2 | 0 | 113.36 |
| stock | DK | 9 | 2.90% | 9 | 0 | 9 | 0 | 70.85 |
| stock | ERO | 7 | 0.97% | 8 | 0 | 8 | -1 | 30.44 |
| stock | FRO | 14 | 3.34% | 9 | 5 | 14 | 0 | 52.45 |
| stock | FSUGY | -13 | -1.17% | -12 | 0 | -12 | -1 | 19.88 |
| stock | FTI | -11 | -3.34% | -11 | 0 | -11 | 0 | 66.74 |
| stock | HAL | -18 | -2.79% | -17 | 0 | -17 | -1 | 34.07 |
| stock | INSW | 6 | 2.86% | 3 | 3 | 6 | 0 | 104.75 |
| stock | MPC | -2 | -3.88% | -2 | 0 | -2 | 0 | 427.34 |
| stock | PBF | 3 | 1.06% | 7 | -4 | 3 | 0 | 77.81 |
| stock | PSX | -1 | -1.24% | 0 | -1 | -1 | 0 | 271.94 |
| stock | RIO | -3 | -1.11% | -3 | 0 | -3 | 0 | 81.62 |
| stock | SCCO | -3 | -2.37% | -3.0318 | 0 | -3.0318 | 0.0318 | 173.49 |
| stock | SLB | -14 | -3.32% | -14 | 0 | -14 | 0 | 52.13 |
| stock | STNG | 2 | 0.79% | 1 | 1 | 2 | 0 | 87.34 |
| stock | TECK | 1 | 0.28% | 1 | 0 | 1 | 0 | 61.81 |
| stock | TNK | 5 | 2.17% | 2 | 3 | 5 | 0 | 95.58 |
| stock | VALE | -11 | -0.55% | -10.8 | 0 | -10.8 | -0.2 | 10.98 |
| stock | VLO | -2 | -3.52% | -2 | 0 | -2 | 0 | 387.65 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DHT | BUY | 12.0 | 19.0 | 31.0 | 23.86 | 23.98 | 1 |
| DINO | BUY | 2.0 | 0.0 | 2.0 | 113.08 | 113.64 | 1 |
| FRO | BUY | 5.0 | 9.0 | 14.0 | 52.32 | 52.58 | 1 |
| INSW | BUY | 3.0 | 3.0 | 6.0 | 104.49 | 105.01 | 1 |
| PBF | SELL | -4.0 | 7.0 | 3.0 | 78.0 | 77.62 | 1 |
| PSX | SELL | -1.0 | 0.0 | -1.0 | 272.62 | 271.26 | 1 |
| STNG | BUY | 1.0 | 1.0 | 2.0 | 87.12 | 87.56 | 1 |
| TNK | BUY | 3.0 | 2.0 | 5.0 | 95.34 | 95.82 | 1 |
| SPY | SELL | -1.0 | 2.0 | 1.0 | 756.24 | 752.46 | 2 |
| XLE | SELL | -20.0 | 25.0 | 5.0 | 66.85 | 66.51 | 2 |

## Beta method for 2026-11-04 — as-of 2026-11-03

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-11-04-wvcqr0yp/cached/targets/2026-11-04. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
