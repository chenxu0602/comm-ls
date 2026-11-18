# IB Daily Reconciliation 2026-10-23

Sources:
- Activity statement: `ib_docs_crypto/2026-10-23/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-10-23/raw/pnls.csv`
- Targets: `targets-crypto/2026-10-23/targets.csv`

## Summary

- AUM basis: $4,000.00
- Fill rows: 3
- Open positions: 8
- Gross traded notional: $65.20 (1.63% of AUM)
- Commission: $-0.65 (100.21 bps of traded notional; 1.63 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $102.34
- Daily security MTM after commission, HKD: 81.53
- Broker NAV change, HKD: 139.90; ending NAV: 200,608.75
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.842400
- Ending USD cash: $5,143.86

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| stock_short_without_hedge | 0.479 | -0.479 | 1916.650 | -1916.650 | 7 |
| total_stock_without_hedge | 0.479 | -0.479 | 1916.650 | -1916.650 | 7 |
| total_hedge | 1.710 | 1.710 | 6839.730 | 6839.730 | 1 |
| total_portfolio | 2.189 | 1.231 | 8756.380 | 4923.080 | 8 |

## Child-Order Mismatches

| instrument | component | target_weight | actual_weight | expected_post_child_shares | actual_shares | share_diff_vs_child |
| --- | --- | --- | --- | --- | --- | --- |
| HIVE | btc_momentum_vol_carry|eth_momentum_vol_carry|hg_carry_and_power | -0.070 | -0.066 | -144.000 | -137.000 | 7.000 |

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
