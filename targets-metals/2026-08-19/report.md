# Metals Daily Targets: 2026-08-19

- Signal as-of date: 2026-08-18
- Target trading date: 2026-08-19
- AUM: $10,000.00
- Gross stock weight: 48.18%
- Single-name cap after sleeve aggregation: 10.00%
- Net stock weight: 40.00%
- Gross hedge weight: 48.16%
- Total net weight after hedges: -8.16%
- Turnover from Metals-attributed current positions: 96.34%
- Full eligible order turnover: 96.34%
- Today's child-order turnover: 39.53%
- Daily turnover cap: 40.00%
- Estimated execution cost: $9.88

## Isolation and Execution Notes

- Signal construction is fail-closed on the `_2` cache/carry pipeline; it does not read the current non-`_2` signal cache.
- Required feature observations must be no more than 3 calendar days old.
- Current positions must be Metals-attributed, not a full shared IB account export.
- Execute stock orders once in the first 30 minutes; aggregate SPY/XME hedge orders only after confirming stock fills.
- Direct same-day reversals are flattened first by the child-order policy.

## Pinned Signal Inputs

- metals_cache: `data/cache/feature_return/METALS-multi_return_2.parquet`; latest n/a
- gc_cache: `data/cache/feature_return/GC-multi_return_2.parquet`; latest n/a
- sco_cache: `data/cache/feature_return/SCO-multi_return_2.parquet`; latest n/a
- carry_dir: `data/comm/carry_data_2`; latest n/a
- commodity_dir: `data/comm`; latest n/a

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.440909 | 0.440909 | 4409.09 | 4409.09 | 7 |
| stock_short_without_hedge | 0.040909 | -0.040909 | 409.09 | -409.09 | 1 |
| total_hedge | 0.481602 | -0.481602 | 4816.02 | -4816.02 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | sco_specialty_alloys | ATI | 0.08 | 3.5 | 226.46 | 1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-1.95002;drawdown_63d=-1.32043;realized_vol_63d=-0.620822 |
| stock | sco_vol_gc_hg_accel_miners|miners | BHP | 0.064091 | 7.2 | 89.09 | 0.6 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.25529;q_short_entry=2.25529;q_short_exit=1.44543;vol_diff=-0.281429;accel=1.93935|persistent_binary active; feature=-0.0176909 |
| stock | sco_specialty_alloys | CRS | 0.08 | 1.5 | 531.96 | 1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-1.95002;drawdown_63d=-1.32043;realized_vol_63d=-0.620822 |
| stock | miners | FSUGY | -0.040909 | -16.4 | 24.94 | 0.7 | 0.3 | persistent_binary active; feature=-0.0176909 |
| stock | sco_specialty_alloys | HWM | 0.04 | 1.4 | 292.65 | 0.8 | 0.1 | sco_specialty_alloys_hysteresis active; ret_63d=-1.95002;drawdown_63d=-1.32043;realized_vol_63d=-0.620822 |
| stock | sco_vol_gc_hg_accel_miners|miners | RIO | 0.099091 | 10.2 | 96.69 | 0.3 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.25529;q_short_entry=2.25529;q_short_exit=1.44543;vol_diff=-0.281429;accel=1.93935|persistent_binary active; feature=-0.0176909 |
| stock | sco_vol_gc_hg_accel_miners|miners | SCCO | 0.056364 | 3 | 187.8 | 0.9 | 0.9 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.25529;q_short_entry=2.25529;q_short_exit=1.44543;vol_diff=-0.281429;accel=1.93935|persistent_binary active; feature=-0.0176909 |
| stock | sco_vol_gc_hg_accel_miners|miners | VALE | 0.021364 | 15.6 | 13.68 | 0.3 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.25529;q_short_entry=2.25529;q_short_exit=1.44543;vol_diff=-0.281429;accel=1.93935|persistent_binary active; feature=-0.0176909 |
| hedge | hedge | SPY | -0.296546 | -3.9 | 767.45 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | -0.185056 | -16.3 | 113.63 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | miners | FSUGY | SELL | -16 | -7 | -0.017458 | False | 24.94 | 24.88 | 25 | execute once; no same-day reversal or duplicate order |
| stock | sco_specialty_alloys | ATI | BUY | 4 | 2 | 0.045292 | False | 226.46 | 225.89 | 227.03 | execute once; no same-day reversal or duplicate order |
| stock | sco_specialty_alloys | CRS | BUY | 2 | 1 | 0.053196 | False | 531.96 | 530.63 | 533.29 | execute once; no same-day reversal or duplicate order |
| stock | sco_specialty_alloys | HWM | BUY | 1 | 1 | 0.029265 | False | 292.65 | 291.92 | 293.38 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners|miners | BHP | BUY | 7 | 3 | 0.026727 | False | 89.09 | 88.87 | 89.31 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners|miners | RIO | BUY | 10 | 4 | 0.038676 | False | 96.69 | 96.45 | 96.93 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners|miners | SCCO | BUY | 3 | 1 | 0.01878 | False | 187.8 | 187.33 | 188.27 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners|miners | VALE | BUY | 16 | 7 | 0.009576 | False | 13.68 | 13.65 | 13.71 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | SPY | SELL | -4 | -1 | -0.076745 | False | 767.45 | 765.53 | 769.37 | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XME | SELL | -16 | -7 | -0.079541 | False | 113.63 | 113.35 | 113.91 | single aggregate hedge order after confirming stock fills |
