from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class HedgeSpecification:
    market_beta_column: str
    observations_column: str
    estimation_end_column: str
    sector_beta_column: str | None = None
    sector_ticker_column: str | None = None


HEDGE_SPECIFICATIONS = {
    "residual_return_mkt_w12m": HedgeSpecification(
        market_beta_column="market_beta_mkt_w12m",
        observations_column="beta_observations_mkt_w12m",
        estimation_end_column="beta_estimation_end_mkt_w12m",
    ),
    "residual_return_mktsec_narrow_w12m": HedgeSpecification(
        market_beta_column="market_beta_mktsec_narrow_w12m",
        sector_beta_column="sector_beta_mktsec_narrow_w12m",
        sector_ticker_column="sector_ticker_narrow",
        observations_column="beta_observations_mktsec_narrow_w12m",
        estimation_end_column="beta_estimation_end_mktsec_narrow_w12m",
    ),
    "residual_return_mktsec_liquid_w12m": HedgeSpecification(
        market_beta_column="market_beta_mktsec_liquid_w12m",
        sector_beta_column="sector_beta_mktsec_liquid_w12m",
        sector_ticker_column="sector_ticker_liquid",
        observations_column="beta_observations_mktsec_liquid_w12m",
        estimation_end_column="beta_estimation_end_mktsec_liquid_w12m",
    ),
}


def read_component_targets(
    path: Path,
    *,
    target_date: pd.Timestamp | str | None = None,
) -> tuple[pd.Timestamp, pd.DataFrame]:
    """Read the notebook's two-row component target CSV into long form."""
    wide = pd.read_csv(path, header=[0, 1])
    date_column = wide.columns[0]
    dates = pd.to_datetime(wide[date_column], errors="coerce").dt.normalize()
    if dates.isna().any():
        raise ValueError(f"Invalid target date in {path}")
    selected_date = (
        pd.Timestamp(target_date).normalize() if target_date is not None else dates.max()
    )
    selected = wide.loc[dates.eq(selected_date)]
    if len(selected) != 1:
        available = ", ".join(
            pd.Timestamp(timestamp).strftime("%Y-%m-%d")
            for timestamp in sorted(dates.unique())
        )
        raise ValueError(
            f"Expected one component target row for {selected_date.date()} in {path}; "
            f"found {len(selected)}. Available target dates: {available or 'none'}. "
            "Set target_date in notebooks/backtest_agri_v43.ipynb, rerun through the "
            "portfolio aggregation cell, then rerun the live generator."
        )

    rows: list[dict[str, object]] = []
    row = selected.iloc[0]
    for column in wide.columns[1:]:
        component, instrument = (str(column[0]).strip(), str(column[1]).strip().upper())
        weight = pd.to_numeric(pd.Series([row[column]]), errors="coerce").iloc[0]
        if not component or not instrument or pd.isna(weight):
            continue
        rows.append(
            {
                "target_date": selected_date,
                "component": component,
                "instrument": instrument,
                "research_target_weight": float(weight),
            }
        )
    if not rows:
        raise ValueError(f"No component targets found in {path}")
    return selected_date, pd.DataFrame(rows)


