# IB Daily Reconciliation 2026-09-08

Sources:
- Activity statement: `ib_docs_crypto/2026-09-08/raw/activity_statement.csv`
- Targets: `targets-crypto/2026-09-08/targets.csv`

## Summary

- AUM basis: $3,000.00
- Fill rows: 2
- Open positions: 7
- Gross traded notional: $36.30 (1.21% of AUM)
- Commission: $-0.36 (100.42 bps of traded notional; 1.22 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $-87.74
- Daily MTM PnL after commission, base currency: -118.99
- Ending USD cash: $8,348.07

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| stock_short_without_hedge | 0.248 | -0.248 | 743.100 | -743.100 | 6 |
| total_stock_without_hedge | 0.248 | -0.248 | 743.100 | -743.100 | 6 |
| total_hedge | 0.766 | 0.766 | 2297.880 | 2297.880 | 1 |
| total_portfolio | 1.014 | 0.518 | 3040.980 | 1554.780 | 7 |

## Child-Order Mismatches

| instrument | component | target_weight | actual_weight | expected_post_child_shares | actual_shares | share_diff_vs_child |
| --- | --- | --- | --- | --- | --- | --- |
| HIVE | btc_momentum_vol_carry|eth_momentum_vol_carry|hg_carry_and_power | -0.040 | -0.048 | -39.000 | -46.000 | -7.000 |

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
