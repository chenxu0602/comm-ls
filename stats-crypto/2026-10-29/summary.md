# IB Daily Reconciliation 2026-10-29

Sources:
- Activity statement: `ib_docs_crypto/2026-10-29/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-10-29/raw/pnls.csv`
- Targets: `targets-crypto/2026-10-29/targets.csv`

## Summary

- AUM basis: $4,000.00
- Fill rows: 4
- Open positions: 8
- Gross traded notional: $95.97 (2.40% of AUM)
- Commission: $-0.98 (101.73 bps of traded notional; 2.44 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $80.10
- Daily security MTM after commission, HKD: 347.13
- Broker NAV change, HKD: 350.14; ending NAV: 200,661.47
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.845900
- Ending USD cash: $2,843.22

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| stock_short_without_hedge | 0.694 | -0.694 | 2775.730 | -2775.730 | 7 |
| total_stock_without_hedge | 0.694 | -0.694 | 2775.730 | -2775.730 | 7 |
| total_hedge | 2.500 | 2.500 | 10001.680 | 10001.680 | 1 |
| total_portfolio | 3.194 | 1.806 | 12777.410 | 7225.950 | 8 |

## Child-Order Mismatches

None

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
