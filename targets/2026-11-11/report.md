# Combined CL v4.3 + Metals + Agriculture targets: 2026-11-11

- Combined AUM: $22,000.00
- Total child turnover: 11.39% ($2,506.09)
- Stock child turnover (40% cap applies): 7.60%
- Hedge child turnover (uncapped): 3.80%
- Orders: 7
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
| hedge | SPY | -1 | -3.41% | -1 | 0 | -1 | 0 | 749.92 |
| hedge | XLE | 34 | 9.61% | 33 | 1 | 34 | 0 | 62.21 |
| hedge | XME | -21 | -9.22% | -13 | -8 | -21 | 0 | 96.60 |
| stock | BHP | 7 | 2.58% | 5 | 2 | 7 | 0 | 81.12 |
| stock | CE | -14 | -3.11% | -14 | 0 | -14 | 0 | 48.93 |
| stock | DHT | 22 | 2.08% | 22 | 0 | 22 | 0 | 20.81 |
| stock | DINO | 2 | 0.90% | 2 | 0 | 2 | 0 | 98.76 |
| stock | DK | 10 | 2.85% | 10 | 0 | 10 | 0 | 62.64 |
| stock | DOW | -21 | -3.00% | -21 | 0 | -21 | 0 | 31.48 |
| stock | ERO | 7 | 0.98% | 8 | 0 | 8 | -1 | 30.67 |
| stock | FRO | 10 | 1.99% | 10 | 0 | 10 | 0 | 43.87 |
| stock | FSUGY | 16 | 1.52% | 0 | 16 | 16 | 0 | 20.88 |
| stock | FTI | -9 | -2.64% | -9 | 0 | -9 | 0 | 64.55 |
| stock | HAL | -9 | -1.30% | -9 | 0 | -9 | 0 | 31.86 |
| stock | INSW | 3 | 1.34% | 3 | 0 | 3 | 0 | 98.25 |
| stock | LYB | -11 | -3.03% | -11 | 0 | -11 | 0 | 60.60 |
| stock | MPC | -2 | -3.54% | -2 | 0 | -2 | 0 | 389.55 |
| stock | PBF | 3 | 0.90% | 3 | 0 | 3 | 0 | 65.91 |
| stock | PSX | -1 | -1.14% | -1 | 0 | -1 | 0 | 250.70 |
| stock | RIO | 7 | 2.69% | 5 | 2 | 7 | 0 | 84.54 |
| stock | SCCO | 4 | 3.10% | 0 | 4 | 4 | 0 | 170.36 |
| stock | SLB | -12 | -2.72% | -12 | 0 | -12 | 0 | 49.90 |
| stock | STNG | 1 | 0.37% | 1 | 0 | 1 | 0 | 80.55 |
| stock | TECK | 1 | 0.29% | 1 | 0 | 1 | 0 | 62.85 |
| stock | TNK | 3 | 1.17% | 3 | 0 | 3 | 0 | 85.70 |
| stock | VALE | 52 | 2.74% | 24 | 28 | 52 | 0 | 11.58 |
| stock | VLO | -2 | -3.19% | -2 | 0 | -2 | 0 | 350.71 |
| stock | WLK | -4 | -1.15% | -4 | 0 | -4 | 0 | 63.16 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BHP | BUY | 2.0 | 5.0 | 7.0 | 80.92 | 81.32 | 1 |
| FSUGY | BUY | 16.0 | 0.0 | 16.0 | 20.83 | 20.93 | 1 |
| RIO | BUY | 2.0 | 5.0 | 7.0 | 84.33 | 84.75 | 1 |
| SCCO | BUY | 4.0 | 0.0 | 4.0 | 169.93 | 170.79 | 1 |
| VALE | BUY | 28.0 | 24.0 | 52.0 | 11.55 | 11.61 | 1 |
| XLE | BUY | 1.0 | 33.0 | 34.0 | 62.05 | 62.37 | 2 |
| XME | SELL | -8.0 | -13.0 | -21.0 | 96.84 | 96.36 | 2 |

## Beta method for 2026-11-11 — as-of 2026-11-10

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-11-11-qblrlzla/cached/targets/2026-11-11. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
