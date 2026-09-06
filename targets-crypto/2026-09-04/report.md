# Crypto v4.3 Daily Targets: 2026-09-04

- Signal as-of date: 2026-09-03
- Target trading date: 2026-09-04
- Separate-account AUM: $2,000.00
- Sleeve weights: Platforms 30%, BTC momentum/vol/carry 35%, ETH momentum 35%.
- Aggregate single-name cap: 12.00%
- Gross stock weight: 35.00%
- Net stock weight: -35.00%
- Continuous SPY hedge weight: 116.74%
- Total net weight after SPY hedge: 81.74%
- Full eligible turnover: 2.91%
- Today's executable turnover: 3.33%
- Estimated execution cost: $0.17

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
| total_hedge | 1.16735 | 1.16735 | 2334.71 | 2334.71 | 1 |

## Targets

| instrument_type | component | instrument | research_target_weight | target_weight | target_shares | rounded_target_shares | previous_close | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | CLSK | -0.07 | -0.07 | -11.1 | -11 | 12.58 | BTC/ETH observation-date state; next-session target |
| stock | platforms\|btc_momentum_vol_carry\|eth_momentum_vol_carry | COIN | -0.07 | -0.07 | -0.7 | -1 | 192.7 | BTC/ETH observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | HIVE | -0.07 | -0.07 | -45.9 | -46 | 3.05 | BTC/ETH observation-date state; next-session target |
| stock | platforms | HOOD | 0 | 0 | 0 | 0 | 124.72 | BTC/ETH observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | MARA | -0.0525 | -0.0525 | -9.1 | -9 | 11.6 | BTC/ETH observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | MSTR | -0.0525 | -0.0525 | -0.7 | -1 | 144.82 | BTC/ETH observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | RIOT | -0.035 | -0.035 | -3.3 | -3 | 21.14 | BTC/ETH observation-date state; next-session target |
| hedge | hedge | SPY |  | 1.16735 | 3 | 3 | 773.17 | separate-account aggregate SPY beta hedge after confirmed stock fills |

## Orders

| instrument_type | component | instrument | execution_action | rounded_trade_shares | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | CLSK | BUY | 1 | 12.58 | 12.55 | 12.61 | execute once; no same-day reversal or duplicate order |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | HIVE | BUY | 7 | 3.05 | 3.04 | 3.06 | execute once; no same-day reversal or duplicate order |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | MARA | BUY | 1 | 11.6 | 11.57 | 11.63 | execute once; no same-day reversal or duplicate order |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | RIOT | BUY | 1 | 21.14 | 21.09 | 21.19 | execute once; no same-day reversal or duplicate order |
