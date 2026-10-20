# Combined CL v4.3 + Metals + Agriculture targets: 2026-10-19

- Combined AUM: $22,000.00
- Total child turnover: 2.64% ($581.57)
- Stock child turnover (40% cap applies): 1.59%
- Hedge child turnover (uncapped): 1.05%
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
| hedge | MOO | -6 | -2.23% | -4 | -2 | -6 | 0 | 81.79 |
| hedge | SPY | 4 | 13.88% | 4 | 0 | 4 | 0 | 763.25 |
| hedge | XLE | 11 | 3.41% | 10 | 1 | 11 | 0 | 68.24 |
| stock | ADM | 3 | 1.13% | 3 | 0 | 3 | 0 | 82.61 |
| stock | AVNT | -5 | -0.89% | -5 | 0 | -5 | 0 | 38.98 |
| stock | BG | 2 | 0.96% | 1 | 1 | 2 | 0 | 106.14 |
| stock | BHP | -5 | -1.89% | -5 | 0 | -5 | 0 | 83.29 |
| stock | CE | -9 | -1.94% | -9 | 0 | -9 | 0 | 47.49 |
| stock | DINO | 2 | 1.14% | 2 | 0 | 2 | 0 | 125.29 |
| stock | DK | 10 | 3.48% | 10 | 0 | 10 | 0 | 76.59 |
| stock | DOW | -25 | -3.40% | -26 | 0 | -26 | 1 | 29.93 |
| stock | EMN | -7 | -1.98% | -7 | 0 | -7 | 0 | 62.33 |
| stock | ERO | 20 | 3.11% | 20 | 0 | 20 | 0 | 34.16 |
| stock | FSUGY | -12 | -1.14% | -15 | 3 | -12 | 0 | 20.99 |
| stock | FTI | -4 | -1.27% | -4 | 0 | -4 | 0 | 69.67 |
| stock | HAL | -4 | -0.61% | -4 | 0 | -4 | 0 | 33.50 |
| stock | HUN | -49 | -1.91% | -52 | 0 | -52 | 3 | 8.58 |
| stock | LYB | -12 | -3.49% | -12 | 0 | -12 | 0 | 64.01 |
| stock | PBF | 5 | 1.92% | 5 | 0 | 5 | 0 | 84.52 |
| stock | PSX | 3 | 4.00% | 3 | 0 | 3 | 0 | 293.17 |
| stock | RIO | -3 | -1.23% | -5 | 2 | -3 | 0 | 90.32 |
| stock | SCCO | -2 | -1.82% | -2 | 0 | -2 | 0 | 200.51 |
| stock | SLB | -6 | -1.35% | -6 | 0 | -6 | 0 | 49.50 |
| stock | TECK | 3 | 0.88% | 3 | 0 | 3 | 0 | 64.62 |
| stock | VALE | -10 | -0.59% | -9.8 | 0 | -9.8 | -0.2 | 13.06 |
| stock | WLK | -12 | -3.45% | -12 | 0 | -12 | 0 | 63.33 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BG | BUY | 1.0 | 1.0 | 2.0 | 105.87 | 106.41 | 1 |
| FSUGY | BUY | 3.0 | -15.0 | -12.0 | 20.94 | 21.04 | 1 |
| RIO | BUY | 2.0 | -5.0 | -3.0 | 90.09 | 90.55 | 1 |
| MOO | SELL | -2.0 | -4.0 | -6.0 | 81.99 | 81.59 | 2 |
| XLE | BUY | 1.0 | 10.0 | 11.0 | 68.07 | 68.41 | 2 |

## Beta method for 2026-10-19 — as-of 2026-10-16

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-10-19-yth0x4tp/cached/targets/2026-10-19. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
