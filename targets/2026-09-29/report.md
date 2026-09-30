# Combined CL v4.3 + Metals targets: 2026-09-29

- Combined AUM: $20,000.00
- Total child turnover: 13.97% ($2,794.80)
- Stock child turnover (40% cap applies): 6.62%
- Hedge child turnover (uncapped): 7.36%
- Orders: 6
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | SPY | 4 | 15.31% | 3 | 0 | 3 | 1 | 765.61 |
| hedge | XLE | 46 | 14.28% | 66 | -22 | 44 | 2 | 62.10 |
| hedge | XME | 4 | 2.11% | 3 | 1 | 4 | 0 | 105.42 |
| stock | AVNT | -5 | -1.03% | -5 | 0 | -5 | 0 | 41.19 |
| stock | BHP | -7 | -2.96% | -7 | 0 | -7 | 0 | 84.58 |
| stock | CE | -9 | -2.07% | -9 | 0 | -9 | 0 | 45.92 |
| stock | DHT | 34 | 3.72% | 35 | 0 | 35 | -1 | 21.90 |
| stock | DINO | 2 | 1.06% | 0 | 2 | 2 | 0 | 106.19 |
| stock | DK | 7 | 2.36% | 0 | 7 | 7 | 0 | 67.47 |
| stock | DOW | -27 | -3.77% | -27 | 0 | -27 | 0 | 27.89 |
| stock | EMN | -6 | -1.99% | -6 | 0 | -6 | 0 | 66.47 |
| stock | ERO | 18 | 3.37% | 18 | 0 | 18 | 0 | 37.41 |
| stock | FRO | 16 | 3.85% | 15 | 0 | 15 | 1 | 48.10 |
| stock | FSUGY | -15 | -1.70% | 0 | -15 | -15 | 0 | 22.73 |
| stock | FTI | -4 | -1.41% | -4 | 0 | -4 | 0 | 70.62 |
| stock | HAL | -5 | -0.81% | -4 | 0 | -4 | -1 | 32.43 |
| stock | HUN | -49 | -2.11% | -47 | 0 | -47 | -2 | 8.63 |
| stock | INSW | 7 | 3.79% | 7 | 0 | 7 | 0 | 108.31 |
| stock | LYB | -13 | -3.79% | -13 | 0 | -13 | 0 | 58.27 |
| stock | PBF | 4 | 1.49% | 0 | 4 | 4 | 0 | 74.39 |
| stock | PSX | -3 | -3.80% | -3 | 0 | -3 | 0 | 253.55 |
| stock | RIO | -6 | -2.83% | -6 | 0 | -6 | 0 | 94.41 |
| stock | SCCO | -2 | -2.03% | -2 | 0 | -2 | 0 | 202.63 |
| stock | SLB | -6 | -1.54% | -6 | 0 | -6 | 0 | 51.49 |
| stock | STNG | 2 | 0.83% | 2 | 0 | 2 | 0 | 83.19 |
| stock | TECK | 3 | 0.98% | 3 | 0 | 3 | 0 | 65.16 |
| stock | TNK | 6 | 2.87% | 6 | 0 | 6 | 0 | 95.71 |
| stock | VALE | -24 | -1.63% | -24 | 0 | -24 | 0 | 13.59 |
| stock | WLK | -11 | -3.68% | -11 | 0 | -11 | 0 | 66.84 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DINO | BUY | 2.0 | 0.0 | 2.0 | 105.92 | 106.46 | 1 |
| DK | BUY | 7.0 | 0.0 | 7.0 | 67.3 | 67.64 | 1 |
| FSUGY | SELL | -15.0 | 0.0 | -15.0 | 22.79 | 22.67 | 1 |
| PBF | BUY | 4.0 | 0.0 | 4.0 | 74.2 | 74.58 | 1 |
| XLE | SELL | -22.0 | 66.0 | 44.0 | 62.26 | 61.94 | 2 |
| XME | BUY | 1.0 | 3.0 | 4.0 | 105.16 | 105.68 | 2 |
