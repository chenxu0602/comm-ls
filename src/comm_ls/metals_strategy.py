from __future__ import annotations

from bisect import bisect_left
from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping

import numpy as np
import pandas as pd

from comm_ls.cl_v32_strategy import fixed_hold_position


METALS_MAX_SINGLE_NAME_WEIGHT = 0.12
METALS_CACHE_PATH = Path("data/cache/feature_return/METALS-multi_return_2.parquet")
GC_CACHE_PATH = Path("data/cache/feature_return/GC-multi_return_2.parquet")
SCO_CACHE_PATH = Path("data/cache/feature_return/SCO-multi_return_2.parquet")
SHADOW_CARRY_DIR = Path("data/comm/carry_data_2")
COMMODITY_DIR = Path("data/comm")
PERSISTENT_AUXILIARY_INPUTS = frozenset({"sco_curve_vol"})

HG_GC_GAP_FEATURE = "feature_value__hg_gc_matched_ratio_ma_gap_3d_50d_raw"
GC_CARRY_FEATURE = "feature_z__liquid_deferred_annualized_carry_chg_21d"
GC_HG_ACCEL_FEATURE = "feature_z__gc_hg_relative_log_accel_11d_vs_63d"
SCO_RETURN_FEATURE = "feature_z__ret_63d_v2"
SCO_DRAWDOWN_FEATURE = "feature_z__drawdown_63d"
SCO_VOL_FEATURE = "feature_z__realized_vol_63d"
SCO_CURVE_VOL_FEATURE = "M0_atr_14"
SCO_PULSE_VOL_FEATURE = "M0_ret_std_20"


@dataclass(frozen=True)
class MetalsSleeveConfig:
    weight: float
    tickers: tuple[str, ...]
    internal_weights: Mapping[str, float]
    signal_rule: str
    signal_ticker: str
    feature: str
    feature_symbol: str
    sector_hedge: str = "XME"
    hold_days: int | None = None
    params: Mapping[str, float | int | str] = field(default_factory=dict)

    @property
    def position_mode(self) -> str:
        return "fixed_hold" if self.hold_days is not None else "sign"


# Source of truth for the Metals production candidate. The rules and
# allocations mirror the executed portfolio cells in
# notebooks/backtest_mt.ipynb after the 2026-08-23 review.
METALS_SLEEVE_CONFIG: dict[str, MetalsSleeveConfig] = {
    "hg_gc_gap_gc_carry_iron": MetalsSleeveConfig(
        weight=0.15,
        tickers=("BHP", "RIO", "VALE", "FSUGY"),
        internal_weights={"BHP": 0.40, "RIO": 0.30, "VALE": 0.20, "FSUGY": 0.10},
        signal_rule="dual_feature_hysteresis",
        signal_ticker="BHP",
        feature="hg_gc_matched_ratio_ma_gap_3d_50d_raw",
        feature_symbol="METALS+GC",
        params={
            "long_entry_hg": -0.01,
            "long_entry_gc": 0.10,
            "long_exit_hg": 0.00,
            "long_exit_gc": 0.30,
            "short_entry_hg": 0.02,
            "short_entry_gc": 0.10,
            "short_exit_hg": 0.00,
            "short_exit_gc": 0.20,
        },
    ),
    "sco_vol_gc_hg_accel_miners": MetalsSleeveConfig(
        weight=0.25,
        tickers=("BHP", "RIO", "VALE", "SCCO"),
        internal_weights={"BHP": 0.30, "RIO": 0.40, "VALE": 0.10, "SCCO": 0.20},
        signal_rule="sco_vol_gc_hg_combo",
        signal_ticker="BHP",
        feature="gc_hg_relative_log_accel_11d_vs_63d",
        feature_symbol="METALS+SCO",
        hold_days=2,
        params={
            "long_entry_accel": 1.0,
            "long_exit_accel": -0.8,
            "short_entry_accel": -1.0,
            "short_exit_accel": 0.3,
            "vol_long_exit_quantile": 0.80,
            "vol_short_entry_quantile": 0.80,
            "vol_short_exit_quantile": 0.20,
            "vol_quantile_window": 504,
            "vol_quantile_min_periods": 252,
            "vol_diff_days": 20,
        },
    ),
    "sco_specialty_alloys": MetalsSleeveConfig(
        weight=0.10,
        tickers=("ATI", "CRS", "HWM"),
        internal_weights={"ATI": 0.40, "CRS": 0.40, "HWM": 0.20},
        signal_rule="sco_specialty_alloys_hysteresis",
        signal_ticker="ATI",
        feature="ret_63d_v2+drawdown_63d+realized_vol_63d",
        feature_symbol="SCO",
        params={
            "zero_threshold": 0.0,
            "short_vol_floor": -1.0,
            "long_vol_ceiling": 1.0,
            "long_vol_exit": 0.0,
        },
    ),
    "sco_vol_miners": MetalsSleeveConfig(
        weight=0.10,
        tickers=("BHP", "RIO", "VALE", "SCCO"),
        internal_weights={"BHP": 0.30, "RIO": 0.30, "VALE": 0.20, "SCCO": 0.20},
        signal_rule="sco_vol_regime_pulse",
        signal_ticker="BHP",
        feature="M0_ret_std_20",
        feature_symbol="SCO",
        # The executed notebook portfolio uses a two-session fixed hold.
        hold_days=2,
        params={
            "threshold": 0.70,
            "side_mult": 1.0,
            "vol_quantile_window": 504,
            "vol_quantile_min_periods": 252,
            "vol_diff_days": 20,
        },
    ),
    "copper_miner": MetalsSleeveConfig(
        weight=0.15,
        tickers=("SCCO",),
        internal_weights={"SCCO": 1.0},
        signal_rule="copper_energy_terms_of_trade",
        signal_ticker="SCCO",
        feature="hg_cl_5d_minus_200d_confirmed_by_ho_20d",
        feature_symbol="HG+CL+HO",
        params={"threshold_multiple": 0.20, "signal_smoothing": 2},
    ),
    "miners": MetalsSleeveConfig(
        weight=0.25,
        tickers=("VALE", "BHP", "RIO", "SCCO", "FSUGY"),
        internal_weights={
            "VALE": 0.10,
            "BHP": 0.30,
            "RIO": 0.20,
            "SCCO": 0.20,
            "FSUGY": 0.20,
        },
        signal_rule="persistent_binary",
        signal_ticker="BHP",
        feature="hg_gc_matched_ratio_ma_gap_3d_50d_raw",
        feature_symbol="METALS",
        params={"threshold": 0.02, "side_mult": -1.0},
    ),
}


