# IB Daily Reconciliation 2026-09-18

Sources:
- Activity statement: `ib_docs_crypto/2026-09-18/raw/activity_statement.csv`
- Targets: `targets-crypto/2026-09-18/targets.csv`

## Summary

- AUM basis: $3,000.00
- Fill rows: 4
- Open positions: 8
- Gross traded notional: $81.04 (2.70% of AUM)
- Commission: $-0.81 (100.00 bps of traded notional; 2.70 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $-218.65
- Daily MTM PnL after commission, base currency: -1,157.83
- Ending USD cash: $7,212.48

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.080 | 0.080 | 239.640 | 239.640 | 1 |
| stock_short_without_hedge | 0.522 | -0.522 | 1565.360 | -1565.360 | 6 |
| total_stock_without_hedge | 0.602 | -0.442 | 1805.000 | -1325.720 | 7 |
| total_hedge | 1.269 | 1.269 | 3808.450 | 3808.450 | 1 |
| total_portfolio | 1.871 | 0.828 | 5613.450 | 2482.730 | 8 |

## Child-Order Mismatches

None

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
