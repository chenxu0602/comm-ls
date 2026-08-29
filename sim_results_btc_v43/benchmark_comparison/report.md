# Crypto v4.3 Benchmark Comparison

- Strategy input: `sim_results_btc_v43/crypto_2.csv`.
- Strategy return is the net SPY-only residual research PnL, not raw stocks plus an explicit tradable hedge.
- Main comparison begins 2022-01-01, when all three sleeves are available.
- BTC time-series momentum uses a 63-session signal, one-session delay and 10.0 bps turnover cost.
- Strategy average gross/net exposure: 44.18% / -26.87%; short-net days: 75.62%.
- All requested local equity benchmarks were found.

## Main-period statistics

| series | annualized_return | annualized_vol | sharpe | max_drawdown | calmar | worst_month | positive_month_share |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Crypto_v43 | 0.5509 | 0.2994 | 1.8402 | 0.3750 | 1.4690 | -0.1913 | 0.7321 |
| SPY | 0.1178 | 0.1741 | 0.6765 | 0.2810 | 0.4192 | -0.0970 | 0.6429 |
| MTUM | 0.1225 | 0.2225 | 0.5507 | 0.3309 | 0.3702 | -0.1356 | 0.5714 |
| BITO | 0.0692 | 0.5424 | 0.1276 | 1.1448 | 0.0605 | -0.5252 | 0.5357 |
| CME_BTC | 0.0548 | 0.5404 | 0.1014 | 1.1273 | 0.0486 | -0.5238 | 0.5179 |
| CME_ETH | -0.1349 | 0.7008 | -0.1925 | 1.3241 | -0.1019 | -0.6405 | 0.4464 |
| BTC_TSMOM_63d | 0.1892 | 0.5404 | 0.3501 | 0.7511 | 0.2519 | -0.2866 | 0.5000 |

## Strategy relationships

| benchmark | correlation | strategy_beta | strategy_avg_when_benchmark_up | strategy_avg_when_benchmark_down | same_sign_share |
| --- | --- | --- | --- | --- | --- |
| SPY | 0.0446 | 0.0766 | 0.0017 | 0.0028 | 0.4938 |
| MTUM | -0.0004 | -0.0006 | 0.0014 | 0.0031 | 0.4885 |
| BITO | -0.3323 | -0.1840 | -0.0026 | 0.0069 | 0.3781 |
| CME_BTC | -0.3308 | -0.1829 | -0.0025 | 0.0067 | 0.3843 |
| CME_ETH | -0.2859 | -0.1218 | -0.0023 | 0.0066 | 0.3908 |
| BTC_TSMOM_63d | 0.1176 | 0.0650 | 0.0039 | 0.0004 | 0.5300 |

## Interpretation guardrails

- Compare Sharpe and drawdown, not total return alone; benchmark volatility differs materially.
- Negative BTC/ETH beta means the strategy is partly an inverse-crypto state trade, not crypto-neutral alpha.
- Re-run this report on the future raw-stock plus explicit-SPY simulation before live promotion.
