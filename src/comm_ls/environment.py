from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from comm_ls.curve_diagnostics import covid_time_regime
from comm_ls.data_access import DEFAULT_COMMODITY_SIGNALS, _read_frame


DEFAULT_ENVIRONMENT_FEATURES = [
    "ret_21d",
    "ret_63d",
    "ret_accel_21d_vs_63d",
    "drawdown_63d",
    "front_second_spread",
    "front_third_spread",
    "front_second_spread_chg_21d",
    "front_third_spread_chg_21d",
    "front_second_backwardation_steepness",
    "front_third_backwardation_steepness",
    "front_second_backwardation_steepness_chg_21d",
    "front_third_backwardation_steepness_chg_21d",
    "carry_pctile_252d",
    "carry_z_252d",
    "realized_vol_20d_z_252d",
    "realized_vol_63d_z_252d",
    "volume_z_252d",
    "oi_z_252d",
    "days_in_contango",
    "days_in_backwardation",
    "backwardation_minus_contango",
]


def _cosine_similarity(left: pd.Series, right: pd.Series) -> float:
    common = left.index.intersection(right.index)
    x = left.loc[common].astype(float)
    y = right.loc[common].astype(float)
    valid = x.notna() & y.notna()
    if valid.sum() < 2:
        return np.nan
    x = x[valid]
    y = y[valid]
    denominator = float(np.linalg.norm(x) * np.linalg.norm(y))
    if denominator == 0:
        return np.nan
    return float(np.dot(x, y) / denominator)


def _euclidean_distance(left: pd.Series, right: pd.Series) -> float:
    common = left.index.intersection(right.index)
    x = left.loc[common].astype(float)
    y = right.loc[common].astype(float)
    valid = x.notna() & y.notna()
    if valid.sum() < 2:
        return np.nan
    return float(np.linalg.norm(x[valid] - y[valid]))


def _load_commodity_signals(path: Path | str, symbol: str, as_of_date: str | None, start: str | None) -> pd.DataFrame:
    df = _read_frame(Path(path))
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"], utc=False)
    if "arrival" in df.columns:
        df["arrival"] = pd.to_datetime(df["arrival"], utc=False)
    else:
        df["arrival"] = df["date"]
    df["symbol"] = df["symbol"].astype(str).str.upper().str.strip()
    out = df[df["symbol"] == symbol.upper().strip()].copy()
    if start is not None:
        out = out[out["date"] >= pd.Timestamp(start)]
    if as_of_date is not None:
        target = pd.Timestamp(as_of_date)
        out = out[out["arrival"] <= target]
    return out.sort_values("date").reset_index(drop=True)


def commodity_environment_similarity(
    symbol: str,
    commodity_signals_path: Path | str = DEFAULT_COMMODITY_SIGNALS,
    as_of_date: str | None = None,
    start: str | None = "2010-01-01",
    current_window_days: int = 63,
    features: list[str] | None = None,
    min_regime_observations: int = 126,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Compare the current commodity feature state with pre/covid/post regimes.

    The comparison is commodity-level, not stock-specific. It standardizes selected
    commodity features on history available up to `as_of_date`, averages the latest
    `current_window_days`, and compares that vector with each time-regime average.
    """

    signals = _load_commodity_signals(commodity_signals_path, symbol=symbol, as_of_date=as_of_date, start=start)
    if signals.empty:
        raise KeyError(f"No commodity signals found for {symbol}")

    feature_list = features or DEFAULT_ENVIRONMENT_FEATURES
    feature_list = [feature for feature in feature_list if feature in signals.columns]
    if not feature_list:
        raise KeyError("No requested environment features are present in commodity signals")

    values = signals[["date", "arrival", *feature_list]].copy()
    for feature in feature_list:
        values[feature] = pd.to_numeric(values[feature], errors="coerce")

    z_values = values.copy()
    for feature in feature_list:
        expanding_mean = values[feature].expanding(min_periods=min_regime_observations).mean()
        expanding_std = values[feature].expanding(min_periods=min_regime_observations).std(ddof=0)
        z_values[feature] = (values[feature] - expanding_mean) / expanding_std.replace(0.0, np.nan)
    z_values["time_regime"] = z_values["date"].map(covid_time_regime)

    current = z_values.tail(current_window_days)
    current_vector = current[feature_list].mean()

    rows: list[dict[str, object]] = []
    detail_rows: list[dict[str, object]] = []
    for time_regime, group in z_values.groupby("time_regime", sort=False):
        if len(group) < min_regime_observations:
            continue
        regime_vector = group[feature_list].mean()
        valid = current_vector.notna() & regime_vector.notna()
        rows.append(
            {
                "symbol": symbol.upper().strip(),
                "as_of_date": z_values["arrival"].max(),
                "current_window_days": current_window_days,
                "current_start_date": current["date"].min(),
                "current_end_date": current["date"].max(),
                "time_regime": time_regime,
                "regime_start_date": group["date"].min(),
                "regime_end_date": group["date"].max(),
                "regime_observations": int(len(group)),
                "features_used": int(valid.sum()),
                "cosine_similarity": _cosine_similarity(current_vector, regime_vector),
                "euclidean_distance": _euclidean_distance(current_vector, regime_vector),
            }
        )
        for feature in feature_list:
            detail_rows.append(
                {
                    "symbol": symbol.upper().strip(),
                    "as_of_date": z_values["arrival"].max(),
                    "current_window_days": current_window_days,
                    "time_regime": time_regime,
                    "feature": feature,
                    "current_mean_z": current_vector[feature],
                    "regime_mean_z": regime_vector[feature],
                    "z_gap": current_vector[feature] - regime_vector[feature],
                }
            )

    summary = pd.DataFrame(rows)
    if summary.empty:
        return summary, pd.DataFrame(detail_rows)

    summary = summary.sort_values(
        ["cosine_similarity", "euclidean_distance"],
        ascending=[False, True],
    ).reset_index(drop=True)
    summary["rank"] = np.arange(1, len(summary) + 1)
    summary["closest_regime"] = summary["rank"].eq(1)
    detail = pd.DataFrame(detail_rows)
    return summary, detail


def write_frame(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix == ".parquet":
        df.to_parquet(output_path, index=False)
    elif output_path.suffix == ".csv":
        df.to_csv(output_path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")


def commodity_environment_similarity_from_paths(
    symbol: str,
    commodity_signals_path: Path,
    output_summary_path: Path,
    output_detail_path: Path | None = None,
    as_of_date: str | None = None,
    start: str | None = "2010-01-01",
    current_window_days: int = 63,
    features: list[str] | None = None,
    min_regime_observations: int = 126,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    summary, detail = commodity_environment_similarity(
        symbol=symbol,
        commodity_signals_path=commodity_signals_path,
        as_of_date=as_of_date,
        start=start,
        current_window_days=current_window_days,
        features=features,
        min_regime_observations=min_regime_observations,
    )
    write_frame(summary, output_summary_path)
    if output_detail_path is not None:
        write_frame(detail, output_detail_path)
    return summary, detail
