# IB Daily Reconciliation 2026-11-05

Sources:
- Activity statement: `ib_docs_crypto/2026-11-05/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-11-05/raw/pnls.csv`
- Targets: `targets-crypto/2026-11-05/targets.csv`

## Summary

- AUM basis: $4,000.00
- Fill rows: 3
- Open positions: 7
- Gross traded notional: $2,657.50 (66.44% of AUM)
- Commission: $-2.76 (10.38 bps of traded notional; 6.90 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $-218.27
- Daily security MTM after commission, HKD: -1,260.80
- Broker NAV change, HKD: -1,303.50; ending NAV: 200,075.64
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.841300
- Ending USD cash: $4,556.66

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| stock_short_without_hedge | 0.287 | -0.287 | 1147.600 | -1147.600 | 6 |
| total_stock_without_hedge | 0.287 | -0.287 | 1147.600 | -1147.600 | 6 |
| total_hedge | 1.649 | 1.649 | 6597.000 | 6597.000 | 1 |
| total_portfolio | 1.936 | 1.362 | 7744.600 | 5449.400 | 7 |

## Child-Order Mismatches

| instrument | component | target_weight | actual_weight | expected_post_child_shares | actual_shares | share_diff_vs_child |
| --- | --- | --- | --- | --- | --- | --- |
| MSTR | btc_momentum_vol_carry|eth_momentum_vol_carry | -0.075 | -0.032 | -2.000 | -1.000 | 1.000 |
| CLSK | btc_momentum_vol_carry|eth_momentum_vol_carry|hg_carry_and_power | -0.100 | -0.028 | -59.000 | -20.000 | 39.000 |
| HIVE | btc_momentum_vol_carry|eth_momentum_vol_carry|hg_carry_and_power | -0.085 | -0.036 | -187.000 | -88.000 | 99.000 |
| MARA | btc_momentum_vol_carry|eth_momentum_vol_carry|hg_carry_and_power | -0.075 | -0.025 | -44.000 | -17.000 | 27.000 |

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
