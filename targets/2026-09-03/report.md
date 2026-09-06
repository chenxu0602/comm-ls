# Combined CL v4.3 + Metals targets: 2026-09-03

- Combined AUM: $20,000.00
- Total child turnover: 6.48% ($1,295.03)
- Stock child turnover (40% cap applies): 2.57%
- Hedge child turnover (uncapped): 3.91%
- Orders: 8
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | SPY | 1 | 3.83% | 1 | 0 | 1 | 0 | 765.16 |
| hedge | XLE | 61 | 19.86% | 49 | 12 | 61 | 0 | 65.10 |
| hedge | XME | -18 | -10.75% | -18 | 0 | -18 | 0 | 119.46 |
| stock | ATI | 1 | 1.01% | 1 | 0 | 1 | 0 | 201.69 |
| stock | AVNT | -5 | -1.09% | -5 | 0 | -5 | 0 | 43.59 |
| stock | BHP | 6 | 2.80% | 6 | 0 | 6 | 0 | 93.43 |
| stock | CE | -9 | -2.10% | -9 | 0 | -9 | 0 | 46.66 |
| stock | DINO | -1 | -0.53% | 1 | -1 | 0 | -1 | 106.06 |
| stock | DK | -2 | -0.71% | 2 | -2 | 0 | -2 | 71.45 |
| stock | DOW | -24 | -3.75% | -25 | 0 | -25 | 1 | 31.28 |
| stock | EMN | -6 | -2.16% | -6 | 0 | -6 | 0 | 72.16 |
| stock | ERO | 19 | 3.30% | 18 | 1 | 19 | 0 | 34.76 |
| stock | FSUGY | 10 | 1.21% | 13 | -3 | 10 | 0 | 24.11 |
| stock | FTI | -4 | -1.59% | -4 | 0 | -4 | 0 | 79.67 |
| stock | HAL | -4 | -0.75% | -4 | 0 | -4 | 0 | 37.63 |
| stock | HUN | -43 | -2.09% | -43 | 0 | -43 | 0 | 9.71 |
| stock | HWM | 1 | 1.26% | 1 | 0 | 1 | 0 | 252.96 |
| stock | LYB | -11 | -3.66% | -12 | 1 | -11 | 0 | 66.57 |
| stock | MUSA | 1 | 2.60% | 1 | 0 | 1 | 0 | 520.47 |
| stock | PBF | -1 | -0.38% | 1 | -1 | 0 | -1 | 75.48 |
| stock | PSX | 1 | 1.28% | 1 | 0 | 1 | 0 | 256.09 |
| stock | RIO | 6 | 3.08% | 6 | 0 | 6 | 0 | 102.75 |
| stock | SCCO | 1 | 1.02% | 1 | 0 | 1 | 0 | 204.26 |
| stock | SLB | -5 | -1.45% | -5 | 0 | -5 | 0 | 58.13 |
| stock | TECK | 3 | 1.01% | 3 | 0 | 3 | 0 | 67.07 |
| stock | VALE | 16 | 1.26% | 17 | -1 | 16 | 0 | 15.73 |
| stock | WLK | -10 | -3.81% | -10 | 0 | -10 | 0 | 76.27 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DINO | SELL | -1.0 | 1.0 | 0.0 | 106.33 | 105.79 | 1 |
| DK | SELL | -2.0 | 2.0 | 0.0 | 71.63 | 71.27 | 1 |
| ERO | BUY | 1.0 | 18.0 | 19.0 | 34.67 | 34.85 | 1 |
| FSUGY | SELL | -3.0 | 13.0 | 10.0 | 24.17 | 24.05 | 1 |
| LYB | BUY | 1.0 | -12.0 | -11.0 | 66.4 | 66.74 | 1 |
| PBF | SELL | -1.0 | 1.0 | 0.0 | 75.67 | 75.29 | 1 |
| VALE | SELL | -1.0 | 17.0 | 16.0 | 15.77 | 15.69 | 1 |
| XLE | BUY | 12.0 | 49.0 | 61.0 | 64.94 | 65.26 | 2 |
