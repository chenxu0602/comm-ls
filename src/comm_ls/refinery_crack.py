from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from comm_ls.commodity import FUTURES_MONTH_CODES, _load_contract_market_data


REFINERY_CRACK_SYMBOL = "REFINERY_CRACK"
REFINERY_COMPONENTS = ("CL", "HO", "XB")
CRACK_BLEND_WEIGHTS = {
    "crack_01": 0.50,
    "crack_02": 0.20,
    "crack_03": 0.30,
}
ROLL_COLUMN_ALIASES = {
    "open int": "open_interest",
    "open_interest": "open_interest",
    "volume": "volume",
}


def _available_contract_years(market: pd.DataFrame, month: str) -> set[int]:
    contracts = market["contract"].astype("string")
    years = pd.to_numeric(
        contracts.str.extract(rf"^(\d{{4}}){month}$", expand=False),
        errors="coerce",
    )
    return set(years.dropna().astype(int).tolist())


def _contract_frame(market: pd.DataFrame, contract: str) -> pd.DataFrame:
    frame = market.loc[
        market["contract"].eq(contract),
        ["date", "settle", "volume", "open_interest"],
    ].copy()
    if frame.empty:
        return frame.set_index("date")
    frame = frame.sort_values("date").drop_duplicates("date", keep="last").set_index("date")
    settle = pd.to_numeric(frame["settle"], errors="coerce")
    frame["contract_log_return"] = np.log(settle.where(settle > 0)).diff()
    return frame


def crack_crossover_signal(value: pd.Series, side_mult: float = 1.0) -> pd.Series:
    """Reproduce the notebook's MA3/MA50 entry and MA3/MA30 exit state."""
    numeric = pd.to_numeric(value, errors="coerce")
    ma_3 = numeric.rolling(3, min_periods=1).mean()
    ma_30 = numeric.rolling(30, min_periods=15).mean()
    ma_50 = numeric.rolling(50, min_periods=25).mean()

    long_state = pd.Series(np.nan, index=numeric.index, dtype=float)
    short_state = pd.Series(np.nan, index=numeric.index, dtype=float)
    long_state.loc[ma_3 > ma_50] = 1.0 * side_mult
    long_state.loc[ma_3 < ma_30] = 0.0
    short_state.loc[ma_3 < ma_50] = -0.5 * side_mult
    short_state.loc[ma_3 > ma_30] = 0.0

    return long_state.ffill().fillna(0.0) + short_state.ffill().fillna(0.0)


def add_crack_crossover_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Add diagnostics and the notebook's crossover states to crack levels."""
    output = frame.copy()
    positions: list[str] = []
    for crack in CRACK_BLEND_WEIGHTS:
        value = pd.to_numeric(output[crack], errors="coerce")
        ma_3 = value.rolling(3, min_periods=1).mean()
        ma_30 = value.rolling(30, min_periods=15).mean()
        ma_50 = value.rolling(50, min_periods=25).mean()

        output[f"{crack}_ma_3"] = ma_3
        output[f"{crack}_ma_30"] = ma_30
        output[f"{crack}_ma_50"] = ma_50
        output[f"{crack}_ma_gap_3d_30d"] = ma_3 - ma_30
        output[f"{crack}_ma_gap_3d_50d"] = ma_3 - ma_50

        position = f"{crack}_crossover_position"
        output[position] = crack_crossover_signal(value)
        positions.append(position)

    output["june_crack_blend_crossover_position"] = sum(
        CRACK_BLEND_WEIGHTS[crack] * output[position]
        for crack, position in zip(CRACK_BLEND_WEIGHTS, positions, strict=True)
    )
    return output


