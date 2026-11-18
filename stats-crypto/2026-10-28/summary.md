# IB Daily Reconciliation 2026-10-28

Sources:
- Activity statement: `ib_docs_crypto/2026-10-28/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-10-28/raw/pnls.csv`
- Targets: `targets-crypto/2026-10-28/targets.csv`

## Summary

- AUM basis: $4,000.00
- Fill rows: 4
- Open positions: 8
- Gross traded notional: $107.53 (2.69% of AUM)
- Commission: $-1.08 (100.42 bps of traded notional; 2.70 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $60.32
- Daily security MTM after commission, HKD: -518.12
- Broker NAV change, HKD: -510.04; ending NAV: 200,311.33
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.845600
- Ending USD cash: $2,940.16

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| stock_short_without_hedge | 0.739 | -0.739 | 2955.270 | -2955.270 | 7 |
| total_stock_without_hedge | 0.739 | -0.739 | 2955.270 | -2955.270 | 7 |
| total_hedge | 2.510 | 2.510 | 10040.030 | 10040.030 | 1 |
| total_portfolio | 3.249 | 1.771 | 12995.300 | 7084.760 | 8 |

## Child-Order Mismatches

None

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
