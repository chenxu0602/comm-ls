# IB Daily Reconciliation 2026-09-24

Sources:
- Activity statement: `ib_docs_crypto/2026-09-24/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-09-24/raw/pnls.csv`
- Targets: `targets-crypto/2026-09-24/targets.csv`

## Summary

- AUM basis: $3,000.00
- Fill rows: 0
- Open positions: 7
- Gross traded notional: $0.00 (0.00% of AUM)
- Commission: $0.00 (nan bps of traded notional; -0.00 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $-60.42
- Daily security MTM after commission, HKD: 53.80
- Broker NAV change, HKD: 45.07; ending NAV: 197,748.66
- MTM source convention: `inverted_usd`; normalization factor: -7.842500; USD/HKD: 7.842500
- Ending USD cash: $8,574.50

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.040 | 0.040 | 120.820 | 120.820 | 1 |
| stock_short_without_hedge | 0.175 | -0.175 | 525.290 | -525.290 | 5 |
| total_stock_without_hedge | 0.215 | -0.135 | 646.110 | -404.470 | 6 |
| total_hedge | 0.511 | 0.511 | 1534.360 | 1534.360 | 1 |
| total_portfolio | 0.727 | 0.377 | 2180.470 | 1129.890 | 7 |

## Child-Order Mismatches

None

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
