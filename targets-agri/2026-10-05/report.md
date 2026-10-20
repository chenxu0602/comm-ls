# Agriculture v4.3 Daily Targets: 2026-10-05

- Signal as-of date: 2026-10-02
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
