# IB Daily Reconciliation 2026-11-03

Sources:
- Activity statement: `ib_docs_crypto/2026-11-03/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-11-03/raw/pnls.csv`
- Targets: `targets-crypto/2026-11-03/targets.csv`

## Summary

- AUM basis: $4,000.00
- Fill rows: 6
- Open positions: 7
- Gross traded notional: $2,112.41 (52.81% of AUM)
- Commission: $-5.92 (28.01 bps of traded notional; 14.79 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $-103.89
- Daily security MTM after commission, HKD: -1,336.72
- Broker NAV change, HKD: -1,334.68; ending NAV: 200,259.10
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.846800
- Ending USD cash: $5,403.60

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| stock_short_without_hedge | 0.542 | -0.542 | 2169.160 | -2169.160 | 6 |
| total_stock_without_hedge | 0.542 | -0.542 | 2169.160 | -2169.160 | 6 |
| total_hedge | 1.697 | 1.697 | 6789.150 | 6789.150 | 1 |
| total_portfolio | 2.240 | 1.155 | 8958.310 | 4619.990 | 7 |

## Child-Order Mismatches

None

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
