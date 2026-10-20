# Combined CL v4.3 + Metals + Agriculture targets: 2026-10-06

策略变更和当前信号状态见 [strategy_notes.md](strategy_notes.md)。

- Combined AUM: $22,000.00
- Total child turnover: 4.16% ($915.88)
- Stock child turnover (40% cap applies): 0.06%
- Hedge child turnover (uncapped): 4.10%
- Orders: 3
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | SPY | 4 | 14.09% | 5 | -1 | 4 | 0 | 774.83 |
| hedge | XLE | 32 | 9.23% | 30 | 2 | 32 | 0 | 63.45 |
| hedge | XME | 3 | 1.47% | 3 | 0 | 3 | 0 | 107.76 |
| stock | AVNT | -5 | -0.95% | -5 | 0 | -5 | 0 | 41.60 |
| stock | BHP | -7 | -2.76% | -7 | 0 | -7 | 0 | 86.83 |
| stock | CE | -9 | -1.86% | -9 | 0 | -9 | 0 | 45.53 |
| stock | DINO | 3 | 1.57% | 3 | 0 | 3 | 0 | 115.22 |
| stock | DK | 10 | 3.43% | 10 | 0 | 10 | 0 | 75.40 |
| stock | DOW | -26 | -3.37% | -27 | 0 | -27 | 1 | 28.51 |
| stock | EMN | -6 | -1.77% | -6 | 0 | -6 | 0 | 64.94 |
| stock | ERO | 18 | 3.15% | 18 | 0 | 18 | 0 | 38.44 |
| stock | FSUGY | -15 | -1.54% | -15 | 0 | -15 | 0 | 22.64 |
| stock | FTI | -4 | -1.28% | -4 | 0 | -4 | 0 | 70.25 |
| stock | HAL | -5 | -0.74% | -4 | 0 | -4 | -1 | 32.78 |
| stock | HUN | -48 | -1.93% | -47 | 0 | -47 | -1 | 8.84 |
| stock | LYB | -13 | -3.50% | -13 | 0 | -13 | 0 | 59.22 |
| stock | PBF | 5 | 1.91% | 5 | 0 | 5 | 0 | 84.16 |
| stock | PSX | -1 | -1.23% | -1 | 0 | -1 | 0 | 269.72 |
| stock | RIO | -6 | -2.61% | -6 | 0 | -6 | 0 | 95.65 |
| stock | SCCO | -2 | -1.87% | -2 | 0 | -2 | 0 | 205.29 |
| stock | SLB | -6 | -1.37% | -6 | 0 | -6 | 0 | 50.28 |
| stock | TECK | 3 | 0.93% | 3 | 0 | 3 | 0 | 67.87 |
| stock | VALE | -23 | -1.48% | -24 | 1 | -23 | 0 | 14.15 |
| stock | WLK | -12 | -3.52% | -12 | 0 | -12 | 0 | 64.61 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| VALE | BUY | 1.0 | -24.0 | -23.0 | 14.11 | 14.19 | 1 |
| SPY | SELL | -1.0 | 5.0 | 4.0 | 776.77 | 772.89 | 2 |
| XLE | BUY | 2.0 | 30.0 | 32.0 | 63.29 | 63.61 | 2 |
