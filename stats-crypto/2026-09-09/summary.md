# IB Daily Reconciliation 2026-09-09

Sources:
- Activity statement: `ib_docs_crypto/2026-09-09/raw/activity_statement.csv`
- Targets: `targets-crypto/2026-09-09/targets.csv`

## Summary

- AUM basis: $3,000.00
- Fill rows: 1
- Open positions: 7
- Gross traded notional: $24.96 (0.83% of AUM)
- Commission: $-0.26 (104.82 bps of traded notional; 0.87 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $-81.83
- Daily MTM PnL after commission, base currency: 6.97
- Ending USD cash: $8,322.85

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| stock_short_without_hedge | 0.235 | -0.235 | 706.310 | -706.310 | 6 |
| total_stock_without_hedge | 0.235 | -0.235 | 706.310 | -706.310 | 6 |
| total_hedge | 0.762 | 0.762 | 2287.200 | 2287.200 | 1 |
| total_portfolio | 0.998 | 0.527 | 2993.510 | 1580.890 | 7 |

## Child-Order Mismatches

None

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
