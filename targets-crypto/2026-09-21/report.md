# Crypto v4.3 Daily Targets: 2026-09-21

- Signal as-of date: 2026-09-18
- Target trading date: 2026-09-21
- Separate-account AUM: $3,000.00
- Sleeve weights: Platforms 20%, BTC momentum/vol/carry 30%, ETH momentum 20%, HG carry + NG power 30%.
- Aggregate single-name cap: 12.00%
- Gross stock weight: 52.00%
- Net stock weight: -40.00%
- Continuous SPY hedge weight: 138.30%
- Total net weight after SPY hedge: 98.30%
- Full eligible turnover: 5.70%
- Today's executable turnover: 8.08%
- Estimated execution cost: $0.61

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
| stock_long_without_hedge | 0.06 | 0.06 | 180 | 180 | 1 |
| stock_short_without_hedge | 0.46 | -0.46 | 1380 | -1380 | 6 |
| total_hedge | 1.38302 | 1.38302 | 4149.07 | 4149.07 | 1 |

## Targets

| instrument_type | component | instrument | research_target_weight | target_weight | target_shares | rounded_target_shares | previous_close | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry\|hg_carry_and_power | CLSK | -0.1 | -0.1 | -20.7 | -21 | 14.47 | BTC/ETH/HG/NG observation-date state; next-session target |
| stock | platforms\|btc_momentum_vol_carry\|eth_momentum_vol_carry\|hg_carry_and_power | COIN | -0.06 | -0.06 | -0.9 | -1 | 194.25 | BTC/ETH/HG/NG observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry\|hg_carry_and_power | HIVE | -0.085 | -0.085 | -74.8 | -75 | 3.41 | BTC/ETH/HG/NG observation-date state; next-session target |
| stock | platforms\|hg_carry_and_power | HOOD | 0.06 | 0.06 | 1.5 | 2 | 119.82 | BTC/ETH/HG/NG observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry\|hg_carry_and_power | MARA | -0.075 | -0.075 | -17 | -17 | 13.24 | BTC/ETH/HG/NG observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | MSTR | -0.075 | -0.075 | -1.5 | -1 | 153.92 | BTC/ETH/HG/NG observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry\|hg_carry_and_power | RIOT | -0.065 | -0.065 | -8.2 | -8 | 23.75 | BTC/ETH/HG/NG observation-date state; next-session target |
| hedge | hedge | SPY |  | 1.38302 | 5.4 | 5 | 761.69 | separate-account aggregate SPY beta hedge after confirmed stock fills |

## Orders

| instrument_type | component | instrument | execution_action | rounded_trade_shares | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | MSTR | BUY | 1 | 153.92 | 153.54 | 154.3 | execute once; no same-day reversal or duplicate order |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry\|hg_carry_and_power | CLSK | BUY | 1 | 14.47 | 14.43 | 14.51 | execute once; no same-day reversal or duplicate order |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry\|hg_carry_and_power | HIVE | BUY | 7 | 3.41 | 3.4 | 3.42 | execute once; no same-day reversal or duplicate order |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry\|hg_carry_and_power | MARA | BUY | 2 | 13.24 | 13.21 | 13.27 | execute once; no same-day reversal or duplicate order |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry\|hg_carry_and_power | RIOT | BUY | 1 | 23.75 | 23.69 | 23.81 | execute once; no same-day reversal or duplicate order |
