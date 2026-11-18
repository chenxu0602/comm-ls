# IB Daily Reconciliation 2026-11-02

Sources:
- Activity statement: `ib_docs_crypto/2026-11-02/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-11-02/raw/pnls.csv`
- Targets: `targets-crypto/2026-11-02/targets.csv`

## Summary

- AUM basis: $4,000.00
- Fill rows: 7
- Open positions: 7
- Gross traded notional: $5,700.56 (142.51% of AUM)
- Commission: $-7.09 (12.45 bps of traded notional; 17.74 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $178.98
- Daily security MTM after commission, HKD: 690.70
- Broker NAV change, HKD: 706.96; ending NAV: 201,593.78
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.846600
- Ending USD cash: $6,311.91

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| stock_short_without_hedge | 0.346 | -0.346 | 1382.670 | -1382.670 | 6 |
| total_stock_without_hedge | 0.346 | -0.346 | 1382.670 | -1382.670 | 6 |
| total_hedge | 1.316 | 1.316 | 5264.700 | 5264.700 | 1 |
| total_portfolio | 1.662 | 0.971 | 6647.370 | 3882.030 | 7 |

## Child-Order Mismatches

None

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
