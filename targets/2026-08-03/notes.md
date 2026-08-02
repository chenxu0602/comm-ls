# CL v3.2 Target Revision Notes: 2026-08-03

## Prospective earnings-event default allow

Before finalizing the 2026-08-03 target package, the live corporate-event
overlay changed prospectively from case-by-case earnings flattening to a
default `allow` policy. WLK and the other confirmed future earnings events in
the current calendar remain eligible while their underlying strategy signals
are active.

This decision is based on two methodology constraints:

- no point-in-time counterfactual backtest currently shows that systematic
  pre-earnings liquidation improves cost-adjusted performance or tail risk;
- the strategy's multi-session holding periods make an earnings move part of
  the realized position path, so removing it also introduces an unvalidated
  exit and re-entry rule.

The change is not based on hindsight from HUN's 2026-07-31 decline. HUN and
the other historical event flatten decisions remain recorded as actually
implemented and are not restated. Earnings dates remain in the calendar for
monitoring and prospective allow-versus-flatten attribution. A separately
documented exceptional risk may still receive a manual `flatten` decision.

The earlier 2026-08-03 target package with WLK flattened is superseded after
regeneration with `--overwrite`. Its orders and aggregate hedge quantities
must not be mixed with the regenerated package.
