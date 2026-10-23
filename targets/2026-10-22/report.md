# Combined CL v4.3 + Metals + Agriculture targets: 2026-10-22

- Combined AUM: $22,000.00
- Total child turnover: 3.18% ($699.77)
- Stock child turnover (40% cap applies): 1.27%
- Hedge child turnover (uncapped): 1.91%
- Orders: 5
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Strategy changes and allocation notes

- Agriculture v4.3 joined the main account effective 2026-10-02: $2,000 allocated AUM. Idle allocation remains cash and still counts in account AUM.
- Agriculture uses component-specific hedges: crush_vol/crush_vol2/adm_bg2 use SPY + MOO; adm_bg/adm_tsn/bg_tsn use SPY only. Keep its virtual book separate.
- Agriculture stock target state for this package: active. This is not a permanent suspension.
- CRO (crack refiner-only) added effective 2026-10-06: 10% allocation from unused CL capacity. CL AUM remains $15,000; existing sleeve weights are NOT reduced or renormalized.
- CRO stocks: VLO/MPC/PSX = 30/40/30%; crack_03; signal lookback 30 sessions; volatility lookback 30 (minimum 20); no signal smoothing; balance=0.5 (maximum CRO stock gross 5% of CL AUM).
- CRO explicit hedge is SPY ONLY, not XLE. Preserve component hedge ownership when PSX overlaps existing sleeves; net single-name cap and execution constraints still apply.
- This addition is refiner-only CRO, NOT the refiner-producer CRP, refiner-VLCC CRV, or refiner-chemical CRC research strategies.
- CRO stock target state for this package: flat. Flat CRO must not create reallocation trades under identical inputs.
- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.
- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.
- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | MOO | -5 | -1.85% | -6 | 1 | -5 | 0 | 81.31 |
| hedge | SPY | 4 | 14.06% | 4 | 0 | 4 | 0 | 773.13 |
| hedge | XLE | 8 | 2.48% | 10 | -2 | 8 | 0 | 68.15 |
| hedge | XME | 2 | 0.92% | 0 | 2 | 2 | 0 | 101.29 |
| stock | ADM | 3 | 1.08% | 3 | 0 | 3 | 0 | 79.35 |
| stock | AVNT | -5 | -0.92% | -5 | 0 | -5 | 0 | 40.70 |
| stock | BG | 2 | 0.93% | 2 | 0 | 2 | 0 | 102.22 |
| stock | BHP | -5 | -1.84% | -5 | 0 | -5 | 0 | 80.82 |
| stock | CE | -9 | -1.93% | -9 | 0 | -9 | 0 | 47.27 |
| stock | DINO | 2 | 1.14% | 2 | 0 | 2 | 0 | 125.61 |
| stock | DK | 10 | 3.56% | 10 | 0 | 10 | 0 | 78.27 |
| stock | DOW | -25 | -3.46% | -24 | 0 | -24 | -1 | 30.41 |
| stock | EMN | -7 | -2.02% | -7 | 0 | -7 | 0 | 63.48 |
| stock | ERO | 21 | 3.05% | 20 | 0 | 20 | 1 | 31.99 |
| stock | FSUGY | -12 | -1.16% | -12 | 0 | -12 | 0 | 21.34 |
| stock | FTI | -4 | -1.27% | -4 | 0 | -4 | 0 | 70.00 |
| stock | HAL | -4 | -0.62% | -4 | 0 | -4 | 0 | 33.99 |
| stock | HUN | -51 | -1.91% | -52 | 0 | -52 | 1 | 8.23 |
| stock | LYB | -12 | -3.45% | -12 | 0 | -12 | 0 | 63.29 |
| stock | PBF | 6 | 2.22% | 5 | 1 | 6 | 0 | 81.54 |
| stock | PSX | 3 | 3.96% | 3 | 0 | 3 | 0 | 290.10 |
| stock | RIO | -3 | -1.19% | -3 | 0 | -3 | 0 | 86.93 |
| stock | SCCO | -3 | -2.70% | -2 | -1 | -3 | 0 | 198.04 |
| stock | SLB | -6 | -1.39% | -6 | 0 | -6 | 0 | 51.11 |
| stock | TECK | 4 | 1.14% | 3 | 0 | 3 | 1 | 62.78 |
| stock | VALE | -10 | -0.58% | -9.8 | 0 | -9.8 | -0.2 | 12.69 |
| stock | WLK | -12 | -3.32% | -12 | 0 | -12 | 0 | 60.81 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PBF | BUY | 1.0 | 5.0 | 6.0 | 81.33 | 81.74 | 1 |
| SCCO | SELL | -1.0 | -2.0 | -3.0 | 198.54 | 197.54 | 1 |
| MOO | BUY | 1.0 | -6.0 | -5.0 | 81.11 | 81.51 | 2 |
| XLE | SELL | -2.0 | 10.0 | 8.0 | 68.32 | 67.98 | 2 |
| XME | BUY | 2.0 | 0.0 | 2.0 | 101.04 | 101.54 | 2 |

## Beta method for 2026-10-22 — as-of 2026-10-21

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-10-22-r50itokr/cached/targets/2026-10-22. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
