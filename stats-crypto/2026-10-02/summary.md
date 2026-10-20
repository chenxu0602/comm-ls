# IB Daily Reconciliation 2026-10-02

Sources:
- Activity statement: `ib_docs_crypto/2026-10-02/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-10-02/raw/pnls.csv`
- Targets: `targets-crypto/2026-10-02/targets.csv`

## Summary

- AUM basis: $3,000.00
- Fill rows: 6
- Open positions: 7
- Gross traded notional: $1,127.28 (37.58% of AUM)
- Commission: $-3.48 (30.89 bps of traded notional; 11.61 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $-5.59
- Daily security MTM after commission, HKD: 215.31
- Broker NAV change, HKD: 227.96; ending NAV: 198,170.99
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.847100
- Ending USD cash: $6,458.45

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| stock_short_without_hedge | 0.441 | -0.441 | 1324.330 | -1324.330 | 6 |
| total_stock_without_hedge | 0.441 | -0.441 | 1324.330 | -1324.330 | 6 |
| total_hedge | 1.539 | 1.539 | 4617.840 | 4617.840 | 1 |
| total_portfolio | 1.981 | 1.098 | 5942.170 | 3293.510 | 7 |

## Child-Order Mismatches

None

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
