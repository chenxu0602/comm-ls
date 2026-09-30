# Combined CL v4.3 + Metals targets: 2026-09-21

- Combined AUM: $20,000.00
- Total child turnover: 10.08% ($2,016.41)
- Stock child turnover (40% cap applies): 8.35%
- Hedge child turnover (uncapped): 1.73%
- Orders: 10
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | SPY | 3 | 11.43% | 3 | 0 | 3 | 0 | 761.69 |
| hedge | XLE | 97 | 31.19% | 99 | -2 | 97 | 0 | 64.31 |
| hedge | XME | -3 | -1.63% | -1 | -2 | -3 | 0 | 108.68 |
| stock | AVNT | -5 | -1.01% | -5 | 0 | -5 | 0 | 40.36 |
| stock | BHP | 7 | 3.02% | 7 | 0 | 7 | 0 | 86.27 |
| stock | CE | -9 | -2.04% | -9 | 0 | -9 | 0 | 45.41 |
| stock | DHT | 32 | 3.72% | 25 | 7 | 32 | 0 | 23.27 |
| stock | DINO | -3 | -1.74% | -3 | 0 | -3 | 0 | 115.90 |
| stock | DK | -10 | -3.91% | -9 | -1 | -10 | 0 | 78.12 |
| stock | DOW | -26 | -3.73% | -25 | 0 | -25 | -1 | 28.73 |
| stock | EMN | -6 | -1.97% | -6 | 0 | -6 | 0 | 65.69 |
| stock | ERO | -20 | -3.42% | -20 | 0 | -20 | 0 | 34.17 |
| stock | FRO | 15 | 3.86% | 10 | 5 | 15 | 0 | 51.42 |
| stock | FSUGY | 11 | 1.30% | 11 | 0 | 11 | 0 | 23.65 |
| stock | FTI | -4 | -1.44% | -4 | 0 | -4 | 0 | 72.02 |
| stock | HAL | -4 | -0.67% | -4 | 0 | -4 | 0 | 33.64 |
| stock | HUN | -46 | -2.09% | -43 | 0 | -43 | -3 | 9.09 |
| stock | INSW | 7 | 3.89% | 3 | 4 | 7 | 0 | 111.15 |
| stock | LYB | -12 | -3.72% | -12 | 0 | -12 | 0 | 61.93 |
| stock | PBF | -6 | -2.32% | -6 | 0 | -6 | 0 | 77.19 |
| stock | PSX | -3 | -4.10% | -3 | 0 | -3 | 0 | 273.13 |
| stock | RIO | 6 | 2.92% | 6 | 0 | 6 | 0 | 97.37 |
| stock | SCCO | 2 | 1.96% | 1 | 1 | 2 | 0 | 195.70 |
| stock | SLB | -6 | -1.53% | -6 | 0 | -6 | 0 | 51.12 |
| stock | STNG | 2 | 0.87% | 1 | 1 | 2 | 0 | 87.16 |
| stock | TECK | -3 | -0.98% | -3 | 0 | -3 | 0 | 65.52 |
| stock | TNK | 6 | 3.03% | 3 | 3 | 6 | 0 | 100.92 |
| stock | VALE | 28 | 1.99% | 18 | 10 | 28 | 0 | 14.21 |
| stock | WLK | -11 | -3.80% | -11 | 0 | -11 | 0 | 69.07 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DHT | BUY | 7.0 | 25.0 | 32.0 | 23.21 | 23.33 | 1 |
| DK | SELL | -1.0 | -9.0 | -10.0 | 78.32 | 77.92 | 1 |
| FRO | BUY | 5.0 | 10.0 | 15.0 | 51.29 | 51.55 | 1 |
| INSW | BUY | 4.0 | 3.0 | 7.0 | 110.87 | 111.43 | 1 |
| SCCO | BUY | 1.0 | 1.0 | 2.0 | 195.21 | 196.19 | 1 |
| STNG | BUY | 1.0 | 1.0 | 2.0 | 86.94 | 87.38 | 1 |
| TNK | BUY | 3.0 | 3.0 | 6.0 | 100.67 | 101.17 | 1 |
| VALE | BUY | 10.0 | 18.0 | 28.0 | 14.17 | 14.25 | 1 |
| XLE | SELL | -2.0 | 99.0 | 97.0 | 64.47 | 64.15 | 2 |
| XME | SELL | -2.0 | -1.0 | -3.0 | 108.95 | 108.41 | 2 |
