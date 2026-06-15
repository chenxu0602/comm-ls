from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from comm_ls.forecast import _category_for, _forward_sum, _map_features_to_signal_dates
from comm_ls.reaction import load_frame
from comm_ls.universe import load_commodity_exposure_map


DEFAULT_DISCOVERY_HORIZONS = [10, 21]
DEFAULT_DISCOVERY_SAMPLE_YEARS = [3, 5, 10]
QUARTERLY_FEATURE_MATRIX_COLUMNS = [
    "commodity",
    "quarter",
    "quarter_start",
    "asof_date",
    "lookback_years",
    "sample_start",
    "sample_end",
    "ticker",
    "theme",
    "role",
    "region",
    "feature",
    "feature_family",
    "horizon_days",
    "observations",
    "effective_observations",
    "corr",
    "t_stat",
    "abs_t_stat",
    "nonoverlap_corr",
    "nonoverlap_t_stat",
    "nonoverlap_abs_t_stat",
    "nonoverlap_beta_per_1z",
    "nonoverlap_hit_rate",
    "beta_per_1z",
    "direction_sign",
    "hit_rate",
    "residual_vol",
    "target_end_date_max",
]
CORE_PRICE_MOMENTUM_FEATURES = [
    "ret_21d",
    "ret_42d",
    "ret_63d",
    "ret_accel_21d_vs_63d",
    "drawdown_63d",
    "breakout_252d",
]
FRONT_PRICE_REGIME_FEATURES = [
    "front_price_high_share_63d_q80_3y",
    "front_price_high_share_100d_q80_3y",
    "front_price_high_share_126d_q80_3y",
    "front_price_high_days_100d_q80_3y",
    "front_price_high_excess_100d_q80_3y",
    "front_price_high_consecutive_days_q80_3y",
    "front_price_high_share_63d_q90_3y",
    "front_price_high_share_100d_q90_3y",
    "front_price_high_share_126d_q90_3y",
    "front_price_high_days_100d_q90_3y",
    "front_price_high_excess_100d_q90_3y",
    "front_price_high_consecutive_days_q90_3y",
    "front_price_low_share_63d_q20_3y",
    "front_price_low_share_100d_q20_3y",
    "front_price_low_share_126d_q20_3y",
    "front_price_low_days_100d_q20_3y",
    "front_price_low_shortfall_100d_q20_3y",
    "front_price_low_consecutive_days_q20_3y",
    "front_price_low_share_63d_q10_3y",
    "front_price_low_share_100d_q10_3y",
    "front_price_low_share_126d_q10_3y",
    "front_price_low_days_100d_q10_3y",
    "front_price_low_shortfall_100d_q10_3y",
    "front_price_low_consecutive_days_q10_3y",
]

CURVE_SHOCK_VOL_FEATURES = [
    "front_second_spread",
    "front_third_spread",
    "front_second_annualized_carry",
    "front_third_annualized_carry",
    "calendar_dec_annualized_carry",
    "next_jun_annualized_carry",
    "liquid_deferred_annualized_carry",
    "activity_deferred_annualized_carry",
    "front_second_backwardation_steepness",
    "front_third_backwardation_steepness",
    "calendar_dec_backwardation_steepness",
    "liquid_deferred_backwardation_steepness",
    "activity_deferred_backwardation_steepness",
    "carry",
    "carry_chg_5d",
    "carry_chg_21d",
    "front_second_spread_chg_21d",
    "front_third_spread_chg_21d",
    "front_second_annualized_carry_chg_21d",
    "front_third_annualized_carry_chg_21d",
    "calendar_dec_annualized_carry_chg_21d",
    "next_jun_annualized_carry_chg_21d",
    "liquid_deferred_annualized_carry_chg_21d",
    "activity_deferred_annualized_carry_chg_21d",
    "front_second_backwardation_steepness_chg_21d",
    "front_third_backwardation_steepness_chg_21d",
    "calendar_dec_backwardation_steepness_chg_21d",
    "liquid_deferred_backwardation_steepness_chg_21d",
    "activity_deferred_backwardation_steepness_chg_21d",
    "term_structure_regime_change",
    "backwardation_regime_change",
    "days_in_backwardation",
    "realized_vol_20d",
    "realized_vol_63d",
    "vol_chg_20d",
    "abs_ret_1d",
    "large_move_2sigma",
    "m0_atr_14_pct",
    "volume_shock_63d",
    "oi_shock_63d",
    "volume_surge_63d",
    "oi_surge_63d",
    "carry_pctile_252d",
]
BROAD_DISCOVERY_FEATURES = [
    *CORE_PRICE_MOMENTUM_FEATURES,
    *FRONT_PRICE_REGIME_FEATURES,
    *CURVE_SHOCK_VOL_FEATURES,
]
DISCOVERY_FEATURE_PRESETS = {
    "priority": BROAD_DISCOVERY_FEATURES,
    "curve_shock_vol": CURVE_SHOCK_VOL_FEATURES,
    "broad": BROAD_DISCOVERY_FEATURES,
}
FIRST_ORDER_ROLES = {
    "CL": {"producer", "services", "drilling"},
    "HG": {"producer", "diversified_miner"},
}
SECOND_ORDER_ROLES = {
    "CL": {"consumer", "refiner", "midstream", "shipping", "exporter", "energy_cost"},
    "HG": {"consumer", "industrial_metals_cycle"},
}


