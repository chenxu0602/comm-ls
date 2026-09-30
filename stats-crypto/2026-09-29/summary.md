# IB Daily Reconciliation 2026-09-29

Sources:
- Activity statement: `ib_docs_crypto/2026-09-29/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-09-29/raw/pnls.csv`
- Targets: `targets-crypto/2026-09-29/targets.csv`

## Summary

- AUM basis: $3,000.00
- Fill rows: 1
- Open positions: 7
- Gross traded notional: $766.95 (25.56% of AUM)
- Commission: $-1.02 (13.25 bps of traded notional; 3.39 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $-36.35
- Daily security MTM after commission, HKD: 30.16
- Broker NAV change, HKD: 44.76; ending NAV: 197,979.23
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.846800
- Ending USD cash: $9,268.75

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.077 | 0.077 | 232.440 | 232.440 | 1 |
| stock_short_without_hedge | 0.179 | -0.179 | 536.940 | -536.940 | 5 |
| total_stock_without_hedge | 0.256 | -0.101 | 769.380 | -304.500 | 6 |
| total_hedge | 0.255 | 0.255 | 764.200 | 764.200 | 1 |
| total_portfolio | 0.511 | 0.153 | 1533.580 | 459.700 | 7 |

## Child-Order Mismatches

None

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
