# Crypto v4.3 Daily Targets: 2026-09-17

- Signal as-of date: 2026-09-16
- Target trading date: 2026-09-17
- Separate-account AUM: $3,000.00
- Sleeve weights: Platforms 20%, BTC momentum/vol/carry 30%, ETH momentum 20%, HG carry + NG power 30%.
- Aggregate single-name cap: 12.00%
- Gross stock weight: 52.00%
- Net stock weight: -40.00%
- Continuous SPY hedge weight: 137.33%
- Total net weight after SPY hedge: 97.33%
- Full eligible turnover: 9.29%
- Today's executable turnover: 9.69%
- Estimated execution cost: $0.73

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
| total_hedge | 1.37328 | 1.37328 | 4119.85 | 4119.85 | 1 |

## Targets

| instrument_type | component | instrument | research_target_weight | target_weight | target_shares | rounded_target_shares | previous_close | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry\|hg_carry_and_power | CLSK | -0.1 | -0.1 | -23.5 | -23 | 12.79 | BTC/ETH/HG/NG observation-date state; next-session target |
| stock | platforms\|btc_momentum_vol_carry\|eth_momentum_vol_carry\|hg_carry_and_power | COIN | -0.06 | -0.06 | -1.1 | -1 | 164.51 | BTC/ETH/HG/NG observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry\|hg_carry_and_power | HIVE | -0.085 | -0.085 | -87.9 | -88 | 2.9 | BTC/ETH/HG/NG observation-date state; next-session target |
| stock | platforms\|hg_carry_and_power | HOOD | 0.06 | 0.06 | 1.7 | 2 | 104.42 | BTC/ETH/HG/NG observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry\|hg_carry_and_power | MARA | -0.075 | -0.075 | -20.4 | -20 | 11.04 | BTC/ETH/HG/NG observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | MSTR | -0.075 | -0.075 | -1.8 | -2 | 126.18 | BTC/ETH/HG/NG observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry\|hg_carry_and_power | RIOT | -0.065 | -0.065 | -9.6 | -10 | 20.35 | BTC/ETH/HG/NG observation-date state; next-session target |
| hedge | hedge | SPY |  | 1.37328 | 5.5 | 5 | 754.05 | separate-account aggregate SPY beta hedge after confirmed stock fills |

## Orders

| instrument_type | component | instrument | execution_action | rounded_trade_shares | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | MSTR | SELL | -1 | 126.18 | 125.86 | 126.5 | execute once; no same-day reversal or duplicate order |
| stock | platforms\|btc_momentum_vol_carry\|eth_momentum_vol_carry\|hg_carry_and_power | COIN | SELL | -1 | 164.51 | 164.1 | 164.92 | execute once; no same-day reversal or duplicate order |
