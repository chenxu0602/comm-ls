from __future__ import annotations

from bisect import bisect_left
from pathlib import Path

import numpy as np
import pandas as pd

from comm_ls.commodity import _load_contract_market_data


SOYBEAN_COMPLEX_SYMBOLS = ("ZS", "ZM", "ZL")
CROP_RESEARCH_SYMBOLS = ("ZC", "ZS", "ZM", "ZL")
MATCHED_CRUSH_MONTHS = frozenset("F H K N Q U".split())
MARGIN_HORIZONS = (5, 10, 21, 30, 42, 63)
OI_HORIZONS = (10, 21, 30, 42, 63)
SEASONAL_CRUSH_MONTHS = ("F", "H", "K", "N", "Q", "U", "V", "Z")
SEASONAL_CRUSH_LEG_MONTHS = {
    "ZM": SEASONAL_CRUSH_MONTHS,
    "ZL": SEASONAL_CRUSH_MONTHS,
    # Soybeans have no V/Z pairing in the executed notebook construction;
    # both late-year meal/oil contracts use the X soybean contract.
    "ZS": ("F", "H", "K", "N", "Q", "U", "X", "X"),
}
CALENDAR_MONTH_CODES = {
    1: "F", 2: "G", 3: "H", 4: "J", 5: "K", 6: "M",
    7: "N", 8: "Q", 9: "U", 10: "V", 11: "X", 12: "Z",
}


def soybean_crush_usd_per_bushel(
    soybean_cents_per_bushel: pd.Series,
    meal_usd_per_short_ton: pd.Series,
    oil_cents_per_pound: pd.Series,
) -> pd.Series:
    """Standard board-crush value using 44lb meal and 11lb oil per soybean bushel."""
    soybean_cost = pd.to_numeric(soybean_cents_per_bushel, errors="coerce") / 100.0
    meal_value = pd.to_numeric(meal_usd_per_short_ton, errors="coerce") * 44.0 / 2000.0
    oil_value = pd.to_numeric(oil_cents_per_pound, errors="coerce") * 11.0 / 100.0
    return meal_value + oil_value - soybean_cost


