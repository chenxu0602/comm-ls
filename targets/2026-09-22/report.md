# Combined CL v4.3 + Metals targets: 2026-09-22

- Combined AUM: $20,000.00
- Total child turnover: 1.08% ($216.90)
- Stock child turnover (40% cap applies): 0.46%
- Hedge child turnover (uncapped): 0.62%
- Orders: 3
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | SPY | 3 | 11.60% | 3 | 0 | 3 | 0 | 773.50 |
| hedge | XLE | 99 | 30.92% | 97 | 2 | 99 | 0 | 62.46 |
| hedge | XME | -3 | -1.64% | -3 | 0 | -3 | 0 | 109.00 |
| stock | AVNT | -5 | -1.01% | -5 | 0 | -5 | 0 | 40.44 |
| stock | BHP | 7 | 3.01% | 7 | 0 | 7 | 0 | 86.09 |
| stock | CE | -9 | -2.00% | -9 | 0 | -9 | 0 | 44.38 |
| stock | DHT | 33 | 3.70% | 32 | 0 | 32 | 1 | 22.45 |
| stock | DINO | -3 | -1.64% | -3 | 0 | -3 | 0 | 109.29 |
| stock | DK | -10 | -3.72% | -10 | 0 | -10 | 0 | 74.37 |
| stock | DOW | -27 | -3.82% | -25 | -2 | -27 | 0 | 28.27 |
| stock | EMN | -6 | -1.95% | -6 | 0 | -6 | 0 | 65.09 |
| stock | ERO | -19 | -3.30% | -20 | 0 | -20 | 1 | 34.70 |
| stock | FRO | 15 | 3.74% | 15 | 0 | 15 | 0 | 49.81 |
| stock | FSUGY | 11 | 1.31% | 11 | 0 | 11 | 0 | 23.76 |
| stock | FTI | -4 | -1.43% | -4 | 0 | -4 | 0 | 71.31 |
| stock | HAL | -4 | -0.67% | -4 | 0 | -4 | 0 | 33.39 |
| stock | HUN | -47 | -2.08% | -43 | -4 | -47 | 0 | 8.86 |
| stock | INSW | 7 | 3.82% | 7 | 0 | 7 | 0 | 109.10 |
| stock | LYB | -12 | -3.61% | -12 | 0 | -12 | 0 | 60.24 |
| stock | PBF | -6 | -2.17% | -6 | 0 | -6 | 0 | 72.48 |
| stock | PSX | -3 | -3.93% | -3 | 0 | -3 | 0 | 261.75 |
| stock | RIO | 6 | 2.91% | 6 | 0 | 6 | 0 | 97.04 |
| stock | SCCO | 2 | 1.98% | 2 | 0 | 2 | 0 | 198.06 |
| stock | SLB | -6 | -1.55% | -6 | 0 | -6 | 0 | 51.76 |
| stock | STNG | 2 | 0.86% | 2 | 0 | 2 | 0 | 86.21 |
| stock | TECK | -3 | -1.00% | -3 | 0 | -3 | 0 | 66.76 |
| stock | TNK | 6 | 2.96% | 6 | 0 | 6 | 0 | 98.76 |
| stock | VALE | 28 | 1.98% | 28 | 0 | 28 | 0 | 14.15 |
| stock | WLK | -11 | -3.73% | -11 | 0 | -11 | 0 | 67.77 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DOW | SELL | -2.0 | -25.0 | -27.0 | 28.34 | 28.2 | 1 |
| HUN | SELL | -4.0 | -43.0 | -47.0 | 8.88 | 8.84 | 1 |
| XLE | BUY | 2.0 | 97.0 | 99.0 | 62.3 | 62.62 | 2 |
