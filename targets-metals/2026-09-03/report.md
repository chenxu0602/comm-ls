# Metals Daily Targets: 2026-09-03

- Signal as-of date: 2026-09-02
- Target trading date: 2026-09-03
- AUM: $5,000.00
- Gross stock weight: 44.00%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: 44.00%
- Gross hedge weight: 46.38%
- Total net weight after hedges: -2.38%
- Turnover from Metals-attributed current positions: 14.38%
- Full eligible order turnover: 1.62%
- Today's total child-order turnover: 1.76%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $0.22

## Isolation and Execution Notes

- Signal construction is fail-closed on the `_2` cache/carry pipeline; it does not read the current non-`_2` signal cache.
- Required feature observations must be no more than 3 calendar days old.
- Current positions must be Metals-attributed, not a full shared IB account export.
- Execute stock orders once in the first 30 minutes; aggregate SPY/XME hedge orders only after confirming stock fills.
- Direct same-day reversals are flattened first by the child-order policy.

## Pinned Signal Inputs

- metals_cache: `data/cache/feature_return_observation_v1/METALS-multi_return_2.parquet`; latest n/a
- gc_cache: `data/cache/feature_return_observation_v1/GC-multi_return_2.parquet`; latest n/a
- sco_cache: `data/cache/feature_return_observation_v1/SCO-multi_return_2.parquet`; latest n/a
- carry_dir: `data/comm/carry_data_2`; latest n/a
- commodity_dir: `data/comm`; latest n/a

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.44 | 0.44 | 2200 | 2200 | 8 |
| stock_short_without_hedge | 0 | 0 | 0 | 0 | 0 |
| total_hedge | 0.463799 | -0.463799 | 2318.99 | -2318.99 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | sco_specialty_alloys | ATI | 0.02 | 0.5 | 201.69 | 1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-0.83585;drawdown_63d=0.149253;realized_vol_63d=-0.49051 |
| stock | sco_vol_gc_hg_accel_miners\|miners | BHP | 0.12 | 6.4 | 93.43 | 0.6 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.26571;q_long_exit=2.19671;q_short_entry=2.19671;q_short_exit=1.43629;vol_diff=-0.105714;accel=0.0809777; aggregate BHP capped at 12.0%\|persistent_binary active; feature=-0.01429; aggregate BHP capped at 12.0% |
| stock | sco_specialty_alloys | CRS | 0.02 | 0.2 | 460.97 | 1.1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-0.83585;drawdown_63d=0.149253;realized_vol_63d=-0.49051 |
| stock | miners | FSUGY | 0.05 | 10.4 | 24.11 | 0.7 | 0.2 | persistent_binary active; feature=-0.01429 |
| stock | sco_specialty_alloys | HWM | 0.01 | 0.2 | 252.96 | 0.9 | 0.1 | sco_specialty_alloys_hysteresis active; ret_63d=-0.83585;drawdown_63d=0.149253;realized_vol_63d=-0.49051 |
| stock | sco_vol_gc_hg_accel_miners\|miners | RIO | 0.12 | 5.8 | 102.75 | 0.3 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.26571;q_long_exit=2.19671;q_short_entry=2.19671;q_short_exit=1.43629;vol_diff=-0.105714;accel=0.0809777; aggregate RIO capped at 12.0%\|persistent_binary active; feature=-0.01429; aggregate RIO capped at 12.0% |
| stock | sco_vol_gc_hg_accel_miners\|copper_miner\|miners | SCCO | 0.05 | 1.2 | 204.26 | 0.8 | 0.9 | sco_vol_gc_hg_combo active; sco_vol=1.26571;q_long_exit=2.19671;q_short_entry=2.19671;q_short_exit=1.43629;vol_diff=-0.105714;accel=0.0809777\|copper_energy_terms_of_trade active; hg_cl_ratio=0.84385;ho_ret=0.00104706;hg_mv_5=0.837224;hg_mv_200=0.851043;hg_mv_diff=-0.0138185;hg_threshold=0.00704821;ho_momentum_20d=0.239312;ho_threshold=0.0300897\|persistent_binary active; feature=-0.01429 |
| stock | sco_vol_gc_hg_accel_miners\|miners | VALE | 0.05 | 15.9 | 15.73 | 0.3 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.26571;q_long_exit=2.19671;q_short_entry=2.19671;q_short_exit=1.43629;vol_diff=-0.105714;accel=0.0809777\|persistent_binary active; feature=-0.01429 |
| hedge | hedge | SPY | -0.251158 | -1.6 | 765.16 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | -0.212641 | -8.9 | 119.46 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | miners | FSUGY | SELL | -3 | -3 | -0.014466 | False | 24.11 | 24.05 | 24.17 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners\|miners | VALE | SELL | -1 | -1 | -0.003146 | False | 15.73 | 15.69 | 15.77 | execute once; no same-day reversal or duplicate order |
