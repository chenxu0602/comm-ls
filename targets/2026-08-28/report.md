# Combined CL v4.3 + Metals targets: 2026-08-28

- Combined AUM: $20,000.00
- Total child turnover: 16.06% ($3,212.88)
- Stock child turnover (40% cap applies): 5.67%
- Hedge child turnover (uncapped): 10.40%
- Orders: 6
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | SPY | 0 | 0.00% | 1 | -1 | 0 | 0 | 771.10 |
| hedge | XLE | 19 | 5.92% | 40 | -21 | 19 | 0 | 62.29 |
| hedge | XME | -22 | -13.53% | -22 | 0 | -22 | 0 | 123.00 |
| stock | ATI | 2 | 2.15% | 2 | 0 | 2 | 0 | 214.52 |
| stock | AVNT | -5 | -1.11% | -5 | 0 | -5 | 0 | 44.26 |
| stock | BHP | 6 | 2.89% | 6 | 0 | 6 | 0 | 96.37 |
| stock | CE | -9 | -2.02% | -9 | 0 | -9 | 0 | 44.87 |
| stock | DINO | 3 | 1.46% | 2 | 1 | 3 | 0 | 97.00 |
| stock | DK | 11 | 3.86% | 6 | 5 | 11 | 0 | 70.26 |
| stock | DOW | -25 | -3.79% | -25 | 0 | -25 | 0 | 30.33 |
| stock | EMN | -6 | -2.18% | -6 | 0 | -6 | 0 | 72.65 |
| stock | ERO | 17 | 3.38% | 17 | 0 | 17 | 0 | 39.82 |
| stock | FSUGY | 13 | 1.66% | 13 | 0 | 13 | 0 | 25.54 |
| stock | FTI | -4 | -1.53% | -4 | 0 | -4 | 0 | 76.32 |
| stock | HAL | -4 | -0.71% | -4 | 0 | -4 | 0 | 35.49 |
| stock | HUN | -44 | -2.12% | -43 | 0 | -43 | -1 | 9.65 |
| stock | HWM | 1 | 1.34% | 1 | 0 | 1 | 0 | 267.65 |
| stock | LYB | -12 | -3.78% | -12 | 0 | -12 | 0 | 63.06 |
| stock | MUSA | 1 | 2.55% | 1 | 0 | 1 | 0 | 509.08 |
| stock | PBF | 7 | 2.40% | 4 | 3 | 7 | 0 | 68.59 |
| stock | PSX | 2 | 2.40% | 0 | 2 | 2 | 0 | 239.81 |
| stock | RIO | 6 | 3.14% | 6 | 0 | 6 | 0 | 104.78 |
| stock | SCCO | 3 | 3.24% | 3 | 0 | 3 | 0 | 216.28 |
| stock | SLB | -5 | -1.38% | -6 | 0 | -6 | 1 | 55.01 |
| stock | TECK | 3 | 1.06% | 3 | 0 | 3 | 0 | 70.54 |
| stock | VALE | 33 | 2.53% | 33 | 0 | 33 | 0 | 15.31 |
| stock | WLK | -10 | -3.70% | -10 | 0 | -10 | 0 | 73.93 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DINO | BUY | 1.0 | 2.0 | 3.0 | 96.76 | 97.24 | 1 |
| DK | BUY | 5.0 | 6.0 | 11.0 | 70.08 | 70.44 | 1 |
| PBF | BUY | 3.0 | 4.0 | 7.0 | 68.42 | 68.76 | 1 |
| PSX | BUY | 2.0 | 0.0 | 2.0 | 239.21 | 240.41 | 1 |
| SPY | SELL | -1.0 | 1.0 | 0.0 | 773.03 | 769.17 | 2 |
| XLE | SELL | -21.0 | 40.0 | 19.0 | 62.45 | 62.13 | 2 |
