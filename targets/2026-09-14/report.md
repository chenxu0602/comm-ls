# Combined CL v4.3 + Metals targets: 2026-09-14

- Combined AUM: $20,000.00
- Total child turnover: 1.16% ($231.99)
- Stock child turnover (40% cap applies): 0.83%
- Hedge child turnover (uncapped): 0.33%
- Orders: 3
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | SPY | 1 | 3.82% | 1 | 0 | 1 | 0 | 764.29 |
| hedge | XLE | 104 | 33.87% | 103 | 1 | 104 | 0 | 65.14 |
| hedge | XME | -20 | -11.36% | -20 | 0 | -20 | 0 | 113.63 |
| stock | ATI | 3 | 2.98% | 3 | 0 | 3 | 0 | 198.77 |
| stock | AVNT | -5 | -1.04% | -5 | 0 | -5 | 0 | 41.41 |
| stock | BHP | 7 | 3.05% | 7 | 0 | 7 | 0 | 87.15 |
| stock | CASY | 1 | 3.08% | 1 | 0 | 1 | 0 | 615.47 |
| stock | CE | -9 | -2.07% | -9 | 0 | -9 | 0 | 46.09 |
| stock | CRS | 1 | 2.22% | 1 | 0 | 1 | 0 | 443.19 |
| stock | DINO | -3 | -1.62% | -3 | 0 | -3 | 0 | 107.84 |
| stock | DK | -10 | -3.81% | -10 | 0 | -10 | 0 | 76.10 |
| stock | DOW | -26 | -3.77% | -25 | 0 | -25 | -1 | 29.03 |
| stock | EMN | -6 | -2.04% | -6 | 0 | -6 | 0 | 68.11 |
| stock | ERO | 19 | 3.37% | 19 | 0 | 19 | 0 | 35.47 |
| stock | FSUGY | 10 | 1.20% | 14 | -4 | 10 | 0 | 24.01 |
| stock | FTI | -4 | -1.53% | -4 | 0 | -4 | 0 | 76.34 |
| stock | HAL | -4 | -0.72% | -4 | 0 | -4 | 0 | 35.84 |
| stock | HUN | -44 | -2.10% | -43 | 0 | -43 | -1 | 9.54 |
| stock | HWM | 1 | 1.15% | 1 | 0 | 1 | 0 | 229.61 |
| stock | LYB | -12 | -3.82% | -12 | 0 | -12 | 0 | 63.69 |
| stock | PBF | -6 | -2.35% | -6 | 0 | -6 | 0 | 78.30 |
| stock | PSX | -3 | -3.89% | -3 | 0 | -3 | 0 | 259.47 |
| stock | RIO | 6 | 3.00% | 6 | 0 | 6 | 0 | 99.96 |
| stock | SCCO | 2 | 1.93% | 2 | 0 | 2 | 0 | 193.49 |
| stock | SLB | -5 | -1.40% | -5 | 0 | -5 | 0 | 56.06 |
| stock | TECK | 3 | 1.00% | 3 | 0 | 3 | 0 | 66.44 |
| stock | VALE | 26 | 1.98% | 26 | 0 | 26 | 0 | 15.23 |
| stock | WLK | -11 | -3.89% | -10 | -1 | -11 | 0 | 70.81 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FSUGY | SELL | -4.0 | 14.0 | 10.0 | 24.07 | 23.95 | 1 |
| WLK | SELL | -1.0 | -10.0 | -11.0 | 70.99 | 70.63 | 1 |
| XLE | BUY | 1.0 | 103.0 | 104.0 | 64.98 | 65.3 | 2 |
