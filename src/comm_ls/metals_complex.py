from __future__ import annotations

from functools import reduce
from pathlib import Path

import numpy as np
import pandas as pd


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


def build_metals_complex_signals(commodity_signals: pd.DataFrame) -> pd.DataFrame:
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
    return output.sort_values("date").reset_index(drop=True)


def build_metals_complex_signals_from_paths(input_path: Path, output_path: Path) -> pd.DataFrame:
    signals = pd.read_parquet(input_path) if input_path.suffix == ".parquet" else pd.read_csv(input_path)
    output = build_metals_complex_signals(signals)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix == ".parquet":
        output.to_parquet(output_path, index=False)
    elif output_path.suffix == ".csv":
        output.to_csv(output_path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")
    return output
