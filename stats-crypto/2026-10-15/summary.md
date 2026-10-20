# IB Daily Reconciliation 2026-10-15

Sources:
- Activity statement: `ib_docs_crypto/2026-10-15/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-10-15/raw/pnls.csv`
- Targets: `targets-crypto/2026-10-15/targets.csv`

## Summary

- AUM basis: $4,000.00
- Fill rows: 3
- Open positions: 6
- Gross traded notional: $124.30 (3.11% of AUM)
- Commission: $-1.25 (100.21 bps of traded notional; 3.11 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $210.28
- Daily security MTM after commission, HKD: -10.72
- Broker NAV change, HKD: -21.71; ending NAV: 200,006.57
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.847300
- Ending USD cash: $8,405.16

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.078 | 0.078 | 311.970 | 311.970 | 1 |
| stock_short_without_hedge | 0.262 | -0.262 | 1047.420 | -1047.420 | 4 |
| total_stock_without_hedge | 0.340 | -0.184 | 1359.390 | -735.450 | 5 |
| total_hedge | 0.579 | 0.579 | 2315.370 | 2315.370 | 1 |
| total_portfolio | 0.919 | 0.395 | 3674.760 | 1579.920 | 6 |

## Child-Order Mismatches

| instrument | component | target_weight | actual_weight | expected_post_child_shares | actual_shares | share_diff_vs_child |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | hedge | 0.760 | 0.579 | 4.000 | 3.000 | -1.000 |
| HIVE | btc_momentum_vol_carry|eth_momentum_vol_carry|hg_carry_and_power | -0.035 | -0.031 | -62.000 | -55.000 | 7.000 |

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
