# IB Daily Reconciliation 2026-10-20

Sources:
- Activity statement: `ib_docs_crypto/2026-10-20/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-10-20/raw/pnls.csv`
- Targets: `targets-crypto/2026-10-20/targets.csv`

## Summary

- AUM basis: $4,000.00
- Fill rows: 8
- Open positions: 7
- Gross traded notional: $5,935.85 (148.40% of AUM)
- Commission: $-7.44 (12.54 bps of traded notional; 18.61 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $267.02
- Daily security MTM after commission, HKD: -73.50
- Broker NAV change, HKD: -69.47; ending NAV: 200,507.78
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.848700
- Ending USD cash: $4,120.96

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| stock_short_without_hedge | 0.634 | -0.634 | 2534.520 | -2534.520 | 6 |
| total_stock_without_hedge | 0.634 | -0.634 | 2534.520 | -2534.520 | 6 |
| total_hedge | 2.115 | 2.115 | 8459.550 | 8459.550 | 1 |
| total_portfolio | 2.749 | 1.481 | 10994.070 | 5925.030 | 7 |

## Child-Order Mismatches

None

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
