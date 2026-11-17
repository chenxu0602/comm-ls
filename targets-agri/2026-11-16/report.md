# Agriculture v4.3 Daily Targets: 2026-11-16

- Signal as-of date: 2026-11-13
- Target source: direct production signal calculation
- AUM: $2,000.00
- Gross raw-stock weight: 0.00%
- Net raw-stock weight: 0.00%
- Gross explicit hedge weight: 0.00%
- Total signed weight after hedges: 0.00%
- Full eligible turnover: 0.00%
- Today's executable turnover: 0.00%
- Estimated execution cost: $0.00
- Hedge child deferred because stock child is partial: False

## Hedge Mapping

- `residual_return_mkt_w12m`: SPY only.
- `residual_return_mktsec_narrow_w12m`: SPY plus the ticker's narrow ETF (ADM/BG=MOO; TSN=PBJ).
- Betas come from the lagged Agriculture processed panel columns matching each residual definition.
- Hedges are calculated per component leg before broker-level netting.
- Production targets are rebuilt directly from the `_2` soybean cache and crush signals; the notebook CSV is not required.
- Notebook basket weights from 2026-11-16: crush_vol ADM60/BG40; crush_vol2 ADM70/BG30; crush_vol3 ADM100; adm_tsn equal/opposite ADM/TSN. Each sleeve allocation25%, no extra normalization.
- ADM/TSN algorithm/allocation effective 2026-11-16: adjusted-price distance gates, equal/opposite dollar legs instead of rolling pair beta. Operator increased adm_tsn15->25%; crush_vol25/crush_vol2 25%/ADM-only crush_vol3 25%, adm_bg/adm_bg2/bg_tsn0. Nominal100%, no normalization; AUM2000 unchanged. crush_vol3 uses adjusted_zs volatility, MA50 entry constraints, asymmetric exits and SPY+MOO hedges. See docs/agri_crush_vol3_sync_2026-11-16.md.
- Calendar-crush data repair (2026-10-15): crush_01/02/03 merge historical and live contract settlements under contract_source_policy.csv. Each sleeve's required signal field/lookbacks and current stock returns must be complete; missing inputs stop generation. Signal rules, allocations and hedge mappings are unchanged.

## Execution Guard

- Execute raw stocks before ETFs.
- If the 40% stock cap or reversal rule creates a partial stock child, ETF changes are deliberately omitted until the component ledger is reconciled.
- At $2,000 AUM, one SPY share is a very large NAV step; inspect continuous versus rounded hedge exposure manually.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0 | 0 | 0 | 0 | 0 |
| stock_short_without_hedge | 0 | 0 | 0 | 0 | 0 |
| total_hedge | 0 | 0 | 0 | 0 | 0 |

## Orders

No executable orders.

## Strategy changes and allocation notes

- Metals reweight from target2026-11-16: hg_gc_gap15/accel20/SCO-vol25/copper15/miners25%; alloys0 and notebook-only hg_gc_gap_gc_carry_iron_2=0. Nominal100%, no normalization; copper10->15 uses the previously idle5pp. AUM5000, legacy DAILY SPY+XME hedges, signal rules,12% name cap and execution controls unchanged. See docs/metals_reweight_2026-11-16.md.
- CL operator risk reduction effective target session 2026-10-23: chemical allocation reduced from 28% to 14%; psx_ref allocation reduced from 5% to 0% (suspended). At that decision, released 19 percentage points remained cash; no renormalization. Later dated decisions below supersede allocation details.
- At that decision other sleeves were unchanged. CL AUM $15,000 and legacy daily beta remain unchanged. CRO retains its own PSX leg and SPY-only hedge: clearing psx_ref does NOT mean flattening all account PSX. Recompute net stocks and component hedges.
- Chemical is halved BEFORE the existing 5% net single-name cap; previously capped names need not fall by exactly half. Allocation migration turnover is not a signal change.
- Chemical decision rationale: operator questioned the economic clarity of asymmetric exits plus renewing hold-21 and potential historical overfitting, not only recent losses. Rules are deterministic and unchanged; overfitting is a concern, not an established finding. Review parameter robustness, simpler exits, hedge/cost attribution and a 28% counterfactual before any restoration. See docs/cl_risk_reduction_2026-10-23.md.
- Agriculture v4.3 joined the main account effective 2026-10-02: $2,000 allocated AUM. Idle allocation remains cash and still counts in account AUM.
- Agriculture uses component-specific hedges: narrow-sector residual sleeves use SPY + MOO for ADM/BG; adm_bg/adm_tsn/bg_tsn use SPY only. Keep its virtual book separate.
- Agriculture stock target state for this package: flat. This is not a permanent suspension.
- Agriculture notebook basket weights: crush_vol ADM60/BG40; crush_vol2 ADM70/BG30; crush_vol3 ADM100; adm_tsn equal/opposite ADM/TSN. Each sleeve allocation25%, no extra normalization.
- ADM/TSN rule and allocation sync from 2026-11-16: crush_02 momentum with ADM-minus-TSN adjusted-price distance entry gates; equal/opposite dollar legs, no rolling pair-beta sizing. Operator allocation25% (previously15%); crush_vol25/crush_vol2 25%/ADM-only crush_vol3 25%, adm_bg/adm_bg2/bg_tsn0. Nominal100%, no normalization; AUM2000 unchanged. crush_vol3 uses adjusted_zs volatility with MA50 entry constraints and SPY + MOO explicit hedges. See docs/agri_crush_vol3_sync_2026-11-16.md.
- CURRENT FINAL CL from 2026-11-09: operator chemical20->15%, services20->10%, shipping STAYS10% (initial20% package superseded before execution); refiner3/slow8/bwt2/CRO20/re_c03 10% unchanged. Nominal budget78%, no normalization. AUM and legacy DAILY beta unchanged.
- Rules unchanged: chemical hold2 and L/PP exits; slow HO m1 gate carry_data_2; CRO half-balance SPY-only, re_c03 SPY+XLE. Track allocation migration separately from signal changes. See docs/cl_reweight_2026-11-09.md.
- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.
- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.
- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.

## Beta method for 2026-11-16 — as-of 2026-11-13

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-11-16-unv2y3l0/cached/targets-agri/2026-11-16. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
