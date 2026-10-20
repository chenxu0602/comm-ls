# Combined CL v4.3 + Metals + Agriculture targets: 2026-10-07

- Combined AUM: $22,000.00
- Total child turnover: 7.38% ($1,623.16)
- Stock child turnover (40% cap applies): 5.93%
- Hedge child turnover (uncapped): 1.45%
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
| hedge | SPY | 4 | 14.17% | 4 | 0 | 4 | 0 | 779.09 |
| hedge | XLE | 27 | 7.82% | 32 | -5 | 27 | 0 | 63.75 |
| hedge | XME | 3 | 1.48% | 3 | 0 | 3 | 0 | 108.24 |
| stock | AVNT | -5 | -0.94% | -5 | 0 | -5 | 0 | 41.49 |
| stock | BHP | -7 | -2.77% | -7 | 0 | -7 | 0 | 87.00 |
| stock | CE | -9 | -1.83% | -9 | 0 | -9 | 0 | 44.85 |
| stock | DINO | 3 | 1.56% | 3 | 0 | 3 | 0 | 114.60 |
| stock | DK | 10 | 3.44% | 10 | 0 | 10 | 0 | 75.67 |
| stock | DOW | -27 | -3.46% | -27 | 0 | -27 | 0 | 28.16 |
| stock | EMN | -7 | -2.04% | -6 | 0 | -6 | -1 | 64.11 |
| stock | ERO | 18 | 3.10% | 18 | 0 | 18 | 0 | 37.93 |
| stock | FSUGY | -15 | -1.56% | -15 | 0 | -15 | 0 | 22.91 |
| stock | FTI | -4 | -1.27% | -4 | 0 | -4 | 0 | 69.89 |
| stock | HAL | -5 | -0.74% | -4 | 0 | -4 | -1 | 32.72 |
| stock | HUN | -48 | -1.91% | -47 | 0 | -47 | -1 | 8.77 |
| stock | LYB | -13 | -3.48% | -13 | 0 | -13 | 0 | 58.93 |
| stock | MPC | 1 | 1.97% | 0 | 1 | 1 | 0 | 432.36 |
| stock | PBF | 5 | 1.88% | 5 | 0 | 5 | 0 | 82.88 |
| stock | PSX | 1 | 1.23% | -1 | 1 | 0 | 1 | 269.79 |
| stock | RIO | -6 | -2.62% | -6 | 0 | -6 | 0 | 95.89 |
| stock | SCCO | -2 | -1.86% | -2 | 0 | -2 | 0 | 204.26 |
| stock | SLB | -6 | -1.36% | -6 | 0 | -6 | 0 | 50.00 |
| stock | TECK | 3 | 0.91% | 3 | 0 | 3 | 0 | 67.10 |
| stock | VALE | -23 | -1.47% | -9.8 | -13 | -22.8 | -0.2 | 14.08 |
| stock | VLO | 1 | 1.91% | 0 | 1 | 1 | 0 | 419.22 |
| stock | WLK | -12 | -3.46% | -12 | 0 | -12 | 0 | 63.39 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| MPC | BUY | 1.0 | 0.0 | 1.0 | 431.28 | 433.44 | 1 |
| PSX | BUY | 1.0 | -1.0 | 0.0 | 269.12 | 270.46 | 1 |
| VALE | SELL | -13.0 | -9.8 | -22.8 | 14.12 | 14.04 | 1 |
| VLO | BUY | 1.0 | 0.0 | 1.0 | 418.17 | 420.27 | 1 |
| XLE | SELL | -5.0 | 32.0 | 27.0 | 63.91 | 63.59 | 2 |
