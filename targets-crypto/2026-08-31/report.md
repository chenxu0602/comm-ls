# Crypto v4.3 Daily Targets: 2026-08-31

- Signal as-of date: 2026-08-28
- Target trading date: 2026-08-31
- Separate-account AUM: $2,000.00
- Sleeve weights: Platforms 30%, BTC momentum/vol/carry 35%, ETH momentum 35%.
- Aggregate single-name cap: 12.00%
- Gross stock weight: 49.00%
- Net stock weight: -49.00%
- Continuous SPY hedge weight: 154.79%
- Total net weight after SPY hedge: 105.79%
- Full eligible turnover: 203.79%
- Today's executable turnover: 155.61%
- Estimated execution cost: $7.78

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
| total_hedge | 1.54786 | 1.54786 | 3095.72 | 3095.72 | 1 |

## Targets

| instrument_type | component | instrument | research_target_weight | target_weight | target_shares | rounded_target_shares | previous_close | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | CLSK | -0.07 | -0.07 | -11.4 | -11 | 12.25 | BTC/ETH observation-date state; next-session target |
| stock | platforms\|btc_momentum_vol_carry\|eth_momentum_vol_carry | COIN | -0.13 | -0.12 | -1.3 | -1 | 183.73 | BTC/ETH observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | HIVE | -0.07 | -0.07 | -48.2 | -48 | 2.9 | BTC/ETH observation-date state; next-session target |
| stock | platforms | HOOD | -0.09 | -0.09 | -1.7 | -2 | 107.77 | BTC/ETH observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | MARA | -0.0525 | -0.0525 | -9.3 | -9 | 11.23 | BTC/ETH observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | MSTR | -0.0525 | -0.0525 | -0.8 | -1 | 132.11 | BTC/ETH observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | RIOT | -0.035 | -0.035 | -3.5 | -4 | 19.96 | BTC/ETH observation-date state; next-session target |
| hedge | hedge | SPY |  | 1.54786 | 4 | 4 | 771.79 | separate-account aggregate SPY beta hedge after confirmed stock fills |

## Orders

| instrument_type | component | instrument | execution_action | rounded_trade_shares | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | CLSK | SELL | -9 | 12.25 | 12.22 | 12.28 | execute once; no same-day reversal or duplicate order |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | HIVE | SELL | -39 | 2.9 | 2.9 | 2.91 | execute once; no same-day reversal or duplicate order |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | MARA | SELL | -8 | 11.23 | 11.2 | 11.26 | execute once; no same-day reversal or duplicate order |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | MSTR | SELL | -1 | 132.11 | 131.78 | 132.44 | execute once; no same-day reversal or duplicate order |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | RIOT | SELL | -3 | 19.96 | 19.91 | 20.01 | execute once; no same-day reversal or duplicate order |
| stock | platforms | HOOD | SELL | -1 | 107.77 | 107.5 | 108.04 | execute once; no same-day reversal or duplicate order |
| stock | platforms\|btc_momentum_vol_carry\|eth_momentum_vol_carry | COIN | SELL | -1 | 183.73 | 183.27 | 184.19 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | SPY | BUY | 3 | 771.79 | 769.86 | 773.72 | single aggregate hedge order after confirming stock fills |
