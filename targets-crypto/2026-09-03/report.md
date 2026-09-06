# Crypto v4.3 Daily Targets: 2026-09-03

- Signal as-of date: 2026-09-02
- Target trading date: 2026-09-03
- Separate-account AUM: $2,000.00
- Sleeve weights: Platforms 30%, BTC momentum/vol/carry 35%, ETH momentum 35%.
- Aggregate single-name cap: 12.00%
- Gross stock weight: 35.00%
- Net stock weight: -35.00%
- Continuous SPY hedge weight: 114.63%
- Total net weight after SPY hedge: 79.63%
- Full eligible turnover: 0.36%
- Today's executable turnover: 0.57%
- Estimated execution cost: $0.03

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
| total_hedge | 1.14631 | 1.14631 | 2292.63 | 2292.63 | 1 |

## Targets

| instrument_type | component | instrument | research_target_weight | target_weight | target_shares | rounded_target_shares | previous_close | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | CLSK | -0.07 | -0.07 | -12.4 | -12 | 11.33 | BTC/ETH observation-date state; next-session target |
| stock | platforms\|btc_momentum_vol_carry\|eth_momentum_vol_carry | COIN | -0.07 | -0.07 | -0.8 | -1 | 174.96 | BTC/ETH observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | HIVE | -0.07 | -0.07 | -51.5 | -51 | 2.72 | BTC/ETH observation-date state; next-session target |
| stock | platforms | HOOD | 0 | 0 | 0 | 0 | 106.99 | BTC/ETH observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | MARA | -0.0525 | -0.0525 | -10 | -10 | 10.47 | BTC/ETH observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | MSTR | -0.0525 | -0.0525 | -0.9 | -1 | 123.19 | BTC/ETH observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | RIOT | -0.035 | -0.035 | -3.8 | -4 | 18.64 | BTC/ETH observation-date state; next-session target |
| hedge | hedge | SPY |  | 1.14631 | 3 | 3 | 765.16 | separate-account aggregate SPY beta hedge after confirmed stock fills |

## Orders

| instrument_type | component | instrument | execution_action | rounded_trade_shares | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | CLSK | BUY | 1 | 11.33 | 11.3 | 11.36 | execute once; no same-day reversal or duplicate order |
