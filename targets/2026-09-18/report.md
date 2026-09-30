# Combined CL v4.3 + Metals targets: 2026-09-18

- Combined AUM: $20,000.00
- Total child turnover: 23.90% ($4,780.84)
- Stock child turnover (40% cap applies): 13.47%
- Hedge child turnover (uncapped): 10.43%
- Orders: 10
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | SPY | 3 | 11.44% | 2 | 1 | 3 | 0 | 762.60 |
| hedge | XLE | 99 | 31.92% | 104 | -5 | 99 | 0 | 64.48 |
| hedge | XME | -1 | -0.56% | -10 | 9 | -1 | 0 | 111.32 |
| stock | AVNT | -5 | -1.01% | -5 | 0 | -5 | 0 | 40.58 |
| stock | BHP | 7 | 3.03% | 7 | 0 | 7 | 0 | 86.56 |
| stock | CE | -9 | -2.11% | -9 | 0 | -9 | 0 | 46.81 |
| stock | DHT | 25 | 2.85% | 0 | 25 | 25 | 0 | 22.82 |
| stock | DINO | -3 | -1.75% | -3 | 0 | -3 | 0 | 116.62 |
| stock | DK | -9 | -3.67% | -9 | 0 | -9 | 0 | 81.55 |
| stock | DOW | -25 | -3.69% | -25 | 0 | -25 | 0 | 29.49 |
| stock | EMN | -6 | -1.99% | -6 | 0 | -6 | 0 | 66.24 |
| stock | ERO | -20 | -3.33% | 0 | -20 | -20 | 0 | 33.28 |
| stock | FRO | 10 | 2.70% | 0 | 10 | 10 | 0 | 54.03 |
| stock | FSUGY | 10 | 1.19% | 11 | 0 | 11 | -1 | 23.81 |
| stock | FTI | -4 | -1.45% | -4 | 0 | -4 | 0 | 72.74 |
| stock | HAL | -4 | -0.68% | -4 | 0 | -4 | 0 | 34.03 |
| stock | HUN | -46 | -2.10% | -43 | 0 | -43 | -3 | 9.12 |
| stock | INSW | 3 | 1.66% | 0 | 3 | 3 | 0 | 110.53 |
| stock | LYB | -12 | -3.85% | -12 | 0 | -12 | 0 | 64.25 |
| stock | PBF | -6 | -2.31% | -6 | 0 | -6 | 0 | 77.16 |
| stock | PSX | -3 | -4.11% | -3 | 0 | -3 | 0 | 274.21 |
| stock | RIO | 6 | 2.94% | 6 | 0 | 6 | 0 | 98.04 |
| stock | SCCO | 1 | 0.98% | 1 | 0 | 1 | 0 | 196.11 |
| stock | SLB | -6 | -1.56% | -6 | 0 | -6 | 0 | 52.08 |
| stock | STNG | 1 | 0.44% | 0 | 1 | 1 | 0 | 87.85 |
| stock | TECK | -3 | -0.98% | 0 | -3 | -3 | 0 | 65.22 |
| stock | TNK | 3 | 1.51% | 0 | 3 | 3 | 0 | 100.82 |
| stock | VALE | 17 | 1.23% | 18 | 0 | 18 | -1 | 14.47 |
| stock | WLK | -11 | -3.88% | -11 | 0 | -11 | 0 | 70.57 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DHT | BUY | 25.0 | 0.0 | 25.0 | 22.76 | 22.88 | 1 |
| ERO | SELL | -20.0 | 0.0 | -20.0 | 33.36 | 33.2 | 1 |
| FRO | BUY | 10.0 | 0.0 | 10.0 | 53.89 | 54.17 | 1 |
| INSW | BUY | 3.0 | 0.0 | 3.0 | 110.25 | 110.81 | 1 |
| STNG | BUY | 1.0 | 0.0 | 1.0 | 87.63 | 88.07 | 1 |
| TECK | SELL | -3.0 | 0.0 | -3.0 | 65.38 | 65.06 | 1 |
| TNK | BUY | 3.0 | 0.0 | 3.0 | 100.57 | 101.07 | 1 |
| SPY | BUY | 1.0 | 2.0 | 3.0 | 760.69 | 764.51 | 2 |
| XLE | SELL | -5.0 | 104.0 | 99.0 | 64.64 | 64.32 | 2 |
| XME | BUY | 9.0 | -10.0 | -1.0 | 111.04 | 111.6 | 2 |
