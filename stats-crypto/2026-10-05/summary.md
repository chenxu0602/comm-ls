# IB Daily Reconciliation 2026-10-05

Sources:
- Activity statement: `ib_docs_crypto/2026-10-05/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-10-05/raw/pnls.csv`
- Targets: `targets-crypto/2026-10-05/targets.csv`

## Summary

- AUM basis: $3,000.00
- Fill rows: 3
- Open positions: 7
- Gross traded notional: $1,957.53 (65.25% of AUM)
- Commission: $-3.03 (15.49 bps of traded notional; 10.11 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $31.39
- Daily security MTM after commission, HKD: 231.31
- Broker NAV change, HKD: 228.38; ending NAV: 198,399.38
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.846800
- Ending USD cash: $7,581.35

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.076 | 0.076 | 228.220 | 228.220 | 1 |
| stock_short_without_hedge | 0.376 | -0.376 | 1127.990 | -1127.990 | 5 |
| total_stock_without_hedge | 0.452 | -0.300 | 1356.210 | -899.770 | 6 |
| total_hedge | 1.033 | 1.033 | 3099.320 | 3099.320 | 1 |
| total_portfolio | 1.485 | 0.733 | 4455.530 | 2199.550 | 7 |

## Child-Order Mismatches

None

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
