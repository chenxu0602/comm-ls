# Combined CL v4.3 + Metals + Agriculture targets: 2026-11-10

- Combined AUM: $22,000.00
- Total child turnover: 26.43% ($5,813.89)
- Stock child turnover (40% cap applies): 9.88%
- Hedge child turnover (uncapped): 16.55%
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
- Agriculture stock target state for this package: flat. This is not a permanent suspension.
- CURRENT FINAL CL from 2026-11-09: operator chemical20->15%, services20->10%, shipping STAYS10% (initial20% package superseded before execution); refiner3/slow8/bwt2/CRO20/re_c03 10% unchanged. Nominal budget78%, no normalization. AUM and legacy DAILY beta unchanged.
- Rules unchanged: chemical hold2 and L/PP exits; slow HO m1 gate carry_data_2; CRO half-balance SPY-only, re_c03 SPY+XLE. Track allocation migration separately from signal changes. See docs/cl_reweight_2026-11-09.md.
- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.
- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.
- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | MOO | 0 | 0.00% | -2 | 2 | 0 | 0 | 84.10 |
| hedge | SPY | -1 | -3.42% | 0 | -1 | -1 | 0 | 752.69 |
| hedge | XLE | 33 | 9.29% | 5 | 28 | 33 | 0 | 61.94 |
| hedge | XME | -13 | -5.83% | -3 | -10 | -13 | 0 | 98.58 |
| stock | ADM | 0 | 0.00% | 4 | -4 | 0 | 0 | 69.84 |
| stock | BG | 0 | 0.00% | -2 | 2 | 0 | 0 | 101.18 |
| stock | BHP | 7 | 2.64% | 0 | 5 | 5 | 2 | 82.86 |
| stock | CE | -14 | -3.10% | -15 | 1 | -14 | 0 | 48.75 |
| stock | DHT | 22 | 2.06% | 34 | -12 | 22 | 0 | 20.56 |
| stock | DINO | 2 | 0.91% | 2 | 0 | 2 | 0 | 99.76 |
| stock | DK | 9 | 2.66% | 10 | 0 | 10 | -1 | 65.00 |
| stock | DOW | -22 | -3.10% | -21 | 0 | -21 | -1 | 30.96 |
| stock | ERO | 7 | 1.00% | 8 | 0 | 8 | -1 | 31.32 |
| stock | FRO | 10 | 2.01% | 10 | 0 | 10 | 0 | 44.29 |
| stock | FSUGY | 15 | 1.46% | -12 | 12 | 0 | 15 | 21.38 |
| stock | FTI | -9 | -2.62% | -9 | 0 | -9 | 0 | 63.98 |
| stock | HAL | -9 | -1.30% | -9 | 0 | -9 | 0 | 31.88 |
| stock | INSW | 3 | 1.32% | 3 | 0 | 3 | 0 | 96.45 |
| stock | LYB | -11 | -2.97% | -11 | 0 | -11 | 0 | 59.50 |
| stock | MPC | -2 | -3.54% | -2 | 0 | -2 | 0 | 389.88 |
| stock | PBF | 3 | 0.95% | 3 | 0 | 3 | 0 | 69.55 |
| stock | PSX | -1 | -1.15% | -1 | 0 | -1 | 0 | 253.02 |
| stock | RIO | 7 | 2.75% | 0 | 5 | 5 | 2 | 86.39 |
| stock | SCCO | 3 | 2.40% | -0.0318 | 0.0318 | 0 | 3 | 176.02 |
| stock | SLB | -12 | -2.75% | -12 | 0 | -12 | 0 | 50.38 |
| stock | STNG | 1 | 0.36% | 1 | 0 | 1 | 0 | 79.62 |
| stock | TECK | 1 | 0.29% | 1 | 0 | 1 | 0 | 64.67 |
| stock | TNK | 3 | 1.16% | 3 | 0 | 3 | 0 | 85.12 |
| stock | VALE | 31 | 1.69% | 0 | 24 | 24 | 7 | 11.97 |
| stock | VLO | -2 | -3.24% | -2 | 0 | -2 | 0 | 356.75 |
| stock | WLK | -4 | -1.17% | -4 | 0 | -4 | 0 | 64.13 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ADM | SELL | -4.0 | 4.0 | 0.0 | 70.01 | 69.67 | 1 |
| BG | BUY | 2.0 | -2.0 | 0.0 | 100.93 | 101.43 | 1 |
| BHP | BUY | 5.0 | 0.0 | 5.0 | 82.65 | 83.07 | 1 |
| CE | BUY | 1.0 | -15.0 | -14.0 | 48.63 | 48.87 | 1 |
| DHT | SELL | -12.0 | 34.0 | 22.0 | 20.61 | 20.51 | 1 |
| FSUGY | BUY | 12.0 | -12.0 | 0.0 | 21.33 | 21.43 | 1 |
| RIO | BUY | 5.0 | 0.0 | 5.0 | 86.17 | 86.61 | 1 |
| SCCO | BUY | 0.0318 | -0.0318 | 0.0 | 175.58 | 176.46 | 1 |
| VALE | BUY | 24.0 | 0.0 | 24.0 | 11.94 | 12.0 | 1 |
| MOO | BUY | 2.0 | -2.0 | 0.0 | 83.89 | 84.31 | 2 |
| SPY | SELL | -1.0 | 0.0 | -1.0 | 754.57 | 750.81 | 2 |
| XLE | BUY | 28.0 | 5.0 | 33.0 | 61.79 | 62.09 | 2 |
| XME | SELL | -10.0 | -3.0 | -13.0 | 98.83 | 98.33 | 2 |

## Beta method for 2026-11-10 — as-of 2026-11-09

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-11-10-y3z13i_u/cached/targets/2026-11-10. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