def build_seasonality_adjusted_soybean_crush(
    commodity_dir: Path,
    dates: pd.Index | pd.Series,
    *,
    lookback_years: int = 8,
    smooth_window: int = 10,
    smooth_min_periods: int = 5,
    earliest_contract_year: int = 2010,
) -> pd.DataFrame:
    """Port the executed agri-notebook seasonal board-crush adjustment.

    The active contract is the next listed ZM month after the observation's
    calendar month (an exact listed month advances once more).  Its raw crush
    is compared with the same contract/month/day observations from strictly
    earlier contract years.  Historical paths are centered-smoothed before
    their cross-year median is taken; this remains timestamp-safe because no
    current/future contract year enters the seasonal baseline.
    """
    if lookback_years < 1:
        raise ValueError("lookback_years must be positive")
    if not 1 <= smooth_min_periods <= smooth_window:
        raise ValueError("Require 1 <= smooth_min_periods <= smooth_window")
    commodity_dir = Path(commodity_dir)
    index = pd.DatetimeIndex(pd.to_datetime(dates, errors="raise")).normalize()
    index = pd.DatetimeIndex(sorted(index.unique()), name="date")
    markets = {
        symbol: _load_contract_market_data(commodity_dir / symbol)
        for symbol in SOYBEAN_COMPLEX_SYMBOLS
    }

    def load_contract(year: int, month_code: str) -> pd.Series | None:
        month_position = SEASONAL_CRUSH_MONTHS.index(month_code)
        legs = []
        for symbol in SOYBEAN_COMPLEX_SYMBOLS:
            contract = f"{year}{SEASONAL_CRUSH_LEG_MONTHS[symbol][month_position]}"
            frame = _contract_frame(markets[symbol], contract)
            if frame.empty:
                return None
            legs.append(frame["settle"].rename(symbol))
        joined = pd.concat(legs, axis=1)
        return soybean_crush_usd_per_bushel(joined["ZS"], joined["ZM"], joined["ZL"])

    first_year = min(index.year.min(), earliest_contract_year) if len(index) else earliest_contract_year
    last_year = index.year.max() if len(index) else earliest_contract_year
    raw_paths: dict[tuple[int, str], pd.Series] = {}
    smooth_paths: dict[tuple[int, str], pd.Series] = {}
    for year in range(max(first_year, earliest_contract_year), last_year + 1):
        for month_code in SEASONAL_CRUSH_MONTHS:
            raw = load_contract(year, month_code)
            if raw is None:
                continue
            raw_paths[(year, month_code)] = raw
            smooth_paths[(year, month_code)] = raw.rolling(
                smooth_window, min_periods=smooth_min_periods, center=True
            ).mean()

    rows = []
    for date in index:
        year = date.year
        current_code = CALENDAR_MONTH_CODES[date.month]
        position = bisect_left(SEASONAL_CRUSH_MONTHS, current_code)
        expiry_code = (
            SEASONAL_CRUSH_MONTHS[(position + 1) % len(SEASONAL_CRUSH_MONTHS)]
            if position < len(SEASONAL_CRUSH_MONTHS)
            and current_code == SEASONAL_CRUSH_MONTHS[position]
            else SEASONAL_CRUSH_MONTHS[position]
        )
        current = raw_paths.get((year, expiry_code))
        raw_value = current.get(date, np.nan) if current is not None else np.nan
        historical = []
        comparison_day = 28 if date.day == 29 else date.day
        for prior_year in range(
            max(year - lookback_years, earliest_contract_year), year
        ):
            path = smooth_paths.get((prior_year, expiry_code))
            if path is None:
                continue
            comparison_date = pd.Timestamp(prior_year, date.month, comparison_day)
            available = path.loc[path.index >= comparison_date]
            if not available.empty:
                historical.append(float(available.iloc[0]))
        median = float(np.median(historical)) if historical else np.nan
        rows.append({
            "date": date,
            "seasonal_crush_contract": f"{year}{expiry_code}",
            "raw": raw_value,
            "median": median,
            "adjusted": raw_value - median,
        })
    return pd.DataFrame(rows).set_index("date")


def _contract_frame(market: pd.DataFrame, contract: str) -> pd.DataFrame:
    columns = ["date", "settle", "volume", "open_interest"]
    frame = market.loc[market["contract"].eq(contract), columns].copy()
    if frame.empty:
        return frame.set_index("date")
    frame = frame.sort_values("date").drop_duplicates("date", keep="last").set_index("date")
    for column in columns[1:]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    return frame


def _common_contracts(markets: dict[str, pd.DataFrame]) -> list[str]:
    common = set.intersection(
        *(set(frame["contract"].dropna().astype(str)) for frame in markets.values())
    )
    return sorted(
        contract
        for contract in common
        if len(contract) == 5
        and contract[:4].isdigit()
        and contract[-1] in MATCHED_CRUSH_MONTHS
    )


