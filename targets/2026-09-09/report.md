# Combined CL v4.3 + Metals targets: 2026-09-09

- Combined AUM: $20,000.00
- Total child turnover: 16.84% ($3,367.17)
- Stock child turnover (40% cap applies): 7.00%
- Hedge child turnover (uncapped): 9.84%
- Orders: 10
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | SPY | 2 | 7.66% | 1 | 1 | 2 | 0 | 765.96 |
| hedge | XLE | 104 | 33.68% | 91 | 13 | 104 | 0 | 64.77 |
| hedge | XME | -16 | -9.60% | -19 | 3 | -16 | 0 | 119.95 |
| stock | ATI | 1 | 1.04% | 1 | 0 | 1 | 0 | 207.32 |
| stock | AVNT | -5 | -1.07% | -5 | 0 | -5 | 0 | 42.61 |
| stock | BHP | 7 | 3.22% | 6 | 1 | 7 | 0 | 91.99 |
| stock | CE | -9 | -2.00% | -9 | 0 | -9 | 0 | 44.53 |
| stock | DINO | -3 | -1.62% | -3 | 0 | -3 | 0 | 108.31 |
| stock | DK | -10 | -3.78% | -10 | 0 | -10 | 0 | 75.67 |
| stock | DOW | -25 | -3.70% | -25 | 0 | -25 | 0 | 29.57 |
| stock | EMN | -6 | -2.11% | -6 | 0 | -6 | 0 | 70.39 |
| stock | ERO | 18 | 3.41% | 19 | -1 | 18 | 0 | 37.91 |
| stock | FSUGY | 14 | 1.78% | 10 | 4 | 14 | 0 | 25.46 |
| stock | FTI | -4 | -1.56% | -4 | 0 | -4 | 0 | 78.16 |
| stock | HAL | -4 | -0.74% | -4 | 0 | -4 | 0 | 36.80 |
| stock | HUN | -43 | -2.11% | -43 | 0 | -43 | 0 | 9.80 |
| stock | HWM | 1 | 1.16% | 1 | 0 | 1 | 0 | 231.53 |
| stock | LYB | -12 | -3.88% | -12 | 0 | -12 | 0 | 64.59 |
| stock | MUSA | 1 | 2.59% | 1 | 0 | 1 | 0 | 517.81 |
| stock | PBF | -6 | -2.30% | -6 | 0 | -6 | 0 | 76.77 |
| stock | PSX | -3 | -3.89% | 0 | -3 | -3 | 0 | 259.14 |
| stock | RIO | 5 | 2.60% | 6 | -1 | 5 | 0 | 103.83 |
| stock | SCCO | 0 | 0.00% | 1 | -1 | 0 | 0 | 208.56 |
| stock | SLB | -5 | -1.43% | -5 | 0 | -5 | 0 | 57.10 |
| stock | TECK | 3 | 1.08% | 3 | 0 | 3 | 0 | 71.97 |
| stock | VALE | 21 | 1.63% | 16 | 5 | 21 | 0 | 15.56 |
| stock | WLK | -10 | -3.74% | -10 | 0 | -10 | 0 | 74.75 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BHP | BUY | 1.0 | 6.0 | 7.0 | 91.76 | 92.22 | 1 |
| ERO | SELL | -1.0 | 19.0 | 18.0 | 38.0 | 37.82 | 1 |
| FSUGY | BUY | 4.0 | 10.0 | 14.0 | 25.4 | 25.52 | 1 |
| PSX | SELL | -3.0 | 0.0 | -3.0 | 259.79 | 258.49 | 1 |
| RIO | SELL | -1.0 | 6.0 | 5.0 | 104.09 | 103.57 | 1 |
| SCCO | SELL | -1.0 | 1.0 | 0.0 | 209.08 | 208.04 | 1 |
| VALE | BUY | 5.0 | 16.0 | 21.0 | 15.52 | 15.6 | 1 |
| SPY | BUY | 1.0 | 1.0 | 2.0 | 764.05 | 767.87 | 2 |
| XLE | BUY | 13.0 | 91.0 | 104.0 | 64.61 | 64.93 | 2 |
| XME | BUY | 3.0 | -19.0 | -16.0 | 119.65 | 120.25 | 2 |
