# Combined CL v4.2 + Metals targets: 2026-08-25

- Combined AUM: $20,000.00
- Total child turnover: 10.58% ($2,115.17)
- Stock child turnover (40% cap applies): 7.19%
- Hedge child turnover (uncapped): 3.39%
- Orders: 7
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | XLE | 72 | 22.72% | 65 | 7 | 72 | 0 | 63.11 |
| hedge | XME | -22 | -12.97% | -20 | -2 | -22 | 0 | 117.87 |
| stock | ATI | 2 | 2.10% | 2 | 0 | 2 | 0 | 209.81 |
| stock | AVNT | -5 | -1.11% | -5 | 0 | -5 | 0 | 44.42 |
| stock | BHP | 6 | 2.91% | 6 | 0 | 6 | 0 | 97.13 |
| stock | CE | -9 | -2.04% | -9 | 0 | -9 | 0 | 45.26 |
| stock | DINO | -2 | -0.95% | -3 | 1 | -2 | 0 | 95.18 |
| stock | DK | -7 | -2.38% | 0 | -7 | -7 | 0 | 68.08 |
| stock | DOW | -24 | -3.77% | -23 | 0 | -23 | -1 | 31.44 |
| stock | EMN | -6 | -2.18% | -6 | 0 | -6 | 0 | 72.69 |
| stock | ERO | 18 | 3.47% | 17 | 0 | 17 | 1 | 38.55 |
| stock | FSUGY | 10 | 1.28% | 10 | 0 | 10 | 0 | 25.64 |
| stock | HUN | -44 | -2.11% | -43 | 0 | -43 | -1 | 9.60 |
| stock | HWM | 1 | 1.32% | 1 | 0 | 1 | 0 | 263.29 |
| stock | LYB | -12 | -3.91% | -11 | 0 | -11 | -1 | 65.20 |
| stock | MUSA | 1 | 2.84% | 1 | 0 | 1 | 0 | 567.90 |
| stock | PBF | -4 | -1.39% | 0 | -4 | -4 | 0 | 69.51 |
| stock | PSX | -1 | -1.21% | -2 | 1 | -1 | 0 | 241.96 |
| stock | RIO | 6 | 3.14% | 6 | 0 | 6 | 0 | 104.80 |
| stock | SCCO | 3 | 3.21% | 3 | 0 | 3 | 0 | 214.25 |
| stock | TECK | 3 | 1.05% | 3 | 0 | 3 | 0 | 70.20 |
| stock | VALE | 23 | 1.73% | 0 | 23 | 23 | 0 | 15.04 |
| stock | WLK | -10 | -3.82% | -10 | 0 | -10 | 0 | 76.49 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DINO | BUY | 1.0 | -3.0 | -2.0 | 94.94 | 95.42 | 1 |
| DK | SELL | -7.0 | 0.0 | -7.0 | 68.25 | 67.91 | 1 |
| PBF | SELL | -4.0 | 0.0 | -4.0 | 69.68 | 69.34 | 1 |
| PSX | BUY | 1.0 | -2.0 | -1.0 | 241.36 | 242.56 | 1 |
| VALE | BUY | 23.0 | 0.0 | 23.0 | 15.0 | 15.08 | 1 |
| XLE | BUY | 7.0 | 65.0 | 72.0 | 62.95 | 63.27 | 2 |
| XME | SELL | -2.0 | -20.0 | -22.0 | 118.16 | 117.58 | 2 |
