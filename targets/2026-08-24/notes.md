# Combined CL v4.2 + Metals production target: 2026-08-24

This is the first shared-account production target that includes the
standalone Metals/mining alpha satellite. It combines CL v4.2 at USD 15,000
with Metals at USD 5,000 using confirmed 2026-08-22 IB positions. Historical
actual-IB performance through 2026-08-21 excludes this standalone satellite.

Each strategy first applies its own sleeve-aware integer allocation and 40%
child policy. The resulting `rounded_trade_shares` are summed by ticker. The
combined child turnover is USD 5,157.68, or 25.79% of combined USD 20,000 AUM,
so no additional account-level scaling is required.

| Instrument | Action | Shares | Post-child shares | Patient | Chase |
| --- | --- | ---: | ---: | ---: | ---: |
| ATI | Buy | 1 | 2 | 206.49 | 207.53 |
| BHP | Buy | 3 | 3 | 96.79 | 97.27 |
| DINO | Sell | 3 | -3 | 97.56 | 97.08 |
| DK | Sell | 10 | -10 | 71.65 | 71.29 |
| ERO | Sell | 2 | 17 | 39.52 | 39.32 |
| FSUGY | Buy | 4 | 4 | 25.63 | 25.75 |
| PBF | Sell | 6 | -6 | 73.71 | 73.35 |
| PSX | Buy | 1 | -2 | 242.26 | 243.48 |
| RIO | Buy | 3 | 3 | 105.04 | 105.56 |
| SCCO | Buy | 1 | 1 | 215.46 | 216.54 |
| VALE | Buy | 9 | 9 | 14.55 | 14.63 |
| XLE | Buy | 24 | 89 | 63.48 | 63.80 |
| XME | Sell | 5 | -14 | 119.64 | 119.04 |

Stocks execute before hedge review. XLE and XME are the net child hedge
instructions from the two strategy packages and should be checked against
confirmed stock fills before execution. There is no SPY child order on this
first Metals implementation day. CRS remains unimplemented because both
strategy-level target allocations round it to zero; do not create a cross-book
CRS share by re-rounding continuous notionals.
