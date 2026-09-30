# Combined CL v4.3 + Metals targets: 2026-09-24

- Combined AUM: $20,000.00
- Total child turnover: 20.69% ($4,138.17)
- Stock child turnover (40% cap applies): 8.73%
- Hedge child turnover (uncapped): 11.96%
- Orders: 11
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | SPY | 4 | 15.36% | 3 | 1 | 4 | 0 | 767.81 |
| hedge | XLE | 85 | 26.51% | 99 | -12 | 87 | -2 | 62.37 |
| hedge | XME | 16 | 8.77% | 0 | 8 | 8 | 8 | 109.58 |
| stock | AVNT | -5 | -1.02% | -5 | 0 | -5 | 0 | 40.97 |
| stock | BHP | -4 | -1.70% | 4 | -4 | 0 | -4 | 84.95 |
| stock | CE | -9 | -2.18% | -9 | 0 | -9 | 0 | 48.49 |
| stock | DHT | 35 | 3.72% | 35 | 0 | 35 | 0 | 21.28 |
| stock | DINO | -2 | -1.06% | -3 | 1 | -2 | 0 | 106.14 |
| stock | DK | -6 | -2.17% | -10 | 4 | -6 | 0 | 72.26 |
| stock | DOW | -26 | -3.72% | -27 | 0 | -27 | 1 | 28.65 |
| stock | EMN | -6 | -2.00% | -6 | 0 | -6 | 0 | 66.80 |
| stock | ERO | -19 | -3.47% | -18 | 0 | -18 | -1 | 36.48 |
| stock | FRO | 16 | 3.80% | 15 | 0 | 15 | 1 | 47.56 |
| stock | FSUGY | -11 | -1.29% | 11 | -11 | 0 | -11 | 23.39 |
| stock | FTI | -4 | -1.42% | -4 | 0 | -4 | 0 | 71.24 |
| stock | HAL | -5 | -0.83% | -4 | 0 | -4 | -1 | 33.01 |
| stock | HUN | -46 | -2.09% | -47 | 0 | -47 | 1 | 9.10 |
| stock | INSW | 7 | 3.57% | 7 | 0 | 7 | 0 | 101.96 |
| stock | LYB | -13 | -3.90% | -13 | 0 | -13 | 0 | 59.97 |
| stock | PBF | -4 | -1.41% | -6 | 2 | -4 | 0 | 70.47 |
| stock | PSX | -3 | -3.85% | -3 | 0 | -3 | 0 | 256.48 |
| stock | RIO | -3 | -1.43% | 3 | -3 | 0 | -3 | 95.25 |
| stock | SCCO | -2 | -2.02% | 0 | -1 | -1 | -1 | 201.94 |
| stock | SLB | -6 | -1.56% | -6 | 0 | -6 | 0 | 51.87 |
| stock | STNG | 2 | 0.81% | 2 | 0 | 2 | 0 | 81.25 |
| stock | TECK | -3 | -1.00% | -3 | 0 | -3 | 0 | 66.80 |
| stock | TNK | 6 | 2.84% | 6 | 0 | 6 | 0 | 94.54 |
| stock | VALE | -9 | -0.62% | 9 | -9 | 0 | -9 | 13.82 |
| stock | WLK | -11 | -3.76% | -11 | 0 | -11 | 0 | 68.42 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BHP | SELL | -4.0 | 4.0 | 0.0 | 85.16 | 84.74 | 1 |
| DINO | BUY | 1.0 | -3.0 | -2.0 | 105.87 | 106.41 | 1 |
| DK | BUY | 4.0 | -10.0 | -6.0 | 72.08 | 72.44 | 1 |
| FSUGY | SELL | -11.0 | 11.0 | 0.0 | 23.45 | 23.33 | 1 |
| PBF | BUY | 2.0 | -6.0 | -4.0 | 70.29 | 70.65 | 1 |
| RIO | SELL | -3.0 | 3.0 | 0.0 | 95.49 | 95.01 | 1 |
| SCCO | SELL | -1.0 | 0.0 | -1.0 | 202.44 | 201.44 | 1 |
| VALE | SELL | -9.0 | 9.0 | 0.0 | 13.85 | 13.79 | 1 |
| SPY | BUY | 1.0 | 3.0 | 4.0 | 765.89 | 769.73 | 2 |
| XLE | SELL | -12.0 | 99.0 | 87.0 | 62.53 | 62.21 | 2 |
| XME | BUY | 8.0 | 0.0 | 8.0 | 109.31 | 109.85 | 2 |
