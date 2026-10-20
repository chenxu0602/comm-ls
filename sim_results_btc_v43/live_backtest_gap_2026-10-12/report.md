# Crypto live versus backtest audit



Period: 2026-09-02 to 2026-10-12. Saved export matches daily_net; max error 4.389e-16.



```

                  period  sessions  actual_usd   stock_usd   spy_usd  trade_usd    fee_usd  other_usd  actual_return  weekly_net  daily_net  archived_signal_weekly_net  archived_signal_daily_net  legacy_continuous_net  bridge_add_back_notebook_stock_cost  bridge_residual_to_explicit_basis  bridge_archived_target_timing_and_configuration  bridge_integer_buffers_and_price_basis  bridge_opening_inventory_vs_same_day_target  bridge_trade_to_close  bridge_actual_fees_and_other  weekly_net_reference_usd  daily_net_reference_usd
                   pilot        28  -61.954027 -135.139431 73.185403     -0.805 -69.229027        0.0      -0.036114    0.021856   0.038475                   -0.019409                   0.008641               0.019395                             0.005675                               -0.0                                        -0.033183                               -0.010008                                    -0.012369              -0.000664                     -0.024040                 94.840107               140.775422
launch_old_configuration         3  -81.973423 -105.543414 23.569991     -0.950  -7.523423        0.0      -0.040987   -0.021153  -0.017755                   -0.038201                  -0.032005              -0.017805                             0.000000                                0.0                                        -0.013316                               -0.004524                                    -0.001155              -0.000475                     -0.003762                -42.306826               -35.509526
   current_configuration        25   20.019396  -29.596017 49.615412      0.145 -61.705604        0.0       0.004873    0.043009   0.056230                    0.018792                   0.040646               0.037200                             0.005675                               -0.0                                        -0.019867                               -0.005484                                    -0.011214              -0.000189                     -0.020278                137.146933               176.284948
                 october         8  212.273094  152.175853 60.097241      7.385 -23.441906        0.0       0.068957    0.067357   0.083624                    0.066719                   0.083095               0.081123                             0.000750                               -0.0                                        -0.000624                               -0.001053                                    -0.008441               0.002224                     -0.007523                210.189327               258.466552

```



The bridge from daily residual net to actual security MTM reconciles within 1e-10 daily.

AUM: $2,000 before Sep8, $3,000 Sep8-Oct9, $4,000 from Oct12. Totals in return units sum daily normalized returns; USD totals sum actual cash amounts.

The Sep2-Sep4 strategy differs from today's four-sleeve notebook. Archived-target full-session gross is a counterfactual; target weights and integer shares are not confirmed fills.

Current notebook history uses refreshed inputs and may differ from archived signals. L1 target discrepancies and actual-minus-planned fills are exported.

Archived-signal residual replays keep the CURRENT return/beta series and the notebook's extra holding delay and 25bps stock cost; they change only the stock weight history to the dated archived targets. They are not actual-fill simulations and regenerated target packages may not preserve every original plan.

The integer/buffer bridge also contains adjusted-log versus broker dollar-return basis. Opening-inventory differences contain holding delay, deferred fills and AUM migration; they are not execution slippage.

Trade-to-close MTM measures how fills performed versus retaining opening inventory through close. It is not execution shortfall versus arrival/30-minute VWAP.

Legacy explicit net applies hypothetical 25bps ETF turnover costs, which are not actual IB commissions. Actual fees must not be charged twice.

Security MTM excludes account cash FX, funding and costs not allocated to instrument rows. Account NAV and realized/open-unrealized PnL are different quantities.

A launch-day normalization uses separately reported USD fill-to-close PnL and commission identities; all subsequent days use the existing validated MTM parser.

Current-input historical production signal replay (not archived-input reconstruction):

```

      date instrument  archived  current_production_replay  current_notebook
2026-09-18       COIN    -0.060                      0.060             0.060
2026-09-18       HOOD     0.060                      0.120             0.120
2026-09-18       MARA    -0.075                     -0.015            -0.015
2026-09-18       RIOT    -0.065                      0.005             0.005
2026-09-18       CLSK    -0.100                     -0.020            -0.020
2026-09-18       MSTR    -0.075                     -0.060            -0.060
2026-09-18       HIVE    -0.085                     -0.035            -0.035

```
