# IB Daily Reconciliation 2026-09-22

Sources:
- Activity statement: `ib_docs_crypto/2026-09-22/raw/activity_statement.csv`
- Targets: `targets-crypto/2026-09-22/targets.csv`

## Summary

- AUM basis: $3,000.00
- Fill rows: 5
- Open positions: 7
- Gross traded notional: $783.86 (26.13% of AUM)
- Commission: $-5.00 (63.82 bps of traded notional; 16.68 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $-154.81
- Daily MTM PnL after commission, base currency: -41.75
- Ending USD cash: $6,410.65

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.041 | 0.041 | 124.250 | 124.250 | 1 |
| stock_short_without_hedge | 0.233 | -0.233 | 699.220 | -699.220 | 5 |
| total_stock_without_hedge | 0.274 | -0.192 | 823.470 | -574.970 | 6 |
| total_hedge | 1.289 | 1.289 | 3866.900 | 3866.900 | 1 |
| total_portfolio | 1.563 | 1.097 | 4690.370 | 3291.930 | 7 |

## Child-Order Mismatches

| instrument | component | target_weight | actual_weight | expected_post_child_shares | actual_shares | share_diff_vs_child |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | hedge | 0.363 | 1.289 | 2.000 | 5.000 | 3.000 |
| HIVE | btc_momentum_vol_carry|eth_momentum_vol_carry|hg_carry_and_power | -0.040 | -0.088 | -34.000 | -75.000 | -41.000 |

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
