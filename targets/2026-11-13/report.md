# Combined CL v4.3 + Metals + Agriculture targets: 2026-11-13

- Combined AUM: $22,000.00
- Total child turnover: 12.24% ($2,692.04)
- Stock child turnover (40% cap applies): 7.33%
- Hedge child turnover (uncapped): 4.90%
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
| hedge | SPY | 0 | 0.00% | -1 | 1 | 0 | 0 | 757.12 |
| hedge | XLE | 39 | 11.40% | 34 | 5 | 39 | 0 | 64.33 |
| hedge | XME | -21 | -9.09% | -21 | 0 | -21 | 0 | 95.25 |
| stock | BHP | 7 | 2.56% | 7 | 0 | 7 | 0 | 80.51 |
| stock | CE | -13 | -3.03% | -13 | 0 | -13 | 0 | 51.26 |
| stock | DHT | 10 | 1.01% | 22 | -12 | 10 | 0 | 22.28 |
| stock | DINO | 2 | 0.93% | 5 | -3 | 2 | 0 | 102.15 |
| stock | DK | 9 | 2.80% | 9 | 0 | 9 | 0 | 68.41 |
| stock | DOW | -20 | -3.01% | -21 | 0 | -21 | 1 | 33.15 |
| stock | ERO | 8 | 1.08% | 8 | 0 | 8 | 0 | 29.76 |
| stock | FRO | 5 | 1.06% | 10 | -5 | 5 | 0 | 46.76 |
| stock | FSUGY | 16 | 1.48% | 0 | 16 | 16 | 0 | 20.29 |
| stock | FTI | -9 | -2.66% | -9 | 0 | -9 | 0 | 64.92 |
| stock | HAL | -9 | -1.34% | -9 | 0 | -9 | 0 | 32.76 |
| stock | INSW | 1 | 0.48% | 3 | -2 | 1 | 0 | 104.65 |
| stock | LYB | -11 | -3.19% | -11 | 0 | -11 | 0 | 63.88 |
| stock | MPC | -2 | -3.75% | -2 | 0 | -2 | 0 | 412.85 |
| stock | PBF | 3 | 0.97% | 3 | 0 | 3 | 0 | 70.96 |
| stock | PSX | -1 | -1.20% | -1 | 0 | -1 | 0 | 262.91 |
| stock | RIO | 7 | 2.65% | 7 | 0 | 7 | 0 | 83.28 |
| stock | SCCO | 4 | 3.06% | 4 | 0 | 4 | 0 | 168.21 |
| stock | SLB | -12 | -2.78% | -12 | 0 | -12 | 0 | 50.91 |
| stock | STNG | 0 | 0.00% | 1 | -1 | 0 | 0 | 83.44 |
| stock | TECK | 1 | 0.28% | 1 | 0 | 1 | 0 | 61.19 |
| stock | TNK | 1 | 0.40% | 3 | -2 | 1 | 0 | 88.50 |
| stock | VALE | 53 | 2.72% | 52 | 1 | 53 | 0 | 11.28 |
| stock | VLO | -2 | -3.41% | -2 | 0 | -2 | 0 | 374.95 |
| stock | WLK | -4 | -1.14% | -4 | 0 | -4 | 0 | 62.78 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DHT | SELL | -12.0 | 22.0 | 10.0 | 22.34 | 22.22 | 1 |
| DINO | SELL | -3.0 | 5.0 | 2.0 | 102.41 | 101.89 | 1 |
| FRO | SELL | -5.0 | 10.0 | 5.0 | 46.88 | 46.64 | 1 |
| FSUGY | BUY | 16.0 | 0.0 | 16.0 | 20.24 | 20.34 | 1 |
| INSW | SELL | -2.0 | 3.0 | 1.0 | 104.91 | 104.39 | 1 |
| STNG | SELL | -1.0 | 1.0 | 0.0 | 83.65 | 83.23 | 1 |
| TNK | SELL | -2.0 | 3.0 | 1.0 | 88.72 | 88.28 | 1 |
| VALE | BUY | 1.0 | 52.0 | 53.0 | 11.25 | 11.31 | 1 |
| SPY | BUY | 1.0 | -1.0 | 0.0 | 755.23 | 759.01 | 2 |
| XLE | BUY | 5.0 | 34.0 | 39.0 | 64.17 | 64.49 | 2 |

## Beta method for 2026-11-13 — as-of 2026-11-12

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-11-13-i3tt0ifh/cached/targets/2026-11-13. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
