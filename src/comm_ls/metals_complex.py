from __future__ import annotations

from functools import reduce
from pathlib import Path

import numpy as np
import pandas as pd

from comm_ls.commodity import FUTURES_MONTH_CODES, _load_contract_market_data


METALS = ("GC", "SI", "HG")
PAIR_SPECS = (
    ("gc_hg", "GC", "HG"),
    ("si_gc", "SI", "GC"),
    ("si_hg", "SI", "HG"),
)

SOURCE_COLUMNS = (
    "front_settle",
    "m0_ret_1d",
    "M0_con",
    "liquid_deferred_annualized_carry",
    "liquid_deferred_contract",
    "activity_deferred_annualized_carry",
    "activity_deferred_contract",
)

MATCHED_HG_GC_MONTH_MAP = {
    "H": "M",
    "K": "Q",
    "U": "V",
    "Z": "Z",
}
MATCHED_HG_GC_FEATURES = (
    "hg_gc_matched_ratio_ma_gap_3d_50d_raw",
    "hg_gc_matched_ratio_ma_gap_3d_50d_chained",
)


def _contract_frame(market: pd.DataFrame, contract: str) -> pd.DataFrame:
    frame = market.loc[market["contract"].eq(contract), [
        "date",
        "settle",
        "open_interest",
    ]].copy()
    if frame.empty:
        return frame.set_index("date")
    frame = frame.sort_values("date").drop_duplicates("date", keep="last").set_index("date")
    settle = pd.to_numeric(frame["settle"], errors="coerce")
    frame["contract_log_return"] = np.log(settle.where(settle > 0)).diff()
    return frame


def _available_contract_years(market: pd.DataFrame) -> list[int]:
    years = pd.to_numeric(
        market["contract"].astype("string").str.extract(r"^(\d{4})", expand=False),
        errors="coerce",
    )
    return sorted(years.dropna().astype(int).unique().tolist())


