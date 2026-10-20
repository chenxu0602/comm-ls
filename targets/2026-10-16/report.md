# Combined CL v4.3 + Metals + Agriculture targets: 2026-10-16

- Combined AUM: $22,000.00
- Total child turnover: 10.43% ($2,294.27)
- Stock child turnover (40% cap applies): 6.65%
- Hedge child turnover (uncapped): 3.78%
- Orders: 11
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
| hedge | MOO | -4 | -1.49% | 0 | -4 | -4 | 0 | 82.14 |
| hedge | SPY | 4 | 14.03% | 4 | 0 | 4 | 0 | 771.79 |
| hedge | XLE | 10 | 3.03% | 13 | -3 | 10 | 0 | 66.56 |
| hedge | XME | 0 | 0.00% | 3 | -3 | 0 | 0 | 101.34 |
| stock | ADM | 3 | 1.13% | 0 | 3 | 3 | 0 | 82.93 |
| stock | AVNT | -5 | -0.89% | -5 | 0 | -5 | 0 | 39.00 |
| stock | BG | 1 | 0.49% | 0 | 1 | 1 | 0 | 107.01 |
| stock | BHP | -5 | -1.88% | -7 | 2 | -5 | 0 | 82.90 |
| stock | CE | -9 | -1.90% | -9 | 0 | -9 | 0 | 46.44 |
| stock | DINO | 2 | 1.13% | 2 | 0 | 2 | 0 | 124.70 |
| stock | DK | 10 | 3.49% | 9 | 1 | 10 | 0 | 76.88 |
| stock | DOW | -25 | -3.37% | -26 | 0 | -26 | 1 | 29.66 |
| stock | EMN | -7 | -2.03% | -7 | 0 | -7 | 0 | 63.87 |
| stock | ERO | 19 | 3.00% | 20 | 0 | 20 | -1 | 34.75 |
| stock | FSUGY | -12 | -1.14% | -15 | 3 | -12 | 0 | 20.99 |
| stock | FTI | -4 | -1.24% | -4 | 0 | -4 | 0 | 68.23 |
| stock | HAL | -5 | -0.75% | -4 | 0 | -4 | -1 | 32.89 |
| stock | HUN | -49 | -1.91% | -52 | 0 | -52 | 3 | 8.56 |
| stock | LYB | -12 | -3.42% | -12 | 0 | -12 | 0 | 62.67 |
| stock | MPC | 0 | 0.00% | 1 | -1 | 0 | 0 | 476.92 |
| stock | PBF | 5 | 1.98% | 5 | 0 | 5 | 0 | 86.99 |
| stock | PSX | 3 | 3.94% | 3 | 0 | 3 | 0 | 289.20 |
| stock | RIO | -3 | -1.23% | -5 | 2 | -3 | 0 | 90.21 |
| stock | SCCO | -2 | -1.83% | -2 | 0 | -2 | 0 | 201.69 |
| stock | SLB | -6 | -1.32% | -6 | 0 | -6 | 0 | 48.37 |
| stock | TECK | 3 | 0.90% | 3 | 0 | 3 | 0 | 65.74 |
| stock | VALE | -10 | -0.59% | -20.8 | 11 | -9.8 | -0.2 | 13.02 |
| stock | WLK | -12 | -3.47% | -12 | 0 | -12 | 0 | 63.61 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ADM | BUY | 3.0 | 0.0 | 3.0 | 82.72 | 83.14 | 1 |
| BG | BUY | 1.0 | 0.0 | 1.0 | 106.74 | 107.28 | 1 |
| BHP | BUY | 2.0 | -7.0 | -5.0 | 82.69 | 83.11 | 1 |
| DK | BUY | 1.0 | 9.0 | 10.0 | 76.69 | 77.07 | 1 |
| FSUGY | BUY | 3.0 | -15.0 | -12.0 | 20.94 | 21.04 | 1 |
| MPC | SELL | -1.0 | 1.0 | 0.0 | 478.11 | 475.73 | 1 |
| RIO | BUY | 2.0 | -5.0 | -3.0 | 89.98 | 90.44 | 1 |
| VALE | BUY | 11.0 | -20.8 | -9.8 | 12.99 | 13.05 | 1 |
| MOO | SELL | -4.0 | 0.0 | -4.0 | 82.35 | 81.93 | 2 |
| XLE | SELL | -3.0 | 13.0 | 10.0 | 66.73 | 66.39 | 2 |
| XME | SELL | -3.0 | 3.0 | 0.0 | 101.59 | 101.09 | 2 |

## Beta method for 2026-10-16 — as-of 2026-10-15

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-10-16-afm7wpl7/cached/targets/2026-10-16. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
