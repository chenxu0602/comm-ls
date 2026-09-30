# IB Daily Reconciliation 2026-09-17

Sources:
- Activity statement: `ib_docs_crypto/2026-09-17/raw/activity_statement.csv`
- Targets: `targets-crypto/2026-09-17/targets.csv`

## Summary

- AUM basis: $3,000.00
- Fill rows: 2
- Open positions: 8
- Gross traded notional: $299.45 (9.98% of AUM)
- Commission: $-2.01 (67.01 bps of traded notional; 6.69 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $-71.06
- Daily MTM PnL after commission, base currency: -161.13
- Ending USD cash: $7,294.33

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.073 | 0.073 | 219.620 | 219.620 | 1 |
| stock_short_without_hedge | 0.495 | -0.495 | 1484.150 | -1484.150 | 6 |
| total_stock_without_hedge | 0.568 | -0.422 | 1703.770 | -1264.530 | 7 |
| total_hedge | 1.271 | 1.271 | 3813.000 | 3813.000 | 1 |
| total_portfolio | 1.839 | 0.849 | 5516.770 | 2548.470 | 8 |

## Child-Order Mismatches

None

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
