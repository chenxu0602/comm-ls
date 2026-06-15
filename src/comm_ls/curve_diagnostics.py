from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from comm_ls.data_access import get_stock_feature_equity_curve, get_stock_feature_matrix


def covid_time_regime(date: pd.Timestamp | str) -> str:
    value = pd.Timestamp(date)
    if value < pd.Timestamp("2020-01-01"):
        return "pre_covid"
    if value < pd.Timestamp("2023-01-01"):
        return "covid_macro"
    return "post_covid"


def _max_drawdown(returns: pd.Series) -> float:
    if returns.empty:
        return np.nan
    equity = (1.0 + returns.fillna(0.0)).cumprod()
    peak = equity.cummax()
    return float((equity / peak - 1.0).min())


def _calmar_ratio(annualized_return: float, max_drawdown: float) -> float:
    if not np.isfinite(annualized_return) or not np.isfinite(max_drawdown) or max_drawdown >= 0:
        return np.nan
    return float(annualized_return / abs(max_drawdown))


def _curve_annual_summary(curve: pd.DataFrame) -> pd.DataFrame:
    if curve.empty:
        return pd.DataFrame()

    df = curve.copy()
    df["date"] = pd.to_datetime(df["date"], utc=False)
    df["year"] = df["date"].dt.year
    df["time_regime"] = df["date"].map(covid_time_regime)
    df["active_position"] = df["position"].fillna(0.0).ne(0.0)

    rows: list[dict[str, object]] = []
    for year, group in df.groupby("year", sort=True):
        returns = pd.to_numeric(group["strategy_return"], errors="coerce").fillna(0.0)
        active = group[group["active_position"]].copy()
        active_returns = pd.to_numeric(active["strategy_return"], errors="coerce").fillna(0.0)
        total_return = float((1.0 + returns).prod() - 1.0)
        max_drawdown = _max_drawdown(returns)
        rows.append(
            {
                "year": int(year),
                "time_regime": covid_time_regime(pd.Timestamp(year=int(year), month=12, day=31)),
                "trading_days": int(len(group)),
                "active_days": int(group["active_position"].sum()),
                "active_day_share": float(group["active_position"].mean()),
                "total_return": total_return,
                "annualized_return": total_return,
                "active_period_return": float((1.0 + active_returns).prod() - 1.0) if len(active) else 0.0,
                "mean_daily_return": float(returns.mean()),
                "daily_volatility": float(returns.std(ddof=0)),
                "hit_rate": float((active_returns > 0).mean()) if len(active) else np.nan,
                "calmar": _calmar_ratio(total_return, max_drawdown),
                "max_drawdown": max_drawdown,
                "mean_feature_z": float(pd.to_numeric(group["feature_z"], errors="coerce").mean()),
                "max_abs_feature_z": float(pd.to_numeric(group["feature_z"], errors="coerce").abs().max()),
            }
        )
    return pd.DataFrame(rows)


def _feature_regime(row: pd.Series) -> str:
    if not bool(row.get("active", False)):
        return "inactive"
    feature_z = row.get("feature_z")
    if pd.isna(feature_z):
        return "inactive"
    return "positive_trigger" if float(feature_z) > 0 else "negative_trigger"


def _curve_regime_summary(curve: pd.DataFrame) -> pd.DataFrame:
    if curve.empty:
        return pd.DataFrame()

    df = curve.copy()
    df["date"] = pd.to_datetime(df["date"], utc=False)
    df["year"] = df["date"].dt.year
    df["feature_regime"] = df.apply(_feature_regime, axis=1)
    rows: list[dict[str, object]] = []
    for (year, regime), group in df.groupby(["year", "feature_regime"], sort=True):
        returns = pd.to_numeric(group["strategy_return"], errors="coerce").fillna(0.0)
        rows.append(
            {
                "year": int(year),
                "feature_regime": regime,
                "days": int(len(group)),
                "total_return": float((1.0 + returns).prod() - 1.0),
                "mean_daily_return": float(returns.mean()),
                "hit_rate": float((returns > 0).mean()) if len(group) else np.nan,
                "mean_position": float(pd.to_numeric(group["position"], errors="coerce").fillna(0.0).mean()),
                "mean_feature_z": float(pd.to_numeric(group["feature_z"], errors="coerce").mean()),
            }
        )
    return pd.DataFrame(rows)


