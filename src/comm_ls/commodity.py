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
    # Henry Hub natural gas trades every listed month; interpretation is seasonal.
    "NG": ALL_CONTRACT_MONTHS,
    # Precious metals concentrate liquidity in even months.
    "GC": (2, 4, 6, 8, 10, 12),
    # SI/HG concentrate liquidity in odd months, but November is thin and December is active.
    "SI": (1, 3, 5, 7, 9, 12),
    "HG": (1, 3, 5, 7, 9, 12),
    # GFEX (Guangzhou Futures Exchange) — all 12 months trade.
    "LC": ALL_CONTRACT_MONTHS,
    "IS": ALL_CONTRACT_MONTHS,
    "PS": ALL_CONTRACT_MONTHS,
    "PD": ALL_CONTRACT_MONTHS,
    "PT": ALL_CONTRACT_MONTHS,
}
LIQUID_DEFERRED_MIN_MONTHS = 6
NG_SUMMER_MONTHS = (4, 5, 6, 7, 8, 9, 10)
NG_WINTER_MONTHS = (11, 12, 1, 2, 3)
NG_MIN_STRIP_MONTHS = 3


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


def _normalize_contract_market_data(
    df: pd.DataFrame,
    contract: str | None = None,
    source_priority: int = 0,
) -> pd.DataFrame:
    required = {"date", "px_settle", "px_last"}
    if required.difference(df.columns):
        return pd.DataFrame(columns=["date", "contract", "settle", "volume", "open_interest", "source_priority"])

    out = df.copy()
    out["date"] = pd.to_datetime(out["date"], utc=False)
    if contract is None:
        if "contract" not in out.columns:
            return pd.DataFrame(columns=["date", "contract", "settle", "volume", "open_interest", "source_priority"])
        out["contract"] = out["contract"].astype("string").str.strip().str.upper()
    else:
        out["contract"] = contract.upper()

    settle = pd.to_numeric(out["px_settle"], errors="coerce")
    last = pd.to_numeric(out["px_last"], errors="coerce")
    out["settle"] = settle.fillna(last)
    out["volume"] = pd.to_numeric(out["volume"], errors="coerce") if "volume" in out.columns else np.nan
    out["open_interest"] = pd.to_numeric(out["open int"], errors="coerce") if "open int" in out.columns else np.nan
    out["source_priority"] = source_priority
    return out[["date", "contract", "settle", "volume", "open_interest", "source_priority"]]


def _live_contract_market_data_path(symbol_dir: Path) -> Path:
    return symbol_dir.parent / "live_data" / f"{symbol_dir.name.upper()}.csv"


def _prefer_historical_contract_rows(market: pd.DataFrame) -> pd.DataFrame:
    if market.empty:
        return market
    out = market.copy()
    out["_settle_missing"] = pd.to_numeric(out["settle"], errors="coerce").isna()
    out = out.sort_values(["date", "contract", "_settle_missing", "source_priority"])
    return out.drop_duplicates(["date", "contract"], keep="first").drop(columns=["_settle_missing"])


def _load_contract_market_data(symbol_dir: Path) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for path in sorted(symbol_dir.glob("*.csv")):
        contract = path.stem.upper()
        df = pd.read_csv(path)
        normalized = _normalize_contract_market_data(df, contract=contract, source_priority=0)
        if not normalized.empty:
            frames.append(normalized)

    live_path = _live_contract_market_data_path(symbol_dir)
    if live_path.exists():
        normalized = _normalize_contract_market_data(pd.read_csv(live_path), source_priority=1)
        if not normalized.empty:
            frames.append(normalized)

    if not frames:
        return pd.DataFrame(columns=["date", "contract", "settle", "volume", "open_interest"])
    out = _prefer_historical_contract_rows(pd.concat(frames, ignore_index=True))
    out["contract_month"] = _contract_month_start(out["contract"])
    return out.drop(columns=["source_priority"]).dropna(subset=["date", "contract_month"]).reset_index(drop=True)


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


