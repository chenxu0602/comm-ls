# Combined CL v4.3 + Metals + Agriculture targets: 2026-10-02

- Combined AUM: $22,000.00
- Total child turnover: 10.70% ($2,354.71)
- Stock child turnover (40% cap applies): 5.14%
- Hedge child turnover (uncapped): 5.56%
- Orders: 10
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | SPY | 5 | 17.36% | 4 | 1 | 5 | 0 | 763.99 |
| hedge | XLE | 30 | 8.55% | 34 | -4 | 30 | 0 | 62.70 |
| hedge | XME | 3 | 1.42% | 1 | 2 | 3 | 0 | 104.29 |
| stock | AVNT | -5 | -0.92% | -5 | 0 | -5 | 0 | 40.54 |
| stock | BHP | -7 | -2.69% | -6 | -1 | -7 | 0 | 84.65 |
| stock | CE | -10 | -2.01% | -9 | 0 | -9 | -1 | 44.20 |
| stock | DINO | 3 | 1.54% | 3 | 0 | 3 | 0 | 112.70 |
| stock | DK | 10 | 3.38% | 11 | -1 | 10 | 0 | 74.34 |
| stock | DOW | -27 | -3.39% | -27 | 0 | -27 | 0 | 27.59 |
| stock | EMN | -7 | -2.04% | -6 | 0 | -6 | -1 | 64.05 |
| stock | ERO | 19 | 3.09% | 18 | 0 | 18 | 1 | 35.75 |
| stock | FSUGY | -15 | -1.54% | -15 | 0 | -15 | 0 | 22.59 |
| stock | FTI | -4 | -1.25% | -4 | 0 | -4 | 0 | 68.85 |
| stock | HAL | -5 | -0.72% | -4 | 0 | -4 | -1 | 31.88 |
| stock | HUN | -48 | -1.89% | -47 | 0 | -47 | -1 | 8.67 |
| stock | LYB | -13 | -3.41% | -13 | 0 | -13 | 0 | 57.78 |
| stock | PBF | 5 | 1.87% | 6 | -1 | 5 | 0 | 82.34 |
| stock | PSX | -1 | -1.20% | -2 | 1 | -1 | 0 | 264.23 |
| stock | RIO | -6 | -2.53% | -3 | -3 | -6 | 0 | 92.87 |
| stock | SCCO | -3 | -2.72% | -2 | -1 | -3 | 0 | 199.22 |
| stock | SLB | -6 | -1.33% | -6 | 0 | -6 | 0 | 48.66 |
| stock | TECK | 3 | 0.89% | 3 | 0 | 3 | 0 | 65.22 |
| stock | VALE | -24 | -1.47% | -13 | -11 | -24 | 0 | 13.45 |
| stock | WLK | -12 | -3.41% | -12 | 0 | -12 | 0 | 62.47 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BHP | SELL | -1.0 | -6.0 | -7.0 | 84.86 | 84.44 | 1 |
| DK | SELL | -1.0 | 11.0 | 10.0 | 74.53 | 74.15 | 1 |
| PBF | SELL | -1.0 | 6.0 | 5.0 | 82.55 | 82.13 | 1 |
| PSX | BUY | 1.0 | -2.0 | -1.0 | 263.57 | 264.89 | 1 |
| RIO | SELL | -3.0 | -3.0 | -6.0 | 93.1 | 92.64 | 1 |
| SCCO | SELL | -1.0 | -2.0 | -3.0 | 199.72 | 198.72 | 1 |
| VALE | SELL | -11.0 | -13.0 | -24.0 | 13.48 | 13.42 | 1 |
| SPY | BUY | 1.0 | 4.0 | 5.0 | 762.08 | 765.9 | 2 |
| XLE | SELL | -4.0 | 34.0 | 30.0 | 62.86 | 62.54 | 2 |
| XME | BUY | 2.0 | 1.0 | 3.0 | 104.03 | 104.55 | 2 |