@dataclass(frozen=True)
class MetalsSignalBundle:
    signals: Mapping[str, pd.Series]
    diagnostics: Mapping[str, pd.DataFrame]
    latest_dates: Mapping[str, pd.Timestamp]
    source_paths: Mapping[str, Path]


def normalize_index(index: pd.Index) -> pd.DatetimeIndex:
    out = pd.to_datetime(index, errors="coerce")
    if getattr(out, "tz", None) is not None:
        out = out.tz_convert(None)
    return out.normalize()


def validate_config(config: Mapping[str, MetalsSleeveConfig] = METALS_SLEEVE_CONFIG) -> None:
    if not np.isclose(sum(cfg.weight for cfg in config.values()), 1.0):
        raise ValueError("Metals sleeve weights must sum to 1")
    for sleeve, cfg in config.items():
        if set(cfg.tickers) != set(cfg.internal_weights):
            raise ValueError(f"{sleeve} internal weights do not match tickers")
        if not np.isclose(sum(cfg.internal_weights.values()), 1.0):
            raise ValueError(f"{sleeve} internal weights must sum to 1")
        if cfg.signal_ticker not in cfg.tickers:
            raise ValueError(f"{sleeve} signal ticker is not in the sleeve")
        if cfg.sector_hedge != "XME":
            raise ValueError(f"{sleeve} must use XME as its sector hedge")


def require_shadow_cache(path: Path) -> None:
    if "_2" not in path.stem:
        raise ValueError(
            f"Metals live targets must remain on the isolated _2 cache pipeline: {path}"
        )
    if not path.exists():
        raise FileNotFoundError(path)


def _load_cache(path: Path, columns: list[str], tickers: set[str]) -> pd.DataFrame:
    require_shadow_cache(path)
    required = ["date", "ticker", *columns]
    frame = pd.read_parquet(path, columns=required)
    frame = frame[frame["ticker"].astype(str).isin(tickers)].copy()
    if frame.empty:
        raise ValueError(f"No configured Metals tickers found in {path}")
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    frame = frame.dropna(subset=["date"]).sort_values(["ticker", "date"])
    frame["date"] = normalize_index(pd.Index(frame["date"]))
    duplicate = frame.duplicated(["ticker", "date"], keep=False)
    if duplicate.any():
        raise ValueError(f"Duplicate ticker/date rows in {path}")
    return frame.set_index(["ticker", "date"]).sort_index()


def _feature(panel: pd.DataFrame, ticker: str, column: str) -> pd.Series:
    if column not in panel.columns:
        raise KeyError(column)
    try:
        value = panel.xs(ticker, level="ticker")[column]
    except KeyError as exc:
        raise KeyError(f"{ticker} is missing from the required feature cache") from exc
    return pd.to_numeric(value, errors="coerce").sort_index()


