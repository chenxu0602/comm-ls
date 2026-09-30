# IB Daily Reconciliation 2026-09-25

Sources:
- Activity statement: `ib_docs_crypto/2026-09-25/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-09-25/raw/pnls.csv`
- Targets: `targets-crypto/2026-09-25/targets.csv`

## Summary

- AUM basis: $3,000.00
- Fill rows: 1
- Open positions: 7
- Gross traded notional: $22.60 (0.75% of AUM)
- Commission: $-0.23 (100.29 bps of traded notional; 0.76 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $-40.33
- Daily security MTM after commission, HKD: 157.54
- Broker NAV change, HKD: 174.05; ending NAV: 197,922.71
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.844200
- Ending USD cash: $8,596.87

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.040 | 0.040 | 119.400 | 119.400 | 1 |
| stock_short_without_hedge | 0.178 | -0.178 | 534.500 | -534.500 | 5 |
| total_stock_without_hedge | 0.218 | -0.138 | 653.900 | -415.100 | 6 |
| total_hedge | 0.514 | 0.514 | 1542.700 | 1542.700 | 1 |
| total_portfolio | 0.732 | 0.376 | 2196.600 | 1127.600 | 7 |

## Child-Order Mismatches

| instrument | component | target_weight | actual_weight | expected_post_child_shares | actual_shares | share_diff_vs_child |
| --- | --- | --- | --- | --- | --- | --- |
| HIVE | btc_momentum_vol_carry|eth_momentum_vol_carry|hg_carry_and_power | -0.040 | -0.036 | -36.000 | -34.000 | 2.000 |

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
