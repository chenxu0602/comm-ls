# comm-ls

`comm-ls` is a research scaffold for studying commodity-triggered equity
long/short strategies.

The project is designed around a simple research question:

> When a commodity market enters an unusual state, which commodity-linked
> equities react in a persistent, economically explainable way after broad
> market and sector effects are controlled?

This repository contains the code framework: data loaders, feature builders,
universe construction, return residualization, reaction studies, candidate
audits, and simple portfolio/backtest utilities. It does not ship private data,
private feature lists, production trading configuration, or research outputs.

This is research infrastructure, not an investment product or trading signal
service.

## What This Project Does

The framework supports a full research workflow:

- Build daily commodity feature panels from futures/carry data.
- Download prototype equity data from yfinance.
- Build quarterly liquidity-filtered equity universes.
- Estimate market, sector, and diagnostic commodity betas.
- Study how equities react after commodity feature shocks.
- Build candidate ticker-feature mappings.
- Audit candidates for overfitting, missing economic exposure, and taxonomy
  problems.
- Build simple long/short or index-hedged portfolios for research backtests.
- Normalize optional fundamental/confirmation data from external research
  pipelines.

The code is intentionally modular. Most commands read CSV/Parquet inputs and
write CSV/Parquet outputs under `data/`, which is ignored by Git.

## Core Concepts

The project separates the research problem into a few explicit layers:

- **Commodity state**: daily features built from futures/carry data, such as
  trend, curve shape, carry, volatility, and contract activity diagnostics.
- **Equity universe**: commodity-linked stocks filtered by liquidity and
  refreshed on a quarterly schedule.
- **Exposure taxonomy**: a manual mapping from stock to commodity role, for
  example producer, consumer, service provider, refiner, industrial user, or
  macro proxy.
- **Return target**: raw stock return and residual returns after removing broad
  market, sector, and optionally mapped commodity beta.
- **Candidate mapping**: ticker-feature pairs that pass statistical and
  economic-exposure checks.
- **Portfolio expression**: simple research portfolios, either single-name
  long/short or long names hedged with an index/ETF.

The intended use is selective research. The code is built to help answer
whether a commodity shock transmits into a particular group of equities, not to
force continuous market exposure.

## Public vs Private Files

This public repository is configured to keep strategy-sensitive files private.

Ignored by default:

- `data/`: raw data, processed panels, candidate files, matrices, backtests.
- `config/*.csv`: private universes, exposure maps, feature lists, hedge maps.
- `docs/`: private methodology notes and internal research documentation.
- `notebooks/`: notebook outputs and ad hoc experiments.
- `AGENTS.md`, `.agents/`, `.codex/`: local agent instructions.

Tracked by default:

- `src/comm_ls/`: Python package and CLI implementation.
- `README.md`: public project overview.
- `pyproject.toml`, `uv.lock`: package and dependency metadata.
- `.gitignore`: public/private boundary.

If you want to publish examples, use sanitized files such as:

```text
config/example_universe.example.csv
data/sample/sample_prices.csv
docs/public/overview.md
notebooks/demo.public.ipynb
```

## Installation

This project uses `uv`.

```bash
git clone <your-repo-url>
cd comm-ls
uv sync
```

Check that the CLI is available:

```bash
uv run comm-ls --help
```

Python requirement:

```text
>=3.13
```

Core dependencies include `pandas`, `numpy`, `pyarrow`, `yfinance`, `ib-insync`,
and `ruff`.

## Data Layout

The code expects local data and research outputs in this general shape:

```text
data/
  comm/
    carry_data/          # chained commodity/carry files
    <SYMBOL>/            # individual futures contract files
  equity/
    yfinance/            # downloaded prototype equity price files
  processed/             # generated research outputs
  cache/                 # generated caches
  matrix/                # generated stock-feature matrices
  sensitivity/           # generated sensitivity studies

config/
  *.csv                  # private universes, exposure maps, feature lists
```

The exact schema depends on the command being run. This public repo does not
include the private datasets or private configs.

## Required Private Inputs

The public code expects several local CSV/Parquet inputs. The filenames below
are conventional defaults; the actual files are intentionally ignored.

