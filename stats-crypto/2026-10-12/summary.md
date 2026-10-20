# IB Daily Reconciliation 2026-10-12

Sources:
- Activity statement: `ib_docs_crypto/2026-10-12/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-10-12/raw/pnls.csv`
- Targets: `targets-crypto/2026-10-12/targets.csv`

## Summary

- AUM basis: $4,000.00
- Fill rows: 5
- Open positions: 6
- Gross traded notional: $410.20 (10.26% of AUM)
- Commission: $-3.49 (85.00 bps of traded notional; 8.72 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $165.51
- Daily security MTM after commission, HKD: 169.54
- Broker NAV change, HKD: 170.53; ending NAV: 199,639.18
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.847900
- Ending USD cash: $8,281.95

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.082 | 0.082 | 327.660 | 327.660 | 1 |
| stock_short_without_hedge | 0.252 | -0.252 | 1006.400 | -1006.400 | 4 |
| total_stock_without_hedge | 0.334 | -0.170 | 1334.060 | -678.740 | 5 |
| total_hedge | 0.584 | 0.584 | 2334.300 | 2334.300 | 1 |
| total_portfolio | 0.917 | 0.414 | 3668.360 | 1655.560 | 6 |

## Child-Order Mismatches

None

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
