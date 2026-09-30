from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from comm_ls.etf_research import load_soybean_crush_data, rolling_betas


ROOT = Path(".")
DEFAULT_CACHE_PATH = (
    ROOT / "data/cache/feature_return_observation_v1/ZS-soybean-common_2.parquet"
)


@dataclass(frozen=True)
class AgricultureSleeve:
    weight: float
    kind: str
    field: str
    return_method: str
    slippage_bps: float
    primary: str = ""
    secondary: str = ""
    version: str = ""


AGRICULTURE_SLEEVES = {
    "crush_vol": AgricultureSleeve(
        0.20,
        "crush_vol",
        "matched_soybean_crush_spread",
        "residual_return_mktsec_narrow_w12m",
        25.0,
    ),
    "crush_vol2": AgricultureSleeve(
        0.20,
        "crush_vol",
        "adjusted_zs",
        "residual_return_mktsec_narrow_w12m",
        25.0,
    ),
    "adm_bg": AgricultureSleeve(
        0.20,
        "spread",
        "adjusted_zs",
        "residual_return_mkt_w12m",
        15.0,
        "ADM",
        "BG",
        "1",
    ),
    "adm_bg2": AgricultureSleeve(
        0.20,
        "spread",
        "adjusted_zs",
        "residual_return_mktsec_narrow_w12m",
        15.0,
        "ADM",
        "BG",
        "1",
    ),
    "adm_tsn": AgricultureSleeve(
        0.15,
        "spread",
        "crush_02",
        "residual_return_mkt_w12m",
        15.0,
        "ADM",
        "TSN",
        "2",
    ),
    "bg_tsn": AgricultureSleeve(
        0.05,
        "spread",
        "crush_02",
        "residual_return_mkt_w12m",
        15.0,
        "BG",
        "TSN",
        "2",
    ),
}


def sleeve_config_frame() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "component": name,
                "weight": sleeve.weight,
                "slippage_bps": sleeve.slippage_bps,
                "return_method": sleeve.return_method,
            }
            for name, sleeve in AGRICULTURE_SLEEVES.items()
        ]
    )


def _load_stock(path: Path, ticker: str, columns: list[str]) -> pd.DataFrame:
    available = set(pd.read_parquet(path, filters=[("ticker", "=", ticker)]).columns)
    missing = set(columns).difference(available)
    if missing:
        raise KeyError(f"{ticker} is missing {sorted(missing)} from {path}")
    frame = pd.read_parquet(
        path,
        columns=["date", "ticker", *columns],
        filters=[("ticker", "=", ticker)],
    )
    if frame.empty:
        raise ValueError(f"{ticker} is absent from {path}")
    frame["date"] = pd.to_datetime(frame["date"], errors="raise").dt.normalize()
    return frame.sort_values("date").drop_duplicates("date", keep="last").set_index("date")


def _state_signal(crush: pd.Series, *, version: str, index: pd.Index) -> pd.Series:
    value = pd.to_numeric(crush, errors="coerce").reindex(index)
    volatility = value.rolling(10, min_periods=5).std()
    vol_change = volatility.diff(10)
    long_state = pd.Series(np.nan, index=index, dtype=float)
    short_state = pd.Series(np.nan, index=index, dtype=float)
    y = 0.05
    if version == "crush_vol":
        change = value.diff(5)
        long_state.loc[(vol_change > y) & (change > 0.10)] = 1.0
        long_state.loc[vol_change < -y / 5] = 0.0
        short_state.loc[(vol_change < -y) & (change < -0.10)] = -1.0
        short_state.loc[vol_change > y / 5] = 0.0
    elif version == "1":
        long_state.loc[(vol_change > y) & (value.diff(20) < 0.20)] = 1.0
        long_state.loc[vol_change < -y / 5] = 0.0
        short_state.loc[(vol_change < -y) & (value.diff(10) > -0.10)] = -1.0
        short_state.loc[vol_change > y / 5] = 0.0
    elif version == "2":
        scale = value.rolling(252 * 3, min_periods=252).std()
        long_state.loc[value.diff(20) > scale] = 1.0
        long_state.loc[value.diff(5) < -scale / 2] = 0.0
        short_state.loc[value.diff(20) < -scale] = -1.0
        short_state.loc[value.diff(5) > scale / 2] = 0.0
    else:
        raise ValueError(f"Unknown Agriculture signal version {version!r}")
    return long_state.ffill().fillna(0.0) + short_state.ffill().fillna(0.0)


def _target_from_signal(signal: pd.Series, *, as_of: pd.Timestamp) -> tuple[float, pd.Timestamp]:
    eligible = signal.loc[signal.index <= as_of].dropna()
    if eligible.empty:
        raise ValueError(f"No Agriculture signal at or before {as_of.date()}")
    # Notebook calc_pos_with_future(..., delay=1) makes the next session's
    # target equal to the latest available signal.
    return float(eligible.iloc[-1]), pd.Timestamp(eligible.index[-1]).normalize()


