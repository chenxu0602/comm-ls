# Crypto v4.3 Daily Targets: 2026-09-02

- Signal as-of date: 2026-09-01
- Target trading date: 2026-09-02
- Separate-account AUM: $2,000.00
- Sleeve weights: Platforms 30%, BTC momentum/vol/carry 35%, ETH momentum 35%.
- Aggregate single-name cap: 12.00%
- Gross stock weight: 35.00%
- Net stock weight: -35.00%
- Continuous SPY hedge weight: 113.95%
- Total net weight after SPY hedge: 78.95%
- Full eligible turnover: 148.95%
- Today's executable turnover: 152.21%
- Estimated execution cost: $7.61

## Execution Notes

- This package belongs to the separate Crypto IB account; never net its SPY hedge with CL/Metals.
- Execute stocks first, then submit the single SPY hedge after confirmed stock fills.
- The SPY child in orders.csv follows post-child integer stock shares; the full continuous hedge remains in targets.csv.
- At $3,000 AUM one SPY share is roughly 25% NAV, so integer hedge rounding is material.
- This is SPY-only hedging. A BTC ETF hedge is not enabled or implied.

## Pinned Signal Inputs

- BTC: `data/cache/feature_return_observation_v1/BTC-multi_return_2.parquet`
- ETH: `data/cache/feature_return_observation_v1/ETH-multi_return_2.parquet`

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0 | 0 | 0 | 0 | 0 |
| stock_short_without_hedge | 0.35 | -0.35 | 700 | -700 | 6 |
| total_hedge | 1.13951 | 1.13951 | 2279.03 | 2279.03 | 1 |

## Targets

| instrument_type | component | instrument | research_target_weight | target_weight | target_shares | rounded_target_shares | previous_close | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | CLSK | -0.07 | -0.07 | -12.7 | -13 | 11.06 | BTC/ETH observation-date state; next-session target |
| stock | platforms\|btc_momentum_vol_carry\|eth_momentum_vol_carry | COIN | -0.07 | -0.07 | -0.8 | -1 | 176.82 | BTC/ETH observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | HIVE | -0.07 | -0.07 | -53 | -53 | 2.64 | BTC/ETH observation-date state; next-session target |
| stock | platforms | HOOD | 0 | 0 | 0 | 0 | 103.51 | BTC/ETH observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | MARA | -0.0525 | -0.0525 | -10.3 | -10 | 10.23 | BTC/ETH observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | MSTR | -0.0525 | -0.0525 | -0.8 | -1 | 124.88 | BTC/ETH observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | RIOT | -0.035 | -0.035 | -3.9 | -4 | 17.79 | BTC/ETH observation-date state; next-session target |
| hedge | hedge | SPY |  | 1.13951 | 3 | 3 | 761.78 | separate-account aggregate SPY beta hedge after confirmed stock fills |

## Orders

| instrument_type | component | instrument | execution_action | rounded_trade_shares | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | CLSK | SELL | -13 | 11.06 | 11.03 | 11.09 | execute once; no same-day reversal or duplicate order |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | HIVE | SELL | -53 | 2.64 | 2.63 | 2.65 | execute once; no same-day reversal or duplicate order |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | MARA | SELL | -10 | 10.23 | 10.2 | 10.26 | execute once; no same-day reversal or duplicate order |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | MSTR | SELL | -1 | 124.88 | 124.57 | 125.19 | execute once; no same-day reversal or duplicate order |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | RIOT | SELL | -4 | 17.79 | 17.75 | 17.83 | execute once; no same-day reversal or duplicate order |
| stock | platforms\|btc_momentum_vol_carry\|eth_momentum_vol_carry | COIN | SELL | -1 | 176.82 | 176.38 | 177.26 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | SPY | BUY | 3 | 761.78 | 759.88 | 763.68 | single aggregate hedge order after confirming stock fills |