def _curve_time_regime_summary(curve: pd.DataFrame) -> pd.DataFrame:
    if curve.empty:
        return pd.DataFrame()

    df = curve.copy()
    df["date"] = pd.to_datetime(df["date"], utc=False)
    df["time_regime"] = df["date"].map(covid_time_regime)
    df["active_position"] = df["position"].fillna(0.0).ne(0.0)

    rows: list[dict[str, object]] = []
    for time_regime, group in df.groupby("time_regime", sort=False):
        returns = pd.to_numeric(group["strategy_return"], errors="coerce").fillna(0.0)
        active = group[group["active_position"]].copy()
        active_returns = pd.to_numeric(active["strategy_return"], errors="coerce").fillna(0.0)
        trading_days = int(len(group))
        total_return = float((1.0 + returns).prod() - 1.0)
        annualized_return = float((1.0 + total_return) ** (252 / trading_days) - 1.0) if trading_days else np.nan
        max_drawdown = _max_drawdown(returns)
        rows.append(
            {
                "time_regime": time_regime,
                "start_date": group["date"].min(),
                "end_date": group["date"].max(),
                "calendar_years": int(group["date"].dt.year.nunique()),
                "trading_days": trading_days,
                "active_days": int(group["active_position"].sum()),
                "active_day_share": float(group["active_position"].mean()),
                "total_return": total_return,
                "annualized_return": annualized_return,
                "active_period_return": float((1.0 + active_returns).prod() - 1.0) if len(active) else 0.0,
                "mean_daily_return": float(returns.mean()),
                "daily_volatility": float(returns.std(ddof=0)),
                "hit_rate": float((active_returns > 0).mean()) if len(active) else np.nan,
                "calmar": _calmar_ratio(annualized_return, max_drawdown),
                "max_drawdown": max_drawdown,
                "mean_position": float(pd.to_numeric(group["position"], errors="coerce").fillna(0.0).mean()),
                "mean_feature_z": float(pd.to_numeric(group["feature_z"], errors="coerce").mean()),
                "max_abs_feature_z": float(pd.to_numeric(group["feature_z"], errors="coerce").abs().max()),
            }
        )
    order = {"pre_covid": 0, "covid_macro": 1, "post_covid": 2}
    out = pd.DataFrame(rows)
    return out.sort_values("time_regime", key=lambda values: values.map(order)).reset_index(drop=True)


def _annual_regime_stats(group: pd.DataFrame) -> dict[str, float | int]:
    if group.empty:
        return {
            "years": 0,
            "active_years": 0,
            "median_return": np.nan,
            "mean_return": np.nan,
            "active_median_return": np.nan,
            "active_mean_return": np.nan,
            "positive_year_share": np.nan,
            "active_positive_year_share": np.nan,
            "compounded_return": np.nan,
        }

    returns = pd.to_numeric(group["total_return"], errors="coerce")
    active_group = group[pd.to_numeric(group["active_days"], errors="coerce").fillna(0) > 0]
    active_returns = pd.to_numeric(active_group["total_return"], errors="coerce")
    return {
        "years": int(group["year"].nunique()),
        "active_years": int(active_group["year"].nunique()),
        "median_return": float(returns.median()),
        "mean_return": float(returns.mean()),
        "active_median_return": float(active_returns.median()) if not active_group.empty else np.nan,
        "active_mean_return": float(active_returns.mean()) if not active_group.empty else np.nan,
        "positive_year_share": float((returns > 0).mean()),
        "active_positive_year_share": float((active_returns > 0).mean()) if not active_group.empty else np.nan,
        "compounded_return": float((1.0 + returns.fillna(0.0)).prod() - 1.0),
    }


