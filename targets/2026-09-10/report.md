# Combined CL v4.3 + Metals targets: 2026-09-10

- Combined AUM: $20,000.00
- Total child turnover: 13.40% ($2,679.98)
- Stock child turnover (40% cap applies): 8.07%
- Hedge child turnover (uncapped): 5.33%
- Orders: 8
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | SPY | 1 | 3.81% | 2 | -1 | 1 | 0 | 762.40 |
| hedge | XLE | 103 | 33.63% | 104 | -1 | 103 | 0 | 65.31 |
| hedge | XME | -18 | -10.73% | -16 | -2 | -18 | 0 | 119.19 |
| stock | ATI | 1 | 1.03% | 1 | 0 | 1 | 0 | 206.54 |
| stock | AVNT | -5 | -1.05% | -5 | 0 | -5 | 0 | 41.90 |
| stock | BHP | 7 | 3.23% | 7 | 0 | 7 | 0 | 92.25 |
| stock | CASY | 1 | 3.15% | 0 | 1 | 1 | 0 | 629.03 |
| stock | CE | -9 | -2.00% | -9 | 0 | -9 | 0 | 44.45 |
| stock | DINO | -3 | -1.62% | -3 | 0 | -3 | 0 | 108.14 |
| stock | DK | -10 | -3.76% | -10 | 0 | -10 | 0 | 75.28 |
| stock | DOW | -26 | -3.82% | -25 | 0 | -25 | -1 | 29.40 |
| stock | EMN | -6 | -2.05% | -6 | 0 | -6 | 0 | 68.34 |
| stock | ERO | 18 | 3.44% | 18 | 0 | 18 | 0 | 38.25 |
| stock | FSUGY | 14 | 1.76% | 14 | 0 | 14 | 0 | 25.12 |
| stock | FTI | -4 | -1.56% | -4 | 0 | -4 | 0 | 77.81 |
| stock | HAL | -4 | -0.74% | -4 | 0 | -4 | 0 | 37.13 |
| stock | HUN | -44 | -2.11% | -43 | 0 | -43 | -1 | 9.58 |
| stock | HWM | 1 | 1.16% | 1 | 0 | 1 | 0 | 232.62 |
| stock | LYB | -12 | -3.87% | -12 | 0 | -12 | 0 | 64.51 |
| stock | MUSA | 0 | 0.00% | 1 | -1 | 0 | 0 | 517.46 |
| stock | PBF | -6 | -2.30% | -6 | 0 | -6 | 0 | 76.51 |
| stock | PSX | -3 | -3.91% | -3 | 0 | -3 | 0 | 260.78 |
| stock | RIO | 6 | 3.11% | 5 | 1 | 6 | 0 | 103.74 |
| stock | SCCO | 1 | 1.05% | 0 | 1 | 1 | 0 | 209.26 |
| stock | SLB | -5 | -1.43% | -5 | 0 | -5 | 0 | 57.05 |
| stock | TECK | 3 | 1.06% | 3 | 0 | 3 | 0 | 70.34 |
| stock | VALE | 31 | 2.39% | 21 | 10 | 31 | 0 | 15.44 |
| stock | WLK | -10 | -3.59% | -10 | 0 | -10 | 0 | 71.78 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CASY | BUY | 1.0 | 0.0 | 1.0 | 627.46 | 630.6 | 1 |
| MUSA | SELL | -1.0 | 1.0 | 0.0 | 518.75 | 516.17 | 1 |
| RIO | BUY | 1.0 | 5.0 | 6.0 | 103.48 | 104.0 | 1 |
| SCCO | BUY | 1.0 | 0.0 | 1.0 | 208.74 | 209.78 | 1 |
| VALE | BUY | 10.0 | 21.0 | 31.0 | 15.4 | 15.48 | 1 |
| SPY | SELL | -1.0 | 2.0 | 1.0 | 764.31 | 760.49 | 2 |
| XLE | SELL | -1.0 | 104.0 | 103.0 | 65.47 | 65.15 | 2 |
| XME | SELL | -2.0 | -16.0 | -18.0 | 119.49 | 118.89 | 2 |
