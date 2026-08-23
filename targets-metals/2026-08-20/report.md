# Metals Daily Targets: 2026-08-20

- Signal as-of date: 2026-08-19
- Target trading date: 2026-08-20
- AUM: $5,000.00
- Gross stock weight: 57.32%
- Single-name cap after sleeve aggregation: 10.00%
- Net stock weight: 57.32%
- Gross hedge weight: 66.58%
- Total net weight after hedges: -9.26%
- Turnover from Metals-attributed current positions: 123.90%
- Full eligible order turnover: 123.90%
- Today's child-order turnover: 39.54%
- Daily turnover cap: 40.00%
- Estimated execution cost: $4.94

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
| stock_long_without_hedge | 0.573182 | 0.573182 | 2865.91 | 2865.91 | 8 |
| stock_short_without_hedge | 0 | 0 | 0 | 0 | 0 |
| total_hedge | 0.665821 | -0.665821 | 3329.11 | -3329.11 | 2 |

## Active Targets

| instrument_type | component | instrument | target_weight | target_shares | previous_close | market_beta | sector_beta | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | sco_specialty_alloys | ATI | 0.08 | 1.9 | 215.99 | 1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-1.63114;drawdown_63d=-1.10838;realized_vol_63d=-0.633404 |
| stock | sco_vol_gc_hg_accel_miners|miners | BHP | 0.1 | 5.4 | 92.29 | 0.6 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.25457;q_short_entry=2.25457;q_short_exit=1.44471;vol_diff=-0.133571;accel=2.43351; aggregate BHP capped at 10.0%|persistent_binary active; feature=-0.0239183; aggregate BHP capped at 10.0% |
| stock | sco_specialty_alloys | CRS | 0.08 | 0.8 | 509.96 | 1 | 0.3 | sco_specialty_alloys_hysteresis active; ret_63d=-1.63114;drawdown_63d=-1.10838;realized_vol_63d=-0.633404 |
| stock | miners | FSUGY | 0.040909 | 7.9 | 25.85 | 0.6 | 0.3 | persistent_binary active; feature=-0.0239183 |
| stock | sco_specialty_alloys | HWM | 0.04 | 0.7 | 283.48 | 0.9 | 0.1 | sco_specialty_alloys_hysteresis active; ret_63d=-1.63114;drawdown_63d=-1.10838;realized_vol_63d=-0.633404 |
| stock | sco_vol_gc_hg_accel_miners|miners | RIO | 0.1 | 5 | 100.44 | 0.3 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.25457;q_short_entry=2.25457;q_short_exit=1.44471;vol_diff=-0.133571;accel=2.43351; aggregate RIO capped at 10.0%|persistent_binary active; feature=-0.0239183; aggregate RIO capped at 10.0% |
| stock | sco_vol_gc_hg_accel_miners|miners | SCCO | 0.083636 | 2.1 | 194.68 | 0.8 | 0.9 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.25457;q_short_entry=2.25457;q_short_exit=1.44471;vol_diff=-0.133571;accel=2.43351|persistent_binary active; feature=-0.0239183 |
| stock | sco_vol_gc_hg_accel_miners|miners | VALE | 0.048636 | 17.5 | 13.9 | 0.3 | 0.5 | sco_vol_gc_hg_combo active; sco_vol=1.20714;q_long_exit=2.25457;q_short_entry=2.25457;q_short_exit=1.44471;vol_diff=-0.133571;accel=2.43351|persistent_binary active; feature=-0.0239183 |
| hedge | hedge | SPY | -0.407276 | -2.6 | 769.06 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |
| hedge | hedge | XME | -0.258546 | -11 | 117.07 |  |  | explicit two-factor beta hedge; aggregate after confirmed stock fills |

## Corporate Event Decisions

No reviewed events in the next 31 days.

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | previous_close | lower_25bps | upper_25bps | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | miners | FSUGY | BUY | 8 | 3 | 0.01551 | False | 25.85 | 25.79 | 25.91 | execute once; no same-day reversal or duplicate order |
| stock | sco_specialty_alloys | ATI | BUY | 2 | 1 | 0.043198 | False | 215.99 | 215.45 | 216.53 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners|miners | BHP | BUY | 5 | 2 | 0.036916 | False | 92.29 | 92.06 | 92.52 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners|miners | RIO | BUY | 5 | 1 | 0.020088 | False | 100.44 | 100.19 | 100.69 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners|miners | SCCO | BUY | 2 | 1 | 0.038936 | False | 194.68 | 194.19 | 195.17 | execute once; no same-day reversal or duplicate order |
| stock | sco_vol_gc_hg_accel_miners|miners | VALE | BUY | 17 | 6 | 0.01668 | False | 13.9 | 13.87 | 13.93 | execute once; no same-day reversal or duplicate order |
| hedge | hedge | SPY | SELL | -3 | -1 | -0.153812 | False | 769.06 | 767.14 | 770.98 | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XME | SELL | -11 | -3 | -0.070242 | False | 117.07 | 116.78 | 117.36 | single aggregate hedge order after confirming stock fills |
