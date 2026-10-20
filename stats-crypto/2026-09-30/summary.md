# IB Daily Reconciliation 2026-09-30

Sources:
- Activity statement: `ib_docs_crypto/2026-09-30/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-09-30/raw/pnls.csv`
- Targets: `targets-crypto/2026-09-30/targets.csv`

## Summary

- AUM basis: $3,000.00
- Fill rows: 3
- Open positions: 7
- Gross traded notional: $1,077.00 (35.90% of AUM)
- Commission: $-3.02 (28.00 bps of traded notional; 10.05 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $-39.63
- Daily security MTM after commission, HKD: -21.00
- Broker NAV change, HKD: -13.02; ending NAV: 197,966.21
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.846800
- Ending USD cash: $9,722.73

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.175 | 0.175 | 523.910 | 523.910 | 2 |
| stock_short_without_hedge | 0.174 | -0.174 | 520.870 | -520.870 | 5 |
| total_stock_without_hedge | 0.348 | 0.001 | 1044.780 | 3.040 | 7 |
| total_hedge | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| total_portfolio | 0.348 | 0.001 | 1044.780 | 3.040 | 7 |

## Child-Order Mismatches

None

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
