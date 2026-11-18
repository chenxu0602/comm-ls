# IB Daily Reconciliation 2026-10-26

Sources:
- Activity statement: `ib_docs_crypto/2026-10-26/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-10-26/raw/pnls.csv`
- Targets: `targets-crypto/2026-10-26/targets.csv`

## Summary

- AUM basis: $4,000.00
- Fill rows: 1
- Open positions: 8
- Gross traded notional: $15.80 (0.40% of AUM)
- Commission: $-0.16 (100.21 bps of traded notional; 0.40 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $186.77
- Daily security MTM after commission, HKD: 662.41
- Broker NAV change, HKD: 693.64; ending NAV: 201,302.39
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.845500
- Ending USD cash: $5,159.50

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| stock_short_without_hedge | 0.474 | -0.474 | 1896.460 | -1896.460 | 7 |
| total_stock_without_hedge | 0.474 | -0.474 | 1896.460 | -1896.460 | 7 |
| total_hedge | 1.722 | 1.722 | 6888.330 | 6888.330 | 1 |
| total_portfolio | 2.196 | 1.248 | 8784.790 | 4991.870 | 8 |

## Child-Order Mismatches

| instrument | component | target_weight | actual_weight | expected_post_child_shares | actual_shares | share_diff_vs_child |
| --- | --- | --- | --- | --- | --- | --- |
| HIVE | btc_momentum_vol_carry|eth_momentum_vol_carry|hg_carry_and_power | -0.070 | -0.065 | -145.000 | -137.000 | 8.000 |
| MARA | btc_momentum_vol_carry|eth_momentum_vol_carry|hg_carry_and_power | -0.075 | -0.070 | -43.000 | -41.000 | 2.000 |

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
