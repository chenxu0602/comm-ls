# IB Daily Reconciliation 2026-11-12

Sources:
- Activity statement: `ib_docs_crypto/2026-11-12/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-11-12/raw/pnls.csv`
- Targets: `targets-crypto/2026-11-12/targets.csv`

## Summary

- AUM basis: $4,000.00
- Fill rows: 2
- Open positions: 7
- Gross traded notional: $66.45 (1.66% of AUM)
- Commission: $-0.66 (100.00 bps of traded notional; 1.66 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $-5.71
- Daily security MTM after commission, HKD: 461.55
- Broker NAV change, HKD: 460.55; ending NAV: 200,863.57
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.844800
- Ending USD cash: $5,919.75

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| stock_short_without_hedge | 0.469 | -0.469 | 1874.670 | -1874.670 | 6 |
| total_stock_without_hedge | 0.469 | -0.469 | 1874.670 | -1874.670 | 6 |
| total_hedge | 1.514 | 1.514 | 6056.960 | 6056.960 | 1 |
| total_portfolio | 1.983 | 1.046 | 7931.630 | 4182.290 | 7 |

## Child-Order Mismatches

None

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
