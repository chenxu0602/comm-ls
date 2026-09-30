# IB Daily Reconciliation 2026-09-15

Sources:
- Activity statement: `ib_docs_crypto/2026-09-15/raw/activity_statement.csv`
- Targets: `targets-crypto/2026-09-15/targets.csv`

## Summary

- AUM basis: $3,000.00
- Fill rows: 6
- Open positions: 7
- Gross traded notional: $793.37 (26.45% of AUM)
- Commission: $-6.00 (75.66 bps of traded notional; 20.01 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $-79.44
- Daily MTM PnL after commission, base currency: 61.17
- Ending USD cash: $7,152.27

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.074 | 0.074 | 220.900 | 220.900 | 1 |
| stock_short_without_hedge | 0.169 | -0.169 | 507.800 | -507.800 | 5 |
| total_stock_without_hedge | 0.243 | -0.096 | 728.700 | -286.900 | 6 |
| total_hedge | 1.010 | 1.010 | 3029.560 | 3029.560 | 1 |
| total_portfolio | 1.253 | 0.914 | 3758.260 | 2742.660 | 7 |

## Child-Order Mismatches

| instrument | component | target_weight | actual_weight | expected_post_child_shares | actual_shares | share_diff_vs_child |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | hedge | 0.364 | 1.010 | 1.000 | 4.000 | 3.000 |

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
