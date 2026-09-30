# Combined CL v4.3 + Metals targets: 2026-09-15

- Combined AUM: $20,000.00
- Total child turnover: 6.13% ($1,226.55)
- Stock child turnover (40% cap applies): 1.13%
- Hedge child turnover (uncapped): 5.00%
- Orders: 6
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | SPY | 2 | 7.61% | 1 | 1 | 2 | 0 | 760.88 |
| hedge | XLE | 106 | 34.20% | 104 | 2 | 106 | 0 | 64.53 |
| hedge | XME | -21 | -11.57% | -20 | -1 | -21 | 0 | 110.17 |
| stock | ATI | 2 | 1.88% | 3 | -1 | 2 | 0 | 188.15 |
| stock | AVNT | -5 | -1.03% | -5 | 0 | -5 | 0 | 41.16 |
| stock | BHP | 7 | 2.97% | 7 | 0 | 7 | 0 | 84.74 |
| stock | CASY | 1 | 3.11% | 1 | 0 | 1 | 0 | 621.61 |
| stock | CE | -9 | -2.02% | -9 | 0 | -9 | 0 | 44.78 |
| stock | CRS | 1 | 2.10% | 1 | 0 | 1 | 0 | 420.38 |
| stock | DINO | -3 | -1.60% | -3 | 0 | -3 | 0 | 106.91 |
| stock | DK | -10 | -3.72% | -10 | 0 | -10 | 0 | 74.47 |
| stock | DOW | -26 | -3.76% | -25 | 0 | -25 | -1 | 28.90 |
| stock | EMN | -6 | -2.01% | -6 | 0 | -6 | 0 | 67.00 |
| stock | ERO | 20 | 3.37% | 19 | 0 | 19 | 1 | 33.68 |
| stock | FSUGY | 11 | 1.30% | 10 | 1 | 11 | 0 | 23.68 |
| stock | FTI | -4 | -1.46% | -4 | 0 | -4 | 0 | 72.87 |
| stock | HAL | -4 | -0.70% | -4 | 0 | -4 | 0 | 35.01 |
| stock | HUN | -45 | -2.09% | -43 | 0 | -43 | -2 | 9.30 |
| stock | HWM | 1 | 1.14% | 1 | 0 | 1 | 0 | 227.13 |
| stock | LYB | -12 | -3.77% | -12 | 0 | -12 | 0 | 62.75 |
| stock | PBF | -6 | -2.11% | -6 | 0 | -6 | 0 | 70.40 |
| stock | PSX | -3 | -3.86% | -3 | 0 | -3 | 0 | 257.06 |
| stock | RIO | 6 | 2.93% | 6 | 0 | 6 | 0 | 97.64 |
| stock | SCCO | 2 | 1.88% | 2 | 0 | 2 | 0 | 188.35 |
| stock | SLB | -6 | -1.60% | -5 | 0 | -5 | -1 | 53.32 |
| stock | TECK | 3 | 0.99% | 3 | 0 | 3 | 0 | 66.25 |
| stock | VALE | 27 | 1.97% | 26 | 1 | 27 | 0 | 14.61 |
| stock | WLK | -11 | -3.79% | -11 | 0 | -11 | 0 | 68.96 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ATI | SELL | -1.0 | 3.0 | 2.0 | 188.62 | 187.68 | 1 |
| FSUGY | BUY | 1.0 | 10.0 | 11.0 | 23.62 | 23.74 | 1 |
| VALE | BUY | 1.0 | 26.0 | 27.0 | 14.57 | 14.65 | 1 |
| SPY | BUY | 1.0 | 1.0 | 2.0 | 758.98 | 762.78 | 2 |
| XLE | BUY | 2.0 | 104.0 | 106.0 | 64.37 | 64.69 | 2 |
| XME | SELL | -1.0 | -20.0 | -21.0 | 110.45 | 109.89 | 2 |
