# Combined CL v4.3 + Metals targets: 2026-10-01

- Combined AUM: $20,000.00
- Total child turnover: 24.40% ($4,879.03)
- Stock child turnover (40% cap applies): 15.95%
- Hedge child turnover (uncapped): 8.44%
- Orders: 16
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | SPY | 4 | 15.25% | 3 | 1 | 4 | 0 | 762.63 |
| hedge | XLE | 36 | 11.07% | 44 | -10 | 34 | 2 | 61.50 |
| hedge | XME | 0 | 0.00% | 4 | -3 | 1 | -1 | 103.56 |
| stock | AVNT | -5 | -1.01% | -5 | 0 | -5 | 0 | 40.25 |
| stock | BHP | -6 | -2.55% | -7 | 1 | -6 | 0 | 84.84 |
| stock | CE | -9 | -2.00% | -9 | 0 | -9 | 0 | 44.37 |
| stock | DHT | 0 | 0.00% | 25 | -25 | 0 | 0 | 22.57 |
| stock | DINO | 3 | 1.61% | 2 | 1 | 3 | 0 | 107.32 |
| stock | DK | 11 | 3.93% | 7 | 4 | 11 | 0 | 71.37 |
| stock | DOW | -27 | -3.72% | -27 | 0 | -27 | 0 | 27.54 |
| stock | EMN | -6 | -1.95% | -6 | 0 | -6 | 0 | 64.84 |
| stock | ERO | 18 | 3.30% | 18 | 0 | 18 | 0 | 36.69 |
| stock | FRO | 0 | 0.00% | 11 | -11 | 0 | 0 | 49.27 |
| stock | FSUGY | -15 | -1.70% | -15 | 0 | -15 | 0 | 22.69 |
| stock | FTI | -4 | -1.36% | -4 | 0 | -4 | 0 | 67.92 |
| stock | HAL | -5 | -0.80% | -4 | 0 | -4 | -1 | 31.80 |
| stock | HUN | -50 | -2.10% | -47 | 0 | -47 | -3 | 8.40 |
| stock | INSW | 0 | 0.00% | 3 | -3 | 0 | 0 | 110.14 |
| stock | LYB | -13 | -3.74% | -13 | 0 | -13 | 0 | 57.47 |
| stock | PBF | 6 | 2.31% | 4 | 2 | 6 | 0 | 76.96 |
| stock | PSX | -2 | -2.55% | -3 | 1 | -2 | 0 | 255.31 |
| stock | RIO | -3 | -1.41% | -6 | 3 | -3 | 0 | 94.17 |
| stock | SCCO | -2 | -2.03% | -2 | 0 | -2 | 0 | 202.64 |
| stock | SLB | -6 | -1.46% | -6 | 0 | -6 | 0 | 48.72 |
| stock | STNG | 0 | 0.00% | 1 | -1 | 0 | 0 | 83.70 |
| stock | TECK | 3 | 0.99% | 3 | 0 | 3 | 0 | 65.79 |
| stock | TNK | 0 | 0.00% | 3 | -3 | 0 | 0 | 97.06 |
| stock | VALE | -13 | -0.87% | -24 | 11 | -13 | 0 | 13.41 |
| stock | WLK | -12 | -3.74% | -11 | -1 | -12 | 0 | 62.31 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BHP | BUY | 1.0 | -7.0 | -6.0 | 84.63 | 85.05 | 1 |
| DHT | SELL | -25.0 | 25.0 | 0.0 | 22.63 | 22.51 | 1 |
| DINO | BUY | 1.0 | 2.0 | 3.0 | 107.05 | 107.59 | 1 |
| DK | BUY | 4.0 | 7.0 | 11.0 | 71.19 | 71.55 | 1 |
| FRO | SELL | -11.0 | 11.0 | 0.0 | 49.39 | 49.15 | 1 |
| INSW | SELL | -3.0 | 3.0 | 0.0 | 110.42 | 109.86 | 1 |
| PBF | BUY | 2.0 | 4.0 | 6.0 | 76.77 | 77.15 | 1 |
| PSX | BUY | 1.0 | -3.0 | -2.0 | 254.67 | 255.95 | 1 |
| RIO | BUY | 3.0 | -6.0 | -3.0 | 93.93 | 94.41 | 1 |
| STNG | SELL | -1.0 | 1.0 | 0.0 | 83.91 | 83.49 | 1 |
| TNK | SELL | -3.0 | 3.0 | 0.0 | 97.3 | 96.82 | 1 |
| VALE | BUY | 11.0 | -24.0 | -13.0 | 13.38 | 13.44 | 1 |
| WLK | SELL | -1.0 | -11.0 | -12.0 | 62.47 | 62.15 | 1 |
| SPY | BUY | 1.0 | 3.0 | 4.0 | 760.72 | 764.54 | 2 |
| XLE | SELL | -10.0 | 44.0 | 34.0 | 61.65 | 61.35 | 2 |
| XME | SELL | -3.0 | 4.0 | 1.0 | 103.82 | 103.3 | 2 |
