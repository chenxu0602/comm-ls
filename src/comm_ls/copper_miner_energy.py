from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ENERGY_EXPOSURE_COLUMNS = (
    "ticker",
    "effective_start_date",
    "effective_end_date",
    "known_date",
    "company_type",
    "open_pit_share_bucket",
    "strip_intensity_bucket",
    "diesel_proxy_purity_bucket",
    "include_in_interaction",
    "structural_break",
    "source_reference",
    "confidence",
)

BUCKET_SCORE = {"none": 0, "low": 1, "mixed": 2, "medium": 2, "high": 3}
COMPANY_TYPES = {"operator", "streamer"}
CONFIDENCE_VALUES = {"low", "medium", "high"}


def validate_energy_exposure_registry(frame: pd.DataFrame) -> pd.DataFrame:
    missing = sorted(set(ENERGY_EXPOSURE_COLUMNS).difference(frame.columns))
    if missing:
        raise ValueError(f"energy exposure registry is missing columns: {missing}")

    out = frame.loc[:, ENERGY_EXPOSURE_COLUMNS].copy()
    for column in ("ticker", "company_type", "open_pit_share_bucket",
                   "strip_intensity_bucket", "diesel_proxy_purity_bucket",
                   "include_in_interaction", "confidence"):
        out[column] = out[column].fillna("").astype(str).str.strip().str.lower()
    out["ticker"] = out["ticker"].str.upper()
    for column in ("structural_break", "source_reference"):
        out[column] = out[column].fillna("").astype(str).str.strip()
    for column in ("effective_start_date", "effective_end_date", "known_date"):
        out[column] = pd.to_datetime(out[column], errors="coerce").dt.normalize()

    for column in ("ticker", "company_type", "structural_break", "source_reference"):
        if out[column].eq("").any():
            raise ValueError(f"energy exposure registry requires {column}")
    for column in ("effective_start_date", "known_date"):
        if out[column].isna().any():
            raise ValueError(f"energy exposure registry requires valid {column}")

    invalid_company_type = sorted(set(out["company_type"]).difference(COMPANY_TYPES))
    if invalid_company_type:
        raise ValueError(f"invalid company_type values: {invalid_company_type}")
    for column in ("open_pit_share_bucket", "strip_intensity_bucket", "diesel_proxy_purity_bucket"):
        invalid = sorted(set(out[column]).difference(BUCKET_SCORE))
        if invalid:
            raise ValueError(f"invalid {column} values: {invalid}")
    invalid_confidence = sorted(set(out["confidence"]).difference(CONFIDENCE_VALUES))
    if invalid_confidence:
        raise ValueError(f"invalid confidence values: {invalid_confidence}")
    if not set(out["include_in_interaction"]).issubset({"true", "false"}):
        raise ValueError("include_in_interaction must be true or false")
    out["include_in_interaction"] = out["include_in_interaction"].eq("true")

    invalid_period = out["effective_end_date"].notna() & out["effective_start_date"].gt(
        out["effective_end_date"]
    )
    if invalid_period.any():
        raise ValueError("energy exposure registry has effective_start_date after effective_end_date")

    far_future = pd.Timestamp.max.normalize()
    for ticker, group in out.groupby("ticker", sort=True):
        prior_end: pd.Timestamp | None = None
        for row in group.sort_values(["effective_start_date", "known_date"]).itertuples(index=False):
            end = row.effective_end_date if pd.notna(row.effective_end_date) else far_future
            if prior_end is not None and row.effective_start_date <= prior_end:
                raise ValueError(f"energy exposure registry has overlapping periods for {ticker}")
            prior_end = end

    out["energy_exposure_score"] = sum(
        out[column].map(BUCKET_SCORE).astype(int)
        for column in ("open_pit_share_bucket", "strip_intensity_bucket", "diesel_proxy_purity_bucket")
    )
    out.loc[out["company_type"].eq("streamer"), "energy_exposure_score"] = 0
    return out.sort_values(["ticker", "effective_start_date", "known_date"]).reset_index(drop=True)


