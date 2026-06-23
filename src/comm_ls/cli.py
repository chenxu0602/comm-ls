from __future__ import annotations

import argparse
from pathlib import Path

from comm_ls.backtest import run_score_backtest_from_paths
from comm_ls.basket_cluster_risk import build_basket_cluster_risk_audit_from_paths
from comm_ls.beta import (
    DEFAULT_COMMODITY_BETA_RETURN_COLUMN,
    DEFAULT_COMMODITY_BETA_SYMBOLS,
    DEFAULT_PRIMARY_PROCESSED_BETA_VARIATION,
    DEFAULT_PROCESSED_BETA_VARIATIONS,
    build_equity_beta_returns_from_paths,
    build_equity_processed_dataset_from_paths,
)
from comm_ls.candidates import build_candidate_signals_from_paths
from comm_ls.commodity import build_commodity_signal_frame, load_carry_directory, write_frame
from comm_ls.commodity_research import research_commodity_features_from_paths
from comm_ls.cross_product_summary import (
    DEFAULT_DIRECT_OIL_ROLES,
    summarize_cross_product_clusters_from_paths,
)
from comm_ls.curve_diagnostics import build_matrix_curve_diagnostics_from_paths
from comm_ls.equity import download_yfinance_prices
from comm_ls.edgar import build_filing_index, download_filings, fetch_company_tickers, extract_form_sections
from comm_ls.environment import commodity_environment_similarity_from_paths
from comm_ls.discovery import (
    audit_commodity_universe_from_paths,
    build_commodity_sensitivity_matrix_from_paths,
    build_daily_feature_return_cache_from_paths,
    build_discovered_commodity_universe_from_paths,
    classify_commodity_universe_tiers_from_paths,
    write_quarterly_stock_feature_matrix_files_from_paths,
)
from comm_ls.feature_basket import (
    build_feature_trade_candidates_from_paths,
    run_feature_basket_backtest_from_paths,
)
from comm_ls.feature_matrix import build_stock_feature_matrix_cache_from_paths, build_stock_feature_matrix_from_paths
from comm_ls.forecast import build_commodity_stock_forecast_study_from_paths
from comm_ls.fundamentals import (
    build_agriculture_fundamental_events_from_paths,
    build_commodity_confirmation_events_from_paths,
    build_fundamental_snapshot_from_paths,
)
from comm_ls.mechanism_alignment import build_mechanism_alignment_audit_from_paths
from comm_ls.mechanism_state import build_mechanism_state_model_from_paths
from comm_ls.portfolio import (
    build_long_index_hedge_weights,
    build_long_short_weights,
    load_scores,
    load_shortability,
    write_weights,
)
from comm_ls.precision import build_precision_event_candidates_from_paths
from comm_ls.reaction import build_feature_reaction_study_from_paths
from comm_ls.research_quality import (
    audit_exposure_taxonomy_from_paths,
    audit_forecast_from_paths,
    audit_nonlinear_commodity_beta_from_paths,
    audit_sensitivity_falsification_from_paths,
    consolidate_candidate_signals_from_paths,
    group_activation_scores_from_paths,
    load_reviewed_features,
    registry_turnover_from_paths,
    review_candidate_taxonomy_from_paths,
    reviewed_feature_list,
)
from comm_ls.regime_validity import (
    DEFAULT_REGIME_DIMENSIONS,
    build_regime_conditioned_validity_audit_from_paths,
)
from comm_ls.regime_adversarial import (
    build_basket_regime_adversarial_audit_from_paths,
    build_basket_state_filter_audit_from_paths,
    build_regime_adversarial_audit_from_paths,
)
from comm_ls.selection_backtest import run_quarterly_selection_backtest_from_paths
from comm_ls.selection_path import simulate_selection_path_stability_from_paths
from comm_ls.selection_v3 import (
    review_curve_first_taxonomy_from_paths,
    run_curve_first_oos_from_paths,
    select_curve_first_candidates_from_paths,
)
from comm_ls.signal_decay import build_signal_decay_audit_from_paths
from comm_ls.peer_expansion import build_peer_expansion_from_paths
from comm_ls.macro import build_macro_regime_frame_from_paths
from comm_ls.year_stability import build_year_stability_audit_from_paths
from comm_ls.shortability import build_shortability_from_price_directory
from comm_ls.sensitivity import build_daily_scores_from_paths, build_stock_sensitivity_registry_from_paths
from comm_ls.state_summary import summarize_state_role_clusters_from_paths
from comm_ls.universe import (
    build_broad_quarterly_liquidity_universe,
    build_commodity_quarterly_universes,
    build_quarterly_liquidity_universe,
    get_exposure_universe,
    load_seed_universe,
    write_commodity_quarterly_universe_files,
)


