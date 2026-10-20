# Combined CL v4.3 + Metals + Agriculture targets: 2026-10-20

- Combined AUM: $22,000.00
- Total child turnover: 0.97% ($212.33)
- Stock child turnover (40% cap applies): 0.66%
- Hedge child turnover (uncapped): 0.31%
- Orders: 3
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
| hedge | MOO | -6 | -2.20% | -6 | 0 | -6 | 0 | 80.69 |
| hedge | SPY | 4 | 13.94% | 4 | 0 | 4 | 0 | 766.48 |
| hedge | XLE | 10 | 3.08% | 11 | -1 | 10 | 0 | 67.80 |
| stock | ADM | 3 | 1.10% | 3 | 0 | 3 | 0 | 80.51 |
| stock | AVNT | -5 | -0.90% | -5 | 0 | -5 | 0 | 39.51 |
| stock | BG | 2 | 0.94% | 2 | 0 | 2 | 0 | 103.11 |
| stock | BHP | -5 | -1.89% | -5 | 0 | -5 | 0 | 83.22 |
| stock | CE | -9 | -1.96% | -9 | 0 | -9 | 0 | 47.88 |
| stock | DINO | 2 | 1.13% | 2 | 0 | 2 | 0 | 124.42 |
| stock | DK | 10 | 3.41% | 10 | 0 | 10 | 0 | 75.08 |
| stock | DOW | -25 | -3.42% | -26 | 0 | -26 | 1 | 30.08 |
| stock | EMN | -7 | -1.99% | -7 | 0 | -7 | 0 | 62.48 |
| stock | ERO | 20 | 3.13% | 20 | 0 | 20 | 0 | 34.43 |
| stock | FSUGY | -12 | -1.15% | -15 | 3 | -12 | 0 | 21.09 |
| stock | FTI | -4 | -1.27% | -4 | 0 | -4 | 0 | 69.86 |
| stock | HAL | -5 | -0.75% | -4 | 0 | -4 | -1 | 32.98 |
| stock | HUN | -50 | -1.89% | -52 | 0 | -52 | 2 | 8.33 |
| stock | LYB | -12 | -3.48% | -12 | 0 | -12 | 0 | 63.71 |
| stock | PBF | 6 | 2.22% | 5 | 1 | 6 | 0 | 81.26 |
| stock | PSX | 3 | 3.96% | 3 | 0 | 3 | 0 | 290.55 |
| stock | RIO | -3 | -1.22% | -3 | 0 | -3 | 0 | 89.50 |
| stock | SCCO | -2 | -1.83% | -2 | 0 | -2 | 0 | 201.78 |
| stock | SLB | -6 | -1.34% | -6 | 0 | -6 | 0 | 49.09 |
| stock | TECK | 4 | 1.15% | 3 | 0 | 3 | 1 | 63.48 |
| stock | VALE | -10 | -0.60% | -9.8 | 0 | -9.8 | -0.2 | 13.11 |
| stock | WLK | -12 | -3.40% | -12 | 0 | -12 | 0 | 62.29 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FSUGY | BUY | 3.0 | -15.0 | -12.0 | 21.04 | 21.14 | 1 |
| PBF | BUY | 1.0 | 5.0 | 6.0 | 81.06 | 81.46 | 1 |
| XLE | SELL | -1.0 | 11.0 | 10.0 | 67.97 | 67.63 | 2 |

## Beta method for 2026-10-20 — as-of 2026-10-19

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-10-20-4i1_am1h/cached/targets/2026-10-20. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
