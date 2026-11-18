# IB Daily Reconciliation 2026-11-11

Sources:
- Activity statement: `ib_docs_crypto/2026-11-11/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-11-11/raw/pnls.csv`
- Targets: `targets-crypto/2026-11-11/targets.csv`

## Summary

- AUM basis: $4,000.00
- Fill rows: 3
- Open positions: 7
- Gross traded notional: $57.35 (1.43% of AUM)
- Commission: $-0.57 (100.15 bps of traded notional; 1.44 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $-70.73
- Daily security MTM after commission, HKD: 174.20
- Broker NAV change, HKD: 169.19; ending NAV: 200,403.02
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.844900
- Ending USD cash: $5,986.86

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| stock_short_without_hedge | 0.506 | -0.506 | 2022.140 | -2022.140 | 6 |
| total_stock_without_hedge | 0.506 | -0.506 | 2022.140 | -2022.140 | 6 |
| total_hedge | 1.520 | 1.520 | 6078.480 | 6078.480 | 1 |
| total_portfolio | 2.025 | 1.014 | 8100.620 | 4056.340 | 7 |

## Child-Order Mismatches

| instrument | component | target_weight | actual_weight | expected_post_child_shares | actual_shares | share_diff_vs_child |
| --- | --- | --- | --- | --- | --- | --- |
| MARA | btc_momentum_vol_carry|eth_momentum_vol_carry|hg_carry_and_power | -0.075 | -0.086 | -41.000 | -45.000 | -4.000 |

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
