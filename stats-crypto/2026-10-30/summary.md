# IB Daily Reconciliation 2026-10-30

Sources:
- Activity statement: `ib_docs_crypto/2026-10-30/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-10-30/raw/pnls.csv`
- Targets: `targets-crypto/2026-10-30/targets.csv`

## Summary

- AUM basis: $4,000.00
- Fill rows: 1
- Open positions: 8
- Gross traded notional: $26.00 (0.65% of AUM)
- Commission: $-0.26 (100.21 bps of traded notional; 0.65 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $90.95
- Daily security MTM after commission, HKD: 288.29
- Broker NAV change, HKD: 225.35; ending NAV: 200,886.82
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.844800
- Ending USD cash: $2,875.57

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.000 | 0.000 | 0.000 | 0.000 | 0 |
| stock_short_without_hedge | 0.649 | -0.649 | 2594.010 | -2594.010 | 7 |
| total_stock_without_hedge | 0.649 | -0.649 | 2594.010 | -2594.010 | 7 |
| total_hedge | 2.456 | 2.456 | 9824.360 | 9824.360 | 1 |
| total_portfolio | 3.105 | 1.808 | 12418.370 | 7230.350 | 8 |

## Child-Order Mismatches

| instrument | component | target_weight | actual_weight | expected_post_child_shares | actual_shares | share_diff_vs_child |
| --- | --- | --- | --- | --- | --- | --- |
| CLSK | btc_momentum_vol_carry|eth_momentum_vol_carry|hg_carry_and_power | -0.120 | -0.107 | -59.000 | -56.000 | 3.000 |
| HIVE | btc_momentum_vol_carry|eth_momentum_vol_carry|hg_carry_and_power | -0.115 | -0.104 | -222.000 | -217.000 | 5.000 |
| MARA | btc_momentum_vol_carry|eth_momentum_vol_carry|hg_carry_and_power | -0.120 | -0.110 | -67.000 | -65.000 | 2.000 |

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
