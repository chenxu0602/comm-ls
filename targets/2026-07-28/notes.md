# CL v3.2 Target Revision Notes: 2026-07-28

## Why turnover increased

The 2026-07-28 target was regenerated after correcting the fixed-hold state
machine and synchronizing the production implementation with the executed
logic in `notebooks/backtest_cl.ipynb`. The resulting increase in turnover is
an intentional model-revision effect, not an unexplained discretionary trade.

The corrected target reports:

- target turnover from current positions: 61.35% of AUM;
- full eligible order turnover: 54.83% of AUM;
- executable child-order turnover: 31.50% of AUM after the 40% daily cap;
- 14 planned child orders: 11 stock orders followed by 3 aggregate ETF hedge
  orders after stock fills are confirmed.

The largest sources of additional stock turnover were:

- `services`: removal of the two-session rolling mean increased each active
  FTI/OII/SLB/HAL target from a partial signal to the full sleeve allocation;
- `bwt`: the corrected five-session hold path targeted long ERO/TECK while the
  account was short. The no-same-day-reversal rule therefore limited the first
  child orders to closing the 17-share ERO short and 8-share TECK short;
- `psx_ref`, `refiner`, and other small rebalance legs changed after production
  signal invalidation was made consistent with the notebook cache.

## Fixed-hold correction

The previous implementation refreshed an active fixed-hold position only when
a same-direction signal landed exactly on the old window boundary. A
same-direction signal observed earlier inside the window was incorrectly
discarded.

The corrected causal rule is:

1. a signal becomes a position after the standard one-session delay;
2. every same-direction observation inside the active window refreshes the
   minimum hold from its own execution date;
3. an opposite-direction observation inside the active window is ignored;
4. a new direction can be accepted only after the active window expires.

This correction was applied both to historical position construction and to
the live target event metadata.

## Sleeve synchronization

The production sleeve definitions were synchronized to the notebook as
follows:

| Sleeve | Production position rule effective 2026-07-28 |
| --- | --- |
| `psx_ref` | five-session rolling mean followed by a five-session fixed-hold/reversal lock |
| `refiner` | five-session rolling mean; no fixed hold |
| `fuel` | raw signal with a five-session fixed hold |
| `services` | raw volatility-scaled hysteresis state; no rolling mean |
| `shipping` | two-session rolling mean; no fixed hold |
| `chemical` | raw signal with a 21-session fixed hold |
| `metals` | continuous sign position with the standard one-session delay |
| `bwt` | raw signal with a five-session fixed hold |

Production feature alignment was also corrected so that an explicitly invalid
commodity observation resets the signal exactly as it does in the
feature-return cache/notebook. A date absent from a commodity's own arrival
calendar may still inherit the most recent valid observation.

## Validation

- The production 2026-07-28 stock target vector matched all 26 notebook stock
  targets exactly.
- The focused strategy and execution-policy suite passed 22 tests.
- Ruff and `git diff --check` passed.