def _front_price_high_regime_features(
    front: pd.Series,
    threshold_window: int = 756,
    threshold_min_periods: int = 252,
) -> dict[str, pd.Series]:
    features: dict[str, pd.Series] = {}
    front_value = pd.to_numeric(front, errors="coerce")
    safe_front = front_value.where(front_value > 0)

    for quantile, label in [(0.80, "q80"), (0.90, "q90")]:
        threshold = safe_front.shift(1).rolling(
            threshold_window,
            min_periods=threshold_min_periods,
        ).quantile(quantile)
        valid_threshold = threshold.notna() & safe_front.notna()
        is_high = safe_front.gt(threshold).where(valid_threshold)
        high_indicator = is_high.astype(float)
        for window, min_periods in [(63, 21), (100, 30), (126, 42)]:
            features[f"front_price_high_share_{window}d_{label}_3y"] = (
                high_indicator.rolling(window, min_periods=min_periods).mean()
            )
        features[f"front_price_high_days_100d_{label}_3y"] = (
            high_indicator.rolling(100, min_periods=30).sum()
        )
        excess = np.log(safe_front / threshold).where(is_high.fillna(False), 0.0).where(valid_threshold)
        features[f"front_price_high_excess_100d_{label}_3y"] = (
            excess.rolling(100, min_periods=30).mean()
        )
        features[f"front_price_high_consecutive_days_{label}_3y"] = (
            _consecutive_days(is_high).where(valid_threshold)
        )

    return features


def _front_price_low_regime_features(
    front: pd.Series,
    threshold_window: int = 756,
    threshold_min_periods: int = 252,
) -> dict[str, pd.Series]:
    features: dict[str, pd.Series] = {}
    front_value = pd.to_numeric(front, errors="coerce")
    safe_front = front_value.where(front_value > 0)

    for quantile, label in [(0.20, "q20"), (0.10, "q10")]:
        threshold = safe_front.shift(1).rolling(
            threshold_window,
            min_periods=threshold_min_periods,
        ).quantile(quantile)
        valid_threshold = threshold.notna() & safe_front.notna()
        is_low = safe_front.lt(threshold).where(valid_threshold)
        low_indicator = is_low.astype(float)
        for window, min_periods in [(63, 21), (100, 30), (126, 42)]:
            features[f"front_price_low_share_{window}d_{label}_3y"] = (
                low_indicator.rolling(window, min_periods=min_periods).mean()
            )
        features[f"front_price_low_days_100d_{label}_3y"] = (
            low_indicator.rolling(100, min_periods=30).sum()
        )
        shortfall = np.log(threshold / safe_front).where(is_low.fillna(False), 0.0).where(valid_threshold)
        features[f"front_price_low_shortfall_100d_{label}_3y"] = (
            shortfall.rolling(100, min_periods=30).mean()
        )
        features[f"front_price_low_consecutive_days_{label}_3y"] = (
            _consecutive_days(is_low).where(valid_threshold)
        )

    return features


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
        normalized = _normalize_contract_market_data(df, contract=contract, source_priority=0)
        if not normalized.empty:
            frames.append(normalized)

    live_path = _live_contract_market_data_path(symbol_dir)
    if live_path.exists():
        live = _normalize_contract_market_data(pd.read_csv(live_path), source_priority=1)
        keep_contracts = set(contracts.dropna().astype(str).str.upper())
        live = live[live["contract"].isin(keep_contracts)].copy()
        if not live.empty:
            frames.append(live)

    if not frames:
        return pd.DataFrame(columns=["date", contract_column, settle_column])
    out = _prefer_historical_contract_rows(pd.concat(frames, ignore_index=True))
    out = out.rename(columns={"contract": contract_column, "settle": settle_column})
    return out[["date", contract_column, settle_column]]


def _ng_season_contracts_after_front(
    front_contract: pd.Series,
    season_months: tuple[int, ...],
    min_months: int = NG_MIN_STRIP_MONTHS,
) -> tuple[pd.Series, pd.Series]:
    """Return nearest forward NG seasonal strip with enough months after front."""
    front_months = _contract_month_start(front_contract)
    contract_lists: list[str | pd.NA] = []
    midpoint_months: list[pd.Timestamp | pd.NaT] = []

    for front_month in front_months:
        if pd.isna(front_month):
            contract_lists.append(pd.NA)
            midpoint_months.append(pd.NaT)
            continue

        selected: list[tuple[pd.Timestamp, str]] = []
        for year_offset in range(4):
            season_year = front_month.year + year_offset
            candidates: list[tuple[pd.Timestamp, str]] = []
            for month in season_months:
                contract_year = season_year + (1 if month <= 3 and max(season_months) == 12 else 0)
                contract_month = pd.Timestamp(year=contract_year, month=month, day=1)
                if contract_month > front_month:
                    candidates.append((contract_month, _contract_for_year_month(contract_year, month)))
            if len(candidates) >= min_months:
                selected = candidates
                break

        if not selected:
            contract_lists.append(pd.NA)
            midpoint_months.append(pd.NaT)
            continue

        contract_lists.append("|".join(contract for _, contract in selected))
        midpoint_ord = int(round(float(np.mean([month.toordinal() for month, _ in selected]))))
        midpoint_months.append(pd.Timestamp.fromordinal(midpoint_ord))

    return (
        pd.Series(contract_lists, index=front_contract.index, dtype="string"),
        pd.Series(midpoint_months, index=front_contract.index),
    )


