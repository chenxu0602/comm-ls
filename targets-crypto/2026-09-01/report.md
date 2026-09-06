# Crypto v4.3 Daily Targets: 2026-09-01

- Signal as-of date: 2026-08-31
- Target trading date: 2026-09-01
- Separate-account AUM: $2,000.00
- Sleeve weights: Platforms 30%, BTC momentum/vol/carry 35%, ETH momentum 35%.
- Aggregate single-name cap: 12.00%
- Gross stock weight: 49.00%
- Net stock weight: -49.00%
- Continuous SPY hedge weight: 155.14%
- Total net weight after SPY hedge: 106.14%
- Full eligible turnover: 204.14%
- Today's executable turnover: 155.02%
- Estimated execution cost: $7.75

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
| stock_short_without_hedge | 0.49 | -0.49 | 980 | -980 | 7 |
| total_hedge | 1.55143 | 1.55143 | 3102.86 | 3102.86 | 1 |

## Targets

| instrument_type | component | instrument | research_target_weight | target_weight | target_shares | rounded_target_shares | previous_close | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | CLSK | -0.07 | -0.07 | -12 | -12 | 11.62 | BTC/ETH observation-date state; next-session target |
| stock | platforms\|btc_momentum_vol_carry\|eth_momentum_vol_carry | COIN | -0.13 | -0.12 | -1.3 | -1 | 188.12 | BTC/ETH observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | HIVE | -0.07 | -0.07 | -50.4 | -50 | 2.78 | BTC/ETH observation-date state; next-session target |
| stock | platforms | HOOD | -0.09 | -0.09 | -1.7 | -2 | 104.81 | BTC/ETH observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | MARA | -0.0525 | -0.0525 | -9.7 | -10 | 10.77 | BTC/ETH observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | MSTR | -0.0525 | -0.0525 | -0.8 | -1 | 132.94 | BTC/ETH observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | RIOT | -0.035 | -0.035 | -3.7 | -4 | 19 | BTC/ETH observation-date state; next-session target |
| hedge | hedge | SPY |  | 1.55143 | 4 | 4 | 767.05 | separate-account aggregate SPY beta hedge after confirmed stock fills |

## Orders

| instrument_type | component | instrument | execution_action | rounded_trade_shares | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | CLSK | SELL | -10 | 11.62 | 11.59 | 11.65 | execute once; no same-day reversal or duplicate order |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | HIVE | SELL | -41 | 2.78 | 2.77 | 2.79 | execute once; no same-day reversal or duplicate order |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | MARA | SELL | -8 | 10.77 | 10.74 | 10.8 | execute once; no same-day reversal or duplicate order |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | MSTR | SELL | -1 | 132.94 | 132.61 | 133.27 | execute once; no same-day reversal or duplicate order |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | RIOT | SELL | -3 | 19 | 18.95 | 19.04 | execute once; no same-day reversal or duplicate order |
| stock | platforms | HOOD | SELL | -1 | 104.81 | 104.55 | 105.07 | execute once; no same-day reversal or duplicate order |
| stock | platforms\|btc_momentum_vol_carry\|eth_momentum_vol_carry | COIN | SELL | -1 | 188.12 | 187.65 | 188.59 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | SPY | BUY | 3 | 767.05 | 765.13 | 768.97 | single aggregate hedge order after confirming stock fills |