def _arrival_by_date(
    dates: pd.Series,
    commodity_signals: pd.DataFrame | None,
) -> pd.Series:
    normalized_dates = pd.to_datetime(dates, errors="coerce").dt.normalize()
    conservative = normalized_dates + pd.Timedelta(days=1, hours=8)
    if commodity_signals is None:
        return conservative

    required = {"date", "arrival", "symbol"}
    missing = required.difference(commodity_signals.columns)
    if missing:
        raise ValueError(f"Commodity signals are missing required columns: {sorted(missing)}")
    signals = commodity_signals.copy()
    signals["symbol"] = signals["symbol"].astype(str).str.upper().str.strip()
    signals = signals.loc[signals["symbol"].isin(REFINERY_COMPONENTS), ["date", "arrival"]]
    signals["date"] = pd.to_datetime(signals["date"], errors="coerce").dt.normalize()
    signals["arrival"] = pd.to_datetime(signals["arrival"], errors="coerce")
    upstream = signals.groupby("date")["arrival"].max()
    aligned = normalized_dates.map(upstream)
    return pd.concat(
        [conservative.rename("conservative"), aligned.rename("upstream")],
        axis=1,
    ).max(axis=1)


def build_refinery_crack_signals(
    commodity_dir: Path,
    commodity_signals: pd.DataFrame | None = None,
    month: str = "M",
    roll_by: str = "open_interest",
    start_year: int = 2010,
    end_year: int | None = None,
    liquidity_window: int = 3,
    liquidity_lag: int = 1,
    roll_mode: str = "point_in_time",
) -> pd.DataFrame:
    """Build fixed-calendar refinery crack features with live-data fallback."""
    month = month.upper().strip()
    if month not in FUTURES_MONTH_CODES:
        raise ValueError(f"Unknown futures month code: {month}")
    if roll_by not in ROLL_COLUMN_ALIASES:
        raise ValueError(f"roll_by must be one of {sorted(ROLL_COLUMN_ALIASES)}")
    if liquidity_window < 1 or liquidity_lag < 0:
        raise ValueError("liquidity_window must be positive and liquidity_lag non-negative")
    if roll_mode not in {"point_in_time", "notebook_compatible"}:
        raise ValueError("roll_mode must be 'point_in_time' or 'notebook_compatible'")
    liquidity_column = ROLL_COLUMN_ALIASES[roll_by]

    market = {
        symbol: _load_contract_market_data(commodity_dir / symbol)
        for symbol in REFINERY_COMPONENTS
    }
    missing_symbols = [symbol for symbol, frame in market.items() if frame.empty]
    if missing_symbols:
        raise ValueError(f"No contract market data found for: {missing_symbols}")

    common_years = set.intersection(
        *(_available_contract_years(market[symbol], month) for symbol in REFINERY_COMPONENTS)
    )
    if not common_years:
        raise ValueError(f"No common {month} contracts found for CL/HO/XB")
    if end_year is None:
        end_year = max(common_years)
    years = [year for year in sorted(common_years) if start_year <= year <= end_year]

    contracts: list[dict[str, object]] = []
    for year in years:
        contract = f"{year}{month}"
        frames = {
            symbol: _contract_frame(market[symbol], contract)
            for symbol in REFINERY_COMPONENTS
        }
        if any(frame.empty for frame in frames.values()):
            continue
        raw_liquidity = (
            pd.to_numeric(frames["CL"][liquidity_column], errors="coerce")
            .rolling(liquidity_window, min_periods=1)
            .mean()
        )
        liquidity = (
            raw_liquidity
            .shift(liquidity_lag)
        )
        contracts.append(
            {
                "year": year,
                "contract": contract,
                "frames": frames,
                "liquidity": liquidity,
                "raw_liquidity": raw_liquidity,
            }
        )
    if not contracts:
        raise ValueError(f"No complete CL/HO/XB {month} contract sets were found")

    all_dates = pd.DatetimeIndex([])
    for item in contracts:
        for frame in item["frames"].values():
            all_dates = all_dates.union(frame.index)
    all_dates = all_dates.sort_values()

    def value(series: pd.Series, date: pd.Timestamp) -> float:
        result = series.get(date, np.nan)
        return float(result) if pd.notna(result) else np.nan

    rows: list[dict[str, object]] = []

    def append_row(item: dict[str, object], date: pd.Timestamp, liquidity_key: str) -> None:
        frames = item["frames"]
        settles = {
            symbol: value(frames[symbol]["settle"], date)
            for symbol in REFINERY_COMPONENTS
        }
        if not all(np.isfinite(list(settles.values()))):
            return
        rows.append(
            {
                "date": date,
                "june_contract": item["contract"],
                "roll_liquidity": value(item[liquidity_key], date),
                "cl_settle": settles["CL"],
                "ho_settle": settles["HO"],
                "xb_settle": settles["XB"],
                "cl_contract_log_return": value(frames["CL"]["contract_log_return"], date),
                "ho_contract_log_return": value(frames["HO"]["contract_log_return"], date),
                "xb_contract_log_return": value(frames["XB"]["contract_log_return"], date),
            }
        )

    if roll_mode == "point_in_time":
        active = 0
        for date in all_dates:
            while active + 1 < len(contracts):
                current_score = value(contracts[active]["liquidity"], date)
                next_score = value(contracts[active + 1]["liquidity"], date)
                if not (
                    np.isfinite(next_score)
                    and (not np.isfinite(current_score) or next_score > current_score)
                ):
                    break
                active += 1
            append_row(contracts[active], date, "liquidity")
    else:
        # Exact research replication only. The last crossover date is selected
        # with future information and therefore must not be used for live/PIT claims.
        start: pd.Timestamp | None = None
        for current, following in zip(contracts[:-1], contracts[1:], strict=True):
            comparison = pd.concat(
                {
                    "current": current["raw_liquidity"],
                    "following": following["raw_liquidity"],
                },
                axis=1,
            )
            eligible = comparison.index[comparison["current"] >= comparison["following"]]
            if eligible.empty:
                continue
            end = eligible[-1]
            if start is None:
                start = eligible[0]
            for date in all_dates[(all_dates >= start) & (all_dates < end)]:
                append_row(current, date, "raw_liquidity")
            start = end

        last = contracts[-1]
        if start is None:
            frame_dates = pd.DatetimeIndex(last["frames"]["CL"].index)
            start = frame_dates.min()
        for date in all_dates[all_dates >= start]:
            append_row(last, date, "raw_liquidity")
    if not rows:
        raise ValueError("No overlapping fixed-calendar CL/HO/XB observations were found")

    output = pd.DataFrame(rows).sort_values("date").drop_duplicates("date", keep="last")
    output["crack_01"] = output["ho_settle"] / 100.0 * 42.0 - output["cl_settle"]
    output["crack_02"] = (
        output["xb_settle"] / 100.0 * 42.0 * 2.0
        + output["ho_settle"] / 100.0 * 42.0
        - output["cl_settle"] * 3.0
    )
    output["crack_03"] = (
        output["xb_settle"] / 100.0 * 42.0 * 3.0
        + output["ho_settle"] / 100.0 * 42.0 * 2.0
        - output["cl_settle"] * 5.0
    )
    output = add_crack_crossover_features(output)
    output.insert(1, "arrival", _arrival_by_date(output["date"], commodity_signals))
    output.insert(2, "symbol", REFINERY_CRACK_SYMBOL)
    output.insert(3, "roll_mode", roll_mode)
    return output.reset_index(drop=True)


def build_refinery_crack_signals_from_paths(
    commodity_signals_path: Path,
    commodity_dir: Path,
    output_path: Path,
    **kwargs: object,
) -> pd.DataFrame:
    if commodity_signals_path.suffix == ".parquet":
        commodity_signals = pd.read_parquet(commodity_signals_path)
    else:
        commodity_signals = pd.read_csv(commodity_signals_path)
    output = build_refinery_crack_signals(
        commodity_dir=commodity_dir,
        commodity_signals=commodity_signals,
        **kwargs,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix == ".parquet":
        output.to_parquet(output_path, index=False)
    elif output_path.suffix == ".csv":
        output.to_csv(output_path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")
    return output
