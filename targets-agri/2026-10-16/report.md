# Agriculture v4.3 Daily Targets: 2026-10-16

- Signal as-of date: 2026-10-15
- Target source: direct production signal calculation
- AUM: $2,000.00
- Gross raw-stock weight: 17.79%
- Net raw-stock weight: 17.79%
- Gross explicit hedge weight: 26.32%
- Total signed weight after hedges: 8.93%
- Full eligible turnover: 35.38%
- Today's executable turnover: 34.22%
- Estimated execution cost: $1.71
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
| stock_long_without_hedge | 0.1779 | 0.1779 | 355.8 | 355.8 | 2 |
| stock_short_without_hedge | 0 | 0 | 0 | 0 | 0 |
| total_hedge | 0.263211 | -0.088589 | 526.42 | -177.18 | 2 |

## Orders

| instrument_type | instrument | execution_action | rounded_trade_shares | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- |
| stock | ADM | BUY | 3 | 82.93 | 82.72 | 83.14 | execute once; no same-day reversal or duplicate order |
| stock | BG | BUY | 1 | 107.01 | 106.74 | 107.28 | execute once; no same-day reversal or duplicate order |
| hedge | MOO | SELL | -4 | 82.14 | 81.93 | 82.35 | single aggregate hedge order after confirming stock fills |

## Strategy changes and allocation notes

- Agriculture v4.3 joined the main account effective 2026-10-02: $2,000 allocated AUM. Idle allocation remains cash and still counts in account AUM.
- Agriculture uses component-specific hedges: crush_vol/crush_vol2/adm_bg2 use SPY + MOO; adm_bg/adm_tsn/bg_tsn use SPY only. Keep its virtual book separate.
- Agriculture stock target state for this package: active. This is not a permanent suspension.
- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.
- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.
- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.

## Beta method for 2026-10-16 — as-of 2026-10-15

Continues the operator's 2026-10-09 decision to retain legacy daily beta. Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Both methods used identical as-of inventories; stock targets and orders matched. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-10-16-afm7wpl7/cached/targets-agri/2026-10-16. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
