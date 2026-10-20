# Combined CL v4.3 + Metals + Agriculture targets: 2026-10-14

- Combined AUM: $22,000.00
- Total child turnover: 3.05% ($671.61)
- Stock child turnover (40% cap applies): 2.44%
- Hedge child turnover (uncapped): 0.61%
- Orders: 3
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
| hedge | SPY | 4 | 14.15% | 4 | 0 | 4 | 0 | 778.01 |
| hedge | XLE | 14 | 4.28% | 16 | -2 | 14 | 0 | 67.20 |
| hedge | XME | 3 | 1.41% | 3 | 0 | 3 | 0 | 103.76 |
| stock | AVNT | -5 | -0.90% | -5 | 0 | -5 | 0 | 39.54 |
| stock | BHP | -7 | -2.70% | -7 | 0 | -7 | 0 | 84.95 |
| stock | CE | -9 | -1.83% | -9 | 0 | -9 | 0 | 44.73 |
| stock | DINO | 2 | 1.17% | 2 | 0 | 2 | 0 | 128.23 |
| stock | DK | 9 | 3.30% | 10 | -1 | 9 | 0 | 80.75 |
| stock | DOW | -26 | -3.37% | -27 | 0 | -27 | 1 | 28.51 |
| stock | EMN | -7 | -2.00% | -7 | 0 | -7 | 0 | 63.00 |
| stock | ERO | 18 | 3.00% | 18 | 0 | 18 | 0 | 36.65 |
| stock | FSUGY | -15 | -1.46% | -15 | 0 | -15 | 0 | 21.35 |
| stock | FTI | -4 | -1.29% | -4 | 0 | -4 | 0 | 70.72 |
| stock | HAL | -5 | -0.75% | -4 | 0 | -4 | -1 | 32.79 |
| stock | HUN | -51 | -1.89% | -52 | 0 | -52 | 1 | 8.16 |
| stock | LYB | -12 | -3.27% | -13 | 0 | -13 | 1 | 60.01 |
| stock | MPC | 1 | 2.17% | 1 | 0 | 1 | 0 | 476.98 |
| stock | PBF | 5 | 2.07% | 5 | 0 | 5 | 0 | 91.17 |
| stock | PSX | 3 | 3.99% | 3 | 0 | 3 | 0 | 292.73 |
| stock | RIO | -5 | -2.12% | -5 | 0 | -5 | 0 | 93.06 |
| stock | SCCO | -2 | -1.89% | -2 | 0 | -2 | 0 | 207.42 |
| stock | SLB | -6 | -1.33% | -6 | 0 | -6 | 0 | 48.77 |
| stock | TECK | 3 | 0.92% | 3 | 0 | 3 | 0 | 67.17 |
| stock | VALE | -21 | -1.28% | -19.8 | 0 | -19.8 | -1.2 | 13.37 |
| stock | VLO | 0 | 0.00% | 1 | -1 | 0 | 0 | 456.46 |
| stock | WLK | -12 | -3.37% | -12 | 0 | -12 | 0 | 61.86 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DK | SELL | -1.0 | 10.0 | 9.0 | 80.95 | 80.55 | 1 |
| VLO | SELL | -1.0 | 1.0 | 0.0 | 457.6 | 455.32 | 1 |
| XLE | SELL | -2.0 | 16.0 | 14.0 | 67.37 | 67.03 | 2 |

## Beta method for 2026-10-14 — as-of 2026-10-13

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-10-14-kibydwm3/cached/targets/2026-10-14. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
