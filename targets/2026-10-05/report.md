# Combined CL v4.3 + Metals + Agriculture targets: 2026-10-05

- Combined AUM: $22,000.00
- Total child turnover: 1.78% ($392.06)
- Stock child turnover (40% cap applies): 1.30%
- Hedge child turnover (uncapped): 0.48%
- Orders: 3
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | SPY | 5 | 17.49% | 5 | 0 | 5 | 0 | 769.64 |
| hedge | XLE | 30 | 8.57% | 30 | 0 | 30 | 0 | 62.82 |
| hedge | XME | 4 | 1.92% | 3 | 1 | 4 | 0 | 105.74 |
| stock | AVNT | -5 | -0.94% | -5 | 0 | -5 | 0 | 41.17 |
| stock | BHP | -7 | -2.74% | -7 | 0 | -7 | 0 | 86.07 |
| stock | CE | -10 | -2.01% | -9 | 0 | -9 | -1 | 44.19 |
| stock | DINO | 3 | 1.55% | 3 | 0 | 3 | 0 | 113.36 |
| stock | DK | 10 | 3.37% | 10 | 0 | 10 | 0 | 74.19 |
| stock | DOW | -27 | -3.43% | -27 | 0 | -27 | 0 | 27.97 |
| stock | EMN | -6 | -1.77% | -6 | 0 | -6 | 0 | 64.87 |
| stock | ERO | 18 | 3.10% | 18 | 0 | 18 | 0 | 37.91 |
| stock | FSUGY | -15 | -1.54% | -15 | 0 | -15 | 0 | 22.61 |
| stock | FTI | -4 | -1.25% | -4 | 0 | -4 | 0 | 68.82 |
| stock | HAL | -5 | -0.72% | -4 | 0 | -4 | -1 | 31.85 |
| stock | HUN | -49 | -1.90% | -47 | 0 | -47 | -2 | 8.53 |
| stock | LYB | -13 | -3.46% | -13 | 0 | -13 | 0 | 58.58 |
| stock | PBF | 6 | 2.20% | 5 | 1 | 6 | 0 | 80.78 |
| stock | PSX | -1 | -1.20% | -1 | 0 | -1 | 0 | 264.58 |
| stock | RIO | -6 | -2.57% | -6 | 0 | -6 | 0 | 94.21 |
| stock | SCCO | -2 | -1.87% | -3 | 1 | -2 | 0 | 205.54 |
| stock | SLB | -6 | -1.33% | -6 | 0 | -6 | 0 | 48.74 |
| stock | TECK | 3 | 0.93% | 3 | 0 | 3 | 0 | 68.56 |
| stock | VALE | -24 | -1.50% | -24 | 0 | -24 | 0 | 13.76 |
| stock | WLK | -12 | -3.46% | -12 | 0 | -12 | 0 | 63.50 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| PBF | BUY | 1.0 | 5.0 | 6.0 | 80.58 | 80.98 | 1 |
| SCCO | BUY | 1.0 | -3.0 | -2.0 | 205.03 | 206.05 | 1 |
| XME | BUY | 1.0 | 3.0 | 4.0 | 105.48 | 106.0 | 2 |
