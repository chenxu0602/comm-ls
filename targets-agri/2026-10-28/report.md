# Agriculture v4.3 Daily Targets: 2026-10-28

- Signal as-of date: 2026-10-27
- Target source: direct production signal calculation
- AUM: $2,000.00
- Gross raw-stock weight: 64.44%
- Net raw-stock weight: 13.76%
- Gross explicit hedge weight: 21.00%
- Total signed weight after hedges: 20.96%
- Full eligible turnover: 5.07%
- Today's executable turnover: 5.07%
- Estimated execution cost: $0.25
- Hedge child deferred because stock child is partial: False

## Hedge Mapping

- `residual_return_mkt_w12m`: SPY only.
- `residual_return_mktsec_narrow_w12m`: SPY plus the ticker's narrow ETF (ADM/BG=MOO; TSN=PBJ).
- Betas come from the lagged Agriculture processed panel columns matching each residual definition.
- Hedges are calculated per component leg before broker-level netting.
- Production targets are rebuilt directly from the `_2` soybean cache and crush signals; the notebook CSV is not required.
- Calendar-crush data repair (2026-10-15): crush_01/02/03 merge historical and live contract settlements under contract_source_policy.csv. Each sleeve's required signal field/lookbacks and current stock returns must be complete; missing inputs stop generation. Signal rules, allocations and hedge mappings are unchanged.

## Execution Guard

- Execute raw stocks before ETFs.
- If the 40% stock cap or reversal rule creates a partial stock child, ETF changes are deliberately omitted until the component ledger is reconciled.
- At $2,000 AUM, one SPY share is a very large NAV step; inspect continuous versus rounded hedge exposure manually.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.391 | 0.391 | 782 | 782 | 1 |
| stock_short_without_hedge | 0.2534 | -0.2534 | 506.8 | -506.8 | 1 |
| total_hedge | 0.210025 | 0.07199 | 420.05 | 143.98 | 2 |

## Orders

| instrument_type | instrument | execution_action | rounded_trade_shares | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- |
| stock | BG | SELL | -1 | 101.36 | 101.11 | 101.61 | execute once; no same-day reversal or duplicate order |

## Strategy changes and allocation notes

- CL operator risk reduction effective target session 2026-10-23: chemical allocation reduced from 28% to 14%; psx_ref allocation reduced from 5% to 0% (suspended). At that decision, released 19 percentage points remained cash; no renormalization. Later dated decisions below supersede allocation details.
- At that decision other sleeves were unchanged. CL AUM $15,000 and legacy daily beta remain unchanged. CRO retains its own PSX leg and SPY-only hedge: clearing psx_ref does NOT mean flattening all account PSX. Recompute net stocks and component hedges.
- Chemical is halved BEFORE the existing 5% net single-name cap; previously capped names need not fall by exactly half. Allocation migration turnover is not a signal change.
- Chemical decision rationale: operator questioned the economic clarity of asymmetric exits plus renewing hold-21 and potential historical overfitting, not only recent losses. Rules are deterministic and unchanged; overfitting is a concern, not an established finding. Review parameter robustness, simpler exits, hedge/cost attribution and a 28% counterfactual before any restoration. See docs/cl_risk_reduction_2026-10-23.md.
- CURRENT CL risk override effective target session 2026-10-28 supersedes earlier allocations: chemical 14% -> 0% (suspended), refiner 5% -> 2.5%, refiner_slow 10% -> 5%. Released 21.5 percentage points stay cash; no renormalization. CL AUM remains $15,000.
- Chemical suspension reflects unresolved exit-rule economics pending chemical input/output commodity research; refiner reduction limits drawdown risk. Neither is proof of alpha failure or an optimized historical improvement. Notebook/research chemical remains 28%; no signal rules changed. Restoration requires renewed operator approval; no automatic restoration.
- psx_ref remains 0%; CRO remains 10% allocation with SPY-only hedging. Old/slow refiner retain SPY/XLE legacy DAILY beta; the slow basket sync is recorded below. Other books and AUM are unchanged. Do not flatten all PSX or remove shared ETF hedges independently of component targets.
- Refiner_slow notebook sync effective 2026-10-28: DK/DINO/PBF/PSX = 30/25/25/20%; CL momentum/vol gate uses carry_data CL m0_ret, not m1_ret; carry change uses ffill then diff(50). Slow allocation remains 5%, old refiner 2.5%; no fixed hold or smoothing. Earlier basket descriptions are superseded.
- Recompute component hedges and account-netted orders from actual inventories; allocation migration is separate from signal turnover. Stock execution caps may leave remaining positions for later sessions. See docs/cl_risk_reduction_2026-10-28.md.
- Agriculture v4.3 joined the main account effective 2026-10-02: $2,000 allocated AUM. Idle allocation remains cash and still counts in account AUM.
- Agriculture uses component-specific hedges: crush_vol/crush_vol2/adm_bg2 use SPY + MOO; adm_bg/adm_tsn/bg_tsn use SPY only. Keep its virtual book separate.
- Agriculture stock target state for this package: active. This is not a permanent suspension.
- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.
- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.
- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.

## Beta method for 2026-10-28 — as-of 2026-10-27

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-10-28-m68fj3vk/cached/targets-agri/2026-10-28. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
