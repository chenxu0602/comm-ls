# IB Daily Reconciliation 2026-09-21

Sources:
- Activity statement: `ib_docs_crypto/2026-09-21/raw/activity_statement.csv`
- Targets: `targets-crypto/2026-09-21/targets.csv`

## Summary

- AUM basis: $3,000.00
- Fill rows: 5
- Open positions: 8
- Gross traded notional: $257.05 (8.57% of AUM)
- Commission: $-1.91 (74.33 bps of traded notional; 6.37 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $-200.70
- Daily MTM PnL after commission, base currency: 99.63
- Ending USD cash: $6,953.52

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.082 | 0.082 | 246.600 | 246.600 | 1 |
| stock_short_without_hedge | 0.453 | -0.453 | 1359.710 | -1359.710 | 6 |
| total_stock_without_hedge | 0.535 | -0.371 | 1606.310 | -1113.110 | 7 |
| total_hedge | 1.289 | 1.289 | 3867.500 | 3867.500 | 1 |
| total_portfolio | 1.825 | 0.918 | 5473.810 | 2754.390 | 8 |

## Child-Order Mismatches

None

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
