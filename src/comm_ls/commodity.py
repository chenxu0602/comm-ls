from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


REQUIRED_CARRY_COLUMNS = {
    "date",
    "arrival",
    "carry",
    "contango",
    "backwardation",
    "M0_settle",
    "M1_settle",
    "M2_settle",
    "total_volume",
    "total_oi",
}


FUTURES_MONTH_CODES = {
    "F": 1,
    "G": 2,
    "H": 3,
    "J": 4,
    "K": 5,
    "M": 6,
    "N": 7,
    "Q": 8,
    "U": 9,
    "V": 10,
    "X": 11,
    "Z": 12,
}
FUTURES_MONTH_NUMBERS = {month: code for code, month in FUTURES_MONTH_CODES.items()}

ALL_CONTRACT_MONTHS = tuple(range(1, 13))
ACTIVE_CONTRACT_MONTHS_BY_SYMBOL = {
    # CL trades every listed month, with December usually the best fixed-calendar anchor.
    "CL": ALL_CONTRACT_MONTHS,
    # Precious metals concentrate liquidity in even months.
    "GC": (2, 4, 6, 8, 10, 12),
    # SI/HG concentrate liquidity in odd months, but November is thin and December is active.
    "SI": (1, 3, 5, 7, 9, 12),
    "HG": (1, 3, 5, 7, 9, 12),
}
LIQUID_DEFERRED_MIN_MONTHS = 6


def _rolling_z(value: pd.Series, window: int = 252, min_periods: int = 63) -> pd.Series:
    mean = value.rolling(window, min_periods=min_periods).mean()
    std = value.rolling(window, min_periods=min_periods).std()
    return (value - mean) / std


def _rolling_pctile(value: pd.Series, window: int = 252, min_periods: int = 63) -> pd.Series:
    return value.rolling(window, min_periods=min_periods).rank(pct=True)


