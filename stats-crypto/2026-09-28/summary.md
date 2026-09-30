# IB Daily Reconciliation 2026-09-28

Sources:
- Activity statement: `ib_docs_crypto/2026-09-28/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-09-28/raw/pnls.csv`
- Targets: `targets-crypto/2026-09-28/targets.csv`

## Summary

- AUM basis: $3,000.00
- Fill rows: 3
- Open positions: 7
- Gross traded notional: $145.21 (4.84% of AUM)
- Commission: $-1.27 (87.12 bps of traded notional; 4.22 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $-40.20
- Daily security MTM after commission, HKD: 1.06
- Broker NAV change, HKD: 11.76; ending NAV: 197,934.47
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.845300
- Ending USD cash: $8,502.81

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.078 | 0.078 | 232.920 | 232.920 | 1 |
| stock_short_without_hedge | 0.181 | -0.181 | 542.350 | -542.350 | 5 |
| total_stock_without_hedge | 0.258 | -0.103 | 775.270 | -309.430 | 6 |
| total_hedge | 0.510 | 0.510 | 1531.220 | 1531.220 | 1 |
| total_portfolio | 0.769 | 0.407 | 2306.490 | 1221.790 | 7 |

## Child-Order Mismatches

None

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
