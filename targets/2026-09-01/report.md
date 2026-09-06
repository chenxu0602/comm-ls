# Combined CL v4.3 + Metals targets: 2026-09-01

- Combined AUM: $20,000.00
- Total child turnover: 12.22% ($2,443.47)
- Stock child turnover (40% cap applies): 6.88%
- Hedge child turnover (uncapped): 5.34%
- Orders: 10
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | SPY | 1 | 3.84% | 1 | 0 | 1 | 0 | 767.05 |
| hedge | XLE | 32 | 10.23% | 19 | 13 | 32 | 0 | 63.96 |
| hedge | XME | -18 | -10.63% | -20 | 2 | -18 | 0 | 118.13 |
| stock | ATI | 2 | 2.04% | 2 | 0 | 2 | 0 | 204.20 |
| stock | AVNT | -5 | -1.10% | -5 | 0 | -5 | 0 | 44.06 |
| stock | BHP | 6 | 2.82% | 6 | 0 | 6 | 0 | 93.92 |
| stock | CE | -9 | -2.05% | -9 | 0 | -9 | 0 | 45.48 |
| stock | DINO | 2 | 1.02% | 3 | -1 | 2 | 0 | 101.61 |
| stock | DK | 6 | 2.23% | 11 | -5 | 6 | 0 | 74.34 |
| stock | DOW | -25 | -3.82% | -25 | 0 | -25 | 0 | 30.52 |
| stock | EMN | -6 | -2.17% | -6 | 0 | -6 | 0 | 72.44 |
| stock | ERO | 18 | 3.34% | 17 | 1 | 18 | 0 | 37.13 |
| stock | FSUGY | 13 | 1.64% | 10 | 3 | 13 | 0 | 25.16 |
| stock | FTI | -4 | -1.56% | -4 | 0 | -4 | 0 | 78.15 |
| stock | HAL | -4 | -0.74% | -4 | 0 | -4 | 0 | 36.85 |
| stock | HUN | -44 | -2.11% | -43 | 0 | -43 | -1 | 9.58 |
| stock | HWM | 1 | 1.22% | 1 | 0 | 1 | 0 | 244.95 |
| stock | LYB | -12 | -3.90% | -12 | 0 | -12 | 0 | 65.08 |
| stock | MUSA | 1 | 2.58% | 1 | 0 | 1 | 0 | 515.39 |
| stock | PBF | 4 | 1.46% | 6 | -2 | 4 | 0 | 72.99 |
| stock | PSX | 2 | 2.47% | 2 | 0 | 2 | 0 | 246.58 |
| stock | RIO | 6 | 3.08% | 6 | 0 | 6 | 0 | 102.50 |
| stock | SCCO | 1 | 1.04% | 3 | -2 | 1 | 0 | 208.87 |
| stock | SLB | -5 | -1.50% | -6 | 1 | -5 | 0 | 60.10 |
| stock | TECK | 3 | 1.02% | 3 | 0 | 3 | 0 | 68.12 |
| stock | VALE | 27 | 2.04% | 16 | 11 | 27 | 0 | 15.09 |
| stock | WLK | -10 | -3.75% | -10 | 0 | -10 | 0 | 75.07 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DINO | SELL | -1.0 | 3.0 | 2.0 | 101.86 | 101.36 | 1 |
| DK | SELL | -5.0 | 11.0 | 6.0 | 74.53 | 74.15 | 1 |
| ERO | BUY | 1.0 | 17.0 | 18.0 | 37.04 | 37.22 | 1 |
| FSUGY | BUY | 3.0 | 10.0 | 13.0 | 25.1 | 25.22 | 1 |
| PBF | SELL | -2.0 | 6.0 | 4.0 | 73.17 | 72.81 | 1 |
| SCCO | SELL | -2.0 | 3.0 | 1.0 | 209.39 | 208.35 | 1 |
| SLB | BUY | 1.0 | -6.0 | -5.0 | 59.95 | 60.25 | 1 |
| VALE | BUY | 11.0 | 16.0 | 27.0 | 15.05 | 15.13 | 1 |
| XLE | BUY | 13.0 | 19.0 | 32.0 | 63.8 | 64.12 | 2 |
| XME | BUY | 2.0 | -20.0 | -18.0 | 117.83 | 118.43 | 2 |
