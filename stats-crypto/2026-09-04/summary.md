# IB Daily Reconciliation 2026-09-04

Sources:
- Activity statement: `ib_docs_crypto/2026-09-04/raw/activity_statement.csv`
- Targets: `targets-crypto/2026-09-04/targets.csv`

## Summary

- AUM basis: $2,000.00
- Fill rows: 4
- Open positions: 7
- Gross traded notional: $65.03 (3.25% of AUM)
- Commission: $-0.67 (102.31 bps of traded notional; 3.33 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $-81.37
- Daily MTM PnL after commission, base currency: -9.61
- Ending USD cash: $8,384.74

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| stock_short_without_hedge | 0.389 | -0.389 | 777.280 | -777.280 | 6 |
| total_stock_without_hedge | 0.389 | -0.389 | 777.280 | -777.280 | 6 |
| total_hedge | 1.155 | 1.155 | 2310.570 | 2310.570 | 1 |
| total_portfolio | 1.544 | 0.767 | 3087.850 | 1533.290 | 7 |

## Child-Order Mismatches

None

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
