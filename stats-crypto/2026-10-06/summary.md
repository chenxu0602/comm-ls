# IB Daily Reconciliation 2026-10-06

Sources:
- Activity statement: `ib_docs_crypto/2026-10-06/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-10-06/raw/pnls.csv`
- Targets: `targets-crypto/2026-10-06/targets.csv`

## Summary

- AUM basis: $3,000.00
- Fill rows: 0
- Open positions: 7
- Gross traded notional: $0.00 (0.00% of AUM)
- Commission: $0.00 (nan bps of traded notional; -0.00 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $36.90
- Daily security MTM after commission, HKD: 203.57
- Broker NAV change, HKD: 211.40; ending NAV: 198,610.77
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.847600
- Ending USD cash: $7,581.35

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.075 | 0.075 | 224.000 | 224.000 | 1 |
| stock_short_without_hedge | 0.372 | -0.372 | 1114.870 | -1114.870 | 5 |
| total_stock_without_hedge | 0.446 | -0.297 | 1338.870 | -890.870 | 6 |
| total_hedge | 1.039 | 1.039 | 3116.360 | 3116.360 | 1 |
| total_portfolio | 1.485 | 0.742 | 4455.230 | 2225.490 | 7 |

## Child-Order Mismatches

None

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
