# Combined CL v4.3 + Metals targets: 2026-09-30

- Combined AUM: $20,000.00
- Total child turnover: 11.92% ($2,383.10)
- Stock child turnover (40% cap applies): 9.15%
- Hedge child turnover (uncapped): 2.77%
- Orders: 10
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | SPY | 4 | 15.28% | 3 | 0 | 3 | 1 | 764.20 |
| hedge | XLE | 37 | 11.38% | 44 | -9 | 35 | 2 | 61.54 |
| hedge | XME | 4 | 2.08% | 4 | 0 | 4 | 0 | 103.90 |
| stock | AVNT | -5 | -1.02% | -5 | 0 | -5 | 0 | 40.78 |
| stock | BHP | -7 | -2.97% | -7 | 0 | -7 | 0 | 84.82 |
| stock | CE | -9 | -2.02% | -9 | 0 | -9 | 0 | 44.84 |
| stock | DHT | 25 | 2.80% | 35 | -10 | 25 | 0 | 22.42 |
| stock | DINO | 3 | 1.58% | 2 | 1 | 3 | 0 | 105.59 |
| stock | DK | 11 | 3.78% | 7 | 4 | 11 | 0 | 68.73 |
| stock | DOW | -27 | -3.73% | -27 | 0 | -27 | 0 | 27.61 |
| stock | EMN | -6 | -1.97% | -6 | 0 | -6 | 0 | 65.75 |
| stock | ERO | 18 | 3.34% | 18 | 0 | 18 | 0 | 37.14 |
| stock | FRO | 11 | 2.69% | 15 | -4 | 11 | 0 | 48.93 |
| stock | FSUGY | -15 | -1.70% | -15 | 0 | -15 | 0 | 22.60 |
| stock | FTI | -4 | -1.38% | -4 | 0 | -4 | 0 | 68.85 |
| stock | HAL | -5 | -0.79% | -4 | 0 | -4 | -1 | 31.54 |
| stock | HUN | -50 | -2.10% | -47 | 0 | -47 | -3 | 8.38 |
| stock | INSW | 3 | 1.65% | 7 | -4 | 3 | 0 | 110.24 |
| stock | LYB | -13 | -3.78% | -13 | 0 | -13 | 0 | 58.18 |
| stock | PBF | 6 | 2.26% | 4 | 2 | 6 | 0 | 75.23 |
| stock | PSX | -3 | -3.78% | -3 | 0 | -3 | 0 | 252.25 |
| stock | RIO | -6 | -2.82% | -6 | 0 | -6 | 0 | 94.16 |
| stock | SCCO | -2 | -2.03% | -2 | 0 | -2 | 0 | 202.55 |
| stock | SLB | -6 | -1.50% | -6 | 0 | -6 | 0 | 49.87 |
| stock | STNG | 1 | 0.42% | 2 | -1 | 1 | 0 | 83.57 |
| stock | TECK | 3 | 0.97% | 3 | 0 | 3 | 0 | 64.85 |
| stock | TNK | 3 | 1.45% | 6 | -3 | 3 | 0 | 96.81 |
| stock | VALE | -24 | -1.60% | -24 | 0 | -24 | 0 | 13.30 |
| stock | WLK | -12 | -3.80% | -11 | -1 | -12 | 0 | 63.39 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DHT | SELL | -10.0 | 35.0 | 25.0 | 22.48 | 22.36 | 1 |
| DINO | BUY | 1.0 | 2.0 | 3.0 | 105.33 | 105.85 | 1 |
| DK | BUY | 4.0 | 7.0 | 11.0 | 68.56 | 68.9 | 1 |
| FRO | SELL | -4.0 | 15.0 | 11.0 | 49.05 | 48.81 | 1 |
| INSW | SELL | -4.0 | 7.0 | 3.0 | 110.52 | 109.96 | 1 |
| PBF | BUY | 2.0 | 4.0 | 6.0 | 75.04 | 75.42 | 1 |
| STNG | SELL | -1.0 | 2.0 | 1.0 | 83.78 | 83.36 | 1 |
| TNK | SELL | -3.0 | 6.0 | 3.0 | 97.05 | 96.57 | 1 |
| WLK | SELL | -1.0 | -11.0 | -12.0 | 63.55 | 63.23 | 1 |
| XLE | SELL | -9.0 | 44.0 | 35.0 | 61.69 | 61.39 | 2 |