def _strip_contract_settles(
    symbol_dir: Path,
    dates: pd.Series,
    contract_lists: pd.Series,
) -> pd.DataFrame:
    unique_contracts = sorted(
        {
            contract
            for text in contract_lists.dropna().astype(str)
            for contract in text.split("|")
            if contract
        }
    )
    if not unique_contracts:
        return pd.DataFrame(
            {
                "strip_settle": np.nan,
                "strip_available_contracts": 0,
            },
            index=contract_lists.index,
        )

    settles = _load_contract_settles(
        symbol_dir=symbol_dir,
        contracts=pd.Series(unique_contracts, dtype="string"),
        contract_column="contract",
        settle_column="settle",
    )
    if settles.empty:
        return pd.DataFrame(
            {
                "strip_settle": np.nan,
                "strip_available_contracts": 0,
            },
            index=contract_lists.index,
        )

    pivot = settles.pivot_table(index="date", columns="contract", values="settle", aggfunc="last")
    values: list[float] = []
    counts: list[int] = []
    for idx, contract_text in contract_lists.items():
        if pd.isna(contract_text):
            values.append(np.nan)
            counts.append(0)
            continue
        date = pd.Timestamp(dates.loc[idx])
        contracts = str(contract_text).split("|")
        if date not in pivot.index:
            values.append(np.nan)
            counts.append(0)
            continue
        row = pd.to_numeric(pivot.loc[date, contracts], errors="coerce")
        counts.append(int(row.notna().sum()))
        values.append(float(row.mean()) if row.notna().sum() >= NG_MIN_STRIP_MONTHS else np.nan)

    return pd.DataFrame(
        {
            "strip_settle": values,
            "strip_available_contracts": counts,
        },
        index=contract_lists.index,
    )


def _year_fraction_to_midpoint(front_contract: pd.Series, midpoint_month: pd.Series) -> pd.Series:
    front_month = _contract_month_start(front_contract)
    days = (pd.to_datetime(midpoint_month, errors="coerce") - front_month).dt.days
    return days.where(days > 0) / 365.25


def _same_month_rolling_z(value: pd.Series, dates: pd.Series, window: int = 105, min_periods: int = 42) -> pd.Series:
    out = pd.Series(np.nan, index=value.index, dtype=float)
    safe_value = pd.to_numeric(value, errors="coerce")
    month = pd.to_datetime(dates, utc=False).dt.month
    for _, idx in month.groupby(month).groups.items():
        s = safe_value.loc[idx]
        mean = s.shift(1).rolling(window, min_periods=min_periods).mean()
        std = s.shift(1).rolling(window, min_periods=min_periods).std()
        out.loc[idx] = (s - mean) / std
    return out


def _same_month_rolling_pctile(
    value: pd.Series,
    dates: pd.Series,
    window: int = 105,
    min_periods: int = 42,
) -> pd.Series:
    out = pd.Series(np.nan, index=value.index, dtype=float)
    safe_value = pd.to_numeric(value, errors="coerce")
    month = pd.to_datetime(dates, utc=False).dt.month
    for _, idx in month.groupby(month).groups.items():
        s = safe_value.loc[idx]
        values = s.to_numpy(dtype=float)
        pctiles = np.full(len(values), np.nan)
        for i, current in enumerate(values):
            if not np.isfinite(current):
                continue
            start = max(0, i - window)
            history = values[start:i]
            history = history[np.isfinite(history)]
            if len(history) < min_periods:
                continue
            pctiles[i] = float(np.mean(history <= current))
        out.loc[idx] = pctiles
    return out


