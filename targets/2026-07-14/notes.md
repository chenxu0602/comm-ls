# Target Notes: 2026-07-14

## BWT holding-period change

- Effective with the 2026-07-14 production target, shorten the BWT sleeve's
  fixed holding period from 21 sessions to 10 sessions.
- Keep the BWT universe (`ERO`, `TECK`), sleeve weight (6%), equal internal
  weights, feature (`brent_wti_carry_spread`), threshold (2%), inverse
  direction, and XME hedge mapping unchanged.
- The change matches the current implementation in
  `notebooks/backtest_cl.ipynb`.

Validation on the latest CL cache, using the unchanged signal and 25 bps
position-turnover cost:

| Metric | 21d hold | 10d hold |
|---|---:|---:|
| Full-sample net Sharpe | 0.468 | 0.508 |
| Pre-2024 net Sharpe | 0.356 | 0.321 |
| 2024+ net Sharpe | 1.018 | 1.434 |
| Unit-weight turnover | 73 | 123 |
| Full-sample max drawdown | 0.743 | 1.061 |

Interpretation: this is a modest holding-period alignment with better recent
OOS behavior, not evidence of a new alpha source. It increases turnover and
worsens the full-sample maximum drawdown, so live execution and subsequent
forward performance should continue to be monitored.
