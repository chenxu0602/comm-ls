# IB Daily Reconciliation 2026-10-01

Sources:
- Activity statement: `ib_docs_crypto/2026-10-01/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-10-01/raw/pnls.csv`
- Targets: `targets-crypto/2026-10-01/targets.csv`

## Summary

- AUM basis: $3,000.00
- Fill rows: 7
- Open positions: 7
- Gross traded notional: $4,793.41 (159.78% of AUM)
- Commission: $-6.99 (14.58 bps of traded notional; 23.30 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $-46.37
- Daily security MTM after commission, HKD: -9.81
- Broker NAV change, HKD: -23.18; ending NAV: 197,943.03
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.845800
- Ending USD cash: $6,879.15

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.037 | 0.037 | 111.150 | 111.150 | 1 |
| stock_short_without_hedge | 0.362 | -0.362 | 1085.730 | -1085.730 | 5 |
| total_stock_without_hedge | 0.399 | -0.325 | 1196.880 | -974.580 | 6 |
| total_hedge | 1.273 | 1.273 | 3819.950 | 3819.950 | 1 |
| total_portfolio | 1.672 | 0.948 | 5016.830 | 2845.370 | 7 |

## Child-Order Mismatches

None

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