def _latest_valid_date(series: pd.Series, label: str) -> pd.Timestamp:
    valid = pd.to_numeric(series, errors="coerce").dropna()
    if valid.empty:
        raise ValueError(f"No valid observations for required Metals input {label}")
    return pd.Timestamp(valid.index.max()).normalize()


def dual_feature_hysteresis(
    hg_gap: pd.Series,
    gc_carry: pd.Series,
    params: Mapping[str, float | int | str],
) -> tuple[pd.Series, pd.DataFrame]:
    data = pd.concat({"hg_gap": hg_gap, "gc_carry": gc_carry}, axis=1).sort_index()
    long_leg = pd.Series(np.nan, index=data.index, dtype=float)
    short_leg = pd.Series(np.nan, index=data.index, dtype=float)
    long_leg.loc[
        (data["hg_gap"] < float(params["long_entry_hg"]))
        & (data["gc_carry"] < float(params["long_entry_gc"]))
    ] = 1.0
    long_leg.loc[
        (data["hg_gap"] > float(params["long_exit_hg"]))
        | (data["gc_carry"] > float(params["long_exit_gc"]))
    ] = 0.0
    short_leg.loc[
        (data["hg_gap"] > float(params["short_entry_hg"]))
        & (data["gc_carry"] > float(params["short_entry_gc"]))
    ] = -1.0
    # Preserve notebook assignment priority: the exit wins on overlap.
    short_leg.loc[
        (data["hg_gap"] < float(params["short_exit_hg"]))
        | (data["gc_carry"] < float(params["short_exit_gc"]))
    ] = 0.0
    data["long_leg"] = long_leg.ffill().fillna(0.0)
    data["short_leg"] = short_leg.ffill().fillna(0.0)
    data["signal"] = data["long_leg"] + data["short_leg"]
    return data["signal"], data


def sco_vol_accel_hysteresis(
    accel: pd.Series,
    sco_vol: pd.Series,
    params: Mapping[str, float | int | str],
) -> tuple[pd.Series, pd.DataFrame]:
    vol = pd.to_numeric(sco_vol, errors="coerce").ffill().sort_index()
    window = int(params["vol_quantile_window"])
    min_periods = int(params["vol_quantile_min_periods"])
    state = pd.DataFrame(index=vol.index)
    state["sco_vol"] = vol
    for name, key in {
        "q_long_exit": "vol_long_exit_quantile",
        "q_short_entry": "vol_short_entry_quantile",
        "q_short_exit": "vol_short_exit_quantile",
    }.items():
        state[name] = vol.rolling(window, min_periods=min_periods).quantile(
            float(params[key])
        ).shift(1)
    state["vol_diff"] = vol.diff(int(params["vol_diff_days"]))
    state = state.reindex(accel.index).ffill()
    state["accel"] = pd.to_numeric(accel, errors="coerce")

    long_leg = pd.Series(np.nan, index=state.index, dtype=float)
    short_leg = pd.Series(np.nan, index=state.index, dtype=float)
    long_entry = (
        ((state["sco_vol"] < state["q_long_exit"]) & (state["vol_diff"] > 0))
        | (state["accel"] > float(params["long_entry_accel"]))
    )
    long_exit = (
        (state["sco_vol"] > state["q_long_exit"])
        | (state["accel"] < float(params["long_exit_accel"]))
    )
    short_entry = (
        (state["sco_vol"] > state["q_short_entry"])
        & (state["accel"] < float(params["short_entry_accel"]))
    )
    short_exit = (
        (state["sco_vol"] < state["q_short_exit"])
        | (state["accel"] > float(params["short_exit_accel"]))
    )
    long_leg.loc[long_entry] = 1.0
    long_leg.loc[long_exit] = 0.0
    short_leg.loc[short_entry] = -1.0
    short_leg.loc[short_exit] = 0.0
    invalid = state[
        ["accel", "sco_vol", "q_long_exit", "q_short_entry", "q_short_exit", "vol_diff"]
    ].isna().any(axis=1)
    long_leg.loc[invalid] = 0.0
    short_leg.loc[invalid] = 0.0
    state["long_leg"] = long_leg.ffill().fillna(0.0)
    state["short_leg"] = short_leg.ffill().fillna(0.0)
    state["signal"] = state["long_leg"] + state["short_leg"]
    return state["signal"], state


def sco_vol_regime_pulse(
    sco_vol: pd.Series,
    params: Mapping[str, float | int | str],
) -> tuple[pd.Series, pd.DataFrame]:
    """Build the notebook's low-level, rising-volatility SCO entry pulse."""
    vol = pd.to_numeric(sco_vol, errors="coerce").ffill().sort_index()
    state = pd.DataFrame(index=vol.index)
    state["sco_vol"] = vol
    state["vol_quantile"] = vol.rolling(
        int(params["vol_quantile_window"]),
        min_periods=int(params["vol_quantile_min_periods"]),
    ).quantile(float(params["threshold"])).shift(1)
    state["vol_diff"] = vol.diff(int(params["vol_diff_days"]))
    state["signal"] = (
        (state["sco_vol"] < state["vol_quantile"])
        & (state["vol_diff"] > 0.0)
    ).astype(float) * float(params["side_mult"])
    return state["signal"], state


