# Combined CL v4.2 + Metals targets: 2026-08-24

- Combined AUM: $20,000.00
- Child turnover: 25.79% ($5,157.68)
- Orders: 13
- Source rule: sum strategy-level rounded_trade_shares; never re-round continuous notionals.
- Execute stocks first; review aggregate hedge children after confirmed stock fills.

## Combined account targets

| instrument_type | component | instrument | cl_target_shares | metals_target_shares | rounded_target_shares | target_weight | current_shares | post_child_shares | remaining_target_shares | previous_close |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| hedge | cl_v42:hedge|metals:hedge | SPY | 2.0 | -2.0 | 0.0 | 0.0 | 2.0 | 2.0 | -2.0 | 765.72 |
| hedge | cl_v42:hedge | XLE | 89.0 | 0.0 | 89.0 | 0.283198 | 65.0 | 89.0 | 0.0 | 63.64 |
| hedge | cl_v42:hedge|metals:hedge | XME | -9.0 | -13.0 | -22.0 | -0.131274 | -9.0 | -14.0 | -8.0 | 119.34 |
| stock | cl_v42:metals|metals:sco_specialty_alloys | ATI | 1.0 | 1.0 | 2.0 | 0.020701 | 1.0 | 2.0 | 0.0 | 207.01 |
| stock | cl_v42:chemical | AVNT | -5.0 | 0.0 | -5.0 | -0.011165 | -5.0 | -5.0 | 0.0 | 44.66 |
| stock | metals:sco_vol_gc_hg_accel_miners|sco_vol_miners|miners | BHP | 0.0 | 6.0 | 6.0 | 0.029109000000000003 | 0.0 | 3.0 | 3.0 | 97.03 |
| stock | cl_v42:chemical | CE | -9.0 | 0.0 | -9.0 | -0.02106 | -9.0 | -9.0 | 0.0 | 46.8 |
| stock | cl_v42:refiner | DINO | -3.0 | 0.0 | -3.0 | -0.014597999999999998 | 0.0 | -3.0 | 0.0 | 97.32 |
| stock | cl_v42:refiner | DK | -10.0 | 0.0 | -10.0 | -0.035735 | 0.0 | -10.0 | 0.0 | 71.47 |
| stock | cl_v42:chemical | DOW | -23.0 | 0.0 | -23.0 | -0.037202500000000006 | -23.0 | -23.0 | 0.0 | 32.35 |
| stock | cl_v42:chemical | EMN | -6.0 | 0.0 | -6.0 | -0.022227 | -6.0 | -6.0 | 0.0 | 74.09 |
| stock | cl_v42:bwt | ERO | 17.0 | 0.0 | 17.0 | 0.033507 | 19.0 | 17.0 | 0.0 | 39.42 |
| stock | metals:miners | FSUGY | 0.0 | 10.0 | 10.0 | 0.012845000000000002 | 0.0 | 4.0 | 6.0 | 25.69 |
| stock | cl_v42:chemical | HUN | -42.0 | 0.0 | -42.0 | -0.020937 | -43.0 | -43.0 | 1.0 | 9.97 |
| stock | cl_v42:metals | HWM | 1.0 | 0.0 | 1.0 | 0.013584 | 1.0 | 1.0 | 0.0 | 271.68 |
| stock | cl_v42:chemical | LYB | -11.0 | 0.0 | -11.0 | -0.0371415 | -11.0 | -11.0 | 0.0 | 67.53 |
| stock | cl_v42:fuel | MUSA | 1.0 | 0.0 | 1.0 | 0.028486 | 1.0 | 1.0 | 0.0 | 569.72 |
| stock | cl_v42:refiner | PBF | -6.0 | 0.0 | -6.0 | -0.022059 | 0.0 | -6.0 | 0.0 | 73.53 |
| stock | cl_v42:psx_ref | PSX | -2.0 | 0.0 | -2.0 | -0.024287 | -3.0 | -2.0 | 0.0 | 242.87 |
| stock | metals:sco_vol_gc_hg_accel_miners|sco_vol_miners|miners | RIO | 0.0 | 6.0 | 6.0 | 0.03159 | 0.0 | 3.0 | 3.0 | 105.3 |
| stock | metals:sco_vol_gc_hg_accel_miners|sco_vol_miners|miners | SCCO | 0.0 | 3.0 | 3.0 | 0.0324 | 0.0 | 1.0 | 2.0 | 216.0 |
| stock | cl_v42:bwt | TECK | 3.0 | 0.0 | 3.0 | 0.01038 | 3.0 | 3.0 | 0.0 | 69.2 |
| stock | metals:sco_vol_gc_hg_accel_miners|sco_vol_miners|miners | VALE | 0.0 | 24.0 | 24.0 | 0.017508 | 0.0 | 9.0 | 15.0 | 14.59 |
| stock | cl_v42:chemical | WLK | -10.0 | 0.0 | -10.0 | -0.039465 | -10.0 | -10.0 | 0.0 | 78.93 |

## Net broker orders

| instrument | execution_action | rounded_trade_shares | current_shares | post_child_shares | patient_limit | chase_reference | execution_sequence |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ATI | BUY | 1.0 | 1.0 | 2.0 | 206.49 | 207.53 | 1 |
| BHP | BUY | 3.0 | 0.0 | 3.0 | 96.79 | 97.27 | 1 |
| DINO | SELL | -3.0 | 0.0 | -3.0 | 97.56 | 97.08 | 1 |
| DK | SELL | -10.0 | 0.0 | -10.0 | 71.65 | 71.29 | 1 |
| ERO | SELL | -2.0 | 19.0 | 17.0 | 39.52 | 39.32 | 1 |
| FSUGY | BUY | 4.0 | 0.0 | 4.0 | 25.63 | 25.75 | 1 |
| PBF | SELL | -6.0 | 0.0 | -6.0 | 73.71 | 73.35 | 1 |
| PSX | BUY | 1.0 | -3.0 | -2.0 | 242.26 | 243.48 | 1 |
| RIO | BUY | 3.0 | 0.0 | 3.0 | 105.04 | 105.56 | 1 |
| SCCO | BUY | 1.0 | 0.0 | 1.0 | 215.46 | 216.54 | 1 |
| VALE | BUY | 9.0 | 0.0 | 9.0 | 14.55 | 14.63 | 1 |
| XLE | BUY | 24.0 | 65.0 | 89.0 | 63.48 | 63.8 | 2 |
| XME | SELL | -5.0 | -9.0 | -14.0 | 119.64 | 119.04 | 2 |
