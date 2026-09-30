# IB Daily Reconciliation 2026-09-16

Sources:
- Activity statement: `ib_docs_crypto/2026-09-16/raw/activity_statement.csv`
- Targets: `targets-crypto/2026-09-16/targets.csv`

## Summary

- AUM basis: $3,000.00
- Fill rows: 5
- Open positions: 7
- Gross traded notional: $1,368.64 (45.62% of AUM)
- Commission: $-5.03 (36.74 bps of traded notional; 16.76 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $-50.53
- Daily MTM PnL after commission, base currency: -247.89
- Ending USD cash: $6,996.89

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.070 | 0.070 | 208.840 | 208.840 | 1 |
| stock_short_without_hedge | 0.371 | -0.371 | 1112.640 | -1112.640 | 5 |
| total_stock_without_hedge | 0.440 | -0.301 | 1321.480 | -903.800 | 6 |
| total_hedge | 1.257 | 1.257 | 3770.250 | 3770.250 | 1 |
| total_portfolio | 1.697 | 0.955 | 5091.730 | 2866.450 | 7 |

## Child-Order Mismatches

| instrument | component | target_weight | actual_weight | expected_post_child_shares | actual_shares | share_diff_vs_child |
| --- | --- | --- | --- | --- | --- | --- |
| MSTR | btc_momentum_vol_carry|eth_momentum_vol_carry | -0.075 | -0.042 | -2.000 | -1.000 | 1.000 |
| COIN | platforms|btc_momentum_vol_carry|eth_momentum_vol_carry|hg_carry_and_power | -0.060 | 0.000 | -1.000 | 0.000 | 1.000 |

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