def build_component_targets(
    *,
    as_of: pd.Timestamp | str,
    target_date: pd.Timestamp | str,
    cache_path: Path = DEFAULT_CACHE_PATH,
    root: Path = ROOT,
    family: str = "_2",
) -> tuple[pd.DataFrame, dict[str, pd.Timestamp], dict[str, Path]]:
    """Reproduce the six executed notebook sleeves without running the notebook."""
    as_of = pd.Timestamp(as_of).normalize()
    target_date = pd.Timestamp(target_date).normalize()
    if target_date <= as_of:
        raise ValueError("target_date must be after as_of")
    crush = load_soybean_crush_data(root=root, family=family).loc[:as_of]
    required_fields = {sleeve.field for sleeve in AGRICULTURE_SLEEVES.values()}
    missing = required_fields.difference(crush.columns)
    if missing:
        raise KeyError(f"Soybean crush data is missing fields: {sorted(missing)}")

    stock_cache: dict[tuple[str, str], pd.DataFrame] = {}

    def stock(ticker: str, return_method: str) -> pd.DataFrame:
        key = (ticker, return_method)
        if key not in stock_cache:
            stock_cache[key] = _load_stock(cache_path, ticker, [return_method]).loc[:as_of]
        return stock_cache[key]

    rows: list[dict[str, object]] = []
    for component, sleeve in AGRICULTURE_SLEEVES.items():
        crush_series = pd.to_numeric(crush[sleeve.field], errors="coerce")
        if sleeve.kind == "crush_vol":
            for ticker, basket_weight in {"ADM": 0.60, "BG": 0.40}.items():
                frame = stock(ticker, sleeve.return_method)
                signal = _state_signal(
                    crush_series,
                    version="crush_vol",
                    index=frame.index,
                ) * basket_weight
                target, signal_date = _target_from_signal(signal, as_of=as_of)
                rows.append(
                    {
                        "target_date": target_date,
                        "component": component,
                        "instrument": ticker,
                        "research_target_weight": target * sleeve.weight,
                        "signal_date": signal_date,
                        "field": sleeve.field,
                    }
                )
            continue

        primary = stock(sleeve.primary, sleeve.return_method)
        secondary = stock(sleeve.secondary, sleeve.return_method)
        common = primary.index.union(secondary.index).sort_values()
        base = _state_signal(crush_series, version=sleeve.version, index=common)
        returns = pd.concat(
            {
                sleeve.primary: primary[sleeve.return_method],
                sleeve.secondary: secondary[sleeve.return_method],
            },
            axis=1,
        ).sort_index()
        beta = rolling_betas(
            returns[sleeve.primary],
            returns[[sleeve.secondary]],
            window=252,
            min_obs=126,
            lag=1,
        )[f"beta_{sleeve.secondary}"]
        pair_signal = base.reindex(returns.index).where(beta.notna())
        signals = {
            sleeve.primary: pair_signal,
            sleeve.secondary: -pair_signal * beta,
        }
        for ticker, signal in signals.items():
            target, signal_date = _target_from_signal(signal, as_of=as_of)
            rows.append(
                {
                    "target_date": target_date,
                    "component": component,
                    "instrument": ticker,
                    "research_target_weight": target * sleeve.weight,
                    "signal_date": signal_date,
                    "field": sleeve.field,
                }
            )

    targets = pd.DataFrame(rows)
    latest_dates = {
        "soybean_crush": pd.Timestamp(crush.index.max()).normalize(),
        "stock_cache": max(
            pd.Timestamp(frame.index.max()).normalize() for frame in stock_cache.values()
        ),
    }
    source = Path(crush.attrs.get("source", "data/processed/soybean_complex_signals_2.parquet"))
    return targets, latest_dates, {"soybean_crush": source, "stock_cache": cache_path}


def build_component_position_history(
    *,
    as_of: pd.Timestamp | str,
    cache_path: Path = DEFAULT_CACHE_PATH,
    root: Path = ROOT,
    family: str = "_2",
    start: str = "2012-01-01",
) -> dict[str, pd.DataFrame]:
    """Return weighted component positions using the executed notebook rules."""
    as_of = pd.Timestamp(as_of).normalize()
    crush = load_soybean_crush_data(root=root, family=family).loc[:as_of]
    stock_cache: dict[tuple[str, str], pd.DataFrame] = {}

    def stock(ticker: str, return_method: str) -> pd.DataFrame:
        key = (ticker, return_method)
        if key not in stock_cache:
            stock_cache[key] = _load_stock(cache_path, ticker, [return_method]).loc[:as_of]
        return stock_cache[key]

    output: dict[str, pd.DataFrame] = {}
    for component, sleeve in AGRICULTURE_SLEEVES.items():
        crush_series = pd.to_numeric(crush[sleeve.field], errors="coerce")
        if sleeve.kind == "crush_vol":
            signals = {}
            for ticker, basket_weight in {"ADM": 0.60, "BG": 0.40}.items():
                frame = stock(ticker, sleeve.return_method)
                signals[ticker] = (
                    _state_signal(
                        crush_series,
                        version="crush_vol",
                        index=frame.index,
                    )
                    * basket_weight
                )
            signal_frame = pd.DataFrame(signals).sort_index()
        else:
            primary = stock(sleeve.primary, sleeve.return_method)
            secondary = stock(sleeve.secondary, sleeve.return_method)
            returns = pd.concat(
                {
                    sleeve.primary: primary[sleeve.return_method],
                    sleeve.secondary: secondary[sleeve.return_method],
                },
                axis=1,
            ).sort_index()
            base = _state_signal(
                crush_series,
                version=sleeve.version,
                index=returns.index,
            )
            beta = rolling_betas(
                returns[sleeve.primary],
                returns[[sleeve.secondary]],
                window=252,
                min_obs=126,
                lag=1,
            )[f"beta_{sleeve.secondary}"]
            pair_signal = base.where(beta.notna())
            signal_frame = pd.DataFrame(
                {
                    sleeve.primary: pair_signal,
                    sleeve.secondary: -pair_signal * beta,
                }
            )
        # All six executed calls use the default non-fixed delay=1 path.
        output[component] = signal_frame.shift(1).fillna(0.0).loc[start:] * sleeve.weight
    return output
