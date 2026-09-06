from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from comm_ls.commodity import _load_contract_market_data


SOYBEAN_COMPLEX_SYMBOLS = ("ZS", "ZM", "ZL")
CROP_RESEARCH_SYMBOLS = ("ZC", "ZS", "ZM", "ZL")
MATCHED_CRUSH_MONTHS = frozenset("F H K N Q U".split())
MARGIN_HORIZONS = (5, 10, 21, 30, 42, 63)
OI_HORIZONS = (10, 21, 30, 42, 63)


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
