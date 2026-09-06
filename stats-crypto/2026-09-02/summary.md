# IB Daily Reconciliation 2026-09-02

Sources:
- Activity statement: `ib_docs_crypto/2026-09-02/raw/activity_statement.csv`
- Targets: `targets-crypto/2026-09-02/targets.csv`

## Summary

- AUM basis: $2,000.00
- Fill rows: 7
- Open positions: 7
- Gross traded notional: $3,040.60 (152.03% of AUM)
- Commission: $-6.74 (22.18 bps of traded notional; 33.72 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $-11.50
- Daily MTM PnL after commission, base currency: -90.22
- Ending USD cash: $8,461.86

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| stock_short_without_hedge | 0.384 | -0.384 | 768.840 | -768.840 | 6 |
| total_stock_without_hedge | 0.384 | -0.384 | 768.840 | -768.840 | 6 |
| total_hedge | 1.148 | 1.148 | 2295.480 | 2295.480 | 1 |
| total_portfolio | 1.532 | 0.763 | 3064.320 | 1526.640 | 7 |

## Child-Order Mismatches

None

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
