# IB Daily Reconciliation 2026-10-27

Sources:
- Activity statement: `ib_docs_crypto/2026-10-27/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-10-27/raw/pnls.csv`
- Targets: `targets-crypto/2026-10-27/targets.csv`

## Summary

- AUM basis: $4,000.00
- Fill rows: 7
- Open positions: 8
- Gross traded notional: $4,035.53 (100.89% of AUM)
- Commission: $-6.90 (17.10 bps of traded notional; 17.25 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $126.36
- Daily security MTM after commission, HKD: -473.91
- Broker NAV change, HKD: -481.02; ending NAV: 200,821.37
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.844800
- Ending USD cash: $3,048.77

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| stock_short_without_hedge | 0.741 | -0.741 | 2963.390 | -2963.390 | 7 |
| total_stock_without_hedge | 0.741 | -0.741 | 2963.390 | -2963.390 | 7 |
| total_hedge | 2.501 | 2.501 | 10005.580 | 10005.580 | 1 |
| total_portfolio | 3.242 | 1.761 | 12968.970 | 7042.190 | 8 |

## Child-Order Mismatches

None

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
