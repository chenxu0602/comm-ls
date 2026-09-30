# Combined CL v4.3 + Metals targets: 2026-09-28

- Combined AUM: $20,000.00
- Total child turnover: 18.49% ($3,697.19)
- Stock child turnover (40% cap applies): 8.12%
- Hedge child turnover (uncapped): 10.36%
- Orders: 10
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | SPY | 4 | 15.43% | 4 | -1 | 3 | 1 | 771.35 |
| hedge | XLE | 59 | 18.30% | 73 | -7 | 66 | -7 | 62.04 |
| hedge | XME | 4 | 2.17% | 11 | -8 | 3 | 1 | 108.33 |
| stock | AVNT | -5 | -1.03% | -5 | 0 | -5 | 0 | 41.28 |
| stock | BHP | -7 | -2.97% | -6 | -1 | -7 | 0 | 84.97 |
| stock | CE | -9 | -2.12% | -9 | 0 | -9 | 0 | 47.09 |
| stock | DHT | 34 | 3.70% | 35 | 0 | 35 | -1 | 21.78 |
| stock | DINO | 1 | 0.53% | -1 | 1 | 0 | 1 | 106.82 |
| stock | DK | 2 | 0.68% | -2 | 2 | 0 | 2 | 67.84 |
| stock | DOW | -27 | -3.78% | -27 | 0 | -27 | 0 | 28.02 |
| stock | EMN | -6 | -2.01% | -6 | 0 | -6 | 0 | 66.97 |
| stock | ERO | 18 | 3.41% | 0 | 18 | 18 | 0 | 37.87 |
| stock | FRO | 16 | 3.82% | 15 | 0 | 15 | 1 | 47.73 |
| stock | FSUGY | -15 | -1.72% | 0 | -15 | -15 | 0 | 22.93 |
| stock | FTI | -4 | -1.42% | -4 | 0 | -4 | 0 | 70.99 |
| stock | HAL | -5 | -0.82% | -4 | 0 | -4 | -1 | 32.76 |
| stock | HUN | -47 | -2.09% | -47 | 0 | -47 | 0 | 8.90 |
| stock | INSW | 7 | 3.70% | 7 | 0 | 7 | 0 | 105.64 |
| stock | LYB | -13 | -3.78% | -13 | 0 | -13 | 0 | 58.14 |
| stock | PBF | 1 | 0.37% | -1 | 1 | 0 | 1 | 73.69 |
| stock | PSX | -3 | -3.84% | -3 | 0 | -3 | 0 | 255.75 |
| stock | RIO | -6 | -2.84% | -6 | 0 | -6 | 0 | 94.56 |
| stock | SCCO | -2 | -2.04% | -2 | 0 | -2 | 0 | 203.92 |
| stock | SLB | -6 | -1.55% | -6 | 0 | -6 | 0 | 51.54 |
| stock | STNG | 2 | 0.81% | 2 | 0 | 2 | 0 | 81.49 |
| stock | TECK | 3 | 0.99% | 0 | 3 | 3 | 0 | 66.05 |
| stock | TNK | 6 | 2.82% | 6 | 0 | 6 | 0 | 94.07 |
| stock | VALE | -24 | -1.63% | -24 | 0 | -24 | 0 | 13.61 |
| stock | WLK | -11 | -3.72% | -11 | 0 | -11 | 0 | 67.71 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BHP | SELL | -1.0 | -6.0 | -7.0 | 85.18 | 84.76 | 1 |
| DINO | BUY | 1.0 | -1.0 | 0.0 | 106.55 | 107.09 | 1 |
| DK | BUY | 2.0 | -2.0 | 0.0 | 67.67 | 68.01 | 1 |
| ERO | BUY | 18.0 | 0.0 | 18.0 | 37.78 | 37.96 | 1 |
| FSUGY | SELL | -15.0 | 0.0 | -15.0 | 22.99 | 22.87 | 1 |
| PBF | BUY | 1.0 | -1.0 | 0.0 | 73.51 | 73.87 | 1 |
| TECK | BUY | 3.0 | 0.0 | 3.0 | 65.88 | 66.22 | 1 |
| SPY | SELL | -1.0 | 4.0 | 3.0 | 773.28 | 769.42 | 2 |
| XLE | SELL | -7.0 | 73.0 | 66.0 | 62.2 | 61.88 | 2 |
| XME | SELL | -8.0 | 11.0 | 3.0 | 108.6 | 108.06 | 2 |
