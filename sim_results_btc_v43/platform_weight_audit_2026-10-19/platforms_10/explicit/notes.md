## Beta algorithm change: notebook residual cached beta

- beta_mode: `notebook_residual_cached_beta_v1`. Source: `data/processed/equity_processed.parquet`.
- Uses the already-computed beta for each notebook residual: `market_beta_mktsec_w12m` / `sector_beta_mktsec_w12m`, or `market_beta_mkt_w12m` for SPY-only sleeves.
- Source pipeline default: 12-month weekly returns, exponential weighting (3-month half-life), monthly updates. No new daily 252-session regression.
- CL CRO and Crypto use SPY only; other CL sleeves and Metals keep their existing residual-specific sector mapping. Shared core: `comm_ls.residual_beta_hedge`, also used by the new explicit backtest.
- Exact beta values, source dates and estimation cutoffs are in `beta_sources.csv`. Only observations known by the signal as-of are used.
- The beta change can produce ETF migration orders even when the stock signal is unchanged. Compare with the legacy package before execution.
- Prices, integer rounding, caps, trade buffers and intraday fills can still differ from implicit research PnL. At monthly beta updates the prior-close explicit hedge and the return-day residual beta can differ by one session; the new audit reports that timing gap separately.

Frozen notebook stock signals and weights, including CRO overlapping PSX. The saved close-dated positions are lagged once for PnL, preserving the notebook delay. Continuous PnL uses adjusted log returns; integer PnL uses adjusted price differences. Integer rows are close-fill rounding diagnostics, not the live 30-minute VWAP/child-cap simulator. Implicit follows notebook missing-return handling: CL omits all-missing residual sessions; Metals/Crypto shift and charge costs on each ticker's valid residual calendar. implicit_missing_sessions.csv discloses active omitted return rows; explicit raw-stock/ETF PnL retains those sessions when prices exist. No actual-IB counterfactual, borrow fees or separate dividend ledger is modeled. Legacy comparison uses the old estimator aligned to its live as-of clock.
