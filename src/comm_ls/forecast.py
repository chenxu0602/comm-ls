from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from comm_ls.reaction import load_frame
from comm_ls.universe import load_seed_universe


DEFAULT_FORECAST_HORIZONS = [1, 5, 10, 21]


def _category_for(feature: str) -> str:
    if feature.startswith(("volume", "oi", "price_volume", "price_oi")):
        return "participation"
    if (
        "realized_vol" in feature
        or feature.startswith("vol_")
        or "atr" in feature
        or "abs_ret" in feature
        or "large_move" in feature
    ):
        return "volatility"
    if (
        "regime" in feature
        or "backwardation" in feature
        or "contango" in feature
        or "term_structure" in feature
    ):
        return "term_structure_regime"
    if (
        "calendar_dec_log_ret" in feature
        or "next_jun_log_ret" in feature
        or "liquid_deferred_log_ret" in feature
    ):
        return "fixed_contract_return"
    if "carry" in feature or "spread" in feature:
        return "curve_carry"
    if "ret" in feature or "breakout" in feature or "drawdown" in feature or "up_days" in feature:
        return "price_momentum"
    return "other"


def _default_feature_columns(
    commodity_features: pd.DataFrame,
    include_prestandardized: bool,
    min_non_null: int,
) -> list[str]:
    excluded = {
        "date",
        "arrival",
        "symbol",
        "front_settle",
        "total_volume",
        "total_oi",
    }
    features: list[str] = []
    for col in commodity_features.columns:
        if col in excluded or col.endswith("_settle") or col.endswith("_contract") or col.endswith("_con"):
            continue
        if not include_prestandardized and col.endswith("_z_252d"):
            continue
        if pd.api.types.is_numeric_dtype(commodity_features[col]) and commodity_features[col].notna().sum() >= min_non_null:
            features.append(col)
    return features


def _forward_sum(series: pd.Series, horizon: int) -> pd.Series:
    shifted = series.shift(-1)
    return shifted.rolling(horizon, min_periods=horizon).sum().shift(-(horizon - 1))


def _map_features_to_signal_dates(
    commodity_features: pd.DataFrame,
    stock_dates: pd.Series,
    feature_columns: list[str],
) -> pd.DataFrame:
    stock_dates = pd.Series(pd.to_datetime(stock_dates, utc=False).sort_values().unique())
    signals = commodity_features[["date", "arrival", "symbol", *feature_columns]].copy()
    signals["date"] = pd.to_datetime(signals["date"], utc=False)
    signals["arrival"] = pd.to_datetime(signals["arrival"], utc=False)
    arrival_days = signals["arrival"].dt.normalize().to_numpy(dtype="datetime64[ns]")
    calendar = stock_dates.to_numpy(dtype="datetime64[ns]")
    indexer = np.searchsorted(calendar, arrival_days, side="left")
    valid = indexer < len(calendar)
    signals = signals.loc[valid].copy()
    signals["signal_date"] = pd.to_datetime(calendar[indexer[valid]])
    signals = signals.sort_values(["signal_date", "arrival", "date"])
    signals = signals.drop_duplicates("signal_date", keep="last")
    return signals


