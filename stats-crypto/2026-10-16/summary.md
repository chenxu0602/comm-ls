# IB Daily Reconciliation 2026-10-16

Sources:
- Activity statement: `ib_docs_crypto/2026-10-16/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-10-16/raw/pnls.csv`
- Targets: `targets-crypto/2026-10-16/targets.csv`

## Summary

- AUM basis: $4,000.00
- Fill rows: 2
- Open positions: 6
- Gross traded notional: $788.12 (19.70% of AUM)
- Commission: $-1.15 (14.61 bps of traded notional; 2.88 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $264.84
- Daily security MTM after commission, HKD: 428.17
- Broker NAV change, HKD: 435.17; ending NAV: 200,441.74
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.848000
- Ending USD cash: $7,615.89

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.074 | 0.074 | 296.610 | 296.610 | 1 |
| stock_short_without_hedge | 0.231 | -0.231 | 925.860 | -925.860 | 4 |
| total_stock_without_hedge | 0.306 | -0.157 | 1222.470 | -629.250 | 5 |
| total_hedge | 0.763 | 0.763 | 3053.000 | 3053.000 | 1 |
| total_portfolio | 1.069 | 0.606 | 4275.470 | 2423.750 | 6 |

## Child-Order Mismatches

| instrument | component | target_weight | actual_weight | expected_post_child_shares | actual_shares | share_diff_vs_child |
| --- | --- | --- | --- | --- | --- | --- |
| HIVE | btc_momentum_vol_carry|eth_momentum_vol_carry|hg_carry_and_power | -0.035 | -0.028 | -63.000 | -55.000 | 8.000 |

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
