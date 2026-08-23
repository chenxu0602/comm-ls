# CL v4.2 Production Cutover Notes: 2026-08-24

## Production decision

- Effective for the 2026-08-24 US session, CL production uses v4.2 through
  `scripts/generate_cl_v42_daily_targets.py`.
- All ordinary CL, HO, XB and NG features use canonical empty-suffix caches:
  `*-multi_return.parquet`. The production entry point rejects `_2` or any
  other non-empty cache suffix.
- V4.2 retains the v4.1 sleeve definitions and weights, but replaces the
  original shipping implementation with the approved NG opposition-veto
  shipping rule.
- CL v4.1 with `_2` remains a rollback/reference path only. Do not combine its
  targets or orders with the 2026-08-24 canonical v4.2 package.

## Attribution boundary

- The 2026-08-19 through 2026-08-21 sessions remain attributed to CL v4.1
  `_2`; those historical targets and PnL are not restated.
- Orders executed on 2026-08-24 start the CL v4.2 canonical actual-IB record.
- The same session is also the first production inclusion of the separately
  researched Metals/mining alpha satellite. Historical IB results through
  2026-08-21 contain CL-family sleeves only and must not be restated as if the
  standalone Metals strategy had already been active.
- The production capital convention from this date is USD 15,000 for CL v4.2
  plus USD 5,000 for Metals, for USD 20,000 combined strategy AUM. Performance
  must retain separate `cl_v42`, `metals`, and combined-account attribution.
- Record the 2026-08-24 migration turnover, explicit-hedge changes, integer
  rounding and execution costs separately from ongoing strategy PnL.
- Because the USD 5,000 Metals satellite begins in the same session, the
  standalone CL and Metals order files are review artifacts only.
  Preserve both generators' strategy-level sleeve rounding and child caps,
  then sum `rounded_trade_shares` by ticker and submit one net order per name.
  Recheck the net child basket against the 40% combined USD 20,000 account
  cap. Preserve CL as the incumbent allocation if further scaling is needed;
  allocate only residual implementation capacity to Metals.
- The 2026-08-21 actual IB result was approximately +29 bp on USD 15,000 AUM,
  versus +36 bp for `_2` implicit residual and -32 bp for the canonical
  counterfactual. This was an `_2`-positioned live session and is not a clean
  ex-post comparison between the two data paths.

See `docs/cl_v42_production_change_2026-08-24.md` for the full production
definition and replication record. See
`docs/shared_account_cl_metals_workflow.md` for the mandatory combined-account
generation, netting, hedge and attribution procedure.
