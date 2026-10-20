# IB Daily Reconciliation 2026-10-13

Sources:
- Activity statement: `ib_docs_crypto/2026-10-13/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-10-13/raw/pnls.csv`
- Targets: `targets-crypto/2026-10-13/targets.csv`

## Summary

- AUM basis: $4,000.00
- Fill rows: 1
- Open positions: 6
- Gross traded notional: $16.50 (0.41% of AUM)
- Commission: $-0.17 (100.21 bps of traded notional; 0.41 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $182.60
- Daily security MTM after commission, HKD: 107.48
- Broker NAV change, HKD: 109.47; ending NAV: 199,748.65
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.848100
- Ending USD cash: $8,298.28

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.083 | 0.083 | 331.560 | 331.560 | 1 |
| stock_short_without_hedge | 0.253 | -0.253 | 1012.670 | -1012.670 | 4 |
| total_stock_without_hedge | 0.336 | -0.170 | 1344.230 | -681.110 | 5 |
| total_hedge | 0.584 | 0.584 | 2334.030 | 2334.030 | 1 |
| total_portfolio | 0.920 | 0.413 | 3678.260 | 1652.920 | 6 |

## Child-Order Mismatches

| instrument | component | target_weight | actual_weight | expected_post_child_shares | actual_shares | share_diff_vs_child |
| --- | --- | --- | --- | --- | --- | --- |
| CLSK | btc_momentum_vol_carry|eth_momentum_vol_carry|hg_carry_and_power | -0.080 | -0.076 | -31.000 | -30.000 | 1.000 |

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