def _scan_feature_forecasts(
    panel: pd.DataFrame,
    ticker: str,
    commodity: str,
    feature_columns: list[str],
    horizons: list[int],
    samples: dict[str, tuple[pd.Timestamp | None, pd.Timestamp | None]],
    feature_z_window: int,
    min_feature_observations: int,
    min_observations: int,
) -> pd.DataFrame:
    z_features = pd.DataFrame({"signal_date": panel["signal_date"]})
    for feature in feature_columns:
        value = pd.to_numeric(panel[feature], errors="coerce")
        mean = value.rolling(feature_z_window, min_periods=min_feature_observations).mean()
        std = value.rolling(feature_z_window, min_periods=min_feature_observations).std()
        z_features[feature] = (value - mean) / std

    rows: list[dict[str, object]] = []
    for sample_name, (start_date, end_date) in samples.items():
        mask = pd.Series(True, index=panel.index)
        if start_date is not None:
            mask &= panel["signal_date"] >= start_date
        if end_date is not None:
            mask &= panel["signal_date"] <= end_date

        for feature in feature_columns:
            feature_name = feature
            x = z_features.loc[mask, feature]
            feature_non_null = int(pd.to_numeric(panel.loc[mask, feature], errors="coerce").notna().sum())

            for horizon in horizons:
                target = f"residual_return_fwd_{horizon}d"
                data = pd.DataFrame(
                    {
                        "signal_date": panel.loc[mask, "signal_date"],
                        "feature_z": x,
                        "target": pd.to_numeric(panel.loc[mask, target], errors="coerce"),
                    }
                )
                data = data.replace([np.inf, -np.inf], np.nan).dropna()
                observations = len(data)
                if observations < min_observations:
                    continue
                if data["feature_z"].std(ddof=1) == 0 or data["target"].std(ddof=1) == 0:
                    continue

                corr = data["feature_z"].corr(data["target"])
                if pd.isna(corr):
                    continue
                t_stat = corr * np.sqrt((observations - 2) / max(1e-12, 1.0 - corr * corr))
                beta_per_z = data["target"].cov(data["feature_z"]) / data["feature_z"].var()
                signed = np.sign(data["feature_z"]) * data["target"]
                q20 = data["feature_z"].quantile(0.2)
                q80 = data["feature_z"].quantile(0.8)
                low = data.loc[data["feature_z"] <= q20, "target"]
                high = data.loc[data["feature_z"] >= q80, "target"]

                rows.append(
                    {
                        "sample": sample_name,
                        "start_date": data["signal_date"].min(),
                        "end_date": data["signal_date"].max(),
                        "ticker": ticker,
                        "commodity": commodity,
                        "feature": feature_name,
                        "category": _category_for(feature_name),
                        "horizon_days": horizon,
                        "observations": observations,
                        "corr": corr,
                        "t_stat": t_stat,
                        "abs_t_stat": abs(t_stat),
                        "beta_per_1z": beta_per_z,
                        "mean_signed_return": signed.mean(),
                        "hit_rate": (signed > 0).mean(),
                        "top_bottom_quintile_spread": high.mean() - low.mean(),
                        "top_quintile_mean_return": high.mean(),
                        "bottom_quintile_mean_return": low.mean(),
                        "feature_non_null": feature_non_null,
                    }
                )

    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows)


