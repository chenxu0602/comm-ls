# Combined CL v4.3 + Metals + Agriculture targets: 2026-10-15

- Combined AUM: $22,000.00
- Total child turnover: 1.09% ($240.12)
- Stock child turnover (40% cap applies): 0.78%
- Hedge child turnover (uncapped): 0.31%
- Orders: 5
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Strategy changes and allocation notes

- Agriculture v4.3 joined the main account effective 2026-10-02: $2,000 allocated AUM. Idle allocation remains cash and still counts in account AUM.
- Agriculture uses component-specific hedges: crush_vol/crush_vol2/adm_bg2 use SPY + MOO; adm_bg/adm_tsn/bg_tsn use SPY only. Keep its virtual book separate.
- Agriculture stock target state for this package: flat. This is not a permanent suspension.
- CRO (crack refiner-only) added effective 2026-10-06: 10% allocation from unused CL capacity. CL AUM remains $15,000; existing sleeve weights are NOT reduced or renormalized.
- CRO stocks: VLO/MPC/PSX = 30/40/30%; crack_03; signal lookback 30 sessions; volatility lookback 30 (minimum 20); no signal smoothing; balance=0.5 (maximum CRO stock gross 5% of CL AUM).
- CRO explicit hedge is SPY ONLY, not XLE. Preserve component hedge ownership when PSX overlaps existing sleeves; net single-name cap and execution constraints still apply.
- This addition is refiner-only CRO, NOT the refiner-producer CRP, refiner-VLCC CRV, or refiner-chemical CRC research strategies.
- CRO stock target state for this package: active. Flat CRO must not create reallocation trades under identical inputs.
- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.
- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.
- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | SPY | 4 | 13.99% | 4 | 0 | 4 | 0 | 769.60 |
| hedge | XLE | 13 | 4.00% | 14 | -1 | 13 | 0 | 67.63 |
| hedge | XME | 3 | 1.36% | 3 | 0 | 3 | 0 | 99.86 |
| stock | AVNT | -5 | -0.88% | -5 | 0 | -5 | 0 | 38.85 |
| stock | BHP | -7 | -2.65% | -7 | 0 | -7 | 0 | 83.26 |
| stock | CE | -9 | -1.87% | -9 | 0 | -9 | 0 | 45.82 |
| stock | DINO | 2 | 1.16% | 2 | 0 | 2 | 0 | 127.69 |
| stock | DK | 9 | 3.23% | 9 | 0 | 9 | 0 | 78.97 |
| stock | DOW | -26 | -3.45% | -27 | 1 | -26 | 0 | 29.19 |
| stock | EMN | -7 | -2.00% | -7 | 0 | -7 | 0 | 62.88 |
| stock | ERO | 20 | 3.13% | 18 | 2 | 20 | 0 | 34.46 |
| stock | FSUGY | -15 | -1.44% | -15 | 0 | -15 | 0 | 21.17 |
| stock | FTI | -4 | -1.26% | -4 | 0 | -4 | 0 | 69.50 |
| stock | HAL | -5 | -0.75% | -4 | 0 | -4 | -1 | 32.83 |
| stock | HUN | -51 | -1.91% | -52 | 0 | -52 | 1 | 8.24 |
| stock | LYB | -12 | -3.34% | -13 | 1 | -12 | 0 | 61.17 |
| stock | MPC | 1 | 2.20% | 1 | 0 | 1 | 0 | 484.92 |
| stock | PBF | 5 | 2.03% | 5 | 0 | 5 | 0 | 89.51 |
| stock | PSX | 3 | 4.05% | 3 | 0 | 3 | 0 | 297.29 |
| stock | RIO | -5 | -2.07% | -5 | 0 | -5 | 0 | 91.25 |
| stock | SCCO | -2 | -1.82% | -2 | 0 | -2 | 0 | 200.68 |
| stock | SLB | -6 | -1.32% | -6 | 0 | -6 | 0 | 48.51 |
| stock | TECK | 3 | 0.88% | 3 | 0 | 3 | 0 | 64.80 |
| stock | VALE | -21 | -1.26% | -19.8 | -1 | -20.8 | -0.2 | 13.21 |
| stock | WLK | -12 | -3.39% | -12 | 0 | -12 | 0 | 62.21 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DOW | BUY | 1.0 | -27.0 | -26.0 | 29.12 | 29.26 | 1 |
| ERO | BUY | 2.0 | 18.0 | 20.0 | 34.37 | 34.55 | 1 |
| LYB | BUY | 1.0 | -13.0 | -12.0 | 61.02 | 61.32 | 1 |
| VALE | SELL | -1.0 | -19.8 | -20.8 | 13.24 | 13.18 | 1 |
| XLE | SELL | -1.0 | 14.0 | 13.0 | 67.8 | 67.46 | 2 |

## Beta method for 2026-10-15 — as-of 2026-10-14

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-10-15-fe4cg33a/cached/targets/2026-10-15. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
