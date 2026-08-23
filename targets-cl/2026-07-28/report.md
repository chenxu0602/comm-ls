# CL v3.2 Daily Targets: 2026-07-28

- Signal as-of date: 2026-07-27
- Target trading date: 2026-07-28
- AUM: $15,000.00
- Gross stock weight: 66.30%
- Single-name stock weight cap: 5.00%
- Net stock weight: -7.30%
- Gross hedge weight: 36.16%
- Total net weight after hedges: 11.20%
- Estimated turnover from current positions: 61.35%
- Full eligible order turnover: 54.83%
- Today's child-order turnover: 31.50%
- Daily turnover cap: 40.00%
- Execution policy: next_session_vwap_30m (09:30-10:00 America/New_York)
- Estimated stock/hedge execution cost: $11.81
- Cost assumptions: stock 25.0bps, hedge 25.0bps one-way
- Trade buffer: 0.25%
- Revision audit: see `targets/2026-07-28/notes.md` for the algorithm changes
  that increased today's turnover and order count.

## Exposure Summary

| bucket | gross_weight | signed_weight | gross_notional_usd | signed_notional_usd | instrument_count |
| --- | --- | --- | --- | --- | --- |
| stock_long_without_hedge | 0.295 | 0.295 | 4425 | 4425 | 10 |
| stock_short_without_hedge | 0.368 | -0.368 | 5520 | -5520 | 11 |
| total_hedge | 0.361574 | 0.185005 | 5423.61 | 2775.08 | 3 |

## Active Stock Targets

| component | instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps | market_beta | sector_beta | corporate_event_date | corporate_event_policy | estimated_liquidate_date | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| bwt | ERO | 0.03 | 17.2 | 26.2 | 2026-07-27 | 26.13 | 26.27 | 0.5 | 1 |  |  | 2026-07-30 | fixed_hold active from 2026-07-23 to before 2026-07-30 (initial signal 2026-07-22, last same-direction signal 2026-07-22) |
| bwt | TECK | 0.03 | 7.5 | 59.75 | 2026-07-27 | 59.6 | 59.9 | 0.9 | 0.7 |  |  | 2026-07-30 | fixed_hold active from 2026-07-23 to before 2026-07-30 (initial signal 2026-07-22, last same-direction signal 2026-07-22) |
| chemical | DOW | -0.05 | -26.1 | 28.75 | 2026-07-27 | 28.68 | 28.82 | 0.5 | 1.2 |  |  | 2026-08-26 | fixed_hold active from 2026-04-21 to before 2026-08-26 (initial signal 2026-04-20, last same-direction signal 2026-07-27) |
| chemical | LYB | -0.05 | -12.8 | 58.62 | 2026-07-27 | 58.47 | 58.77 | 0.1 | 1.2 |  |  | 2026-08-26 | fixed_hold active from 2026-04-21 to before 2026-08-26 (initial signal 2026-04-20, last same-direction signal 2026-07-27) |
| chemical | WLK | -0.05 | -10.4 | 72.33 | 2026-07-27 | 72.15 | 72.51 | 0.8 | 0.8 |  |  | 2026-08-26 | fixed_hold active from 2026-04-21 to before 2026-08-26 (initial signal 2026-04-20, last same-direction signal 2026-07-27) |
| chemical | CE | -0.028 | -9.5 | 44.4 | 2026-07-27 | 44.29 | 44.51 | 0.9 | 1 |  |  | 2026-08-26 | fixed_hold active from 2026-04-21 to before 2026-08-26 (initial signal 2026-04-20, last same-direction signal 2026-07-27) |
| chemical | EMN | -0.028 | -6.2 | 67.68 | 2026-07-27 | 67.51 | 67.85 | 1.2 | 0.4 |  |  | 2026-08-26 | fixed_hold active from 2026-04-21 to before 2026-08-26 (initial signal 2026-04-20, last same-direction signal 2026-07-27) |
| chemical | HUN | -0.028 | -35.8 | 11.74 | 2026-07-27 | 11.71 | 11.77 | 1.7 | 0.8 |  |  | 2026-08-26 | fixed_hold active from 2026-04-21 to before 2026-08-26 (initial signal 2026-04-20, last same-direction signal 2026-07-27) |
| chemical | AVNT | -0.014 | -5.8 | 36.44 | 2026-07-27 | 36.35 | 36.53 | 1.1 | -0 |  |  | 2026-08-26 | fixed_hold active from 2026-04-21 to before 2026-08-26 (initial signal 2026-04-20, last same-direction signal 2026-07-27) |
| fuel | CASY | 0.024 | 0.4 | 853.38 | 2026-07-27 | 851.25 | 855.51 | -0 | 0 |  |  | 2026-08-04 | fixed_hold active from 2026-03-05 to before 2026-08-04 (initial signal 2026-03-04, last same-direction signal 2026-07-27) |
| fuel | MUSA | 0.016 | 0.4 | 610.44 | 2026-07-27 | 608.91 | 611.97 | -0.5 | 0 |  |  | 2026-08-04 | fixed_hold active from 2026-03-05 to before 2026-08-04 (initial signal 2026-03-04, last same-direction signal 2026-07-27) |
| metals | ATI | 0.05 | 3.9 | 192.64 | 2026-07-27 | 192.16 | 193.12 | 1 | 0.3 |  |  |  | continuous hysteresis sign active |
| metals | CRS | 0.045 | 1.2 | 580.25 | 2026-07-27 | 578.8 | 581.7 | 0.9 | 0.3 |  |  |  | continuous hysteresis sign active |
| psx_ref | PSX | -0.04 | -2.9 | 207.82 | 2026-07-27 | 207.3 | 208.34 | 0.1 | 1.1 |  |  | 2026-08-04 | fixed_hold active from 2026-07-28 to before 2026-08-04 (initial signal 2026-07-27, last same-direction signal 2026-07-27) |
| refiner | DK | -0.032 | -7.4 | 64.44 | 2026-07-27 | 64.28 | 64.6 | 0.1 | 1.3 |  |  |  | 5d rolling-mean hysteresis active |
| refiner | DINO | -0.024 | -4 | 90.78 | 2026-07-27 | 90.55 | 91.01 | 0.2 | 1 |  |  |  | 5d rolling-mean hysteresis active |
| refiner | PBF | -0.024 | -5.7 | 62.76 | 2026-07-27 | 62.6 | 62.92 | -0 | 1.7 |  |  |  | 5d rolling-mean hysteresis active |
| services | FTI | 0.025 | 5 | 75.04 | 2026-07-27 | 74.85 | 75.23 | 0.6 | 0.8 |  |  |  | continuous hysteresis sign active |
| services | HAL | 0.025 | 11.7 | 32.13 | 2026-07-27 | 32.05 | 32.21 | 0.6 | 1.2 |  |  |  | continuous hysteresis sign active |
| services | OII | 0.025 | 7.2 | 52.17 | 2026-07-27 | 52.04 | 52.3 | 1.1 | 1 |  |  |  | continuous hysteresis sign active |
| services | SLB | 0.025 | 7.3 | 51.53 | 2026-07-27 | 51.4 | 51.66 | 1 | 1 |  |  |  | continuous hysteresis sign active |

