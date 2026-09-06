# Combined CL v4.3 + Metals targets: 2026-09-02

- Combined AUM: $20,000.00
- Total child turnover: 12.19% ($2,438.43)
- Stock child turnover (40% cap applies): 6.69%
- Hedge child turnover (uncapped): 5.51%
- Orders: 9
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | SPY | 1 | 3.81% | 1 | 0 | 1 | 0 | 761.78 |
| hedge | XLE | 49 | 15.87% | 32 | 17 | 49 | 0 | 64.77 |
| hedge | XME | -18 | -10.42% | -18 | 0 | -18 | 0 | 115.77 |
| stock | ATI | 1 | 1.00% | 2 | -1 | 1 | 0 | 200.95 |
| stock | AVNT | -5 | -1.07% | -5 | 0 | -5 | 0 | 42.62 |
| stock | BHP | 6 | 2.78% | 6 | 0 | 6 | 0 | 92.82 |
| stock | CE | -10 | -2.21% | -9 | 0 | -9 | -1 | 44.13 |
| stock | DINO | 1 | 0.52% | 2 | -1 | 1 | 0 | 103.97 |
| stock | DK | 2 | 0.73% | 6 | -4 | 2 | 0 | 73.34 |
| stock | DOW | -25 | -3.81% | -25 | 0 | -25 | 0 | 30.46 |
| stock | EMN | -6 | -2.10% | -6 | 0 | -6 | 0 | 70.14 |
| stock | ERO | 19 | 3.31% | 18 | 1 | 19 | 0 | 34.82 |
| stock | FSUGY | 10 | 1.27% | 13 | -3 | 10 | 0 | 25.35 |
| stock | FTI | -4 | -1.57% | -4 | 0 | -4 | 0 | 78.31 |
| stock | HAL | -4 | -0.74% | -4 | 0 | -4 | 0 | 36.80 |
| stock | HUN | -45 | -2.11% | -43 | 0 | -43 | -2 | 9.39 |
| stock | HWM | 1 | 1.27% | 1 | 0 | 1 | 0 | 254.89 |
| stock | LYB | -12 | -3.91% | -12 | 0 | -12 | 0 | 65.17 |
| stock | MUSA | 1 | 2.68% | 1 | 0 | 1 | 0 | 536.45 |
| stock | PBF | 1 | 0.37% | 4 | -3 | 1 | 0 | 74.99 |
| stock | PSX | 1 | 1.26% | 2 | -1 | 1 | 0 | 252.02 |
| stock | RIO | 6 | 3.06% | 6 | 0 | 6 | 0 | 101.86 |
| stock | SCCO | 1 | 1.01% | 1 | 0 | 1 | 0 | 201.61 |
| stock | SLB | -5 | -1.43% | -5 | 0 | -5 | 0 | 57.15 |
| stock | TECK | 3 | 1.00% | 3 | 0 | 3 | 0 | 66.79 |
| stock | VALE | 17 | 1.29% | 27 | -10 | 17 | 0 | 15.12 |
| stock | WLK | -10 | -3.71% | -10 | 0 | -10 | 0 | 74.23 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ATI | SELL | -1.0 | 2.0 | 1.0 | 201.45 | 200.45 | 1 |
| DINO | SELL | -1.0 | 2.0 | 1.0 | 104.23 | 103.71 | 1 |
| DK | SELL | -4.0 | 6.0 | 2.0 | 73.52 | 73.16 | 1 |
| ERO | BUY | 1.0 | 18.0 | 19.0 | 34.73 | 34.91 | 1 |
| FSUGY | SELL | -3.0 | 13.0 | 10.0 | 25.41 | 25.29 | 1 |
| PBF | SELL | -3.0 | 4.0 | 1.0 | 75.18 | 74.8 | 1 |
| PSX | SELL | -1.0 | 2.0 | 1.0 | 252.65 | 251.39 | 1 |
| VALE | SELL | -10.0 | 27.0 | 17.0 | 15.16 | 15.08 | 1 |
| XLE | BUY | 17.0 | 32.0 | 49.0 | 64.61 | 64.93 | 2 |