| Input | Default path | Purpose |
| --- | --- | --- |
| Seed equity universe | `config/us_commodity_equity_seed.csv` | Starting list of tickers, themes, exchanges, and optional metadata. |
| Commodity exposure map | `config/commodity_exposure_map.csv` | Maps each ticker to commodity exposure, role, and prior direction/weight. |
| Theme hedge map | `config/theme_sector_hedges.csv` | Maps equity themes to sector/index hedge instruments. |
| Reviewed feature list | `config/reviewed_commodity_features.csv` | Optional allowlist/metadata for features that passed manual review. |
| Futures/carry data | `data/comm/` | Local commodity futures and chained carry panels. |
| Equity prices | `data/equity/yfinance/` | Prototype adjusted equity history downloaded from yfinance. |

Typical config columns:

```text
seed universe:
  ticker, exchange, name, theme

commodity exposure map:
  ticker, commodity, role, prior_weight, notes

theme hedge map:
  theme, hedge_ticker
```

The code is permissive about extra columns. Private research columns can be kept
locally without changing the public package.

## Commodity Contract Handling

Commodity futures are not interchangeable across symbols. The feature builder
contains machinery for contract-aware curve features, and research should avoid
assuming that one calendar month is always the correct deferred anchor.

Examples:

- Some commodities trade actively in every listed month.
- Some metals concentrate liquidity in specific delivery months.
- Near expiration, the most liquid contract can switch before the nominal front
  contract fully expires.

For deferred-curve features, prefer commodity-specific liquid-contract
selection unless the hypothesis explicitly requires a named calendar month.

## Typical Research Flow

The commands below show the intended workflow. They require private input files
under `data/` and `config/`.

### 1. Build Commodity Features

```bash
uv run comm-ls build-commodity-signals \
  --input-dir data/comm/carry_data \
  --commodity-dir data/comm \
  --output data/processed/commodity_signals.parquet
```

This produces a daily commodity feature table. The feature builder supports
front-contract returns, curve/carry fields, term-structure regimes, volatility,
participation, and contract-liquidity-aware deferred features.

### 2. Download Prototype Equity Prices

```bash
uv run comm-ls download-equities \
  --universe config/us_commodity_equity_seed.csv \
  --output-dir data/equity/yfinance \
  --start 2000-01-01
```

yfinance is useful for fast iteration, but it is not a production-grade
point-in-time data source.

### 3. Build Processed Equity Returns

```bash
uv run comm-ls build-equity-processed-dataset \
  --prices-dir data/equity/yfinance \
  --universe config/us_commodity_equity_seed.csv \
  --theme-hedges config/theme_sector_hedges.csv \
  --commodity-signals data/processed/commodity_signals.parquet \
  --exposure-map config/commodity_exposure_map.csv \
  --output data/processed/equity_processed.parquet
```

Important return columns:

- `raw_return`: adjusted daily log return.
- `residual_return_mktsec_w12m`: market + sector residual return.
- `residual_return_mktseccomm_w12m`: market + sector + mapped commodity
  residual return for mapped commodity-linked names.

The three-beta residual is a diagnostic target. It helps distinguish
stock-specific alpha from commodity beta transmission.

In practice, run feature selection against multiple targets. If a signal works
on `residual_return_mktsec_w12m` but disappears on
`residual_return_mktseccomm_w12m`, the apparent edge may be mostly commodity
beta rather than stock-specific transmission.

### 4. Build Universes

```bash
uv run comm-ls build-quarterly-universe
uv run comm-ls build-commodity-quarterly-universes
uv run comm-ls build-broad-quarterly-liquidity-universe
```

Universe construction is quarterly and should only use information available at
the rebalance date. The public repo contains the machinery, not the private
universe definitions.

### 5. Run Reaction and Forecast Studies

```bash
uv run comm-ls study-feature-reactions \
  --as-of-date 2026-06-30 \
  --commodity-signals data/processed/commodity_signals.parquet \
  --prices-dir data/equity/yfinance \
  --quarterly-universe data/processed/quarterly_universe.csv

uv run comm-ls study-commodity-forecast \
  --commodity CL \
  --output data/processed/forecast_cl.csv
```

These commands are discovery tools. Their outputs should be audited before
being used in a portfolio.