def _write_frame(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".parquet":
        df.to_parquet(path, index=False)
    elif path.suffix == ".csv":
        df.to_csv(path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")


def _feature_columns_for_signals(
    signals: pd.DataFrame,
    features: list[str] | None,
    feature_preset: str,
    min_observations: int,
    include_prestandardized: bool,
) -> list[str]:
    if features:
        feature_columns = features
    else:
        if feature_preset not in DISCOVERY_FEATURE_PRESETS:
            raise ValueError(f"Unknown feature_preset: {feature_preset}")
        feature_columns = [
            feature
            for feature in DISCOVERY_FEATURE_PRESETS[feature_preset]
            if feature in signals.columns and signals[feature].notna().sum() >= min_observations
        ]
        if include_prestandardized:
            feature_columns.extend(
                col
                for col in signals.columns
                if col.endswith("_z_252d") and signals[col].notna().sum() >= min_observations
            )

    missing = sorted(set(feature_columns).difference(signals.columns))
    if missing:
        raise ValueError(f"Commodity features are missing columns: {missing}")
    if not feature_columns:
        raise ValueError("No usable discovery features found")
    return list(dict.fromkeys(feature_columns))


def _quarter_periods(frame: pd.DataFrame, start: str | None, end: str | None) -> list[tuple[str, pd.Timestamp, pd.Timestamp]]:
    if frame.empty:
        return []
    q = frame[["quarter", "quarter_start", "asof_date"]].drop_duplicates().copy()
    q["quarter_start"] = pd.to_datetime(q["quarter_start"], utc=False)
    q["asof_date"] = pd.to_datetime(q["asof_date"], utc=False)
    if start is not None:
        q = q[q["quarter_start"] >= pd.Timestamp(start)]
    if end is not None:
        q = q[q["quarter_start"] <= pd.Timestamp(end)]
    return [
        (str(row.quarter), pd.Timestamp(row.quarter_start), pd.Timestamp(row.asof_date))
        for row in q.sort_values("quarter_start").itertuples(index=False)
    ]


def _scale_0_1(series: pd.Series) -> pd.Series:
    values = pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan)
    if values.notna().sum() == 0:
        return pd.Series(0.0, index=series.index)
    lo = values.min()
    hi = values.max()
    if pd.isna(lo) or pd.isna(hi) or hi <= lo:
        return pd.Series(0.5, index=series.index)
    return ((values - lo) / (hi - lo)).fillna(0.0)


def _scan_one_ticker_quarter(
    panel: pd.DataFrame,
    z_features: pd.DataFrame,
    ticker: str,
    commodity: str,
    quarter: str,
    quarter_start: pd.Timestamp,
    asof_date: pd.Timestamp,
    feature_columns: list[str],
    horizons: list[int],
    sample_years: list[int],
    min_observations: int,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    signal_dates = pd.to_datetime(panel["signal_date"], utc=False)
    signal_ns = signal_dates.to_numpy(dtype="datetime64[ns]")
    feature_arrays = {
        feature: pd.to_numeric(z_features[feature], errors="coerce").to_numpy(dtype=float)
        for feature in feature_columns
    }
    target_arrays = {
        horizon: pd.to_numeric(panel[f"residual_return_fwd_{horizon}d"], errors="coerce").to_numpy(dtype=float)
        for horizon in horizons
    }
    target_end_masks = {
        horizon: (
            pd.to_datetime(panel[f"target_end_date_{horizon}d"], utc=False) <= asof_date
        ).to_numpy()
        for horizon in horizons
    }
    for years in sample_years:
        sample_start = asof_date - pd.DateOffset(years=years)
        sample_name = f"last_{years}y"
        base_mask = (signal_dates >= sample_start).to_numpy() & (signal_dates <= asof_date).to_numpy()
        for feature in feature_columns:
            x_all = feature_arrays[feature]
            for horizon in horizons:
                target_values = target_arrays[horizon]
                mask = base_mask & target_end_masks[horizon]
                x = x_all[mask]
                y = target_values[mask]
                valid = np.isfinite(x) & np.isfinite(y)
                x = x[valid]
                y = y[valid]
                observations = len(x)
                if observations < min_observations:
                    continue
                x_std = float(np.std(x, ddof=1))
                y_std = float(np.std(y, ddof=1))
                if x_std == 0 or y_std == 0:
                    continue

                corr = float(np.corrcoef(x, y)[0, 1])
                if pd.isna(corr):
                    continue
                t_stat = corr * np.sqrt((observations - 2) / max(1e-12, 1.0 - corr * corr))
                beta_per_z = float(np.cov(y, x, ddof=1)[0, 1] / np.var(x, ddof=1))
                signed = np.sign(x) * y
                valid_signal_ns = signal_ns[mask][valid]
                rows.append(
                    {
                        "quarter": quarter,
                        "quarter_start": quarter_start.date().isoformat(),
                        "asof_date": asof_date.date().isoformat(),
                        "commodity": commodity,
                        "ticker": ticker,
                        "sample": sample_name,
                        "sample_years": years,
                        "sample_start": pd.Timestamp(valid_signal_ns.min()).date().isoformat(),
                        "sample_end": pd.Timestamp(valid_signal_ns.max()).date().isoformat(),
                        "feature": feature,
                        "feature_family": _category_for(feature),
                        "horizon_days": horizon,
                        "observations": observations,
                        "corr": corr,
                        "t_stat": t_stat,
                        "abs_t_stat": abs(t_stat),
                        "beta_per_1z": beta_per_z,
                        "direction_sign": float(np.sign(beta_per_z)) if beta_per_z != 0 else 0.0,
                        "mean_signed_return": float(np.mean(signed)),
                        "hit_rate": float(np.mean(signed > 0)),
                        "residual_vol": y_std,
                    }
                )
    return pd.DataFrame(rows)


def build_commodity_sensitivity_matrix(
    commodity_signals: pd.DataFrame,
    beta_returns: pd.DataFrame,
    broad_universe: pd.DataFrame,
    commodity: str,
    features: list[str] | None = None,
    horizons: list[int] | None = None,
    sample_years: list[int] | None = None,
    start: str | None = None,
    end: str | None = None,
    feature_z_window: int = 252,
    min_feature_observations: int = 126,
    min_observations: int = 126,
    include_prestandardized: bool = False,
    feature_preset: str = "priority",
) -> pd.DataFrame:
    commodity = commodity.upper().strip()
    horizons = horizons or DEFAULT_DISCOVERY_HORIZONS
    sample_years = sample_years or DEFAULT_DISCOVERY_SAMPLE_YEARS

    signals = commodity_signals.copy()
    signals["symbol"] = signals["symbol"].astype(str).str.upper().str.strip()
    signals = signals[signals["symbol"] == commodity].copy()
    if signals.empty:
        raise ValueError(f"No commodity features found for {commodity}")
    signals["date"] = pd.to_datetime(signals["date"], utc=False)
    signals["arrival"] = pd.to_datetime(signals["arrival"], utc=False)

    feature_columns = _feature_columns_for_signals(
        signals=signals,
        features=features,
        feature_preset=feature_preset,
        min_observations=min_observations,
        include_prestandardized=include_prestandardized,
    )

    stock = beta_returns.copy()
    stock["date"] = pd.to_datetime(stock["date"], utc=False)
    stock["ticker"] = stock["ticker"].astype(str).str.upper().str.strip()
    stock = stock.dropna(subset=["residual_return"])

    quarters = _quarter_periods(broad_universe, start=start, end=end)
    if not quarters:
        return pd.DataFrame()

    stock_dates = pd.Series(stock["date"].unique()).sort_values()
    aligned = _map_features_to_signal_dates(
        commodity_features=signals,
        stock_dates=stock_dates,
        feature_columns=feature_columns,
    )

    rows: list[pd.DataFrame] = []
    active_by_quarter = {
        quarter: sorted(group["ticker"].astype(str).str.upper().unique())
        for quarter, group in broad_universe.groupby("quarter", sort=True)
    }
    for ticker, s in stock.groupby("ticker", sort=True):
        needed_quarters = [item for item in quarters if ticker in active_by_quarter.get(item[0], [])]
        if not needed_quarters:
            continue

        s = s.sort_values("date").copy()
        for horizon in horizons:
            s[f"residual_return_fwd_{horizon}d"] = _forward_sum(s["residual_return"], horizon)
            s[f"target_end_date_{horizon}d"] = s["date"].shift(-horizon)

        merge_cols = ["date", "ticker", "theme", "role", "region"]
        for horizon in horizons:
            merge_cols.extend([f"residual_return_fwd_{horizon}d", f"target_end_date_{horizon}d"])
        panel = aligned.merge(
            s[merge_cols],
            left_on="signal_date",
            right_on="date",
            how="inner",
        ).drop(columns=["date_y"])
        panel = panel.rename(columns={"date_x": "feature_date"}).sort_values("signal_date").reset_index(drop=True)
        if panel.empty:
            continue

        z_features = pd.DataFrame({"signal_date": panel["signal_date"]})
        for feature in feature_columns:
            value = pd.to_numeric(panel[feature], errors="coerce")
            mean = value.rolling(feature_z_window, min_periods=min_feature_observations).mean()
            std = value.rolling(feature_z_window, min_periods=min_feature_observations).std()
            z_features[feature] = (value - mean) / std

        for quarter, quarter_start, asof_date in needed_quarters:
            result = _scan_one_ticker_quarter(
                panel=panel,
                z_features=z_features,
                ticker=ticker,
                commodity=commodity,
                quarter=quarter,
                quarter_start=quarter_start,
                asof_date=asof_date,
                feature_columns=feature_columns,
                horizons=horizons,
                sample_years=sample_years,
                min_observations=min_observations,
            )
            if not result.empty:
                meta = s[["ticker", "theme", "role", "region"]].drop_duplicates("ticker")
                result = result.merge(meta, on="ticker", how="left")
                rows.append(result)

    if not rows:
        return pd.DataFrame()
    return pd.concat(rows, ignore_index=True).sort_values(
        ["commodity", "quarter", "ticker", "feature", "horizon_days", "sample_years"]
    ).reset_index(drop=True)


def build_commodity_sensitivity_matrix_from_paths(
    commodity_signals_path: Path,
    beta_returns_path: Path,
    broad_universe_path: Path,
    output_path: Path,
    commodity: str,
    features: list[str] | None = None,
    horizons: list[int] | None = None,
    sample_years: list[int] | None = None,
    start: str | None = None,
    end: str | None = None,
    feature_z_window: int = 252,
    min_feature_observations: int = 126,
    min_observations: int = 126,
    include_prestandardized: bool = False,
    feature_preset: str = "priority",
) -> pd.DataFrame:
    matrix = build_commodity_sensitivity_matrix(
        commodity_signals=load_frame(commodity_signals_path),
        beta_returns=load_frame(beta_returns_path),
        broad_universe=load_frame(broad_universe_path),
        commodity=commodity,
        features=features,
        horizons=horizons,
        sample_years=sample_years,
        start=start,
        end=end,
        feature_z_window=feature_z_window,
        min_feature_observations=min_feature_observations,
        min_observations=min_observations,
        include_prestandardized=include_prestandardized,
        feature_preset=feature_preset,
    )
    _write_frame(matrix, output_path)
    return matrix


def build_daily_feature_return_cache(
    commodity_signals: pd.DataFrame,
    beta_returns: pd.DataFrame,
    commodity: str,
    features: list[str] | None = None,
    horizons: list[int] | None = None,
    feature_preset: str = "priority",
    feature_z_window: int = 252,
    min_feature_observations: int = 126,
    min_observations: int = 126,
    include_prestandardized: bool = False,
) -> pd.DataFrame:
    commodity = commodity.upper().strip()
    horizons = horizons or DEFAULT_DISCOVERY_HORIZONS

    signals = commodity_signals.copy()
    signals["symbol"] = signals["symbol"].astype(str).str.upper().str.strip()
    signals = signals[signals["symbol"] == commodity].copy()
    if signals.empty:
        raise ValueError(f"No commodity features found for {commodity}")
    signals["date"] = pd.to_datetime(signals["date"], utc=False)
    signals["arrival"] = pd.to_datetime(signals["arrival"], utc=False)

    feature_columns = _feature_columns_for_signals(
        signals=signals,
        features=features,
        feature_preset=feature_preset,
        min_observations=min_observations,
        include_prestandardized=include_prestandardized,
    )

    stock = beta_returns.copy()
    stock["date"] = pd.to_datetime(stock["date"], utc=False)
    stock["ticker"] = stock["ticker"].astype(str).str.upper().str.strip()
    stock = stock.sort_values(["ticker", "date"]).copy()

    stock_dates = pd.Series(stock["date"].unique()).sort_values()
    aligned = _map_features_to_signal_dates(
        commodity_features=signals,
        stock_dates=stock_dates,
        feature_columns=feature_columns,
    )
    aligned = aligned.rename(columns={"date": "commodity_feature_date", "arrival": "commodity_arrival"})
    z = aligned[["signal_date", "commodity_feature_date", "commodity_arrival"]].copy()
    for feature in feature_columns:
        value = pd.to_numeric(aligned[feature], errors="coerce")
        mean = value.rolling(feature_z_window, min_periods=min_feature_observations).mean()
        std = value.rolling(feature_z_window, min_periods=min_feature_observations).std()
        z[f"feature_z__{feature}"] = (value - mean) / std

    keep_cols = [
        "date",
        "ticker",
        "theme",
        "role",
        "region",
        "adj_close",
        "raw_return",
        "market_ticker",
        "sector_ticker",
        "market_return",
        "sector_return",
        "market_beta",
        "sector_beta",
        "beta_observations",
        "residual_return",
    ]
    optional_cols = [
        "beta_estimation_end",
        "beta_return_frequency",
        "beta_update_frequency",
        "beta_weighting",
        "beta_lookback_observations",
        "beta_half_life_months",
        "beta_smoothing",
        "hedge_ratio_scale",
    ]
    keep_cols.extend([col for col in optional_cols if col in stock.columns])
    cache = stock[[col for col in keep_cols if col in stock.columns]].copy()

    for ticker, group_index in cache.groupby("ticker", sort=False).groups.items():
        idx = list(group_index)
        s = cache.loc[idx, "residual_return"]
        dates = cache.loc[idx, "date"]
        for horizon in horizons:
            cache.loc[idx, f"fwd_residual_return_{horizon}d"] = _forward_sum(s, horizon).to_numpy()
            cache.loc[idx, f"target_end_{horizon}d"] = dates.shift(-horizon).to_numpy()

    cache = cache.merge(z, left_on="date", right_on="signal_date", how="left").drop(columns=["signal_date"])
    cache.insert(0, "commodity", commodity)
    cache["feature_preset"] = feature_preset
    cache["feature_z_window"] = feature_z_window
    cache["min_feature_observations"] = min_feature_observations
    return cache.sort_values(["commodity", "ticker", "date"]).reset_index(drop=True)


def build_daily_feature_return_cache_from_paths(
    commodity_signals_path: Path,
    beta_returns_path: Path,
    output_path: Path,
    commodity: str,
    features: list[str] | None = None,
    horizons: list[int] | None = None,
    feature_preset: str = "priority",
    feature_z_window: int = 252,
    min_feature_observations: int = 126,
    min_observations: int = 126,
    include_prestandardized: bool = False,
) -> pd.DataFrame:
    cache = build_daily_feature_return_cache(
        commodity_signals=load_frame(commodity_signals_path),
        beta_returns=load_frame(beta_returns_path),
        commodity=commodity,
        features=features,
        horizons=horizons,
        feature_preset=feature_preset,
        feature_z_window=feature_z_window,
        min_feature_observations=min_feature_observations,
        min_observations=min_observations,
        include_prestandardized=include_prestandardized,
    )
    _write_frame(cache, output_path)
    return cache


def build_quarterly_stock_feature_matrix(
    cache: pd.DataFrame,
    broad_universe: pd.DataFrame,
    commodity: str,
    lookback_years: list[int] | None = None,
    horizons: list[int] | None = None,
    start: str | None = None,
    end: str | None = None,
    min_observations: int = 126,
) -> pd.DataFrame:
    commodity = commodity.upper().strip()
    lookback_years = lookback_years or DEFAULT_DISCOVERY_SAMPLE_YEARS
    horizons = horizons or DEFAULT_DISCOVERY_HORIZONS

    cache = cache.copy()
    cache["commodity"] = cache["commodity"].astype(str).str.upper().str.strip()
    cache = cache[cache["commodity"] == commodity].copy()
    if cache.empty:
        return pd.DataFrame()
    cache["date"] = pd.to_datetime(cache["date"], utc=False)
    cache["ticker"] = cache["ticker"].astype(str).str.upper().str.strip()
    for horizon in horizons:
        end_col = f"target_end_{horizon}d"
        if end_col in cache.columns:
            cache[end_col] = pd.to_datetime(cache[end_col], utc=False)

    feature_z_cols = [col for col in cache.columns if col.startswith("feature_z__")]
    if not feature_z_cols:
        raise ValueError("Cache has no feature_z__ columns")

    quarters = _quarter_periods(broad_universe, start=start, end=end)
    active_by_quarter = {
        quarter: sorted(group["ticker"].astype(str).str.upper().unique())
        for quarter, group in broad_universe.groupby("quarter", sort=True)
    }
    cache_by_ticker = {
        ticker: group.sort_values("date").copy()
        for ticker, group in cache.groupby("ticker", sort=True)
    }

    rows: list[dict[str, object]] = []
    for quarter, quarter_start, asof_date in quarters:
        active_tickers = active_by_quarter.get(quarter, [])
        for ticker in active_tickers:
            ticker_cache = cache_by_ticker.get(ticker)
            if ticker_cache is None:
                continue
            base_asof = ticker_cache[ticker_cache["date"] <= asof_date]
            if base_asof.empty:
                continue

            for years in lookback_years:
                sample_start = asof_date - pd.DateOffset(years=years)
                sample_base = base_asof[base_asof["date"] >= sample_start]
                if sample_base.empty:
                    continue

                for horizon in horizons:
                    target_col = f"fwd_residual_return_{horizon}d"
                    target_end_col = f"target_end_{horizon}d"
                    if target_col not in sample_base.columns or target_end_col not in sample_base.columns:
                        continue
                    sample = sample_base[sample_base[target_end_col] <= asof_date]
                    if sample.empty:
                        continue
                    y_all = pd.to_numeric(sample[target_col], errors="coerce").to_numpy(dtype=float)

                    for feature_col in feature_z_cols:
                        x_all = pd.to_numeric(sample[feature_col], errors="coerce").to_numpy(dtype=float)
                        valid = np.isfinite(x_all) & np.isfinite(y_all)
                        observations = int(valid.sum())
                        if observations < min_observations:
                            continue
                        x = x_all[valid]
                        y = y_all[valid]
                        x_std = float(np.std(x, ddof=1))
                        y_std = float(np.std(y, ddof=1))
                        if x_std == 0 or y_std == 0:
                            continue

                        corr = float(np.corrcoef(x, y)[0, 1])
                        if pd.isna(corr):
                            continue
                        beta_per_z = float(np.cov(y, x, ddof=1)[0, 1] / np.var(x, ddof=1))
                        t_stat = corr * np.sqrt((observations - 2) / max(1e-12, 1.0 - corr * corr))
                        signed = np.sign(x) * y
                        feature = feature_col.removeprefix("feature_z__")
                        valid_dates = sample.loc[valid, "date"]
                        rows.append(
                            {
                                "commodity": commodity,
                                "quarter": quarter,
                                "quarter_start": quarter_start.date().isoformat(),
                                "asof_date": asof_date.date().isoformat(),
                                "lookback_years": years,
                                "sample_start": valid_dates.min().date().isoformat(),
                                "sample_end": valid_dates.max().date().isoformat(),
                                "ticker": ticker,
                                "feature": feature,
                                "feature_family": _category_for(feature),
                                "horizon_days": horizon,
                                "observations": observations,
                                "corr": corr,
                                "t_stat": t_stat,
                                "abs_t_stat": abs(t_stat),
                                "beta_per_1z": beta_per_z,
                                "direction_sign": float(np.sign(beta_per_z)) if beta_per_z != 0 else 0.0,
                                "hit_rate": float(np.mean(signed > 0)),
                                "residual_vol": y_std,
                                "target_end_date_max": sample.loc[valid, target_end_col].max().date().isoformat(),
                            }
                        )

    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows).sort_values(
        ["commodity", "quarter", "ticker", "feature", "horizon_days", "lookback_years"]
    ).reset_index(drop=True)


def _nonoverlap_stats(
    dates: pd.Series,
    target_end_dates: pd.Series,
    x_all: np.ndarray,
    y_all: np.ndarray,
    valid: np.ndarray,
) -> dict[str, float | int]:
    selected: list[int] = []
    last_target_end: pd.Timestamp | None = None
    date_values = pd.to_datetime(dates, utc=False)
    target_end_values = pd.to_datetime(target_end_dates, utc=False)
    for idx in np.flatnonzero(valid):
        date = pd.Timestamp(date_values.iloc[idx])
        target_end = pd.Timestamp(target_end_values.iloc[idx])
        if pd.isna(date) or pd.isna(target_end):
            continue
        if last_target_end is None or date > last_target_end:
            selected.append(int(idx))
            last_target_end = target_end

    observations = len(selected)
    if observations < 3:
        return {
            "effective_observations": observations,
            "nonoverlap_corr": np.nan,
            "nonoverlap_t_stat": np.nan,
            "nonoverlap_abs_t_stat": np.nan,
            "nonoverlap_beta_per_1z": np.nan,
            "nonoverlap_hit_rate": np.nan,
        }

    x = x_all[selected].astype(float)
    y = y_all[selected].astype(float)
    x_std = float(np.std(x, ddof=1))
    y_std = float(np.std(y, ddof=1))
    if x_std == 0 or y_std == 0:
        return {
            "effective_observations": observations,
            "nonoverlap_corr": np.nan,
            "nonoverlap_t_stat": np.nan,
            "nonoverlap_abs_t_stat": np.nan,
            "nonoverlap_beta_per_1z": np.nan,
            "nonoverlap_hit_rate": np.nan,
        }

    corr = float(np.corrcoef(x, y)[0, 1])
    if not np.isfinite(corr):
        t_stat = np.nan
    else:
        t_stat = corr * np.sqrt((observations - 2) / max(1e-12, 1.0 - corr * corr))
    beta_per_z = float(np.cov(y, x, ddof=1)[0, 1] / np.var(x, ddof=1))
    hit_rate = float(np.mean(np.sign(x) * y > 0))
    return {
        "effective_observations": observations,
        "nonoverlap_corr": corr,
        "nonoverlap_t_stat": float(t_stat),
        "nonoverlap_abs_t_stat": abs(float(t_stat)) if np.isfinite(t_stat) else np.nan,
        "nonoverlap_beta_per_1z": beta_per_z,
        "nonoverlap_hit_rate": hit_rate,
    }


def _stock_feature_rows_for_quarter_window(
    ticker_cache: pd.DataFrame,
    feature_z_cols: list[str],
    commodity: str,
    quarter: str,
    quarter_start: pd.Timestamp,
    asof_date: pd.Timestamp,
    ticker: str,
    years: int,
    horizons: list[int],
    min_observations: int,
) -> list[dict[str, object]]:
    sample_start = asof_date - pd.DateOffset(years=years)
    sample_base = ticker_cache[(ticker_cache["date"] >= sample_start) & (ticker_cache["date"] <= asof_date)]
    if sample_base.empty:
        return []

    theme = sample_base["theme"].dropna().iloc[-1] if "theme" in sample_base and sample_base["theme"].notna().any() else None
    role = sample_base["role"].dropna().iloc[-1] if "role" in sample_base and sample_base["role"].notna().any() else None
    region = (
        sample_base["region"].dropna().iloc[-1]
        if "region" in sample_base and sample_base["region"].notna().any()
        else None
    )

    rows: list[dict[str, object]] = []
    for horizon in horizons:
        target_col = f"fwd_residual_return_{horizon}d"
        target_end_col = f"target_end_{horizon}d"
        if target_col not in sample_base.columns or target_end_col not in sample_base.columns:
            continue
        sample = sample_base[sample_base[target_end_col] <= asof_date]
        if sample.empty:
            continue
        y = pd.to_numeric(sample[target_col], errors="coerce").to_numpy(dtype=float)
        x_matrix = sample[feature_z_cols].to_numpy(dtype=float)
        valid = np.isfinite(x_matrix) & np.isfinite(y[:, None])
        observations_by_feature = valid.sum(axis=0).astype(int)
        good = observations_by_feature >= min_observations
        if not good.any():
            continue

        y_matrix = np.broadcast_to(y[:, None], x_matrix.shape)
        x_values = np.where(valid, x_matrix, 0.0)
        y_values = np.where(valid, y_matrix, 0.0)
        n = observations_by_feature.astype(float)

        with np.errstate(invalid="ignore", divide="ignore"):
            x_mean = x_values.sum(axis=0) / n
            y_mean = y_values.sum(axis=0) / n
        dx = np.where(valid, x_matrix - x_mean, 0.0)
        dy = np.where(valid, y_matrix - y_mean, 0.0)
        cov_sum = (dx * dy).sum(axis=0)
        x_var_sum = (dx * dx).sum(axis=0)
        y_var_sum = (dy * dy).sum(axis=0)

        with np.errstate(invalid="ignore", divide="ignore"):
            corr_values = cov_sum / np.sqrt(x_var_sum * y_var_sum)
            beta_values = cov_sum / x_var_sum
            t_values = corr_values * np.sqrt((n - 2.0) / np.maximum(1e-12, 1.0 - corr_values * corr_values))
            residual_vol_values = np.sqrt(y_var_sum / (n - 1.0))
        hit_counts = ((np.sign(x_matrix) * y[:, None] > 0) & valid).sum(axis=0)
        hit_rates = np.divide(hit_counts, n, out=np.full_like(n, np.nan, dtype=float), where=n > 0)

        nonoverlap_idx = np.arange(0, len(sample), max(1, horizon), dtype=int)
        x_non = x_matrix[nonoverlap_idx]
        y_non = y[nonoverlap_idx]
        valid_non = np.isfinite(x_non) & np.isfinite(y_non[:, None])
        n_non = valid_non.sum(axis=0).astype(float)
        x_non_values = np.where(valid_non, x_non, 0.0)
        y_non_matrix = np.broadcast_to(y_non[:, None], x_non.shape)
        y_non_values = np.where(valid_non, y_non_matrix, 0.0)
        with np.errstate(invalid="ignore", divide="ignore"):
            x_non_mean = np.divide(
                x_non_values.sum(axis=0),
                n_non,
                out=np.full_like(n_non, np.nan, dtype=float),
                where=n_non > 0,
            )
            y_non_mean = np.divide(
                y_non_values.sum(axis=0),
                n_non,
                out=np.full_like(n_non, np.nan, dtype=float),
                where=n_non > 0,
            )
        dx_non = np.where(valid_non, x_non - x_non_mean, 0.0)
        dy_non = np.where(valid_non, y_non_matrix - y_non_mean, 0.0)
        cov_non_sum = (dx_non * dy_non).sum(axis=0)
        x_non_var_sum = (dx_non * dx_non).sum(axis=0)
        y_non_var_sum = (dy_non * dy_non).sum(axis=0)
        with np.errstate(invalid="ignore", divide="ignore"):
            corr_non_values = cov_non_sum / np.sqrt(x_non_var_sum * y_non_var_sum)
            beta_non_values = cov_non_sum / x_non_var_sum
            t_non_values = corr_non_values * np.sqrt(
                (n_non - 2.0) / np.maximum(1e-12, 1.0 - corr_non_values * corr_non_values)
            )
        valid_non_for_t = n_non >= 3
        corr_non_values = np.where(valid_non_for_t, corr_non_values, np.nan)
        beta_non_values = np.where(valid_non_for_t, beta_non_values, np.nan)
        t_non_values = np.where(valid_non_for_t, t_non_values, np.nan)
        hit_non_counts = ((np.sign(x_non) * y_non[:, None] > 0) & valid_non).sum(axis=0)
        hit_non_rates = np.divide(
            hit_non_counts,
            n_non,
            out=np.full_like(n_non, np.nan, dtype=float),
            where=n_non > 0,
        )

        dates = sample["date"]
        target_end_dates = sample[target_end_col]
        for feature_idx, feature_col in enumerate(feature_z_cols):
            if not good[feature_idx]:
                continue
            corr = float(corr_values[feature_idx])
            beta_per_z = float(beta_values[feature_idx])
            t_stat = float(t_values[feature_idx])
            residual_vol = float(residual_vol_values[feature_idx])
            if not all(np.isfinite(value) for value in [corr, beta_per_z, t_stat, residual_vol]):
                continue
            feature_valid = valid[:, feature_idx]
            observations = int(observations_by_feature[feature_idx])
            if observations < min_observations:
                continue
            feature = feature_col.removeprefix("feature_z__")
            valid_dates = dates.iloc[feature_valid]
            rows.append(
                {
                    "commodity": commodity,
                    "quarter": quarter,
                    "quarter_start": quarter_start.date().isoformat(),
                    "asof_date": asof_date.date().isoformat(),
                    "lookback_years": years,
                    "sample_start": valid_dates.min().date().isoformat(),
                    "sample_end": valid_dates.max().date().isoformat(),
                    "ticker": ticker,
                    "theme": theme,
                    "role": role,
                    "region": region,
                    "feature": feature,
                    "feature_family": _category_for(feature),
                    "horizon_days": horizon,
                    "observations": observations,
                    "effective_observations": int(n_non[feature_idx]),
                    "corr": corr,
                    "t_stat": t_stat,
                    "abs_t_stat": abs(t_stat),
                    "nonoverlap_corr": float(corr_non_values[feature_idx]),
                    "nonoverlap_t_stat": float(t_non_values[feature_idx]),
                    "nonoverlap_abs_t_stat": abs(float(t_non_values[feature_idx]))
                    if np.isfinite(t_non_values[feature_idx])
                    else np.nan,
                    "nonoverlap_beta_per_1z": float(beta_non_values[feature_idx]),
                    "nonoverlap_hit_rate": float(hit_non_rates[feature_idx]),
                    "beta_per_1z": beta_per_z,
                    "direction_sign": float(np.sign(beta_per_z)) if beta_per_z != 0 else 0.0,
                    "hit_rate": float(hit_rates[feature_idx]),
                    "residual_vol": residual_vol,
                    "target_end_date_max": target_end_dates.iloc[feature_valid].max().date().isoformat(),
                }
            )
    return rows


def write_quarterly_stock_feature_matrix_files(
    cache: pd.DataFrame,
    broad_universe: pd.DataFrame,
    output_dir: Path,
    commodity: str,
    lookback_years: list[int] | None = None,
    horizons: list[int] | None = None,
    start: str | None = None,
    end: str | None = None,
    min_observations: int = 126,
) -> pd.DataFrame:
    commodity = commodity.upper().strip()
    lookback_years = lookback_years or DEFAULT_DISCOVERY_SAMPLE_YEARS
    horizons = horizons or DEFAULT_DISCOVERY_HORIZONS

    cache = cache.copy()
    cache["commodity"] = cache["commodity"].astype(str).str.upper().str.strip()
    cache = cache[cache["commodity"] == commodity].copy()
    if cache.empty:
        return pd.DataFrame()
    cache["date"] = pd.to_datetime(cache["date"], utc=False)
    cache["ticker"] = cache["ticker"].astype(str).str.upper().str.strip()
    feature_z_cols = [col for col in cache.columns if col.startswith("feature_z__")]
    if not feature_z_cols:
        raise ValueError("Cache has no feature_z__ columns")
    for col in feature_z_cols:
        cache[col] = pd.to_numeric(cache[col], errors="coerce")
    for horizon in horizons:
        end_col = f"target_end_{horizon}d"
        if end_col in cache.columns:
            cache[end_col] = pd.to_datetime(cache[end_col], utc=False)

    quarters = _quarter_periods(broad_universe, start=start, end=end)
    active_by_quarter = {
        quarter: sorted(group["ticker"].astype(str).str.upper().unique())
        for quarter, group in broad_universe.groupby("quarter", sort=True)
    }
    cache_by_ticker = {
        ticker: group.sort_values("date").copy()
        for ticker, group in cache.groupby("ticker", sort=True)
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    manifest_rows: list[dict[str, object]] = []
    for quarter, quarter_start, asof_date in quarters:
        active_tickers = active_by_quarter.get(quarter, [])
        for years in lookback_years:
            rows: list[dict[str, object]] = []
            for ticker in active_tickers:
                ticker_cache = cache_by_ticker.get(ticker)
                if ticker_cache is None:
                    continue
                rows.extend(
                    _stock_feature_rows_for_quarter_window(
                        ticker_cache=ticker_cache,
                        feature_z_cols=feature_z_cols,
                        commodity=commodity,
                        quarter=quarter,
                        quarter_start=quarter_start,
                        asof_date=asof_date,
                        ticker=ticker,
                        years=years,
                        horizons=horizons,
                        min_observations=min_observations,
                    )
                )

            matrix = pd.DataFrame(rows, columns=QUARTERLY_FEATURE_MATRIX_COLUMNS)
            if not matrix.empty:
                matrix = matrix.sort_values(
                    ["commodity", "quarter", "ticker", "feature", "horizon_days", "lookback_years"]
                ).reset_index(drop=True)
            output_path = output_dir / f"{commodity}-Features-{quarter}-{years}Y.csv"
            matrix.to_csv(output_path, index=False)
            manifest_rows.append(
                {
                    "commodity": commodity,
                    "quarter": quarter,
                    "quarter_start": quarter_start.date().isoformat(),
                    "asof_date": asof_date.date().isoformat(),
                    "lookback_years": years,
                    "rows": len(matrix),
                    "tickers": len(active_tickers),
                    "features": len(feature_z_cols),
                    "horizons": ",".join(str(horizon) for horizon in horizons),
                    "path": str(output_path),
                }
            )
    return pd.DataFrame(manifest_rows)


def build_quarterly_stock_feature_matrix_from_paths(
    cache_path: Path,
    broad_universe_path: Path,
    output_path: Path,
    commodity: str,
    lookback_years: list[int] | None = None,
    horizons: list[int] | None = None,
    start: str | None = None,
    end: str | None = None,
    min_observations: int = 126,
) -> pd.DataFrame:
    matrix = build_quarterly_stock_feature_matrix(
        cache=load_frame(cache_path),
        broad_universe=load_frame(broad_universe_path),
        commodity=commodity,
        lookback_years=lookback_years,
        horizons=horizons,
        start=start,
        end=end,
        min_observations=min_observations,
    )
    _write_frame(matrix, output_path)
    return matrix


def write_quarterly_stock_feature_matrix_files_from_paths(
    cache_path: Path,
    broad_universe_path: Path,
    output_dir: Path,
    manifest_path: Path | None,
    commodity: str,
    lookback_years: list[int] | None = None,
    horizons: list[int] | None = None,
    start: str | None = None,
    end: str | None = None,
    min_observations: int = 126,
) -> pd.DataFrame:
    manifest = write_quarterly_stock_feature_matrix_files(
        cache=load_frame(cache_path),
        broad_universe=load_frame(broad_universe_path),
        output_dir=output_dir,
        commodity=commodity,
        lookback_years=lookback_years,
        horizons=horizons,
        start=start,
        end=end,
        min_observations=min_observations,
    )
    if manifest_path is not None:
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest.to_csv(manifest_path, index=False)
    return manifest


def _best_sensitivity_by_ticker(matrix: pd.DataFrame, min_abs_t: float) -> pd.DataFrame:
    if matrix.empty:
        return pd.DataFrame()

    df = matrix.copy()
    df["signed_beta_for_stability"] = np.sign(pd.to_numeric(df["beta_per_1z"], errors="coerce"))
    grouped = (
        df.groupby(["commodity", "quarter", "ticker", "feature", "feature_family", "horizon_days"], dropna=False)
        .agg(
            samples=("sample", "nunique"),
            observations_min=("observations", "min"),
            observations_mean=("observations", "mean"),
            mean_beta_per_1z=("beta_per_1z", "mean"),
            median_beta_per_1z=("beta_per_1z", "median"),
            mean_abs_t_stat=("abs_t_stat", "mean"),
            max_abs_t_stat=("abs_t_stat", "max"),
            mean_hit_rate=("hit_rate", "mean"),
            residual_vol=("residual_vol", "mean"),
            sign_stability=("signed_beta_for_stability", lambda s: abs(float(pd.Series(s).dropna().mean()))),
            latest_asof_date=("asof_date", "max"),
        )
        .reset_index()
    )
    grouped["sensitivity_strength"] = grouped["mean_beta_per_1z"].abs()
    grouped["sensitivity_score_raw"] = (
        grouped["sensitivity_strength"]
        * grouped["mean_abs_t_stat"].clip(upper=6.0)
        * grouped["sign_stability"].fillna(0.0)
    )
    grouped["passes_discovery"] = (
        (grouped["samples"] >= 2)
        & (grouped["max_abs_t_stat"] >= min_abs_t)
        & (grouped["sign_stability"] >= 0.5)
    )
    grouped = grouped.sort_values(
        ["commodity", "quarter", "ticker", "passes_discovery", "sensitivity_score_raw"],
        ascending=[True, True, True, False, False],
    )
    return grouped.drop_duplicates(["commodity", "quarter", "ticker"], keep="first").reset_index(drop=True)


def _commodity_role_tier(commodity: str, role: str | float | None) -> str:
    role_text = "" if pd.isna(role) else str(role).strip()
    if role_text in FIRST_ORDER_ROLES.get(commodity, set()):
        return "first_order_anchor"
    if role_text in SECOND_ORDER_ROLES.get(commodity, set()):
        return "second_order_economic"
    return "unmapped"


def _anchor_correlation(
    beta_returns: pd.DataFrame,
    candidates: pd.DataFrame,
    exposure_map: pd.DataFrame,
    commodity: str,
    lookback_days: int,
) -> pd.DataFrame:
    stock = beta_returns.copy()
    stock["date"] = pd.to_datetime(stock["date"], utc=False)
    stock["ticker"] = stock["ticker"].astype(str).str.upper().str.strip()
    stock = stock.dropna(subset=["residual_return"])

    exposure = exposure_map.copy()
    exposure["ticker"] = exposure["ticker"].astype(str).str.upper().str.strip()
    exposure["commodity"] = exposure["commodity"].astype(str).str.upper().str.strip()
    anchors = exposure[
        (exposure["commodity"] == commodity)
        & (exposure["exposure_role"].astype(str).isin(FIRST_ORDER_ROLES.get(commodity, set())))
    ]["ticker"].unique()
    if len(anchors) == 0:
        return candidates[["commodity", "quarter", "ticker"]].assign(anchor_residual_corr=np.nan)

    rows: list[dict[str, object]] = []
    quarter_frame = candidates[["commodity", "quarter", "asof_date"]].drop_duplicates()
    for qrow in quarter_frame.itertuples(index=False):
        asof_date = pd.Timestamp(qrow.asof_date)
        start = asof_date - pd.offsets.BDay(lookback_days * 2)
        window = stock[(stock["date"] <= asof_date) & (stock["date"] >= start)].copy()
        pivot = window.pivot_table(index="date", columns="ticker", values="residual_return", aggfunc="last").tail(lookback_days)
        anchor_cols = [ticker for ticker in anchors if ticker in pivot.columns]
        quarter_candidates = candidates[candidates["quarter"].eq(qrow.quarter)]["ticker"].drop_duplicates()
        if not anchor_cols:
            for ticker in quarter_candidates:
                rows.append(
                    {
                        "commodity": qrow.commodity,
                        "quarter": qrow.quarter,
                        "ticker": ticker,
                        "anchor_residual_corr": np.nan,
                    }
                )
            continue

        anchor_ret = pivot[anchor_cols].mean(axis=1)
        for ticker in quarter_candidates:
            if ticker not in pivot.columns:
                corr = np.nan
            else:
                corr = pivot[ticker].corr(anchor_ret)
            rows.append(
                {
                    "commodity": qrow.commodity,
                    "quarter": qrow.quarter,
                    "ticker": ticker,
                    "anchor_residual_corr": corr,
                }
            )
    return pd.DataFrame(rows)


def classify_commodity_universe_tiers(
    sensitivity_matrix: pd.DataFrame,
    broad_universe: pd.DataFrame,
    exposure_map: pd.DataFrame,
    beta_returns: pd.DataFrame,
    commodity: str,
    min_abs_t: float = 2.0,
    anchor_corr_lookback_days: int = 252,
) -> pd.DataFrame:
    commodity = commodity.upper().strip()
    broad = broad_universe.copy()
    broad["ticker"] = broad["ticker"].astype(str).str.upper().str.strip()
    broad["quarter"] = broad["quarter"].astype(str)

    exposure = exposure_map.copy()
    exposure["ticker"] = exposure["ticker"].astype(str).str.upper().str.strip()
    exposure["commodity"] = exposure["commodity"].astype(str).str.upper().str.strip()
    exposure = exposure[exposure["commodity"] == commodity].copy()

    best = _best_sensitivity_by_ticker(sensitivity_matrix, min_abs_t=min_abs_t)
    if best.empty:
        best = pd.DataFrame(columns=["commodity", "quarter", "ticker"])

    candidates = broad.copy()
    candidates.insert(4, "commodity", commodity)
    candidates = candidates.merge(
        exposure[["ticker", "commodity", "exposure_role", "prior_weight", "notes"]],
        on=["ticker", "commodity"],
        how="left",
    )
    candidates = candidates.merge(best, on=["commodity", "quarter", "ticker"], how="left", suffixes=("", "_best"))

    candidates["tier"] = candidates["exposure_role"].map(lambda role: _commodity_role_tier(commodity, role))
    discovery = candidates["passes_discovery"].fillna(False) & candidates["exposure_role"].isna()
    candidates.loc[discovery, "tier"] = "statistical_discovery"
    candidates["economic_exposure"] = candidates["exposure_role"].notna()

    corr = _anchor_correlation(
        beta_returns=beta_returns,
        candidates=candidates,
        exposure_map=exposure_map,
        commodity=commodity,
        lookback_days=anchor_corr_lookback_days,
    )
    candidates = candidates.merge(corr, on=["commodity", "quarter", "ticker"], how="left")

    candidates["liquidity_score"] = candidates.groupby(["commodity", "quarter"])["adv_63d"].transform(
        lambda s: _scale_0_1(np.log1p(s))
    )
    candidates["sensitivity_score"] = candidates.groupby(["commodity", "quarter"])["sensitivity_score_raw"].transform(_scale_0_1)
    candidates["stability_score"] = pd.to_numeric(candidates["sign_stability"], errors="coerce").fillna(0.0).clip(0.0, 1.0)
    candidates["second_order_score"] = np.where(candidates["tier"].eq("second_order_economic"), 1.0, 0.0)
    candidates["obviousness_penalty"] = np.select(
        [
            candidates["tier"].eq("first_order_anchor"),
            candidates["tier"].eq("second_order_economic"),
        ],
        [1.0, 0.15],
        default=0.0,
    )
    candidates["anchor_correlation_penalty"] = pd.to_numeric(
        candidates["anchor_residual_corr"], errors="coerce"
    ).abs().fillna(0.0).clip(0.0, 1.0)
    candidates["universe_score"] = (
        0.30 * candidates["liquidity_score"]
        + 0.30 * candidates["sensitivity_score"]
        + 0.20 * candidates["stability_score"]
        + 0.20 * candidates["second_order_score"]
        - 0.25 * candidates["obviousness_penalty"]
        - 0.20 * candidates["anchor_correlation_penalty"]
    )
    candidates["selection_pool"] = np.select(
        [
            candidates["tier"].eq("first_order_anchor"),
            candidates["tier"].eq("second_order_economic"),
            candidates["tier"].eq("statistical_discovery"),
        ],
        ["anchor", "second_order", "discovery"],
        default="reject",
    )
    candidates["selection_reason"] = np.select(
        [
            candidates["tier"].eq("first_order_anchor"),
            candidates["tier"].eq("second_order_economic"),
            candidates["tier"].eq("statistical_discovery"),
        ],
        [
            "economic first-order anchor; capped in final universe",
            "economic second-order exposure",
            "statistical residual sensitivity discovery",
        ],
        default="no economic map and did not pass sensitivity discovery",
    )
    return candidates.sort_values(["commodity", "quarter", "universe_score"], ascending=[True, True, False]).reset_index(drop=True)


def classify_commodity_universe_tiers_from_paths(
    sensitivity_matrix_path: Path,
    broad_universe_path: Path,
    exposure_map_path: Path,
    beta_returns_path: Path,
    output_path: Path,
    commodity: str,
    min_abs_t: float = 2.0,
    anchor_corr_lookback_days: int = 252,
) -> pd.DataFrame:
    tiers = classify_commodity_universe_tiers(
        sensitivity_matrix=load_frame(sensitivity_matrix_path),
        broad_universe=load_frame(broad_universe_path),
        exposure_map=load_commodity_exposure_map(exposure_map_path),
        beta_returns=load_frame(beta_returns_path),
        commodity=commodity,
        min_abs_t=min_abs_t,
        anchor_corr_lookback_days=anchor_corr_lookback_days,
    )
    _write_frame(tiers, output_path)
    return tiers


def build_discovered_commodity_universe(
    tiers: pd.DataFrame,
    commodity: str,
    max_names: int = 60,
    max_anchor_share: float = 0.25,
    min_second_order: int = 10,
    min_discovery_score: float = 0.0,
) -> pd.DataFrame:
    commodity = commodity.upper().strip()
    df = tiers.copy()
    df = df[df["commodity"].astype(str).str.upper().eq(commodity)].copy()
    if df.empty:
        return df

    frames: list[pd.DataFrame] = []
    static_anchor_cap = max(1, int(round(max_names * max_anchor_share)))
    for quarter, group in df.groupby("quarter", sort=True):
        g = group.sort_values("universe_score", ascending=False).copy()
        second = g[g["selection_pool"].eq("second_order")]
        discovery = g[(g["selection_pool"].eq("discovery")) & (g["universe_score"] >= min_discovery_score)]
        non_anchor_available = len(second) + len(discovery)
        if non_anchor_available > 0 and max_anchor_share < 1.0:
            dynamic_anchor_cap = int(np.floor(non_anchor_available * max_anchor_share / (1.0 - max_anchor_share)))
            anchor_cap = max(0, min(static_anchor_cap, dynamic_anchor_cap))
        else:
            anchor_cap = static_anchor_cap
        anchors = g[g["selection_pool"].eq("anchor")].head(anchor_cap)

        selected = pd.concat([anchors, second.head(max(min_second_order, max_names))], ignore_index=True)
        remaining = max_names - len(selected)
        if remaining > 0:
            selected = pd.concat([selected, discovery.head(remaining)], ignore_index=True)
        if len(selected) < max_names:
            filler = g[
                g["selection_pool"].isin(["second_order", "discovery"])
                & ~g["ticker"].isin(selected["ticker"])
            ].head(max_names - len(selected))
            selected = pd.concat([selected, filler], ignore_index=True)

        selected = selected.drop_duplicates("ticker").sort_values("universe_score", ascending=False).head(max_names).copy()
        selected["selected"] = True
        selected["final_rank"] = np.arange(1, len(selected) + 1)
        frames.append(selected)

    if not frames:
        return pd.DataFrame()
    out = pd.concat(frames, ignore_index=True)
    out["is_tradeable"] = True
    out["inclusion_rule_version"] = "discovered_commodity_universe_v1"
    return out.sort_values(["commodity", "quarter", "final_rank"]).reset_index(drop=True)


def write_discovered_universe_files(universe: pd.DataFrame, output_dir: Path) -> list[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    if universe.empty:
        return written
    for (commodity, quarter), group in universe.groupby(["commodity", "quarter"], sort=True):
        commodity_dir = output_dir / str(commodity)
        commodity_dir.mkdir(parents=True, exist_ok=True)
        path = commodity_dir / f"{commodity}-Univ-{quarter}.csv"
        group.to_csv(path, index=False)
        written.append(path)
    return written


def build_discovered_commodity_universe_from_paths(
    tiers_path: Path,
    output_path: Path,
    output_dir: Path,
    commodity: str,
    max_names: int = 60,
    max_anchor_share: float = 0.25,
    min_second_order: int = 10,
    min_discovery_score: float = 0.0,
) -> pd.DataFrame:
    universe = build_discovered_commodity_universe(
        tiers=load_frame(tiers_path),
        commodity=commodity,
        max_names=max_names,
        max_anchor_share=max_anchor_share,
        min_second_order=min_second_order,
        min_discovery_score=min_discovery_score,
    )
    _write_frame(universe, output_path)
    write_discovered_universe_files(universe, output_dir)
    return universe


def audit_commodity_universe_from_paths(
    tiers_path: Path,
    selected_universe_path: Path,
    output_path: Path,
    commodity: str,
    quarter: str,
    max_rejected: int = 100,
) -> pd.DataFrame:
    commodity = commodity.upper().strip()
    tiers = load_frame(tiers_path)
    selected = load_frame(selected_universe_path)

    tiers = tiers[
        tiers["commodity"].astype(str).str.upper().eq(commodity)
        & tiers["quarter"].astype(str).eq(quarter)
    ].copy()
    if tiers.empty:
        raise ValueError(f"No tier rows found for {commodity} {quarter}")

    selected = selected[
        selected["commodity"].astype(str).str.upper().eq(commodity)
        & selected["quarter"].astype(str).eq(quarter)
    ].copy()
    selected_tickers = set(selected["ticker"].astype(str).str.upper())

    tiers["selected"] = tiers["ticker"].astype(str).str.upper().isin(selected_tickers)
    selected_rank = selected[["ticker", "final_rank"]].drop_duplicates("ticker") if "final_rank" in selected.columns else selected[["ticker"]]
    tiers = tiers.merge(selected_rank, on="ticker", how="left", suffixes=("", "_selected"))
    tiers["audit_status"] = np.where(tiers["selected"], "selected", "rejected")
    tiers["audit_reason"] = np.where(
        tiers["selected"],
        tiers["selection_reason"],
        np.select(
            [
                tiers["selection_pool"].eq("reject"),
                tiers["selection_pool"].eq("anchor"),
                tiers["selection_pool"].isin(["second_order", "discovery"]),
            ],
            [
                tiers["selection_reason"],
                "first-order anchor excluded by anchor cap or low score",
                "not high enough after score/cap ordering",
            ],
            default="not selected",
        ),
    )

    selected_rows = tiers[tiers["selected"]].copy()
    rejected_rows = tiers[~tiers["selected"]].sort_values("universe_score", ascending=False).head(max_rejected)
    audit = pd.concat([selected_rows, rejected_rows], ignore_index=True)
    keep = [
        "quarter",
        "asof_date",
        "commodity",
        "ticker",
        "audit_status",
        "final_rank",
        "selection_pool",
        "tier",
        "audit_reason",
        "universe_score",
        "liquidity_score",
        "sensitivity_score",
        "stability_score",
        "second_order_score",
        "obviousness_penalty",
        "anchor_correlation_penalty",
        "anchor_residual_corr",
        "adv_63d",
        "price",
        "exposure_role",
        "prior_weight",
        "feature",
        "feature_family",
        "horizon_days",
        "max_abs_t_stat",
        "sign_stability",
        "mean_beta_per_1z",
        "notes",
    ]
    audit = audit[[col for col in keep if col in audit.columns]].sort_values(
        ["audit_status", "final_rank", "universe_score"],
        ascending=[False, True, False],
    )
    _write_frame(audit, output_path)
    return audit.reset_index(drop=True)
