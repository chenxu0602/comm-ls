# IB Daily Reconciliation 2026-10-14

Sources:
- Activity statement: `ib_docs_crypto/2026-10-14/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-10-14/raw/pnls.csv`
- Targets: `targets-crypto/2026-10-14/targets.csv`

## Summary

- AUM basis: $4,000.00
- Fill rows: 1
- Open positions: 6
- Gross traded notional: $16.01 (0.40% of AUM)
- Commission: $-0.16 (100.94 bps of traded notional; 0.40 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $217.85
- Daily security MTM after commission, HKD: 276.64
- Broker NAV change, HKD: 279.63; ending NAV: 200,028.28
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.848400
- Ending USD cash: $8,282.11

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.076 | 0.076 | 303.240 | 303.240 | 1 |
| stock_short_without_hedge | 0.227 | -0.227 | 907.700 | -907.700 | 4 |
| total_stock_without_hedge | 0.303 | -0.151 | 1210.940 | -604.460 | 5 |
| total_hedge | 0.577 | 0.577 | 2308.800 | 2308.800 | 1 |
| total_portfolio | 0.880 | 0.426 | 3519.740 | 1704.340 | 6 |

## Child-Order Mismatches

| instrument | component | target_weight | actual_weight | expected_post_child_shares | actual_shares | share_diff_vs_child |
| --- | --- | --- | --- | --- | --- | --- |
| CLSK | btc_momentum_vol_carry|eth_momentum_vol_carry|hg_carry_and_power | -0.080 | -0.069 | -32.000 | -30.000 | 2.000 |
| MARA | btc_momentum_vol_carry|eth_momentum_vol_carry|hg_carry_and_power | -0.060 | -0.051 | -26.000 | -25.000 | 1.000 |

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
