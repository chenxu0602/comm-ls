# IB Daily Reconciliation 2026-11-16

Sources:
- Activity statement: `ib_docs_crypto/2026-11-16/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-11-16/raw/pnls.csv`
- Targets: `targets-crypto/2026-11-16/targets.csv`

## Summary

- AUM basis: $4,000.00
- Fill rows: 0
- Open positions: 7
- Gross traded notional: $0.00 (0.00% of AUM)
- Commission: $0.00 (nan bps of traded notional; -0.00 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $6.69
- Daily security MTM after commission, HKD: -211.93
- Broker NAV change, HKD: -206.86; ending NAV: 200,927.93
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.846200
- Ending USD cash: $5,166.75

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| stock_short_without_hedge | 0.429 | -0.429 | 1717.860 | -1717.860 | 6 |
| total_stock_without_hedge | 0.429 | -0.429 | 1717.860 | -1717.860 | 6 |
| total_hedge | 1.665 | 1.665 | 6659.550 | 6659.550 | 1 |
| total_portfolio | 2.094 | 1.235 | 8377.410 | 4941.690 | 7 |

## Child-Order Mismatches

| instrument | component | target_weight | actual_weight | expected_post_child_shares | actual_shares | share_diff_vs_child |
| --- | --- | --- | --- | --- | --- | --- |
| MSTR | btc_momentum_vol_carry|eth_momentum_vol_carry | -0.075 | -0.052 | -3.000 | -2.000 | 1.000 |
| CLSK | btc_momentum_vol_carry|eth_momentum_vol_carry|hg_carry_and_power | -0.100 | -0.091 | -60.000 | -58.000 | 2.000 |
| HIVE | btc_momentum_vol_carry|eth_momentum_vol_carry|hg_carry_and_power | -0.085 | -0.072 | -217.000 | -198.000 | 19.000 |
| MARA | btc_momentum_vol_carry|eth_momentum_vol_carry|hg_carry_and_power | -0.075 | -0.065 | -43.000 | -39.000 | 4.000 |
| RIOT | btc_momentum_vol_carry|eth_momentum_vol_carry|hg_carry_and_power | -0.065 | -0.060 | -15.000 | -14.000 | 1.000 |

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
