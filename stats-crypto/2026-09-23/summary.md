# IB Daily Reconciliation 2026-09-23

Sources:
- Activity statement: `ib_docs_crypto/2026-09-23/raw/activity_statement.csv`
- Targets: `targets-crypto/2026-09-23/targets.csv`

## Summary

- AUM basis: $3,000.00
- Fill rows: 2
- Open positions: 7
- Gross traded notional: $2,449.61 (81.65% of AUM)
- Commission: $-2.05 (8.36 bps of traded notional; 6.83 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $-73.94
- Daily MTM PnL after commission, base currency: -39.67
- Ending USD cash: $8,574.50

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.041 | 0.041 | 122.700 | 122.700 | 1 |
| stock_short_without_hedge | 0.178 | -0.178 | 535.290 | -535.290 | 5 |
| total_stock_without_hedge | 0.219 | -0.138 | 657.990 | -412.590 | 6 |
| total_hedge | 0.512 | 0.512 | 1535.620 | 1535.620 | 1 |
| total_portfolio | 0.731 | 0.374 | 2193.610 | 1123.030 | 7 |

## Child-Order Mismatches

None

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
