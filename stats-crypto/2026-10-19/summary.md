# IB Daily Reconciliation 2026-10-19

Sources:
- Activity statement: `ib_docs_crypto/2026-10-19/raw/activity_statement.csv`
- PnL/NAV statement: `ib_docs_crypto/2026-10-19/raw/pnls.csv`
- Targets: `targets-crypto/2026-10-19/targets.csv`

## Summary

- AUM basis: $4,000.00
- Fill rows: 6
- Open positions: 7
- Gross traded notional: $1,302.52 (32.56% of AUM)
- Commission: $-5.69 (43.72 bps of traded notional; 14.24 bps of AUM)
- Cumulative realized plus open unrealized PnL, USD: $276.39
- Daily security MTM after commission, HKD: 123.34
- Broker NAV change, HKD: 135.52; ending NAV: 200,577.26
- MTM source convention: `base`; normalization factor: 1.000000; USD/HKD: 7.848300
- Ending USD cash: $7,377.12

## Actual Exposure

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.072 | 0.072 | 289.560 | 289.560 | 1 |
| stock_short_without_hedge | 0.361 | -0.361 | 1443.720 | -1443.720 | 5 |
| total_stock_without_hedge | 0.433 | -0.289 | 1733.280 | -1154.160 | 6 |
| total_hedge | 0.958 | 0.958 | 3832.400 | 3832.400 | 1 |
| total_portfolio | 1.391 | 0.670 | 5565.680 | 2678.240 | 7 |

## Child-Order Mismatches

| instrument | component | target_weight | actual_weight | expected_post_child_shares | actual_shares | share_diff_vs_child |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | hedge | 1.120 | 0.958 | 6.000 | 5.000 | -1.000 |

## Avoidable Same-Day Round Trips

None

## Notes

- Borrow fee rates are not available from this statement. Add IB review / borrow snapshot later for hard-to-borrow monitoring.
- Cumulative PnL is since each position's cost basis; daily MTM is the report-date broker-book result. Neither is research alpha attribution.
- The MTM parser verifies sign and units against prior shares times close-to-close price changes. Unrecognized conventions fail closed.
