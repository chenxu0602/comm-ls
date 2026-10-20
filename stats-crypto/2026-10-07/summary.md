# IB Daily Reconciliation 2026-10-07

Sources:
- Activity statement: `ib_docs_crypto/2026-10-07/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-10-07/raw/pnls.csv`
- Targets: `targets-crypto/2026-10-07/targets.csv`

## Summary

- AUM basis: $3,000.00
- Fill rows: 1
- Open positions: 7
- Gross traded notional: $18.50 (0.62% of AUM)
- Commission: $-0.19 (100.21 bps of traded notional; 0.62 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $81.56
- Daily security MTM after commission, HKD: 350.47
- Broker NAV change, HKD: 359.30; ending NAV: 198,970.08
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.848500
- Ending USD cash: $7,599.66

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.073 | 0.073 | 219.020 | 219.020 | 1 |
| stock_short_without_hedge | 0.359 | -0.359 | 1076.070 | -1076.070 | 5 |
| total_stock_without_hedge | 0.432 | -0.286 | 1295.090 | -857.050 | 6 |
| total_hedge | 1.036 | 1.036 | 3108.880 | 3108.880 | 1 |
| total_portfolio | 1.468 | 0.751 | 4403.970 | 2251.830 | 7 |

## Child-Order Mismatches

None

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
