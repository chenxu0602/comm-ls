from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path

import numpy as np
import pandas as pd

from comm_ls.etf_research import load_soybean_crush_data, rolling_betas


ROOT = Path(".")
AGRICULTURE_PRODUCTION_START_DATE = pd.Timestamp("2026-10-02")
AGRICULTURE_PRODUCTION_AUM = 2_000.0
ADM_TSN_DISTANCE_START_DATE = pd.Timestamp("2026-11-16")
ADM_CRUSH_VOL3_START_DATE = pd.Timestamp("2026-11-16")
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
    basket: tuple[tuple[str, float], ...] = (("ADM", .60), ("BG", .40))


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


def agriculture_config_for_target(target_date):
    """Dated operator allocation; never rewrite discovery/backtest defaults."""
    config = dict(AGRICULTURE_SLEEVES)
    if target_date is not None and pd.Timestamp(target_date) >= pd.Timestamp('2026-11-10'):
        weights = dict(crush_vol=.25, crush_vol2=.25, adm_bg=0., adm_bg2=0.,
                       adm_tsn=.15, bg_tsn=0.)
        config = {name: replace(sleeve, weight=weights.get(name, sleeve.weight))
                  for name, sleeve in config.items()}
    if target_date is not None and pd.Timestamp(target_date) >= ADM_TSN_DISTANCE_START_DATE:
        config['adm_tsn'] = replace(config['adm_tsn'], kind='adm_tsn_distance', weight=.25)
    if target_date is not None and pd.Timestamp(target_date) >= ADM_CRUSH_VOL3_START_DATE:
        config['crush_vol2'] = replace(config['crush_vol2'], basket=(("ADM", .70), ("BG", .30)))
        config['crush_vol3'] = AgricultureSleeve(
            .25, 'adm_crush_constrained', 'adjusted_zs',
            'residual_return_mktsec_narrow_w12m', 25., primary='ADM',
        )
    return config


def sleeve_config_frame(target_date=None) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "component": name,
                "weight": sleeve.weight,
                "slippage_bps": sleeve.slippage_bps,
                "return_method": sleeve.return_method,
            }
            for name, sleeve in agriculture_config_for_target(target_date).items()
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
    if as_of not in signal.index or not np.isfinite(signal.loc[as_of]):
        raise ValueError(f"Missing Agriculture target signal/beta on {as_of.date()}; refusing a stale target")
    eligible = signal.loc[signal.index <= as_of].dropna()
    if eligible.empty:
        raise ValueError(f"No Agriculture signal at or before {as_of.date()}")
    # Notebook calc_pos_with_future(..., delay=1) makes the next session's
    # target equal to the latest available signal.
    return float(eligible.iloc[-1]), pd.Timestamp(eligible.index[-1]).normalize()


def _adm_tsn_distance_signal(crush, adm_prices, tsn_prices):
    """Notebook calc_adm_tsn: ADM calendar, price-distance entry gate, equal legs."""
    value = pd.to_numeric(crush, errors="coerce").reindex(adm_prices.index)
    distance = adm_prices - tsn_prices.reindex(adm_prices.index)
    distance_sd = distance.rolling(252 * 5, min_periods=252).std()
    scale = value.rolling(252 * 3, min_periods=252).std()
    change_long = value.diff(20)
    change_tiny = value.diff(5)
    long_state = pd.Series(np.nan, index=value.index, dtype=float)
    short_state = long_state.copy()
    long_state.loc[(change_long > scale) & (distance < distance_sd)] = 1.0
    long_state.loc[change_tiny < -scale / 2] = 0.0
    short_state.loc[(change_long < -scale) & (distance > -distance_sd)] = -1.0
    short_state.loc[change_tiny > scale / 2] = 0.0
    return long_state.ffill().fillna(0.0) + short_state.ffill().fillna(0.0)


