# CL v4.3 (_2 stock-observation alignment + veto shipping) Daily Targets: 2026-10-12

- Signal as-of date: 2026-10-09
- Target trading date: 2026-10-12
- AUM: $15,000.00
- Gross stock weight: 54.30%
- Single-name stock weight cap: 5.00%
- Net stock weight: -5.30%
- Gross hedge weight: 29.47%
- Total net weight after hedges: 12.34%
- Estimated turnover from current positions: 7.95%
- Full eligible order turnover: 5.15%
- Today's total child-order turnover: 8.21%
- Stock daily turnover cap: 40.00%
- Hedge turnover policy: uncapped; complete integer hedge targets after stock fills.
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $3.08
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%

## Strategy Notes

- Shipping remains allocated 25%, with the NG jun-Dec carry opposition veto flattening the sleeve whenever its delayed sign opposes the CL tanker position.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.245 | 0.245 | 3675 | 3675 | 8 |
| stock_short_without_hedge | 0.298 | -0.298 | 4470 | -4470 | 10 |
| total_hedge | 0.294696 | 0.176379 | 4420.44 | 2645.69 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.045 | 17.9 | 37.61 | 2026-10-09 | 37.52 | 37.7 | 0.5 | 1.1 |  |  | 2026-10-15 | fixed_hold active from 2026-09-28 to before 2026-10-15 (initial signal 2026-09-25, last same-direction signal 2026-10-09) |
| bwt | TECK | 0.015 | 3.3 | 68.05 | 2026-10-09 | 67.88 | 68.22 | 0.9 | 0.7 |  |  | 2026-10-15 | fixed_hold active from 2026-09-28 to before 2026-10-15 (initial signal 2026-09-25, last same-direction signal 2026-10-09) |
| chemical | DOW | -0.05 | -26.4 | 28.42 | 2026-10-09 | 28.35 | 28.49 | 0.3 | 1.2 |  |  | 2026-11-10 | fixed_hold active from 2026-04-20 to before 2026-11-10 (initial signal 2026-04-17, last same-direction signal 2026-10-09) |
| chemical | LYB | -0.05 | -12.5 | 60.03 | 2026-10-09 | 59.88 | 60.18 | -0 | 1.2 |  |  | 2026-11-10 | fixed_hold active from 2026-04-20 to before 2026-11-10 (initial signal 2026-04-17, last same-direction signal 2026-10-09) |
| chemical | WLK | -0.05 | -12 | 62.29 | 2026-10-09 | 62.13 | 62.45 | 0.8 | 0.7 |  |  | 2026-11-10 | fixed_hold active from 2026-04-20 to before 2026-11-10 (initial signal 2026-04-17, last same-direction signal 2026-10-09) |
| chemical | CE | -0.028 | -9.3 | 45.02 | 2026-10-09 | 44.91 | 45.13 | 0.9 | 1 |  |  | 2026-11-10 | fixed_hold active from 2026-04-20 to before 2026-11-10 (initial signal 2026-04-17, last same-direction signal 2026-10-09) |
| chemical | EMN | -0.028 | -6.7 | 62.69 | 2026-10-09 | 62.53 | 62.85 | 1 | 0.2 |  |  | 2026-11-10 | fixed_hold active from 2026-04-20 to before 2026-11-10 (initial signal 2026-04-17, last same-direction signal 2026-10-09) |
| chemical | HUN | -0.028 | -51.6 | 8.14 | 2026-10-09 | 8.12 | 8.16 | 1.4 | 0.7 |  |  | 2026-11-10 | fixed_hold active from 2026-04-20 to before 2026-11-10 (initial signal 2026-04-17, last same-direction signal 2026-10-09) |
| chemical | AVNT | -0.014 | -5.6 | 37.79 | 2026-10-09 | 37.7 | 37.88 | 1.1 | -0 |  |  | 2026-11-10 | fixed_hold active from 2026-04-20 to before 2026-11-10 (initial signal 2026-04-17, last same-direction signal 2026-10-09) |
| cro | MPC | 0.02 | 0.7 | 455.03 | 2026-10-09 | 453.89 | 456.17 | -0.1 | 0 |  |  |  | continuous hysteresis sign active |
| cro | VLO | 0.015 | 0.5 | 433.75 | 2026-10-09 | 432.67 | 434.83 | -0.3 | 0 |  |  |  | continuous hysteresis sign active |
| psx_ref\|cro | PSX | 0.05 | 2.7 | 278.18 | 2026-10-09 | 277.48 | 278.88 | -0 | 0.8 |  |  | 2026-10-15 | fixed_hold active from 2026-10-08 to before 2026-10-15 (initial signal 2026-10-07, last same-direction signal 2026-10-09)\|continuous hysteresis sign active |
| refiner | DK | 0.05 | 10.1 | 74.51 | 2026-10-09 | 74.32 | 74.7 | 0.2 | 1.3 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | PBF | 0.03 | 5.3 | 84.27 | 2026-10-09 | 84.06 | 84.48 | 0 | 1.7 |  |  |  | 5d rolling-mean band_hysteresis active |
| refiner | DINO | 0.02 | 2.5 | 121.3 | 2026-10-09 | 121 | 121.6 | 0.1 | 1 |  |  |  | 5d rolling-mean band_hysteresis active |
| services | FTI | -0.02 | -4.3 | 69.57 | 2026-10-09 | 69.4 | 69.74 | 0.6 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | SLB | -0.02 | -6.1 | 48.95 | 2026-10-09 | 48.83 | 49.07 | 1.1 | 1 |  |  |  | continuous hysteresis sign active |
| services | HAL | -0.01 | -4.6 | 32.55 | 2026-10-09 | 32.47 | 32.63 | 0.6 | 1.2 |  |  |  | continuous hysteresis sign active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | 0.161022 | 3.10226 | 778.57 | 2026-10-09 | 776.624 | 780.516 |
| XLE | 0.0745158 | 17.1748 | 65.08 | 2026-10-09 | 64.9173 | 65.2427 |
| XME | -0.0591582 | -8.34389 | 106.35 | 2026-10-09 | 106.084 | 106.616 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | cro | MPC | BUY | 1 | 1 | 0.0303353 | False |  | 455.03 | 2026-10-09 | 453.892 | 456.168 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | cro | VLO | BUY | 1 | 1 | 0.0289167 | False |  | 433.75 | 2026-10-09 | 432.666 | 434.834 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | psx_ref\|cro | PSX | BUY | 1 | 1 | 0.0185453 | False |  | 278.18 | 2026-10-09 | 277.485 | 278.875 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | XLE | SELL | -1 | -1 | -0.00433867 | False |  | 65.08 | 2026-10-09 | 64.9173 | 65.2427 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |


