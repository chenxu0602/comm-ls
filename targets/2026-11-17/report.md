# Combined CL v4.3 + Metals + Agriculture targets: 2026-11-17

- Combined AUM: $22,000.00
- Total child turnover: 10.39% ($2,285.67)
- Stock child turnover (40% cap applies): 4.57%
- Hedge child turnover (uncapped): 5.82%
- Orders: 9
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Strategy changes and allocation notes

- Metals operator risk reduction from target2026-11-17: gap7.5/accel10/SCO-vol12.5/copper7.5/miners12.5%; all other sleeves0. Each Nov16 sleeve allocation halved before the unchanged12% name cap; nominal50%, released50% stays cash, no normalization or automatic restoration. AUM5000, signal rules, legacy DAILY SPY+XME hedges and execution controls unchanged. Recompute hedges from reduced stock targets and distinguish allocation migration from signal turnover. See docs/metals_risk_reduction_2026-11-17.md.
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
| hedge | SPY | 1 | 3.36% | 0 | 1 | 1 | 0 | 739.95 |
| hedge | XLE | 43 | 12.45% | 43 | 0 | 43 | 0 | 63.69 |
| hedge | XME | -15 | -6.13% | -21 | 6 | -15 | 0 | 89.91 |
| stock | BHP | 7 | 2.40% | 8 | -1 | 7 | 0 | 75.55 |
| stock | CE | -14 | -3.12% | -13 | -1 | -14 | 0 | 48.96 |
| stock | DINO | 2 | 0.90% | 2 | 0 | 2 | 0 | 99.05 |
| stock | DK | 9 | 2.77% | 9 | 0 | 9 | 0 | 67.82 |
| stock | DOW | -21 | -3.05% | -21 | 0 | -21 | 0 | 31.96 |
| stock | ERO | 8 | 0.99% | 8 | 0 | 8 | 0 | 27.33 |
| stock | FSUGY | 6 | 0.53% | 16 | -10 | 6 | 0 | 19.31 |
| stock | FTI | -9 | -2.61% | -9 | 0 | -9 | 0 | 63.81 |
| stock | HAL | -9 | -1.33% | -9 | 0 | -9 | 0 | 32.50 |
| stock | INSW | 0 | 0.00% | 1 | -1 | 0 | 0 | 102.12 |
| stock | LYB | -11 | -3.08% | -11 | 0 | -11 | 0 | 61.67 |
| stock | MPC | -2 | -3.66% | -2 | 0 | -2 | 0 | 402.19 |
| stock | PBF | 3 | 0.94% | 3 | 0 | 3 | 0 | 68.63 |
| stock | PSX | -1 | -1.18% | -1 | 0 | -1 | 0 | 260.62 |
| stock | RIO | 6 | 2.18% | 7 | -1 | 6 | 0 | 80.05 |
| stock | SCCO | 2 | 1.40% | 4 | -2 | 2 | 0 | 153.87 |
| stock | SLB | -12 | -2.73% | -12 | 0 | -12 | 0 | 50.08 |
| stock | TECK | 1 | 0.26% | 1 | 0 | 1 | 0 | 57.16 |
| stock | VALE | 23 | 1.09% | 42 | -19 | 23 | 0 | 10.46 |
| stock | VLO | -2 | -3.36% | -2 | 0 | -2 | 0 | 369.73 |
| stock | WLK | -4 | -1.12% | -4 | 0 | -4 | 0 | 61.63 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BHP | SELL | -1.0 | 8.0 | 7.0 | 75.74 | 75.36 | 1 |
| CE | SELL | -1.0 | -13.0 | -14.0 | 49.08 | 48.84 | 1 |
| FSUGY | SELL | -10.0 | 16.0 | 6.0 | 19.36 | 19.26 | 1 |
| INSW | SELL | -1.0 | 1.0 | 0.0 | 102.38 | 101.86 | 1 |
| RIO | SELL | -1.0 | 7.0 | 6.0 | 80.25 | 79.85 | 1 |
| SCCO | SELL | -2.0 | 4.0 | 2.0 | 154.25 | 153.49 | 1 |
| VALE | SELL | -19.0 | 42.0 | 23.0 | 10.49 | 10.43 | 1 |
| SPY | BUY | 1.0 | 0.0 | 1.0 | 738.1 | 741.8 | 2 |
| XME | BUY | 6.0 | -21.0 | -15.0 | 89.69 | 90.13 | 2 |

## Beta method for 2026-11-17 — as-of 2026-11-16

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-11-17-p0gussny/cached/targets/2026-11-17. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
