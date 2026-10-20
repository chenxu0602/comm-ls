# IB Daily Reconciliation 2026-10-09

Sources:
- Activity statement: `ib_docs_crypto/2026-10-09/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-10-09/raw/pnls.csv`
- Targets: `targets-crypto/2026-10-09/targets.csv`

## Summary

- AUM basis: $3,000.00
- Fill rows: 3
- Open positions: 7
- Gross traded notional: $327.00 (10.90% of AUM)
- Commission: $-2.75 (84.06 bps of traded notional; 9.16 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $143.91
- Daily security MTM after commission, HKD: 181.53
- Broker NAV change, HKD: 177.57; ending NAV: 199,468.65
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.847800
- Ending USD cash: $8,398.95

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.073 | 0.073 | 218.040 | 218.040 | 1 |
| stock_short_without_hedge | 0.346 | -0.346 | 1036.800 | -1036.800 | 5 |
| total_stock_without_hedge | 0.418 | -0.273 | 1254.840 | -818.760 | 6 |
| total_hedge | 0.779 | 0.779 | 2335.710 | 2335.710 | 1 |
| total_portfolio | 1.197 | 0.506 | 3590.550 | 1516.950 | 7 |

## Child-Order Mismatches

| instrument | component | target_weight | actual_weight | expected_post_child_shares | actual_shares | share_diff_vs_child |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | hedge | 1.065 | 0.779 | 4.000 | 3.000 | -1.000 |
| HIVE | btc_momentum_vol_carry|eth_momentum_vol_carry|hg_carry_and_power | -0.055 | -0.046 | -64.000 | -55.000 | 9.000 |
| MARA | btc_momentum_vol_carry|eth_momentum_vol_carry|hg_carry_and_power | -0.075 | -0.055 | -23.000 | -17.000 | 6.000 |

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