## Strategy changes and allocation notes

- CRO (crack refiner-only) added effective 2026-10-06: 10% allocation from unused CL capacity. CL AUM remains $15,000; existing sleeve weights are NOT reduced or renormalized.
- CRO stocks: VLO/MPC/PSX = 30/40/30%; crack_03; signal lookback 30 sessions; volatility lookback 30 (minimum 20); no signal smoothing; balance=0.5 (maximum CRO stock gross 5% of CL AUM).
- CRO explicit hedge is SPY ONLY, not XLE. Preserve component hedge ownership when PSX overlaps existing sleeves; net single-name cap and execution constraints still apply.
- This addition is refiner-only CRO, NOT the refiner-producer CRP, refiner-VLCC CRV, or refiner-chemical CRC research strategies.
- CRO stock target state for this package: active. Flat CRO must not create reallocation trades under identical inputs.
- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.
- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.
- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.
## Operator beta decision — 2026-10-09

Legacy daily-beta method is selected for this session pending further research. Cached-beta targets are comparison-only, not broker instructions. Cached research comparison FAILED and is not validated; no stock-invariance comparison is available. Legacy generation completed its normal validation independently. Research failure: Command '['uv', 'run', 'python', '/Users/chenxu/Work/comm-ls/scripts/generate_metals_cached_beta_daily_targets.py', '--aum', '5000', '--as-of', '2026-10-09', '--target-date', '2026-10-12', '--current-positions', '/Users/chenxu/Work/comm-ls/stats/2026-10-09/metals_positions_attributed.csv', '--output-dir', '/var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-10-12-rn3jt1yc/cached/targets-metals']' returned non-zero exit status 1.. Previous production files were backed up before publication. Cached comparison: /var/folders/g9/s0dqxvt557l2gr1n1d9z_r7m0000gn/T/comm-ls-beta-2026-10-12-rn3jt1yc/cached/targets-cl/2026-10-12. Agriculture's existing component-specific cached beta is unchanged.

## Approved allocation changes — effective 2026-10-12

Metals AUM remains $5,000: gap 15%, accel 20%, SCO-vol 25%, copper 10%, miners 25%; alloys remains suspended with 5% cash. Crypto separate-account AUM is $4,000 (+33.33% vs $3,000), review on 2026-11-12 with no automatic increase or rollback. CL $15,000 and Agriculture $2,000 are unchanged; main AUM remains $22,000. Legacy daily beta remains the live method; allocation migration turnover is not a signal change. Use confirmed fills for ETF orders and attribution. See docs/live_allocation_change_2026-10-12.md.
