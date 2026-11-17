# Combined CL v4.3 + Metals + Agriculture targets: 2026-11-05

- Combined AUM: $22,000.00
- Total child turnover: 2.64% ($580.53)
- Stock child turnover (40% cap applies): 1.77%
- Hedge child turnover (uncapped): 0.87%
- Orders: 6
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
| hedge | MOO | -2 | -0.76% | -2 | 0 | -2 | 0 | 83.71 |
| hedge | SPY | 1 | 3.49% | 1 | 0 | 1 | 0 | 766.81 |
| hedge | XLE | 5 | 1.44% | 5 | 0 | 5 | 0 | 63.52 |
| hedge | XME | 6 | 2.61% | 8 | -2 | 6 | 0 | 95.78 |
| stock | ADM | 11 | 3.54% | 11 | 0 | 11 | 0 | 70.84 |
| stock | BG | -5 | -2.20% | -5 | 0 | -5 | 0 | 97.01 |
| stock | BHP | -5 | -1.82% | -5 | 0 | -5 | 0 | 80.14 |
| stock | DHT | 34 | 3.41% | 31 | 3 | 34 | 0 | 22.05 |
| stock | DINO | 2 | 0.95% | 2 | 0 | 2 | 0 | 104.57 |
| stock | DK | 9 | 2.68% | 9 | 0 | 9 | 0 | 65.46 |
| stock | ERO | 7 | 0.98% | 8 | 0 | 8 | -1 | 30.82 |
| stock | FRO | 15 | 3.31% | 14 | 1 | 15 | 0 | 48.48 |
| stock | FSUGY | -12 | -1.10% | -12 | 0 | -12 | 0 | 20.16 |
| stock | FTI | -12 | -3.52% | -11 | -1 | -12 | 0 | 64.50 |
| stock | HAL | -18 | -2.70% | -17 | -1 | -18 | 0 | 33.00 |
| stock | INSW | 6 | 2.71% | 6 | 0 | 6 | 0 | 99.36 |
| stock | MPC | -2 | -3.57% | -2 | 0 | -2 | 0 | 392.68 |
| stock | PBF | 3 | 0.99% | 3 | 0 | 3 | 0 | 72.62 |
| stock | PSX | -1 | -1.18% | -1 | 0 | -1 | 0 | 259.63 |
| stock | RIO | -3 | -1.15% | -3 | 0 | -3 | 0 | 84.56 |
| stock | SCCO | -2 | -1.61% | -3.0318 | 1 | -2.0318 | 0.0318 | 176.84 |
| stock | SLB | -15 | -3.52% | -14 | 0 | -14 | -1 | 51.56 |
| stock | STNG | 2 | 0.77% | 2 | 0 | 2 | 0 | 85.05 |
| stock | TECK | 1 | 0.29% | 1 | 0 | 1 | 0 | 64.46 |
| stock | TNK | 5 | 2.02% | 5 | 0 | 5 | 0 | 88.88 |
| stock | VALE | -11 | -0.57% | -10.8 | 0 | -10.8 | -0.2 | 11.43 |
| stock | VLO | -2 | -3.32% | -2 | 0 | -2 | 0 | 365.34 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DHT | BUY | 3.0 | 31.0 | 34.0 | 21.99 | 22.11 | 1 |
| FRO | BUY | 1.0 | 14.0 | 15.0 | 48.36 | 48.6 | 1 |
| FTI | SELL | -1.0 | -11.0 | -12.0 | 64.66 | 64.34 | 1 |
| HAL | SELL | -1.0 | -17.0 | -18.0 | 33.08 | 32.92 | 1 |
| SCCO | BUY | 1.0 | -3.0318 | -2.0318 | 176.4 | 177.28 | 1 |
| XME | SELL | -2.0 | 8.0 | 6.0 | 96.02 | 95.54 | 2 |

## Beta method for 2026-11-05 — as-of 2026-11-04

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-11-05-4_s52ks6/cached/targets/2026-11-05. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
