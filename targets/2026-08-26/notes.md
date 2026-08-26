# 2026-08-26 production notes: CL v4.3 cutover

## Decision and attribution boundary

The 2026-08-26 US session is the production cutover from CL v4.2 to CL v4.3.
Orders executed for this session begin the CL v4.3 actual-IB record. Do not
relabel the 2026-08-24 or 2026-08-25 sessions as v4.3, and keep today's
migration turnover identifiable in reconciliation.

V4.3 does not change sleeve definitions, weights, thresholds, holding rules,
the NG shipping veto, name caps or execution rules. It changes the daily
commodity/equity date alignment and pins production to the `_2` cache family:

- stock trading dates are the authoritative left calendar;
- each stock date receives the latest commodity observation date less than or
  equal to that stock date;
- arrival remains audit metadata and no longer moves the daily feature to a
  later stock row;
- production caches must report
  `feature_alignment_mode=stock_observation_asof`.

The prior v4.2 generator and legacy cache root remain the rollback path.

## Exact backtest replication

The production dry run and final source packages were compared with the
executed v43 notebooks for target date 2026-08-26:

- all 26 CL stock target weights matched `backtest_cl_v43` exactly;
- all 8 capped Metals stock target weights matched `backtest_mt_v43` exactly;
- maximum absolute target-weight difference was `0.0` for both strategies;
- CL canonical and `_2` v43 caches produced the same target today, while
  production remains pinned to the audited `_2` family.

## Target changes versus the superseded package

The original 2026-08-26 package was generated under the prior alignment. The
v4.3 CL continuous targets changed as follows:

| Instrument | Prior target | V4.3 target | Change |
| --- | ---: | ---: | ---: |
| DINO | -0.004 | 0.004 | 0.008 |
| DK | -0.010 | 0.010 | 0.020 |
| PBF | -0.006 | 0.006 | 0.012 |
| FTI | 0.000 | -0.020 | -0.020 |
| HAL | 0.000 | -0.010 | -0.010 |
| SLB | 0.000 | -0.020 | -0.020 |

All other CL continuous stock weights were unchanged. The refiner targets
crossed from small shorts to small longs, but the no-direct-reversal rule means
today's DINO, DK and PBF children only flatten the existing shorts. Their
remaining long targets are deferred.

The Metals v43 alignment changed the capped targets for VALE from 0.070 to
0.100 and FSUGY from 0.050 to 0.065. Other capped Metals stock targets were
unchanged.

## Why the oil-services trades reappeared

The corrected CL history treats the services short as a carried state that
began on 2026-01-30, not as a fresh 2026-08-25 entry. The legacy `_2` alignment
mapped a non-stock-session observation dated 2026-04-26 into the 2026-04-27
stock row with a missing feature. The strategy's fail-flat missing-value rule
then cleared the hysteresis state. Under stock-observation-date alignment, the
latest valid futures observation is retained and the false reset disappears.

The current `jun_dec_annualized_carry_v2` z-score is approximately -0.0095.
The services short remains active because its original entry was below -1 and
the configured exit requires a subsequent z-score above +0.5. Therefore the
SLB, HAL and FTI orders restore a previously interrupted carried state; they
are not a new extreme-value trigger.

## Broker-order differences

Relative to the superseded seven-order package:

- DINO buy increased from 1 to 2 shares;
- DK buy increased from 5 to 7 shares;
- PBF buy increased from 3 to 4 shares;
- XLE sell increased from 14 to 16 shares;
- the prior XME buy 1 order was cancelled because the combined XME target is
  already the current -22 shares;
- new orders were added: sell 6 SLB, sell 4 HAL, sell 4 FTI, buy 3 FSUGY and
  buy 10 VALE;
- sell 2 DOW and sell 1 LYB were unchanged.

The final combined package contains 11 executable orders and 15.13% child
turnover on USD 20,000 combined AUM. `targets/2026-08-26/orders.csv` is the
sole broker-order source for this session.
