# Combined CL v4.2 + Metals targets: 2026-08-26

- Combined AUM: $20,000.00
- Total child turnover: 8.72% ($1,743.37)
- Stock child turnover (40% cap applies): 3.77%
- Hedge child turnover (uncapped): 4.95%
- Orders: 7
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | XLE | 58 | 18.00% | 72 | -14 | 58 | 0 | 62.06 |
| hedge | XME | -21 | -12.70% | -22 | 1 | -21 | 0 | 120.94 |
| stock | ATI | 2 | 2.15% | 2 | 0 | 2 | 0 | 215.23 |
| stock | AVNT | -5 | -1.12% | -5 | 0 | -5 | 0 | 44.62 |
| stock | BHP | 6 | 2.96% | 6 | 0 | 6 | 0 | 98.69 |
| stock | CE | -9 | -2.00% | -9 | 0 | -9 | 0 | 44.52 |
| stock | DINO | -1 | -0.47% | -2 | 1 | -1 | 0 | 93.24 |
| stock | DK | -2 | -0.68% | -7 | 5 | -2 | 0 | 67.59 |
| stock | DOW | -25 | -3.77% | -23 | -2 | -25 | 0 | 30.16 |
| stock | EMN | -6 | -2.16% | -6 | 0 | -6 | 0 | 72.02 |
| stock | ERO | 17 | 3.43% | 17 | 0 | 17 | 0 | 40.40 |
| stock | FSUGY | 10 | 1.27% | 10 | 0 | 10 | 0 | 25.49 |
| stock | HUN | -44 | -2.10% | -43 | 0 | -43 | -1 | 9.53 |
| stock | HWM | 1 | 1.32% | 1 | 0 | 1 | 0 | 264.04 |
| stock | LYB | -12 | -3.75% | -11 | -1 | -12 | 0 | 62.55 |
| stock | MUSA | 1 | 2.72% | 1 | 0 | 1 | 0 | 544.31 |
| stock | PBF | -1 | -0.33% | -4 | 3 | -1 | 0 | 66.51 |
| stock | PSX | -1 | -1.18% | -1 | 0 | -1 | 0 | 236.90 |
| stock | RIO | 6 | 3.20% | 6 | 0 | 6 | 0 | 106.81 |
| stock | SCCO | 3 | 3.30% | 3 | 0 | 3 | 0 | 219.70 |
| stock | TECK | 3 | 1.07% | 3 | 0 | 3 | 0 | 71.62 |
| stock | VALE | 23 | 1.76% | 23 | 0 | 23 | 0 | 15.33 |
| stock | WLK | -10 | -3.74% | -10 | 0 | -10 | 0 | 74.80 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DINO | BUY | 1.0 | -2.0 | -1.0 | 93.01 | 93.47 | 1 |
| DK | BUY | 5.0 | -7.0 | -2.0 | 67.42 | 67.76 | 1 |
| DOW | SELL | -2.0 | -23.0 | -25.0 | 30.24 | 30.08 | 1 |
| LYB | SELL | -1.0 | -11.0 | -12.0 | 62.71 | 62.39 | 1 |
| PBF | BUY | 3.0 | -4.0 | -1.0 | 66.34 | 66.68 | 1 |
| XLE | SELL | -14.0 | 72.0 | 58.0 | 62.22 | 61.9 | 2 |
| XME | BUY | 1.0 | -22.0 | -21.0 | 120.64 | 121.24 | 2 |
