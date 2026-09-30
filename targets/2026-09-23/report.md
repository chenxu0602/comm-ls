# Combined CL v4.3 + Metals targets: 2026-09-23

- Combined AUM: $20,000.00
- Total child turnover: 8.83% ($1,765.25)
- Stock child turnover (40% cap applies): 7.18%
- Hedge child turnover (uncapped): 1.65%
- Orders: 8
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | SPY | 3 | 11.57% | 3 | 0 | 3 | 0 | 771.39 |
| hedge | XLE | 99 | 30.89% | 99 | 0 | 99 | 0 | 62.40 |
| hedge | XME | 4 | 2.20% | -3 | 3 | 0 | 4 | 109.81 |
| stock | AVNT | -5 | -1.03% | -5 | 0 | -5 | 0 | 41.26 |
| stock | BHP | 4 | 1.76% | 7 | -3 | 4 | 0 | 87.81 |
| stock | CE | -9 | -2.14% | -9 | 0 | -9 | 0 | 47.46 |
| stock | DHT | 35 | 3.74% | 32 | 3 | 35 | 0 | 21.39 |
| stock | DINO | -3 | -1.60% | -3 | 0 | -3 | 0 | 106.73 |
| stock | DK | -10 | -3.67% | -10 | 0 | -10 | 0 | 73.37 |
| stock | DOW | -27 | -3.81% | -27 | 0 | -27 | 0 | 28.19 |
| stock | EMN | -6 | -2.01% | -6 | 0 | -6 | 0 | 67.04 |
| stock | ERO | -18 | -3.36% | -20 | 2 | -18 | 0 | 37.28 |
| stock | FRO | 16 | 3.83% | 15 | 0 | 15 | 1 | 47.91 |
| stock | FSUGY | 11 | 1.31% | 11 | 0 | 11 | 0 | 23.76 |
| stock | FTI | -4 | -1.42% | -4 | 0 | -4 | 0 | 70.82 |
| stock | HAL | -5 | -0.82% | -4 | 0 | -4 | -1 | 32.84 |
| stock | HUN | -46 | -2.08% | -47 | 0 | -47 | 1 | 9.06 |
| stock | INSW | 7 | 3.64% | 7 | 0 | 7 | 0 | 103.87 |
| stock | LYB | -13 | -3.85% | -12 | -1 | -13 | 0 | 59.24 |
| stock | PBF | -6 | -2.14% | -6 | 0 | -6 | 0 | 71.42 |
| stock | PSX | -3 | -3.85% | -3 | 0 | -3 | 0 | 256.76 |
| stock | RIO | 3 | 1.46% | 6 | -3 | 3 | 0 | 97.42 |
| stock | SCCO | 0 | 0.00% | 2 | -2 | 0 | 0 | 206.18 |
| stock | SLB | -6 | -1.56% | -6 | 0 | -6 | 0 | 52.14 |
| stock | STNG | 2 | 0.82% | 2 | 0 | 2 | 0 | 82.35 |
| stock | TECK | -3 | -1.03% | -3 | 0 | -3 | 0 | 68.86 |
| stock | TNK | 6 | 2.87% | 6 | 0 | 6 | 0 | 95.63 |
| stock | VALE | 9 | 0.64% | 28 | -19 | 9 | 0 | 14.20 |
| stock | WLK | -11 | -3.78% | -11 | 0 | -11 | 0 | 68.77 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BHP | SELL | -3.0 | 7.0 | 4.0 | 88.03 | 87.59 | 1 |
| DHT | BUY | 3.0 | 32.0 | 35.0 | 21.34 | 21.44 | 1 |
| ERO | BUY | 2.0 | -20.0 | -18.0 | 37.19 | 37.37 | 1 |
| LYB | SELL | -1.0 | -12.0 | -13.0 | 59.39 | 59.09 | 1 |
| RIO | SELL | -3.0 | 6.0 | 3.0 | 97.66 | 97.18 | 1 |
| SCCO | SELL | -2.0 | 2.0 | 0.0 | 206.7 | 205.66 | 1 |
| VALE | SELL | -19.0 | 28.0 | 9.0 | 14.24 | 14.17 | 1 |
| XME | BUY | 3.0 | -3.0 | 0.0 | 109.53 | 110.08 | 2 |
