# Combined CL v4.3 + Metals + Agriculture targets: 2026-10-21

- Combined AUM: $22,000.00
- Total child turnover: 0.66% ($144.38)
- Stock child turnover (40% cap applies): 0.66%
- Hedge child turnover (uncapped): 0.00%
- Orders: 2
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
| hedge | MOO | -6 | -2.21% | -6 | 0 | -6 | 0 | 81.12 |
| hedge | SPY | 4 | 13.98% | 4 | 0 | 4 | 0 | 769.05 |
| hedge | XLE | 10 | 3.09% | 10 | 0 | 10 | 0 | 67.97 |
| stock | ADM | 3 | 1.10% | 3 | 0 | 3 | 0 | 80.46 |
| stock | AVNT | -5 | -0.92% | -5 | 0 | -5 | 0 | 40.35 |
| stock | BG | 2 | 0.94% | 2 | 0 | 2 | 0 | 103.00 |
| stock | BHP | -5 | -1.86% | -5 | 0 | -5 | 0 | 81.87 |
| stock | CE | -9 | -1.94% | -9 | 0 | -9 | 0 | 47.52 |
| stock | DINO | 2 | 1.14% | 2 | 0 | 2 | 0 | 125.31 |
| stock | DK | 10 | 3.53% | 10 | 0 | 10 | 0 | 77.63 |
| stock | DOW | -24 | -3.35% | -26 | 2 | -24 | 0 | 30.69 |
| stock | EMN | -7 | -2.02% | -7 | 0 | -7 | 0 | 63.50 |
| stock | ERO | 21 | 3.14% | 20 | 0 | 20 | 1 | 32.90 |
| stock | FSUGY | -12 | -1.17% | -12 | 0 | -12 | 0 | 21.53 |
| stock | FTI | -4 | -1.25% | -4 | 0 | -4 | 0 | 68.93 |
| stock | HAL | -4 | -0.61% | -4 | 0 | -4 | 0 | 33.59 |
| stock | HUN | -50 | -1.90% | -52 | 0 | -52 | 2 | 8.34 |
| stock | LYB | -12 | -3.49% | -12 | 0 | -12 | 0 | 63.96 |
| stock | PBF | 5 | 1.89% | 6 | -1 | 5 | 0 | 83.00 |
| stock | PSX | 3 | 3.97% | 3 | 0 | 3 | 0 | 291.03 |
| stock | RIO | -3 | -1.20% | -3 | 0 | -3 | 0 | 88.16 |
| stock | SCCO | -2 | -1.84% | -2 | 0 | -2 | 0 | 202.34 |
| stock | SLB | -6 | -1.36% | -6 | 0 | -6 | 0 | 49.98 |
| stock | TECK | 3 | 0.88% | 3 | 0 | 3 | 0 | 64.33 |
| stock | VALE | -10 | -0.59% | -9.8 | 0 | -9.8 | -0.2 | 13.02 |
| stock | WLK | -12 | -3.42% | -12 | 0 | -12 | 0 | 62.69 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DOW | BUY | 2.0 | -26.0 | -24.0 | 30.61 | 30.77 | 1 |
| PBF | SELL | -1.0 | 6.0 | 5.0 | 83.21 | 82.79 | 1 |

## Beta method for 2026-10-21 — as-of 2026-10-20

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-10-21-8mp77h2e/cached/targets/2026-10-21. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
