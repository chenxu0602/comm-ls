"""Additive target entrypoints preserving legacy signals/execution code.

The legacy generator is reused through scoped function hooks, restored on exit.
Only its beta provider changes. The shared explicit engine then verifies every
continuous ETF target before this new package is handed off.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import importlib
from pathlib import Path
import sys

import numpy as np
import pandas as pd

from comm_ls.residual_beta_hedge import (
    BETA_MODE, DEFAULT_PANEL, ResidualBetaStore, beta_notes, return_method,
    snapshot_hedges,
)

OUTPUT_ROOTS = {"cl": "targets-cl-cached-beta", "metals": "targets-metals-cached-beta",
                "crypto": "targets-crypto-cached-beta"}
PROTECTED_ROOTS = [Path(p).resolve() for p in
                   ["targets", "targets-cl", "targets-metals", "targets-crypto", "targets-agri"]]


def check_new_output(path: Path):
    resolved = path.resolve()
    if any(resolved == root or root in resolved.parents for root in PROTECTED_ROOTS):
        raise ValueError(f"Cached-beta comparison must use a separate output directory: {path}")


@contextmanager
def scoped_hooks(module, **hooks):
    previous = {name: getattr(module, name) for name in hooks}
    try:
        for name, value in hooks.items():
            setattr(module, name, value)
        yield
    finally:
        for name, value in previous.items():
            setattr(module, name, value)


class CachedBetaProvider:
    def __init__(self, store: ResidualBetaStore, strategy: str, as_of, market="SPY"):
        self.store, self.strategy = store, strategy
        self.as_of = pd.Timestamp(as_of).normalize()
        self.market = market.upper()
        self.sources = []

    def two_factor(self, stock, market, sector, window=252, min_obs=126):
        ticker = str(stock.name)
        if ticker not in self.store.histories and self.strategy == "crypto":
            # The existing Crypto generator renames concat columns to stock/
            # market. Recover the unique ticker from its supplied return vector;
            # this validates the input and does not estimate any beta.
            candidates = []
            for name, history in self.store.histories.items():
                expected = history.raw_return.reindex(stock.index)
                if np.allclose(stock.to_numpy(), expected.to_numpy(), atol=1e-12,
                               rtol=0., equal_nan=True):
                    candidates.append(name)
            if len(candidates) != 1:
                raise ValueError(f"Cannot uniquely identify Crypto beta input: {candidates}")
            ticker = candidates[0]
        sector_name = str(sector.name) if sector is not None else None
        method = ("residual_return_mkt_w12m" if sector_name is None and
                  ticker not in {"MUSA", "CASY"} else "residual_return_mktsec_w12m")
        beta = self.store.lookup(ticker, method, self.as_of,
                                 market=self.market, sector=sector_name)
        self.sources.append(beta)
        return beta["market_beta"], beta["sector_beta"], int(beta["beta_observations"])

    def market_only(self, stock, market, window=252, min_obs=126):
        return self.two_factor(stock, market, None, window, min_obs)[0]


def run_targets(strategy: str):
    extra = argparse.ArgumentParser(add_help=False)
    extra.add_argument("--beta-equity", type=Path, default=DEFAULT_PANEL)
    settings, remaining = extra.parse_known_args()
    for option in ("--beta-window", "--beta-min-obs"):
        if any(arg == option or arg.startswith(option + "=") for arg in remaining):
            raise ValueError(f"{option} is not used by cached-beta targets; select --beta-equity")
    module_name = {"cl": "generate_cl_v32_daily_targets",
                   "metals": "generate_metals_daily_targets",
                   "crypto": "generate_crypto_v43_daily_targets"}[strategy]
    module = importlib.import_module(module_name)
    old_parse = module.parse_args
    old_format = module.format_csv_for_display
    captured = {}
    provider = None

    def parse(*args, **kwargs):
        nonlocal provider
        parsed = old_parse(*args, **kwargs)
        if not parsed.as_of or not parsed.target_date:
            raise ValueError("Cached-beta targets require explicit --as-of and --target-date")
        if getattr(parsed, "target_file", None) is not None:
            raise ValueError("Use --output-dir for the isolated cached-beta package")
        if not any(arg == "--output-dir" or arg.startswith("--output-dir=") for arg in remaining):
            parsed.output_dir = Path(OUTPUT_ROOTS[strategy])
        check_new_output(parsed.output_dir)
        captured["args"] = parsed
        provider = CachedBetaProvider(ResidualBetaStore.from_path(settings.beta_equity),
                                      strategy, parsed.as_of, parsed.market_hedge)
        return parsed

    def formatted(frame):
        # Capture full precision in-memory tables before legacy CSV display rounding.
        if {"instrument_type", "post_child_shares", "executable_hedge_target_weight"}.issubset(frame):
            if len(frame) > len(captured.get("targets", [])):
                captured["targets"] = frame.copy()
        if {"beta_observations", "market_beta", "component", "target_weight"}.issubset(frame) and "instrument_type" not in frame:
            if len(frame) > len(captured.get("betas", [])):
                captured["betas"] = frame.copy()
        return old_format(frame)

    def two_factor(*args, **kwargs):
        return provider.two_factor(*args, **kwargs)

    def market_only(*args, **kwargs):
        return provider.market_only(*args, **kwargs)

    hooks = {"parse_args": parse, "format_csv_for_display": formatted}
    hooks["market_only_beta" if strategy == "crypto" else "two_factor_beta"] = (
        market_only if strategy == "crypto" else two_factor)
    original_argv = sys.argv
    try:
        sys.argv = [original_argv[0], *remaining]
        with scoped_hooks(module, **hooks):
            if strategy == "cl":
                from comm_ls.cl_cro import CRO_CONFIG, CRO_EFFECTIVE_DATE
                from comm_ls.cl_v43_strategy import (
                    CL_V43_CACHE_SUFFIX, CL_V43_FEATURE_ALIGNMENT_MODE,
                    CL_V43_MAX_SINGLE_NAME_WEIGHT, CL_V43_SHIPPING_VETO_CONFIG,
                    CL_V43_SLEEVE_CONFIG,
                )
                module.main(
                    config=CL_V43_SLEEVE_CONFIG,
                    strategy_label="CL v4.3 (notebook cached beta)",
                    max_single_name_weight=CL_V43_MAX_SINGLE_NAME_WEIGHT,
                    default_signals_path=Path("data/processed/commodity_signals_2.parquet"),
                    default_feature_cache_dir=Path("data/cache/feature_return_observation_v1"),
                    default_cache_suffix=CL_V43_CACHE_SUFFIX,
                    required_cache_suffix=CL_V43_CACHE_SUFFIX,
                    required_feature_alignment_mode=CL_V43_FEATURE_ALIGNMENT_MODE,
                    require_feature_cache=True, shipping_veto_config=CL_V43_SHIPPING_VETO_CONFIG,
                    live_suspensions={"fuel": "2026-09-17", "metals": "2026-09-17"},
                    live_additions={"cro": (CRO_EFFECTIVE_DATE, CRO_CONFIG)},
                )
            else:
                module.main()
    finally:
        sys.argv = original_argv

    args = captured["args"]
    targets, betas = captured["targets"], captured["betas"]
    legs = betas.copy()
    if "sector_hedge" not in legs:
        legs["sector_hedge"] = ""
    legs["return_method"] = [return_method(strategy, str(row.component)) for row in legs.itertuples()]
    expected, detail = snapshot_hedges(legs, provider.store, args.as_of)
    actual = targets.loc[targets.instrument_type.eq("hedge")].set_index("instrument").target_weight
    delta = actual.subtract(expected, fill_value=0.0)
    if delta.abs().max() > 1e-12:
        raise AssertionError(f"Daily target differs from shared explicit engine: {delta.to_dict()}")
    output = args.output_dir / str(args.target_date)
    source_columns = ["instrument", "return_method", "market_hedge", "sector_hedge",
                      "market_beta", "sector_beta", "beta_observations", "beta_source_date",
                      "beta_estimation_end", "beta_source_path", "beta_mode"]
    sources = pd.DataFrame(provider.sources, columns=source_columns).drop_duplicates(
        ["instrument", "return_method"])
    sources.to_csv(output / "beta_sources.csv", index=False, float_format="%.12g")
    # Replace only this new package's rounded display beta table with exact provenance.
    metadata = ["beta_source_date", "beta_estimation_end", "beta_source_path", "beta_mode"]
    full_betas = legs.merge(sources[["instrument", "return_method", *metadata]],
                            on=["instrument", "return_method"], how="left", validate="many_to_one")
    full_betas["beta_mode"] = BETA_MODE
    full_betas["beta_source_path"] = str(settings.beta_equity)
    full_betas.to_csv(output / "betas.csv", index=False, float_format="%.12g")
    notes = beta_notes(str(settings.beta_equity))
    (output / "beta_notes.md").write_text(notes, encoding="utf-8")
    notes_path = output / "strategy_notes.md"
    old_notes = notes_path.read_text() if notes_path.exists() else ""
    notes_path.write_text(old_notes + "\n" + notes, encoding="utf-8")
    report = output / "report.md"
    report.write_text(report.read_text() + "\n" + notes, encoding="utf-8")
    new_targets = pd.read_csv(output / "targets.csv")
    new_targets["beta_mode"] = BETA_MODE
    new_targets["beta_source_path"] = str(settings.beta_equity)
    new_targets.to_csv(output / "targets.csv", index=False)
    print(f"Verified shared explicit hedge engine; beta notes written to {output}")
