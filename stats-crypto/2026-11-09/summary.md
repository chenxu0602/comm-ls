# IB Daily Reconciliation 2026-11-09

Sources:
- Activity statement: `ib_docs_crypto/2026-11-09/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-11-09/raw/pnls.csv`
- Targets: `targets-crypto/2026-11-09/targets.csv`

## Summary

- AUM basis: $4,000.00
- Fill rows: 2
- Open positions: 8
- Gross traded notional: $45.00 (1.12% of AUM)
- Commission: $-0.45 (100.01 bps of traded notional; 1.13 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $-82.53
- Daily security MTM after commission, HKD: 404.10
- Broker NAV change, HKD: 427.04; ending NAV: 200,237.40
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.842000
- Ending USD cash: $6,950.54

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.021 | 0.021 | 83.320 | 83.320 | 1 |
| stock_short_without_hedge | 0.381 | -0.381 | 1524.200 | -1524.200 | 6 |
| total_stock_without_hedge | 0.402 | -0.360 | 1607.520 | -1440.880 | 7 |
| total_hedge | 1.129 | 1.129 | 4516.140 | 4516.140 | 1 |
| total_portfolio | 1.531 | 0.769 | 6123.660 | 3075.260 | 8 |

## Child-Order Mismatches

| instrument | component | target_weight | actual_weight | expected_post_child_shares | actual_shares | share_diff_vs_child |
| --- | --- | --- | --- | --- | --- | --- |
| CLSK | btc_momentum_vol_carry|eth_momentum_vol_carry|hg_carry_and_power | -0.070 | -0.085 | -45.000 | -49.000 | -4.000 |
| RIOT | btc_momentum_vol_carry|eth_momentum_vol_carry|hg_carry_and_power | -0.035 | -0.040 | -8.000 | -9.000 | -1.000 |

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