def build_matched_hg_gc_signals(
    commodity_dir: Path,
    month_list: str | tuple[str, ...] = "HKUZ",
    roll_anchor: str = "joint",
    start_year: int = 2010,
    end_year: int | None = None,
    liquidity_window: int = 3,
    liquidity_lag: int = 1,
) -> pd.DataFrame:
    """Build notebook-compatible and roll-safe matched HG/GC ratio features.

    Historical contract rows are preferred by ``_load_contract_market_data``;
    live rows fill only missing ``(date, contract)`` observations. That loader
    also normalizes live HG dollars/lb to the historical cents/lb convention.
    """
    months = tuple(str(month).upper() for month in month_list)
    invalid_months = sorted(set(months).difference(MATCHED_HG_GC_MONTH_MAP))
    if invalid_months:
        raise ValueError(
            f"Unsupported HG months: {invalid_months}. "
            f"Supported months are {sorted(MATCHED_HG_GC_MONTH_MAP)}."
        )
    if roll_anchor not in {"joint", "SI", "HG"}:
        raise ValueError("roll_anchor must be 'joint', 'SI', or 'HG'")
    if liquidity_window < 1 or liquidity_lag < 0:
        raise ValueError("liquidity_window must be positive and liquidity_lag non-negative")

    market = {
        symbol: _load_contract_market_data(commodity_dir / symbol)
        for symbol in METALS
    }
    missing_symbols = [symbol for symbol, frame in market.items() if frame.empty]
    if missing_symbols:
        raise ValueError(f"No contract market data found for: {missing_symbols}")

    common_years = set(_available_contract_years(market["HG"]))
    common_years &= set(_available_contract_years(market["SI"]))
    if end_year is None:
        end_year = max(common_years)
    years = [year for year in sorted(common_years) if start_year <= year <= end_year]
    month_order = {code: month for code, month in FUTURES_MONTH_CODES.items()}

    contract_pairs: list[dict[str, object]] = []
    for year in years:
        for hg_month in months:
            gc_month = MATCHED_HG_GC_MONTH_MAP[hg_month]
            contracts = {
                "GC": f"{year}{gc_month}",
                "SI": f"{year}{hg_month}",
                "HG": f"{year}{hg_month}",
            }
            frames = {
                symbol: _contract_frame(market[symbol], contract)
                for symbol, contract in contracts.items()
            }
            if any(frame.empty for frame in frames.values()):
                continue

            si_liquidity = (
                frames["SI"]["open_interest"]
                .rolling(liquidity_window, min_periods=1)
                .mean()
                .shift(liquidity_lag)
            )
            hg_liquidity = (
                frames["HG"]["open_interest"]
                .rolling(liquidity_window, min_periods=1)
                .mean()
                .shift(liquidity_lag)
            )
            if roll_anchor == "SI":
                liquidity = si_liquidity
            elif roll_anchor == "HG":
                liquidity = hg_liquidity
            else:
                aligned = pd.concat({"SI": si_liquidity, "HG": hg_liquidity}, axis=1)
                liquidity = np.sqrt(
                    aligned["SI"].clip(lower=0) * aligned["HG"].clip(lower=0)
                )

            contract_pairs.append(
                {
                    "sort_key": (year, month_order[hg_month]),
                    "contracts": contracts,
                    "frames": frames,
                    "liquidity": liquidity,
                }
            )

    if not contract_pairs:
        raise ValueError("No complete matched GC/SI/HG contract pairs were found")
    contract_pairs.sort(key=lambda pair: pair["sort_key"])

    all_dates = pd.DatetimeIndex([])
    for pair in contract_pairs:
        frames = pair["frames"]
        all_dates = all_dates.union(frames["HG"].index).union(frames["SI"].index)
    all_dates = all_dates.sort_values()

    def value(series: pd.Series, date: pd.Timestamp) -> float:
        result = series.get(date, np.nan)
        return float(result) if pd.notna(result) else np.nan

    rows: list[dict[str, object]] = []
    active_pair = 0
    for date in all_dates:
        while active_pair + 1 < len(contract_pairs):
            current_score = value(contract_pairs[active_pair]["liquidity"], date)
            next_score = value(contract_pairs[active_pair + 1]["liquidity"], date)
            if not (
                np.isfinite(next_score)
                and (not np.isfinite(current_score) or next_score > current_score)
            ):
                break
            active_pair += 1

        pair = contract_pairs[active_pair]
        frames = pair["frames"]
        settles = {
            symbol: value(frames[symbol]["settle"], date)
            for symbol in METALS
        }
        if not all(np.isfinite(list(settles.values()))):
            continue

        contracts = pair["contracts"]
        rows.append(
            {
                "date": date,
                "hg_gc_matched_gc_contract": contracts["GC"],
                "hg_gc_matched_si_contract": contracts["SI"],
                "hg_gc_matched_hg_contract": contracts["HG"],
                "hg_gc_matched_roll_liquidity": value(pair["liquidity"], date),
                "hg_gc_matched_gc_settle": settles["GC"],
                "hg_gc_matched_si_settle": settles["SI"],
                "hg_gc_matched_hg_settle": settles["HG"],
                "hg_gc_matched_gc_log_return": value(
                    frames["GC"]["contract_log_return"], date
                ),
                "hg_gc_matched_hg_log_return": value(
                    frames["HG"]["contract_log_return"], date
                ),
            }
        )

    if not rows:
        raise ValueError("No overlapping matched GC/SI/HG observations were found")

    output = pd.DataFrame(rows).sort_values("date").drop_duplicates("date", keep="last")
    raw_ratio = output["hg_gc_matched_hg_settle"] / output["hg_gc_matched_gc_settle"]
    output["hg_gc_matched_ratio_raw"] = raw_ratio
    output["hg_gc_matched_ratio_ma_gap_3d_50d_raw"] = np.log(
        raw_ratio.rolling(3, min_periods=1).mean()
        / raw_ratio.rolling(50, min_periods=25).mean()
    )

    relative_log_return = (
        output["hg_gc_matched_hg_log_return"]
        - output["hg_gc_matched_gc_log_return"]
    )
    valid_count = relative_log_return.notna().cumsum()
    relative_log_index = relative_log_return.fillna(0.0).cumsum().where(valid_count > 0)
    chained_ratio = np.exp(relative_log_index)
    output["hg_gc_matched_relative_log_return_1d"] = relative_log_return
    output["hg_gc_matched_ratio_index_chained"] = chained_ratio
    output["hg_gc_matched_ratio_ma_gap_3d_50d_chained"] = np.log(
        chained_ratio.rolling(3, min_periods=1).mean()
        / chained_ratio.rolling(50, min_periods=25).mean()
    )
    return output.reset_index(drop=True)


def _prepare_symbol(signals: pd.DataFrame, symbol: str) -> pd.DataFrame:
    available = [column for column in SOURCE_COLUMNS if column in signals.columns]
    frame = signals.loc[signals["symbol"].eq(symbol), ["date", "arrival", *available]].copy()
    if frame.empty:
        raise ValueError(f"No commodity signals found for {symbol}")

    frame["date"] = pd.to_datetime(frame["date"], utc=False)
    frame["arrival"] = pd.to_datetime(frame["arrival"], utc=False)
    frame = frame.sort_values(["date", "arrival"]).drop_duplicates("date", keep="last")
    prefix = symbol.lower()
    return frame.rename(
        columns={column: f"{prefix}__{column}" for column in frame.columns if column != "date"}
    )


