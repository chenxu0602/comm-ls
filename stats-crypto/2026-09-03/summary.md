# IB Daily Reconciliation 2026-09-03

Sources:
- Activity statement: `ib_docs_crypto/2026-09-03/raw/activity_statement.csv`
- Targets: `targets-crypto/2026-09-03/targets.csv`

## Summary

- AUM basis: $2,000.00
- Fill rows: 1
- Open positions: 7
- Gross traded notional: $11.31 (0.57% of AUM)
- Commission: $-0.11 (100.00 bps of traded notional; 0.57 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $-80.75
- Daily MTM PnL after commission, base currency: -542.85
- Ending USD cash: $8,450.43

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| stock_short_without_hedge | 0.425 | -0.425 | 850.690 | -850.690 | 6 |
| total_stock_without_hedge | 0.425 | -0.425 | 850.690 | -850.690 | 6 |
| total_hedge | 1.160 | 1.160 | 2319.510 | 2319.510 | 1 |
| total_portfolio | 1.585 | 0.734 | 3170.200 | 1468.820 | 7 |

## Child-Order Mismatches

None

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