def build_commodity_stock_forecast_study(
    commodity_features: pd.DataFrame,
    beta_returns: pd.DataFrame,
    commodity: str,
    tickers: list[str],
    features: list[str] | None = None,
    horizons: list[int] | None = None,
    sample_years: list[int] | None = None,
    feature_z_window: int = 252,
    min_feature_observations: int = 126,
    min_observations: int = 126,
    include_prestandardized: bool = False,
    include_annual: bool = False,
) -> pd.DataFrame:
    commodity = commodity.upper().strip()
    tickers = [ticker.upper().strip() for ticker in tickers]
    horizons = horizons or DEFAULT_FORECAST_HORIZONS
    sample_years = sample_years or [10, 5]

    signals = commodity_features.copy()
    signals["symbol"] = signals["symbol"].astype(str).str.upper().str.strip()
    signals = signals[signals["symbol"] == commodity].copy()
    if signals.empty:
        raise ValueError(f"No commodity features found for {commodity}")
    signals["date"] = pd.to_datetime(signals["date"], utc=False)
    signals["arrival"] = pd.to_datetime(signals["arrival"], utc=False)

    feature_columns = features or _default_feature_columns(
        signals,
        include_prestandardized=include_prestandardized,
        min_non_null=min_observations,
    )
    missing_features = sorted(set(feature_columns).difference(signals.columns))
    if missing_features:
        raise ValueError(f"Commodity features are missing columns: {missing_features}")

    stock = beta_returns.copy()
    stock["date"] = pd.to_datetime(stock["date"], utc=False)
    stock["ticker"] = stock["ticker"].astype(str).str.upper().str.strip()

    rows: list[pd.DataFrame] = []
    for ticker in tickers:
        s = stock[stock["ticker"] == ticker].sort_values("date").copy()
        if s.empty:
            continue
        for horizon in horizons:
            s[f"residual_return_fwd_{horizon}d"] = _forward_sum(s["residual_return"], horizon)

        aligned = _map_features_to_signal_dates(
            commodity_features=signals,
            stock_dates=s["date"],
            feature_columns=feature_columns,
        )
        panel = aligned.merge(
            s[["date", "ticker", "theme", "role", "region", *[f"residual_return_fwd_{h}d" for h in horizons]]],
            left_on="signal_date",
            right_on="date",
            how="inner",
        ).drop(columns=["date_y"])
        panel = panel.rename(columns={"date_x": "feature_date"}).sort_values("signal_date").reset_index(drop=True)
        if panel.empty:
            continue

        max_signal_date = panel["signal_date"].max()
        samples: dict[str, tuple[pd.Timestamp | None, pd.Timestamp | None]] = {"full_available": (None, None)}
        for years in sample_years:
            start = max_signal_date - pd.DateOffset(years=years)
            samples[f"last_{years}y"] = (start, None)
            if include_annual:
                for year in range(start.year, max_signal_date.year + 1):
                    year_start = max(pd.Timestamp(year=year, month=1, day=1), start)
                    year_end = min(pd.Timestamp(year=year, month=12, day=31), max_signal_date)
                    if year_start <= year_end:
                        samples[f"last_{years}y_year_{year}"] = (year_start, year_end)

        result = _scan_feature_forecasts(
            panel=panel,
            ticker=ticker,
            commodity=commodity,
            feature_columns=feature_columns,
            horizons=horizons,
            samples=samples,
            feature_z_window=feature_z_window,
            min_feature_observations=min_feature_observations,
            min_observations=min_observations,
        )
        if not result.empty:
            meta = s[["ticker", "theme", "role", "region"]].drop_duplicates("ticker")
            result = result.merge(meta, on="ticker", how="left")
            rows.append(result)

    if not rows:
        return pd.DataFrame()
    out = pd.concat(rows, ignore_index=True)
    return out.sort_values(
        ["sample", "ticker", "horizon_days", "abs_t_stat"],
        ascending=[True, True, True, False],
    ).reset_index(drop=True)


def build_commodity_stock_forecast_study_from_paths(
    commodity_signals_path: Path,
    beta_returns_path: Path,
    output_path: Path,
    commodity: str,
    tickers: list[str] | None = None,
    universe_path: Path | None = None,
    theme: str | None = None,
    features: list[str] | None = None,
    horizons: list[int] | None = None,
    sample_years: list[int] | None = None,
    feature_z_window: int = 252,
    min_feature_observations: int = 126,
    min_observations: int = 126,
    include_prestandardized: bool = False,
    include_annual: bool = False,
) -> pd.DataFrame:
    commodity_features = load_frame(commodity_signals_path)
    beta_returns = load_frame(beta_returns_path)

    selected_tickers = [ticker.upper().strip() for ticker in tickers] if tickers else []
    if theme is not None:
        if universe_path is None:
            raise ValueError("--universe is required when --theme is used")
        seed = load_seed_universe(universe_path)
        theme_tickers = (
            seed[seed["theme"].astype(str).str.lower() == theme.lower()]["ticker"].astype(str).str.upper().tolist()
        )
        selected_tickers.extend(theme_tickers)
    if not selected_tickers:
        raise ValueError("Provide at least one --ticker or --theme")
    selected_tickers = sorted(set(selected_tickers))

    result = build_commodity_stock_forecast_study(
        commodity_features=commodity_features,
        beta_returns=beta_returns,
        commodity=commodity,
        tickers=selected_tickers,
        features=features,
        horizons=horizons,
        sample_years=sample_years,
        feature_z_window=feature_z_window,
        min_feature_observations=min_feature_observations,
        min_observations=min_observations,
        include_prestandardized=include_prestandardized,
        include_annual=include_annual,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix == ".parquet":
        result.to_parquet(output_path, index=False)
    elif output_path.suffix == ".csv":
        result.to_csv(output_path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")
    return result
