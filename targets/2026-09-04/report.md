# Combined CL v4.3 + Metals targets: 2026-09-04

- Combined AUM: $20,000.00
- Total child turnover: 9.59% ($1,917.46)
- Stock child turnover (40% cap applies): 5.06%
- Hedge child turnover (uncapped): 4.52%
- Orders: 5
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | SPY | 1 | 3.87% | 1 | 0 | 1 | 0 | 773.17 |
| hedge | XLE | 75 | 24.23% | 61 | 14 | 75 | 0 | 64.62 |
| hedge | XME | -18 | -10.65% | -18 | 0 | -18 | 0 | 118.38 |
| stock | ATI | 1 | 1.02% | 1 | 0 | 1 | 0 | 204.54 |
| stock | AVNT | -5 | -1.07% | -5 | 0 | -5 | 0 | 42.91 |
| stock | BHP | 6 | 2.78% | 6 | 0 | 6 | 0 | 92.71 |
| stock | CE | -9 | -2.03% | -9 | 0 | -9 | 0 | 45.20 |
| stock | DINO | -2 | -1.06% | 0 | -2 | -2 | 0 | 106.15 |
| stock | DK | -6 | -2.17% | 0 | -6 | -6 | 0 | 72.40 |
| stock | DOW | -25 | -3.79% | -25 | 0 | -25 | 0 | 30.36 |
| stock | EMN | -6 | -2.12% | -6 | 0 | -6 | 0 | 70.77 |
| stock | ERO | 19 | 3.36% | 19 | 0 | 19 | 0 | 35.32 |
| stock | FSUGY | 10 | 1.23% | 10 | 0 | 10 | 0 | 24.54 |
| stock | FTI | -4 | -1.60% | -4 | 0 | -4 | 0 | 80.08 |
| stock | HAL | -4 | -0.75% | -4 | 0 | -4 | 0 | 37.29 |
| stock | HUN | -45 | -2.11% | -43 | 0 | -43 | -2 | 9.40 |
| stock | HWM | 1 | 1.30% | 1 | 0 | 1 | 0 | 260.49 |
| stock | LYB | -12 | -3.89% | -11 | -1 | -12 | 0 | 64.76 |
| stock | MUSA | 1 | 2.61% | 1 | 0 | 1 | 0 | 522.30 |
| stock | PBF | -4 | -1.51% | 0 | -4 | -4 | 0 | 75.33 |
| stock | PSX | 1 | 1.27% | 1 | 0 | 1 | 0 | 254.66 |
| stock | RIO | 6 | 3.09% | 6 | 0 | 6 | 0 | 102.84 |
| stock | SCCO | 1 | 1.00% | 1 | 0 | 1 | 0 | 199.53 |
| stock | SLB | -5 | -1.44% | -5 | 0 | -5 | 0 | 57.41 |
| stock | TECK | 3 | 1.03% | 3 | 0 | 3 | 0 | 68.82 |
| stock | VALE | 16 | 1.22% | 16 | 0 | 16 | 0 | 15.31 |
| stock | WLK | -10 | -3.73% | -10 | 0 | -10 | 0 | 74.60 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DINO | SELL | -2.0 | 0.0 | -2.0 | 106.42 | 105.88 | 1 |
| DK | SELL | -6.0 | 0.0 | -6.0 | 72.58 | 72.22 | 1 |
| LYB | SELL | -1.0 | -11.0 | -12.0 | 64.92 | 64.6 | 1 |
| PBF | SELL | -4.0 | 0.0 | -4.0 | 75.52 | 75.14 | 1 |
| XLE | BUY | 14.0 | 61.0 | 75.0 | 64.46 | 64.78 | 2 |
