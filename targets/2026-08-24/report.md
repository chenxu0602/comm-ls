# Combined CL v4.2 + Metals targets: 2026-08-24

- Combined AUM: $20,000.00
- Total child turnover: 41.84% ($8,367.58)
- Stock child turnover (40% cap applies): 18.79%
- Hedge child turnover (uncapped): 23.05%
- Orders: 14
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | SPY | 0 | 0.00% | 2 | -2 | 0 | 0 | 765.72 |
| hedge | XLE | 89 | 28.32% | 65 | 24 | 89 | 0 | 63.64 |
| hedge | XME | -22 | -13.13% | -9 | -13 | -22 | 0 | 119.34 |
| stock | ATI | 2 | 2.07% | 1 | 1 | 2 | 0 | 207.01 |
| stock | AVNT | -5 | -1.12% | -5 | 0 | -5 | 0 | 44.66 |
| stock | BHP | 6 | 2.91% | 0 | 5 | 5 | 1 | 97.03 |
| stock | CE | -9 | -2.11% | -9 | 0 | -9 | 0 | 46.80 |
| stock | DINO | -3 | -1.46% | 0 | -3 | -3 | 0 | 97.32 |
| stock | DK | -10 | -3.57% | 0 | -10 | -10 | 0 | 71.47 |
| stock | DOW | -23 | -3.72% | -23 | 0 | -23 | 0 | 32.35 |
| stock | EMN | -6 | -2.22% | -6 | 0 | -6 | 0 | 74.09 |
| stock | ERO | 17 | 3.35% | 19 | -2 | 17 | 0 | 39.42 |
| stock | FSUGY | 10 | 1.28% | 0 | 7 | 7 | 3 | 25.69 |
| stock | HUN | -42 | -2.09% | -43 | 0 | -43 | 1 | 9.97 |
| stock | HWM | 1 | 1.36% | 1 | 0 | 1 | 0 | 271.68 |
| stock | LYB | -11 | -3.71% | -11 | 0 | -11 | 0 | 67.53 |
| stock | MUSA | 1 | 2.85% | 1 | 0 | 1 | 0 | 569.72 |
| stock | PBF | -6 | -2.21% | 0 | -6 | -6 | 0 | 73.53 |
| stock | PSX | -2 | -2.43% | -3 | 1 | -2 | 0 | 242.87 |
| stock | RIO | 6 | 3.16% | 0 | 4 | 4 | 2 | 105.30 |
| stock | SCCO | 3 | 3.24% | 0 | 2 | 2 | 1 | 216.00 |
| stock | TECK | 3 | 1.04% | 3 | 0 | 3 | 0 | 69.20 |
| stock | VALE | 24 | 1.75% | 0 | 18 | 18 | 6 | 14.59 |
| stock | WLK | -10 | -3.95% | -10 | 0 | -10 | 0 | 78.93 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ATI | BUY | 1.0 | 1.0 | 2.0 | 206.49 | 207.53 | 1 |
| BHP | BUY | 5.0 | 0.0 | 5.0 | 96.79 | 97.27 | 1 |
| DINO | SELL | -3.0 | 0.0 | -3.0 | 97.56 | 97.08 | 1 |
| DK | SELL | -10.0 | 0.0 | -10.0 | 71.65 | 71.29 | 1 |
| ERO | SELL | -2.0 | 19.0 | 17.0 | 39.52 | 39.32 | 1 |
| FSUGY | BUY | 7.0 | 0.0 | 7.0 | 25.63 | 25.75 | 1 |
| PBF | SELL | -6.0 | 0.0 | -6.0 | 73.71 | 73.35 | 1 |
| PSX | BUY | 1.0 | -3.0 | -2.0 | 242.26 | 243.48 | 1 |
| RIO | BUY | 4.0 | 0.0 | 4.0 | 105.04 | 105.56 | 1 |
| SCCO | BUY | 2.0 | 0.0 | 2.0 | 215.46 | 216.54 | 1 |
| VALE | BUY | 18.0 | 0.0 | 18.0 | 14.55 | 14.63 | 1 |
| SPY | SELL | -2.0 | 2.0 | 0.0 | 767.63 | 763.81 | 2 |
| XLE | BUY | 24.0 | 65.0 | 89.0 | 63.48 | 63.8 | 2 |
| XME | SELL | -13.0 | -9.0 | -22.0 | 119.64 | 119.04 | 2 |