def _adm_crush_constrained_inputs(crush, prices):
    """Keep notebook order: compute crush volatility BEFORE stock alignment."""
    crush = pd.to_numeric(crush, errors="coerce")
    price = pd.to_numeric(prices, errors="coerce")
    value = crush.reindex(price.index)
    volatility = crush.rolling(10, min_periods=5).std().reindex(price.index)
    return pd.DataFrame({
        "vol_change": volatility.diff(10),
        "crush_change": value.diff(5),
        "price": price,
        "ma50": price.rolling(50, min_periods=25).mean(),
    }, index=price.index)


def _adm_crush_constrained_signal(crush, prices):
    """Notebook calc_crush_vol(constraint=True), unit ADM leg, no smoothing."""
    values = _adm_crush_constrained_inputs(crush, prices)
    vol_change, change = values.vol_change, values.crush_change
    long_state = pd.Series(np.nan, index=prices.index, dtype=float)
    short_state = long_state.copy()
    long_state.loc[(vol_change > .05) & (change > .10)
                   & (values.price < values.ma50)] = 1.
    long_state.loc[vol_change < -.05/2] = 0.
    short_state.loc[(vol_change < -.05) & (change < -.10)
                    & (values.price > values.ma50)] = -1.
    short_state.loc[(vol_change > .05/2) | (change > .10/2)] = 0.
    return long_state.ffill().fillna(0.) + short_state.ffill().fillna(0.)


def _validate_live_crush_inputs(value, index, *, component, field, version, as_of):
    """Require the actual field and its decision lookbacks, even for a flat state."""
    index = index[index <= as_of]
    if len(index) < 21 or index[-1] != as_of:
        raise ValueError(f"{component}: Agriculture stock calendar must cover {as_of.date()} and 21 sessions")
    aligned = pd.to_numeric(value, errors="coerce").reindex(index)
    recent = aligned.iloc[-21:]
    bad = recent.index[~np.isfinite(recent)]
    if len(bad):
        raise ValueError(
            f"Missing Agriculture signal inputs for {component}/{field}: "
            f"{[str(day.date()) for day in bad[:5]]}. "
            "Review ZS/ZM/ZL contract/live settles and rebuild inputs; do not fill missing crush with zero."
        )
    if version == "2" and not np.isfinite(aligned.rolling(252*3, min_periods=252).std().iloc[-1]):
        raise ValueError(f"{component}/{field}: insufficient history for the 252-observation volatility scale")


