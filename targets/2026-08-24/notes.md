# Combined CL v4.2 + Metals production target: 2026-08-24

This is the first shared-account production target that includes the
standalone Metals/mining alpha satellite. It combines CL v4.2 at USD 15,000
with Metals at USD 5,000 using confirmed 2026-08-22 IB positions. Historical
actual-IB performance through 2026-08-21 excludes this standalone satellite.

Each strategy first applies its own sleeve-aware integer allocation. For this
initial Metals deployment only, the operator elected to remove the usual 40%
Metals stock-turnover throttle and generated the Metals child package with a
100% stock cap. This keeps the fully executed Metals stock basket aligned with
its full explicit hedge. This is a one-day override, not a prospective change
to the default 40% policy.

The resulting `rounded_trade_shares` are summed by ticker. Combined child
turnover is USD 9,055.82, or 45.28% of combined USD 20,000 AUM. Stock child
turnover is 22.23%; hedge turnover is 23.05%. Hedge turnover remains uncapped,
so SPY, XLE and XME are completed to their account-netted integer targets only
after stock fills are confirmed.

| Instrument | Action | Shares | Post-child shares | Patient | Chase |
| --- | --- | ---: | ---: | ---: | ---: |
| ATI | Buy | 1 | 2 | 206.49 | 207.53 |
| BHP | Buy | 6 | 6 | 96.79 | 97.27 |
| DINO | Sell | 3 | -3 | 97.56 | 97.08 |
| DK | Sell | 10 | -10 | 71.65 | 71.29 |
| ERO | Sell | 2 | 17 | 39.52 | 39.32 |
| FSUGY | Buy | 10 | 10 | 25.63 | 25.75 |
| PBF | Sell | 6 | -6 | 73.71 | 73.35 |
| PSX | Buy | 1 | -2 | 242.26 | 243.48 |
| RIO | Buy | 6 | 6 | 105.04 | 105.56 |
| SCCO | Buy | 3 | 3 | 215.46 | 216.54 |
| SPY | Sell | 2 | 0 | 767.63 | 763.81 |
| VALE | Buy | 24 | 24 | 14.55 | 14.63 |
| XLE | Buy | 24 | 89 | 63.48 | 63.80 |
| XME | Sell | 13 | -22 | 119.64 | 119.04 |

This package supersedes the earlier capped package for the same date. If the
earlier orders are still working, amend/cancel-replace them rather than adding
new orders: BHP 5→6, FSUGY 7→10, RIO 4→6, SCCO 2→3 and VALE 18→24. All other
listed quantities are unchanged.

Stocks execute before hedge review. SPY, XLE and XME are account-netted hedge
instructions and should be checked against confirmed stock fills before
execution. Unlike stock legs, hedge legs are not throttled by the daily stock
turnover cap. All rounded Metals stock targets are completed in this package.
CRS remains unimplemented because both strategy-level allocations round it to
zero; do not create a cross-book CRS share by re-rounding continuous notionals.
HUN remains one share away from its CL target because of the CL trade buffer;
this is unrelated to the Metals turnover policy.