def _safe_log_ratio(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    numerator = pd.to_numeric(numerator, errors="coerce")
    denominator = pd.to_numeric(denominator, errors="coerce")
    return np.log(numerator.where(numerator > 0)) - np.log(denominator.where(denominator > 0))


def _safe_log_return(value: pd.Series) -> pd.Series:
    value = pd.to_numeric(value, errors="coerce")
    return np.log1p(value.where(value > -1.0))


def _same_contract_change(
    value: pd.Series,
    contracts: list[pd.Series],
    periods: int,
) -> pd.Series:
    stable = pd.Series(True, index=value.index)
    for contract in contracts:
        stable &= contract.astype("string").eq(contract.astype("string").shift(periods))
    return value.diff(periods).where(stable)


def build_metals_complex_signals(
    commodity_signals: pd.DataFrame,
    commodity_dir: Path | None = None,
) -> pd.DataFrame:
    required = {"date", "arrival", "symbol"}
    missing = sorted(required.difference(commodity_signals.columns))
    if missing:
        raise ValueError(f"Commodity signals are missing required columns: {missing}")

    signals = commodity_signals.copy()
    signals["symbol"] = signals["symbol"].astype(str).str.upper().str.strip()
    frames = [_prepare_symbol(signals, symbol) for symbol in METALS]
    joined = reduce(lambda left, right: left.merge(right, on="date", how="outer"), frames)
    joined = joined.sort_values("date").reset_index(drop=True)

    arrival_columns = [f"{symbol.lower()}__arrival" for symbol in METALS]
    arrival = joined[arrival_columns].max(axis=1)
    output = pd.DataFrame({"date": joined["date"], "arrival": arrival, "symbol": "METALS"})

    for label, numerator, denominator in PAIR_SPECS:
        num = numerator.lower()
        den = denominator.lower()
        num_front = joined[f"{num}__front_settle"]
        den_front = joined[f"{den}__front_settle"]

        # Keep the direct ratio only as an audit diagnostic. Its changes can
        # contain asynchronous front-contract roll jumps.
        raw_ratio = _safe_log_ratio(num_front, den_front)
        output[f"{label}_front_log_ratio_raw"] = raw_ratio
        output[f"{label}_front_log_ratio_raw_chg_21d"] = raw_ratio.diff(21)

        # The relative index compounds source-provided M0 returns, avoiding
        # direct comparison of differently rolling front-contract price levels.
        relative_return = _safe_log_return(joined[f"{num}__m0_ret_1d"]) - _safe_log_return(
            joined[f"{den}__m0_ret_1d"]
        )
        valid_count = relative_return.notna().cumsum()
        relative_index = relative_return.fillna(0.0).cumsum().where(valid_count > 0)
        output[f"{label}_relative_log_return_1d"] = relative_return
        output[f"{label}_relative_log_price_index"] = relative_index
        output[f"{label}_relative_log_momentum_21d"] = relative_return.rolling(
            21, min_periods=21
        ).sum()
        output[f"{label}_relative_log_momentum_63d"] = relative_return.rolling(
            63, min_periods=63
        ).sum()
        output[f"{label}_relative_log_accel_21d_vs_63d"] = (
            output[f"{label}_relative_log_momentum_21d"]
            - output[f"{label}_relative_log_momentum_63d"] / 3.0
        )

        for carry_kind in ("liquid_deferred", "activity_deferred"):
            num_carry = joined[f"{num}__{carry_kind}_annualized_carry"]
            den_carry = joined[f"{den}__{carry_kind}_annualized_carry"]
            spread = pd.to_numeric(num_carry, errors="coerce") - pd.to_numeric(
                den_carry, errors="coerce"
            )
            feature = f"{label}_{carry_kind}_carry_spread"
            output[feature] = spread

            num_contracts = [joined[f"{num}__M0_con"], joined[f"{num}__{carry_kind}_contract"]]
            den_contracts = [joined[f"{den}__M0_con"], joined[f"{den}__{carry_kind}_contract"]]
            output[f"{feature}_same_contract_chg_21d"] = _same_contract_change(
                spread,
                [*num_contracts, *den_contracts],
                periods=21,
            )

        for source_column in (
            "M0_con",
            "liquid_deferred_contract",
            "activity_deferred_contract",
        ):
            output[f"{num}_{source_column}"] = joined[f"{num}__{source_column}"]
            output[f"{den}_{source_column}"] = joined[f"{den}__{source_column}"]

    output = output.loc[:, ~output.columns.duplicated()].copy()
    if commodity_dir is not None:
        matched = build_matched_hg_gc_signals(commodity_dir=commodity_dir)
        output = output.merge(matched, on="date", how="outer")
        output["symbol"] = output["symbol"].fillna("METALS")
        output = output.sort_values("date").reset_index(drop=True)

        # Contract rows do not carry publication timestamps. Reuse the latest
        # arrival across the three underlying commodity signal rows for that
        # settlement date, including live carry rows.
        arrival_by_date = (
            signals.loc[signals["symbol"].isin(METALS), ["date", "arrival"]]
            .groupby("date", as_index=False)["arrival"]
            .max()
            .rename(columns={"arrival": "matched_arrival"})
        )
        output = output.merge(arrival_by_date, on="date", how="left")
        output["arrival"] = output["arrival"].fillna(output["matched_arrival"])
        output = output.drop(columns="matched_arrival")
    return output.sort_values("date").reset_index(drop=True)


def build_metals_complex_signals_from_paths(
    input_path: Path,
    output_path: Path,
    commodity_dir: Path = Path("data/comm"),
) -> pd.DataFrame:
    signals = pd.read_parquet(input_path) if input_path.suffix == ".parquet" else pd.read_csv(input_path)
    output = build_metals_complex_signals(signals, commodity_dir=commodity_dir)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix == ".parquet":
        output.to_parquet(output_path, index=False)
    elif output_path.suffix == ".csv":
        output.to_csv(output_path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")
    return output
