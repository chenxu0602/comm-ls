# Combined CL v4.3 + Metals targets: 2026-08-31

- Combined AUM: $20,000.00
- Total child turnover: 8.18% ($1,635.38)
- Stock child turnover (40% cap applies): 3.10%
- Hedge child turnover (uncapped): 5.08%
- Orders: 6
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | SPY | 1 | 3.86% | 0 | 1 | 1 | 0 | 771.79 |
| hedge | XLE | 19 | 5.93% | 19 | 0 | 19 | 0 | 62.40 |
| hedge | XME | -20 | -12.18% | -22 | 2 | -20 | 0 | 121.82 |
| stock | ATI | 2 | 2.13% | 2 | 0 | 2 | 0 | 213.06 |
| stock | AVNT | -5 | -1.12% | -5 | 0 | -5 | 0 | 44.68 |
| stock | BHP | 6 | 2.89% | 6 | 0 | 6 | 0 | 96.35 |
| stock | CE | -9 | -2.03% | -9 | 0 | -9 | 0 | 45.09 |
| stock | DINO | 3 | 1.47% | 3 | 0 | 3 | 0 | 98.13 |
| stock | DK | 10 | 3.58% | 11 | 0 | 11 | -1 | 71.54 |
| stock | DOW | -25 | -3.82% | -25 | 0 | -25 | 0 | 30.52 |
| stock | EMN | -6 | -2.20% | -6 | 0 | -6 | 0 | 73.27 |
| stock | ERO | 17 | 3.37% | 17 | 0 | 17 | 0 | 39.66 |
| stock | FSUGY | 10 | 1.29% | 13 | -3 | 10 | 0 | 25.79 |
| stock | FTI | -4 | -1.52% | -4 | 0 | -4 | 0 | 76.07 |
| stock | HAL | -4 | -0.72% | -4 | 0 | -4 | 0 | 35.78 |
| stock | HUN | -43 | -2.09% | -43 | 0 | -43 | 0 | 9.72 |
| stock | HWM | 1 | 1.33% | 1 | 0 | 1 | 0 | 265.80 |
| stock | LYB | -12 | -3.82% | -12 | 0 | -12 | 0 | 63.62 |
| stock | MUSA | 1 | 2.53% | 1 | 0 | 1 | 0 | 505.06 |
| stock | PBF | 6 | 2.10% | 7 | -1 | 6 | 0 | 69.98 |
| stock | PSX | 2 | 2.42% | 2 | 0 | 2 | 0 | 241.92 |
| stock | RIO | 6 | 3.13% | 6 | 0 | 6 | 0 | 104.42 |
| stock | SCCO | 2 | 2.15% | 3 | -1 | 2 | 0 | 214.88 |
| stock | SLB | -5 | -1.39% | -6 | 0 | -6 | 1 | 55.63 |
| stock | TECK | 3 | 1.06% | 3 | 0 | 3 | 0 | 70.77 |
| stock | VALE | 16 | 1.21% | 33 | -17 | 16 | 0 | 15.16 |
| stock | WLK | -10 | -3.74% | -10 | 0 | -10 | 0 | 74.88 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FSUGY | SELL | -3.0 | 13.0 | 10.0 | 25.85 | 25.73 | 1 |
| PBF | SELL | -1.0 | 7.0 | 6.0 | 70.16 | 69.81 | 1 |
| SCCO | SELL | -1.0 | 3.0 | 2.0 | 215.41 | 214.34 | 1 |
| VALE | SELL | -17.0 | 33.0 | 16.0 | 15.2 | 15.12 | 1 |
| SPY | BUY | 1.0 | 0.0 | 1.0 | 769.86 | 773.72 | 2 |
| XME | BUY | 2.0 | -22.0 | -20.0 | 121.51 | 122.12 | 2 |
