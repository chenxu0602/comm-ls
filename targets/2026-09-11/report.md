# Combined CL v4.3 + Metals targets: 2026-09-11

- Combined AUM: $20,000.00
- Total child turnover: 13.16% ($2,632.45)
- Stock child turnover (40% cap applies): 12.01%
- Hedge child turnover (uncapped): 1.15%
- Orders: 9
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | SPY | 1 | 3.79% | 1 | 0 | 1 | 0 | 757.83 |
| hedge | XLE | 103 | 33.44% | 103 | 0 | 103 | 0 | 64.93 |
| hedge | XME | -20 | -11.48% | -18 | -2 | -20 | 0 | 114.77 |
| stock | ATI | 3 | 2.99% | 1 | 2 | 3 | 0 | 199.00 |
| stock | AVNT | -5 | -1.04% | -5 | 0 | -5 | 0 | 41.72 |
| stock | BHP | 7 | 3.06% | 7 | 0 | 7 | 0 | 87.35 |
| stock | CASY | 1 | 3.14% | 0 | 1 | 1 | 0 | 627.64 |
| stock | CE | -9 | -2.06% | -9 | 0 | -9 | 0 | 45.72 |
| stock | CRS | 1 | 2.24% | 0 | 1 | 1 | 0 | 448.25 |
| stock | DINO | -3 | -1.62% | -3 | 0 | -3 | 0 | 107.72 |
| stock | DK | -10 | -3.74% | -10 | 0 | -10 | 0 | 74.89 |
| stock | DOW | -25 | -3.71% | -25 | 0 | -25 | 0 | 29.64 |
| stock | EMN | -6 | -2.05% | -6 | 0 | -6 | 0 | 68.38 |
| stock | ERO | 19 | 3.32% | 18 | 1 | 19 | 0 | 34.98 |
| stock | FSUGY | 10 | 1.22% | 14 | -4 | 10 | 0 | 24.43 |
| stock | FTI | -4 | -1.51% | -4 | 0 | -4 | 0 | 75.58 |
| stock | HAL | -4 | -0.72% | -4 | 0 | -4 | 0 | 36.07 |
| stock | HUN | -44 | -2.10% | -43 | 0 | -43 | -1 | 9.53 |
| stock | HWM | 1 | 1.14% | 1 | 0 | 1 | 0 | 227.91 |
| stock | LYB | -12 | -3.86% | -12 | 0 | -12 | 0 | 64.30 |
| stock | MUSA | 0 | 0.00% | 1 | -1 | 0 | 0 | 525.78 |
| stock | PBF | -6 | -2.31% | -6 | 0 | -6 | 0 | 77.08 |
| stock | PSX | -3 | -3.88% | -3 | 0 | -3 | 0 | 258.51 |
| stock | RIO | 6 | 2.98% | 6 | 0 | 6 | 0 | 99.39 |
| stock | SCCO | 2 | 1.94% | 1 | 1 | 2 | 0 | 194.14 |
| stock | SLB | -5 | -1.40% | -5 | 0 | -5 | 0 | 56.01 |
| stock | TECK | 3 | 0.99% | 3 | 0 | 3 | 0 | 65.90 |
| stock | VALE | 26 | 1.99% | 31 | -5 | 26 | 0 | 15.28 |
| stock | WLK | -10 | -3.58% | -10 | 0 | -10 | 0 | 71.62 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ATI | BUY | 2.0 | 1.0 | 3.0 | 198.5 | 199.5 | 1 |
| CASY | BUY | 1.0 | 0.0 | 1.0 | 626.07 | 629.21 | 1 |
| CRS | BUY | 1.0 | 0.0 | 1.0 | 447.13 | 449.37 | 1 |
| ERO | BUY | 1.0 | 18.0 | 19.0 | 34.89 | 35.07 | 1 |
| FSUGY | SELL | -4.0 | 14.0 | 10.0 | 24.49 | 24.37 | 1 |
| MUSA | SELL | -1.0 | 1.0 | 0.0 | 527.09 | 524.47 | 1 |
| SCCO | BUY | 1.0 | 1.0 | 2.0 | 193.65 | 194.63 | 1 |
| VALE | SELL | -5.0 | 31.0 | 26.0 | 15.32 | 15.24 | 1 |
| XME | SELL | -2.0 | -18.0 | -20.0 | 115.06 | 114.48 | 2 |
