# IB Daily Reconciliation 2026-10-08

Sources:
- Activity statement: `ib_docs_crypto/2026-10-08/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-10-08/raw/pnls.csv`
- Targets: `targets-crypto/2026-10-08/targets.csv`

## Summary

- AUM basis: $3,000.00
- Fill rows: 6
- Open positions: 6
- Gross traded notional: $1,071.63 (35.72% of AUM)
- Commission: $-3.52 (32.82 bps of traded notional; 11.72 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $122.83
- Daily security MTM after commission, HKD: 323.96
- Broker NAV change, HKD: 321.00; ending NAV: 199,291.08
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.848200
- Ending USD cash: $8,074.70

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.071 | 0.071 | 214.020 | 214.020 | 1 |
| stock_short_without_hedge | 0.239 | -0.239 | 717.740 | -717.740 | 4 |
| total_stock_without_hedge | 0.311 | -0.168 | 931.760 | -503.720 | 5 |
| total_hedge | 0.774 | 0.774 | 2321.790 | 2321.790 | 1 |
| total_portfolio | 1.085 | 0.606 | 3253.550 | 1818.070 | 6 |

## Child-Order Mismatches

None

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
