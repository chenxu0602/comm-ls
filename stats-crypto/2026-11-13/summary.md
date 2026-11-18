# IB Daily Reconciliation 2026-11-13

Sources:
- Activity statement: `ib_docs_crypto/2026-11-13/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-11-13/raw/pnls.csv`
- Targets: `targets-crypto/2026-11-13/targets.csv`

## Summary

- AUM basis: $4,000.00
- Fill rows: 1
- Open positions: 7
- Gross traded notional: $752.00 (18.80% of AUM)
- Commission: $-1.00 (13.30 bps of traded notional; 2.50 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $33.70
- Daily security MTM after commission, HKD: 262.12
- Broker NAV change, HKD: 271.22; ending NAV: 201,134.79
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.845700
- Ending USD cash: $5,166.75

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| stock_short_without_hedge | 0.455 | -0.455 | 1820.630 | -1820.630 | 6 |
| total_stock_without_hedge | 0.455 | -0.455 | 1820.630 | -1820.630 | 6 |
| total_hedge | 1.697 | 1.697 | 6789.330 | 6789.330 | 1 |
| total_portfolio | 2.152 | 1.242 | 8609.960 | 4968.700 | 7 |

## Child-Order Mismatches

| instrument | component | target_weight | actual_weight | expected_post_child_shares | actual_shares | share_diff_vs_child |
| --- | --- | --- | --- | --- | --- | --- |
| MSTR | btc_momentum_vol_carry|eth_momentum_vol_carry | -0.075 | -0.056 | -3.000 | -2.000 | 1.000 |
| HIVE | btc_momentum_vol_carry|eth_momentum_vol_carry|hg_carry_and_power | -0.085 | -0.078 | -206.000 | -198.000 | 8.000 |
| MARA | btc_momentum_vol_carry|eth_momentum_vol_carry|hg_carry_and_power | -0.075 | -0.068 | -42.000 | -39.000 | 3.000 |
| RIOT | btc_momentum_vol_carry|eth_momentum_vol_carry|hg_carry_and_power | -0.065 | -0.061 | -15.000 | -14.000 | 1.000 |

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
