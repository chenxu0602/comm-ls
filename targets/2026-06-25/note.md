# 2026-06-25 Notes

## Strategy Version Change

The 2026-06-25 target files were generated after reducing the `services`
sleeve from the prior live weight of 17.5% to 10.0%.

Current services target weights:

| instrument | target_weight |
| --- | ---: |
| FTI | -6.0% |
| OII | -4.0% |

Prior live sizing was approximately:

| instrument | target_weight |
| --- | ---: |
| FTI | -10.5% |
| OII | -7.0% |

The 2026-06-25 IB/live PnL should therefore be interpreted carefully: actual
positions still reflected the older, larger services sizing, while the generated
targets reflected the reduced 10% services sleeve.

## Backtest Comparison Policy

For research comparability, backtests after this change should use the new 10%
services sleeve weight across the full historical sample. This is a clean
"what would the current strategy have done historically" comparison.

Do not splice the historical backtest by using 17.5% before 2026-06-25 and 10%
after 2026-06-25 unless the goal is specifically to reproduce the live pilot
implementation path. The spliced path is useful for IB reconciliation, but it is
not the preferred strategy-quality benchmark.

## Reconciliation Note

The 2026-06-25 target generation did not ingest current IB positions, so
`current_shares` in `targets.csv` / `orders.csv` is zero. As a result, the order
plan shows target opening trades from zero rather than the rebalance trades
needed to reduce an existing 17.5% services sleeve to the new 10% sleeve.

Future live target runs should pass current IB positions into the target
generator before relying on `trade_shares` or `rounded_trade_shares`.
