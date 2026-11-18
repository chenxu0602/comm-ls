# IB Daily Reconciliation 2026-11-04

Sources:
- Activity statement: `ib_docs_crypto/2026-11-04/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-11-04/raw/pnls.csv`
- Targets: `targets-crypto/2026-11-04/targets.csv`

## Summary

- AUM basis: $4,000.00
- Fill rows: 6
- Open positions: 7
- Gross traded notional: $3,369.81 (84.25% of AUM)
- Commission: $-6.05 (17.95 bps of traded notional; 15.12 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $40.54
- Daily security MTM after commission, HKD: 1,133.06
- Broker NAV change, HKD: 1,120.04; ending NAV: 201,379.14
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.845500
- Ending USD cash: $6,611.12

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| stock_short_without_hedge | 0.261 | -0.261 | 1045.130 | -1045.130 | 6 |
| total_stock_without_hedge | 0.261 | -0.261 | 1045.130 | -1045.130 | 6 |
| total_hedge | 1.150 | 1.150 | 4600.860 | 4600.860 | 1 |
| total_portfolio | 1.411 | 0.889 | 5645.990 | 3555.730 | 7 |

## Child-Order Mismatches

| instrument | component | target_weight | actual_weight | expected_post_child_shares | actual_shares | share_diff_vs_child |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | hedge | 0.688 | 1.150 | 4.000 | 6.000 | 2.000 |
| RIOT | btc_momentum_vol_carry|eth_momentum_vol_carry|hg_carry_and_power | -0.020 | -0.085 | -6.000 | -22.000 | -16.000 |

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
