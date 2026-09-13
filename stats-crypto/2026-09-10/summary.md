# IB Daily Reconciliation 2026-09-10

Sources:
- Activity statement: `ib_docs_crypto/2026-09-10/raw/activity_statement.csv`
- Targets: `targets-crypto/2026-09-10/targets.csv`

## Summary

- AUM basis: $3,000.00
- Fill rows: 3
- Open positions: 7
- Gross traded notional: $2,027.58 (67.59% of AUM)
- Commission: $-3.03 (14.95 bps of traded notional; 10.11 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $-65.01
- Daily MTM PnL after commission, base currency: 99.19
- Ending USD cash: $9,330.24

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.113 | 0.113 | 339.990 | 339.990 | 1 |
| stock_short_without_hedge | 0.171 | -0.171 | 511.670 | -511.670 | 5 |
| total_stock_without_hedge | 0.284 | -0.057 | 851.660 | -171.680 | 6 |
| total_hedge | 0.253 | 0.253 | 757.830 | 757.830 | 1 |
| total_portfolio | 0.536 | 0.195 | 1609.490 | 586.150 | 7 |

## Child-Order Mismatches

None

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