def load_energy_exposure_registry(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(path)
    return validate_energy_exposure_registry(pd.read_csv(path, dtype=str))


def attach_point_in_time_exposure(
    observations: pd.DataFrame,
    registry: pd.DataFrame,
) -> pd.DataFrame:
    """Attach the latest profile that was both effective and known on each date."""
    required = {"date", "ticker"}
    if not required.issubset(observations.columns):
        raise ValueError(f"observations require columns: {sorted(required)}")
    profiles = validate_energy_exposure_registry(registry)
    left = observations.copy()
    left["date"] = pd.to_datetime(left["date"], errors="coerce").dt.normalize()
    left["ticker"] = left["ticker"].astype(str).str.upper()

    joined = left.merge(profiles, on="ticker", how="left")
    valid = (
        joined["known_date"].le(joined["date"])
        & joined["effective_start_date"].le(joined["date"])
        & (joined["effective_end_date"].isna() | joined["effective_end_date"].ge(joined["date"]))
    )
    joined = joined.loc[valid].sort_values(["date", "ticker", "known_date"])
    return joined.drop_duplicates(["date", "ticker"], keep="last").reset_index(drop=True)


def _lagged_rolling_beta(
    dependent: pd.Series,
    independent: pd.Series,
    window: int,
    min_periods: int,
) -> pd.Series:
    covariance = dependent.rolling(window, min_periods=min_periods).cov(independent)
    variance = independent.rolling(window, min_periods=min_periods).var()
    return (covariance / variance.where(variance.gt(0))).shift(1)


def _lagged_rolling_z(value: pd.Series, window: int, min_periods: int) -> pd.Series:
    mean = value.rolling(window, min_periods=min_periods).mean().shift(1)
    std = value.rolling(window, min_periods=min_periods).std().shift(1)
    return (value - mean) / std.where(std.gt(0))


def build_energy_signal_frame(
    commodity_signals: pd.DataFrame,
    signal_window: int = 20,
    beta_window: int = 252,
    beta_min_periods: int = 126,
    z_window: int = 252,
    z_min_periods: int = 126,
) -> pd.DataFrame:
    """Build roll-safe CL, HO, HG and RBOB residual momentum states.

    All estimated betas and z-score moments are lagged one session. The current
    session's settlement return is allowed in the signal and therefore the
    signal can only target a later equity session.
    """
    required = {"date", "symbol", "front_log_ret_1d_v2"}
    if not required.issubset(commodity_signals.columns):
        raise ValueError(f"commodity_signals require columns: {sorted(required)}")
    selected_columns = ["date", "symbol", "front_log_ret_1d_v2"]
    if "arrival" in commodity_signals.columns:
        selected_columns.append("arrival")
    selected = commodity_signals.loc[
        commodity_signals["symbol"].astype(str).str.upper().isin(["CL", "HO", "HG", "XB"]),
        selected_columns,
    ].copy()
    selected["date"] = pd.to_datetime(selected["date"], errors="coerce").dt.normalize()
    selected["symbol"] = selected["symbol"].astype(str).str.upper()
    selected["front_log_ret_1d_v2"] = pd.to_numeric(selected["front_log_ret_1d_v2"], errors="coerce")
    returns = selected.pivot_table(
        index="date", columns="symbol", values="front_log_ret_1d_v2", aggfunc="last"
    ).sort_index()
    missing_symbols = sorted({"CL", "HO", "HG", "XB"}.difference(returns.columns))
    if missing_symbols:
        raise ValueError(f"commodity signal frame is missing symbols: {missing_symbols}")

    output = returns.rename(columns={symbol: f"{symbol.lower()}_return_1d" for symbol in returns.columns})
    if "arrival" in selected.columns:
        selected["arrival"] = pd.to_datetime(selected["arrival"], errors="coerce")
        output["commodity_known_at"] = selected.groupby("date")["arrival"].max().reindex(output.index)
    else:
        output["commodity_known_at"] = output.index
    cl = output["cl_return_1d"]
    for symbol in ("ho", "xb"):
        beta = _lagged_rolling_beta(
            output[f"{symbol}_return_1d"], cl, beta_window, beta_min_periods
        )
        output[f"{symbol}_cl_beta"] = beta
        output[f"{symbol}_residual_1d"] = output[f"{symbol}_return_1d"] - beta * cl

    components = {
        "cl_state": output["cl_return_1d"],
        "ho_state": output["ho_return_1d"],
        "ho_residual": output["ho_residual_1d"],
        "xb_residual": output["xb_residual_1d"],
        "hg_state": output["hg_return_1d"],
    }
    for name, daily in components.items():
        cumulative = daily.rolling(signal_window, min_periods=signal_window).sum()
        output[f"{name}_{signal_window}d"] = cumulative
        output[f"{name}_{signal_window}d_z"] = _lagged_rolling_z(
            cumulative, z_window, z_min_periods
        )
    output[f"cl_ho_joint_{signal_window}d_z"] = output[
        [f"cl_state_{signal_window}d_z", f"ho_residual_{signal_window}d_z"]
    ].min(axis=1)
    return output.reset_index()


def add_forward_returns(
    equity: pd.DataFrame,
    return_columns: list[str],
    horizon: int,
) -> pd.DataFrame:
    required = {"date", "ticker", *return_columns}
    if not required.issubset(equity.columns):
        raise ValueError(f"equity frame is missing columns: {sorted(required.difference(equity.columns))}")
    out = equity.copy()
    out["date"] = pd.to_datetime(out["date"], errors="coerce").dt.normalize()
    out = out.sort_values(["ticker", "date"]).reset_index(drop=True)
    out[f"forward_{horizon}d_entry_date"] = out.groupby("ticker")["date"].shift(-1)
    out[f"forward_{horizon}d_end_date"] = out.groupby("ticker")["date"].shift(-horizon)
    for column in return_columns:
        values = pd.to_numeric(out[column], errors="coerce")
        out[f"forward_{horizon}d__{column}"] = values.groupby(out["ticker"]).transform(
            lambda series: series.shift(-1).rolling(horizon, min_periods=horizon).sum().shift(-(horizon - 1))
        )
    return out


def select_nonoverlapping_shock_dates(
    signals: pd.DataFrame,
    signal_column: str,
    threshold: float,
    horizon: int,
) -> pd.DataFrame:
    if signal_column not in signals.columns or "date" not in signals.columns:
        raise ValueError(f"signals require date and {signal_column}")
    frame = signals.loc[:, ["date", signal_column]].copy().sort_values("date")
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce").dt.normalize()
    value = pd.to_numeric(frame[signal_column], errors="coerce")
    frame["threshold_crossing"] = value.ge(threshold) & value.shift(1).lt(threshold)
    candidates = frame.loc[frame["threshold_crossing"]].copy()
    selected: list[int] = []
    last_position = -10**9
    date_position = {date: idx for idx, date in enumerate(frame["date"])}
    for idx, row in candidates.iterrows():
        position = date_position[row["date"]]
        if position > last_position + horizon:
            selected.append(idx)
            last_position = position
    return candidates.loc[selected].reset_index(drop=True)


def mean_t_stat(value: pd.Series) -> float:
    clean = pd.to_numeric(value, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    if len(clean) < 2:
        return np.nan
    std = float(clean.std(ddof=1))
    return float(clean.mean() / std * np.sqrt(len(clean))) if std > 0 else np.nan


def bootstrap_mean_interval(
    value: pd.Series,
    samples: int = 10_000,
    seed: int = 20260803,
) -> tuple[float, float, float]:
    clean = pd.to_numeric(value, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna().to_numpy()
    if len(clean) < 2:
        return np.nan, np.nan, np.nan
    rng = np.random.default_rng(seed)
    draws = rng.choice(clean, size=(samples, len(clean)), replace=True).mean(axis=1)
    return tuple(float(x) for x in np.quantile(draws, [0.025, 0.5, 0.975]))
