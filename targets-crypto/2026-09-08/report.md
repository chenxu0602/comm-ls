# Crypto v4.3 Daily Targets: 2026-09-08

- Signal as-of date: 2026-09-04
- Target trading date: 2026-09-08
- Separate-account AUM: $3,000.00
- Sleeve weights: Platforms 20%, BTC momentum/vol/carry 30%, ETH momentum 20%, HG carry + NG power 30%.
- Aggregate single-name cap: 12.00%
- Gross stock weight: 20.00%
- Net stock weight: -20.00%
- Continuous SPY hedge weight: 67.14%
- Total net weight after SPY hedge: 47.14%
- Full eligible turnover: 1.81%
- Today's executable turnover: 1.95%
- Estimated execution cost: $0.15

## Execution Notes

- This package belongs to the separate Crypto IB account; never net its SPY hedge with CL/Metals.
- Execute stocks first, then submit the single SPY hedge after confirmed stock fills.
- The SPY child in orders.csv follows post-child integer stock shares; the full continuous hedge remains in targets.csv.
- At $3,000 AUM one SPY share is roughly 25% NAV, so integer hedge rounding is material.
- This is SPY-only hedging. A BTC ETF hedge is not enabled or implied.

## Pinned Signal Inputs

- BTC: `data/cache/feature_return_observation_v1/BTC-multi_return_2.parquet`
- ETH: `data/cache/feature_return_observation_v1/ETH-multi_return_2.parquet`
- HG_NG: `data/processed/commodity_signals_2.parquet`

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0 | 0 | 0 | 0 | 0 |
| stock_short_without_hedge | 0.2 | -0.2 | 600 | -600 | 6 |
| total_hedge | 0.671384 | 0.671384 | 2014.15 | 2014.15 | 1 |

## Targets

| instrument_type | component | instrument | research_target_weight | target_weight | target_shares | rounded_target_shares | previous_close | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry\|hg_carry_and_power | CLSK | -0.04 | -0.04 | -9.5 | -9 | 12.69 | BTC/ETH/HG/NG observation-date state; next-session target |
| stock | platforms\|btc_momentum_vol_carry\|eth_momentum_vol_carry\|hg_carry_and_power | COIN | -0.04 | -0.04 | -0.6 | -1 | 184.64 | BTC/ETH/HG/NG observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry\|hg_carry_and_power | HIVE | -0.04 | -0.04 | -38.6 | -39 | 3.11 | BTC/ETH/HG/NG observation-date state; next-session target |
| stock | platforms\|hg_carry_and_power | HOOD | 0 | 0 | 0 | 0 | 122.11 | BTC/ETH/HG/NG observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry\|hg_carry_and_power | MARA | -0.03 | -0.03 | -8 | -8 | 11.31 | BTC/ETH/HG/NG observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | MSTR | -0.03 | -0.03 | -0.6 | -1 | 142.8 | BTC/ETH/HG/NG observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry\|hg_carry_and_power | RIOT | -0.02 | -0.02 | -2.8 | -3 | 21.8 | BTC/ETH/HG/NG observation-date state; next-session target |
| hedge | hedge | SPY |  | 0.671384 | 2.6 | 3 | 770.19 | separate-account aggregate SPY beta hedge after confirmed stock fills |

## Orders

| instrument_type | component | instrument | execution_action | rounded_trade_shares | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry\|hg_carry_and_power | CLSK | BUY | 2 | 12.69 | 12.66 | 12.72 | execute once; no same-day reversal or duplicate order |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry\|hg_carry_and_power | HIVE | BUY | 7 | 3.11 | 3.1 | 3.12 | execute once; no same-day reversal or duplicate order |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry\|hg_carry_and_power | MARA | BUY | 1 | 11.31 | 11.28 | 11.34 | execute once; no same-day reversal or duplicate order |