def specialty_alloys_hysteresis(
    ret_63d: pd.Series,
    drawdown_63d: pd.Series,
    realized_vol_63d: pd.Series,
    params: Mapping[str, float | int | str],
) -> tuple[pd.Series, pd.DataFrame]:
    state = pd.concat(
        {
            "ret_63d": ret_63d,
            "drawdown_63d": drawdown_63d,
            "realized_vol_63d": realized_vol_63d,
        },
        axis=1,
    ).sort_index()
    zero = float(params["zero_threshold"])
    long_leg = pd.Series(np.nan, index=state.index, dtype=float)
    short_leg = pd.Series(np.nan, index=state.index, dtype=float)
    short_leg.loc[
        (state["ret_63d"] > zero)
        & (state["drawdown_63d"] > zero)
        & (state["realized_vol_63d"] > float(params["short_vol_floor"]))
    ] = -1.0
    short_leg.loc[
        (state["ret_63d"] < zero) | (state["drawdown_63d"] < zero)
    ] = 0.0
    long_leg.loc[
        (state["ret_63d"] < zero)
        & (state["drawdown_63d"] < zero)
        & (state["realized_vol_63d"] < float(params["long_vol_ceiling"]))
    ] = 1.0
    long_leg.loc[
        (state["ret_63d"] > zero)
        | (state["realized_vol_63d"] > float(params["long_vol_exit"]))
    ] = 0.0
    state["long_leg"] = long_leg.ffill().fillna(0.0)
    state["short_leg"] = short_leg.ffill().fillna(0.0)
    state["signal"] = state["long_leg"] + state["short_leg"]
    return state["signal"], state


def persistent_binary(
    feature: pd.Series,
    *,
    threshold: float,
    side_mult: float,
) -> tuple[pd.Series, pd.DataFrame]:
    state = pd.DataFrame({"feature": pd.to_numeric(feature, errors="coerce")})
    signal = pd.Series(np.nan, index=state.index, dtype=float)
    signal.loc[state["feature"] > threshold] = 1.0 * side_mult
    signal.loc[state["feature"] < -threshold] = -1.0 * side_mult
    state["signal"] = signal.ffill().fillna(0.0)
    return state["signal"], state


def _read_contract(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path)
    missing = {"date", "px_settle", "volume"} - set(frame.columns)
    if missing:
        raise KeyError(f"{path} is missing columns: {sorted(missing)}")
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    frame["px_settle"] = pd.to_numeric(frame["px_settle"], errors="coerce")
    frame["volume"] = pd.to_numeric(frame["volume"], errors="coerce")
    return frame.dropna(subset=["date"]).sort_values("date").drop_duplicates(
        "date", keep="last"
    ).set_index("date")


def _extend_hg_cl_ratio_from_carry(
    historical: pd.DataFrame,
    carry_dir: Path,
    *,
    allow_canonical_carry: bool = False,
) -> pd.DataFrame:
    """Extend the notebook's contract-matched ratio with merged live settles."""
    allowed_names = {"carry_data_2"}
    if allow_canonical_carry:
        allowed_names.add("carry_data")
    if carry_dir.name not in allowed_names:
        raise ValueError(f"Metals live targets require carry_data_2: {carry_dir}")
    hg = pd.read_csv(carry_dir / "HG.csv", low_memory=False)
    cl = pd.read_csv(carry_dir / "CL.csv", low_memory=False)
    hg_columns = ["date", "M0_con", "M0_settle"]
    cl_months = "HMUZ"
    calendar_pairs = [(f"{month}_con", f"{month}_settle") for month in cl_months]
    chain_pairs = [(f"M{number}_con", f"M{number}_settle") for number in range(3)]
    cl_pairs = (
        calendar_pairs
        if all(column in cl.columns for pair in calendar_pairs for column in pair)
        else chain_pairs
    )
    cl_columns = ["date", *[column for pair in cl_pairs for column in pair]]
    hg = hg[hg_columns].copy()
    cl = cl[cl_columns].copy()
    for frame in (hg, cl):
        frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    hg["M0_settle"] = pd.to_numeric(hg["M0_settle"], errors="coerce")
    for _, settle_column in cl_pairs:
        cl[settle_column] = pd.to_numeric(cl[settle_column], errors="coerce")
    if cl_pairs == chain_pairs:
        rename = {
            column: f"CL_{column}"
            for pair in cl_pairs
            for column in pair
        }
        cl = cl.rename(columns=rename)
        cl_pairs = [(rename[contract], rename[settle]) for contract, settle in cl_pairs]
    live = hg.merge(cl, on="date", how="inner").sort_values("date")
    live = live[live["date"] > historical.index.max()]

    rows: list[dict[str, object]] = []
    for row in live.itertuples(index=False):
        hg_contract = str(row.M0_con)
        if not hg_contract or hg_contract == "nan" or not np.isfinite(row.M0_settle):
            continue
        candidates: list[tuple[str, float]] = []
        for contract_column, settle_column in cl_pairs:
            contract = str(getattr(row, contract_column))
            settle = getattr(row, settle_column)
            if contract and contract != "nan" and np.isfinite(settle):
                candidates.append((contract, float(settle)))
        if not candidates:
            continue
        candidates.sort(key=lambda item: item[0])
        next_contracts = [item for item in candidates if item[0] > hg_contract]
        cl_contract, cl_settle = next_contracts[0] if next_contracts else candidates[-1]
        rows.append(
            {
                "date": row.date,
                "hg": float(row.M0_settle),
                "cl": cl_settle,
                "hg_contract": hg_contract,
                "cl_contract": cl_contract,
            }
        )
    if not rows:
        return historical
    extension = pd.DataFrame(rows).set_index("date")
    extension["ratio"] = extension["hg"] / extension["cl"]
    out = pd.concat([historical, extension], axis=0, sort=False).sort_index()
    return out[~out.index.duplicated(keep="last")]