def read_sleeve_config(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    first = frame.columns[0]
    if first != "component":
        frame = frame.rename(columns={first: "component"})
    required = {"component", "weight", "slippage_bps", "return_method"}
    missing = required.difference(frame.columns)
    if missing:
        raise KeyError(f"{path} is missing Agriculture sleeve columns: {sorted(missing)}")
    frame["component"] = frame["component"].astype(str).str.strip()
    frame["return_method"] = frame["return_method"].astype(str).str.strip()
    unknown = sorted(set(frame["return_method"]) - set(HEDGE_SPECIFICATIONS))
    if unknown:
        raise ValueError(f"No explicit hedge mapping for return methods: {unknown}")
    if frame["component"].duplicated().any():
        raise ValueError("Agriculture sleeve config contains duplicate components")
    return frame


def attach_explicit_hedge_betas(
    component_targets: pd.DataFrame,
    sleeve_config: pd.DataFrame,
    equity_panel: pd.DataFrame,
    *,
    as_of: pd.Timestamp | str,
    market_hedge: str = "SPY",
) -> pd.DataFrame:
    """Attach the lagged beta definition used by each research residual."""
    as_of = pd.Timestamp(as_of).normalize()
    legs = component_targets.merge(
        sleeve_config[["component", "return_method", "slippage_bps"]],
        on="component",
        how="left",
        validate="many_to_one",
    )
    if legs["return_method"].isna().any():
        names = sorted(legs.loc[legs["return_method"].isna(), "component"].unique())
        raise KeyError(f"Missing sleeve config for components: {names}")

    panel = equity_panel.copy()
    panel["date"] = pd.to_datetime(panel["date"], errors="coerce").dt.normalize()
    panel["ticker"] = panel["ticker"].astype(str).str.upper().str.strip()
    panel = panel[
        panel["ticker"].isin(legs["instrument"].unique()) & panel["date"].le(as_of)
    ].sort_values(["ticker", "date"])
    latest = panel.groupby("ticker", as_index=False).tail(1).set_index("ticker")

    rows: list[dict[str, object]] = []
    for leg in legs.to_dict("records"):
        ticker = str(leg["instrument"])
        if ticker not in latest.index:
            raise ValueError(f"No Agriculture beta row for {ticker} at or before {as_of.date()}")
        source = latest.loc[ticker]
        method = str(leg["return_method"])
        spec = HEDGE_SPECIFICATIONS[method]
        market_beta = pd.to_numeric(pd.Series([source[spec.market_beta_column]]), errors="coerce").iloc[0]
        sector_beta = 0.0
        sector_hedge = ""
        if spec.sector_beta_column is not None:
            sector_beta = pd.to_numeric(
                pd.Series([source[spec.sector_beta_column]]), errors="coerce"
            ).iloc[0]
            sector_hedge = str(source[spec.sector_ticker_column]).strip().upper()
        weight = float(leg["research_target_weight"])
        if weight != 0 and (
            not np.isfinite(market_beta)
            or (spec.sector_beta_column is not None and not np.isfinite(sector_beta))
            or (spec.sector_beta_column is not None and not sector_hedge)
        ):
            raise ValueError(
                f"Missing explicit hedge beta for active {leg['component']}:{ticker} "
                f"using {method}"
            )
        row = dict(leg)
        row.update(
            {
                "market_hedge": market_hedge.upper(),
                "sector_hedge": sector_hedge,
                "market_beta": float(market_beta) if np.isfinite(market_beta) else np.nan,
                "sector_beta": float(sector_beta) if np.isfinite(sector_beta) else np.nan,
                "beta_observations": pd.to_numeric(
                    pd.Series([source[spec.observations_column]]), errors="coerce"
                ).iloc[0],
                "beta_estimation_end": pd.to_datetime(
                    source[spec.estimation_end_column], errors="coerce"
                ),
                "beta_source_date": source["date"],
            }
        )
        rows.append(row)
    return pd.DataFrame(rows)


def integer_adjust_component_weights(
    legs: pd.DataFrame,
    *,
    closes: pd.Series,
    aum: float,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Round the net broker stock target while preserving component mix per ticker."""
    adjusted = legs.copy()
    stock_rows: list[dict[str, object]] = []
    for ticker, group in adjusted.groupby("instrument", sort=True):
        close = float(closes.get(ticker, np.nan))
        if not np.isfinite(close) or close <= 0:
            raise ValueError(f"Missing positive as-of close for {ticker}")
        continuous = float(group["research_target_weight"].sum())
        target_shares = float(round(continuous * aum / close))
        integer_weight = target_shares * close / aum
        scale = integer_weight / continuous if abs(continuous) > 1e-12 else 1.0
        adjusted.loc[group.index, "target_weight"] = (
            group["research_target_weight"] * scale
        )
        stock_rows.append(
            {
                "instrument": ticker,
                "research_target_weight": continuous,
                "target_weight": integer_weight,
                "target_shares": target_shares,
                "rounding_scale": scale,
            }
        )
    return adjusted, pd.DataFrame(stock_rows)


def aggregate_hedge_weights(legs: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Build component-level and broker-net explicit ETF hedge weights."""
    rows: list[dict[str, object]] = []
    for leg in legs.to_dict("records"):
        weight = float(leg["target_weight"])
        rows.append(
            {
                "component": leg["component"],
                "stock_instrument": leg["instrument"],
                "hedge_instrument": leg["market_hedge"],
                "hedge_kind": "market",
                "stock_target_weight": weight,
                "beta": leg["market_beta"],
                "hedge_target_weight": -weight * float(leg["market_beta"]),
                "return_method": leg["return_method"],
            }
        )
        if str(leg["sector_hedge"]):
            rows.append(
                {
                    "component": leg["component"],
                    "stock_instrument": leg["instrument"],
                    "hedge_instrument": leg["sector_hedge"],
                    "hedge_kind": "sector",
                    "stock_target_weight": weight,
                    "beta": leg["sector_beta"],
                    "hedge_target_weight": -weight * float(leg["sector_beta"]),
                    "return_method": leg["return_method"],
                }
            )
    component_hedges = pd.DataFrame(rows)
    broker_hedges = (
        component_hedges.groupby("hedge_instrument", as_index=False)["hedge_target_weight"]
        .sum()
        .rename(
            columns={
                "hedge_instrument": "instrument",
                "hedge_target_weight": "target_weight",
            }
        )
    )
    return component_hedges, broker_hedges
