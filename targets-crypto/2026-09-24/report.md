# Crypto v4.3 Daily Targets: 2026-09-24

- Signal as-of date: 2026-09-23
- Target trading date: 2026-09-24
- Separate-account AUM: $3,000.00
- Sleeve weights: Platforms 20%, BTC momentum/vol/carry 30%, ETH momentum 20%, HG carry + NG power 30%.
- Aggregate single-name cap: 12.00%
- Gross stock weight: 22.00%
- Net stock weight: -10.00%
- Continuous SPY hedge weight: 36.50%
- Total net weight after SPY hedge: 26.50%
- Full eligible turnover: 14.69%
- Today's executable turnover: 0.00%
- Estimated execution cost: $0.00

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
| stock_short_without_hedge | 0.16 | -0.16 | 480 | -480 | 5 |
| total_hedge | 0.364958 | 0.364958 | 1094.88 | 1094.88 | 1 |

## Targets

| instrument_type | component | instrument | research_target_weight | target_weight | target_shares | rounded_target_shares | previous_close | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry\|hg_carry_and_power | CLSK | -0.04 | -0.04 | -8.3 | -8 | 14.46 | BTC/ETH/HG/NG observation-date state; next-session target |
| stock | platforms\|btc_momentum_vol_carry\|eth_momentum_vol_carry\|hg_carry_and_power | COIN | 0 | 0 | 0 | 0 | 198.13 | BTC/ETH/HG/NG observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry\|hg_carry_and_power | HIVE | -0.04 | -0.04 | -35.6 | -36 | 3.37 | BTC/ETH/HG/NG observation-date state; next-session target |
| stock | platforms\|hg_carry_and_power | HOOD | 0.06 | 0.06 | 1.5 | 1 | 122.7 | BTC/ETH/HG/NG observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry\|hg_carry_and_power | MARA | -0.03 | -0.03 | -6.7 | -7 | 13.35 | BTC/ETH/HG/NG observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry | MSTR | -0.03 | -0.03 | -0.6 | -1 | 162.2 | BTC/ETH/HG/NG observation-date state; next-session target |
| stock | btc_momentum_vol_carry\|eth_momentum_vol_carry\|hg_carry_and_power | RIOT | -0.02 | -0.02 | -2.4 | -2 | 24.69 | BTC/ETH/HG/NG observation-date state; next-session target |
| hedge | hedge | SPY |  | 0.364958 | 1.4 | 1 | 767.81 | separate-account aggregate SPY beta hedge after confirmed stock fills |

## Orders

No trades above buffer.