def build_hg_cl_ratio(
    commodity_dir: Path = COMMODITY_DIR,
    carry_dir: Path | None = None,
    *,
    allow_canonical_carry: bool = False,
) -> pd.DataFrame:
    hg_dir = commodity_dir / "HG"
    cl_dir = commodity_dir / "CL"
    hg_data: dict[str, pd.DataFrame] = {}
    cl_data: dict[str, pd.DataFrame] = {}
    current_year = pd.Timestamp.today().year
    years = sorted(
        {
            int(path.stem[:4])
            for directory in (hg_dir, cl_dir)
            for path in directory.glob("?????.csv")
            if path.stem[:4].isdigit()
            and 2010 <= int(path.stem[:4]) <= current_year
        }
    )
    for year in years:
        for month in "HKNUZ":
            path = hg_dir / f"{year}{month}.csv"
            if path.exists():
                hg_data[f"{year}{month}"] = _read_contract(path)
        for month in "HMUZ":
            path = cl_dir / f"{year}{month}.csv"
            if path.exists():
                cl_data[f"{year}{month}"] = _read_contract(path)
    if len(hg_data) < 2 or not cl_data:
        raise ValueError("Insufficient HG/CL contract history")

    cl_contracts = sorted(cl_data)
    volume = pd.DataFrame({symbol: frame["volume"] for symbol, frame in hg_data.items()})
    volume = volume[sorted(volume)].rolling(3, min_periods=1).mean()
    start = volume.index[0]
    hg_parts: list[pd.Series] = []
    cl_parts: list[pd.Series] = []
    columns = list(volume.columns)
    last_next = columns[-1]
    for current, next_contract in zip(columns[:-1], columns[1:], strict=True):
        valid = volume.loc[volume[current] >= volume[next_contract]]
        if valid.empty:
            continue
        end = valid.index[-1]
        cl_number = bisect_left(cl_contracts, current)
        cl_key = cl_contracts[min(cl_number + 1, len(cl_contracts) - 1)]
        cl_parts.append(cl_data[cl_key].loc[(cl_data[cl_key].index > start) & (cl_data[cl_key].index <= end), "px_settle"])
        hg_parts.append(hg_data[current].loc[(hg_data[current].index > start) & (hg_data[current].index <= end), "px_settle"])
        start = end
        last_next = next_contract
    if last_next in hg_data:
        cl_number = bisect_left(cl_contracts, last_next)
        cl_key = cl_contracts[min(cl_number, len(cl_contracts) - 1)]
        cl_parts.append(cl_data[cl_key].loc[cl_data[cl_key].index > start, "px_settle"])
        hg_parts.append(hg_data[last_next].loc[hg_data[last_next].index > start, "px_settle"])
    result = pd.DataFrame({"hg": pd.concat(hg_parts), "cl": pd.concat(cl_parts)}).sort_index()
    result = result[~result.index.duplicated(keep="last")]
    result["ratio"] = result["hg"].ffill() / result["cl"].ffill()
    if carry_dir is not None:
        result = _extend_hg_cl_ratio_from_carry(
            result,
            carry_dir,
            allow_canonical_carry=allow_canonical_carry,
        )
    return result


