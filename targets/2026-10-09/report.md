# Combined CL v4.3 + Metals + Agriculture targets: 2026-10-09

- Combined AUM: $22,000.00
- Total child turnover: 11.54% ($2,539.14)
- Stock child turnover (40% cap applies): 6.96%
- Hedge child turnover (uncapped): 4.59%
- Orders: 9
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
- CRO stock target state for this package: flat. Flat CRO must not create reallocation trades under identical inputs.
- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.
- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.
- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | SPY | 5 | 17.59% | 4 | 1 | 5 | 0 | 773.93 |
| hedge | XLE | 18 | 5.34% | 16 | 2 | 18 | 0 | 65.24 |
| hedge | XME | 5 | 2.38% | 4 | 1 | 5 | 0 | 104.61 |
| stock | AVNT | -5 | -0.93% | -5 | 0 | -5 | 0 | 40.98 |
| stock | BHP | -7 | -2.70% | -7 | 0 | -7 | 0 | 84.83 |
| stock | CE | -9 | -1.83% | -9 | 0 | -9 | 0 | 44.81 |
| stock | DINO | 2 | 1.10% | 3 | -1 | 2 | 0 | 120.72 |
| stock | DK | 10 | 3.48% | 10 | 0 | 10 | 0 | 76.60 |
| stock | DOW | -26 | -3.38% | -27 | 0 | -27 | 1 | 28.59 |
| stock | EMN | -7 | -2.03% | -7 | 0 | -7 | 0 | 63.76 |
| stock | ERO | 19 | 3.11% | 18 | 0 | 18 | 1 | 35.98 |
| stock | FSUGY | -16 | -1.60% | -15 | -1 | -16 | 0 | 22.00 |
| stock | FTI | -4 | -1.27% | -4 | 0 | -4 | 0 | 69.63 |
| stock | HAL | -5 | -0.74% | -4 | 0 | -4 | -1 | 32.57 |
| stock | HUN | -49 | -1.89% | -47 | 0 | -47 | -2 | 8.50 |
| stock | LYB | -12 | -3.29% | -13 | 0 | -13 | 1 | 60.34 |
| stock | MPC | 0 | 0.00% | 1 | -1 | 0 | 0 | 463.34 |
| stock | PBF | 5 | 2.03% | 5 | 0 | 5 | 0 | 89.34 |
| stock | PSX | 2 | 2.56% | 3 | -1 | 2 | 0 | 281.60 |
| stock | RIO | -6 | -2.55% | -6 | 0 | -6 | 0 | 93.34 |
| stock | SCCO | -3 | -2.71% | -2 | -1 | -3 | 0 | 198.66 |
| stock | SLB | -6 | -1.34% | -6 | 0 | -6 | 0 | 48.98 |
| stock | TECK | 3 | 0.88% | 3 | 0 | 3 | 0 | 64.82 |
| stock | VALE | -24 | -1.46% | -23.8 | 0 | -23.8 | -0.2 | 13.42 |
| stock | VLO | 0 | 0.00% | 1 | -1 | 0 | 0 | 443.80 |
| stock | WLK | -12 | -3.40% | -12 | 0 | -12 | 0 | 62.31 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DINO | SELL | -1.0 | 3.0 | 2.0 | 121.02 | 120.42 | 1 |
| FSUGY | SELL | -1.0 | -15.0 | -16.0 | 22.06 | 21.94 | 1 |
| MPC | SELL | -1.0 | 1.0 | 0.0 | 464.5 | 462.18 | 1 |
| PSX | SELL | -1.0 | 3.0 | 2.0 | 282.3 | 280.9 | 1 |
| SCCO | SELL | -1.0 | -2.0 | -3.0 | 199.16 | 198.16 | 1 |
| VLO | SELL | -1.0 | 1.0 | 0.0 | 444.91 | 442.69 | 1 |
| SPY | BUY | 1.0 | 4.0 | 5.0 | 772.0 | 775.86 | 2 |
| XLE | BUY | 2.0 | 16.0 | 18.0 | 65.08 | 65.4 | 2 |
| XME | BUY | 1.0 | 4.0 | 5.0 | 104.35 | 104.87 | 2 |

## Operator beta decision — 2026-10-09

Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-10-09-31i2mpxo/cached/targets/2026-10-09. Agriculture's existing component-specific cached beta is unchanged.
