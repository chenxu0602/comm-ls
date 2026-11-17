# Combined CL v4.3 + Metals + Agriculture targets: 2026-11-09

- Combined AUM: $22,000.00
- Total child turnover: 31.94% ($7,026.99)
- Stock child turnover (40% cap applies): 19.48%
- Hedge child turnover (uncapped): 12.46%
- Orders: 17
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
| hedge | MOO | 0 | 0.00% | -2 | 0 | -2 | 2 | 82.12 |
| hedge | SPY | 0 | 0.00% | 1 | -1 | 0 | 0 | 735.29 |
| hedge | XLE | 33 | 9.24% | 5 | 28 | 33 | 0 | 61.62 |
| hedge | XME | -3 | -1.27% | 0 | -3 | -3 | 0 | 93.45 |
| stock | ADM | 0 | 0.00% | 11 | -7 | 4 | -4 | 69.97 |
| stock | BG | 0 | 0.00% | -5 | 3 | -2 | 2 | 99.10 |
| stock | BHP | 4 | 1.45% | 0 | 4 | 4 | 0 | 79.89 |
| stock | CE | -15 | -3.17% | 0 | -15 | -15 | 0 | 46.49 |
| stock | DHT | 22 | 2.07% | 34 | -12 | 22 | 0 | 20.68 |
| stock | DINO | 2 | 0.88% | 2 | 0 | 2 | 0 | 97.18 |
| stock | DK | 10 | 2.91% | 10 | 0 | 10 | 0 | 63.95 |
| stock | DOW | -21 | -3.00% | 0 | -21 | -21 | 0 | 31.40 |
| stock | ERO | 8 | 1.05% | 8 | 0 | 8 | 0 | 28.86 |
| stock | FRO | 10 | 2.06% | 10 | 0 | 10 | 0 | 45.42 |
| stock | FSUGY | -12 | -1.14% | -12 | 0 | -12 | 0 | 20.91 |
| stock | FTI | -9 | -2.60% | -12 | 3 | -9 | 0 | 63.52 |
| stock | HAL | -9 | -1.30% | -18 | 9 | -9 | 0 | 31.84 |
| stock | INSW | 3 | 1.34% | 3 | 0 | 3 | 0 | 98.02 |
| stock | LYB | -11 | -3.04% | -12 | 1 | -11 | 0 | 60.72 |
| stock | MPC | -2 | -3.39% | -2 | 0 | -2 | 0 | 372.74 |
| stock | PBF | 3 | 0.92% | 3 | 0 | 3 | 0 | 67.27 |
| stock | PSX | -1 | -1.12% | -1 | 0 | -1 | 0 | 245.72 |
| stock | RIO | 6 | 2.28% | 0 | 6 | 6 | 0 | 83.73 |
| stock | SCCO | 1 | 0.76% | -0.0318 | 0.0318 | 0 | 1 | 167.27 |
| stock | SLB | -12 | -2.72% | -15 | 3 | -12 | 0 | 49.92 |
| stock | STNG | 1 | 0.37% | 1 | 0 | 1 | 0 | 80.76 |
| stock | TECK | 1 | 0.27% | 1 | 0 | 1 | 0 | 60.46 |
| stock | TNK | 3 | 1.17% | 3 | 0 | 3 | 0 | 85.71 |
| stock | VALE | 19 | 1.00% | -10.8 | 10.8 | 0 | 19 | 11.59 |
| stock | VLO | -2 | -3.15% | -2 | 0 | -2 | 0 | 346.45 |
| stock | WLK | -4 | -1.15% | 0 | -4 | -4 | 0 | 63.49 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ADM | SELL | -7.0 | 11.0 | 4.0 | 70.14 | 69.8 | 1 |
| BG | BUY | 3.0 | -5.0 | -2.0 | 98.85 | 99.35 | 1 |
| BHP | BUY | 4.0 | 0.0 | 4.0 | 79.69 | 80.09 | 1 |
| CE | SELL | -15.0 | 0.0 | -15.0 | 46.61 | 46.37 | 1 |
| DHT | SELL | -12.0 | 34.0 | 22.0 | 20.73 | 20.63 | 1 |
| DOW | SELL | -21.0 | 0.0 | -21.0 | 31.48 | 31.32 | 1 |
| FTI | BUY | 3.0 | -12.0 | -9.0 | 63.36 | 63.68 | 1 |
| HAL | BUY | 9.0 | -18.0 | -9.0 | 31.76 | 31.92 | 1 |
| LYB | BUY | 1.0 | -12.0 | -11.0 | 60.57 | 60.87 | 1 |
| RIO | BUY | 6.0 | 0.0 | 6.0 | 83.52 | 83.94 | 1 |
| SCCO | BUY | 0.0318 | -0.0318 | 0.0 | 166.85 | 167.69 | 1 |
| SLB | BUY | 3.0 | -15.0 | -12.0 | 49.8 | 50.04 | 1 |
| VALE | BUY | 10.8 | -10.8 | 0.0 | 11.56 | 11.62 | 1 |
| WLK | SELL | -4.0 | 0.0 | -4.0 | 63.65 | 63.33 | 1 |
| SPY | SELL | -1.0 | 1.0 | 0.0 | 737.13 | 733.45 | 2 |
| XLE | BUY | 28.0 | 5.0 | 33.0 | 61.47 | 61.77 | 2 |
| XME | SELL | -3.0 | 0.0 | -3.0 | 93.68 | 93.22 | 2 |

## Beta method for 2026-11-09 — as-of 2026-11-06

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-11-09-t7cxj9rr/cached/targets/2026-11-09. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