def copper_energy_terms_of_trade_signal(
    signal_calendar: pd.Index,
    *,
    threshold_multiple: float,
    smoothing: int,
    commodity_dir: Path = COMMODITY_DIR,
    carry_dir: Path = SHADOW_CARRY_DIR,
) -> tuple[pd.Series, pd.DataFrame]:
    ratio = build_hg_cl_ratio(commodity_dir, carry_dir=carry_dir)
    ho_path = carry_dir / "HO.csv"
    if carry_dir.name != "carry_data_2":
        raise ValueError(f"Metals live targets require carry_data_2: {carry_dir}")
    ho = pd.read_csv(ho_path, usecols=["date", "m0_ret"])
    ho["date"] = pd.to_datetime(ho["date"], errors="coerce")
    ho["m0_ret"] = pd.to_numeric(ho["m0_ret"], errors="coerce")
    ho = ho.dropna(subset=["date"]).sort_values("date").drop_duplicates("date", keep="last").set_index("date")["m0_ret"].fillna(0.0)

    dates = normalize_index(pd.Index(signal_calendar)).sort_values().unique()
    state = pd.DataFrame(index=dates)
    state["hg_cl_ratio"] = (ratio["ratio"] * 0.1).reindex(dates)
    state["ho_ret"] = ho.reindex(dates)
    state["hg_mv_5"] = state["hg_cl_ratio"].rolling(5, min_periods=2).mean()
    state["hg_mv_200"] = state["hg_cl_ratio"].rolling(200, min_periods=100).mean()
    state["hg_mv_diff"] = state["hg_mv_5"] - state["hg_mv_200"]
    state["hg_threshold"] = state["hg_mv_diff"].rolling(63, min_periods=42).std() * threshold_multiple
    state["ho_momentum_20d"] = state["ho_ret"].rolling(20).sum()
    state["ho_threshold"] = state["ho_ret"].rolling(60, min_periods=30).std()
    long_leg = pd.Series(np.nan, index=dates, dtype=float)
    short_leg = pd.Series(np.nan, index=dates, dtype=float)
    short_leg.loc[
        (state["hg_mv_diff"] < -state["hg_threshold"])
        & (state["ho_momentum_20d"] > state["ho_threshold"])
    ] = -0.5
    short_leg.loc[
        (state["hg_mv_diff"] > state["hg_threshold"])
        | (state["ho_momentum_20d"] < -state["ho_threshold"])
    ] = 0.0
    long_leg.loc[
        (state["hg_mv_diff"] > state["hg_threshold"])
        & (state["ho_momentum_20d"] < -state["ho_threshold"])
    ] = 1.0
    long_leg.loc[
        (state["hg_mv_diff"] < -state["hg_threshold"])
        | (state["ho_momentum_20d"] > -state["ho_threshold"])
    ] = 0.0
    state["long_leg"] = long_leg.ffill().fillna(0.0)
    state["short_leg"] = short_leg.ffill().fillna(0.0)
    state["signal"] = state["long_leg"] + state["short_leg"]
    if smoothing > 1:
        state["signal"] = state["signal"].rolling(smoothing, min_periods=1).mean()
    return state["signal"], state


