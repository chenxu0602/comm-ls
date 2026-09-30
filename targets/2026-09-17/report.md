# Combined CL v4.3 + Metals targets: 2026-09-17

- Combined AUM: $20,000.00
- Total child turnover: 18.20% ($3,640.30)
- Stock child turnover (40% cap applies): 12.67%
- Hedge child turnover (uncapped): 5.53%
- Orders: 11
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Combined account targets

`remaining_to_target = target_shares - post_trade_shares`; non-zero stock values are deferred by strategy-level rounding or the stock-only daily turnover limit.

| instrument_type | instrument | target_shares | target_weight_pct | current_shares | tonight_trade_shares | post_trade_shares | remaining_to_target | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | SPY | 2 | 7.54% | 2 | 0 | 2 | 0 | 754.05 |
| hedge | XLE | 104 | 33.30% | 106 | -2 | 104 | 0 | 64.03 |
| hedge | XME | -10 | -5.44% | -19 | 9 | -10 | 0 | 108.77 |
| stock | ATI | 1 | 0.95% | 2 | -1 | 1 | 0 | 189.65 |
| stock | AVNT | -5 | -1.02% | -5 | 0 | -5 | 0 | 40.93 |
| stock | BHP | 7 | 2.94% | 7 | 0 | 7 | 0 | 84.14 |
| stock | CASY | 0 | 0.00% | 1 | -1 | 0 | 0 | 589.00 |
| stock | CE | -9 | -2.11% | -9 | 0 | -9 | 0 | 46.87 |
| stock | CRS | 0 | 0.00% | 1 | -1 | 0 | 0 | 411.80 |
| stock | DINO | -3 | -1.71% | -3 | 0 | -3 | 0 | 113.97 |
| stock | DK | -9 | -3.56% | -10 | 1 | -9 | 0 | 79.16 |
| stock | DOW | -25 | -3.76% | -25 | 0 | -25 | 0 | 30.08 |
| stock | EMN | -6 | -1.95% | -6 | 0 | -6 | 0 | 65.07 |
| stock | ERO | 0 | 0.00% | 21 | -21 | 0 | 0 | 32.28 |
| stock | FSUGY | 11 | 1.27% | 11 | 0 | 11 | 0 | 23.16 |
| stock | FTI | -4 | -1.46% | -4 | 0 | -4 | 0 | 72.78 |
| stock | HAL | -4 | -0.69% | -4 | 0 | -4 | 0 | 34.51 |
| stock | HUN | -46 | -2.11% | -43 | 0 | -43 | -3 | 9.19 |
| stock | HWM | 0 | 0.00% | 1 | -1 | 0 | 0 | 227.73 |
| stock | LYB | -12 | -3.89% | -12 | 0 | -12 | 0 | 64.90 |
| stock | PBF | -6 | -2.28% | -6 | 0 | -6 | 0 | 75.93 |
| stock | PSX | -3 | -3.97% | -3 | 0 | -3 | 0 | 264.63 |
| stock | RIO | 6 | 2.87% | 6 | 0 | 6 | 0 | 95.79 |
| stock | SCCO | 1 | 0.95% | 1 | 0 | 1 | 0 | 189.88 |
| stock | SLB | -6 | -1.57% | -5 | -1 | -6 | 0 | 52.30 |
| stock | TECK | 0 | 0.00% | 3 | -3 | 0 | 0 | 64.25 |
| stock | VALE | 18 | 1.27% | 26 | -8 | 18 | 0 | 14.13 |
| stock | WLK | -11 | -3.89% | -11 | 0 | -11 | 0 | 70.66 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ATI | SELL | -1.0 | 2.0 | 1.0 | 190.12 | 189.18 | 1 |
| CASY | SELL | -1.0 | 1.0 | 0.0 | 590.47 | 587.53 | 1 |
| CRS | SELL | -1.0 | 1.0 | 0.0 | 412.83 | 410.77 | 1 |
| DK | BUY | 1.0 | -10.0 | -9.0 | 78.96 | 79.36 | 1 |
| ERO | SELL | -21.0 | 21.0 | 0.0 | 32.36 | 32.2 | 1 |
| HWM | SELL | -1.0 | 1.0 | 0.0 | 228.3 | 227.16 | 1 |
| SLB | SELL | -1.0 | -5.0 | -6.0 | 52.43 | 52.17 | 1 |
| TECK | SELL | -3.0 | 3.0 | 0.0 | 64.41 | 64.09 | 1 |
| VALE | SELL | -8.0 | 26.0 | 18.0 | 14.17 | 14.09 | 1 |
| XLE | SELL | -2.0 | 106.0 | 104.0 | 64.19 | 63.87 | 2 |
| XME | BUY | 9.0 | -19.0 | -10.0 | 108.5 | 109.04 | 2 |
