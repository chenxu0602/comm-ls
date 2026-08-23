# Combined CL v4.2 + Metals production target: 2026-08-24

This is the first shared-account production target that includes the
standalone Metals/mining alpha satellite. It combines CL v4.2 at USD 15,000
with Metals at USD 5,000 using confirmed 2026-08-22 IB positions. Historical
actual-IB performance through 2026-08-21 excludes this standalone satellite.

Each strategy first applies its own sleeve-aware integer allocation and 40%
child policy. The resulting `rounded_trade_shares` are summed by ticker. The
combined child turnover is USD 8,367.58, or 41.84% of combined USD 20,000 AUM.
Stock child turnover is 18.79% and remains subject to the 40% cap. Hedge
turnover is temporarily uncapped, so SPY, XLE and XME are completed to their
account-netted integer targets after stock fills are confirmed.

| Instrument | Action | Shares | Post-child shares | Patient | Chase |
| --- | --- | ---: | ---: | ---: | ---: |
| ATI | Buy | 1 | 2 | 206.49 | 207.53 |
| BHP | Buy | 5 | 5 | 96.79 | 97.27 |
| DINO | Sell | 3 | -3 | 97.56 | 97.08 |
| DK | Sell | 10 | -10 | 71.65 | 71.29 |
| ERO | Sell | 2 | 17 | 39.52 | 39.32 |
| FSUGY | Buy | 7 | 7 | 25.63 | 25.75 |
| PBF | Sell | 6 | -6 | 73.71 | 73.35 |
| PSX | Buy | 1 | -2 | 242.26 | 243.48 |
| RIO | Buy | 4 | 4 | 105.04 | 105.56 |
| SCCO | Buy | 2 | 2 | 215.46 | 216.54 |
| SPY | Sell | 2 | 0 | 767.63 | 763.81 |
| VALE | Buy | 18 | 18 | 14.55 | 14.63 |
| XLE | Buy | 24 | 89 | 63.48 | 63.80 |
| XME | Sell | 13 | -22 | 119.64 | 119.04 |

Stocks execute before hedge review. SPY, XLE and XME are account-netted hedge
instructions and should be checked against confirmed stock fills before
execution. Unlike stock legs, hedge legs are not throttled by the 40% daily
turnover cap. CRS remains unimplemented because both strategy-level target
allocations round it to zero; do not create a cross-book CRS share by
re-rounding continuous notionals.
