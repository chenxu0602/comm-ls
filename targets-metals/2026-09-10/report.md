# Metals Daily Targets: 2026-09-10

- Signal as-of date: 2026-09-09
- Target trading date: 2026-09-10
- AUM: $5,000.00
- Gross stock weight: 48.50%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: 48.50%
- Gross hedge weight: 47.36%
- Total net weight after hedges: 1.14%
- Turnover from Metals-attributed current positions: 29.01%
- Full eligible order turnover: 23.06%
- Today's total child-order turnover: 29.36%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $3.67

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
| stock_long_without_hedge | 0.485 | 0.485 | 2425 | 2425 | 8 |
| stock_short_without_hedge | 0 | 0 | 0 | 0 | 0 |
| total_hedge | 0.47356 | -0.47356 | 2367.8 | -2367.8 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | sco_specialty_alloys | ATI | 0.02 | 0.5 | 206.54 | 1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-0.467837;drawdown_63d=0.668252;realized_vol_63d=-0.0919812 |
| stock | hg_gc_gap_gc_carry_iron\|sco_vol_miners\|miners | BHP | 0.12 | 6.5 | 92.25 | 0.6 | 0.5 | dual_feature_hysteresis active; hg_gap=0.00458366;gc_carry=-0.118862; aggregate BHP capped at 12.0%\|sco_vol_regime_pulse active; sco_vol=1.43143;vol_quantile=2.0205;vol_diff=0.04; aggregate BHP capped at 12.0%\|persistent_binary active; feature=0.00458366; aggregate BHP capped at 12.0% |
| stock | sco_specialty_alloys | CRS | 0.02 | 0.2 | 458.45 | 1.1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-0.467837;drawdown_63d=0.668252;realized_vol_63d=-0.0919812 |
| stock | hg_gc_gap_gc_carry_iron\|miners | FSUGY | 0.07 | 13.9 | 25.12 | 0.6 | 0.3 | dual_feature_hysteresis active; hg_gap=0.00458366;gc_carry=-0.118862\|persistent_binary active; feature=0.00458366 |
| stock | sco_specialty_alloys | HWM | 0.01 | 0.2 | 232.62 | 1 | 0.1 | sco_specialty_alloys_hysteresis active; ret_63d=-0.467837;drawdown_63d=0.668252;realized_vol_63d=-0.0919812 |
| stock | hg_gc_gap_gc_carry_iron\|sco_vol_miners\|miners | RIO | 0.12 | 5.8 | 103.74 | 0.3 | 0.5 | dual_feature_hysteresis active; hg_gap=0.00458366;gc_carry=-0.118862; aggregate RIO capped at 12.0%\|sco_vol_regime_pulse active; sco_vol=1.43143;vol_quantile=2.0205;vol_diff=0.04; aggregate RIO capped at 12.0%\|persistent_binary active; feature=0.00458366; aggregate RIO capped at 12.0% |
| stock | sco_vol_miners\|copper_miner\|miners | SCCO | 0.03 | 0.7 | 209.26 | 0.7 | 0.9 | sco_vol_regime_pulse active; sco_vol=1.43143;vol_quantile=2.0205;vol_diff=0.04\|copper_energy_terms_of_trade active; hg_cl_ratio=0.84719;ho_ret=0.0497925;hg_mv_5=0.808119;hg_mv_200=0.849755;hg_mv_diff=-0.0416365;hg_threshold=0.00745267;ho_momentum_20d=0.150862;ho_threshold=0.0299025\|persistent_binary active; feature=0.00458366 |
| stock | hg_gc_gap_gc_carry_iron\|sco_vol_miners\|miners | VALE | 0.095 | 30.8 | 15.44 | 0.2 | 0.5 | dual_feature_hysteresis active; hg_gap=0.00458366;gc_carry=-0.118862\|sco_vol_regime_pulse active; sco_vol=1.43143;vol_quantile=2.0205;vol_diff=0.04\|persistent_binary active; feature=0.00458366 |
| hedge | hedge | SPY | -0.249369 | -1.6 | 762.4 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | -0.224191 | -9.4 | 119.19 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | hg_gc_gap_gc_carry_iron\|sco_vol_miners\|miners | RIO | BUY | 1 | 1 | 0.020748 | False | 103.74 | 103.48 | 104 | execute once; no same-day reversal or duplicate order |
| stock | hg_gc_gap_gc_carry_iron\|sco_vol_miners\|miners | VALE | BUY | 10 | 10 | 0.03088 | False | 15.44 | 15.4 | 15.48 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_miners\|copper_miner\|miners | SCCO | BUY | 1 | 1 | 0.041852 | False | 209.26 | 208.74 | 209.78 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | SPY | SELL | -1 | -1 | -0.15248 | False | 762.4 | 760.49 | 764.31 | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XME | SELL | -2 | -2 | -0.047676 | False | 119.19 | 118.89 | 119.49 | single aggregate hedge order after confirming stock fills |