DEFAULT_EXCLUDED_BROAD_UNIVERSE_TICKERS = ["SPY", "XLE", "XME", "GDX", "SIL", "XLU", "MOO", "LIT", "URA", "XHB"]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="comm-ls")
    subparsers = parser.add_subparsers(dest="command", required=True)

    commodity = subparsers.add_parser("build-commodity-signals")
    commodity.add_argument("--input-dir", type=Path, default=Path("data/comm/carry_data"))
    commodity.add_argument("--commodity-dir", type=Path, default=Path("data/comm"))
    commodity.add_argument("--output", type=Path, default=Path("data/processed/commodity_signals.parquet"))
    commodity.add_argument(
        "--no-brent-wti-features",
        action="store_true",
        help="Skip Brent-WTI companion features on CL rows.",
    )

    download = subparsers.add_parser("download-equities")
    download.add_argument("--universe", type=Path, default=Path("config/us_commodity_equity_seed.csv"))
    download.add_argument("--output-dir", type=Path, default=Path("data/equity/yfinance"))
    download.add_argument("--start", default="2000-01-01")
    download.add_argument("--end", default=None)
    download.add_argument("--ticker", action="append", default=None)
    download.add_argument("--limit", type=int, default=None)
    download.add_argument(
        "--auto-adjust",
        action="store_true",
        help="Store adjusted OHLC only. Default stores raw OHLC plus adj_close when yfinance provides it.",
    )

    quarterly = subparsers.add_parser("build-quarterly-universe")
    quarterly.add_argument("--universe", type=Path, default=Path("config/us_commodity_equity_seed.csv"))
    quarterly.add_argument("--prices-dir", type=Path, default=Path("data/equity/yfinance"))
    quarterly.add_argument("--output", type=Path, default=Path("data/processed/quarterly_universe.csv"))
    quarterly.add_argument("--min-price", type=float, default=5.0)
    quarterly.add_argument("--min-adv", type=float, default=5_000_000.0)
    quarterly.add_argument("--lookback-days", type=int, default=63)

    commodity_quarterly = subparsers.add_parser("build-commodity-quarterly-universes")
    commodity_quarterly.add_argument("--exposure-map", type=Path, default=Path("config/commodity_exposure_map.csv"))
    commodity_quarterly.add_argument("--seed-universe", type=Path, default=Path("config/us_commodity_equity_seed.csv"))
    commodity_quarterly.add_argument("--prices-dir", type=Path, default=Path("data/equity/yfinance"))
    commodity_quarterly.add_argument("--commodity", action="append", default=None)
    commodity_quarterly.add_argument("--start", default="2010-01-01")
    commodity_quarterly.add_argument("--end", default=None)
    commodity_quarterly.add_argument("--output-dir", type=Path, default=Path("data/universe"))
    commodity_quarterly.add_argument(
        "--combined-output",
        type=Path,
        default=Path("data/processed/cl_hg_quarterly_universe.csv"),
    )
    commodity_quarterly.add_argument("--min-price", type=float, default=5.0)
    commodity_quarterly.add_argument("--min-adv", type=float, default=5_000_000.0)
    commodity_quarterly.add_argument("--lookback-days", type=int, default=63)
    commodity_quarterly.add_argument("--min-lookback-observations", type=int, default=42)
    commodity_quarterly.add_argument("--min-history-observations", type=int, default=252)
    commodity_quarterly.add_argument("--max-staleness-days", type=int, default=10)
    commodity_quarterly.add_argument("--min-abs-prior-weight", type=float, default=0.0)

    broad_quarterly = subparsers.add_parser("build-broad-quarterly-liquidity-universe")
    broad_quarterly.add_argument("--prices-dir", type=Path, default=Path("data/equity/yfinance"))
    broad_quarterly.add_argument("--seed-universe", type=Path, default=Path("config/us_commodity_equity_seed.csv"))
    broad_quarterly.add_argument("--output", type=Path, default=Path("data/processed/broad_liquid_universe_quarterly.csv"))
    broad_quarterly.add_argument("--start", default="2010-01-01")
    broad_quarterly.add_argument("--end", default=None)
    broad_quarterly.add_argument("--min-price", type=float, default=5.0)
    broad_quarterly.add_argument("--min-adv", type=float, default=5_000_000.0)
    broad_quarterly.add_argument("--lookback-days", type=int, default=63)
    broad_quarterly.add_argument("--min-lookback-observations", type=int, default=42)
    broad_quarterly.add_argument("--min-history-observations", type=int, default=252)
    broad_quarterly.add_argument("--max-staleness-days", type=int, default=10)
    broad_quarterly.add_argument("--exclude-ticker", action="append", default=None)

    pseudo_russell = subparsers.add_parser("build-pseudo-russell1000-universe")
    pseudo_russell.add_argument("--prices-dir", type=Path, default=Path("data/equity/yfinance"))
    pseudo_russell.add_argument("--seed-universe", type=Path, default=Path("config/us_commodity_equity_seed.csv"))
    pseudo_russell.add_argument(
        "--output",
        type=Path,
        default=Path("data/processed/pseudo_russell1000_universe_quarterly.csv"),
    )
    pseudo_russell.add_argument("--start", default="2010-01-01")
    pseudo_russell.add_argument("--end", default=None)
    pseudo_russell.add_argument("--max-names", type=int, default=1000)
    pseudo_russell.add_argument("--min-price", type=float, default=5.0)
    pseudo_russell.add_argument("--min-adv", type=float, default=5_000_000.0)
    pseudo_russell.add_argument("--lookback-days", type=int, default=63)
    pseudo_russell.add_argument("--min-lookback-observations", type=int, default=42)
    pseudo_russell.add_argument("--min-history-observations", type=int, default=252)
    pseudo_russell.add_argument("--max-staleness-days", type=int, default=10)
    pseudo_russell.add_argument("--exclude-ticker", action="append", default=None)

    sensitivity_matrix = subparsers.add_parser("build-commodity-sensitivity-matrix")
    sensitivity_matrix.add_argument("--commodity", required=True)
    sensitivity_matrix.add_argument("--commodity-signals", type=Path, default=Path("data/processed/commodity_signals.parquet"))
    sensitivity_matrix.add_argument("--beta-returns", type=Path, default=Path("data/processed/equity_beta_returns.parquet"))
    sensitivity_matrix.add_argument(
        "--broad-universe",
        type=Path,
        default=Path("data/processed/broad_liquid_universe_quarterly.csv"),
    )
    sensitivity_matrix.add_argument("--output", type=Path, default=None)
    sensitivity_matrix.add_argument("--feature", action="append", default=None)
    sensitivity_matrix.add_argument(
        "--feature-preset",
        choices=["priority", "curve_shock_vol", "broad"],
        default="priority",
    )
    sensitivity_matrix.add_argument("--horizon", action="append", type=int, default=None)
    sensitivity_matrix.add_argument("--sample-years", action="append", type=int, default=None)
    sensitivity_matrix.add_argument("--start", default=None)
    sensitivity_matrix.add_argument("--end", default=None)
    sensitivity_matrix.add_argument("--feature-z-window", type=int, default=252)
    sensitivity_matrix.add_argument("--min-feature-observations", type=int, default=126)
    sensitivity_matrix.add_argument("--min-observations", type=int, default=126)
    sensitivity_matrix.add_argument("--include-prestandardized", action="store_true")

    feature_return_cache = subparsers.add_parser("build-daily-feature-return-cache")
    feature_return_cache.add_argument("--commodity", required=True)
    feature_return_cache.add_argument("--commodity-signals", type=Path, default=Path("data/processed/commodity_signals.parquet"))
    feature_return_cache.add_argument("--beta-returns", type=Path, default=Path("data/processed/equity_beta_returns.parquet"))
    feature_return_cache.add_argument("--output", type=Path, default=None)
    feature_return_cache.add_argument("--feature", action="append", default=None)
    feature_return_cache.add_argument(
        "--feature-preset",
        choices=["priority", "curve_shock_vol", "broad"],
        default="priority",
    )
    feature_return_cache.add_argument("--horizon", action="append", type=int, default=None)
    feature_return_cache.add_argument("--feature-z-window", type=int, default=252)
    feature_return_cache.add_argument("--min-feature-observations", type=int, default=126)
    feature_return_cache.add_argument("--min-observations", type=int, default=126)
    feature_return_cache.add_argument("--include-prestandardized", action="store_true")
    feature_return_cache.add_argument("--return-column", action="append", default=None)

    quarterly_matrix = subparsers.add_parser("build-quarterly-stock-feature-matrix")
    quarterly_matrix.add_argument("--commodity", required=True)
    quarterly_matrix.add_argument("--cache", type=Path, default=None)
    quarterly_matrix.add_argument(
        "--broad-universe",
        type=Path,
        default=Path("data/processed/pseudo_russell1000_universe_quarterly.csv"),
    )
    quarterly_matrix.add_argument("--output-dir", type=Path, default=None)
    quarterly_matrix.add_argument("--manifest", type=Path, default=None)
    quarterly_matrix.add_argument("--lookback-years", action="append", type=int, default=None)
    quarterly_matrix.add_argument("--horizon", action="append", type=int, default=None)
    quarterly_matrix.add_argument("--target-return-column", action="append", default=None)
    quarterly_matrix.add_argument("--start", default=None)
    quarterly_matrix.add_argument("--end", default=None)
    quarterly_matrix.add_argument("--min-observations", type=int, default=126)
    quarterly_matrix.add_argument("--verbose", action="store_true")
    quarterly_matrix.add_argument("--progress-interval", type=int, default=25)

    selection_backtest = subparsers.add_parser("run-quarterly-selection-backtest")
    selection_backtest.add_argument("--commodity", required=True)
    selection_backtest.add_argument("--feature", action="append", required=True)
    selection_backtest.add_argument("--ticker", action="append", default=None)
    selection_backtest.add_argument("--cache", type=Path, required=True)
    selection_backtest.add_argument("--equity-processed", type=Path, default=Path("data/processed/equity_processed.parquet"))
    selection_backtest.add_argument("--matrix-dir", type=Path, default=None)
    selection_backtest.add_argument("--output-dir", type=Path, default=Path("data/backtests"))
    selection_backtest.add_argument("--target-return-column", default="residual_return_mktsec_w12m")
    selection_backtest.add_argument("--return-column", action="append", default=None)
    selection_backtest.add_argument("--horizon-days", type=int, default=21)
    selection_backtest.add_argument("--lookback-years", action="append", type=int, default=None)
    selection_backtest.add_argument("--min-nonoverlap-abs-t-stat", type=float, default=1.5)
    selection_backtest.add_argument("--min-effective-observations", type=int, default=20)
    selection_backtest.add_argument("--min-selected-lookbacks", type=int, default=1)
    selection_backtest.add_argument("--min-direction-share", type=float, default=0.5)
    selection_backtest.add_argument("--min-pairs", type=int, default=2)
    selection_backtest.add_argument("--basket-scope", choices=["quarter", "feature"], default="quarter")
    selection_backtest.add_argument("--activation-z", type=float, default=1.5)
    selection_backtest.add_argument("--trigger-mode", choices=["z-abs", "level-ge", "level-le"], default="z-abs")
    selection_backtest.add_argument("--activation-level", type=float, default=None)
    selection_backtest.add_argument("--hold-days", type=int, default=21)
    selection_backtest.add_argument("--signal-lag-days", type=int, default=1)
    selection_backtest.add_argument("--gross-exposure", type=float, default=1.0)

    selection_path = subparsers.add_parser("simulate-selection-path")
    selection_path.add_argument("--commodity", required=True)
    selection_path.add_argument("--feature", action="append", required=True)
    selection_path.add_argument("--ticker", action="append", default=None)
    selection_path.add_argument("--matrix-dir", type=Path, default=None)
    selection_path.add_argument("--output-pairs", type=Path, default=None)
    selection_path.add_argument("--output-baskets", type=Path, default=None)
    selection_path.add_argument("--target-return-column", default="residual_return_mktsec_w12m")
    selection_path.add_argument("--horizon-days", type=int, default=21)
    selection_path.add_argument("--lookback-years", action="append", type=int, default=None)
    selection_path.add_argument("--min-nonoverlap-abs-t-stat", type=float, default=1.5)
    selection_path.add_argument("--min-effective-observations", type=int, default=20)
    selection_path.add_argument("--min-selected-lookbacks", type=int, default=1)
    selection_path.add_argument("--min-direction-share", type=float, default=0.5)
    selection_path.add_argument("--min-pairs", type=int, default=2)
    selection_path.add_argument("--basket-scope", choices=["quarter", "feature"], default="quarter")
    selection_path.add_argument("--simulations", type=int, default=500)
    selection_path.add_argument("--t-stat-noise", type=float, default=1.0)
    selection_path.add_argument("--random-seed", type=int, default=7)

    basket_cluster = subparsers.add_parser("audit-basket-cluster-risk")
    basket_cluster.add_argument("--selection-pairs", type=Path, required=True)
    basket_cluster.add_argument("--exposure-map", type=Path, default=Path("config/commodity_exposure_map.csv"))
    basket_cluster.add_argument("--candidates", type=Path, default=None)
    basket_cluster.add_argument("--output", type=Path, default=Path("data/processed/basket_cluster_risk_audit.csv"))
    basket_cluster.add_argument(
        "--detail-output",
        type=Path,
        default=Path("data/processed/basket_cluster_risk_audit_detail.csv"),
    )
    basket_cluster.add_argument("--min-selection-probability", type=float, default=0.8)
    basket_cluster.add_argument("--max-direction-flip-probability", type=float, default=0.1)
    basket_cluster.add_argument("--min-tickers", type=int, default=5)
    basket_cluster.add_argument("--min-roles", type=int, default=2)
    basket_cluster.add_argument("--min-effective-tickers", type=float, default=4.0)
    basket_cluster.add_argument("--min-effective-roles", type=float, default=1.5)
    basket_cluster.add_argument("--max-ticker-share", type=float, default=0.35)
    basket_cluster.add_argument("--max-role-share", type=float, default=0.65)
    basket_cluster.add_argument("--max-unknown-role-share", type=float, default=0.25)
    basket_cluster.add_argument("--group-by-feature", action="store_true")
    basket_cluster.add_argument("--allow-macro-regime", action="store_true")

    mechanism_state = subparsers.add_parser("build-mechanism-state-model")
    mechanism_state.add_argument("--commodity-signals", type=Path, default=Path("data/processed/commodity_signals.parquet"))
    mechanism_state.add_argument("--exposure-map", type=Path, default=Path("config/commodity_exposure_map.csv"))
    mechanism_state.add_argument("--role-taxonomy", type=Path, default=Path("config/commodity_role_taxonomy.csv"))
    mechanism_state.add_argument("--commodity", default=None)
    mechanism_state.add_argument("--as-of-date", default=None)
    mechanism_state.add_argument("--output", type=Path, default=Path("data/processed/mechanism_state_roles.csv"))
    mechanism_state.add_argument(
        "--ticker-output",
        type=Path,
        default=Path("data/processed/mechanism_state_tickers.csv"),
    )
    mechanism_state.add_argument("--curve-z-threshold", type=float, default=1.5)
    mechanism_state.add_argument("--momentum-z-threshold", type=float, default=1.0)
    mechanism_state.add_argument("--price-regime-share-threshold", type=float, default=0.6)
    mechanism_state.add_argument("--vol-z-threshold", type=float, default=1.0)
    mechanism_state.add_argument("--participation-z-threshold", type=float, default=1.0)
    mechanism_state.add_argument("--min-spread-abs", type=float, default=0.005)
    mechanism_state.add_argument("--min-spread-chg-abs", type=float, default=0.01)
    mechanism_state.add_argument("--min-role-tickers", type=int, default=1)

    mechanism_alignment = subparsers.add_parser("audit-mechanism-alignment")
    mechanism_alignment.add_argument("--mechanism-tickers", type=Path, required=True)
    mechanism_alignment.add_argument("--matrix-dir", type=Path, default=None)
    mechanism_alignment.add_argument("--commodity", default="CL")
    mechanism_alignment.add_argument("--output", type=Path, default=Path("data/processed/mechanism_alignment_audit.csv"))
    mechanism_alignment.add_argument(
        "--detail-output",
        type=Path,
        default=Path("data/processed/mechanism_alignment_audit_detail.csv"),
    )
    mechanism_alignment.add_argument("--target-return-column", default="residual_return_mktsec_w12m")
    mechanism_alignment.add_argument("--horizon-days", action="append", type=int, default=None)
    mechanism_alignment.add_argument("--lookback-years", action="append", type=int, default=None)
    mechanism_alignment.add_argument("--min-alignment-probability", type=float, default=0.67)
    mechanism_alignment.add_argument("--review-band", type=float, default=0.55)

    tiers = subparsers.add_parser("classify-commodity-universe-tiers")
    tiers.add_argument("--commodity", required=True)
    tiers.add_argument("--sensitivity-matrix", type=Path, default=None)
    tiers.add_argument("--broad-universe", type=Path, default=Path("data/processed/broad_liquid_universe_quarterly.csv"))
    tiers.add_argument("--exposure-map", type=Path, default=Path("config/commodity_exposure_map.csv"))
    tiers.add_argument("--beta-returns", type=Path, default=Path("data/processed/equity_beta_returns.parquet"))
    tiers.add_argument("--output", type=Path, default=None)
    tiers.add_argument("--min-abs-t", type=float, default=2.0)
    tiers.add_argument("--anchor-corr-lookback-days", type=int, default=252)

    discovered_universe = subparsers.add_parser("build-discovered-commodity-universe")
    discovered_universe.add_argument("--commodity", required=True)
    discovered_universe.add_argument("--tiers", type=Path, default=None)
    discovered_universe.add_argument("--output", type=Path, default=None)
    discovered_universe.add_argument("--output-dir", type=Path, default=Path("data/universe_discovered"))
    discovered_universe.add_argument("--max-names", type=int, default=60)
    discovered_universe.add_argument("--max-anchor-share", type=float, default=0.25)
    discovered_universe.add_argument("--min-second-order", type=int, default=10)
    discovered_universe.add_argument("--min-discovery-score", type=float, default=0.0)

    universe_audit = subparsers.add_parser("audit-commodity-universe")
    universe_audit.add_argument("--commodity", required=True)
    universe_audit.add_argument("--quarter", required=True)
    universe_audit.add_argument("--tiers", type=Path, default=None)
    universe_audit.add_argument("--selected-universe", type=Path, default=None)
    universe_audit.add_argument("--output", type=Path, default=None)
    universe_audit.add_argument("--max-rejected", type=int, default=100)

    shortability = subparsers.add_parser("build-shortability")
    shortability.add_argument("--prices-dir", type=Path, default=Path("data/equity/yfinance"))
    shortability.add_argument("--output", type=Path, default=Path("data/processed/shortability.parquet"))
    shortability.add_argument("--min-price", type=float, default=5.0)
    shortability.add_argument("--min-adv", type=float, default=5_000_000.0)
    shortability.add_argument("--lookback-days", type=int, default=63)

    portfolio = subparsers.add_parser("build-portfolio-weights")
    portfolio.add_argument("--scores", type=Path, required=True)
    portfolio.add_argument("--output", type=Path, default=Path("data/processed/portfolio_weights.csv"))
    portfolio.add_argument("--mode", choices=["long-short", "index-hedge"], default="index-hedge")
    portfolio.add_argument("--shortability", type=Path, default=None)
    portfolio.add_argument("--long-count", type=int, default=20)
    portfolio.add_argument("--short-count", type=int, default=20)
    portfolio.add_argument("--gross-long", type=float, default=1.0)
    portfolio.add_argument("--gross-short", type=float, default=1.0)
    portfolio.add_argument("--hedge-symbol", default="SPY")
    portfolio.add_argument("--hedge-weight", type=float, default=-1.0)
    portfolio.add_argument("--shortability-max-staleness-days", type=int, default=5)

    backtest = subparsers.add_parser("run-backtest")
    backtest.add_argument("--scores", type=Path, required=True)
    backtest.add_argument("--prices-dir", type=Path, default=Path("data/equity/yfinance"))
    backtest.add_argument("--output-daily", type=Path, default=Path("data/processed/backtest_daily.csv"))
    backtest.add_argument("--output-weights", type=Path, default=Path("data/processed/backtest_weights.csv"))
    backtest.add_argument("--output-summary", type=Path, default=Path("data/processed/backtest_summary.csv"))
    backtest.add_argument("--mode", choices=["long-short", "index-hedge"], default="index-hedge")
    backtest.add_argument("--shortability", type=Path, default=None)
    backtest.add_argument("--long-count", type=int, default=20)
    backtest.add_argument("--short-count", type=int, default=20)
    backtest.add_argument("--gross-long", type=float, default=1.0)
    backtest.add_argument("--gross-short", type=float, default=1.0)
    backtest.add_argument("--hedge-symbol", default="SPY")
    backtest.add_argument("--hedge-weight", type=float, default=-1.0)
    backtest.add_argument("--hold-days", type=int, default=21)
    backtest.add_argument("--execution-lag-days", type=int, default=1)
    backtest.add_argument("--transaction-cost-bps", type=float, default=0.0)
    backtest.add_argument("--capital-per-sleeve", type=float, default=None)
    backtest.add_argument("--shortability-max-staleness-days", type=int, default=5)

    reactions = subparsers.add_parser("study-feature-reactions")
    reactions.add_argument(
        "--commodity-signals",
        type=Path,
        default=Path("data/processed/commodity_signals.parquet"),
    )
    reactions.add_argument("--prices-dir", type=Path, default=Path("data/equity/yfinance"))
    reactions.add_argument(
        "--quarterly-universe",
        type=Path,
        default=Path("data/processed/quarterly_universe.csv"),
    )
    reactions.add_argument("--output", type=Path, default=Path("data/processed/feature_reactions.csv"))
    reactions.add_argument("--feature", action="append", default=None)
    reactions.add_argument("--horizon", action="append", type=int, default=None)
    reactions.add_argument("--as-of-date", default=None)
    reactions.add_argument("--lookback-years", type=float, default=3.0)
    reactions.add_argument("--shock-z-threshold", type=float, default=1.0)
    reactions.add_argument("--feature-z-window", type=int, default=252)
    reactions.add_argument("--min-feature-observations", type=int, default=126)
    reactions.add_argument("--min-events", type=int, default=8)
    reactions.add_argument("--adjust-market", default=None)
    reactions.add_argument("--non-overlap-events", action="store_true")
    reactions.add_argument("--residualize", action="store_true")
    reactions.add_argument("--residual-market", default="SPY")
    reactions.add_argument("--sector-map", type=Path, default=Path("config/theme_sector_hedges.csv"))
    reactions.add_argument("--beta-lookback-days", type=int, default=252)
    reactions.add_argument("--min-beta-observations", type=int, default=126)

    candidates = subparsers.add_parser("build-candidate-signals")
    candidates.add_argument("--reactions", type=Path, default=Path("data/processed/feature_reactions.csv"))
    candidates.add_argument("--universe", type=Path, default=Path("config/us_commodity_equity_seed.csv"))
    candidates.add_argument("--output", type=Path, default=Path("data/processed/candidate_signals.csv"))
    candidates.add_argument("--min-events", type=int, default=30)
    candidates.add_argument("--min-abs-t", type=float, default=3.0)
    candidates.add_argument("--min-same-direction-horizons", type=int, default=2)

    registry = subparsers.add_parser("build-sensitivity-registry")
    registry.add_argument("--reactions", type=Path, default=Path("data/processed/feature_reactions.csv"))
    registry.add_argument("--universe", type=Path, default=Path("config/us_commodity_equity_seed.csv"))
    registry.add_argument("--output", type=Path, default=Path("data/processed/stock_sensitivity_registry.csv"))
    registry.add_argument("--min-events", type=int, default=30)
    registry.add_argument("--min-abs-t", type=float, default=3.0)
    registry.add_argument("--min-same-direction-horizons", type=int, default=2)

    scores = subparsers.add_parser("build-daily-scores")
    scores.add_argument("--registry", type=Path, default=Path("data/processed/stock_sensitivity_registry.csv"))
    scores.add_argument(
        "--commodity-signals",
        type=Path,
        default=Path("data/processed/commodity_signals.parquet"),
    )
    scores.add_argument("--output", type=Path, default=Path("data/processed/daily_scores.csv"))
    scores.add_argument("--as-of-date", required=True)
    scores.add_argument("--feature-z-window", type=int, default=252)
    scores.add_argument("--min-feature-observations", type=int, default=126)

    beta = subparsers.add_parser("build-equity-beta-returns")
    beta.add_argument("--prices-dir", type=Path, default=Path("data/equity/yfinance"))
    beta.add_argument("--universe", type=Path, default=Path("config/us_commodity_equity_seed.csv"))
    beta.add_argument("--theme-hedges", type=Path, default=Path("config/theme_sector_hedges.csv"))
    beta.add_argument("--output", type=Path, default=Path("data/processed/equity_beta_returns.parquet"))
    beta.add_argument("--market-ticker", default="SPY")
    beta.add_argument("--beta-lookback-days", type=int, default=252)
    beta.add_argument("--beta-lookback-months", type=int, default=12)
    beta.add_argument("--min-beta-observations", type=int, default=26)
    beta.add_argument("--beta-lag-days", type=int, default=1)
    beta.add_argument("--beta-return-frequency", choices=["daily", "weekly"], default="weekly")
    beta.add_argument("--beta-update-frequency", choices=["daily", "monthly"], default="monthly")
    beta.add_argument("--beta-weighting", choices=["equal", "exponential"], default="exponential")
    beta.add_argument("--beta-half-life-months", type=float, default=3.0)
    beta.add_argument("--beta-smoothing", type=float, default=0.0)
    beta.add_argument("--hedge-ratio-scale", type=float, default=1.0)

    equity_processed = subparsers.add_parser("build-equity-processed-dataset")
    equity_processed.add_argument("--prices-dir", type=Path, default=Path("data/equity/yfinance"))
    equity_processed.add_argument("--universe", type=Path, default=Path("config/us_commodity_equity_seed.csv"))
    equity_processed.add_argument("--theme-hedges", type=Path, default=Path("config/theme_sector_hedges.csv"))
    equity_processed.add_argument("--output", type=Path, default=Path("data/processed/equity_processed.parquet"))
    equity_processed.add_argument("--commodity-signals", type=Path, default=Path("data/processed/commodity_signals.parquet"))
    equity_processed.add_argument("--exposure-map", type=Path, default=Path("config/commodity_exposure_map.csv"))
    equity_processed.add_argument("--market-ticker", default="SPY")
    equity_processed.add_argument("--start", default="2010-01-01")
    equity_processed.add_argument("--end", default=None)
    equity_processed.add_argument(
        "--beta-variation",
        action="append",
        choices=sorted(DEFAULT_PROCESSED_BETA_VARIATIONS),
        default=None,
    )
    equity_processed.add_argument(
        "--primary-variation",
        choices=sorted(DEFAULT_PROCESSED_BETA_VARIATIONS),
        default=DEFAULT_PRIMARY_PROCESSED_BETA_VARIATION,
    )
    equity_processed.add_argument("--beta-lag-days", type=int, default=1)
    equity_processed.add_argument("--commodity-beta-symbol", action="append", default=None)
    equity_processed.add_argument("--commodity-return-column", default=DEFAULT_COMMODITY_BETA_RETURN_COLUMN)
    equity_processed.add_argument("--skip-commodity-beta-residuals", action="store_true")
    equity_processed.add_argument("--quiet", action="store_true", help="Suppress progress logs.")

    forecast = subparsers.add_parser("study-commodity-forecast")
    forecast.add_argument("--commodity-signals", type=Path, default=Path("data/processed/commodity_signals.parquet"))
    forecast.add_argument("--beta-returns", type=Path, default=Path("data/processed/equity_beta_returns.parquet"))
    forecast.add_argument("--universe", type=Path, default=Path("config/us_commodity_equity_seed.csv"))
    forecast.add_argument("--output", type=Path, required=True)
    forecast.add_argument("--commodity", required=True)
    forecast.add_argument("--ticker", action="append", default=None)
    forecast.add_argument("--theme", default=None)
    forecast.add_argument("--feature", action="append", default=None)
    forecast.add_argument("--horizon", action="append", type=int, default=None)
    forecast.add_argument("--sample-years", action="append", type=int, default=None)
    forecast.add_argument("--feature-z-window", type=int, default=252)
    forecast.add_argument("--min-feature-observations", type=int, default=126)
    forecast.add_argument("--min-observations", type=int, default=126)
    forecast.add_argument("--include-prestandardized", action="store_true")
    forecast.add_argument("--include-annual", action="store_true")

    exposure = subparsers.add_parser("list-exposure-universe")
    exposure.add_argument("--exposure-map", type=Path, default=Path("config/commodity_exposure_map.csv"))
    exposure.add_argument("--commodity", default=None)
    exposure.add_argument("--min-abs-prior-weight", type=float, default=0.0)
    exposure.add_argument("--output", type=Path, default=None)

    reviewed = subparsers.add_parser("list-reviewed-features")
    reviewed.add_argument("--reviewed-features", type=Path, default=Path("config/reviewed_commodity_features.csv"))
    reviewed.add_argument("--commodity", default=None)
    reviewed.add_argument("--family", default=None)
    reviewed.add_argument("--enabled-only", action="store_true")
    reviewed.add_argument("--output", type=Path, default=None)

    audit = subparsers.add_parser("audit-forecast-signals")
    audit.add_argument("--forecast", action="append", type=Path, required=True)
    audit.add_argument("--exposure-map", type=Path, default=Path("config/commodity_exposure_map.csv"))
    audit.add_argument("--reviewed-features", type=Path, default=Path("config/reviewed_commodity_features.csv"))
    audit.add_argument("--output", type=Path, default=Path("data/processed/forecast_signal_audit.csv"))
    audit.add_argument("--aggregate-sample", default=None)
    audit.add_argument("--high-abs-t", type=float, default=8.0)
    audit.add_argument("--min-same-direction-share", type=float, default=0.6)
    audit.add_argument("--min-peer-direction-share", type=float, default=0.6)

    falsification = subparsers.add_parser("audit-sensitivity-falsification")
    falsification.add_argument("--matrix", type=Path, required=True)
    falsification.add_argument("--exposure-map", type=Path, default=Path("config/commodity_exposure_map.csv"))
    falsification.add_argument("--output", type=Path, default=Path("data/processed/sensitivity_falsification_audit.csv"))
    falsification.add_argument("--min-abs-t", type=float, default=2.0)
    falsification.add_argument("--min-nonoverlap-abs-t", type=float, default=1.0)
    falsification.add_argument("--min-effective-observations", type=int, default=20)
    falsification.add_argument("--max-overlap-inflation", type=float, default=3.0)
    falsification.add_argument("--min-hit-rate-edge", type=float, default=0.03)

    nonlinear_beta = subparsers.add_parser("audit-nonlinear-commodity-beta")
    nonlinear_beta.add_argument("--candidates", type=Path, required=True)
    nonlinear_beta.add_argument("--equity-processed", type=Path, default=Path("data/processed/equity_processed.parquet"))
    nonlinear_beta.add_argument("--commodity-signals", type=Path, default=Path("data/processed/commodity_signals.parquet"))
    nonlinear_beta.add_argument("--exposure-map", type=Path, default=Path("config/commodity_exposure_map.csv"))
    nonlinear_beta.add_argument("--output", type=Path, default=Path("data/processed/nonlinear_commodity_beta_audit.csv"))
    nonlinear_beta.add_argument("--return-column", default="residual_return_mktsec_w12m")
    nonlinear_beta.add_argument("--commodity-return-column", default="commodity_return_mktseccomm")
    nonlinear_beta.add_argument("--commodity-signal-return-column", default="front_log_ret_1d")
    nonlinear_beta.add_argument("--lag-days", action="append", type=int, default=None)
    nonlinear_beta.add_argument("--min-observations", type=int, default=126)
    nonlinear_beta.add_argument("--large-move-quantile", type=float, default=0.80)
    nonlinear_beta.add_argument("--volatility-window", type=int, default=21)
    nonlinear_beta.add_argument("--max-abs-lag-corr-threshold", type=float, default=0.15)
    nonlinear_beta.add_argument("--asymmetry-corr-diff-threshold", type=float, default=0.15)

    signal_decay = subparsers.add_parser("audit-signal-decay")
    signal_decay.add_argument("--candidates", type=Path, required=True)
    signal_decay.add_argument("--cache", type=Path, required=True)
    signal_decay.add_argument("--commodity", default=None)
    signal_decay.add_argument("--output", type=Path, default=Path("data/processed/signal_decay_audit.csv"))
    signal_decay.add_argument("--detail-output", type=Path, default=Path("data/processed/signal_decay_audit_detail.csv"))
    signal_decay.add_argument("--return-column", default="residual_return_mktsec_w12m")
    signal_decay.add_argument("--horizon", action="append", type=int, default=None)
    signal_decay.add_argument("--activation-z", type=float, default=1.5)
    signal_decay.add_argument("--min-event-count", type=int, default=20)
    signal_decay.add_argument("--min-sign-stability", type=float, default=0.67)




    peer_expansion = subparsers.add_parser("expand-candidate-peers")
    peer_expansion.add_argument("--candidates", type=Path, required=True)
    peer_expansion.add_argument("--selected-features", type=Path, required=True)
    peer_expansion.add_argument("--cache", type=Path, required=True)
    peer_expansion.add_argument("--commodity", default=None)
    peer_expansion.add_argument("--output", type=Path, default=Path("data/processed/peer_expansion.csv"))
    peer_expansion.add_argument("--return-column", default="residual_return_mktsec_w12m")
    peer_expansion.add_argument("--activation-z", type=float, default=1.5)
    peer_expansion.add_argument("--min-peer-nonoverlap-abs-t", type=float, default=1.0)
    peer_expansion.add_argument("--min-peer-events", type=int, default=10)
    peer_expansion.add_argument("--min-peer-event-sum", type=float, default=0.0)
    macro_regime = subparsers.add_parser("build-macro-regime-signals")
    macro_regime.add_argument("--raw-dir", type=Path, default=Path("data/macro/raw"))
    macro_regime.add_argument("--output", type=Path, default=Path("data/processed/macro_regime.parquet"))
    year_stability = subparsers.add_parser("audit-year-stability")
    year_stability.add_argument("--candidates", type=Path, required=True)
    year_stability.add_argument("--cache", type=Path, required=True)
    year_stability.add_argument("--commodity", default=None)
    year_stability.add_argument("--output", type=Path, default=Path("data/processed/year_stability_audit.csv"))
    year_stability.add_argument(
        "--detail-output",
        type=Path,
        default=Path("data/processed/year_stability_audit_detail.csv"),
    )
    year_stability.add_argument("--return-column", default="residual_return_mktsec_w12m")
    year_stability.add_argument("--horizon", type=int, default=21)
    year_stability.add_argument("--activation-z", type=float, default=1.5)
    year_stability.add_argument("--min-event-count", type=int, default=20)
    year_stability.add_argument("--max-concentration", type=float, default=0.30)
    year_stability.add_argument("--min-loyo-abs-t", type=float, default=1.5)
    regime_validity = subparsers.add_parser("audit-regime-conditioned-validity")
    regime_validity.add_argument("--candidates", type=Path, required=True)
    regime_validity.add_argument("--cache", type=Path, required=True)
    regime_validity.add_argument(
        "--commodity-signals",
        type=Path,
        default=Path("data/processed/commodity_signals.parquet"),
    )
    regime_validity.add_argument("--commodity", default=None)
    regime_validity.add_argument("--output", type=Path, default=Path("data/processed/regime_validity_audit.csv"))
    regime_validity.add_argument(
        "--detail-output",
        type=Path,
        default=Path("data/processed/regime_validity_audit_detail.csv"),
    )
    regime_validity.add_argument("--return-column", default="residual_return_mktsec_w12m")
    regime_validity.add_argument("--horizon", action="append", type=int, default=None)
    regime_validity.add_argument("--activation-z", type=float, default=1.5)
    regime_validity.add_argument(
        "--regime-dimension",
        action="append",
        choices=DEFAULT_REGIME_DIMENSIONS,
        default=None,
    )
    regime_validity.add_argument("--min-regime-event-count", type=int, default=20)
    regime_validity.add_argument("--min-positive-regime-share", type=float, default=0.67)
    regime_validity.add_argument("--max-dominant-regime-event-share", type=float, default=0.70)
    regime_validity.add_argument("--min-effective-regime-count", type=float, default=1.5)
    regime_validity.add_argument("--curve-z-threshold", type=float, default=1.0)
    regime_validity.add_argument("--price-share-threshold", type=float, default=0.6)
    regime_validity.add_argument("--vol-z-threshold", type=float, default=1.0)
    regime_validity.add_argument("--momentum-z-threshold", type=float, default=1.0)
    regime_validity.add_argument("--macro-regime", type=Path, default=None)

    regime_adversarial = subparsers.add_parser("audit-regime-adversarial")
    regime_adversarial.add_argument("--candidates", type=Path, required=True)
    regime_adversarial.add_argument("--cache", type=Path, required=True)
    regime_adversarial.add_argument(
        "--commodity-signals",
        type=Path,
        default=Path("data/processed/commodity_signals.parquet"),
    )
    regime_adversarial.add_argument("--commodity", default=None)
    regime_adversarial.add_argument("--output", type=Path, default=Path("data/processed/regime_adversarial_audit.csv"))
    regime_adversarial.add_argument(
        "--detail-output",
        type=Path,
        default=Path("data/processed/regime_adversarial_audit_detail.csv"),
    )
    regime_adversarial.add_argument("--return-column", default="residual_return_mktsec_w12m")
    regime_adversarial.add_argument("--horizon", action="append", type=int, default=None)
    regime_adversarial.add_argument("--activation-z", type=float, default=1.5)
    regime_adversarial.add_argument(
        "--regime-dimension",
        action="append",
        choices=DEFAULT_REGIME_DIMENSIONS,
        default=None,
    )
    regime_adversarial.add_argument("--min-removed-event-count", type=int, default=20)
    regime_adversarial.add_argument("--min-holdout-event-count", type=int, default=40)
    regime_adversarial.add_argument("--max-removed-event-share", type=float, default=0.60)
    regime_adversarial.add_argument("--max-mean-drop-ratio", type=float, default=0.50)
    regime_adversarial.add_argument("--curve-z-threshold", type=float, default=1.0)
    regime_adversarial.add_argument("--price-share-threshold", type=float, default=0.6)
    regime_adversarial.add_argument("--vol-z-threshold", type=float, default=1.0)
    regime_adversarial.add_argument("--momentum-z-threshold", type=float, default=1.0)
    regime_adversarial.add_argument("--macro-regime", type=Path, default=None)

    basket_regime_adversarial = subparsers.add_parser("audit-basket-regime-adversarial")
    basket_regime_adversarial.add_argument("--candidates", type=Path, required=True)
    basket_regime_adversarial.add_argument("--cache", type=Path, required=True)
    basket_regime_adversarial.add_argument(
        "--commodity-signals",
        type=Path,
        default=Path("data/processed/commodity_signals.parquet"),
    )
    basket_regime_adversarial.add_argument("--commodity", default=None)
    basket_regime_adversarial.add_argument(
        "--output",
        type=Path,
        default=Path("data/processed/basket_regime_adversarial_audit.csv"),
    )
    basket_regime_adversarial.add_argument(
        "--events-output",
        type=Path,
        default=Path("data/processed/basket_regime_adversarial_events.csv"),
    )
    basket_regime_adversarial.add_argument("--return-column", default="residual_return_mktsec_w12m")
    basket_regime_adversarial.add_argument("--horizon", type=int, default=42)
    basket_regime_adversarial.add_argument("--activation-z", type=float, default=1.5)
    basket_regime_adversarial.add_argument(
        "--regime-dimension",
        action="append",
        choices=DEFAULT_REGIME_DIMENSIONS,
        default=None,
    )
    basket_regime_adversarial.add_argument("--min-removed-event-count", type=int, default=20)
    basket_regime_adversarial.add_argument("--min-holdout-event-count", type=int, default=40)
    basket_regime_adversarial.add_argument("--max-removed-event-share", type=float, default=0.60)
    basket_regime_adversarial.add_argument("--max-mean-drop-ratio", type=float, default=0.50)
    basket_regime_adversarial.add_argument("--curve-z-threshold", type=float, default=1.0)
    basket_regime_adversarial.add_argument("--price-share-threshold", type=float, default=0.6)
    basket_regime_adversarial.add_argument("--vol-z-threshold", type=float, default=1.0)
    basket_regime_adversarial.add_argument("--momentum-z-threshold", type=float, default=1.0)

    basket_state_filter = subparsers.add_parser("audit-basket-state-filter")
    basket_state_filter.add_argument("--events", type=Path, required=True)
    basket_state_filter.add_argument("--output", type=Path, default=Path("data/processed/basket_state_filter_audit.csv"))
    basket_state_filter.add_argument("--regime-dimension", default="vol_regime")
    basket_state_filter.add_argument("--horizon", type=int, default=42)
    basket_state_filter.add_argument("--min-nonoverlap-events", type=int, default=5)
    basket_state_filter.add_argument("--min-nonoverlap-t-stat", type=float, default=1.5)

    taxonomy_audit = subparsers.add_parser("audit-exposure-taxonomy")
    taxonomy_audit.add_argument("--exposure-map", type=Path, default=Path("config/commodity_exposure_map.csv"))
    taxonomy_audit.add_argument("--role-taxonomy", type=Path, default=Path("config/commodity_role_taxonomy.csv"))
    taxonomy_audit.add_argument("--candidates", type=Path, default=None)
    taxonomy_audit.add_argument("--output", type=Path, default=Path("data/processed/exposure_taxonomy_audit.csv"))
    taxonomy_audit.add_argument(
        "--unmapped-output",
        type=Path,
        default=Path("data/processed/exposure_taxonomy_unmapped_candidates.csv"),
    )

    candidate_taxonomy = subparsers.add_parser("review-candidate-taxonomy")
    candidate_taxonomy.add_argument("--candidates", type=Path, required=True)
    candidate_taxonomy.add_argument("--exposure-map", type=Path, default=Path("config/commodity_exposure_map.csv"))
    candidate_taxonomy.add_argument("--role-taxonomy", type=Path, default=Path("config/commodity_role_taxonomy.csv"))
    candidate_taxonomy.add_argument("--mechanism-alignment", type=Path, default=None)
    candidate_taxonomy.add_argument("--output", type=Path, default=Path("data/processed/candidate_taxonomy_review.csv"))
    candidate_taxonomy.add_argument("--min-mechanism-alignment-probability", type=float, default=0.67)
    candidate_taxonomy.add_argument("--mechanism-review-band", type=float, default=0.55)

    turnover = subparsers.add_parser("study-registry-turnover")
    turnover.add_argument("--registry", action="append", type=Path, default=None)
    turnover.add_argument("--reactions", type=Path, default=None)
    turnover.add_argument("--universe", type=Path, default=Path("config/us_commodity_equity_seed.csv"))
    turnover.add_argument("--output", type=Path, default=Path("data/processed/registry_turnover_summary.csv"))
    turnover.add_argument("--detail-output", type=Path, default=Path("data/processed/registry_turnover_detail.csv"))
    turnover.add_argument("--min-events", type=int, default=30)
    turnover.add_argument("--min-abs-t", type=float, default=3.0)
    turnover.add_argument("--min-same-direction-horizons", type=int, default=2)

    group_scores = subparsers.add_parser("build-group-activation-scores")
    group_scores.add_argument("--registry", type=Path, default=Path("data/processed/stock_sensitivity_registry.csv"))
    group_scores.add_argument(
        "--commodity-signals",
        type=Path,
        default=Path("data/processed/commodity_signals.parquet"),
    )
    group_scores.add_argument("--exposure-map", type=Path, default=Path("config/commodity_exposure_map.csv"))
    group_scores.add_argument("--output", type=Path, default=Path("data/processed/group_activation_scores.csv"))
    group_scores.add_argument("--as-of-date", required=True)
    group_scores.add_argument("--activation-z", type=float, default=1.0)
    group_scores.add_argument("--feature-z-window", type=int, default=252)
    group_scores.add_argument("--min-feature-observations", type=int, default=126)
    group_scores.add_argument("--allow-unmapped", action="store_true")

    consolidate = subparsers.add_parser("consolidate-candidate-signals")
    consolidate.add_argument("--candidates", type=Path, default=Path("data/processed/candidate_signals.csv"))
    consolidate.add_argument("--forecast-audit", type=Path, default=Path("data/processed/forecast_signal_audit.csv"))
    consolidate.add_argument("--reviewed-features", type=Path, default=Path("config/reviewed_commodity_features.csv"))
    consolidate.add_argument("--mechanism-alignment", type=Path, default=None)
    consolidate.add_argument("--output", type=Path, default=Path("data/processed/consolidated_candidate_signals.csv"))
    consolidate.add_argument("--min-confidence", choices=["low", "medium", "high"], default="medium")
    consolidate.add_argument("--require-audit-candidate", action="store_true")
    consolidate.add_argument("--require-mechanism-pass", action="store_true")
    consolidate.add_argument("--block-mechanism-conflicts", action="store_true")
    consolidate.add_argument("--min-mechanism-alignment-probability", type=float, default=0.67)
    consolidate.add_argument("--mechanism-review-band", type=float, default=0.55)
    consolidate.add_argument("--min-same-direction-share", type=float, default=0.6)
    consolidate.add_argument("--min-peer-direction-share", type=float, default=0.0)
    consolidate.add_argument("--max-per-ticker", type=int, default=3)

    matrix = subparsers.add_parser("build-stock-feature-matrix")
    matrix.add_argument(
        "--signals",
        type=Path,
        default=Path("data/processed/consolidated_candidate_signals.csv"),
    )
    matrix.add_argument("--output", type=Path, default=Path("data/processed/stock_feature_matrix.csv"))
    matrix.add_argument("--source", default="consolidated_candidate_signals")

    matrix_cache = subparsers.add_parser("build-stock-feature-matrix-cache")
    matrix_cache.add_argument("--reactions", type=Path, default=Path("data/processed/feature_reactions.csv"))
    matrix_cache.add_argument("--universe", type=Path, default=Path("config/us_commodity_equity_seed.csv"))
    matrix_cache.add_argument("--forecast-audit", type=Path, default=Path("data/processed/forecast_signal_audit.csv"))
    matrix_cache.add_argument("--reviewed-features", type=Path, default=Path("config/reviewed_commodity_features.csv"))
    matrix_cache.add_argument("--output", type=Path, default=Path("data/processed/stock_feature_matrix_cache.parquet"))
    matrix_cache.add_argument("--min-events", type=int, default=30)
    matrix_cache.add_argument("--min-abs-t", type=float, default=3.0)
    matrix_cache.add_argument("--min-same-direction-horizons", type=int, default=2)
    matrix_cache.add_argument("--min-confidence", choices=["low", "medium", "high"], default="medium")
    matrix_cache.add_argument("--require-audit-candidate", action="store_true")
    matrix_cache.add_argument("--min-same-direction-share", type=float, default=0.6)
    matrix_cache.add_argument("--min-peer-direction-share", type=float, default=0.0)
    matrix_cache.add_argument("--max-per-ticker", type=int, default=3)
    matrix_cache.add_argument("--source", default="rolling_feature_reactions")

    diagnostics = subparsers.add_parser("build-stock-feature-curve-diagnostics")
    diagnostics.add_argument(
        "--matrix",
        type=Path,
        default=Path("data/processed/stock_feature_matrix_cache.parquet"),
    )
    diagnostics.add_argument("--as-of-date", required=True)
    diagnostics.add_argument(
        "--output-annual",
        type=Path,
        default=Path("data/processed/stock_feature_curve_annual.csv"),
    )
    diagnostics.add_argument(
        "--output-regime",
        type=Path,
        default=Path("data/processed/stock_feature_curve_regime.csv"),
    )
    diagnostics.add_argument(
        "--output-time-regime",
        type=Path,
        default=Path("data/processed/stock_feature_curve_time_regime.csv"),
    )
    diagnostics.add_argument(
        "--output-summary",
        type=Path,
        default=Path("data/processed/stock_feature_curve_stability_summary.csv"),
    )
    diagnostics.add_argument("--ticker", default=None)
    diagnostics.add_argument("--commodity", default=None)
    diagnostics.add_argument("--feature", default=None)
    diagnostics.add_argument("--start", default="2016-01-01")
    diagnostics.add_argument("--end", default=None)
    diagnostics.add_argument("--return-column", default="residual_return")
    diagnostics.add_argument("--activation-z", type=float, default=1.0)
    diagnostics.add_argument("--position-mode", choices=["sign", "continuous"], default="sign")
    diagnostics.add_argument("--transaction-cost-bps", type=float, default=0.0)

    env = subparsers.add_parser("classify-commodity-environment")
    env.add_argument("--symbol", required=True)
    env.add_argument(
        "--commodity-signals",
        type=Path,
        default=Path("data/processed/commodity_signals.parquet"),
    )
    env.add_argument("--as-of-date", default=None)
    env.add_argument("--start", default="2010-01-01")
    env.add_argument("--current-window-days", type=int, default=63)
    env.add_argument("--feature", action="append", default=None)
    env.add_argument("--min-regime-observations", type=int, default=126)
    env.add_argument(
        "--output-summary",
        type=Path,
        default=Path("data/processed/commodity_environment_similarity.csv"),
    )
    env.add_argument(
        "--output-detail",
        type=Path,
        default=Path("data/processed/commodity_environment_similarity_detail.csv"),
    )

    feature_candidates = subparsers.add_parser("build-feature-trade-candidates")
    feature_candidates.add_argument(
        "--matrix",
        type=Path,
        default=Path("data/processed/stock_feature_matrix_cache_curve_loose.parquet"),
    )
    feature_candidates.add_argument("--as-of-date", required=True)
    feature_candidates.add_argument(
        "--commodity-signals",
        type=Path,
        default=Path("data/processed/commodity_signals.parquet"),
    )
    feature_candidates.add_argument(
        "--stability-summary",
        action="append",
        type=Path,
        default=None,
    )
    feature_candidates.add_argument("--commodity", action="append", default=None)
    feature_candidates.add_argument("--theme", action="append", default=None)
    feature_candidates.add_argument("--environment-start", default="2010-01-01")
    feature_candidates.add_argument("--environment-window-days", type=int, default=63)
    feature_candidates.add_argument("--max-per-commodity", type=int, default=12)
    feature_candidates.add_argument("--max-per-theme", type=int, default=4)
    feature_candidates.add_argument("--min-post-covid-active-median-return", type=float, default=0.0)
    feature_candidates.add_argument(
        "--output",
        type=Path,
        default=Path("data/processed/feature_trade_candidates.csv"),
    )

    feature_basket = subparsers.add_parser("run-feature-basket-backtest")
    feature_basket.add_argument("--candidates", type=Path, required=True)
    feature_basket.add_argument(
        "--matrix",
        type=Path,
        default=Path("data/processed/stock_feature_matrix_cache_curve_loose.parquet"),
    )
    feature_basket.add_argument("--as-of-date", required=True)
    feature_basket.add_argument(
        "--commodity-signals",
        type=Path,
        default=Path("data/processed/commodity_signals.parquet"),
    )
    feature_basket.add_argument(
        "--beta-returns",
        type=Path,
        default=Path("data/processed/equity_beta_returns.parquet"),
    )
    feature_basket.add_argument("--start", default="2010-01-01")
    feature_basket.add_argument("--end", default=None)
    feature_basket.add_argument("--return-column", default="residual_return")
    feature_basket.add_argument("--activation-z", type=float, default=1.0)
    feature_basket.add_argument("--exit-z", type=float, default=None)
    feature_basket.add_argument("--position-mode", choices=["sign", "continuous"], default="sign")
    feature_basket.add_argument("--transaction-cost-bps", type=float, default=10.0)
    feature_basket.add_argument("--max-pair-weight", type=float, default=0.12)
    feature_basket.add_argument("--target-gross", type=float, default=1.0)
    feature_basket.add_argument("--rebalance-frequency", choices=["daily", "weekly", "monthly"], default="daily")
    feature_basket.add_argument("--include-ineligible", action="store_true")
    feature_basket.add_argument("--label", default="feature_basket")
    feature_basket.add_argument(
        "--output-daily",
        type=Path,
        default=Path("data/processed/feature_basket_daily.csv"),
    )
    feature_basket.add_argument(
        "--output-weights",
        type=Path,
        default=Path("data/processed/feature_basket_weights.csv"),
    )
    feature_basket.add_argument(
        "--output-summary",
        type=Path,
        default=Path("data/processed/feature_basket_summary.csv"),
    )

    precision_candidates = subparsers.add_parser("build-precision-event-candidates")
    precision_candidates.add_argument("--candidates", type=Path, required=True)
    precision_candidates.add_argument("--as-of-date", required=True)
    precision_candidates.add_argument(
        "--commodity-signals",
        type=Path,
        default=Path("data/processed/commodity_signals.parquet"),
    )
    precision_candidates.add_argument("--exposure-map", type=Path, default=Path("config/commodity_exposure_map.csv"))
    precision_candidates.add_argument(
        "--role-taxonomy",
        type=Path,
        default=Path("config/commodity_role_taxonomy.csv"),
    )
    precision_candidates.add_argument("--falsification-audit", type=Path, default=None)
    precision_candidates.add_argument("--shortability", type=Path, default=None)
    precision_candidates.add_argument("--no-require-trigger", action="store_true")
    precision_candidates.add_argument("--allow-low-priority-roles", action="store_true")
    precision_candidates.add_argument("--max-names", type=int, default=None)
    precision_candidates.add_argument(
        "--output",
        type=Path,
        default=Path("data/processed/precision_event_candidates.csv"),
    )

    fundamentals = subparsers.add_parser("build-fundamental-snapshot")
    fundamentals.add_argument(
        "--openbb-metrics",
        type=Path,
        default=Path("data/external/port_research/openbb_equity_fundamental_metrics.csv"),
    )
    fundamentals.add_argument(
        "--edgar-factors",
        type=Path,
        default=Path("data/external/port_research/edgar_factors.csv"),
    )
    fundamentals.add_argument("--exposure-map", type=Path, default=Path("config/commodity_exposure_map.csv"))
    fundamentals.add_argument("--role-taxonomy", type=Path, default=Path("config/commodity_role_taxonomy.csv"))
    fundamentals.add_argument(
        "--output-snapshot",
        type=Path,
        default=Path("data/processed/fundamental_snapshot.csv"),
    )
    fundamentals.add_argument(
        "--output-factors",
        type=Path,
        default=Path("data/processed/fundamental_factors.csv"),
    )
    fundamentals.add_argument("--min-market-cap", type=float, default=500_000_000.0)

    ag_fundamentals = subparsers.add_parser("build-agriculture-fundamental-events")
    ag_fundamentals.add_argument(
        "--nass-factors",
        type=Path,
        default=Path("data/external/port_research/nass_factors.csv"),
    )
    ag_fundamentals.add_argument(
        "--usda-report-factors",
        type=Path,
        default=Path("data/external/port_research/usda_report_factors.csv"),
    )
    ag_fundamentals.add_argument(
        "--output",
        type=Path,
        default=Path("data/processed/agriculture_fundamental_events.csv"),
    )
    ag_fundamentals.add_argument("--usda-tradable-hour-utc", type=int, default=18)

    commodity_confirmation = subparsers.add_parser("build-commodity-confirmation-events")
    commodity_confirmation.add_argument("--commodity", default="CL")
    commodity_confirmation.add_argument(
        "--eia-factors",
        type=Path,
        default=Path("data/external/port_research/eia_factors.csv"),
    )
    commodity_confirmation.add_argument(
        "--cftc-factors",
        type=Path,
        default=Path("data/external/port_research/cftc_factors.csv"),
    )
    commodity_confirmation.add_argument(
        "--output",
        type=Path,
        default=Path("data/processed/cl_commodity_confirmation_events.csv"),
    )
    commodity_confirmation.add_argument("--eia-tradable-lag-days", type=int, default=1)
    commodity_confirmation.add_argument("--cftc-tradable-lag-days", type=int, default=3)

    commodity_research = subparsers.add_parser("research-commodity-features")
    commodity_research.add_argument("--commodity", required=True)
    commodity_research.add_argument("--matrix-dir", type=Path, default=None)
    commodity_research.add_argument("--manifest", type=Path, default=None)
    commodity_research.add_argument("--diagnostic-matrix-dir", type=Path, default=None)
    commodity_research.add_argument("--diagnostic-manifest", type=Path, default=None)
    commodity_research.add_argument("--exposure-map", type=Path, default=Path("config/commodity_exposure_map.csv"))
    commodity_research.add_argument("--role-taxonomy", type=Path, default=Path("config/commodity_role_taxonomy.csv"))
    commodity_research.add_argument("--reviewed-features", type=Path, default=Path("config/reviewed_commodity_features.csv"))
    commodity_research.add_argument("--output-dir", type=Path, default=None)
    commodity_research.add_argument("--quarter", action="append", default=None)
    commodity_research.add_argument("--include-unreviewed-features", action="store_true")
    commodity_research.add_argument("--target-return-column", default="residual_return_mktsec_w12m")
    commodity_research.add_argument("--diagnostic-target-return-column", default="residual_return_mktseccomm_w12m")
    commodity_research.add_argument("--min-abs-t", type=float, default=2.0)
    commodity_research.add_argument("--min-nonoverlap-abs-t", type=float, default=1.0)
    commodity_research.add_argument("--min-effective-observations", type=int, default=20)
    commodity_research.add_argument("--min-hit-rate-edge", type=float, default=0.03)
    commodity_research.add_argument("--min-sign-stability", type=float, default=0.5)
    commodity_research.add_argument("--commodity-neutral-min-ratio", type=float, default=0.5)
    commodity_research.add_argument("--verbose", action="store_true")
    commodity_research.add_argument("--progress-interval", type=int, default=10)

    curve_first = subparsers.add_parser("select-curve-first-candidates")
    curve_first.add_argument("--commodity", required=True)
    curve_first.add_argument("--matrix-dir", type=Path, required=True)
    curve_first.add_argument("--cache", type=Path, required=True)
    curve_first.add_argument("--output", type=Path, required=True)
    curve_first.add_argument("--selected-output", type=Path, default=None)
    curve_first.add_argument("--quarter", action="append", default=None)
    curve_first.add_argument("--lookback-years", action="append", type=int, default=None)
    curve_first.add_argument("--target-return-column", default="residual_return_mktsec_w12m")
    curve_first.add_argument("--activation-z", type=float, default=1.5)
    curve_first.add_argument(
        "--allowed-state",
        action="append",
        default=None,
        help="Allowed state_hypothesis. Defaults to curve_tightness and curve_tightness_change.",
    )
    curve_first.add_argument("--min-nonoverlap-abs-t", type=float, default=1.0)
    curve_first.add_argument("--min-effective-observations", type=int, default=20)
    curve_first.add_argument("--min-robust-calmar", type=float, default=0.5)
    curve_first.add_argument("--max-dominant-year-share", type=float, default=0.5)
    curve_first.add_argument("--max-candidates", type=int, default=None)

    curve_first_taxonomy = subparsers.add_parser("review-curve-first-taxonomy")
    curve_first_taxonomy.add_argument("--candidates", type=Path, required=True)
    curve_first_taxonomy.add_argument("--exposure-map", type=Path, default=Path("config/commodity_exposure_map.csv"))
    curve_first_taxonomy.add_argument("--role-taxonomy", type=Path, default=Path("config/commodity_role_taxonomy.csv"))
    curve_first_taxonomy.add_argument("--output", type=Path, required=True)
    curve_first_taxonomy.add_argument("--block-low-priority", action="store_true")

    curve_first_oos = subparsers.add_parser("run-curve-first-oos")
    curve_first_oos.add_argument("--taxonomy", action="append", type=Path, required=True)
    curve_first_oos.add_argument("--cache", type=Path, required=True)
    curve_first_oos.add_argument("--events-output", type=Path, required=True)
    curve_first_oos.add_argument("--daily-output", type=Path, required=True)
    curve_first_oos.add_argument("--summary-output", type=Path, required=True)
    curve_first_oos.add_argument("--verdict", action="append", default=None)
    curve_first_oos.add_argument("--return-column", action="append", default=None)
    curve_first_oos.add_argument("--activation-z", type=float, default=1.5)
    curve_first_oos.add_argument("--weighting", choices=["equal"], default="equal")
    curve_first_oos.add_argument("--no-collapse-same-ticker-state", action="store_true")
    curve_first_oos.add_argument("--oos-mode", choices=["next-quarter", "year-remainder"], default="next-quarter")
    curve_first_oos.add_argument("--oos-end-quarter", default=None)

    cross_summary = subparsers.add_parser("summarize-cross-product-clusters")
    cross_summary.add_argument("--commodity", default="CL")
    cross_summary.add_argument("--trigger-role-results", type=Path, default=None)
    cross_summary.add_argument("--output", type=Path, default=None)
    cross_summary.add_argument("--detail-output", type=Path, default=None)
    cross_summary.add_argument("--min-keep-count", type=int, default=5)
    cross_summary.add_argument("--top", type=int, default=50)
    cross_summary.add_argument("--exclude-role", action="append", default=None)
    cross_summary.add_argument("--include-direct-oil-roles", action="store_true")

    state_summary = subparsers.add_parser("summarize-state-role-clusters")
    state_summary.add_argument("--candidates", type=Path, required=True)
    state_summary.add_argument("--output", type=Path, required=True)
    state_summary.add_argument("--detail-output", type=Path, required=True)
    state_summary.add_argument("--min-keep-count", type=int, default=5)
    state_summary.add_argument("--keep-only", action="store_true")

    edgar_sections = subparsers.add_parser("extract-edgar-sections")
    edgar_sections.add_argument("--tickers", required=True, help="Comma-separated tickers or @filename")
    edgar_sections.add_argument("--filings-dir", type=Path, default=Path("data/edgar_filings/filings"))
    edgar_sections.add_argument("--output-dir", type=Path, default=Path("data/edgar_filings/sections"))
    edgar_sections.add_argument("--form-types", default="10-K,20-F", help="Form types to process")
    edgar_sections.add_argument("--sections", default="", help="Comma-separated sections (default: all applicable)")
    edgar_sections.add_argument("--year", type=int, default=2025, help="Filing year")
    edgar_sections.add_argument("--print", dest="print_stdout", action="store_true", help="Print to stdout instead of files")
    state_summary.add_argument("--top", type=int, default=50)

    edgar_cache = subparsers.add_parser("build-edgar-filing-cache")
    edgar_cache.add_argument("--tickers", default="", help="Comma-separated tickers (e.g. PSX,WLK,DOW)")
    edgar_cache.add_argument(
        "--tickers-file", type=Path, default=None, help="Path to file with one ticker per line"
    )
    edgar_cache.add_argument(
        "--form-types", default="10-K,10-Q", help="Comma-separated form types (default: 10-K,10-Q)"
    )
    edgar_cache.add_argument("--start-year", type=int, default=2005)
    edgar_cache.add_argument("--output-dir", type=Path, default=Path("data/edgar_filings"))
    edgar_cache.add_argument(
        "--index-cache", type=Path, default=None, help="Path to cached filing_index.csv to avoid re-scraping"
    )
    edgar_cache.add_argument(
        "--skip-download", action="store_true", help="Only build the filing index, do not download filings"
    )
    edgar_cache.add_argument(
        "--skip-index", action="store_true", help="Only download filings using an existing index"
    )
    edgar_cache.add_argument(
        "--dry-run", action="store_true", help="Print what would be downloaded without actually downloading"
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "build-commodity-signals":
        print(f"Loading carry data from {args.input_dir} ...")
        carry = load_carry_directory(args.input_dir)
        carry_summary = (
            carry.groupby("symbol", sort=True)
            .agg(rows=("date", "size"), start=("date", "min"), end=("date", "max"))
            .reset_index()
        )
        for row in carry_summary.itertuples(index=False):
            print(f"  {row.symbol}: {row.rows:,} rows, {row.start.date()} -> {row.end.date()}")

        include_brent_wti = not args.no_brent_wti_features
        print(
            "Building commodity signal frame "
            f"(calendar_contracts=on, brent_wti_features={'on' if include_brent_wti else 'off'}) ..."
        )
        signals = build_commodity_signal_frame(
            carry,
            commodity_dir=args.commodity_dir,
            include_brent_wti_features=include_brent_wti,
        )
        if include_brent_wti:
            brent_wti_cols = [
                col
                for col in signals.columns
                if col.startswith("brent_wti_") or col.startswith("brent_minus_wti_")
            ]
            cl_rows = signals["symbol"].astype(str).str.upper().eq("CL")
            if brent_wti_cols:
                non_null = int(signals.loc[cl_rows, brent_wti_cols[0]].notna().sum())
                print(
                    "Added Brent-WTI companion features on CL rows: "
                    f"{len(brent_wti_cols)} columns, {non_null:,} aligned observations"
                )
            else:
                print("No Brent-WTI companion features were added.")
        write_frame(signals, args.output)
        print(f"Wrote {len(signals):,} commodity signal rows to {args.output}")
        return

    if args.command == "download-equities":
        seed = load_seed_universe(args.universe)
        if args.ticker:
            tickers = [ticker.upper() for ticker in args.ticker]
        else:
            tickers = seed["ticker"].tolist()
        if args.limit is not None:
            tickers = tickers[: args.limit]
        paths = download_yfinance_prices(
            tickers,
            output_dir=args.output_dir,
            start=args.start,
            end=args.end,
            auto_adjust=args.auto_adjust,
        )
        print(f"Wrote {len(paths):,} yfinance price files to {args.output_dir}")
        return

    if args.command == "build-quarterly-universe":
        quarterly = build_quarterly_liquidity_universe(
            seed_path=args.universe,
            prices_dir=args.prices_dir,
            min_price=args.min_price,
            min_adv=args.min_adv,
            lookback_days=args.lookback_days,
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        quarterly.to_csv(args.output, index=False)
        print(f"Wrote {len(quarterly):,} quarterly universe rows to {args.output}")
        return

    if args.command == "build-commodity-quarterly-universes":
        commodities = args.commodity or ["CL", "HG"]
        universe = build_commodity_quarterly_universes(
            exposure_map_path=args.exposure_map,
            seed_path=args.seed_universe,
            prices_dir=args.prices_dir,
            commodities=commodities,
            start=args.start,
            end=args.end,
            min_price=args.min_price,
            min_adv=args.min_adv,
            lookback_days=args.lookback_days,
            min_lookback_observations=args.min_lookback_observations,
            min_history_observations=args.min_history_observations,
            max_staleness_days=args.max_staleness_days,
            min_abs_prior_weight=args.min_abs_prior_weight,
        )
        args.combined_output.parent.mkdir(parents=True, exist_ok=True)
        universe.to_csv(args.combined_output, index=False)
        paths = write_commodity_quarterly_universe_files(universe, args.output_dir)
        print(
            f"Wrote {len(universe):,} commodity-quarter universe rows to {args.combined_output} "
            f"and {len(paths):,} files under {args.output_dir}"
        )
        return

    if args.command == "build-broad-quarterly-liquidity-universe":
        exclude_tickers = args.exclude_ticker or DEFAULT_EXCLUDED_BROAD_UNIVERSE_TICKERS
        universe = build_broad_quarterly_liquidity_universe(
            prices_dir=args.prices_dir,
            seed_path=args.seed_universe,
            start=args.start,
            end=args.end,
            min_price=args.min_price,
            min_adv=args.min_adv,
            lookback_days=args.lookback_days,
            min_lookback_observations=args.min_lookback_observations,
            min_history_observations=args.min_history_observations,
            max_staleness_days=args.max_staleness_days,
            exclude_tickers=exclude_tickers,
            max_names=None,
            universe_source="local_broad_liquidity",
            constituent_pit_status="local_symbol_universe_not_constituent_pit",
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        universe.to_csv(args.output, index=False)
        print(f"Wrote {len(universe):,} broad quarterly liquidity rows to {args.output}")
        return

    if args.command == "build-pseudo-russell1000-universe":
        exclude_tickers = args.exclude_ticker or DEFAULT_EXCLUDED_BROAD_UNIVERSE_TICKERS
        universe = build_broad_quarterly_liquidity_universe(
            prices_dir=args.prices_dir,
            seed_path=args.seed_universe,
            start=args.start,
            end=args.end,
            min_price=args.min_price,
            min_adv=args.min_adv,
            lookback_days=args.lookback_days,
            min_lookback_observations=args.min_lookback_observations,
            min_history_observations=args.min_history_observations,
            max_staleness_days=args.max_staleness_days,
            exclude_tickers=exclude_tickers,
            max_names=args.max_names,
            universe_source="pseudo_russell1000_liquidity",
            constituent_pit_status="not_true_russell_constituents_local_symbols_only",
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        universe.to_csv(args.output, index=False)
        print(
            f"Wrote {len(universe):,} pseudo Russell 1000 quarterly rows to {args.output}; "
            f"max names per quarter: {args.max_names:,}"
        )
        return

    if args.command == "build-commodity-sensitivity-matrix":
        commodity_code = args.commodity.upper().strip()
        output = args.output or Path(f"data/sensitivity/{commodity_code}/{commodity_code}-Sensitivity-Matrix.parquet")
        matrix = build_commodity_sensitivity_matrix_from_paths(
            commodity_signals_path=args.commodity_signals,
            beta_returns_path=args.beta_returns,
            broad_universe_path=args.broad_universe,
            output_path=output,
            commodity=commodity_code,
            features=args.feature,
            horizons=args.horizon,
            sample_years=args.sample_years,
            start=args.start,
            end=args.end,
            feature_z_window=args.feature_z_window,
            min_feature_observations=args.min_feature_observations,
            min_observations=args.min_observations,
            include_prestandardized=args.include_prestandardized,
            feature_preset=args.feature_preset,
        )
        print(f"Wrote {len(matrix):,} {commodity_code} sensitivity matrix rows to {output}")
        return

    if args.command == "build-daily-feature-return-cache":
        commodity_code = args.commodity.upper().strip()
        return_columns = args.return_column or ["residual_return"]
        return_slug = "multi_return" if len(return_columns) > 1 else "".join(
            ch if ch.isalnum() else "_" for ch in return_columns[0]
        ).strip("_")
        output = args.output or (
            Path(f"data/cache/feature_return/{commodity_code}.parquet")
            if return_columns == ["residual_return"]
            else Path(f"data/cache/feature_return/{commodity_code}-{return_slug}.parquet")
        )
        print(
            f"Building {commodity_code} daily feature-return cache from {args.commodity_signals} "
            f"and {args.beta_returns} ..."
        )
        print(
            f"  feature_preset={args.feature_preset}, explicit_features={len(args.feature or [])}, "
            f"returns={','.join(return_columns)}, output={output}"
        )
        cache = build_daily_feature_return_cache_from_paths(
            commodity_signals_path=args.commodity_signals,
            beta_returns_path=args.beta_returns,
            output_path=output,
            commodity=commodity_code,
            features=args.feature,
            horizons=args.horizon,
            feature_preset=args.feature_preset,
            feature_z_window=args.feature_z_window,
            min_feature_observations=args.min_feature_observations,
            min_observations=args.min_observations,
            include_prestandardized=args.include_prestandardized,
            return_column=return_columns,
        )
        feature_z_cols = [col for col in cache.columns if col.startswith("feature_z__")]
        brent_wti_cols = [col for col in feature_z_cols if "brent_wti" in col or "brent_minus_wti" in col]
        print(
            f"  cache feature columns: {len(feature_z_cols)} total, "
            f"{len(brent_wti_cols)} Brent-WTI companion columns"
        )
        print(
            f"Wrote {len(cache):,} {commodity_code} daily feature-return cache rows "
            f"using {','.join(return_columns)} to {output}"
        )
        return

    if args.command == "build-quarterly-stock-feature-matrix":
        commodity_code = args.commodity.upper().strip()
        cache_path = args.cache or Path(f"data/cache/feature_return/{commodity_code}.parquet")
        output_dir = args.output_dir or Path(f"data/matrix/{commodity_code}")
        manifest_path = args.manifest or output_dir / f"{commodity_code}-Features-manifest.csv"
        manifest = write_quarterly_stock_feature_matrix_files_from_paths(
            cache_path=cache_path,
            broad_universe_path=args.broad_universe,
            output_dir=output_dir,
            manifest_path=manifest_path,
            commodity=commodity_code,
            lookback_years=args.lookback_years,
            horizons=args.horizon,
            target_return_columns=args.target_return_column,
            start=args.start,
            end=args.end,
            min_observations=args.min_observations,
            verbose=args.verbose,
            progress_interval=args.progress_interval,
        )
        print(
            f"Wrote {len(manifest):,} {commodity_code} quarterly stock-feature matrix files "
            f"to {output_dir}; manifest: {manifest_path}"
        )
        return

    if args.command == "run-quarterly-selection-backtest":
        commodity_code = args.commodity.upper().strip()
        matrix_dir = args.matrix_dir or Path(f"data/matrix/{commodity_code}")
        pair, events, stock_daily, portfolio_daily = run_quarterly_selection_backtest_from_paths(
            cache_path=args.cache,
            equity_processed_path=args.equity_processed,
            matrix_dir=matrix_dir,
            output_dir=args.output_dir,
            commodity=commodity_code,
            feature=args.feature,
            tickers=args.ticker,
            target_return_column=args.target_return_column,
            horizon_days=args.horizon_days,
            lookback_years=args.lookback_years,
            min_nonoverlap_abs_t_stat=args.min_nonoverlap_abs_t_stat,
            min_effective_observations=args.min_effective_observations,
            min_selected_lookbacks=args.min_selected_lookbacks,
            min_direction_share=args.min_direction_share,
            min_pairs=args.min_pairs,
            basket_scope=args.basket_scope,
            activation_z=args.activation_z,
            trigger_mode=args.trigger_mode,
            activation_level=args.activation_level,
            hold_days=args.hold_days,
            signal_lag_days=args.signal_lag_days,
            gross_exposure=args.gross_exposure,
            return_columns=args.return_column,
        )
        print(
            f"Wrote {len(pair):,} eligibility rows, {len(events):,} events, "
            f"{len(stock_daily):,} stock daily rows, and {len(portfolio_daily):,} portfolio daily rows "
            f"to {args.output_dir / commodity_code}"
        )
        return

    if args.command == "simulate-selection-path":
        commodity_code = args.commodity.upper().strip()
        matrix_dir = args.matrix_dir or Path(f"data/matrix/{commodity_code}")
        feature_set = "__".join(feature.replace("/", "_").replace(" ", "_") for feature in args.feature)
        output_pairs = args.output_pairs or Path(
            f"data/processed/{commodity_code}-{feature_set}-selection_path_pairs.csv"
        )
        output_baskets = args.output_baskets or Path(
            f"data/processed/{commodity_code}-{feature_set}-selection_path_baskets.csv"
        )
        pairs, baskets = simulate_selection_path_stability_from_paths(
            matrix_dir=matrix_dir,
            output_pairs_path=output_pairs,
            output_baskets_path=output_baskets,
            commodity=commodity_code,
            feature=args.feature,
            tickers=args.ticker,
            target_return_column=args.target_return_column,
            horizon_days=args.horizon_days,
            lookback_years=args.lookback_years,
            min_nonoverlap_abs_t_stat=args.min_nonoverlap_abs_t_stat,
            min_effective_observations=args.min_effective_observations,
            min_selected_lookbacks=args.min_selected_lookbacks,
            min_direction_share=args.min_direction_share,
            min_pairs=args.min_pairs,
            basket_scope=args.basket_scope,
            simulations=args.simulations,
            t_stat_noise=args.t_stat_noise,
            random_seed=args.random_seed,
        )
        pair_counts = pairs["path_stability_verdict"].value_counts().to_dict() if not pairs.empty else {}
        basket_counts = baskets["basket_path_verdict"].value_counts().to_dict() if not baskets.empty else {}
        print(
            f"Wrote {len(pairs):,} selection path pair rows to {output_pairs} "
            f"and {len(baskets):,} basket rows to {output_baskets}; "
            f"pair verdicts: {pair_counts}; basket verdicts: {basket_counts}"
        )
        return

    if args.command == "build-mechanism-state-model":
        role_states, ticker_detail = build_mechanism_state_model_from_paths(
            commodity_signals_path=args.commodity_signals,
            exposure_map_path=args.exposure_map,
            role_taxonomy_path=args.role_taxonomy,
            output_path=args.output,
            ticker_output_path=args.ticker_output,
            commodity=args.commodity,
            as_of_date=args.as_of_date,
            curve_z_threshold=args.curve_z_threshold,
            momentum_z_threshold=args.momentum_z_threshold,
            price_regime_share_threshold=args.price_regime_share_threshold,
            vol_z_threshold=args.vol_z_threshold,
            participation_z_threshold=args.participation_z_threshold,
            min_spread_abs=args.min_spread_abs,
            min_spread_chg_abs=args.min_spread_chg_abs,
            min_role_tickers=args.min_role_tickers,
        )
        counts = (
            role_states["mechanism_verdict"].value_counts().to_dict()
            if "mechanism_verdict" in role_states
            else {}
        )
        print(
            f"Wrote {len(role_states):,} mechanism state-role rows to {args.output} "
            f"and {len(ticker_detail):,} ticker rows to {args.ticker_output}; verdicts: {counts}"
        )
        return

    if args.command == "audit-mechanism-alignment":
        commodity_code = args.commodity.upper().strip()
        matrix_dir = args.matrix_dir or Path(f"data/matrix/{commodity_code}")
        summary, detail = build_mechanism_alignment_audit_from_paths(
            mechanism_tickers_path=args.mechanism_tickers,
            matrix_dir=matrix_dir,
            output_path=args.output,
            detail_output_path=args.detail_output,
            commodity=commodity_code,
            target_return_column=args.target_return_column,
            horizon_days=args.horizon_days,
            lookback_years=args.lookback_years,
            min_alignment_probability=args.min_alignment_probability,
            review_band=args.review_band,
        )
        counts = (
            summary["mechanism_alignment_verdict"].value_counts().to_dict()
            if "mechanism_alignment_verdict" in summary
            else {}
        )
        print(
            f"Wrote {len(summary):,} mechanism alignment rows to {args.output} "
            f"and {len(detail):,} detail rows to {args.detail_output}; verdicts: {counts}"
        )
        return

    if args.command == "audit-basket-cluster-risk":
        summary, detail = build_basket_cluster_risk_audit_from_paths(
            selection_pairs_path=args.selection_pairs,
            exposure_map_path=args.exposure_map,
            candidates_path=args.candidates,
            output_path=args.output,
            detail_output_path=args.detail_output,
            min_selection_probability=args.min_selection_probability,
            max_direction_flip_probability=args.max_direction_flip_probability,
            min_tickers=args.min_tickers,
            min_roles=args.min_roles,
            min_effective_tickers=args.min_effective_tickers,
            min_effective_roles=args.min_effective_roles,
            max_ticker_share=args.max_ticker_share,
            max_role_share=args.max_role_share,
            max_unknown_role_share=args.max_unknown_role_share,
            group_by_feature=args.group_by_feature,
            macro_regime_review=not args.allow_macro_regime,
        )
        counts = (
            summary["basket_cluster_verdict"].value_counts().to_dict()
            if "basket_cluster_verdict" in summary
            else {}
        )
        print(
            f"Wrote {len(summary):,} basket cluster risk rows to {args.output} "
            f"and {len(detail):,} detail rows to {args.detail_output}; verdicts: {counts}"
        )
        return

    if args.command == "classify-commodity-universe-tiers":
        commodity_code = args.commodity.upper().strip()
        sensitivity_path = args.sensitivity_matrix or Path(
            f"data/sensitivity/{commodity_code}/{commodity_code}-Sensitivity-Matrix.parquet"
        )
        output = args.output or Path(f"data/processed/{commodity_code.lower()}_universe_tiers.csv")
        tiers = classify_commodity_universe_tiers_from_paths(
            sensitivity_matrix_path=sensitivity_path,
            broad_universe_path=args.broad_universe,
            exposure_map_path=args.exposure_map,
            beta_returns_path=args.beta_returns,
            output_path=output,
            commodity=commodity_code,
            min_abs_t=args.min_abs_t,
            anchor_corr_lookback_days=args.anchor_corr_lookback_days,
        )
        print(f"Wrote {len(tiers):,} {commodity_code} universe tier rows to {output}")
        return

    if args.command == "build-discovered-commodity-universe":
        commodity_code = args.commodity.upper().strip()
        tiers_path = args.tiers or Path(f"data/processed/{commodity_code.lower()}_universe_tiers.csv")
        output = args.output or Path(f"data/processed/{commodity_code.lower()}_discovered_quarterly_universe.csv")
        universe = build_discovered_commodity_universe_from_paths(
            tiers_path=tiers_path,
            output_path=output,
            output_dir=args.output_dir,
            commodity=commodity_code,
            max_names=args.max_names,
            max_anchor_share=args.max_anchor_share,
            min_second_order=args.min_second_order,
            min_discovery_score=args.min_discovery_score,
        )
        print(
            f"Wrote {len(universe):,} {commodity_code} discovered universe rows to {output} "
            f"and quarter files under {args.output_dir}"
        )
        return

    if args.command == "audit-commodity-universe":
        commodity_code = args.commodity.upper().strip()
        tiers_path = args.tiers or Path(f"data/processed/{commodity_code.lower()}_universe_tiers.csv")
        selected_path = args.selected_universe or Path(
            f"data/processed/{commodity_code.lower()}_discovered_quarterly_universe.csv"
        )
        output = args.output or Path(f"data/reports/universe/{commodity_code}-{args.quarter}-audit.csv")
        audit = audit_commodity_universe_from_paths(
            tiers_path=tiers_path,
            selected_universe_path=selected_path,
            output_path=output,
            commodity=commodity_code,
            quarter=args.quarter,
            max_rejected=args.max_rejected,
        )
        print(f"Wrote {len(audit):,} {commodity_code} {args.quarter} universe audit rows to {output}")
        return

    if args.command == "build-shortability":
        shortability = build_shortability_from_price_directory(
            prices_dir=args.prices_dir,
            min_price=args.min_price,
            min_adv=args.min_adv,
            lookback_days=args.lookback_days,
        )
        write_frame(shortability, args.output)
        print(f"Wrote {len(shortability):,} shortability rows to {args.output}")
        return

    if args.command == "build-portfolio-weights":
        scores = load_scores(args.scores)
        if args.mode == "long-short":
            shortability = load_shortability(args.shortability) if args.shortability else None
            weights = build_long_short_weights(
                scores=scores,
                shortability=shortability,
                long_count=args.long_count,
                short_count=args.short_count,
                gross_long=args.gross_long,
                gross_short=args.gross_short,
                shortability_max_staleness_days=args.shortability_max_staleness_days,
            )
        else:
            weights = build_long_index_hedge_weights(
                scores=scores,
                long_count=args.long_count,
                gross_long=args.gross_long,
                hedge_symbol=args.hedge_symbol,
                hedge_weight=args.hedge_weight,
            )
        write_weights(weights, args.output)
        print(f"Wrote {len(weights):,} portfolio weight rows to {args.output}")
        return

    if args.command == "run-backtest":
        daily, weights, summary = run_score_backtest_from_paths(
            scores_path=args.scores,
            prices_dir=args.prices_dir,
            output_daily_path=args.output_daily,
            output_weights_path=args.output_weights,
            output_summary_path=args.output_summary,
            mode=args.mode,
            shortability_path=args.shortability,
            long_count=args.long_count,
            short_count=args.short_count,
            gross_long=args.gross_long,
            gross_short=args.gross_short,
            hedge_symbol=args.hedge_symbol,
            hedge_weight=args.hedge_weight,
            hold_days=args.hold_days,
            execution_lag_days=args.execution_lag_days,
            transaction_cost_bps=args.transaction_cost_bps,
            capital_per_sleeve=args.capital_per_sleeve,
            shortability_max_staleness_days=args.shortability_max_staleness_days,
        )
        print(
            f"Wrote {len(daily):,} backtest daily rows to {args.output_daily}, "
            f"{len(weights):,} weight rows to {args.output_weights}, "
            f"and {len(summary):,} summary rows to {args.output_summary}"
        )
        return

    if args.command == "study-feature-reactions":
        reactions = build_feature_reaction_study_from_paths(
            commodity_signals_path=args.commodity_signals,
            prices_dir=args.prices_dir,
            quarterly_universe_path=args.quarterly_universe,
            output_path=args.output,
            features=args.feature,
            horizons=args.horizon,
            as_of_date=args.as_of_date,
            lookback_years=args.lookback_years,
            shock_z_threshold=args.shock_z_threshold,
            feature_z_window=args.feature_z_window,
            min_feature_observations=args.min_feature_observations,
            min_events=args.min_events,
            adjust_market=args.adjust_market,
            non_overlap_events=args.non_overlap_events,
            residualize=args.residualize,
            residual_market=args.residual_market,
            sector_map_path=args.sector_map,
            beta_lookback_days=args.beta_lookback_days,
            min_beta_observations=args.min_beta_observations,
        )
        print(f"Wrote {len(reactions):,} feature reaction rows to {args.output}")
        return

    if args.command == "build-candidate-signals":
        candidates = build_candidate_signals_from_paths(
            reactions_path=args.reactions,
            universe_path=args.universe,
            output_path=args.output,
            min_events=args.min_events,
            min_abs_t=args.min_abs_t,
            min_same_direction_horizons=args.min_same_direction_horizons,
        )
        print(f"Wrote {len(candidates):,} candidate signal rows to {args.output}")
        return

    if args.command == "build-sensitivity-registry":
        registry = build_stock_sensitivity_registry_from_paths(
            reactions_path=args.reactions,
            universe_path=args.universe,
            output_path=args.output,
            min_events=args.min_events,
            min_abs_t=args.min_abs_t,
            min_same_direction_horizons=args.min_same_direction_horizons,
        )
        print(f"Wrote {len(registry):,} sensitivity registry rows to {args.output}")
        return

    if args.command == "build-daily-scores":
        scores = build_daily_scores_from_paths(
            registry_path=args.registry,
            commodity_signals_path=args.commodity_signals,
            output_path=args.output,
            as_of_date=args.as_of_date,
            feature_z_window=args.feature_z_window,
            min_feature_observations=args.min_feature_observations,
        )
        print(f"Wrote {len(scores):,} daily score rows to {args.output}")
        return

    if args.command == "build-equity-beta-returns":
        beta_returns = build_equity_beta_returns_from_paths(
            prices_dir=args.prices_dir,
            universe_path=args.universe,
            theme_hedges_path=args.theme_hedges,
            output_path=args.output,
            market_ticker=args.market_ticker,
            beta_lookback_days=args.beta_lookback_days,
            beta_lookback_months=args.beta_lookback_months,
            min_beta_observations=args.min_beta_observations,
            beta_lag_days=args.beta_lag_days,
            beta_return_frequency=args.beta_return_frequency,
            beta_update_frequency=args.beta_update_frequency,
            beta_weighting=args.beta_weighting,
            beta_half_life_months=args.beta_half_life_months,
            beta_smoothing=args.beta_smoothing,
            hedge_ratio_scale=args.hedge_ratio_scale,
        )
        print(f"Wrote {len(beta_returns):,} equity beta/return rows to {args.output}")
        return

    if args.command == "build-equity-processed-dataset":
        commodity_beta_symbols = args.commodity_beta_symbol or DEFAULT_COMMODITY_BETA_SYMBOLS
        dataset = build_equity_processed_dataset_from_paths(
            prices_dir=args.prices_dir,
            universe_path=args.universe,
            theme_hedges_path=args.theme_hedges,
            output_path=args.output,
            commodity_signals_path=args.commodity_signals,
            exposure_map_path=args.exposure_map,
            market_ticker=args.market_ticker,
            start=args.start,
            end=args.end,
            beta_variations=args.beta_variation,
            primary_variation=args.primary_variation,
            beta_lag_days=args.beta_lag_days,
            commodity_beta_symbols=commodity_beta_symbols,
            commodity_return_column=args.commodity_return_column,
            include_commodity_beta_residuals=not args.skip_commodity_beta_residuals,
            progress=not args.quiet,
        )
        print(f"Wrote {len(dataset):,} processed equity rows to {args.output}")
        return

    if args.command == "study-commodity-forecast":
        result = build_commodity_stock_forecast_study_from_paths(
            commodity_signals_path=args.commodity_signals,
            beta_returns_path=args.beta_returns,
            output_path=args.output,
            commodity=args.commodity,
            tickers=args.ticker,
            universe_path=args.universe,
            theme=args.theme,
            features=args.feature,
            horizons=args.horizon,
            sample_years=args.sample_years,
            feature_z_window=args.feature_z_window,
            min_feature_observations=args.min_feature_observations,
            min_observations=args.min_observations,
            include_prestandardized=args.include_prestandardized,
            include_annual=args.include_annual,
        )
        print(f"Wrote {len(result):,} commodity forecast rows to {args.output}")
        return

    if args.command == "list-exposure-universe":
        exposure = get_exposure_universe(
            exposure_map_path=args.exposure_map,
            commodity=args.commodity,
            min_abs_prior_weight=args.min_abs_prior_weight,
        )
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            exposure.to_csv(args.output, index=False)
            print(f"Wrote {len(exposure):,} exposure rows to {args.output}")
        else:
            print(exposure.to_string(index=False))
        return

    if args.command == "list-reviewed-features":
        reviewed = load_reviewed_features(args.reviewed_features)
        out = reviewed.copy()
        if args.enabled_only:
            out = out[out["default_enabled"]]
        if args.commodity:
            keep = args.commodity.upper().strip()
            out = out[out["commodity"].isin(["ALL", keep])]
        if args.family:
            out = out[out["feature_family"] == args.family]
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            out.to_csv(args.output, index=False)
            print(f"Wrote {len(out):,} reviewed feature rows to {args.output}")
        else:
            if args.commodity:
                features = reviewed_feature_list(reviewed, commodity=args.commodity, enabled_only=args.enabled_only)
                print("\n".join(features))
            else:
                print(out.to_string(index=False))
        return

    if args.command == "audit-forecast-signals":
        audit = audit_forecast_from_paths(
            forecast_paths=args.forecast,
            exposure_map_path=args.exposure_map,
            reviewed_features_path=args.reviewed_features,
            output_path=args.output,
            aggregate_sample=args.aggregate_sample,
            high_abs_t=args.high_abs_t,
            min_same_direction_share=args.min_same_direction_share,
            min_peer_direction_share=args.min_peer_direction_share,
        )
        print(f"Wrote {len(audit):,} forecast audit rows to {args.output}")
        return

    if args.command == "audit-sensitivity-falsification":
        audit = audit_sensitivity_falsification_from_paths(
            matrix_path=args.matrix,
            exposure_map_path=args.exposure_map,
            output_path=args.output,
            min_abs_t=args.min_abs_t,
            min_nonoverlap_abs_t=args.min_nonoverlap_abs_t,
            min_effective_observations=args.min_effective_observations,
            max_overlap_inflation=args.max_overlap_inflation,
            min_hit_rate_edge=args.min_hit_rate_edge,
        )
        print(f"Wrote {len(audit):,} sensitivity falsification audit rows to {args.output}")
        return

    if args.command == "audit-nonlinear-commodity-beta":
        audit = audit_nonlinear_commodity_beta_from_paths(
            candidates_path=args.candidates,
            equity_processed_path=args.equity_processed,
            commodity_signals_path=args.commodity_signals,
            exposure_map_path=args.exposure_map,
            output_path=args.output,
            return_column=args.return_column,
            commodity_return_column=args.commodity_return_column,
            commodity_signal_return_column=args.commodity_signal_return_column,
            lag_days=args.lag_days or [0, 1, 5, 10, 21],
            min_observations=args.min_observations,
            large_move_quantile=args.large_move_quantile,
            volatility_window=args.volatility_window,
            max_abs_lag_corr_threshold=args.max_abs_lag_corr_threshold,
            asymmetry_corr_diff_threshold=args.asymmetry_corr_diff_threshold,
        )
        counts = (
            audit["nonlinear_beta_verdict"].value_counts().to_dict()
            if "nonlinear_beta_verdict" in audit
            else {}
        )
        print(f"Wrote {len(audit):,} nonlinear commodity beta audit rows to {args.output}; verdicts: {counts}")
        return

    if args.command == "audit-signal-decay":
        summary, detail = build_signal_decay_audit_from_paths(
            candidates_path=args.candidates,
            cache_path=args.cache,
            output_path=args.output,
            detail_output_path=args.detail_output,
            commodity=args.commodity,
            return_column=args.return_column,
            horizons=args.horizon,
            activation_z=args.activation_z,
            min_event_count=args.min_event_count,
            min_sign_stability=args.min_sign_stability,
        )
        counts = summary["decay_verdict"].value_counts().to_dict() if "decay_verdict" in summary else {}
        print(
            f"Wrote {len(summary):,} signal decay rows to {args.output} "
            f"and {len(detail):,} detail rows to {args.detail_output}; verdicts: {counts}"
        )
        return



    if args.command == "expand-candidate-peers":
        peers = build_peer_expansion_from_paths(
            candidates_path=args.candidates,
            selected_features_path=args.selected_features,
            cache_path=args.cache,
            output_path=args.output,
            commodity=args.commodity,
            return_column=args.return_column,
            activation_z=args.activation_z,
            min_peer_nonoverlap_abs_t=args.min_peer_nonoverlap_abs_t,
            min_peer_events=args.min_peer_events,
            min_peer_event_sum=args.min_peer_event_sum,
        )
        if peers.empty:
            print("No qualified peers found.")
        else:
            groups = peers["peer_group_primaries"].nunique()
            print(f"Wrote {len(peers):,} peer-expanded candidates across {groups} peer groups to {args.output}")
            print(peers[["ticker","feature","peer_group_primaries","events","event_t_stat"]].to_string(index=False))
        return
    if args.command == "build-macro-regime-signals":
        frame = build_macro_regime_frame_from_paths(
            raw_dir=args.raw_dir,
            output_path=args.output,
        )
        regime_cols = ["vix_regime", "dxy_regime", "us10y_regime", "ovx_regime"]
        for col in regime_cols:
            if col in frame.columns:
                print(f"  {col}: {dict(frame[col].value_counts().to_dict())}")
        print(f"Wrote {len(frame):,} macro regime rows to {args.output}")
        return
    if args.command == "audit-year-stability":
        summary, detail = build_year_stability_audit_from_paths(
            candidates_path=args.candidates,
            cache_path=args.cache,
            output_path=args.output,
            detail_output_path=args.detail_output,
            commodity=args.commodity,
            return_column=args.return_column,
            horizon=args.horizon,
            activation_z=args.activation_z,
            min_event_count=args.min_event_count,
            max_concentration=args.max_concentration,
            min_loyo_abs_t=args.min_loyo_abs_t,
        )
        counts = summary["year_stability_verdict"].value_counts().to_dict() if "year_stability_verdict" in summary else {}
        print(
            f"Wrote {len(summary):,} year stability rows to {args.output} "
            f"and {len(detail):,} detail rows to {args.detail_output}; verdicts: {counts}"
        )
        return

    if args.command == "audit-regime-conditioned-validity":
        summary, detail = build_regime_conditioned_validity_audit_from_paths(
            candidates_path=args.candidates,
            cache_path=args.cache,
            commodity_signals_path=args.commodity_signals,
            output_path=args.output,
            detail_output_path=args.detail_output,
            commodity=args.commodity,
            return_column=args.return_column,
            horizons=args.horizon,
            activation_z=args.activation_z,
            regime_dimensions=args.regime_dimension,
            min_regime_event_count=args.min_regime_event_count,
            min_positive_regime_share=args.min_positive_regime_share,
            max_dominant_regime_event_share=args.max_dominant_regime_event_share,
            min_effective_regime_count=args.min_effective_regime_count,
            curve_z_threshold=args.curve_z_threshold,
            price_share_threshold=args.price_share_threshold,
            vol_z_threshold=args.vol_z_threshold,
            momentum_z_threshold=args.momentum_z_threshold,
            macro_regime_path=args.macro_regime,
        )
        counts = (
            summary["regime_validity_verdict"].value_counts().to_dict()
            if "regime_validity_verdict" in summary
            else {}
        )
        print(
            f"Wrote {len(summary):,} regime validity rows to {args.output} "
            f"and {len(detail):,} detail rows to {args.detail_output}; verdicts: {counts}"
        )
        return

    if args.command == "audit-regime-adversarial":
        summary, detail = build_regime_adversarial_audit_from_paths(
            candidates_path=args.candidates,
            cache_path=args.cache,
            commodity_signals_path=args.commodity_signals,
            output_path=args.output,
            detail_output_path=args.detail_output,
            commodity=args.commodity,
            return_column=args.return_column,
            horizons=args.horizon,
            activation_z=args.activation_z,
            regime_dimensions=args.regime_dimension,
            min_removed_event_count=args.min_removed_event_count,
            min_holdout_event_count=args.min_holdout_event_count,
            max_removed_event_share=args.max_removed_event_share,
            max_mean_drop_ratio=args.max_mean_drop_ratio,
            curve_z_threshold=args.curve_z_threshold,
            price_share_threshold=args.price_share_threshold,
            vol_z_threshold=args.vol_z_threshold,
            momentum_z_threshold=args.momentum_z_threshold,
            macro_regime_path=args.macro_regime,
        )
        counts = (
            summary["adversarial_verdict"].value_counts().to_dict()
            if "adversarial_verdict" in summary
            else {}
        )
        print(
            f"Wrote {len(summary):,} regime adversarial rows to {args.output} "
            f"and {len(detail):,} detail rows to {args.detail_output}; verdicts: {counts}"
        )
        return

    if args.command == "audit-basket-regime-adversarial":
        summary, events = build_basket_regime_adversarial_audit_from_paths(
            candidates_path=args.candidates,
            cache_path=args.cache,
            commodity_signals_path=args.commodity_signals,
            output_path=args.output,
            events_output_path=args.events_output,
            commodity=args.commodity,
            return_column=args.return_column,
            horizon=args.horizon,
            activation_z=args.activation_z,
            regime_dimensions=args.regime_dimension,
            min_removed_event_count=args.min_removed_event_count,
            min_holdout_event_count=args.min_holdout_event_count,
            max_removed_event_share=args.max_removed_event_share,
            max_mean_drop_ratio=args.max_mean_drop_ratio,
            curve_z_threshold=args.curve_z_threshold,
            price_share_threshold=args.price_share_threshold,
            vol_z_threshold=args.vol_z_threshold,
            momentum_z_threshold=args.momentum_z_threshold,
        )
        counts = (
            summary["adversarial_verdict"].value_counts().to_dict()
            if "adversarial_verdict" in summary
            else {}
        )
        print(
            f"Wrote {len(summary):,} basket regime adversarial rows to {args.output} "
            f"and {len(events):,} basket event days to {args.events_output}; verdicts: {counts}"
        )
        return

    if args.command == "audit-basket-state-filter":
        audit = build_basket_state_filter_audit_from_paths(
            events_path=args.events,
            output_path=args.output,
            regime_dimension=args.regime_dimension,
            horizon=args.horizon,
            min_nonoverlap_events=args.min_nonoverlap_events,
            min_nonoverlap_t_stat=args.min_nonoverlap_t_stat,
        )
        counts = audit["filter_verdict"].value_counts().to_dict() if "filter_verdict" in audit else {}
        print(f"Wrote {len(audit):,} basket state-filter rows to {args.output}; verdicts: {counts}")
        return

    if args.command == "audit-exposure-taxonomy":
        summary, unmapped = audit_exposure_taxonomy_from_paths(
            exposure_map_path=args.exposure_map,
            role_taxonomy_path=args.role_taxonomy,
            candidates_path=args.candidates,
            output_path=args.output,
            unmapped_output_path=args.unmapped_output,
        )
        print(
            f"Wrote {len(summary):,} exposure taxonomy rows to {args.output} "
            f"and {len(unmapped):,} unmapped candidate rows to {args.unmapped_output}"
        )
        return

    if args.command == "review-candidate-taxonomy":
        review = review_candidate_taxonomy_from_paths(
            candidates_path=args.candidates,
            exposure_map_path=args.exposure_map,
            role_taxonomy_path=args.role_taxonomy,
            output_path=args.output,
            mechanism_alignment_path=args.mechanism_alignment,
            min_mechanism_alignment_probability=args.min_mechanism_alignment_probability,
            mechanism_review_band=args.mechanism_review_band,
        )
        taxonomy_counts = review["taxonomy_verdict"].value_counts().to_dict() if "taxonomy_verdict" in review else {}
        gate_counts = (
            review["candidate_gate_verdict"].value_counts().to_dict()
            if "candidate_gate_verdict" in review
            else {}
        )
        print(
            f"Wrote {len(review):,} candidate taxonomy review rows to {args.output}; "
            f"taxonomy verdicts: {taxonomy_counts}; candidate gate verdicts: {gate_counts}"
        )
        return

    if args.command == "study-registry-turnover":
        summary, detail = registry_turnover_from_paths(
            output_path=args.output,
            detail_output_path=args.detail_output,
            registry_paths=args.registry,
            reactions_path=args.reactions,
            universe_path=args.universe,
            min_events=args.min_events,
            min_abs_t=args.min_abs_t,
            min_same_direction_horizons=args.min_same_direction_horizons,
        )
        print(
            f"Wrote {len(summary):,} turnover summary rows to {args.output} "
            f"and {len(detail):,} detail rows to {args.detail_output}"
        )
        return

    if args.command == "build-group-activation-scores":
        scores = group_activation_scores_from_paths(
            registry_path=args.registry,
            commodity_signals_path=args.commodity_signals,
            exposure_map_path=args.exposure_map,
            output_path=args.output,
            as_of_date=args.as_of_date,
            activation_z=args.activation_z,
            feature_z_window=args.feature_z_window,
            min_feature_observations=args.min_feature_observations,
            require_exposure=not args.allow_unmapped,
        )
        print(f"Wrote {len(scores):,} group activation score rows to {args.output}")
        return

    if args.command == "consolidate-candidate-signals":
        consolidated = consolidate_candidate_signals_from_paths(
            candidates_path=args.candidates,
            forecast_audit_path=args.forecast_audit,
            reviewed_features_path=args.reviewed_features,
            mechanism_alignment_path=args.mechanism_alignment,
            output_path=args.output,
            min_confidence=args.min_confidence,
            require_audit_candidate=args.require_audit_candidate,
            require_mechanism_pass=args.require_mechanism_pass,
            block_mechanism_conflicts=args.block_mechanism_conflicts,
            min_mechanism_alignment_probability=args.min_mechanism_alignment_probability,
            mechanism_review_band=args.mechanism_review_band,
            min_same_direction_share=args.min_same_direction_share,
            min_peer_direction_share=args.min_peer_direction_share,
            max_per_ticker=args.max_per_ticker,
        )
        print(f"Wrote {len(consolidated):,} consolidated candidate signal rows to {args.output}")
        return

    if args.command == "build-stock-feature-matrix":
        matrix = build_stock_feature_matrix_from_paths(
            signals_path=args.signals,
            output_path=args.output,
            source=args.source,
        )
        print(f"Wrote {len(matrix):,} stock-feature matrix rows to {args.output}")
        return

    if args.command == "build-stock-feature-matrix-cache":
        matrix = build_stock_feature_matrix_cache_from_paths(
            reactions_path=args.reactions,
            universe_path=args.universe,
            forecast_audit_path=args.forecast_audit,
            reviewed_features_path=args.reviewed_features,
            output_path=args.output,
            min_events=args.min_events,
            min_abs_t=args.min_abs_t,
            min_same_direction_horizons=args.min_same_direction_horizons,
            min_confidence=args.min_confidence,
            require_audit_candidate=args.require_audit_candidate,
            min_same_direction_share=args.min_same_direction_share,
            min_peer_direction_share=args.min_peer_direction_share,
            max_per_ticker=args.max_per_ticker,
            source=args.source,
        )
        print(f"Wrote {len(matrix):,} stock-feature matrix cache rows to {args.output}")
        return

    if args.command == "build-stock-feature-curve-diagnostics":
        annual, regime, time_regime, summary = build_matrix_curve_diagnostics_from_paths(
            matrix_path=args.matrix,
            as_of_date=args.as_of_date,
            output_annual_path=args.output_annual,
            output_regime_path=args.output_regime,
            output_time_regime_path=args.output_time_regime,
            output_summary_path=args.output_summary,
            ticker=args.ticker,
            commodity=args.commodity,
            feature=args.feature,
            start=args.start,
            end=args.end,
            return_column=args.return_column,
            activation_z=args.activation_z,
            exit_z=args.exit_z,
            position_mode=args.position_mode,
            transaction_cost_bps=args.transaction_cost_bps,
        )
        print(
            f"Wrote {len(annual):,} annual diagnostic rows to {args.output_annual} "
            f"{len(regime):,} regime diagnostic rows to {args.output_regime}, "
            f"{len(time_regime):,} time-regime rows to {args.output_time_regime}, "
            f"and {len(summary):,} stability summary rows to {args.output_summary}"
        )
        return

    if args.command == "classify-commodity-environment":
        summary, detail = commodity_environment_similarity_from_paths(
            symbol=args.symbol,
            commodity_signals_path=args.commodity_signals,
            output_summary_path=args.output_summary,
            output_detail_path=args.output_detail,
            as_of_date=args.as_of_date,
            start=args.start,
            current_window_days=args.current_window_days,
            features=args.feature,
            min_regime_observations=args.min_regime_observations,
        )
        closest = "n/a"
        if not summary.empty:
            closest = str(summary.sort_values("rank").iloc[0]["time_regime"])
        print(
            f"Wrote {len(summary):,} environment summary rows to {args.output_summary}, "
            f"{len(detail):,} detail rows to {args.output_detail}; closest regime: {closest}"
        )
        return

    if args.command == "build-feature-trade-candidates":
        stability_paths = args.stability_summary or [
            Path("data/processed/cl_curve_stability_summary.csv"),
            Path("data/processed/hg_curve_stability_summary.csv"),
        ]
        candidates = build_feature_trade_candidates_from_paths(
            matrix_path=args.matrix,
            stability_summary_paths=stability_paths,
            output_path=args.output,
            as_of_date=args.as_of_date,
            commodities=args.commodity,
            themes=args.theme,
            commodity_signals_path=args.commodity_signals,
            environment_start=args.environment_start,
            environment_window_days=args.environment_window_days,
            max_per_commodity=args.max_per_commodity,
            max_per_theme=args.max_per_theme,
            min_post_covid_active_median_return=args.min_post_covid_active_median_return,
        )
        eligible = int(candidates["eligible"].sum()) if "eligible" in candidates.columns else 0
        print(f"Wrote {len(candidates):,} feature trade candidates to {args.output}; eligible: {eligible:,}")
        return

    if args.command == "run-feature-basket-backtest":
        daily, weights, summary = run_feature_basket_backtest_from_paths(
            candidates_path=args.candidates,
            matrix_path=args.matrix,
            output_daily_path=args.output_daily,
            output_weights_path=args.output_weights,
            output_summary_path=args.output_summary,
            as_of_date=args.as_of_date,
            commodity_signals_path=args.commodity_signals,
            beta_returns_path=args.beta_returns,
            start=args.start,
            end=args.end,
            return_column=args.return_column,
            activation_z=args.activation_z,
            position_mode=args.position_mode,
            transaction_cost_bps=args.transaction_cost_bps,
            max_pair_weight=args.max_pair_weight,
            target_gross=args.target_gross,
            rebalance_frequency=args.rebalance_frequency,
            eligible_only=not args.include_ineligible,
            label=args.label,
        )
        sharpe = "n/a" if summary.empty else f"{float(summary.iloc[0]['sharpe']):.2f}"
        calmar = "n/a" if summary.empty else f"{float(summary.iloc[0]['calmar']):.2f}"
        print(
            f"Wrote {len(daily):,} basket daily rows to {args.output_daily}, "
            f"{len(weights):,} weight rows to {args.output_weights}, "
            f"and summary to {args.output_summary}; sharpe: {sharpe}, calmar: {calmar}"
        )
        return

    if args.command == "build-precision-event-candidates":
        candidates = build_precision_event_candidates_from_paths(
            candidates_path=args.candidates,
            commodity_signals_path=args.commodity_signals,
            exposure_map_path=args.exposure_map,
            role_taxonomy_path=args.role_taxonomy,
            falsification_audit_path=args.falsification_audit,
            shortability_path=args.shortability,
            output_path=args.output,
            as_of_date=args.as_of_date,
            require_trigger=not args.no_require_trigger,
            allow_low_priority_roles=args.allow_low_priority_roles,
            max_names=args.max_names,
        )
        counts = candidates["precision_verdict"].value_counts().to_dict() if "precision_verdict" in candidates else {}
        print(f"Wrote {len(candidates):,} precision event candidates to {args.output}; verdicts: {counts}")
        return

    if args.command == "build-fundamental-snapshot":
        snapshot, factors = build_fundamental_snapshot_from_paths(
            openbb_metrics_path=args.openbb_metrics,
            edgar_factors_path=args.edgar_factors,
            exposure_map_path=args.exposure_map,
            role_taxonomy_path=args.role_taxonomy,
            output_snapshot_path=args.output_snapshot,
            output_factors_path=args.output_factors,
            min_market_cap=args.min_market_cap,
        )
        gates = snapshot["fundamental_gate"].value_counts().to_dict() if "fundamental_gate" in snapshot else {}
        print(
            f"Wrote {len(snapshot):,} fundamental snapshot rows to {args.output_snapshot}, "
            f"{len(factors):,} factor rows to {args.output_factors}; gates: {gates}"
        )
        return

    if args.command == "build-agriculture-fundamental-events":
        events = build_agriculture_fundamental_events_from_paths(
            nass_factors_path=args.nass_factors,
            usda_report_factors_path=args.usda_report_factors,
            output_path=args.output,
            usda_tradable_hour_utc=args.usda_tradable_hour_utc,
        )
        counts = events["source_type"].value_counts().to_dict() if "source_type" in events else {}
        print(f"Wrote {len(events):,} agriculture fundamental event rows to {args.output}; sources: {counts}")
        return

    if args.command == "build-commodity-confirmation-events":
        events = build_commodity_confirmation_events_from_paths(
            eia_factors_path=args.eia_factors,
            cftc_factors_path=args.cftc_factors,
            output_path=args.output,
            commodity=args.commodity,
            eia_tradable_lag_days=args.eia_tradable_lag_days,
            cftc_tradable_lag_days=args.cftc_tradable_lag_days,
        )
        counts = events["source_type"].value_counts().to_dict() if "source_type" in events else {}
        print(f"Wrote {len(events):,} commodity confirmation rows to {args.output}; sources: {counts}")
        return

    if args.command == "research-commodity-features":
        commodity_code = args.commodity.upper().strip()
        output_dir = args.output_dir or Path(f"data/research/feature_selection/{commodity_code}")
        candidate_scores, selected, blocked, role_results = research_commodity_features_from_paths(
            commodity=commodity_code,
            matrix_dir=args.matrix_dir,
            manifest_path=args.manifest,
            diagnostic_matrix_dir=args.diagnostic_matrix_dir,
            diagnostic_manifest_path=args.diagnostic_manifest,
            exposure_map_path=args.exposure_map,
            role_taxonomy_path=args.role_taxonomy,
            reviewed_features_path=args.reviewed_features,
            output_dir=output_dir,
            quarters=args.quarter,
            include_unreviewed_features=args.include_unreviewed_features,
            target_return_column=args.target_return_column,
            diagnostic_target_return_column=args.diagnostic_target_return_column,
            min_abs_t=args.min_abs_t,
            min_nonoverlap_abs_t=args.min_nonoverlap_abs_t,
            min_effective_observations=args.min_effective_observations,
            min_hit_rate_edge=args.min_hit_rate_edge,
            min_sign_stability=args.min_sign_stability,
            commodity_neutral_min_ratio=args.commodity_neutral_min_ratio,
            verbose=args.verbose,
            progress_interval=args.progress_interval,
        )
        verdicts = (
            candidate_scores["selection_verdict"].value_counts().to_dict()
            if "selection_verdict" in candidate_scores
            else {}
        )
        print(
            f"Wrote {len(candidate_scores):,} {commodity_code} candidate score rows to {output_dir}; "
            f"selected: {len(selected):,}, blocked: {len(blocked):,}, "
            f"trigger-role rows: {len(role_results):,}, verdicts: {verdicts}"
        )
        return

    if args.command == "select-curve-first-candidates":
        commodity_code = args.commodity.upper().strip()
        selected_output = args.selected_output or args.output.with_name(
            f"{args.output.stem}-selected{args.output.suffix}"
        )
        scored, selected = select_curve_first_candidates_from_paths(
            matrix_dir=args.matrix_dir,
            cache_path=args.cache,
            output_path=args.output,
            selected_output_path=selected_output,
            commodity=commodity_code,
            quarters=args.quarter,
            lookback_years=args.lookback_years,
            target_return_column=args.target_return_column,
            activation_z=args.activation_z,
            allowed_states=args.allowed_state,
            min_nonoverlap_abs_t=args.min_nonoverlap_abs_t,
            min_effective_observations=args.min_effective_observations,
            min_robust_calmar=args.min_robust_calmar,
            max_dominant_year_share=args.max_dominant_year_share,
            max_candidates=args.max_candidates,
        )
        verdicts = (
            scored["v3_selected"].value_counts(dropna=False).to_dict()
            if "v3_selected" in scored
            else {}
        )
        print(
            f"Wrote {len(scored):,} curve-first scored rows to {args.output}; "
            f"selected {len(selected):,} rows to {selected_output}; verdicts: {verdicts}"
        )
        return

    if args.command == "review-curve-first-taxonomy":
        reviewed = review_curve_first_taxonomy_from_paths(
            candidates_path=args.candidates,
            exposure_map_path=args.exposure_map,
            role_taxonomy_path=args.role_taxonomy,
            output_path=args.output,
            block_low_priority=args.block_low_priority,
        )
        counts = (
            reviewed["v3_taxonomy_verdict"].value_counts(dropna=False).to_dict()
            if "v3_taxonomy_verdict" in reviewed
            else {}
        )
        print(f"Wrote {len(reviewed):,} curve-first taxonomy review rows to {args.output}; verdicts: {counts}")
        return

    if args.command == "run-curve-first-oos":
        return_columns = args.return_column or [
            "raw_return",
            "residual_return_mktsec_w12m",
            "residual_return_mktseccomm_w12m",
        ]
        verdicts = args.verdict or ["pass"]
        events, daily, summary = run_curve_first_oos_from_paths(
            taxonomy_paths=args.taxonomy,
            cache_path=args.cache,
            events_output_path=args.events_output,
            daily_output_path=args.daily_output,
            summary_output_path=args.summary_output,
            verdicts=verdicts,
            return_columns=return_columns,
            activation_z=args.activation_z,
            weighting=args.weighting,
            collapse_same_ticker_state=not args.no_collapse_same_ticker_state,
            oos_mode=args.oos_mode,
            oos_end_quarter=args.oos_end_quarter,
        )
        print(
            f"Wrote {len(events):,} OOS events to {args.events_output}, "
            f"{len(daily):,} daily rows to {args.daily_output}, "
            f"and {len(summary):,} summary rows to {args.summary_output}"
        )
        if not summary.empty:
            show_cols = [
                "oos_quarter",
                "event_count",
                "ticker_count",
                "pnl__residual_return_mktsec_w12m_total_pnl",
                "pnl__residual_return_mktsec_w12m_sharpe",
                "pnl__residual_return_mktsec_w12m_calmar",
                "pnl__residual_return_mktsec_w12m_max_drawdown",
            ]
            print(summary[[col for col in show_cols if col in summary.columns]].to_string(index=False))
        return

    if args.command == "summarize-cross-product-clusters":
        commodity_code = args.commodity.upper().strip()
        trigger_path = args.trigger_role_results or Path(
            f"data/research/feature_selection/{commodity_code}/trigger_role_results.csv"
        )
        output_path = args.output or Path(f"data/research/feature_selection/{commodity_code}/cluster_summary.csv")
        detail_output_path = args.detail_output or Path(
            f"data/research/feature_selection/{commodity_code}/cross_product_cluster_detail.csv"
        )
        if args.include_direct_oil_roles:
            excluded_roles = []
        elif args.exclude_role is not None:
            excluded_roles = args.exclude_role
        else:
            excluded_roles = list(DEFAULT_DIRECT_OIL_ROLES)
        summary, detail = summarize_cross_product_clusters_from_paths(
            trigger_role_results_path=trigger_path,
            output_path=output_path,
            detail_output_path=detail_output_path,
            min_keep_count=args.min_keep_count,
            excluded_roles=excluded_roles,
        )
        print(
            f"Wrote {len(summary):,} cluster summary rows to {output_path} "
            f"and {len(detail):,} cross-product detail rows to {detail_output_path}"
        )
        if not summary.empty:
            print("\nTop cluster families:")
            print(summary.head(args.top).to_string(index=False))
        if not detail.empty:
            print("\nTop cross-product clusters:")
            detail_cols = [
                "quarter",
                "feature",
                "feature_family",
                "horizon_days",
                "exposure_role",
                "candidate_count",
                "keep_count",
                "median_selection_score",
                "median_nonoverlap_abs_t_stat",
                "dominant_direction",
                "tickers",
            ]
            print(detail[[col for col in detail_cols if col in detail.columns]].head(args.top).to_string(index=False))
        return

    if args.command == "summarize-state-role-clusters":
        summary, detail = summarize_state_role_clusters_from_paths(
            candidates_path=args.candidates,
            output_path=args.output,
            detail_output_path=args.detail_output,
            min_keep_count=args.min_keep_count,
            include_weak_keep=not args.keep_only,
        )
        print(
            f"Wrote {len(summary):,} state-role summary rows to {args.output} "
            f"and {len(detail):,} detail rows to {args.detail_output}"
        )
        if not summary.empty:
            print("\nTop state-role clusters:")
            cols = [
                "commodity",
                "state_hypothesis",
                "exposure_role",
                "horizon_days",
                "quarters",
                "total_keep",
                "median_feature_count",
                "supporting_features",
                "median_score",
                "median_t",
                "dominant_direction",
                "tickers",
            ]
            print(summary[[col for col in cols if col in summary.columns]].head(args.top).to_string(index=False))
        return

    if args.command == "build-edgar-filing-cache":
        tickers = [t.strip().upper() for t in args.tickers.split(",") if t.strip()]
        if args.tickers_file:
            file_tickers = [
                line.strip().upper()
                for line in args.tickers_file.read_text(encoding="utf-8").splitlines()
                if line.strip() and not line.strip().startswith("#")
            ]
            tickers = sorted(set(tickers + file_tickers))
        if not tickers:
            raise ValueError("build-edgar-filing-cache requires --tickers or --tickers-file")
        form_types = tuple(sorted({f.strip() for f in args.form_types.split(",") if f.strip()}))
        output_dir: Path = args.output_dir

        print(f"Resolving CIKs for {len(tickers)} tickers ...")
        cik_map = fetch_company_tickers(cache_path=output_dir / "company_tickers.json")
        found = [t for t in tickers if t in cik_map]
        missing = [t for t in tickers if t not in cik_map]
        if missing:
            print(f"  Warning: {len(missing)} tickers not found in SEC CIK map: {', '.join(sorted(missing))}")
        print(f"  Found CIKs for {len(found)}/{len(tickers)} tickers")

        index_path = args.index_cache or (output_dir / "filing_index.csv")
        if not args.skip_index:
            print(f"Building filing index for {form_types} from {args.start_year} ...")
            index, _ = build_filing_index(
                tickers=found,
                cik_map=cik_map,
                form_types=form_types,
                start_year=args.start_year,
                cache_dir=output_dir,
            )
            output_dir.mkdir(parents=True, exist_ok=True)
            index.to_csv(index_path, index=False)
            print(f"  Saved {len(index)} filing entries to {index_path}")
            for ticker in sorted(index["ticker"].unique()):
                tdf = index[index["ticker"] == ticker]
                print(f"    {ticker}: {len(tdf)} filings ({tdf['fiscal_year'].min():.0f}-{tdf['fiscal_year'].max():.0f})")
        else:
            print(f"Loading existing index from {index_path}")
            import pandas as pd
            index = pd.read_csv(index_path)
            print(f"  Loaded {len(index)} filing entries")

        if not args.skip_download:
            print(f"Downloading filings to {output_dir / 'filings'} ...")
            stats = download_filings(
                index, output_dir, form_types=form_types, dry_run=args.dry_run
            )
            if args.dry_run:
                print(
                    f"  [DRY RUN] Would download {stats['would_download']}, "
                    f"already cached {stats['skipped']}"
                )
            else:
                print(f"  Downloaded {stats['downloaded']}, skipped {stats['skipped']}, failed {stats['failed']}")

        print("Done.")

    if args.command == "extract-edgar-sections":
        tickers = [t.strip().upper() for t in args.tickers.split(",") if t.strip() and not t.strip().startswith("@")]
        form_types = [f.strip() for f in args.form_types.split(",") if f.strip()]
        section_ids = [s.strip() for s in args.sections.split(",") if s.strip()] if args.sections else []
        filings_dir: Path = args.filings_dir
        output_dir: Path = args.output_dir
        year = args.year

        output_dir.mkdir(parents=True, exist_ok=True)
        found_any = False
        for ticker in tickers:
            for form_type in form_types:
                path = filings_dir / ticker / form_type / f"{year}.txt"
                if not path.exists():
                    continue
                text = path.read_text(encoding="utf-8", errors="replace")
                sections = extract_form_sections(text, form_type, item_ids=tuple(section_ids) if section_ids else None)
                if not sections:
                    continue
                found_any = True
                ticker_out = output_dir / ticker / form_type / str(year)
                ticker_out.mkdir(parents=True, exist_ok=True)
                for item_id, content in sections.items():
                    out_path = ticker_out / f"Item_{item_id}.txt"
                    out_path.write_text(content, encoding="utf-8")
                    if args.print_stdout:
                        print(f"\n===== {ticker} {form_type} Item {item_id} ({len(content):,} chars) =====\n")
                        print(content[:2000])
                        if len(content) > 2000:
                            print(f"\n... ({len(content) - 2000:,} more chars)")
                    else:
                        print(f"  {ticker:6s} {form_type:4s} Item {item_id}: {len(content):>8,d} chars -> {out_path}")
        if not found_any:
            print(f"No sections found for tickers={tickers} forms={form_types} year={year}")
        else:
            print(f"Extracted sections to {output_dir}")
        return
        return

    parser.error(f"Unknown command: {args.command}")