def summarize_stock_feature_curve(
    ticker: str,
    commodity: str,
    feature: str,
    matrix_path: Path | str,
    as_of_date: str,
    start: str | None = "2016-01-01",
    end: str | None = None,
    return_column: str = "residual_return",
    activation_z: float = 1.0,
    position_mode: str = "sign",
    transaction_cost_bps: float = 0.0,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    curve = get_stock_feature_equity_curve(
        ticker=ticker,
        commodity=commodity,
        feature=feature,
        matrix_path=matrix_path,
        as_of_date=as_of_date,
        start=start,
        end=end,
        return_column=return_column,
        activation_z=activation_z,
        position_mode=position_mode,
        transaction_cost_bps=transaction_cost_bps,
        date_as_index=False,
    )
    annual = _curve_annual_summary(curve)
    regime = _curve_regime_summary(curve)
    meta_cols = {
        "ticker": ticker.upper().strip(),
        "commodity": commodity.upper().strip(),
        "feature": feature.strip(),
        "as_of_date": pd.Timestamp(as_of_date),
        "return_column": return_column,
        "activation_z": activation_z,
        "position_mode": position_mode,
        "transaction_cost_bps": transaction_cost_bps,
    }
    for key, value in meta_cols.items():
        annual.insert(0, key, value)
        regime.insert(0, key, value)
    return annual, regime


def summarize_stock_feature_curve_time_regime(
    ticker: str,
    commodity: str,
    feature: str,
    matrix_path: Path | str,
    as_of_date: str,
    start: str | None = "2010-01-01",
    end: str | None = None,
    return_column: str = "residual_return",
    activation_z: float = 1.0,
    position_mode: str = "sign",
    transaction_cost_bps: float = 0.0,
) -> pd.DataFrame:
    curve = get_stock_feature_equity_curve(
        ticker=ticker,
        commodity=commodity,
        feature=feature,
        matrix_path=matrix_path,
        as_of_date=as_of_date,
        start=start,
        end=end,
        return_column=return_column,
        activation_z=activation_z,
        position_mode=position_mode,
        transaction_cost_bps=transaction_cost_bps,
        date_as_index=False,
    )
    time_regime = _curve_time_regime_summary(curve)
    meta_cols = {
        "ticker": ticker.upper().strip(),
        "commodity": commodity.upper().strip(),
        "feature": feature.strip(),
        "as_of_date": pd.Timestamp(as_of_date),
        "return_column": return_column,
        "activation_z": activation_z,
        "position_mode": position_mode,
        "transaction_cost_bps": transaction_cost_bps,
    }
    for key, value in meta_cols.items():
        time_regime.insert(0, key, value)
    return time_regime


def build_matrix_curve_diagnostics(
    matrix_path: Path | str,
    as_of_date: str,
    ticker: str | None = None,
    commodity: str | None = None,
    feature: str | None = None,
    start: str | None = "2016-01-01",
    end: str | None = None,
    return_column: str = "residual_return",
    activation_z: float = 1.0,
    position_mode: str = "sign",
    transaction_cost_bps: float = 0.0,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    matrix = get_stock_feature_matrix(
        ticker=ticker,
        commodity=commodity,
        feature=feature,
        matrix_path=matrix_path,
        as_of_date=as_of_date,
    )
    annual_frames: list[pd.DataFrame] = []
    regime_frames: list[pd.DataFrame] = []
    time_regime_frames: list[pd.DataFrame] = []
    for row in matrix.itertuples(index=False):
        annual, regime = summarize_stock_feature_curve(
            ticker=row.ticker,
            commodity=row.commodity,
            feature=row.feature,
            matrix_path=matrix_path,
            as_of_date=as_of_date,
            start=start,
            end=end,
            return_column=return_column,
            activation_z=activation_z,
            position_mode=position_mode,
            transaction_cost_bps=transaction_cost_bps,
        )
        time_regime = summarize_stock_feature_curve_time_regime(
            ticker=row.ticker,
            commodity=row.commodity,
            feature=row.feature,
            matrix_path=matrix_path,
            as_of_date=as_of_date,
            start=start,
            end=end,
            return_column=return_column,
            activation_z=activation_z,
            position_mode=position_mode,
            transaction_cost_bps=transaction_cost_bps,
        )
        for col in ["theme", "role", "feature_family", "direction", "confidence", "preferred_horizon"]:
            if hasattr(row, col):
                annual[col] = getattr(row, col)
                regime[col] = getattr(row, col)
                time_regime[col] = getattr(row, col)
        annual_frames.append(annual)
        regime_frames.append(regime)
        time_regime_frames.append(time_regime)

    annual_out = pd.concat(annual_frames, ignore_index=True) if annual_frames else pd.DataFrame()
    regime_out = pd.concat(regime_frames, ignore_index=True) if regime_frames else pd.DataFrame()
    time_regime_out = pd.concat(time_regime_frames, ignore_index=True) if time_regime_frames else pd.DataFrame()
    return annual_out, regime_out, time_regime_out


def build_curve_stability_summary(annual: pd.DataFrame) -> pd.DataFrame:
    if annual.empty:
        return annual.copy()

    df = annual.copy()
    key_cols = ["ticker", "commodity", "feature"]
    optional_cols = ["theme", "role", "feature_family", "direction", "confidence", "preferred_horizon"]
    group_cols = key_cols + [col for col in optional_cols if col in df.columns]
    rows: list[dict[str, object]] = []
    for key, group in df.groupby(group_cols, dropna=False, sort=True):
        record = dict(zip(group_cols, key if isinstance(key, tuple) else (key,), strict=False))
        returns = pd.to_numeric(group["total_return"], errors="coerce")
        active_days = pd.to_numeric(group["active_days"], errors="coerce")
        pre = group[group["time_regime"] == "pre_covid"] if "time_regime" in group.columns else group[group["year"] < 2020]
        crisis = group[group["year"].between(2020, 2022)]
        post = group[group["year"] >= 2023]
        pre_stats = _annual_regime_stats(pre)
        crisis_stats = _annual_regime_stats(crisis)
        post_stats = _annual_regime_stats(post)
        pre_median = pre_stats["median_return"]
        crisis_median = crisis_stats["median_return"]
        post_median = post_stats["median_return"]
        pre_active_median = pre_stats["active_median_return"]
        crisis_active_median = crisis_stats["active_median_return"]
        post_active_median = post_stats["active_median_return"]
        record.update(
            {
                "annual_years": int(group["year"].nunique()),
                "active_years": int((active_days > 0).sum()),
                "positive_years": int((returns > 0).sum()),
                "positive_year_share": float((returns > 0).mean()),
                "median_annual_return": float(returns.median()),
                "mean_annual_return": float(returns.mean()),
                "worst_annual_return": float(returns.min()),
                "best_annual_return": float(returns.max()),
                "bad_years_lt_minus5pct": int((returns < -0.05).sum()),
                "pre_covid_years": pre_stats["years"],
                "pre_covid_active_years": pre_stats["active_years"],
                "pre_covid_median_return": pre_median,
                "pre_covid_mean_return": pre_stats["mean_return"],
                "pre_covid_active_median_return": pre_active_median,
                "pre_covid_active_mean_return": pre_stats["active_mean_return"],
                "pre_covid_compounded_return": pre_stats["compounded_return"],
                "pre_covid_positive_year_share": pre_stats["positive_year_share"],
                "pre_covid_active_positive_year_share": pre_stats["active_positive_year_share"],
                "covid_macro_years": crisis_stats["years"],
                "covid_macro_active_years": crisis_stats["active_years"],
                "covid_macro_median_return": crisis_median,
                "covid_macro_mean_return": crisis_stats["mean_return"],
                "covid_macro_active_median_return": crisis_active_median,
                "covid_macro_active_mean_return": crisis_stats["active_mean_return"],
                "covid_macro_compounded_return": crisis_stats["compounded_return"],
                "covid_macro_positive_year_share": crisis_stats["positive_year_share"],
                "covid_macro_active_positive_year_share": crisis_stats["active_positive_year_share"],
                "post_covid_years": post_stats["years"],
                "post_covid_active_years": post_stats["active_years"],
                "post_covid_median_return": post_median,
                "post_covid_mean_return": post_stats["mean_return"],
                "post_covid_active_median_return": post_active_median,
                "post_covid_active_mean_return": post_stats["active_mean_return"],
                "post_covid_compounded_return": post_stats["compounded_return"],
                "post_covid_positive_year_share": post_stats["positive_year_share"],
                "post_covid_active_positive_year_share": post_stats["active_positive_year_share"],
                "crisis_2020_2022_median_return": crisis_median,
                "post_2023_median_return": post_median,
                "median_active_day_share": float(pd.to_numeric(group["active_day_share"], errors="coerce").median()),
            }
        )
        pre_signal_return = pre_active_median if pd.notna(pre_active_median) else pre_median
        crisis_signal_return = crisis_active_median if pd.notna(crisis_active_median) else crisis_median
        post_signal_return = post_active_median if pd.notna(post_active_median) else post_median
        record["pre_post_same_direction"] = (
            bool(np.sign(pre_signal_return) == np.sign(post_signal_return))
            if pd.notna(pre_signal_return) and pd.notna(post_signal_return)
            else False
        )
        record["time_regime_verdict"] = _time_regime_verdict(
            float(pre_signal_return) if pd.notna(pre_signal_return) else np.nan,
            float(crisis_signal_return) if pd.notna(crisis_signal_return) else np.nan,
            float(post_signal_return) if pd.notna(post_signal_return) else np.nan,
        )
        rows.append(record)

    out = pd.DataFrame(rows)
    out["stability_verdict"] = np.select(
        [
            (out["positive_year_share"] >= 0.6)
            & (out["median_annual_return"] > 0)
            & (out["bad_years_lt_minus5pct"] <= 3),
            (out["post_2023_median_return"] > 0)
            & (out["crisis_2020_2022_median_return"] <= 0),
        ],
        ["stable_candidate", "post_2023_regime_only"],
        default="review",
    )
    return out.sort_values(
        ["time_regime_verdict", "stability_verdict", "positive_year_share", "median_annual_return"],
        ascending=[True, True, False, False],
    ).reset_index(drop=True)


def _time_regime_verdict(pre_median: float, crisis_median: float, post_median: float) -> str:
    has_pre = pd.notna(pre_median)
    has_covid = pd.notna(crisis_median)
    has_post = pd.notna(post_median)
    if has_pre and has_covid and has_post and pre_median > 0 and crisis_median > 0 and post_median > 0:
        return "positive_all_regimes"
    if has_pre and has_post and pre_median > 0 and post_median > 0 and (not has_covid or crisis_median <= 0):
        return "pre_post_positive_covid_weak"
    if has_pre and has_post and np.sign(pre_median) != np.sign(post_median):
        return "structural_break_review"
    if has_post and post_median > 0 and (not has_pre or pre_median <= 0):
        return "post_covid_only"
    return "review"


def write_frame(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix == ".parquet":
        df.to_parquet(output_path, index=False)
    elif output_path.suffix == ".csv":
        df.to_csv(output_path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")


def build_matrix_curve_diagnostics_from_paths(
    matrix_path: Path,
    as_of_date: str,
    output_annual_path: Path,
    output_regime_path: Path,
    output_summary_path: Path | None = None,
    output_time_regime_path: Path | None = None,
    ticker: str | None = None,
    commodity: str | None = None,
    feature: str | None = None,
    start: str | None = "2016-01-01",
    end: str | None = None,
    return_column: str = "residual_return",
    activation_z: float = 1.0,
    position_mode: str = "sign",
    transaction_cost_bps: float = 0.0,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    annual, regime, time_regime = build_matrix_curve_diagnostics(
        matrix_path=matrix_path,
        as_of_date=as_of_date,
        ticker=ticker,
        commodity=commodity,
        feature=feature,
        start=start,
        end=end,
        return_column=return_column,
        activation_z=activation_z,
        position_mode=position_mode,
        transaction_cost_bps=transaction_cost_bps,
    )
    summary = build_curve_stability_summary(annual)
    write_frame(annual, output_annual_path)
    write_frame(regime, output_regime_path)
    if output_time_regime_path is not None:
        write_frame(time_regime, output_time_regime_path)
    if output_summary_path is not None:
        write_frame(summary, output_summary_path)
    return annual, regime, time_regime, summary