def add_ng_seasonal_features(signals: pd.DataFrame, commodity_dir: Path) -> pd.DataFrame:
    out = signals.copy()
    if out.empty or "symbol" not in out.columns:
        return out

    symbol = out["symbol"].astype(str).str.upper().str.strip()
    if "NG" not in set(symbol):
        return out

    ng = out.loc[symbol.eq("NG")].sort_values("date").copy()
    if ng.empty:
        return out

    for label, season_months in [
        ("summer", NG_SUMMER_MONTHS),
        ("winter", NG_WINTER_MONTHS),
    ]:
        contracts, midpoint = _ng_season_contracts_after_front(ng["M0_con"], season_months=season_months)
        strip = _strip_contract_settles(commodity_dir / "NG", ng["date"], contracts)
        ng[f"ng_forward_{label}_strip_contracts"] = contracts
        ng[f"ng_forward_{label}_strip_midpoint"] = midpoint
        ng[f"ng_forward_{label}_strip_settle"] = strip["strip_settle"]
        ng[f"ng_forward_{label}_strip_available_contracts"] = strip["strip_available_contracts"]
        carry_col = f"ng_forward_{label}_strip_annualized_carry"
        ng[carry_col] = (
            _safe_log_ratio(ng[f"ng_forward_{label}_strip_settle"], ng["front_settle"])
            / _year_fraction_to_midpoint(ng["M0_con"], midpoint)
        )
        ng[f"ng_forward_{label}_strip_backwardation_steepness"] = -ng[carry_col]
        ng[f"{carry_col}_chg_21d"] = ng[carry_col].diff(21)
        ng[f"{carry_col}_z_252d"] = _rolling_z(ng[carry_col])
        steep_col = f"ng_forward_{label}_strip_backwardation_steepness"
        ng[f"{steep_col}_chg_21d"] = ng[steep_col].diff(21)
        ng[f"{steep_col}_z_252d"] = _rolling_z(ng[steep_col])

    ng["ng_winter_summer_strip_log_spread"] = _safe_log_ratio(
        ng["ng_forward_winter_strip_settle"],
        ng["ng_forward_summer_strip_settle"],
    )
    ng["ng_winter_summer_strip_spread"] = (
        ng["ng_forward_winter_strip_settle"] / ng["ng_forward_summer_strip_settle"] - 1.0
    )
    ng["ng_winter_summer_strip_log_spread_chg_21d"] = ng["ng_winter_summer_strip_log_spread"].diff(21)
    ng["ng_winter_summer_strip_log_spread_z_252d"] = _rolling_z(
        ng["ng_winter_summer_strip_log_spread"]
    )
    ng["ng_winter_summer_strip_spread_chg_21d"] = ng["ng_winter_summer_strip_spread"].diff(21)
    ng["ng_winter_summer_strip_spread_z_252d"] = _rolling_z(ng["ng_winter_summer_strip_spread"])
    ng["ng_injection_season"] = ng["date"].dt.month.isin(NG_SUMMER_MONTHS).astype(int)
    ng["ng_withdrawal_season"] = ng["date"].dt.month.isin(NG_WINTER_MONTHS).astype(int)

    log_front = np.log(pd.to_numeric(ng["front_settle"], errors="coerce").where(ng["front_settle"] > 0))
    ng["ng_front_settle_month_z_5y"] = _same_month_rolling_z(log_front, ng["date"])
    ng["ng_front_settle_month_pctile_5y"] = _same_month_rolling_pctile(log_front, ng["date"])

    out.loc[ng.index, ng.columns] = ng
    return out


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

        # The deferred contract series can have sparse gaps during rolls or
        # hand-entered fallback coverage. Forward-fill only for the change
        # feature so the 21d delta remains continuous once the level feature
        # resumes. The raw level feature itself is left untouched.
        liquid_deferred_level_ffill = g["liquid_deferred_annualized_carry"].ffill()
        g["liquid_deferred_annualized_carry_chg_21d"] = liquid_deferred_level_ffill.diff(21)
        g["liquid_deferred_annualized_carry_z_252d"] = _rolling_z(g["liquid_deferred_annualized_carry"])
        g["liquid_deferred_backwardation_steepness_chg_21d"] = (
            (-liquid_deferred_level_ffill).diff(21)
        )
        g["liquid_deferred_backwardation_steepness_z_252d"] = _rolling_z(
            g["liquid_deferred_backwardation_steepness"]
        )

        # ── calendar-anchor carry features (Mar/Jun/Sep vs next-active Dec) ──
        for anchor_code, anchor_month, anchor_label in [
            ("H", 3, "mar"),
            ("M", 6, "jun"),
            ("U", 9, "sep"),
        ]:
            # Anchor contract: same-year if current month < anchor month,
            # otherwise next-year.  (Code matches CME month-letter convention.)
            anchor_year = np.where(
                g["date"].dt.month < anchor_month,
                g["date"].dt.year,
                g["date"].dt.year + 1,
            )
            anchor_contract_col = f"{anchor_label}_anchor_contract"
            anchor_settle_col = f"{anchor_label}_anchor_settle"
            g[anchor_contract_col] = (
                pd.Series(anchor_year, index=g.index).astype(str) + anchor_code
            )

            anchor_settles = _load_contract_settles(
                symbol_dir=commodity_dir / symbol,
                contracts=g[anchor_contract_col],
                contract_column=anchor_contract_col,
                settle_column=anchor_settle_col,
            )
            if anchor_settles.empty:
                g[anchor_settle_col] = np.nan
            else:
                g = g.merge(
                    anchor_settles,
                    on=["date", anchor_contract_col],
                    how="left",
                )

            # The Dec leg must be after the selected anchor. If the anchor has
            # rolled to next year, use next year's Dec as well.
            rolling_dec_year = anchor_year
            rolling_dec_contract_col = f"{anchor_label}_dec_contract"
            rolling_dec_settle_col = f"{anchor_label}_dec_settle"
            g[rolling_dec_contract_col] = (
                pd.Series(rolling_dec_year, index=g.index).astype(str) + "Z"
            )

            rolling_dec_settles = _load_contract_settles(
                symbol_dir=commodity_dir / symbol,
                contracts=g[rolling_dec_contract_col],
                contract_column=rolling_dec_contract_col,
                settle_column=rolling_dec_settle_col,
            )
            if rolling_dec_settles.empty:
                g[rolling_dec_settle_col] = np.nan
            else:
                g = g.merge(
                    rolling_dec_settles,
                    on=["date", rolling_dec_contract_col],
                    how="left",
                )

            carry_col = f"{anchor_label}_dec_annualized_carry"
            year_frac = _year_fraction_between_contracts(
                g[anchor_contract_col], g[rolling_dec_contract_col]
            )
            g[carry_col] = (
                _safe_log_ratio(g[rolling_dec_settle_col], g[anchor_settle_col])
                / year_frac
            )
            g[f"{anchor_label}_dec_backwardation_steepness"] = -g[carry_col]
            g[f"{anchor_label}_dec_annualized_carry_chg_21d"] = g[carry_col].diff(21)
            g[f"{anchor_label}_dec_annualized_carry_z_252d"] = _rolling_z(g[carry_col])
            g[f"{anchor_label}_dec_backwardation_steepness_chg_21d"] = (
                g[f"{anchor_label}_dec_backwardation_steepness"].diff(21)
            )
            g[f"{anchor_label}_dec_backwardation_steepness_z_252d"] = _rolling_z(
                g[f"{anchor_label}_dec_backwardation_steepness"]
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


def add_brent_wti_spread_features(
    signals: pd.DataFrame,
    base_symbol: str = "CL",
    brent_symbol: str = "CO",
) -> pd.DataFrame:
    """Attach Brent-WTI companion features to the base WTI symbol rows.

    The sign convention is always Brent minus WTI (`CO - CL`) for spreads and
    return divergence. The resulting columns are populated only on `base_symbol`
    rows so downstream CL feature-return caches can consume them normally.
    """
    out = signals.copy()
    if out.empty or "symbol" not in out.columns:
        return out

    symbol = out["symbol"].astype(str).str.upper().str.strip()
    base_symbol = base_symbol.upper().strip()
    brent_symbol = brent_symbol.upper().strip()
    if base_symbol not in set(symbol) or brent_symbol not in set(symbol):
        return out

    required = {
        "date",
        "front_settle",
        "front_log_ret_1d",
        "front_log_ret_5d",
        "front_log_ret_21d",
        "carry",
        "front_second_annualized_carry",
        "front_third_annualized_carry",
    }
    if required.difference(out.columns):
        return out

    optional = [
        "calendar_dec_annualized_carry",
        "liquid_deferred_annualized_carry",
        "activity_deferred_annualized_carry",
    ]
    value_cols = sorted(required.difference({"date"})) + [col for col in optional if col in out.columns]

    pair = (
        out.loc[symbol.isin({base_symbol, brent_symbol}), ["date", "symbol", *value_cols]]
        .copy()
        .sort_values(["symbol", "date"])
    )
    pair["date"] = pd.to_datetime(pair["date"], utc=False)
    base = pair[pair["symbol"] == base_symbol].drop(columns=["symbol"]).add_prefix("wti_")
    brent = pair[pair["symbol"] == brent_symbol].drop(columns=["symbol"]).add_prefix("brent_")
    joined = base.merge(brent, left_on="wti_date", right_on="brent_date", how="inner")
    if joined.empty:
        return out

    features = pd.DataFrame({"date": joined["wti_date"]})
    features["brent_wti_log_spread"] = _safe_log_ratio(
        joined["brent_front_settle"],
        joined["wti_front_settle"],
    )
    features["brent_wti_front_price_spread"] = joined["brent_front_settle"] / joined["wti_front_settle"] - 1.0
    features["brent_wti_log_spread_chg_5d"] = features["brent_wti_log_spread"].diff(5)
    features["brent_wti_log_spread_chg_21d"] = features["brent_wti_log_spread"].diff(21)
    features["brent_wti_log_spread_z_252d"] = _rolling_z(features["brent_wti_log_spread"])

    for horizon in [1, 5, 21]:
        features[f"brent_minus_wti_front_log_ret_{horizon}d"] = (
            joined[f"brent_front_log_ret_{horizon}d"] - joined[f"wti_front_log_ret_{horizon}d"]
        )

    carry_spread_specs = {
        "brent_wti_carry_spread": ("brent_carry", "wti_carry"),
        "brent_wti_front_second_annualized_carry_spread": (
            "brent_front_second_annualized_carry",
            "wti_front_second_annualized_carry",
        ),
        "brent_wti_front_third_annualized_carry_spread": (
            "brent_front_third_annualized_carry",
            "wti_front_third_annualized_carry",
        ),
        "brent_wti_calendar_dec_annualized_carry_spread": (
            "brent_calendar_dec_annualized_carry",
            "wti_calendar_dec_annualized_carry",
        ),
        "brent_wti_liquid_deferred_annualized_carry_spread": (
            "brent_liquid_deferred_annualized_carry",
            "wti_liquid_deferred_annualized_carry",
        ),
        "brent_wti_activity_deferred_annualized_carry_spread": (
            "brent_activity_deferred_annualized_carry",
            "wti_activity_deferred_annualized_carry",
        ),
    }
    for feature_name, (brent_col, wti_col) in carry_spread_specs.items():
        if brent_col not in joined.columns or wti_col not in joined.columns:
            continue
        features[feature_name] = joined[brent_col] - joined[wti_col]
        features[f"{feature_name}_chg_21d"] = features[feature_name].diff(21)
        features[f"{feature_name}_z_252d"] = _rolling_z(features[feature_name])

    feature_cols = [col for col in features.columns if col != "date"]
    out = out.merge(features, on="date", how="left", suffixes=("", "__brent_wti"))
    non_base = out["symbol"].astype(str).str.upper().str.strip() != base_symbol
    out.loc[non_base, feature_cols] = np.nan
    return out


def build_commodity_signal_frame(
    carry: pd.DataFrame,
    commodity_dir: Path | None = None,
    include_brent_wti_features: bool = True,
) -> pd.DataFrame:
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
        front_price_high_features = _front_price_high_regime_features(front)
        front_price_low_features = _front_price_low_regime_features(front)

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
                **front_price_high_features,
                **front_price_low_features,
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
        signals = add_ng_seasonal_features(signals, commodity_dir=commodity_dir)
    if include_brent_wti_features:
        signals = add_brent_wti_spread_features(signals)
    return signals.sort_values(["date", "symbol"]).reset_index(drop=True)


def write_frame(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix == ".parquet":
        df.to_parquet(output_path, index=False)
    elif output_path.suffix == ".csv":
        df.to_csv(output_path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")