def _safe_log_ratio(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    ratio = numerator / denominator
    return np.log(ratio.where(ratio > 0))


def _contract_month_start(contract: pd.Series) -> pd.Series:
    text = contract.astype("string").str.strip().str.upper()
    year = pd.to_numeric(text.str.extract(r"^(\d{4})", expand=False), errors="coerce")
    code = text.str.extract(r"([FGHJKMNQUVXZ])$", expand=False)
    month = code.map(FUTURES_MONTH_CODES)
    date_text = (
        year.astype("Int64").astype("string")
        + "-"
        + month.astype("Int64").astype("string").str.zfill(2)
        + "-01"
    )
    return pd.to_datetime(date_text, errors="coerce")


def _contract_for_year_month(year: int, month: int) -> str:
    return f"{year}{FUTURES_MONTH_NUMBERS[month]}"


def _liquid_deferred_contract(
    front_contract: pd.Series,
    symbol: str,
    min_months: int = LIQUID_DEFERRED_MIN_MONTHS,
) -> pd.Series:
    active_months = ACTIVE_CONTRACT_MONTHS_BY_SYMBOL.get(symbol.upper(), ALL_CONTRACT_MONTHS)
    front_month = _contract_month_start(front_contract)
    contracts: list[object] = []

    for value in front_month:
        if pd.isna(value):
            contracts.append(pd.NA)
            continue

        target = value + pd.DateOffset(months=min_months)
        selected = pd.NA
        for year in range(target.year, target.year + 3):
            for month in active_months:
                candidate = pd.Timestamp(year=year, month=month, day=1)
                if candidate >= target:
                    selected = _contract_for_year_month(year, month)
                    break
            if not pd.isna(selected):
                break
        contracts.append(selected)

    return pd.Series(contracts, index=front_contract.index, dtype="string")


def _load_contract_market_data(symbol_dir: Path) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for path in sorted(symbol_dir.glob("*.csv")):
        contract = path.stem.upper()
        df = pd.read_csv(path)
        required = {"date", "px_settle", "px_last"}
        if required.difference(df.columns):
            continue
        df["date"] = pd.to_datetime(df["date"], utc=False)
        df["contract"] = contract
        settle = pd.to_numeric(df["px_settle"], errors="coerce")
        last = pd.to_numeric(df["px_last"], errors="coerce")
        df["settle"] = settle.fillna(last)
        df["volume"] = pd.to_numeric(df["volume"], errors="coerce") if "volume" in df.columns else np.nan
        df["open_interest"] = pd.to_numeric(df["open int"], errors="coerce") if "open int" in df.columns else np.nan
        frames.append(df[["date", "contract", "settle", "volume", "open_interest"]])

    if not frames:
        return pd.DataFrame(columns=["date", "contract", "settle", "volume", "open_interest"])
    out = pd.concat(frames, ignore_index=True)
    out["contract_month"] = _contract_month_start(out["contract"])
    return out.dropna(subset=["date", "contract_month"]).reset_index(drop=True)


def _activity_deferred_contract(
    dates: pd.Series,
    front_contract: pd.Series,
    symbol_dir: Path,
    symbol: str,
    min_months: int = LIQUID_DEFERRED_MIN_MONTHS,
) -> pd.DataFrame:
    fallback = _liquid_deferred_contract(front_contract=front_contract, symbol=symbol, min_months=min_months)
    base = pd.DataFrame(
        {
            "date": pd.to_datetime(dates, utc=False),
            "front_contract": front_contract.astype("string"),
            "fallback_contract": fallback,
        },
        index=front_contract.index,
    )
    base["front_month"] = _contract_month_start(base["front_contract"])
    base["target_month"] = base["front_month"] + pd.DateOffset(months=min_months)

    market = _load_contract_market_data(symbol_dir)
    if market.empty:
        return pd.DataFrame(
            {
                "activity_deferred_contract": fallback,
                "activity_deferred_volume": np.nan,
                "activity_deferred_open_interest": np.nan,
                "activity_deferred_activity_score": np.nan,
            },
            index=front_contract.index,
        )

    candidates = market.merge(base[["date", "target_month"]], on="date", how="inner")
    candidates = candidates[
        candidates["contract_month"].ge(candidates["target_month"])
        & pd.to_numeric(candidates["settle"], errors="coerce").gt(0)
    ].copy()
    candidates["activity_score"] = candidates["open_interest"].fillna(0.0) + candidates["volume"].fillna(0.0)
    candidates = candidates[candidates["activity_score"] > 0].copy()
    if candidates.empty:
        selected = pd.DataFrame(columns=["date", "contract", "volume", "open_interest", "activity_score"])
    else:
        selected = candidates.sort_values(
            ["date", "activity_score", "open_interest", "volume", "contract_month"],
            ascending=[True, False, False, False, True],
        ).drop_duplicates("date", keep="first")

    aligned = base[["date", "fallback_contract"]].merge(
        selected[["date", "contract", "volume", "open_interest", "activity_score"]],
        on="date",
        how="left",
    )
    contract = aligned["contract"].astype("string").fillna(aligned["fallback_contract"].astype("string"))
    return pd.DataFrame(
        {
            "activity_deferred_contract": contract.to_numpy(),
            "activity_deferred_volume": aligned["volume"].to_numpy(dtype=float),
            "activity_deferred_open_interest": aligned["open_interest"].to_numpy(dtype=float),
            "activity_deferred_activity_score": aligned["activity_score"].to_numpy(dtype=float),
        },
        index=front_contract.index,
    )


def _year_fraction_between_contracts(front_contract: pd.Series, deferred_contract: pd.Series) -> pd.Series:
    front_month = _contract_month_start(front_contract)
    deferred_month = _contract_month_start(deferred_contract)
    days = (deferred_month - front_month).dt.days
    return days.where(days > 0) / 365.25


def _annualized_log_spread(
    front_price: pd.Series,
    deferred_price: pd.Series,
    front_contract: pd.Series,
    deferred_contract: pd.Series,
) -> pd.Series:
    year_fraction = _year_fraction_between_contracts(front_contract, deferred_contract)
    return _safe_log_ratio(deferred_price, front_price) / year_fraction


def _consecutive_days(condition: pd.Series) -> pd.Series:
    condition = condition.fillna(False).astype(bool)
    groups = condition.ne(condition.shift(fill_value=False)).cumsum()
    return condition.groupby(groups).cumcount().add(1).where(condition, 0)


def load_carry_file(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    missing = REQUIRED_CARRY_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"{path} is missing required columns: {sorted(missing)}")

    df = df.copy()
    df["symbol"] = path.stem
    df["date"] = pd.to_datetime(df["date"], utc=False)
    df["arrival"] = pd.to_datetime(df["arrival"], utc=False)

    text_cols = {"symbol", "date", "arrival", "M0_con", "M1_con", "M2_con"}
    numeric_cols = [col for col in df.columns if col not in text_cols]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
    for col in ["M0_con", "M1_con", "M2_con"]:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip().str.upper()
    return df.sort_values("date").reset_index(drop=True)


def load_carry_directory(input_dir: Path) -> pd.DataFrame:
    frames = [load_carry_file(path) for path in sorted(input_dir.glob("*.csv"))]
    if not frames:
        raise FileNotFoundError(f"No carry CSV files found in {input_dir}")
    return pd.concat(frames, ignore_index=True)


def _load_contract_settles(
    symbol_dir: Path,
    contracts: pd.Series,
    contract_column: str = "calendar_dec_contract",
    settle_column: str = "calendar_dec_settle",
) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for contract in sorted(contracts.dropna().astype(str).unique()):
        path = symbol_dir / f"{contract}.csv"
        if not path.exists():
            continue
        df = pd.read_csv(path, usecols=["date", "px_settle", "px_last"])
        df["date"] = pd.to_datetime(df["date"], utc=False)
        df[contract_column] = contract
        settle = pd.to_numeric(df["px_settle"], errors="coerce")
        last = pd.to_numeric(df["px_last"], errors="coerce")
        df[settle_column] = settle.fillna(last)
        frames.append(df[["date", contract_column, settle_column]])

    if not frames:
        return pd.DataFrame(columns=["date", contract_column, settle_column])
    return pd.concat(frames, ignore_index=True)


def _same_contract_log_return(settle: pd.Series, contract: pd.Series, periods: int) -> pd.Series:
    value = np.log(settle.where(settle > 0)).diff(periods)
    return value.where(contract == contract.shift(periods))


def add_calendar_contract_features(signals: pd.DataFrame, commodity_dir: Path) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for symbol, group in signals.groupby("symbol", sort=True):
        g = group.sort_values("date").copy()
        g["calendar_dec_contract"] = g["date"].dt.year.astype(str) + "Z"
        g["next_jun_contract"] = (g["date"].dt.year + 1).astype(str) + "M"
        g["liquid_deferred_contract"] = _liquid_deferred_contract(g["M0_con"], symbol=symbol)
        activity_deferred = _activity_deferred_contract(
            dates=g["date"],
            front_contract=g["M0_con"],
            symbol_dir=commodity_dir / symbol,
            symbol=symbol,
        )
        for col in activity_deferred.columns:
            g[col] = activity_deferred[col].to_numpy()

        dec_settles = _load_contract_settles(
            symbol_dir=commodity_dir / symbol,
            contracts=g["calendar_dec_contract"],
            contract_column="calendar_dec_contract",
            settle_column="calendar_dec_settle",
        )
        if dec_settles.empty:
            g["calendar_dec_settle"] = np.nan
        else:
            g = g.merge(dec_settles, on=["date", "calendar_dec_contract"], how="left")

        year_fraction = _year_fraction_between_contracts(g["M0_con"], g["calendar_dec_contract"])
        g["calendar_dec_annualized_carry"] = (
            _safe_log_ratio(g["calendar_dec_settle"], g["front_settle"]) / year_fraction
        )
        g["calendar_dec_backwardation_steepness"] = -g["calendar_dec_annualized_carry"]
        g["calendar_dec_annualized_carry_chg_21d"] = g["calendar_dec_annualized_carry"].diff(21)
        g["calendar_dec_annualized_carry_z_252d"] = _rolling_z(g["calendar_dec_annualized_carry"])
        g["calendar_dec_backwardation_steepness_chg_21d"] = g["calendar_dec_backwardation_steepness"].diff(21)
        g["calendar_dec_backwardation_steepness_z_252d"] = _rolling_z(
            g["calendar_dec_backwardation_steepness"]
        )
        g["calendar_dec_log_ret_1d"] = _same_contract_log_return(
            g["calendar_dec_settle"],
            g["calendar_dec_contract"],
            periods=1,
        )
        g["calendar_dec_log_ret_5d"] = _same_contract_log_return(
            g["calendar_dec_settle"],
            g["calendar_dec_contract"],
            periods=5,
        )
        g["calendar_dec_log_ret_21d"] = _same_contract_log_return(
            g["calendar_dec_settle"],
            g["calendar_dec_contract"],
            periods=21,
        )

        next_jun_settles = _load_contract_settles(
            symbol_dir=commodity_dir / symbol,
            contracts=g["next_jun_contract"],
            contract_column="next_jun_contract",
            settle_column="next_jun_settle",
        )
        if next_jun_settles.empty:
            g["next_jun_settle"] = np.nan
        else:
            g = g.merge(next_jun_settles, on=["date", "next_jun_contract"], how="left")

        g["next_jun_log_ret_1d"] = _same_contract_log_return(
            g["next_jun_settle"],
            g["next_jun_contract"],
            periods=1,
        )
        g["next_jun_log_ret_5d"] = _same_contract_log_return(
            g["next_jun_settle"],
            g["next_jun_contract"],
            periods=5,
        )
        g["next_jun_log_ret_21d"] = _same_contract_log_return(
            g["next_jun_settle"],
            g["next_jun_contract"],
            periods=21,
        )
        g["next_jun_annualized_carry"] = (
            _safe_log_ratio(g["next_jun_settle"], g["front_settle"])
            / _year_fraction_between_contracts(g["M0_con"], g["next_jun_contract"])
        )
        g["next_jun_backwardation_steepness"] = -g["next_jun_annualized_carry"]
        g["next_jun_annualized_carry_chg_21d"] = g["next_jun_annualized_carry"].diff(21)
        g["next_jun_annualized_carry_z_252d"] = _rolling_z(g["next_jun_annualized_carry"])
        g["next_jun_backwardation_steepness_chg_21d"] = g["next_jun_backwardation_steepness"].diff(21)
        g["next_jun_backwardation_steepness_z_252d"] = _rolling_z(g["next_jun_backwardation_steepness"])

        liquid_deferred_settles = _load_contract_settles(
            symbol_dir=commodity_dir / symbol,
            contracts=g["liquid_deferred_contract"],
            contract_column="liquid_deferred_contract",
            settle_column="liquid_deferred_settle",
        )
        if liquid_deferred_settles.empty:
            g["liquid_deferred_settle"] = np.nan
        else:
            g = g.merge(liquid_deferred_settles, on=["date", "liquid_deferred_contract"], how="left")

        g["liquid_deferred_log_ret_1d"] = _same_contract_log_return(
            g["liquid_deferred_settle"],
            g["liquid_deferred_contract"],
            periods=1,
        )
        g["liquid_deferred_log_ret_5d"] = _same_contract_log_return(
            g["liquid_deferred_settle"],
            g["liquid_deferred_contract"],
            periods=5,
        )
        g["liquid_deferred_log_ret_21d"] = _same_contract_log_return(
            g["liquid_deferred_settle"],
            g["liquid_deferred_contract"],
            periods=21,
        )
        g["liquid_deferred_annualized_carry"] = (
            _safe_log_ratio(g["liquid_deferred_settle"], g["front_settle"])
            / _year_fraction_between_contracts(g["M0_con"], g["liquid_deferred_contract"])
        )
        g["liquid_deferred_backwardation_steepness"] = -g["liquid_deferred_annualized_carry"]
        g["liquid_deferred_annualized_carry_chg_21d"] = g["liquid_deferred_annualized_carry"].diff(21)
        g["liquid_deferred_annualized_carry_z_252d"] = _rolling_z(g["liquid_deferred_annualized_carry"])
        g["liquid_deferred_backwardation_steepness_chg_21d"] = (
            g["liquid_deferred_backwardation_steepness"].diff(21)
        )
        g["liquid_deferred_backwardation_steepness_z_252d"] = _rolling_z(
            g["liquid_deferred_backwardation_steepness"]
        )

        activity_deferred_settles = _load_contract_settles(
            symbol_dir=commodity_dir / symbol,
            contracts=g["activity_deferred_contract"],
            contract_column="activity_deferred_contract",
            settle_column="activity_deferred_settle",
        )
        if activity_deferred_settles.empty:
            g["activity_deferred_settle"] = np.nan
        else:
            g = g.merge(activity_deferred_settles, on=["date", "activity_deferred_contract"], how="left")

        g["activity_deferred_log_ret_1d"] = _same_contract_log_return(
            g["activity_deferred_settle"],
            g["activity_deferred_contract"],
            periods=1,
        )
        g["activity_deferred_log_ret_5d"] = _same_contract_log_return(
            g["activity_deferred_settle"],
            g["activity_deferred_contract"],
            periods=5,
        )
        g["activity_deferred_log_ret_21d"] = _same_contract_log_return(
            g["activity_deferred_settle"],
            g["activity_deferred_contract"],
            periods=21,
        )
        g["activity_deferred_annualized_carry"] = (
            _safe_log_ratio(g["activity_deferred_settle"], g["front_settle"])
            / _year_fraction_between_contracts(g["M0_con"], g["activity_deferred_contract"])
        )
        g["activity_deferred_backwardation_steepness"] = -g["activity_deferred_annualized_carry"]
        g["activity_deferred_annualized_carry_chg_21d"] = g["activity_deferred_annualized_carry"].diff(21)
        g["activity_deferred_annualized_carry_z_252d"] = _rolling_z(g["activity_deferred_annualized_carry"])
        g["activity_deferred_backwardation_steepness_chg_21d"] = (
            g["activity_deferred_backwardation_steepness"].diff(21)
        )
        g["activity_deferred_backwardation_steepness_z_252d"] = _rolling_z(
            g["activity_deferred_backwardation_steepness"]
        )
        frames.append(g)

    if not frames:
        return signals
    return pd.concat(frames, ignore_index=True).sort_values(["date", "symbol"]).reset_index(drop=True)


def add_calendar_december_carry_features(signals: pd.DataFrame, commodity_dir: Path) -> pd.DataFrame:
    return add_calendar_contract_features(signals=signals, commodity_dir=commodity_dir)


def build_commodity_signal_frame(carry: pd.DataFrame, commodity_dir: Path | None = None) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []

    for symbol, group in carry.groupby("symbol", sort=True):
        g = group.sort_values("date").copy()
        front = g["M0_settle"]
        second = g["M1_settle"]
        third = g["M2_settle"]
        m0_ret = g["m0_ret"] if "m0_ret" in g.columns else front.pct_change()
        m1_ret = g["m1_ret"] if "m1_ret" in g.columns else second.pct_change()
        m2_ret = g["m2_ret"] if "m2_ret" in g.columns else third.pct_change()
        front_log_ret_1d = np.log(front.where(front > 0)).diff()
        is_contango = g["contango"] > g["backwardation"]
        is_backwardation = g["backwardation"] > g["contango"]

        state = np.select(
            [is_contango, is_backwardation],
            [1, -1],
            default=0,
        )

        front_second_log_spread = _safe_log_ratio(front, second)
        front_third_log_spread = _safe_log_ratio(front, third)
        front_second_annualized_carry = _annualized_log_spread(front, second, g["M0_con"], g["M1_con"])
        front_third_annualized_carry = _annualized_log_spread(front, third, g["M0_con"], g["M2_con"])
        front_second_backwardation_steepness = -front_second_annualized_carry
        front_third_backwardation_steepness = -front_third_annualized_carry

        dec_is_m1 = g["M1_con"].astype("string").str.upper().str.endswith("Z")
        dec_is_m2 = g["M2_con"].astype("string").str.upper().str.endswith("Z")
        dec_price = second.where(dec_is_m1, third.where(dec_is_m2))
        dec_contract = g["M1_con"].where(dec_is_m1, g["M2_con"].where(dec_is_m2))
        front_dec_annualized_carry = _annualized_log_spread(front, dec_price, g["M0_con"], dec_contract)
        front_dec_backwardation_steepness = -front_dec_annualized_carry

        realized_vol_20d = m0_ret.rolling(20, min_periods=10).std() * np.sqrt(252)
        realized_vol_63d = m0_ret.rolling(63, min_periods=21).std() * np.sqrt(252)
        abs_ret = m0_ret.abs()
        volume_surge_63d = (
            g["total_volume"] / g["total_volume"].rolling(63, min_periods=21).median() - 1.0
        )
        oi_surge_63d = g["total_oi"] / g["total_oi"].rolling(63, min_periods=21).median() - 1.0

        out = pd.DataFrame(
            {
                "date": g["date"],
                "arrival": g["arrival"],
                "symbol": symbol,
                "front_settle": front,
                "M0_con": g["M0_con"],
                "M1_con": g["M1_con"],
                "M2_con": g["M2_con"],
                "m0_ret_1d": m0_ret,
                "m1_ret_1d": m1_ret,
                "m2_ret_1d": m2_ret,
                "front_log_ret_1d": front_log_ret_1d,
                "ret_5d": front.pct_change(5),
                "ret_21d": front.pct_change(21),
                "ret_42d": front.pct_change(42),
                "ret_63d": front.pct_change(63),
                "front_log_ret_5d": np.log(front.where(front > 0)).diff(5),
                "front_log_ret_21d": np.log(front.where(front > 0)).diff(21),
                "front_log_ret_63d": np.log(front.where(front > 0)).diff(63),
                "ret_accel_21d_vs_63d": front.pct_change(21) - front.pct_change(63) / 3.0,
                "up_days_21d": (m0_ret > 0).rolling(21, min_periods=10).mean(),
                "drawdown_63d": front / front.rolling(63, min_periods=21).max() - 1.0,
                "breakout_252d": front / front.rolling(252, min_periods=63).max() - 1.0,
                "front_second_spread": front / second - 1.0,
                "front_third_spread": front / third - 1.0,
                "front_second_log_spread": front_second_log_spread,
                "front_third_log_spread": front_third_log_spread,
                "front_second_annualized_carry": front_second_annualized_carry,
                "front_third_annualized_carry": front_third_annualized_carry,
                "front_dec_annualized_carry": front_dec_annualized_carry,
                "front_second_backwardation_steepness": front_second_backwardation_steepness,
                "front_third_backwardation_steepness": front_third_backwardation_steepness,
                "front_dec_backwardation_steepness": front_dec_backwardation_steepness,
                "carry": g["carry"],
                "carry_360_perc": g.get("carry_360_perc"),
                "term_structure_state": state,
                "is_contango": is_contango.astype(int),
                "is_backwardation": is_backwardation.astype(int),
                "backwardation_minus_contango": g["backwardation"] - g["contango"],
                "days_in_contango": _consecutive_days(is_contango),
                "days_in_backwardation": _consecutive_days(is_backwardation),
                "realized_vol_20d": realized_vol_20d,
                "realized_vol_63d": realized_vol_63d,
                "vol_chg_20d": realized_vol_20d / realized_vol_20d.shift(20) - 1.0,
                "abs_ret_1d": abs_ret,
                "abs_ret_z_252d": _rolling_z(abs_ret),
                "large_move_2sigma": (
                    abs_ret > 2.0 * m0_ret.rolling(63, min_periods=21).std()
                ).astype(int),
                "total_volume": g["total_volume"],
                "total_oi": g["total_oi"],
                "volume_surge_63d": volume_surge_63d,
                "volume_z_252d": _rolling_z(g["total_volume"]),
                "oi_surge_63d": oi_surge_63d,
                "oi_z_252d": _rolling_z(g["total_oi"]),
            }
        )

        out["front_second_spread_chg_21d"] = out["front_second_spread"].diff(21)
        out["front_third_spread_chg_21d"] = out["front_third_spread"].diff(21)
        out["front_second_annualized_carry_chg_21d"] = out["front_second_annualized_carry"].diff(21)
        out["front_third_annualized_carry_chg_21d"] = out["front_third_annualized_carry"].diff(21)
        out["front_dec_annualized_carry_chg_21d"] = out["front_dec_annualized_carry"].diff(21)
        out["front_second_backwardation_steepness_chg_21d"] = out[
            "front_second_backwardation_steepness"
        ].diff(21)
        out["front_third_backwardation_steepness_chg_21d"] = out[
            "front_third_backwardation_steepness"
        ].diff(21)
        out["front_dec_backwardation_steepness_chg_21d"] = out["front_dec_backwardation_steepness"].diff(21)
        out["term_structure_regime_change"] = out["term_structure_state"].diff().fillna(0)
        out["backwardation_regime_change"] = out["is_backwardation"].diff().fillna(0)
        out["volume_shock_63d"] = out["volume_surge_63d"]
        out["oi_shock_63d"] = out["oi_surge_63d"]
        out["carry_chg_5d"] = out["carry"].diff(5)
        out["carry_chg_21d"] = out["carry"].diff(21)
        out["carry_z_252d"] = _rolling_z(out["carry"])
        out["carry_pctile_252d"] = _rolling_pctile(out["carry"])
        out["front_second_spread_z_252d"] = _rolling_z(out["front_second_spread"])
        out["front_third_spread_z_252d"] = _rolling_z(out["front_third_spread"])
        out["front_second_annualized_carry_z_252d"] = _rolling_z(out["front_second_annualized_carry"])
        out["front_third_annualized_carry_z_252d"] = _rolling_z(out["front_third_annualized_carry"])
        out["front_dec_annualized_carry_z_252d"] = _rolling_z(out["front_dec_annualized_carry"])
        out["front_second_backwardation_steepness_z_252d"] = _rolling_z(
            out["front_second_backwardation_steepness"]
        )
        out["front_third_backwardation_steepness_z_252d"] = _rolling_z(
            out["front_third_backwardation_steepness"]
        )
        out["front_dec_backwardation_steepness_z_252d"] = _rolling_z(
            out["front_dec_backwardation_steepness"]
        )
        out["ret_21d_z_252d"] = _rolling_z(out["ret_21d"])
        out["ret_63d_z_252d"] = _rolling_z(out["ret_63d"])
        out["realized_vol_20d_z_252d"] = _rolling_z(out["realized_vol_20d"])
        out["price_volume_confirm_21d"] = out["ret_21d_z_252d"] * out["volume_z_252d"]
        out["price_oi_confirm_21d"] = out["ret_21d_z_252d"] * out["oi_z_252d"]
        if "M0_atr_14" in g.columns:
            out["m0_atr_14_pct"] = g["M0_atr_14"] / front
            out["m0_atr_14_pct_z_252d"] = _rolling_z(out["m0_atr_14_pct"])

        frames.append(out)

    signals = pd.concat(frames, ignore_index=True)
    if commodity_dir is not None:
        signals = add_calendar_contract_features(signals, commodity_dir=commodity_dir)
    return signals.sort_values(["date", "symbol"]).reset_index(drop=True)


def write_frame(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix == ".parquet":
        df.to_parquet(output_path, index=False)
    elif output_path.suffix == ".csv":
        df.to_csv(output_path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")
