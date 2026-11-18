# IB Daily Reconciliation 2026-11-10

Sources:
- Activity statement: `ib_docs_crypto/2026-11-10/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-11-10/raw/pnls.csv`
- Targets: `targets-crypto/2026-11-10/targets.csv`

## Summary

- AUM basis: $4,000.00
- Fill rows: 7
- Open positions: 7
- Gross traded notional: $2,028.77 (50.72% of AUM)
- Commission: $-5.82 (28.68 bps of traded notional; 14.55 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $-90.86
- Daily security MTM after commission, HKD: -37.65
- Broker NAV change, HKD: -3.56; ending NAV: 200,233.83
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.845400
- Ending USD cash: $5,966.09

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| stock_short_without_hedge | 0.486 | -0.486 | 1944.450 | -1944.450 | 6 |
| total_stock_without_hedge | 0.486 | -0.486 | 1944.450 | -1944.450 | 6 |
| total_hedge | 1.500 | 1.500 | 5999.360 | 5999.360 | 1 |
| total_portfolio | 1.986 | 1.014 | 7943.810 | 4054.910 | 7 |

## Child-Order Mismatches

None

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
