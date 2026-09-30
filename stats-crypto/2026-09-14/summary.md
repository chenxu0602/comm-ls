# IB Daily Reconciliation 2026-09-14

Sources:
- Activity statement: `ib_docs_crypto/2026-09-14/raw/activity_statement.csv`
- Targets: `targets-crypto/2026-09-14/targets.csv`

## Summary

- AUM basis: $3,000.00
- Fill rows: 2
- Open positions: 7
- Gross traded notional: $23.82 (0.79% of AUM)
- Commission: $-0.24 (101.26 bps of traded notional; 0.80 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $-90.48
- Daily MTM PnL after commission, base currency: 57.17
- Ending USD cash: $7,727.65

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.114 | 0.114 | 342.990 | 342.990 | 1 |
| stock_short_without_hedge | 0.409 | -0.409 | 1227.020 | -1227.020 | 5 |
| total_stock_without_hedge | 0.523 | -0.295 | 1570.010 | -884.030 | 6 |
| total_hedge | 1.015 | 1.015 | 3043.520 | 3043.520 | 1 |
| total_portfolio | 1.538 | 0.720 | 4613.530 | 2159.490 | 7 |

## Child-Order Mismatches

None

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
