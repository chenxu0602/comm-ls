# Metals Daily Targets: 2026-10-01

- Signal as-of date: 2026-09-30
- Target trading date: 2026-10-01
- AUM: $5,000.00
- Gross stock weight: 35.00%
- Single-name cap after sleeve aggregation: 12.00%
- Net stock weight: -35.00%
- Gross hedge weight: 37.89%
- Total net weight after hedges: 2.89%
- Turnover from Metals-attributed current positions: 19.32%
- Full eligible order turnover: 14.43%
- Today's total child-order turnover: 16.51%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Estimated execution cost: $2.06

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
| stock_long_without_hedge | 0 | 0 | 0 | 0 | 0 |
| stock_short_without_hedge | 0.35 | -0.35 | 1750 | -1750 | 5 |
| total_hedge | 0.378936 | 0.378936 | 1894.68 | 1894.68 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | hg_gc_gap_gc_carry_iron\|sco_vol_miners\|miners | BHP | -0.11 | -6.5 | 84.84 | 0.6 | 0.5 | dual_feature_hysteresis active; hg_gap=0.0423125;gc_carry=1.20983\|sco_vol_regime_pulse active; sco_vol=1.21786;vol_quantile=1.95071;vol_diff=-0.0621429\|persistent_binary active; feature=0.0423125 |
| stock | hg_gc_gap_gc_carry_iron\|miners | FSUGY | -0.07 | -15.4 | 22.69 | 0.6 | 0.3 | dual_feature_hysteresis active; hg_gap=0.0423125;gc_carry=1.20983\|persistent_binary active; feature=0.0423125 |
| stock | hg_gc_gap_gc_carry_iron\|sco_vol_miners\|miners | RIO | -0.065 | -3.5 | 94.17 | 0.3 | 0.5 | dual_feature_hysteresis active; hg_gap=0.0423125;gc_carry=1.20983\|sco_vol_regime_pulse active; sco_vol=1.21786;vol_quantile=1.95071;vol_diff=-0.0621429\|persistent_binary active; feature=0.0423125 |
| stock | sco_vol_miners\|copper_miner\|miners | SCCO | -0.07 | -1.7 | 202.64 | 0.7 | 0.9 | sco_vol_regime_pulse active; sco_vol=1.21786;vol_quantile=1.95071;vol_diff=-0.0621429\|copper_energy_terms_of_trade active; hg_cl_ratio=0.756848;ho_ret=0.0387302;hg_mv_5=0.753727;hg_mv_200=0.836227;hg_mv_diff=-0.0825;hg_threshold=0.010782;ho_momentum_20d=0.0450457;ho_threshold=0.030418\|persistent_binary active; feature=0.0423125 |
| stock | hg_gc_gap_gc_carry_iron\|sco_vol_miners\|miners | VALE | -0.035 | -13 | 13.41 | 0.2 | 0.5 | dual_feature_hysteresis active; hg_gap=0.0423125;gc_carry=1.20983\|sco_vol_regime_pulse active; sco_vol=1.21786;vol_quantile=1.95071;vol_diff=-0.0621429\|persistent_binary active; feature=0.0423125 |
| hedge | hedge | SPY | 0.188514 | 1.2 | 762.63 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | 0.190422 | 9.2 | 103.56 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | hg_gc_gap_gc_carry_iron\|sco_vol_miners\|miners | BHP | BUY | 1 | 1 | 0.016968 | False | 84.84 | 84.63 | 85.05 | execute once; no same-day reversal or duplicate order |
| stock | hg_gc_gap_gc_carry_iron\|sco_vol_miners\|miners | RIO | BUY | 3 | 3 | 0.056502 | False | 94.17 | 93.93 | 94.41 | execute once; no same-day reversal or duplicate order |
| stock | hg_gc_gap_gc_carry_iron\|sco_vol_miners\|miners | VALE | BUY | 11 | 11 | 0.029502 | False | 13.41 | 13.38 | 13.44 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XME | SELL | -3 | -3 | -0.062136 | False | 103.56 | 103.3 | 103.82 | single aggregate hedge order after confirming stock fills |
