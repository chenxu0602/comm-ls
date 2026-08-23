# Metals production-start notes: 2026-08-24

- Production AUM: USD 5,000.
- This is the first IB production target for the standalone Metals/mining
  alpha satellite. Earlier `targets-metals` packages were simulation/shadow
  artifacts and are not part of the historical actual-IB strategy record.
- Data version: `_2` (`carry_data_2` and `_2` feature-return caches).
- Portfolio revision: six sleeves at 15%/25%/10%/10%/15%/25%.
- Added `sco_vol_miners` using SCO `M0_ret_std_20`, lagged 70th-percentile
  low-volatility gate, positive 20-observation change and a two-session hold.
- Aggregate single-name cap increased from 10% to 12%.
- Research return remains `residual_return_mktsec_w12m`.
- When combined with CL v4.2 in the shared IB account, do not trade standalone
  order files. Preserve each strategy's sleeve-aware rounding and child cap,
  sum `rounded_trade_shares` by ticker, and apply the account-level cap on USD
  20,000. If constrained, CL has implementation priority over new Metals risk.
- The complete operating and attribution procedure is in
  `docs/shared_account_cl_metals_workflow.md`.
