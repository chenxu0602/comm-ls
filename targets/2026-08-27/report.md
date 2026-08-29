# Combined CL v4.3 + Metals targets: 2026-08-27

- Combined AUM: $20,000.00
- Total child turnover: 14.52% ($2,904.19)
- Stock child turnover (40% cap applies): 5.70%
- Hedge child turnover (uncapped): 8.82%
- Orders: 6
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | SPY | 1 | 3.83% | 0 | 1 | 1 | 0 | 766.08 |
| hedge | XLE | 40 | 12.49% | 56 | -16 | 40 | 0 | 62.43 |
| hedge | XME | -22 | -13.23% | -22 | 0 | -22 | 0 | 120.31 |
| stock | ATI | 2 | 2.13% | 2 | 0 | 2 | 0 | 212.86 |
| stock | AVNT | -5 | -1.12% | -5 | 0 | -5 | 0 | 44.78 |
| stock | BHP | 6 | 2.89% | 6 | 0 | 6 | 0 | 96.33 |
| stock | CE | -9 | -2.01% | -9 | 0 | -9 | 0 | 44.70 |
| stock | DINO | 2 | 0.97% | 0 | 2 | 2 | 0 | 96.52 |
| stock | DK | 6 | 2.13% | 0 | 6 | 6 | 0 | 70.84 |
| stock | DOW | -25 | -3.79% | -25 | 0 | -25 | 0 | 30.33 |
| stock | EMN | -6 | -2.19% | -6 | 0 | -6 | 0 | 72.93 |
| stock | ERO | 17 | 3.34% | 17 | 0 | 17 | 0 | 39.24 |
| stock | FSUGY | 13 | 1.63% | 13 | 0 | 13 | 0 | 25.02 |
| stock | FTI | -4 | -1.51% | -4 | 0 | -4 | 0 | 75.70 |
| stock | HAL | -4 | -0.69% | -4 | 0 | -4 | 0 | 34.44 |
| stock | HUN | -44 | -2.12% | -43 | 0 | -43 | -1 | 9.63 |
| stock | HWM | 1 | 1.35% | 1 | 0 | 1 | 0 | 269.34 |
| stock | LYB | -12 | -3.76% | -12 | 0 | -12 | 0 | 62.62 |
| stock | MUSA | 1 | 2.66% | 1 | 0 | 1 | 0 | 531.64 |
| stock | PBF | 4 | 1.39% | 0 | 4 | 4 | 0 | 69.73 |
| stock | PSX | 0 | 0.00% | -1 | 1 | 0 | 0 | 242.23 |
| stock | RIO | 6 | 3.14% | 6 | 0 | 6 | 0 | 104.70 |
| stock | SCCO | 3 | 3.21% | 3 | 0 | 3 | 0 | 213.75 |
| stock | SLB | -6 | -1.61% | -6 | 0 | -6 | 0 | 53.60 |
| stock | TECK | 3 | 1.07% | 3 | 0 | 3 | 0 | 71.12 |
| stock | VALE | 33 | 2.50% | 33 | 0 | 33 | 0 | 15.16 |
| stock | WLK | -10 | -3.73% | -10 | 0 | -10 | 0 | 74.61 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DINO | BUY | 2.0 | 0.0 | 2.0 | 96.28 | 96.76 | 1 |
| DK | BUY | 6.0 | 0.0 | 6.0 | 70.66 | 71.02 | 1 |
| PBF | BUY | 4.0 | 0.0 | 4.0 | 69.56 | 69.9 | 1 |
| PSX | BUY | 1.0 | -1.0 | 0.0 | 241.62 | 242.84 | 1 |
| SPY | BUY | 1.0 | 0.0 | 1.0 | 764.16 | 768.0 | 2 |
| XLE | SELL | -16.0 | 56.0 | 40.0 | 62.59 | 62.27 | 2 |
