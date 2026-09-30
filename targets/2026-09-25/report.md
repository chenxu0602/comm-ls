# Combined CL v4.3 + Metals targets: 2026-09-25

- Combined AUM: $20,000.00
- Total child turnover: 23.06% ($4,612.90)
- Stock child turnover (40% cap applies): 17.06%
- Hedge child turnover (uncapped): 6.00%
- Orders: 12
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | SPY | 5 | 19.18% | 4 | 0 | 4 | 1 | 767.18 |
| hedge | XLE | 72 | 22.54% | 87 | -14 | 73 | -1 | 62.60 |
| hedge | XME | 12 | 6.48% | 8 | 3 | 11 | 1 | 107.96 |
| stock | AVNT | -5 | -1.02% | -5 | 0 | -5 | 0 | 40.78 |
| stock | BHP | -7 | -2.98% | 0 | -6 | -6 | -1 | 85.09 |
| stock | CE | -9 | -2.14% | -9 | 0 | -9 | 0 | 47.56 |
| stock | DHT | 35 | 3.79% | 35 | 0 | 35 | 0 | 21.68 |
| stock | DINO | -1 | -0.53% | -2 | 1 | -1 | 0 | 105.79 |
| stock | DK | -2 | -0.67% | -6 | 4 | -2 | 0 | 66.91 |
| stock | DOW | -26 | -3.71% | -27 | 0 | -27 | 1 | 28.56 |
| stock | EMN | -6 | -1.99% | -6 | 0 | -6 | 0 | 66.19 |
| stock | ERO | 0 | 0.00% | -18 | 18 | 0 | 0 | 37.11 |
| stock | FRO | 16 | 3.84% | 15 | 0 | 15 | 1 | 47.97 |
| stock | FSUGY | -15 | -1.76% | 0 | -15 | -15 | 0 | 23.44 |
| stock | FTI | -4 | -1.42% | -4 | 0 | -4 | 0 | 70.95 |
| stock | HAL | -5 | -0.82% | -4 | 0 | -4 | -1 | 32.76 |
| stock | HUN | -48 | -2.11% | -47 | 0 | -47 | -1 | 8.79 |
| stock | INSW | 7 | 3.67% | 7 | 0 | 7 | 0 | 104.85 |
| stock | LYB | -12 | -3.61% | -13 | 0 | -13 | 1 | 60.18 |
| stock | PBF | -1 | -0.36% | -4 | 3 | -1 | 0 | 71.90 |
| stock | PSX | -3 | -3.84% | -3 | 0 | -3 | 0 | 255.87 |
| stock | RIO | -6 | -2.83% | 0 | -6 | -6 | 0 | 94.47 |
| stock | SCCO | -2 | -2.02% | -1 | -1 | -2 | 0 | 201.58 |
| stock | SLB | -6 | -1.54% | -6 | 0 | -6 | 0 | 51.43 |
| stock | STNG | 2 | 0.81% | 2 | 0 | 2 | 0 | 80.96 |
| stock | TECK | 0 | 0.00% | -3 | 3 | 0 | 0 | 66.51 |
| stock | TNK | 6 | 2.82% | 6 | 0 | 6 | 0 | 94.08 |
| stock | VALE | -24 | -1.63% | 0 | -24 | -24 | 0 | 13.56 |
| stock | WLK | -11 | -3.67% | -11 | 0 | -11 | 0 | 66.76 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BHP | SELL | -6.0 | 0.0 | -6.0 | 85.3 | 84.88 | 1 |
| DINO | BUY | 1.0 | -2.0 | -1.0 | 105.53 | 106.05 | 1 |
| DK | BUY | 4.0 | -6.0 | -2.0 | 66.74 | 67.08 | 1 |
| ERO | BUY | 18.0 | -18.0 | 0.0 | 37.02 | 37.2 | 1 |
| FSUGY | SELL | -15.0 | 0.0 | -15.0 | 23.5 | 23.38 | 1 |
| PBF | BUY | 3.0 | -4.0 | -1.0 | 71.72 | 72.08 | 1 |
| RIO | SELL | -6.0 | 0.0 | -6.0 | 94.71 | 94.23 | 1 |
| SCCO | SELL | -1.0 | -1.0 | -2.0 | 202.08 | 201.08 | 1 |
| TECK | BUY | 3.0 | -3.0 | 0.0 | 66.34 | 66.68 | 1 |
| VALE | SELL | -24.0 | 0.0 | -24.0 | 13.59 | 13.53 | 1 |
| XLE | SELL | -14.0 | 87.0 | 73.0 | 62.76 | 62.44 | 2 |
| XME | BUY | 3.0 | 8.0 | 11.0 | 107.69 | 108.23 | 2 |
