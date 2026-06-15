from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from comm_ls.data_access import (
    DEFAULT_COMMODITY_SIGNALS,
    DEFAULT_EQUITY_BETA_RETURNS,
    _read_frame,
    get_stock_feature_equity_curve,
    get_stock_feature_matrix,
)
from comm_ls.environment import commodity_environment_similarity
from comm_ls.event_regime import add_event_regime


DEFAULT_RESEARCH_COMMODITIES = ["CL", "HG"]


def _read_optional_frame(path: Path | None) -> pd.DataFrame:
    if path is None or not path.exists():
        return pd.DataFrame()
    return _read_frame(path)


def _write_frame(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix == ".parquet":
        df.to_parquet(output_path, index=False)
    elif output_path.suffix == ".csv":
        df.to_csv(output_path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")


def _candidate_priority(row: pd.Series) -> float:
    stability_score = {
        "stable_candidate": 1.0,
        "post_2023_regime_only": 0.65,
        "review": 0.35,
    }.get(str(row.get("stability_verdict")), 0.35)
    regime_score = {
        "positive_all_regimes": 1.0,
        "pre_post_positive_covid_weak": 0.85,
        "post_covid_only": 0.65,
        "structural_break_review": 0.45,
        "review": 0.25,
    }.get(str(row.get("time_regime_verdict")), 0.25)
    confidence_score = {
        "high": 1.0,
        "medium": 0.8,
        "low": 0.55,
    }.get(str(row.get("confidence")).lower(), 0.55)
    post_return = pd.to_numeric(pd.Series([row.get("post_covid_active_median_return")]), errors="coerce").iloc[0]
    post_bonus = min(max(float(post_return) if pd.notna(post_return) else 0.0, 0.0), 0.25)
    return float(0.35 * stability_score + 0.30 * regime_score + 0.20 * confidence_score + post_bonus)


def _gate_candidate(row: pd.Series) -> tuple[bool, str]:
    closest = str(row.get("closest_time_regime", "")).strip()
    stability = str(row.get("stability_verdict", "")).strip()
    regime = str(row.get("time_regime_verdict", "")).strip()
    post_active = pd.to_numeric(pd.Series([row.get("post_covid_active_median_return")]), errors="coerce").iloc[0]
    covid_active = pd.to_numeric(pd.Series([row.get("covid_macro_active_median_return")]), errors="coerce").iloc[0]

    if stability == "stable_candidate" or regime == "positive_all_regimes":
        return True, "stable_or_all_regime"
    if regime == "pre_post_positive_covid_weak":
        if closest == "covid_macro" and pd.notna(covid_active) and covid_active <= 0:
            return False, "blocked_by_covid_weak_regime"
        return True, "pre_post_positive"
    if regime in {"post_covid_only", "structural_break_review"}:
        if closest == "post_covid" and pd.notna(post_active) and post_active > 0:
            return True, "post_covid_environment_match"
        return False, "requires_post_covid_environment"
    return False, "insufficient_regime_support"


def build_feature_trade_candidates(
    matrix: pd.DataFrame,
    stability_summary: pd.DataFrame,
    environment_summary: pd.DataFrame,
    commodities: list[str] | None = None,
    max_per_commodity: int = 12,
    max_per_theme: int = 4,
    min_post_covid_active_median_return: float = 0.0,
    themes: list[str] | None = None,
) -> pd.DataFrame:
    if matrix.empty or stability_summary.empty:
        return pd.DataFrame()

    keep_commodities = {symbol.upper().strip() for symbol in (commodities or DEFAULT_RESEARCH_COMMODITIES)}
    matrix_data = matrix.copy()
    matrix_data["ticker"] = matrix_data["ticker"].astype(str).str.upper().str.strip()
    matrix_data["commodity"] = matrix_data["commodity"].astype(str).str.upper().str.strip()
    matrix_data["feature"] = matrix_data["feature"].astype(str).str.strip()
    matrix_data = matrix_data[matrix_data["commodity"].isin(keep_commodities)].copy()
    if themes is not None:
        keep_themes = {theme.strip() for theme in themes}
        matrix_data = matrix_data[matrix_data["theme"].astype(str).isin(keep_themes)].copy()

    stability = stability_summary.copy()
    stability["ticker"] = stability["ticker"].astype(str).str.upper().str.strip()
    stability["commodity"] = stability["commodity"].astype(str).str.upper().str.strip()
    stability["feature"] = stability["feature"].astype(str).str.strip()
    stability = stability[stability["commodity"].isin(keep_commodities)].copy()

    merged = matrix_data.merge(
        stability,
        on=["ticker", "commodity", "feature"],
        how="inner",
        suffixes=("", "_stability"),
    )
    if merged.empty:
        return merged

    env = environment_summary.copy()
    if not env.empty:
        env["symbol"] = env["symbol"].astype(str).str.upper().str.strip()
        closest = env[env["closest_regime"].astype(bool)].copy()
        closest = closest.rename(
            columns={
                "symbol": "commodity",
                "time_regime": "closest_time_regime",
                "cosine_similarity": "environment_similarity",
                "euclidean_distance": "environment_distance",
            }
        )
        merged = merged.merge(
            closest[
                [
                    "commodity",
                    "closest_time_regime",
                    "environment_similarity",
                    "environment_distance",
                    "current_start_date",
                    "current_end_date",
                ]
            ],
            on="commodity",
            how="left",
        )
    else:
        merged["closest_time_regime"] = np.nan
        merged["environment_similarity"] = np.nan
        merged["environment_distance"] = np.nan

    merged["candidate_priority"] = merged.apply(_candidate_priority, axis=1)
    gates = merged.apply(_gate_candidate, axis=1, result_type="expand")
    merged["eligible"] = gates[0].astype(bool)
    merged["gate_reason"] = gates[1]

    post_active = pd.to_numeric(merged["post_covid_active_median_return"], errors="coerce")
    merged = merged[(post_active.isna()) | (post_active >= min_post_covid_active_median_return)].copy()
    merged = merged.sort_values(
        ["eligible", "commodity", "candidate_priority", "positive_year_share", "post_covid_active_median_return"],
        ascending=[False, True, False, False, False],
    )

    capped_frames: list[pd.DataFrame] = []
    for commodity, group in merged.groupby("commodity", sort=True):
        selected: list[pd.DataFrame] = []
        theme_counts: dict[str, int] = {}
        for _, row in group.iterrows():
            theme = str(row.get("theme", "unknown"))
            if theme_counts.get(theme, 0) >= max_per_theme:
                continue
            selected.append(row.to_frame().T)
            theme_counts[theme] = theme_counts.get(theme, 0) + 1
            if len(selected) >= max_per_commodity:
                break
        if selected:
            capped_frames.append(pd.concat(selected, ignore_index=True))

    if not capped_frames:
        return merged.iloc[0:0].copy()
    return pd.concat(capped_frames, ignore_index=True).reset_index(drop=True)


def build_feature_trade_candidates_from_paths(
    matrix_path: Path,
    stability_summary_paths: list[Path],
    output_path: Path,
    as_of_date: str,
    commodities: list[str] | None = None,
    commodity_signals_path: Path = DEFAULT_COMMODITY_SIGNALS,
    environment_start: str = "2010-01-01",
    environment_window_days: int = 63,
    max_per_commodity: int = 12,
    max_per_theme: int = 4,
    min_post_covid_active_median_return: float = 0.0,
    themes: list[str] | None = None,
) -> pd.DataFrame:
    commodity_list = commodities or DEFAULT_RESEARCH_COMMODITIES
    matrix = get_stock_feature_matrix(
        matrix_path=matrix_path,
        as_of_date=as_of_date,
    )
    stability_frames = [_read_optional_frame(path) for path in stability_summary_paths]
    stability = pd.concat([frame for frame in stability_frames if not frame.empty], ignore_index=True)

    env_frames: list[pd.DataFrame] = []
    for symbol in commodity_list:
        env_summary, _ = commodity_environment_similarity(
            symbol=symbol,
            commodity_signals_path=commodity_signals_path,
            as_of_date=as_of_date,
            start=environment_start,
            current_window_days=environment_window_days,
        )
        env_frames.append(env_summary)
    environment_summary = pd.concat(env_frames, ignore_index=True) if env_frames else pd.DataFrame()

    candidates = build_feature_trade_candidates(
        matrix=matrix,
        stability_summary=stability,
        environment_summary=environment_summary,
        commodities=commodity_list,
        max_per_commodity=max_per_commodity,
        max_per_theme=max_per_theme,
        min_post_covid_active_median_return=min_post_covid_active_median_return,
        themes=themes,
    )
    _write_frame(candidates, output_path)
    return candidates


def _summary_metrics(daily: pd.DataFrame) -> dict[str, object]:
    if daily.empty:
        return {
            "start_date": pd.NaT,
            "end_date": pd.NaT,
            "trading_days": 0,
            "total_return": np.nan,
            "annualized_return": np.nan,
            "gross_annualized_return": np.nan,
            "annualized_volatility": np.nan,
            "sharpe": np.nan,
            "calmar": np.nan,
            "max_drawdown": np.nan,
            "average_active_pairs": np.nan,
            "average_gross_exposure": np.nan,
            "annualized_turnover": np.nan,
            "cost_drag_total": np.nan,
        }
    n_days = len(daily)
    returns = pd.to_numeric(daily["net_return"], errors="coerce").fillna(0.0)
    gross = pd.to_numeric(daily["gross_return"], errors="coerce").fillna(0.0)
    equity = (1.0 + returns).cumprod()
    total_return = float(equity.iloc[-1] - 1.0)
    annualized_return = float(equity.iloc[-1] ** (252 / n_days) - 1.0) if n_days else np.nan
    annualized_vol = float(returns.std(ddof=0) * np.sqrt(252)) if n_days else np.nan
    gross_annualized_return = float((1.0 + gross).cumprod().iloc[-1] ** (252 / n_days) - 1.0) if n_days else np.nan
    drawdown = equity / equity.cummax() - 1.0
    max_drawdown = float(drawdown.min())
    sharpe = annualized_return / annualized_vol if annualized_vol and not np.isnan(annualized_vol) else np.nan
    calmar = (
        annualized_return / abs(max_drawdown)
        if np.isfinite(annualized_return) and np.isfinite(max_drawdown) and max_drawdown < 0
        else np.nan
    )
    return {
        "start_date": daily["date"].min(),
        "end_date": daily["date"].max(),
        "trading_days": n_days,
        "total_return": total_return,
        "annualized_return": annualized_return,
        "gross_annualized_return": gross_annualized_return,
        "annualized_volatility": annualized_vol,
        "sharpe": sharpe,
        "calmar": calmar,
        "max_drawdown": max_drawdown,
        "average_active_pairs": float(daily["active_pairs"].mean()),
        "average_gross_exposure": float(daily["gross_exposure"].mean()),
        "annualized_turnover": float(daily["turnover"].mean() * 252),
        "cost_drag_total": float(daily["transaction_cost"].sum()),
    }


def _performance_summary(daily: pd.DataFrame, weights: pd.DataFrame, label: str) -> pd.DataFrame:
    if daily.empty:
        return pd.DataFrame()
    active_weights = weights[weights["abs_weight"] > 0].copy() if not weights.empty else pd.DataFrame()
    metrics = _summary_metrics(daily)
    non_event_daily = daily[daily["event_regime"].eq("none")].copy() if "event_regime" in daily.columns else daily.copy()
    non_event_metrics = _summary_metrics(non_event_daily)
    hormuz_daily = (
        daily[daily["event_regime"].eq("hormuz_crisis")].copy()
        if "event_regime" in daily.columns
        else daily.iloc[0:0].copy()
    )
    hormuz_metrics = _summary_metrics(hormuz_daily)
    return pd.DataFrame(
        [
            {
                "label": label,
                **metrics,
                "exclude_event_trading_days": non_event_metrics["trading_days"],
                "exclude_event_total_return": non_event_metrics["total_return"],
                "exclude_event_annualized_return": non_event_metrics["annualized_return"],
                "exclude_event_annualized_volatility": non_event_metrics["annualized_volatility"],
                "exclude_event_sharpe": non_event_metrics["sharpe"],
                "exclude_event_calmar": non_event_metrics["calmar"],
                "exclude_event_max_drawdown": non_event_metrics["max_drawdown"],
                "hormuz_trading_days": hormuz_metrics["trading_days"],
                "hormuz_total_return": hormuz_metrics["total_return"],
                "hormuz_mean_daily_return": float(
                    pd.to_numeric(hormuz_daily["net_return"], errors="coerce").fillna(0.0).mean()
                )
                if not hormuz_daily.empty
                else np.nan,
                "candidate_count": int(weights[["ticker", "commodity", "feature"]].drop_duplicates().shape[0])
                if not weights.empty
                else 0,
                "active_candidate_count": int(active_weights[["ticker", "commodity", "feature"]].drop_duplicates().shape[0])
                if not active_weights.empty
                else 0,
            }
        ]
    )


def _apply_position_hysteresis(
    curve: pd.DataFrame,
    activation_z: float,
    exit_z: float | None,
    position_lag_days: int = 1,
) -> pd.DataFrame:
    if exit_z is None or exit_z >= activation_z:
        return curve

    out = curve.sort_values("date").copy()
    feature_z = pd.to_numeric(out["feature_z"], errors="coerce")
    raw_signal = pd.to_numeric(out["raw_signal"], errors="coerce")
    state = 0.0
    desired: list[float] = []
    for z_value, signal_value in zip(feature_z, raw_signal, strict=False):
        if pd.isna(z_value) or pd.isna(signal_value):
            state = 0.0
        elif state == 0.0 and abs(float(z_value)) >= activation_z:
            state = float(np.sign(signal_value))
        elif state != 0.0 and abs(float(z_value)) < exit_z:
            state = 0.0
        desired.append(state)

    out["desired_position"] = desired
    out["active"] = out["desired_position"] != 0.0
    out["position"] = pd.Series(desired, index=out.index).shift(position_lag_days).fillna(0.0)
    return out


def _is_rebalance_date(date: pd.Timestamp, previous_date: pd.Timestamp | None, frequency: str) -> bool:
    if previous_date is None or frequency == "daily":
        return True
    if frequency == "weekly":
        return date.to_period("W") != previous_date.to_period("W")
    if frequency == "monthly":
        return date.to_period("M") != previous_date.to_period("M")
    raise ValueError("rebalance_frequency must be 'daily', 'weekly', or 'monthly'")


def _allocate_base_weights(active: pd.DataFrame, target_gross: float, max_pair_weight: float) -> pd.Series:
    if active.empty:
        return pd.Series(dtype=float)
    raw = pd.to_numeric(active["candidate_priority"], errors="coerce").fillna(1.0).clip(lower=0.05)
    raw = raw / raw.sum() * target_gross
    return raw.clip(upper=max_pair_weight)


def run_feature_basket_backtest(
    candidates: pd.DataFrame,
    matrix_path: Path | str,
    as_of_date: str,
    commodity_signals_path: Path | str = DEFAULT_COMMODITY_SIGNALS,
    beta_returns_path: Path | str = DEFAULT_EQUITY_BETA_RETURNS,
    start: str | None = "2010-01-01",
    end: str | None = None,
    return_column: str = "residual_return",
    activation_z: float = 1.0,
    exit_z: float | None = None,
    position_mode: str = "sign",
    transaction_cost_bps: float = 10.0,
    max_pair_weight: float = 0.12,
    target_gross: float = 1.0,
    rebalance_frequency: str = "daily",
    eligible_only: bool = True,
    label: str = "feature_basket",
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    if candidates.empty:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    rows = candidates.copy()
    rows["ticker"] = rows["ticker"].astype(str).str.upper().str.strip()
    rows["commodity"] = rows["commodity"].astype(str).str.upper().str.strip()
    rows["feature"] = rows["feature"].astype(str).str.strip()
    if eligible_only and "eligible" in rows.columns:
        rows = rows[rows["eligible"].astype(bool)].copy()
    if rows.empty:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    curve_frames: list[pd.DataFrame] = []
    for row in rows.itertuples(index=False):
        try:
            curve = get_stock_feature_equity_curve(
                ticker=row.ticker,
                commodity=row.commodity,
                feature=row.feature,
                matrix_path=matrix_path,
                commodity_signals_path=commodity_signals_path,
                beta_returns_path=beta_returns_path,
                as_of_date=as_of_date,
                return_column=return_column,
                activation_z=activation_z,
                position_mode=position_mode,
                transaction_cost_bps=0.0,
                start=start,
                end=end,
                date_as_index=False,
            )
        except (KeyError, FileNotFoundError, ValueError):
            continue
        if curve.empty:
            continue
        curve = _apply_position_hysteresis(curve, activation_z=activation_z, exit_z=exit_z)
        curve = curve.copy()
        curve["candidate_priority"] = float(getattr(row, "candidate_priority", 1.0))
        curve["theme"] = getattr(row, "theme", None)
        curve["role"] = getattr(row, "role", None)
        curve["stability_verdict"] = getattr(row, "stability_verdict", None)
        curve["time_regime_verdict"] = getattr(row, "time_regime_verdict", None)
        curve_frames.append(curve)

    if not curve_frames:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    curves = pd.concat(curve_frames, ignore_index=True)
    curves["date"] = pd.to_datetime(curves["date"], utc=False)
    curves["pair_id"] = curves["ticker"] + "/" + curves["commodity"] + "/" + curves["feature"]
    curves["position"] = pd.to_numeric(curves["position"], errors="coerce").fillna(0.0)
    curves[return_column] = pd.to_numeric(curves[return_column], errors="coerce").fillna(0.0)
    curves["active_pair"] = curves["position"].ne(0.0)

    weighted_frames: list[pd.DataFrame] = []
    base_weights: dict[str, float] = {}
    previous_date: pd.Timestamp | None = None
    for date, group in curves.groupby("date", sort=True):
        g = group.copy()
        active = g["active_pair"]
        if _is_rebalance_date(pd.Timestamp(date), previous_date, rebalance_frequency):
            allocated = _allocate_base_weights(g[active], target_gross=target_gross, max_pair_weight=max_pair_weight)
            base_weights = {
                str(pair_id): float(weight)
                for pair_id, weight in zip(g.loc[active, "pair_id"], allocated, strict=False)
            }
        else:
            for pair_id in g.loc[~active, "pair_id"].astype(str):
                base_weights[pair_id] = 0.0

        g["base_weight"] = g["pair_id"].map(base_weights).fillna(0.0)
        g["effective_weight"] = g["base_weight"] * g["position"]
        weighted_frames.append(g)
        previous_date = pd.Timestamp(date)

    weights = pd.concat(weighted_frames, ignore_index=True).sort_values(["pair_id", "date"]).reset_index(drop=True)
    weights["previous_effective_weight"] = weights.groupby("pair_id")["effective_weight"].shift().fillna(0.0)
    weights["turnover"] = (weights["effective_weight"] - weights["previous_effective_weight"]).abs()
    weights["abs_weight"] = weights["effective_weight"].abs()
    weights["gross_return"] = weights["effective_weight"] * weights[return_column]
    weights["transaction_cost"] = weights["turnover"] * transaction_cost_bps / 10_000.0
    weights["net_return"] = weights["gross_return"] - weights["transaction_cost"]

    daily = (
        weights.groupby("date", sort=True)
        .agg(
            gross_return=("gross_return", "sum"),
            transaction_cost=("transaction_cost", "sum"),
            net_return=("net_return", "sum"),
            turnover=("turnover", "sum"),
            gross_exposure=("abs_weight", "sum"),
            active_pairs=("active_pair", "sum"),
        )
        .reset_index()
    )
    daily["equity"] = (1.0 + daily["net_return"]).cumprod()
    daily = add_event_regime(daily)
    weights = add_event_regime(weights)
    summary = _performance_summary(daily=daily, weights=weights, label=label)
    return daily, weights, summary


def run_feature_basket_backtest_from_paths(
    candidates_path: Path,
    matrix_path: Path,
    output_daily_path: Path,
    output_weights_path: Path,
    output_summary_path: Path,
    as_of_date: str,
    commodity_signals_path: Path = DEFAULT_COMMODITY_SIGNALS,
    beta_returns_path: Path = DEFAULT_EQUITY_BETA_RETURNS,
    start: str | None = "2010-01-01",
    end: str | None = None,
    return_column: str = "residual_return",
    activation_z: float = 1.0,
    exit_z: float | None = None,
    position_mode: str = "sign",
    transaction_cost_bps: float = 10.0,
    max_pair_weight: float = 0.12,
    target_gross: float = 1.0,
    rebalance_frequency: str = "daily",
    eligible_only: bool = True,
    label: str = "feature_basket",
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    candidates = _read_frame(candidates_path)
    daily, weights, summary = run_feature_basket_backtest(
        candidates=candidates,
        matrix_path=matrix_path,
        as_of_date=as_of_date,
        commodity_signals_path=commodity_signals_path,
        beta_returns_path=beta_returns_path,
        start=start,
        end=end,
        return_column=return_column,
        activation_z=activation_z,
        exit_z=exit_z,
        position_mode=position_mode,
        transaction_cost_bps=transaction_cost_bps,
        max_pair_weight=max_pair_weight,
        target_gross=target_gross,
        rebalance_frequency=rebalance_frequency,
        eligible_only=eligible_only,
        label=label,
    )
    _write_frame(daily, output_daily_path)
    _write_frame(weights, output_weights_path)
    _write_frame(summary, output_summary_path)
    return daily, weights, summary
