# Combined CL v4.3 + Metals targets: 2026-09-16

- Combined AUM: $20,000.00
- Total child turnover: 3.68% ($735.42)
- Stock child turnover (40% cap applies): 1.92%
- Hedge child turnover (uncapped): 1.75%
- Orders: 5
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | SPY | 2 | 7.57% | 2 | 0 | 2 | 0 | 757.39 |
| hedge | XLE | 104 | 34.28% | 106 | -2 | 104 | 0 | 65.93 |
| hedge | XME | -19 | -10.40% | -21 | 2 | -19 | 0 | 109.44 |
| stock | ATI | 2 | 1.87% | 2 | 0 | 2 | 0 | 186.69 |
| stock | AVNT | -5 | -1.02% | -5 | 0 | -5 | 0 | 40.97 |
| stock | BHP | 7 | 2.97% | 7 | 0 | 7 | 0 | 84.77 |
| stock | CASY | 1 | 2.94% | 1 | 0 | 1 | 0 | 587.14 |
| stock | CE | -9 | -2.12% | -9 | 0 | -9 | 0 | 47.22 |
| stock | CRS | 1 | 2.08% | 1 | 0 | 1 | 0 | 415.32 |
| stock | DINO | -3 | -1.68% | -3 | 0 | -3 | 0 | 112.25 |
| stock | DK | -10 | -3.91% | -10 | 0 | -10 | 0 | 78.14 |
| stock | DOW | -25 | -3.73% | -25 | 0 | -25 | 0 | 29.85 |
| stock | EMN | -6 | -1.98% | -6 | 0 | -6 | 0 | 65.88 |
| stock | ERO | 21 | 3.42% | 19 | 2 | 21 | 0 | 32.53 |
| stock | FSUGY | 11 | 1.28% | 11 | 0 | 11 | 0 | 23.22 |
| stock | FTI | -4 | -1.50% | -4 | 0 | -4 | 0 | 74.97 |
| stock | HAL | -4 | -0.71% | -4 | 0 | -4 | 0 | 35.67 |
| stock | HUN | -46 | -2.12% | -43 | 0 | -43 | -3 | 9.22 |
| stock | HWM | 1 | 1.12% | 1 | 0 | 1 | 0 | 224.67 |
| stock | LYB | -11 | -3.60% | -12 | 0 | -12 | 1 | 65.43 |
| stock | PBF | -6 | -2.24% | -6 | 0 | -6 | 0 | 74.72 |
| stock | PSX | -3 | -3.97% | -3 | 0 | -3 | 0 | 264.93 |
| stock | RIO | 6 | 2.92% | 6 | 0 | 6 | 0 | 97.26 |
| stock | SCCO | 1 | 0.95% | 2 | -1 | 1 | 0 | 189.39 |
| stock | SLB | -6 | -1.63% | -5 | 0 | -5 | -1 | 54.20 |
| stock | TECK | 3 | 0.97% | 3 | 0 | 3 | 0 | 64.65 |
| stock | VALE | 17 | 1.23% | 26 | -9 | 17 | 0 | 14.47 |
| stock | WLK | -11 | -3.85% | -11 | 0 | -11 | 0 | 70.02 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ERO | BUY | 2.0 | 19.0 | 21.0 | 32.45 | 32.61 | 1 |
| SCCO | SELL | -1.0 | 2.0 | 1.0 | 189.86 | 188.92 | 1 |
| VALE | SELL | -9.0 | 26.0 | 17.0 | 14.51 | 14.43 | 1 |
| XLE | SELL | -2.0 | 106.0 | 104.0 | 66.09 | 65.77 | 2 |
| XME | BUY | 2.0 | -21.0 | -19.0 | 109.17 | 109.71 | 2 |
