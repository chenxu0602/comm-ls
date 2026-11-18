# IB Daily Reconciliation 2026-11-06

Sources:
- Activity statement: `ib_docs_crypto/2026-11-06/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-11-06/raw/pnls.csv`
- Targets: `targets-crypto/2026-11-06/targets.csv`

## Summary

- AUM basis: $4,000.00
- Fill rows: 8
- Open positions: 8
- Gross traded notional: $3,128.70 (78.22% of AUM)
- Commission: $-7.86 (25.11 bps of traded notional; 19.64 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $-238.83
- Daily security MTM after commission, HKD: -249.27
- Broker NAV change, HKD: -265.28; ending NAV: 199,810.36
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.839700
- Ending USD cash: $6,995.99

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.020 | 0.020 | 80.910 | 80.910 | 1 |
| stock_short_without_hedge | 0.379 | -0.379 | 1514.370 | -1514.370 | 6 |
| total_stock_without_hedge | 0.399 | -0.358 | 1595.280 | -1433.460 | 7 |
| total_hedge | 1.103 | 1.103 | 4411.740 | 4411.740 | 1 |
| total_portfolio | 1.502 | 0.745 | 6007.020 | 2978.280 | 8 |

## Child-Order Mismatches

None

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