def build_matched_soybean_crush(
    commodity_dir: Path,
    liquidity_window: int = 3,
    liquidity_lag: int = 1,
) -> pd.DataFrame:
    """Build a point-in-time, same-expiry soybean board-crush series."""
    markets = {
        symbol: _load_contract_market_data(commodity_dir / symbol)
        for symbol in SOYBEAN_COMPLEX_SYMBOLS
    }
    missing = [symbol for symbol, frame in markets.items() if frame.empty]
    if missing:
        raise ValueError(f"No contract market data found for: {missing}")

    candidates: list[pd.DataFrame] = []
    for contract in _common_contracts(markets):
        frames = {
            symbol: _contract_frame(markets[symbol], contract)
            for symbol in SOYBEAN_COMPLEX_SYMBOLS
        }
        if any(frame.empty for frame in frames.values()):
            continue
        joined = pd.concat(
            {
                symbol: frame[["settle", "volume", "open_interest"]]
                for symbol, frame in frames.items()
            },
            axis=1,
            join="inner",
        ).dropna(subset=[("ZS", "settle"), ("ZM", "settle"), ("ZL", "settle")])
        if joined.empty:
            continue

        out = pd.DataFrame(index=joined.index)
        out["matched_soybean_crush_contract"] = contract
        out["matched_soybean_crush_spread"] = soybean_crush_usd_per_bushel(
            joined[("ZS", "settle")],
            joined[("ZM", "settle")],
            joined[("ZL", "settle")],
        )
        activity_parts = []
        for symbol in SOYBEAN_COMPLEX_SYMBOLS:
            activity = joined[(symbol, "open_interest")].where(
                joined[(symbol, "open_interest")].gt(0),
                joined[(symbol, "volume")],
            )
            activity_parts.append(np.log1p(activity.clip(lower=0)))
        out["matched_soybean_crush_roll_activity"] = (
            pd.concat(activity_parts, axis=1).mean(axis=1, skipna=False)
            .rolling(liquidity_window, min_periods=1).mean()
            .shift(liquidity_lag)
        )
        for horizon in MARGIN_HORIZONS:
            out[f"matched_soybean_crush_spread_chg_{horizon}d"] = (
                out["matched_soybean_crush_spread"].diff(horizon)
            )
        candidates.append(out.reset_index(names="date"))

    if not candidates:
        raise ValueError("No complete matched ZS/ZM/ZL contract observations were found")

    panel = pd.concat(candidates, ignore_index=True)
    panel["contract_month"] = pd.to_datetime(
        panel["matched_soybean_crush_contract"].str[:4]
        + panel["matched_soybean_crush_contract"].str[-1].map(
            {"F": "01", "H": "03", "K": "05", "N": "07", "Q": "08", "U": "09"}
        ),
        format="%Y%m",
    )
    panel = panel.loc[panel["contract_month"].ge(panel["date"].dt.to_period("M").dt.start_time)]
    panel = panel.sort_values(
        ["date", "matched_soybean_crush_roll_activity", "contract_month"],
        ascending=[True, False, True],
        na_position="last",
    )
    rows: list[pd.Series] = []
    active_month: pd.Timestamp | None = None
    for _, daily in panel.groupby("date", sort=True):
        eligible = daily if active_month is None else daily.loc[daily["contract_month"].ge(active_month)]
        if eligible.empty:
            continue
        choice = eligible.iloc[0]
        rows.append(choice)
        active_month = choice["contract_month"]
    selected = pd.DataFrame(rows).sort_values("date")
    return selected.drop(columns="contract_month").reset_index(drop=True)


def _rolling_z(series: pd.Series, window: int = 252, min_periods: int = 126) -> pd.Series:
    numeric = pd.to_numeric(series, errors="coerce")
    mean = numeric.rolling(window, min_periods=min_periods).mean()
    std = numeric.rolling(window, min_periods=min_periods).std(ddof=0).replace(0.0, np.nan)
    return (numeric - mean) / std


def _arrival_by_date(signals: pd.DataFrame, symbols: tuple[str, ...]) -> pd.Series:
    subset = signals.loc[signals["symbol"].isin(symbols), ["date", "arrival"]].copy()
    subset["arrival"] = pd.to_datetime(subset["arrival"], errors="coerce")
    return subset.groupby("date")["arrival"].max()


def _cross_oi_features(signals: pd.DataFrame) -> pd.DataFrame:
    dates = pd.Index(sorted(signals["date"].dropna().unique()), name="date")
    output = pd.DataFrame(index=dates)
    for horizon in OI_HORIZONS:
        column = f"oi_shock_{horizon}d"
        pivot = signals.loc[signals["symbol"].isin(SOYBEAN_COMPLEX_SYMBOLS)].pivot_table(
            index="date", columns="symbol", values=column, aggfunc="last"
        )
        standardized = pivot.apply(_rolling_z)
        output[f"zm_minus_zs_oi_shock_{horizon}d_z_spread"] = (
            standardized.get("ZM") - standardized.get("ZS")
        )
        output[f"zl_minus_zs_oi_shock_{horizon}d_z_spread"] = (
            standardized.get("ZL") - standardized.get("ZS")
        )
    return output.reset_index()