### 6. Build and Audit Candidates

```bash
uv run comm-ls build-candidate-signals
uv run comm-ls consolidate-candidate-signals
uv run comm-ls audit-sensitivity-falsification \
  --matrix data/processed/candidate_matrix.csv
uv run comm-ls audit-exposure-taxonomy \
  --candidates data/processed/candidate_matrix.csv
uv run comm-ls review-candidate-taxonomy \
  --candidates data/processed/candidate_matrix.csv
```

Candidate review is meant to catch:

- missing economic exposure mapping;
- weak peer support;
- overlapping-forward-return artifacts;
- unstable regime behavior;
- apparent alpha that is mostly commodity beta leakage.

The most important review step is economic exposure. A statistically strong
ticker-feature pair is not automatically useful. The pair should have a
defensible commodity channel, and peer names with similar exposure should not
contradict the result without explanation.

### 7. Optional Context Layers

If external research pipelines provide fundamentals, positioning, inventory, or
other confirmation data, normalize them locally:

```bash
uv run comm-ls build-fundamental-snapshot
uv run comm-ls build-commodity-confirmation-events
uv run comm-ls build-agriculture-fundamental-events
```

These layers are intended for confirmation, gating, and attribution. They should
not be blindly blended into alpha scores.

### 8. Backtest Research Portfolios

```bash
uv run comm-ls build-portfolio-weights \
  --scores data/processed/daily_scores.csv \
  --mode index-hedge

uv run comm-ls run-backtest \
  --scores data/processed/daily_scores.csv \
  --mode index-hedge \
  --transaction-cost-bps 5
```

Backtests in this scaffold are research diagnostics, not production performance
claims.

## Research Discipline

The project is designed around a conservative workflow:

1. Start with an economically motivated commodity hypothesis.
2. Confirm that the feature is constructed from liquid, tradable contract data.
3. Test reaction on raw and residual equity returns.
4. Check whether peer names with the same exposure behave consistently.
5. Re-run diagnostics across time regimes and non-overlapping events.
6. Penalize or reject candidates that fail taxonomy, cost, or borrow checks.
7. Treat portfolio backtests as a final diagnostic, not as the source of the
   hypothesis.

The framework deliberately keeps manual taxonomy and feature review in the loop.
For this type of strategy, statistical significance without economic exposure is
usually a warning sign, not a green light.

## Command Reference

Show all commands:

```bash
uv run comm-ls --help
```

Show help for one command:

```bash
uv run comm-ls build-equity-processed-dataset --help
uv run comm-ls review-candidate-taxonomy --help
```

## Development

Run static checks:

```bash
uv run ruff check src/comm_ls
```

The project is organized as a normal Python package:

```text
src/comm_ls/
  commodity.py          # commodity feature construction
  equity.py             # yfinance price download/load helpers
  beta.py               # beta and residual-return panels
  universe.py           # liquidity/universe construction
  reaction.py           # feature reaction study
  forecast.py           # commodity-to-equity forecast studies
  research_quality.py   # audit and review layers
  precision.py          # precision event candidate checks
  fundamentals.py       # optional fundamental/confirmation normalization
  portfolio.py          # simple portfolio weights
  backtest.py           # research backtests
  cli.py                # command-line interface
```

## Publishing Notes

The `.gitignore` is configured to keep data, private configs, notebooks, private
docs, and local agent instructions out of the public repository. This only
applies to files that have not already been committed. If sensitive files were
committed in the past, remove them from Git history before publishing.

The package code itself may still reveal parts of the research process. If the
goal is to publish only a minimal public scaffold, review `src/comm_ls/` before
making the repository public.

## Limitations

This is a research scaffold, not an investable product.

Known limitations:

- yfinance data is not point-in-time and may have survivorship or adjustment
  issues.
- Private configs and research outputs are not included.
- Borrow availability, borrow fees, buy-ins, SSR constraints, dividends,
  slippage, market impact, and corporate actions need production-grade handling
  before live trading.
- Commodity futures data must be timestamped carefully. Signals should be gated
  by when data was available, not merely by the market date.
- Statistical significance is not enough. Candidate signals need economic
  exposure mapping and out-of-sample discipline.

## License

No license has been specified yet.
