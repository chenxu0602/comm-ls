# Crypto v4.3 Daily Targets: 2026-09-30

- Signal as-of date: 2026-09-29
- Target trading date: 2026-09-30
- Separate-account AUM: $3,000.00
- Sleeve weights: Platforms 20%, BTC momentum/vol/carry 30%, ETH momentum 20%, HG carry + NG power 30%.
- Aggregate single-name cap: 12.00%
- Gross stock weight: 32.00%
- Net stock weight: -0.00%
- Continuous SPY hedge weight: 5.67%
- Total net weight after SPY hedge: 5.67%
- Full eligible turnover: 28.06%
- Today's executable turnover: 35.68%
- Estimated execution cost: $2.68

## Strategy Change Notes

- Effective with the 2026-09-08 target, separate-account AUM increased from $2,000 to $3,000.
- Added the HG carry + NG power shared sleeve at 30%; allocation changed from Platforms/BTC/ETH = 30%/35%/35% to Platforms/BTC/ETH/HG+NG = 20%/30%/20%/30%.
- The $3,000 AUM keeps the original three sleeves' aggregate nominal budget near its prior level: $3,000 x 70% = $2,100 versus the former $2,000 budget. The incremental capital primarily reserves capacity for the new sleeve when its signal is active.
- On the 2026-09-04 signal date the HG+NG sleeve signal is zero; the 2026-09-08 stock target therefore reflects only the active legacy sleeves and integer rounding.

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
| stock_long_without_hedge | 0.16 | 0.16 | 480 | 480 | 2 |
| stock_short_without_hedge | 0.16 | -0.16 | 480 | -480 | 5 |
| total_hedge | 0.056665 | 0.056665 | 169.99 | 169.99 | 1 |

## Targets

| instrument_type | component | instrument | research_target_weight | target_weight | target_shares | rounded_target_shares | previous_close | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry\|hg_carry_and_power | CLSK | -0.04 | -0.04 | -9 | -9 | 13.31 | BTC/ETH/HG/NG observation-date state; next-session target |
| stock | platforms\|btc_momentum_vol_carry\|eth_momentum_vol_carry\|hg_carry_and_power | COIN | 0.04 | 0.04 | 0.6 | 1 | 190.02 | BTC/ETH/HG/NG observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry\|hg_carry_and_power | HIVE | -0.04 | -0.04 | -39.9 | -40 | 3.01 | BTC/ETH/HG/NG observation-date state; next-session target |
| stock | platforms\|hg_carry_and_power | HOOD | 0.12 | 0.12 | 3.1 | 3 | 116.22 | BTC/ETH/HG/NG observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry\|hg_carry_and_power | MARA | -0.03 | -0.03 | -7.5 | -8 | 11.99 | BTC/ETH/HG/NG observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | MSTR | -0.03 | -0.03 | -0.6 | -1 | 154.67 | BTC/ETH/HG/NG observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry\|hg_carry_and_power | RIOT | -0.02 | -0.02 | -2.8 | -3 | 21.39 | BTC/ETH/HG/NG observation-date state; next-session target |
| hedge | hedge | SPY |  | 0.056665 | 0.2 | 0 | 764.2 | separate-account aggregate SPY beta hedge after confirmed stock fills |

## Orders

| instrument_type | component | instrument | execution_action | rounded_trade_shares | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | platforms\|btc_momentum_vol_carry\|eth_momentum_vol_carry\|hg_carry_and_power | COIN | BUY | 1 | 190.02 | 189.54 | 190.5 | execute once; no same-day reversal or duplicate order |
| stock | platforms\|hg_carry_and_power | HOOD | BUY | 1 | 116.22 | 115.93 | 116.51 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | SPY | SELL | -1 | 764.2 | 762.29 | 766.11 | single aggregate hedge order after confirming stock fills |