def _corn_processing_features(signals: pd.DataFrame) -> pd.DataFrame:
    symbols = ("ZC", "XB", "CL", "NG")
    output: pd.DataFrame | None = None
    for horizon in MARGIN_HORIZONS:
        source = f"front_log_ret_{horizon}d_v2"
        pivot = signals.loc[signals["symbol"].isin(symbols)].pivot_table(
            index="date", columns="symbol", values=source, aggfunc="last"
        )
        frame = pd.DataFrame(index=pivot.index)
        frame[f"corn_ethanol_output_input_momentum_{horizon}d"] = pivot["XB"] - pivot["ZC"]
        frame[f"corn_processing_energy_cost_tailwind_{horizon}d"] = -pivot["NG"]
        frame[f"corn_processing_margin_proxy_chg_{horizon}d"] = (
            pivot["XB"] - pivot["ZC"] - pivot["NG"]
        )
        frame[f"corn_crude_demand_context_{horizon}d"] = pivot["CL"] - pivot["ZC"]
        output = frame if output is None else output.join(frame, how="outer")
    if output is None:
        return pd.DataFrame(columns=["date"])
    return output.reset_index()


def build_soybean_complex_signals(
    commodity_signals: pd.DataFrame,
    commodity_dir: Path,
) -> pd.DataFrame:
    """Add matched crush, cross-OI, and corn-processing proxies to crop signals."""
    required = {"date", "arrival", "symbol", *(f"oi_shock_{h}d" for h in OI_HORIZONS)}
    missing = required.difference(commodity_signals.columns)
    if missing:
        raise ValueError(f"Commodity signals are missing required columns: {sorted(missing)}")
    signals = commodity_signals.copy()
    signals["date"] = pd.to_datetime(signals["date"], errors="coerce").dt.normalize()
    signals["symbol"] = signals["symbol"].astype(str).str.upper().str.strip()
    output = signals.loc[signals["symbol"].isin(CROP_RESEARCH_SYMBOLS)].copy()

    crush = build_matched_soybean_crush(commodity_dir)
    cross_oi = _cross_oi_features(signals)
    corn = _corn_processing_features(signals)
    soybean_features = crush.merge(cross_oi, on="date", how="outer")
    output = output.merge(soybean_features, on="date", how="left")
    output = output.merge(corn, on="date", how="left")

    soybean_rows = output["symbol"].isin(SOYBEAN_COMPLEX_SYMBOLS)
    corn_rows = output["symbol"].eq("ZC")
    soybean_derived = set(soybean_features.columns) - {"date"}
    corn_derived = set(corn.columns) - {"date"}
    output.loc[~soybean_rows, list(soybean_derived)] = np.nan
    output.loc[~corn_rows, list(corn_derived)] = np.nan

    soybean_arrival = _arrival_by_date(signals, SOYBEAN_COMPLEX_SYMBOLS)
    corn_arrival = _arrival_by_date(signals, ("ZC", "XB", "CL", "NG"))
    own_arrival = pd.to_datetime(output["arrival"], errors="coerce")
    derived_arrival = output["date"].map(soybean_arrival).where(
        soybean_rows, output["date"].map(corn_arrival).where(corn_rows)
    )
    output["arrival"] = pd.concat([own_arrival, derived_arrival], axis=1).max(axis=1)
    return output.sort_values(["symbol", "date"]).reset_index(drop=True)


def build_soybean_complex_signals_from_paths(
    commodity_signals_path: Path,
    commodity_dir: Path,
    output_path: Path,
) -> pd.DataFrame:
    signals = (
        pd.read_parquet(commodity_signals_path)
        if commodity_signals_path.suffix == ".parquet"
        else pd.read_csv(commodity_signals_path)
    )
    output = build_soybean_complex_signals(signals, commodity_dir)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix == ".parquet":
        output.to_parquet(output_path, index=False)
    elif output_path.suffix == ".csv":
        output.to_csv(output_path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")
    return output
