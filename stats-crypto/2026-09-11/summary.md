# IB Daily Reconciliation 2026-09-11

Sources:
- Activity statement: `ib_docs_crypto/2026-09-11/raw/activity_statement.csv`
- Targets: `targets-crypto/2026-09-11/targets.csv`

## Summary

- AUM basis: $3,000.00
- Fill rows: 6
- Open positions: 7
- Gross traded notional: $3,017.50 (100.58% of AUM)
- Commission: $-6.03 (19.99 bps of traded notional; 20.10 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $-97.77
- Daily MTM PnL after commission, base currency: -286.58
- Ending USD cash: $7,751.71

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.113 | 0.113 | 337.710 | 337.710 | 1 |
| stock_short_without_hedge | 0.422 | -0.422 | 1266.730 | -1266.730 | 5 |
| total_stock_without_hedge | 0.535 | -0.310 | 1604.440 | -929.020 | 6 |
| total_hedge | 1.019 | 1.019 | 3057.160 | 3057.160 | 1 |
| total_portfolio | 1.554 | 0.709 | 4661.600 | 2128.140 | 7 |

## Child-Order Mismatches

None

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