def build_component_targets(
    *,
    as_of: pd.Timestamp | str,
    target_date: pd.Timestamp | str,
    cache_path: Path = DEFAULT_CACHE_PATH,
    root: Path = ROOT,
    family: str = "_2",
) -> tuple[pd.DataFrame, dict[str, pd.Timestamp], dict[str, Path]]:
    """Reproduce effective-dated notebook sleeves without executing the notebook."""
    as_of = pd.Timestamp(as_of).normalize()
    target_date = pd.Timestamp(target_date).normalize()
    if target_date <= as_of:
        raise ValueError("target_date must be after as_of")
    config = agriculture_config_for_target(target_date)
    crush = load_soybean_crush_data(root=root, family=family).loc[:as_of]
    required_fields = {sleeve.field for sleeve in config.values() if sleeve.weight != 0}
    missing = required_fields.difference(crush.columns)
    if missing:
        raise KeyError(f"Soybean crush data is missing fields: {sorted(missing)}")

    stock_cache: dict[tuple[str, str], pd.DataFrame] = {}

    def stock(ticker: str, return_method: str) -> pd.DataFrame:
        key = (ticker, return_method)
        if key not in stock_cache:
            stock_cache[key] = _load_stock(cache_path, ticker, [return_method]).loc[:as_of]
            frame = stock_cache[key]
            if as_of not in frame.index or not np.isfinite(frame.loc[as_of, return_method]):
                raise ValueError(f"Missing Agriculture {ticker}/{return_method} on {as_of.date()}")
        return stock_cache[key]

    rows: list[dict[str, object]] = []
    for component, sleeve in config.items():
        if sleeve.weight == 0:
            # Preserve zero component rows and the clearing universe, without
            # requiring a suspended pair's signal or rolling trading beta.
            tickers = ('ADM','BG') if sleeve.kind == 'crush_vol' else (sleeve.primary,sleeve.secondary)
            for ticker in tickers:
                rows.append(dict(target_date=target_date, component=component,
                                 instrument=ticker, research_target_weight=0.,
                                 signal_date=as_of, field=sleeve.field))
            continue
        crush_series = pd.to_numeric(crush[sleeve.field], errors="coerce")
        if sleeve.kind == "adm_crush_constrained":
            frame = stock(sleeve.primary, sleeve.return_method)
            _validate_live_crush_inputs(
                crush_series, frame.index, component=component,
                field=sleeve.field, version="crush_vol", as_of=as_of,
            )
            prices = _load_stock(cache_path, sleeve.primary, ["adj_close"]).loc[:as_of, "adj_close"].reindex(frame.index)
            inputs = _adm_crush_constrained_inputs(crush_series, prices)
            if (not np.isfinite(inputs.iloc[-1].astype(float)).all()
                    or inputs.price.iloc[-1] <= 0):
                raise ValueError(f"{component}: missing current ADM adjusted price/MA50/crush inputs on {as_of.date()}")
            signal = _adm_crush_constrained_signal(crush_series, prices)
            target, signal_date = _target_from_signal(signal, as_of=as_of)
            rows.append(dict(target_date=target_date, component=component,
                             instrument=sleeve.primary,
                             research_target_weight=target*sleeve.weight,
                             signal_date=signal_date, field=sleeve.field))
            continue
        if sleeve.kind == "crush_vol":
            for ticker, basket_weight in sleeve.basket:
                frame = stock(ticker, sleeve.return_method)
                _validate_live_crush_inputs(
                    crush_series, frame.index, component=component,
                    field=sleeve.field, version="crush_vol", as_of=as_of,
                )
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

        if sleeve.kind == "adm_tsn_distance":
            primary = stock(sleeve.primary, sleeve.return_method)
            secondary = stock(sleeve.secondary, sleeve.return_method)
            _validate_live_crush_inputs(
                crush_series, primary.index, component=component,
                field=sleeve.field, version=sleeve.version, as_of=as_of,
            )
            prices = {
                ticker: _load_stock(cache_path, ticker, ["adj_close"]).loc[:as_of, "adj_close"]
                for ticker in (sleeve.primary, sleeve.secondary)
            }
            aligned_prices = pd.concat(prices, axis=1).reindex(primary.index)
            if not np.isfinite(aligned_prices.iloc[-1].astype(float)).all():
                raise ValueError(f"Missing current ADM/TSN adjusted prices on {as_of.date()}")
            distance = aligned_prices[sleeve.primary] - aligned_prices[sleeve.secondary]
            if not np.isfinite(distance.rolling(252 * 5, min_periods=252).std().iloc[-1]):
                raise ValueError("Insufficient ADM/TSN price-distance history: requires 252 joint observations")
            base = _adm_tsn_distance_signal(
                crush_series, prices[sleeve.primary].reindex(primary.index), prices[sleeve.secondary]
            )
            # Exactly equal and opposite dollar weights; no ADM/TSN rolling pair beta.
            for ticker, side in ((sleeve.primary, 1.0), (sleeve.secondary, -1.0)):
                target, signal_date = _target_from_signal(base * side, as_of=as_of)
                rows.append(dict(target_date=target_date, component=component,
                                 instrument=ticker, research_target_weight=target * sleeve.weight,
                                 signal_date=signal_date, field=sleeve.field))
            continue

        primary = stock(sleeve.primary, sleeve.return_method)
        secondary = stock(sleeve.secondary, sleeve.return_method)
        common = primary.index.union(secondary.index).sort_values()
        _validate_live_crush_inputs(
            crush_series, common, component=component,
            field=sleeve.field, version=sleeve.version, as_of=as_of,
        )
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
    latest_dates.update({
        f"soybean_crush_{field}": pd.Timestamp(crush[field].last_valid_index()).normalize()
        for field in sorted(required_fields)
    })
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
