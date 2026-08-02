# CL v3.2 Execution Notes: 2026-07-30

## Intraday corporate-event override

After the original 2026-07-30 target package was generated, a manual
corporate-event risk decision was approved for the three chemical shorts with
earnings scheduled for 2026-07-31. This was a temporary risk overlay, not a
change to the underlying CL signal or chemical sleeve specification.

| Instrument | Generated target weight | Position before override | Executed event target | Status |
| --- | ---: | ---: | ---: | --- |
| EMN | -2.8% | -6 shares | 0 shares | bought to cover; complete |
| HUN | -2.8% | -33 shares | 0 shares | bought to cover; complete |
| LYB | -5.0% | -13 shares | 0 shares | bought to cover; complete |

The decision used the `event_risk_v0_1` conservative tail-risk prior. It does
not assert earnings-direction alpha. The released weight remains in cash and
is not redistributed to other chemical names.

The production event calendar records all three decisions as `flatten`, with
`pre_event_sessions=1` and `post_event_sessions=1`. They must remain at zero
through the first full post-announcement session. For the current calendar,
the action window ends on 2026-08-03, so the earliest possible strategy
re-entry is the 2026-08-04 target, conditional on a fresh signal and target
calculation.

## Hedge recalculation after confirmed stock fills

The explicit hedge was recalculated from confirmed integer stock positions,
USD 15,000 AUM, the 252-session two-factor beta estimates available through
2026-07-29, and the intraday prices shown in IB. The continuous hedge estimates
and executed integer positions were:

| Hedge | Continuous shares | Prior shares | Executed shares | Final shares |
| --- | ---: | ---: | ---: | ---: |
| SPY | -1.6073 | 0 | sell short 2 | -2 |
| XLE | 55.8169 | 76 | sell 20 | 56 |
| XME | -4.1886 | -5 | buy to cover 1 | -4 |

The final IB position snapshot confirmed EMN, HUN, and LYB absent from the
book and hedge positions of SPY -2, XLE +56, and XME -4.

## Artifact interpretation

`targets.csv`, `orders.csv`, `summary.csv`, and `report.md` in this directory
remain the immutable pre-override target-generation snapshot. This note and
`targets/corporate_event_calendar.csv` document the subsequent discretionary
risk overlay and the actual post-fill hedge state. Future live reconciliation
should use the confirmed IB positions rather than treating the original hedge
rows as the executed target.
