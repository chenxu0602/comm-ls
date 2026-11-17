# Combined CL v4.3 + Metals + Agriculture targets: 2026-11-16

- Combined AUM: $22,000.00
- Total child turnover: 5.38% ($1,183.70)
- Stock child turnover (40% cap applies): 4.20%
- Hedge child turnover (uncapped): 1.18%
- Orders: 8
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Strategy changes and allocation notes

- Metals reweight from target2026-11-16: hg_gc_gap15/accel20/SCO-vol25/copper15/miners25%; alloys0 and notebook-only hg_gc_gap_gc_carry_iron_2=0. Nominal100%, no normalization; copper10->15 uses the previously idle5pp. AUM5000, legacy DAILY SPY+XME hedges, signal rules,12% name cap and execution controls unchanged. See docs/metals_reweight_2026-11-16.md.
- CL operator risk reduction effective target session 2026-10-23: chemical allocation reduced from 28% to 14%; psx_ref allocation reduced from 5% to 0% (suspended). At that decision, released 19 percentage points remained cash; no renormalization. Later dated decisions below supersede allocation details.
- At that decision other sleeves were unchanged. CL AUM $15,000 and legacy daily beta remain unchanged. CRO retains its own PSX leg and SPY-only hedge: clearing psx_ref does NOT mean flattening all account PSX. Recompute net stocks and component hedges.
- Chemical is halved BEFORE the existing 5% net single-name cap; previously capped names need not fall by exactly half. Allocation migration turnover is not a signal change.
- Chemical decision rationale: operator questioned the economic clarity of asymmetric exits plus renewing hold-21 and potential historical overfitting, not only recent losses. Rules are deterministic and unchanged; overfitting is a concern, not an established finding. Review parameter robustness, simpler exits, hedge/cost attribution and a 28% counterfactual before any restoration. See docs/cl_risk_reduction_2026-10-23.md.
- Agriculture v4.3 joined the main account effective 2026-10-02: $2,000 allocated AUM. Idle allocation remains cash and still counts in account AUM.
- Agriculture uses component-specific hedges: narrow-sector residual sleeves use SPY + MOO for ADM/BG; adm_bg/adm_tsn/bg_tsn use SPY only. Keep its virtual book separate.
- Agriculture stock target state for this package: flat. This is not a permanent suspension.
- Agriculture notebook basket weights: crush_vol ADM60/BG40; crush_vol2 ADM70/BG30; crush_vol3 ADM100; adm_tsn equal/opposite ADM/TSN. Each sleeve allocation25%, no extra normalization.
- ADM/TSN rule and allocation sync from 2026-11-16: crush_02 momentum with ADM-minus-TSN adjusted-price distance entry gates; equal/opposite dollar legs, no rolling pair-beta sizing. Operator allocation25% (previously15%); crush_vol25/crush_vol2 25%/ADM-only crush_vol3 25%, adm_bg/adm_bg2/bg_tsn0. Nominal100%, no normalization; AUM2000 unchanged. crush_vol3 uses adjusted_zs volatility with MA50 entry constraints and SPY + MOO explicit hedges. See docs/agri_crush_vol3_sync_2026-11-16.md.
- CURRENT FINAL CL from 2026-11-09: operator chemical20->15%, services20->10%, shipping STAYS10% (initial20% package superseded before execution); refiner3/slow8/bwt2/CRO20/re_c03 10% unchanged. Nominal budget78%, no normalization. AUM and legacy DAILY beta unchanged.
- Rules unchanged: chemical hold2 and L/PP exits; slow HO m1 gate carry_data_2; CRO half-balance SPY-only, re_c03 SPY+XLE. Track allocation migration separately from signal changes. See docs/cl_reweight_2026-11-09.md.
- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.
- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.
- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | XLE | 43 | 12.70% | 39 | 4 | 43 | 0 | 64.96 |
| hedge | XME | -21 | -8.95% | -21 | 0 | -21 | 0 | 93.74 |
| stock | BHP | 8 | 2.89% | 7 | 1 | 8 | 0 | 79.49 |
| stock | CE | -13 | -3.04% | -13 | 0 | -13 | 0 | 51.41 |
| stock | DHT | 0 | 0.00% | 10 | -10 | 0 | 0 | 22.25 |
| stock | DINO | 2 | 0.93% | 2 | 0 | 2 | 0 | 102.18 |
| stock | DK | 9 | 2.80% | 9 | 0 | 9 | 0 | 68.50 |
| stock | DOW | -20 | -3.00% | -21 | 0 | -21 | 1 | 33.04 |
| stock | ERO | 8 | 1.06% | 8 | 0 | 8 | 0 | 29.06 |
| stock | FRO | 0 | 0.00% | 5 | -5 | 0 | 0 | 46.97 |
| stock | FSUGY | 12 | 1.09% | 16 | -4 | 12 | 0 | 20.04 |
| stock | FTI | -9 | -2.71% | -9 | 0 | -9 | 0 | 66.26 |
| stock | HAL | -9 | -1.38% | -9 | 0 | -9 | 0 | 33.78 |
| stock | INSW | 0 | 0.00% | 1 | -1 | 0 | 0 | 105.23 |
| stock | LYB | -10 | -2.93% | -11 | 0 | -11 | 1 | 64.43 |
| stock | MPC | -2 | -3.77% | -2 | 0 | -2 | 0 | 414.65 |
| stock | PBF | 3 | 0.97% | 3 | 0 | 3 | 0 | 71.28 |
| stock | PSX | -1 | -1.20% | -1 | 0 | -1 | 0 | 264.90 |
| stock | RIO | 7 | 2.64% | 7 | 0 | 7 | 0 | 82.95 |
| stock | SCCO | 4 | 2.98% | 4 | 0 | 4 | 0 | 164.08 |
| stock | SLB | -12 | -2.82% | -12 | 0 | -12 | 0 | 51.67 |
| stock | TECK | 1 | 0.27% | 1 | 0 | 1 | 0 | 60.19 |
| stock | TNK | 0 | 0.00% | 1 | -1 | 0 | 0 | 89.43 |
| stock | VALE | 42 | 2.14% | 52 | -10 | 42 | 0 | 11.22 |
| stock | VLO | -2 | -3.45% | -2 | 0 | -2 | 0 | 379.83 |
| stock | WLK | -4 | -1.16% | -4 | 0 | -4 | 0 | 63.61 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BHP | BUY | 1.0 | 7.0 | 8.0 | 79.29 | 79.69 | 1 |
| DHT | SELL | -10.0 | 10.0 | 0.0 | 22.31 | 22.19 | 1 |
| FRO | SELL | -5.0 | 5.0 | 0.0 | 47.09 | 46.85 | 1 |
| FSUGY | SELL | -4.0 | 16.0 | 12.0 | 20.09 | 19.99 | 1 |
| INSW | SELL | -1.0 | 1.0 | 0.0 | 105.49 | 104.97 | 1 |
| TNK | SELL | -1.0 | 1.0 | 0.0 | 89.65 | 89.21 | 1 |
| VALE | SELL | -10.0 | 52.0 | 42.0 | 11.25 | 11.19 | 1 |
| XLE | BUY | 4.0 | 39.0 | 43.0 | 64.8 | 65.12 | 2 |

## Beta method for 2026-11-16 — as-of 2026-11-13

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-11-16-unv2y3l0/cached/targets/2026-11-16. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
