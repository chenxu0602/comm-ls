# Combined CL v4.3 + Metals + Agriculture targets: 2026-11-06

- Combined AUM: $22,000.00
- Total child turnover: 36.77% ($8,090.04)
- Stock child turnover (40% cap applies): 21.72%
- Hedge child turnover (uncapped): 15.05%
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
- Agriculture stock target state for this package: active. This is not a permanent suspension.
- CURRENT CL from 2026-11-06: shipping20->10% operator risk reduction; chemical20/refiner3/refiner_slow8/services20/bwt2/CRO20/re_c03 10% unchanged. Nominal budget93%, no normalization; released10 percentage points stay cash. No automatic shipping restoration.
- Operator corrected notebook: chemical retains hold2 (NOT direct signal, NOT hold21). Slow HO m1 gate reads carry_data_2 from Nov06 to match notebook default loader, with strict lookback/arrival validation, no canonical fallback. L/PP exits and baskets unchanged. CRO remains half-balance SPY-only; re_c03 SPY+XLE. AUM and legacy DAILY beta unchanged. See docs/cl_shipping_reduction_2026-11-06.md.
- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.
- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.
- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | MOO | -2 | -0.75% | -2 | 0 | -2 | 0 | 82.62 |
| hedge | SPY | 1 | 3.33% | 1 | 0 | 1 | 0 | 733.00 |
| hedge | XLE | 47 | 13.17% | 5 | 42 | 47 | 0 | 61.63 |
| hedge | XME | -2 | -0.82% | 8 | -8 | 0 | -2 | 90.42 |
| stock | ADM | 11 | 3.52% | 11 | 0 | 11 | 0 | 70.47 |
| stock | BG | -5 | -2.24% | -5 | 0 | -5 | 0 | 98.54 |
| stock | BHP | 4 | 1.43% | -5 | 5 | 0 | 4 | 78.58 |
| stock | CE | -16 | -3.48% | 0 | -16 | -16 | 0 | 47.84 |
| stock | DHT | 22 | 2.05% | 34 | -12 | 22 | 0 | 20.48 |
| stock | DINO | 2 | 0.89% | 2 | 0 | 2 | 0 | 97.77 |
| stock | DK | 10 | 2.84% | 9 | 1 | 10 | 0 | 62.49 |
| stock | DOW | -23 | -3.34% | 0 | -23 | -23 | 0 | 31.98 |
| stock | ERO | 8 | 1.02% | 8 | 0 | 8 | 0 | 28.09 |
| stock | FRO | 10 | 2.03% | 15 | -5 | 10 | 0 | 44.70 |
| stock | FSUGY | -12 | -1.15% | -12 | 0 | -12 | 0 | 21.14 |
| stock | FTI | -12 | -3.36% | -12 | 0 | -12 | 0 | 61.59 |
| stock | HAL | -19 | -2.76% | -18 | 0 | -18 | -1 | 31.92 |
| stock | INSW | 3 | 1.29% | 6 | -3 | 3 | 0 | 94.47 |
| stock | LYB | -12 | -3.36% | 0 | -12 | -12 | 0 | 61.63 |
| stock | MPC | -2 | -3.43% | -2 | 0 | -2 | 0 | 377.32 |
| stock | PBF | 3 | 0.93% | 3 | 0 | 3 | 0 | 68.37 |
| stock | PSX | -1 | -1.12% | -1 | 0 | -1 | 0 | 247.04 |
| stock | RIO | 6 | 2.27% | -3 | 3 | 0 | 6 | 83.16 |
| stock | SCCO | 1 | 0.75% | -2.0318 | 2 | -0.0318 | 1.0318 | 165.38 |
| stock | SLB | -15 | -3.38% | -14 | -1 | -15 | 0 | 49.64 |
| stock | STNG | 1 | 0.37% | 2 | -1 | 1 | 0 | 80.74 |
| stock | TECK | 1 | 0.27% | 1 | 0 | 1 | 0 | 59.91 |
| stock | TNK | 3 | 1.12% | 5 | -2 | 3 | 0 | 81.97 |
| stock | VALE | 20 | 1.04% | -10.8 | 10.8 | 0 | 20 | 11.45 |
| stock | VLO | -2 | -3.19% | -2 | 0 | -2 | 0 | 351.23 |
| stock | WLK | -5 | -1.51% | 0 | -5 | -5 | 0 | 66.28 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BHP | BUY | 5.0 | -5.0 | 0.0 | 78.38 | 78.78 | 1 |
| CE | SELL | -16.0 | 0.0 | -16.0 | 47.96 | 47.72 | 1 |
| DHT | SELL | -12.0 | 34.0 | 22.0 | 20.53 | 20.43 | 1 |
| DK | BUY | 1.0 | 9.0 | 10.0 | 62.33 | 62.65 | 1 |
| DOW | SELL | -23.0 | 0.0 | -23.0 | 32.06 | 31.9 | 1 |
| FRO | SELL | -5.0 | 15.0 | 10.0 | 44.81 | 44.59 | 1 |
| INSW | SELL | -3.0 | 6.0 | 3.0 | 94.71 | 94.23 | 1 |
| LYB | SELL | -12.0 | 0.0 | -12.0 | 61.78 | 61.48 | 1 |
| RIO | BUY | 3.0 | -3.0 | 0.0 | 82.95 | 83.37 | 1 |
| SCCO | BUY | 2.0 | -2.0318 | -0.03180000000000005 | 164.97 | 165.79 | 1 |
| SLB | SELL | -1.0 | -14.0 | -15.0 | 49.76 | 49.52 | 1 |
| STNG | SELL | -1.0 | 2.0 | 1.0 | 80.94 | 80.54 | 1 |
| TNK | SELL | -2.0 | 5.0 | 3.0 | 82.17 | 81.77 | 1 |
| VALE | BUY | 10.8 | -10.8 | 0.0 | 11.42 | 11.48 | 1 |
| WLK | SELL | -5.0 | 0.0 | -5.0 | 66.45 | 66.11 | 1 |
| XLE | BUY | 42.0 | 5.0 | 47.0 | 61.48 | 61.78 | 2 |
| XME | SELL | -8.0 | 8.0 | 0.0 | 90.65 | 90.19 | 2 |

## Beta method for 2026-11-06 — as-of 2026-11-05

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-11-06-lajdlroc/cached/targets/2026-11-06. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
