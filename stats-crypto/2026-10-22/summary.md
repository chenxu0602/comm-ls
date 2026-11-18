# IB Daily Reconciliation 2026-10-22

Sources:
- Activity statement: `ib_docs_crypto/2026-10-22/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-10-22/raw/pnls.csv`
- Targets: `targets-crypto/2026-10-22/targets.csv`

## Summary

- AUM basis: $4,000.00
- Fill rows: 7
- Open positions: 8
- Gross traded notional: $2,473.36 (61.83% of AUM)
- Commission: $-6.97 (28.19 bps of traded notional; 17.43 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $332.21
- Daily security MTM after commission, HKD: 485.42
- Broker NAV change, HKD: 380.41; ending NAV: 200,468.85
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.836600
- Ending USD cash: $5,079.32

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| stock_short_without_hedge | 0.475 | -0.475 | 1898.410 | -1898.410 | 7 |
| total_stock_without_hedge | 0.475 | -0.475 | 1898.410 | -1898.410 | 7 |
| total_hedge | 1.719 | 1.719 | 6875.640 | 6875.640 | 1 |
| total_portfolio | 2.194 | 1.244 | 8774.050 | 4977.230 | 8 |

## Child-Order Mismatches

None

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
