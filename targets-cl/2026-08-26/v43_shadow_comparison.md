# CL v4.3 shadow comparison for 2026-08-26

The production-code dry run was written under
`/private/tmp/comm-ls-v43-check` and did not overwrite this day's existing
v4.2 package.

V4.3 `_2` stock-observation alignment exactly matched the v43 notebook target.
Relative to the existing v4.2 package, continuous CL target changes were:

| Ticker | v4.2 | v4.3 | Change |
| --- | ---: | ---: | ---: |
| DINO | -0.004 | 0.004 | 0.008 |
| DK | -0.010 | 0.010 | 0.020 |
| PBF | -0.006 | 0.006 | 0.012 |
| FTI | 0.000 | -0.020 | -0.020 |
| HAL | 0.000 | -0.010 | -0.010 |
| SLB | 0.000 | -0.020 | -0.020 |

All other CL stock target weights were unchanged. The gross absolute change is
9.0% of CL AUM. This file records a comparison, not submitted broker orders.
