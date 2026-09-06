# Combined CL v4.3 + Metals targets: 2026-09-08

- Combined AUM: $20,000.00
- Total child turnover: 11.64% ($2,328.57)
- Stock child turnover (40% cap applies): 5.92%
- Hedge child turnover (uncapped): 5.72%
- Orders: 9
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | SPY | 1 | 3.85% | 1 | 0 | 1 | 0 | 770.19 |
| hedge | XLE | 91 | 29.15% | 75 | 16 | 91 | 0 | 64.06 |
| hedge | XME | -19 | -11.27% | -18 | -1 | -19 | 0 | 118.62 |
| stock | ATI | 1 | 1.05% | 1 | 0 | 1 | 0 | 210.65 |
| stock | AVNT | -5 | -1.08% | -5 | 0 | -5 | 0 | 43.40 |
| stock | BHP | 7 | 3.16% | 6 | 1 | 7 | 0 | 90.42 |
| stock | CE | -9 | -2.01% | -9 | 0 | -9 | 0 | 44.67 |
| stock | DINO | -3 | -1.58% | -2 | -1 | -3 | 0 | 105.41 |
| stock | DK | -10 | -3.59% | -6 | -4 | -10 | 0 | 71.86 |
| stock | DOW | -25 | -3.68% | -25 | 0 | -25 | 0 | 29.44 |
| stock | EMN | -6 | -2.14% | -6 | 0 | -6 | 0 | 71.19 |
| stock | ERO | 19 | 3.32% | 19 | 0 | 19 | 0 | 34.90 |
| stock | FSUGY | 14 | 1.74% | 10 | 4 | 14 | 0 | 24.86 |
| stock | FTI | -4 | -1.60% | -4 | 0 | -4 | 0 | 79.84 |
| stock | HAL | -4 | -0.74% | -4 | 0 | -4 | 0 | 37.07 |
| stock | HUN | -44 | -2.12% | -43 | 0 | -43 | -1 | 9.62 |
| stock | HWM | 1 | 1.30% | 1 | 0 | 1 | 0 | 259.27 |
| stock | LYB | -12 | -3.81% | -12 | 0 | -12 | 0 | 63.52 |
| stock | MUSA | 1 | 2.56% | 1 | 0 | 1 | 0 | 511.33 |
| stock | PBF | -6 | -2.23% | -4 | -2 | -6 | 0 | 74.34 |
| stock | PSX | 0 | 0.00% | 1 | -1 | 0 | 0 | 255.09 |
| stock | RIO | 6 | 3.10% | 6 | 0 | 6 | 0 | 103.27 |
| stock | SCCO | 1 | 0.99% | 1 | 0 | 1 | 0 | 198.76 |
| stock | SLB | -5 | -1.44% | -5 | 0 | -5 | 0 | 57.51 |
| stock | TECK | 3 | 1.04% | 3 | 0 | 3 | 0 | 69.10 |
| stock | VALE | 29 | 2.21% | 16 | 13 | 29 | 0 | 15.27 |
| stock | WLK | -10 | -3.74% | -10 | 0 | -10 | 0 | 74.79 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BHP | BUY | 1.0 | 6.0 | 7.0 | 90.19 | 90.65 | 1 |
| DINO | SELL | -1.0 | -2.0 | -3.0 | 105.67 | 105.15 | 1 |
| DK | SELL | -4.0 | -6.0 | -10.0 | 72.04 | 71.68 | 1 |
| FSUGY | BUY | 4.0 | 10.0 | 14.0 | 24.8 | 24.92 | 1 |
| PBF | SELL | -2.0 | -4.0 | -6.0 | 74.53 | 74.15 | 1 |
| PSX | SELL | -1.0 | 1.0 | 0.0 | 255.73 | 254.45 | 1 |
| VALE | BUY | 13.0 | 16.0 | 29.0 | 15.23 | 15.31 | 1 |
| XLE | BUY | 16.0 | 75.0 | 91.0 | 63.9 | 64.22 | 2 |
| XME | SELL | -1.0 | -18.0 | -19.0 | 118.92 | 118.32 | 2 |