def load_signal_bundle(
    *,
    metals_cache: Path = METALS_CACHE_PATH,
    gc_cache: Path = GC_CACHE_PATH,
    sco_cache: Path = SCO_CACHE_PATH,
    carry_dir: Path = SHADOW_CARRY_DIR,
    commodity_dir: Path = COMMODITY_DIR,
    config: Mapping[str, MetalsSleeveConfig] = METALS_SLEEVE_CONFIG,
) -> MetalsSignalBundle:
    validate_config(config)
    metals = _load_cache(
        metals_cache,
        [HG_GC_GAP_FEATURE, GC_HG_ACCEL_FEATURE],
        {"BHP", "SCCO"},
    )
    gc = _load_cache(gc_cache, [GC_CARRY_FEATURE], {"BHP"})
    sco = _load_cache(
        sco_cache,
        [SCO_RETURN_FEATURE, SCO_DRAWDOWN_FEATURE, SCO_VOL_FEATURE],
        {"ATI"},
    )
    if carry_dir.name != "carry_data_2":
        raise ValueError(f"Metals live targets require carry_data_2: {carry_dir}")
    sco_carry_path = carry_dir / "SCO.csv"
    sco_carry = pd.read_csv(
        sco_carry_path,
        usecols=["date", SCO_CURVE_VOL_FEATURE, SCO_PULSE_VOL_FEATURE],
    )
    sco_carry["date"] = pd.to_datetime(sco_carry["date"], errors="coerce")
    for column in (SCO_CURVE_VOL_FEATURE, SCO_PULSE_VOL_FEATURE):
        sco_carry[column] = pd.to_numeric(sco_carry[column], errors="coerce")
    sco_carry = (
        sco_carry.dropna(subset=["date"])
        .sort_values("date")
        .drop_duplicates("date", keep="last")
        .set_index("date")
    )
    sco_curve_vol = sco_carry[SCO_CURVE_VOL_FEATURE]
    sco_pulse_vol = sco_carry[SCO_PULSE_VOL_FEATURE]

    gap_cfg = config["hg_gc_gap_gc_carry_iron"]
    gap_signal, gap_diag = dual_feature_hysteresis(
        _feature(metals, gap_cfg.signal_ticker, HG_GC_GAP_FEATURE),
        _feature(gc, gap_cfg.signal_ticker, GC_CARRY_FEATURE),
        gap_cfg.params,
    )
    vol_cfg = config["sco_vol_gc_hg_accel_miners"]
    vol_signal, vol_diag = sco_vol_accel_hysteresis(
        _feature(metals, vol_cfg.signal_ticker, GC_HG_ACCEL_FEATURE),
        sco_curve_vol,
        vol_cfg.params,
    )
    alloy_cfg = config["sco_specialty_alloys"]
    alloy_signal, alloy_diag = specialty_alloys_hysteresis(
        _feature(sco, alloy_cfg.signal_ticker, SCO_RETURN_FEATURE),
        _feature(sco, alloy_cfg.signal_ticker, SCO_DRAWDOWN_FEATURE),
        _feature(sco, alloy_cfg.signal_ticker, SCO_VOL_FEATURE),
        alloy_cfg.params,
    )
    pulse_cfg = config["sco_vol_miners"]
    pulse_signal, pulse_diag = sco_vol_regime_pulse(
        sco_pulse_vol,
        pulse_cfg.params,
    )
    miner_cfg = config["miners"]
    miner_signal, miner_diag = persistent_binary(
        _feature(metals, miner_cfg.signal_ticker, HG_GC_GAP_FEATURE),
        threshold=float(miner_cfg.params["threshold"]),
        side_mult=float(miner_cfg.params["side_mult"]),
    )
    copper_cfg = config["copper_miner"]
    copper_calendar = _feature(metals, copper_cfg.signal_ticker, HG_GC_GAP_FEATURE).index
    copper_signal, copper_diag = copper_energy_terms_of_trade_signal(
        copper_calendar,
        threshold_multiple=float(copper_cfg.params["threshold_multiple"]),
        smoothing=int(copper_cfg.params["signal_smoothing"]),
        commodity_dir=commodity_dir,
        carry_dir=carry_dir,
    )

    signals = {
        "hg_gc_gap_gc_carry_iron": gap_signal,
        "sco_vol_gc_hg_accel_miners": vol_signal,
        "sco_specialty_alloys": alloy_signal,
        "sco_vol_miners": pulse_signal,
        "copper_miner": copper_signal,
        "miners": miner_signal,
    }
    diagnostics = {
        "hg_gc_gap_gc_carry_iron": gap_diag,
        "sco_vol_gc_hg_accel_miners": vol_diag,
        "sco_specialty_alloys": alloy_diag,
        "sco_vol_miners": pulse_diag,
        "copper_miner": copper_diag,
        "miners": miner_diag,
    }
    latest_dates = {
        # Use the last actual feature value, not the last padded equity row.
        # Daily caches intentionally contain NaN feature rows when the equity
        # calendar extends beyond the latest known commodity observation.
        "metals_hg_gc_gap": _latest_valid_date(
            _feature(metals, gap_cfg.signal_ticker, HG_GC_GAP_FEATURE),
            HG_GC_GAP_FEATURE,
        ),
        "metals_gc_hg_accel": _latest_valid_date(
            _feature(metals, vol_cfg.signal_ticker, GC_HG_ACCEL_FEATURE),
            GC_HG_ACCEL_FEATURE,
        ),
        "gc_carry": _latest_valid_date(
            _feature(gc, gap_cfg.signal_ticker, GC_CARRY_FEATURE),
            GC_CARRY_FEATURE,
        ),
        "sco_ret_63d": _latest_valid_date(
            _feature(sco, alloy_cfg.signal_ticker, SCO_RETURN_FEATURE),
            SCO_RETURN_FEATURE,
        ),
        "sco_drawdown_63d": _latest_valid_date(
            _feature(sco, alloy_cfg.signal_ticker, SCO_DRAWDOWN_FEATURE),
            SCO_DRAWDOWN_FEATURE,
        ),
        "sco_realized_vol_63d": _latest_valid_date(
            _feature(sco, alloy_cfg.signal_ticker, SCO_VOL_FEATURE),
            SCO_VOL_FEATURE,
        ),
        "sco_curve_vol": _latest_valid_date(sco_curve_vol, SCO_CURVE_VOL_FEATURE),
        "sco_ret_std_20": _latest_valid_date(sco_pulse_vol, SCO_PULSE_VOL_FEATURE),
        "copper_hg_cl_ratio": _latest_valid_date(
            copper_diag["hg_cl_ratio"], "copper hg/cl ratio"
        ),
        "copper_ho_return": _latest_valid_date(copper_diag["ho_ret"], "HO return"),
    }
    return MetalsSignalBundle(
        signals=signals,
        diagnostics=diagnostics,
        latest_dates=latest_dates,
        source_paths={
            "metals_cache": metals_cache,
            "gc_cache": gc_cache,
            "sco_cache": sco_cache,
            "carry_dir": carry_dir,
            "commodity_dir": commodity_dir,
        },
    )


