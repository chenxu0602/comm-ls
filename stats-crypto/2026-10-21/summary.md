# IB Daily Reconciliation 2026-10-21

Sources:
- Activity statement: `ib_docs_crypto/2026-10-21/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-10-21/raw/pnls.csv`
- Targets: `targets-crypto/2026-10-21/targets.csv`

## Summary

- AUM basis: $4,000.00
- Fill rows: 4
- Open positions: 8
- Gross traded notional: $373.47 (9.34% of AUM)
- Commission: $-2.79 (74.67 bps of traded notional; 6.97 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $270.27
- Daily security MTM after commission, HKD: -403.25
- Broker NAV change, HKD: -419.34; ending NAV: 200,088.45
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.847100
- Ending USD cash: $4,491.64

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| stock_short_without_hedge | 0.750 | -0.750 | 3001.030 | -3001.030 | 7 |
| total_stock_without_hedge | 0.750 | -0.750 | 3001.030 | -3001.030 | 7 |
| total_hedge | 2.126 | 2.126 | 8503.990 | 8503.990 | 1 |
| total_portfolio | 2.876 | 1.376 | 11505.020 | 5502.960 | 8 |

## Child-Order Mismatches

| instrument | component | target_weight | actual_weight | expected_post_child_shares | actual_shares | share_diff_vs_child |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | hedge | 2.475 | 2.126 | 13.000 | 11.000 | -2.000 |

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
