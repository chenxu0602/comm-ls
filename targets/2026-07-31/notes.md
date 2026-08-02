# CL v3.2 Target Revision Notes: 2026-07-31

## Prospective service sleeve risk reduction

Before regenerating the 2026-07-31 target package, the `services` sleeve was
reduced from 10% to 5%. FTI, OII, SLB, and HAL remain equal-weighted, changing
each continuous target from 2.5% to 1.25%.

This is a prospective risk-budget decision prompted by deterioration in the
service sleeve since 2024 and an unusually weak recent five-session result. A
mechanical diagnostic that halved only the service contribution showed:

| Diagnostic | 10% service | 5% service |
| --- | ---: | ---: |
| Full-history Sharpe | 1.90 | 1.87 |
| 2024+ Sharpe | 3.06 | 3.11 |
| 2024+ maximum drawdown | -4.10% | -3.76% |
| Latest four-session portfolio PnL | -259 bps | -220 bps |
| Current portfolio drawdown | -2.59% | -2.20% |

The small deterioration in full-history Sharpe indicates that the sleeve had
useful earlier history, while the post-2024 and recent diagnostics support
lowering its current risk allocation. The 5% allocation preserves forward
evidence collection without deleting the sleeve after a drawdown.

No service signal parameter was changed: the feature remains CL
`carry_chg_21d`, direction remains inverse, the 60-session volatility-scaled
hysteresis rule remains in force, and the hedge mapping remains SPY plus XLE.
Changing only the sleeve weight avoids simultaneously reselecting the signal
or constituents.

The released 5% remains in cash. It is not reallocated to sleeves with strong
recent performance.

## Prospective metals sleeve risk reduction

The `metals` sleeve was also reduced from 10% to 5% before the 2026-07-31
target was regenerated. The existing 55% ATI / 45% CRS internal weights are
unchanged, giving continuous targets of 2.75% for ATI and 2.25% for CRS.

This decision is supported by fragility that predates the latest loss:

- the sleeve contains only two closely related specialty-alloy companies;
- approximately 53% of its cumulative historical PnL came from 2020, exceeding
  the strategy's 30% single-year concentration guardrail;
- standalone sleeve Sharpe was approximately 0.03 from 2025 onward before the
  latest update;
- its latest five-session PnL was approximately -126 bps, around the bottom
  0.22% of historical rolling five-session observations.

A mechanical diagnostic that halved only the metals contribution reduced the
latest five-session portfolio loss by approximately 63 bps and improved the
2025+ portfolio Sharpe from 3.44 to 3.59, while full-history portfolio Sharpe
changed only modestly from 1.87 to 1.85.

No metals signal parameter was changed: the feature remains CL
`next_dec_annualized_carry_gap_le_9m_v2`, direction remains inverse, the
continuous position rule remains in force, ATI/CRS remain the constituents,
and the hedge mapping remains SPY plus XME.

The released metals allocation also remains in cash. Following both risk
reductions, total configured sleeve weight is 88%, leaving 12% strategic cash
before inactive signals and single-name caps.

## Recordkeeping and regeneration

The lower allocations are effective prospectively for the 2026-07-31 target
and must not be used to restate earlier live results. The target package that
existed before these changes used 10% service and 10% metals allocations and
is superseded once the package is regenerated with `--overwrite`.

Corporate-event overlays remain separate from this strategy-weight decision.
In particular, the approved EMN, HUN, and LYB earnings-event flatten decisions
continue to apply when the target package is regenerated.

All stock orders and aggregate SPY/XLE/XME hedge orders from the earlier
2026-07-31 package become stale after regeneration. Execution must use the new
`orders.csv` and recalculate aggregate hedge orders after confirming stock
fills.