## Corporate Event Decisions

No reviewed corporate events in the next 31 calendar days.

## Hedge Targets

| instrument | target_weight | target_shares | previous_close | previous_close_date | lower_25bps | upper_25bps |
| --- | --- | --- | --- | --- | --- | --- |
| SPY | -0.0066331 | -0.13462 | 739.09 | 2026-07-27 | 737.242 | 740.938 |
| XLE | 0.273289 | 70.2423 | 58.36 | 2026-07-27 | 58.2141 | 58.5059 |
| XME | -0.0816512 | -11.8783 | 103.11 | 2026-07-27 | 102.852 | 103.368 |

## Order Plan

| instrument_type | component | instrument | execution_action | full_rounded_trade_shares | rounded_trade_shares | execution_trade_weight | direct_reversal_blocked | corporate_event_policy | previous_close | previous_close_date | lower_25bps | upper_25bps | manual_price_note | execution_instruction |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| stock | bwt | TECK | BUY | 16 | 8 | 0.0318667 | True |  | 59.75 | 2026-07-27 | 59.6006 | 59.8994 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | bwt | ERO | BUY | 34 | 17 | 0.0296933 | True |  | 26.2 | 2026-07-27 | 26.1345 | 26.2655 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | psx_ref | PSX | BUY | 1 | 1 | 0.0138547 | False |  | 207.82 | 2026-07-27 | 207.3 | 208.34 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | services | FTI | BUY | 3 | 2 | 0.0100053 | False |  | 75.04 | 2026-07-27 | 74.8524 | 75.2276 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | services | HAL | BUY | 6 | 4 | 0.008568 | False |  | 32.13 | 2026-07-27 | 32.0497 | 32.2103 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | services | SLB | BUY | 3 | 2 | 0.00687067 | False |  | 51.53 | 2026-07-27 | 51.4012 | 51.6588 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | services | OII | BUY | 3 | 2 | 0.006956 | False |  | 52.17 | 2026-07-27 | 52.0396 | 52.3004 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | DK | BUY | 2 | 2 | 0.008592 | False |  | 64.44 | 2026-07-27 | 64.2789 | 64.6011 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | DINO | BUY | 1 | 1 | 0.006052 | False |  | 90.78 | 2026-07-27 | 90.553 | 91.0069 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | refiner | PBF | BUY | 1 | 1 | 0.004184 | False |  | 62.76 | 2026-07-27 | 62.6031 | 62.9169 | buy: lower_25bps is patient bid; upper_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| stock | chemical | LYB | SELL | -1 | -1 | -0.003908 | False |  | 58.62 | 2026-07-27 | 58.4734 | 58.7665 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | execute once; no same-day reversal or duplicate order |
| hedge | hedge | SPY | SELL | -3 | -2 | -0.0985453 | False |  | 739.09 | 2026-07-27 | 737.242 | 740.938 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XME | SELL | -16 | -4 | -0.027496 | True |  | 103.11 | 2026-07-27 | 102.852 | 103.368 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
| hedge | hedge | XLE | SELL | -20 | -15 | -0.05836 | False |  | 58.36 | 2026-07-27 | 58.2141 | 58.5059 | sell: upper_25bps is patient offer; lower_25bps is 25bps chase reference | single aggregate hedge order after confirming stock fills |