def target_side(
    signal: pd.Series,
    *,
    as_of: pd.Timestamp,
    target_date: pd.Timestamp,
    hold_days: int | None,
) -> float:
    as_of = pd.Timestamp(as_of).normalize()
    target_date = pd.Timestamp(target_date).normalize()
    known = pd.to_numeric(signal, errors="coerce").loc[:as_of].sort_index()
    if known.empty:
        raise ValueError(f"No signal history at or before {as_of.date()}")
    if pd.Timestamp(known.index.max()).normalize() != as_of:
        raise ValueError(
            f"Signal cache is stale: latest={known.index.max().date()} as_of={as_of.date()}"
        )
    extended = pd.concat([known, pd.Series(0.0, index=pd.DatetimeIndex([target_date]))])
    extended = extended[~extended.index.duplicated(keep="last")].sort_index()
    if hold_days is None:
        position = extended.shift(1).fillna(0.0)
    else:
        position = fixed_hold_position(extended, hold_days=hold_days, execution_lag=1)
    return float(position.loc[target_date])


def build_component_targets(
    bundle: MetalsSignalBundle,
    *,
    as_of: pd.Timestamp,
    target_date: pd.Timestamp,
    config: Mapping[str, MetalsSleeveConfig] = METALS_SLEEVE_CONFIG,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for component, cfg in config.items():
        side = target_side(
            bundle.signals[component],
            as_of=as_of,
            target_date=target_date,
            hold_days=cfg.hold_days,
        )
        diagnostic = bundle.diagnostics[component].loc[:as_of]
        latest = diagnostic.iloc[-1] if not diagnostic.empty else pd.Series(dtype=float)
        diagnostic_text = ";".join(
            f"{key}={float(value):.6g}"
            for key, value in latest.items()
            if pd.notna(value) and key not in {"long_leg", "short_leg", "signal"}
        )
        for ticker in cfg.tickers:
            internal_weight = float(cfg.internal_weights[ticker])
            rows.append(
                {
                    "component": component,
                    "instrument": ticker,
                    "feature_symbol": cfg.feature_symbol,
                    "feature": cfg.feature,
                    "mode": cfg.position_mode,
                    "hold_days": cfg.hold_days,
                    "side": side,
                    "sleeve_weight": cfg.weight,
                    "internal_weight": internal_weight,
                    "research_target_weight": side * cfg.weight * internal_weight,
                    "sector_hedge": cfg.sector_hedge,
                    "signal_date": as_of if side != 0 else pd.NaT,
                    "reason": (
                        f"{cfg.signal_rule} active; {diagnostic_text}"
                        if side != 0
                        else f"{cfg.signal_rule} inactive; {diagnostic_text}"
                    ),
                }
            )
    return pd.DataFrame(rows)


def apply_aggregate_name_cap(
    legs: pd.DataFrame,
    *,
    aum: float,
    max_weight: float = METALS_MAX_SINGLE_NAME_WEIGHT,
) -> pd.DataFrame:
    """Scale overlapping component legs pro rata after summing by ticker."""
    out = legs.copy()
    out["pre_name_cap_target_weight"] = pd.to_numeric(
        out["target_weight"], errors="coerce"
    ).fillna(0.0)
    out["name_cap_scale"] = 1.0
    for instrument, group in out.groupby("instrument", sort=False):
        total = float(group["pre_name_cap_target_weight"].sum())
        capped = float(np.clip(total, -max_weight, max_weight))
        scale = capped / total if total != 0 else 1.0
        out.loc[group.index, "name_cap_scale"] = scale
        out.loc[group.index, "target_weight"] = (
            group["pre_name_cap_target_weight"] * scale
        )
        if not np.isclose(scale, 1.0):
            out.loc[group.index, "reason"] = (
                out.loc[group.index, "reason"].astype(str)
                + f"; aggregate {instrument} capped at {max_weight:.1%}"
            )
    out["target_notional"] = out["target_weight"] * aum
    close = pd.to_numeric(out["previous_close"], errors="coerce").replace(0, np.nan)
    out["target_shares"] = out["target_notional"] / close
    out["target_weight_adjustment"] = (
        out["target_weight"] - out["research_target_weight"]
    )
    return out


validate_config()
