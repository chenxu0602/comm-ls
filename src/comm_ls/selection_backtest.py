from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from comm_ls.research_quality import feature_hypothesis_family


DEFAULT_RETURN_COLUMNS = [
    "raw_return",
    "residual_return_mktsec_w12m",
    "residual_return_mktseccomm_w12m",
]
RETURN_LABELS = {
    "raw_return": "unhedged",
    "residual_return_mktsec_w12m": "hedged_alpha",
    "residual_return_mktseccomm_w12m": "commodity_neutral",
}
TRIGGER_MODES = {"z-abs", "level-ge", "level-le"}


def _read_frame(path: Path) -> pd.DataFrame:
    if path.suffix == ".parquet":
        return pd.read_parquet(path)
    return pd.read_csv(path)


def _write_frame(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix == ".parquet":
        df.to_parquet(output_path, index=False)
    elif output_path.suffix == ".csv":
        df.to_csv(output_path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")


def _quarter_label_from_date(value: object) -> str:
    date = pd.Timestamp(value)
    return f"{date.year}-Q{((date.month - 1) // 3) + 1}"


def _quarter_start(label: str) -> pd.Timestamp:
    return pd.Period(label, freq="Q").start_time.normalize()


def _quarter_end(label: str) -> pd.Timestamp:
    return pd.Period(label, freq="Q").end_time.normalize()


def _normalize_tickers(tickers: list[str] | tuple[str, ...] | None) -> set[str] | None:
    if tickers is None:
        return None
    return {ticker.upper().strip() for ticker in tickers}


def _normalize_features(features: str | list[str] | tuple[str, ...]) -> list[str]:
    if isinstance(features, str):
        return [features.strip()]
    out = [feature.strip() for feature in features]
    if not out:
        raise ValueError("At least one feature is required")
    return out


def _feature_set_id(features: list[str]) -> str:
    return "__".join(feature.replace("/", "_").replace(" ", "_") for feature in features)


def _matrix_files(matrix_dir: Path, commodity: str) -> list[Path]:
    return sorted(matrix_dir.glob(f"{commodity.upper()}-Features-*-*.csv"))


def _source_paths(paths: pd.Series) -> str:
    return ",".join(sorted(set(paths.dropna().astype(str))))


def _dominant_direction(values: pd.Series) -> tuple[float, int, int, float]:
    signs = pd.to_numeric(values, errors="coerce").dropna()
    signs = signs[signs.ne(0)]
    if signs.empty:
        return 0.0, 0, 0, 0.0
    positive = int((signs > 0).sum())
    negative = int((signs < 0).sum())
    if positive >= negative:
        return 1.0, positive, negative, positive / len(signs)
    return -1.0, positive, negative, negative / len(signs)


def build_quarterly_feature_eligibility(
    matrix_dir: Path,
    commodity: str,
    feature: str | list[str] | tuple[str, ...],
    tickers: list[str] | tuple[str, ...] | None = None,
    target_return_column: str = "residual_return_mktsec_w12m",
    horizon_days: int = 21,
    lookback_years: list[int] | tuple[int, ...] | None = None,
    min_nonoverlap_abs_t_stat: float = 1.5,
    min_effective_observations: int = 20,
    min_selected_lookbacks: int = 1,
    min_direction_share: float = 0.5,
    min_pairs: int = 2,
    basket_scope: str = "quarter",
) -> tuple[pd.DataFrame, pd.DataFrame]:
    commodity = commodity.upper().strip()
    features = _normalize_features(feature)
    keep_tickers = _normalize_tickers(tickers)
    keep_lookbacks = set(lookback_years) if lookback_years is not None else None
    if basket_scope not in {"quarter", "feature"}:
        raise ValueError("basket_scope must be 'quarter' or 'feature'")

    frames: list[pd.DataFrame] = []
    for path in _matrix_files(matrix_dir, commodity):
        matrix = pd.read_csv(path)
        if matrix.empty:
            continue
        rows = matrix[
            matrix["feature"].astype(str).isin(features)
            & matrix["target_return_column"].astype(str).eq(target_return_column)
            & pd.to_numeric(matrix["horizon_days"], errors="coerce").eq(horizon_days)
        ].copy()
        if keep_tickers is not None:
            rows = rows[rows["ticker"].astype(str).str.upper().isin(keep_tickers)].copy()
        if keep_lookbacks is not None:
            rows = rows[pd.to_numeric(rows["lookback_years"], errors="coerce").isin(keep_lookbacks)].copy()
        if rows.empty:
            continue
        rows["source_matrix_path"] = str(path)
        frames.append(rows)

    if not frames:
        empty_pair = pd.DataFrame(
            columns=[
                "commodity",
                "quarter",
                "asof_date",
                "ticker",
                "feature",
                "feature_hypothesis_family",
                "target_return_column",
                "horizon_days",
                "direction_sign",
                "pair_selected",
            ]
        )
        empty_basket = pd.DataFrame(columns=["commodity", "quarter", "basket_selected", "selected_count"])
        return empty_pair, empty_basket

    raw = pd.concat(frames, ignore_index=True)
    raw["ticker"] = raw["ticker"].astype(str).str.upper().str.strip()
    raw["feature"] = raw["feature"].astype(str).str.strip()
    if "feature_hypothesis_family" not in raw.columns:
        raw["feature_hypothesis_family"] = raw["feature"].map(feature_hypothesis_family)
    raw["quarter"] = raw["quarter"].astype(str)
    raw["asof_date"] = pd.to_datetime(raw["asof_date"], utc=False)
    raw["lookback_years"] = pd.to_numeric(raw["lookback_years"], errors="coerce").astype("Int64")
    raw["direction_sign"] = pd.to_numeric(raw["direction_sign"], errors="coerce")
    raw["nonoverlap_abs_t_stat"] = pd.to_numeric(raw["nonoverlap_abs_t_stat"], errors="coerce")
    raw["nonoverlap_t_stat"] = pd.to_numeric(raw["nonoverlap_t_stat"], errors="coerce")
    raw["nonoverlap_hit_rate"] = pd.to_numeric(raw["nonoverlap_hit_rate"], errors="coerce")
    raw["effective_observations"] = pd.to_numeric(raw["effective_observations"], errors="coerce")
    raw["lookback_selected"] = (
        raw["direction_sign"].notna()
        & raw["direction_sign"].ne(0)
        & raw["nonoverlap_abs_t_stat"].ge(min_nonoverlap_abs_t_stat)
        & raw["effective_observations"].ge(min_effective_observations)
    )

    rows: list[dict[str, object]] = []
    keys = ["commodity", "quarter", "ticker", "feature", "target_return_column", "horizon_days"]
    for key, group in raw.groupby(keys, dropna=False, sort=True):
        selected = group[group["lookback_selected"]].copy()
        direction_source = selected if not selected.empty else group
        direction_sign, positive_count, negative_count, direction_share = _dominant_direction(
            direction_source["direction_sign"]
        )
        strongest = group.sort_values("nonoverlap_abs_t_stat", ascending=False).iloc[0]
        selected_lookback_count = int(selected["lookback_years"].nunique())
        pair_selected = (
            selected_lookback_count >= min_selected_lookbacks
            and direction_sign != 0
            and direction_share >= min_direction_share
        )
        rows.append(
            {
                "commodity": key[0],
                "quarter": key[1],
                "asof_date": group["asof_date"].max(),
                "ticker": key[2],
                "feature": key[3],
                "feature_hypothesis_family": group["feature_hypothesis_family"].dropna().astype(str).iloc[0]
                if group["feature_hypothesis_family"].notna().any()
                else feature_hypothesis_family(str(key[3])),
                "target_return_column": key[4],
                "horizon_days": int(key[5]),
                "direction_sign": direction_sign,
                "pair_selected": bool(pair_selected),
                "selected_lookback_count": selected_lookback_count,
                "lookback_count": int(group["lookback_years"].nunique()),
                "direction_positive_count": positive_count,
                "direction_negative_count": negative_count,
                "direction_share": direction_share,
                "max_nonoverlap_abs_t_stat": float(group["nonoverlap_abs_t_stat"].max()),
                "median_nonoverlap_abs_t_stat": float(group["nonoverlap_abs_t_stat"].median()),
                "strongest_lookback_years": int(strongest["lookback_years"]),
                "strongest_nonoverlap_t_stat": float(strongest["nonoverlap_t_stat"]),
                "strongest_nonoverlap_hit_rate": float(strongest["nonoverlap_hit_rate"]),
                "min_effective_observations": float(group["effective_observations"].min()),
                "source_matrix_paths": _source_paths(group["source_matrix_path"]),
                "selection_rule_id": (
                    f"nonoverlap_abs_t>={min_nonoverlap_abs_t_stat};"
                    f"eff_obs>={min_effective_observations};"
                    f"selected_lookbacks>={min_selected_lookbacks};"
                    f"direction_share>={min_direction_share}"
                ),
            }
        )

    pair = pd.DataFrame(rows).sort_values(["quarter", "feature", "ticker"]).reset_index(drop=True)
    basket_group_cols = ["commodity", "quarter"] if basket_scope == "quarter" else ["commodity", "quarter", "feature"]
    basket = (
        pair.groupby(basket_group_cols, as_index=False)
        .agg(
            selected_count=("pair_selected", "sum"),
            candidate_count=("ticker", "count"),
            ticker_count=("ticker", "nunique"),
            feature_count=("feature", "nunique"),
            pairs_selected=(
                "ticker",
                lambda s: ",".join(
                    sorted(
                        (
                            pair.loc[s.index][pair.loc[s.index, "pair_selected"]]["feature"]
                            + ":"
                            + pair.loc[s.index][pair.loc[s.index, "pair_selected"]]["ticker"]
                        ).tolist()
                    )
                ),
            ),
            asof_date=("asof_date", "max"),
        )
        .reset_index(drop=True)
    )
    basket["basket_selected"] = basket["selected_count"].ge(min_pairs)
    basket["basket_scope"] = basket_scope
    basket["basket_rule_id"] = f"{basket_scope}_selected_count>={min_pairs}"
    return pair, basket.sort_values(basket_group_cols).reset_index(drop=True)


def _event_dates_for_quarter(calendar: pd.Index, quarter: str) -> pd.Index:
    start = _quarter_start(quarter)
    end = _quarter_end(quarter)
    return calendar[(calendar >= start) & (calendar <= end)]


def _trigger_signal(
    feature_z: object,
    feature_value: object,
    trigger_mode: str,
    activation_z: float,
    activation_level: float | None,
) -> tuple[bool, float, float]:
    if trigger_mode == "z-abs":
        z = float(feature_z) if not pd.isna(feature_z) else np.nan
        if pd.isna(z) or abs(z) < activation_z:
            return False, np.nan, np.nan
        return True, z, float(np.sign(z))

    value = float(feature_value) if not pd.isna(feature_value) else np.nan
    if pd.isna(value):
        return False, np.nan, np.nan
    if activation_level is None:
        raise ValueError("activation_level is required for level trigger modes")
    if trigger_mode == "level-ge":
        if value < activation_level:
            return False, value, np.nan
        return True, value, 1.0
    if trigger_mode == "level-le":
        if value > activation_level:
            return False, value, np.nan
        return True, value, -1.0
    raise ValueError(f"Unsupported trigger_mode={trigger_mode!r}")


def build_quarterly_trigger_events(
    cache: pd.DataFrame,
    pair: pd.DataFrame,
    basket: pd.DataFrame,
    commodity: str,
    feature: str | list[str] | tuple[str, ...],
    tickers: list[str] | tuple[str, ...] | None = None,
    activation_z: float = 1.5,
    trigger_mode: str = "z-abs",
    activation_level: float | None = None,
    hold_days: int = 21,
    signal_lag_days: int = 1,
) -> pd.DataFrame:
    features = _normalize_features(feature)
    if trigger_mode not in TRIGGER_MODES:
        raise ValueError(f"trigger_mode must be one of {sorted(TRIGGER_MODES)}")
    missing_z_cols = [f"feature_z__{name}" for name in features if f"feature_z__{name}" not in cache.columns]
    if missing_z_cols:
        raise ValueError(f"Cache is missing feature z columns: {missing_z_cols}")
    missing_value_cols = [
        f"feature_value__{name}"
        for name in features
        if trigger_mode.startswith("level-") and f"feature_value__{name}" not in cache.columns
    ]
    if missing_value_cols:
        raise ValueError(
            "Cache is missing raw feature value columns required by level trigger modes: "
            f"{missing_value_cols}. Rebuild it with build-daily-feature-return-cache."
        )
    if trigger_mode.startswith("level-") and activation_level is None:
        raise ValueError("activation_level is required for level trigger modes")

    keep_tickers = _normalize_tickers(tickers)
    data = cache.copy()
    data["commodity"] = data["commodity"].astype(str).str.upper().str.strip()
    data = data[data["commodity"].eq(commodity.upper().strip())].copy()
    data["ticker"] = data["ticker"].astype(str).str.upper().str.strip()
    if keep_tickers is not None:
        data = data[data["ticker"].isin(keep_tickers)].copy()
    data["date"] = pd.to_datetime(data["date"], utc=False)
    data["quarter"] = data["date"].map(_quarter_label_from_date)
    for name in features:
        data[f"feature_z__{name}"] = pd.to_numeric(data[f"feature_z__{name}"], errors="coerce")
        value_col = f"feature_value__{name}"
        if value_col in data.columns:
            data[value_col] = pd.to_numeric(data[value_col], errors="coerce")
    if "commodity_arrival" in data.columns:
        data["commodity_arrival"] = pd.to_datetime(data["commodity_arrival"], utc=False)
        data["commodity_known_date"] = data["commodity_arrival"].dt.normalize()
    else:
        data["commodity_known_date"] = pd.NaT
    if "commodity_feature_date" in data.columns:
        data["commodity_feature_date"] = pd.to_datetime(data["commodity_feature_date"], utc=False)

    pair_source = pair.copy()
    if "feature_hypothesis_family" not in pair_source.columns:
        pair_source["feature_hypothesis_family"] = pair_source["feature"].astype(str).map(feature_hypothesis_family)
    pair_key = pair_source[
        [
            "quarter",
            "ticker",
            "feature",
            "feature_hypothesis_family",
            "direction_sign",
            "pair_selected",
            "target_return_column",
            "horizon_days",
            "source_matrix_paths",
            "selection_rule_id",
        ]
    ].copy()
    pair_key["ticker"] = pair_key["ticker"].astype(str).str.upper().str.strip()
    pair_key["feature"] = pair_key["feature"].astype(str)
    pair_key["direction_sign"] = pd.to_numeric(pair_key["direction_sign"], errors="coerce")
    basket_key = basket.copy()
    basket_join_cols = ["quarter", "feature"] if "feature" in basket_key.columns else ["quarter"]
    basket_cols = [*basket_join_cols, "basket_selected", "basket_rule_id"]
    basket_key = basket_key[basket_cols].drop_duplicates(basket_join_cols)

    feature_frames: list[pd.DataFrame] = []
    base_cols = [
        "commodity",
        "date",
        "ticker",
        "quarter",
        "commodity_feature_date",
        "commodity_arrival",
        "commodity_known_date",
    ]
    for name in features:
        z_col = f"feature_z__{name}"
        value_col = f"feature_value__{name}"
        feature_cols = [z_col]
        if value_col in data.columns:
            feature_cols.append(value_col)
        feature_data = data[[col for col in base_cols if col in data.columns] + feature_cols].copy()
        feature_data = feature_data.rename(columns={z_col: "feature_z", value_col: "feature_value"})
        if "feature_value" not in feature_data.columns:
            feature_data["feature_value"] = np.nan
        feature_data["feature"] = name
        feature_data = feature_data.merge(basket_key, on=basket_join_cols, how="left")
        feature_data = feature_data.merge(
            pair_key,
            on=["quarter", "ticker", "feature"],
            how="left",
            suffixes=("", "_eligibility"),
        )
        feature_frames.append(feature_data)

    data = pd.concat(feature_frames, ignore_index=True) if feature_frames else pd.DataFrame()
    data["basket_selected"] = data["basket_selected"].fillna(False).astype(bool)
    data["pair_selected"] = data["pair_selected"].fillna(False).astype(bool)
    data["direction_sign"] = pd.to_numeric(data["direction_sign"], errors="coerce").fillna(0.0)

    calendar = pd.Index(sorted(data["date"].dropna().unique()))
    date_to_idx = {date: idx for idx, date in enumerate(calendar)}

    events: list[dict[str, object]] = []
    event_number = 0
    for row in data.sort_values(["date", "feature", "ticker"]).itertuples(index=False):
        triggered, trigger_value, trigger_sign = _trigger_signal(
            feature_z=row.feature_z,
            feature_value=row.feature_value,
            trigger_mode=trigger_mode,
            activation_z=activation_z,
            activation_level=activation_level,
        )
        if not triggered:
            continue
        direction_sign = float(row.direction_sign)
        if direction_sign == 0:
            continue
        signal_date = pd.Timestamp(row.date)
        signal_idx = date_to_idx.get(signal_date)
        if signal_idx is None:
            continue
        entry_idx = signal_idx + signal_lag_days
        if entry_idx >= len(calendar):
            continue
        quarter_dates = _event_dates_for_quarter(calendar, row.quarter)
        if quarter_dates.empty:
            continue
        quarter_end_date = pd.Timestamp(quarter_dates.max())
        entry_date = pd.Timestamp(calendar[entry_idx])
        if entry_date > quarter_end_date:
            continue
        planned_exit_idx = min(entry_idx + hold_days - 1, len(calendar) - 1)
        planned_exit_date = pd.Timestamp(calendar[planned_exit_idx])
        exit_date = min(planned_exit_date, quarter_end_date)
        side = float(trigger_sign * direction_sign)
        if side == 0:
            continue

        selected = bool(row.basket_selected) and bool(row.pair_selected)
        event_number += 1
        events.append(
            {
                "event_id": f"{commodity.upper()}-{row.quarter}-{event_number:06d}",
                "commodity": commodity.upper(),
                "quarter": row.quarter,
                "signal_date": signal_date,
                "entry_date": entry_date,
                "planned_exit_date": planned_exit_date,
                "quarter_end_date": quarter_end_date,
                "exit_date": exit_date,
                "exit_reason": "quarter_end" if exit_date == quarter_end_date < planned_exit_date else "hold_days",
                "ticker": row.ticker,
                "feature": row.feature,
                "feature_hypothesis_family": row.feature_hypothesis_family,
                "feature_z": float(row.feature_z) if not pd.isna(row.feature_z) else np.nan,
                "feature_value": float(row.feature_value) if not pd.isna(row.feature_value) else np.nan,
                "trigger_value": trigger_value,
                "trigger_sign": trigger_sign,
                "trigger_mode": trigger_mode,
                "side": side,
                "selected": selected,
                "basket_selected": bool(row.basket_selected),
                "pair_selected": bool(row.pair_selected),
                "direction_sign": direction_sign,
                "activation_z": activation_z,
                "activation_level": activation_level,
                "hold_days": hold_days,
                "signal_lag_days": signal_lag_days,
                "target_return_column": row.target_return_column,
                "horizon_days": row.horizon_days,
                "commodity_feature_date": getattr(row, "commodity_feature_date", pd.NaT),
                "commodity_arrival": getattr(row, "commodity_arrival", pd.NaT),
                "commodity_known_date": getattr(row, "commodity_known_date", pd.NaT),
                "source_matrix_paths": row.source_matrix_paths,
                "selection_rule_id": row.selection_rule_id,
                "basket_rule_id": row.basket_rule_id,
            }
        )

    if not events:
        return pd.DataFrame()
    return pd.DataFrame(events).sort_values(["quarter", "signal_date", "ticker"]).reset_index(drop=True)


def _load_return_panel(
    equity_processed: pd.DataFrame,
    tickers: set[str],
    return_columns: list[str],
) -> pd.DataFrame:
    missing = [col for col in return_columns if col not in equity_processed.columns]
    if missing:
        raise ValueError(f"equity_processed is missing return columns: {missing}")
    panel = equity_processed.copy()
    panel["ticker"] = panel["ticker"].astype(str).str.upper().str.strip()
    panel = panel[panel["ticker"].isin(tickers)].copy()
    panel["date"] = pd.to_datetime(panel["date"], utc=False)
    keep = ["date", "ticker", *return_columns]
    panel = panel[keep].copy()
    for col in return_columns:
        panel[col] = pd.to_numeric(panel[col], errors="coerce")
    return panel.sort_values(["ticker", "date"]).reset_index(drop=True)


def build_event_pnl(
    events: pd.DataFrame,
    equity_processed: pd.DataFrame,
    return_columns: list[str] | None = None,
    gross_exposure: float = 1.0,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if events.empty:
        return pd.DataFrame(), pd.DataFrame()
    return_columns = return_columns or DEFAULT_RETURN_COLUMNS
    event_data = events.copy()
    for col in ["signal_date", "entry_date", "exit_date"]:
        event_data[col] = pd.to_datetime(event_data[col], utc=False)
    tickers = set(event_data["ticker"].astype(str).str.upper())
    returns = _load_return_panel(equity_processed, tickers=tickers, return_columns=return_columns)
    calendar = pd.Index(sorted(returns["date"].dropna().unique()))

    rows: list[pd.DataFrame] = []
    for event in event_data.itertuples(index=False):
        active_dates = calendar[(calendar >= event.entry_date) & (calendar <= event.exit_date)]
        if active_dates.empty:
            continue
        frame = pd.DataFrame(
            {
                "date": active_dates,
                "event_id": event.event_id,
                "commodity": event.commodity,
                "quarter": event.quarter,
                "ticker": event.ticker,
                "feature": event.feature,
                "feature_hypothesis_family": event.feature_hypothesis_family,
                "side": event.side,
                "selected": event.selected,
                "signal_date": event.signal_date,
                "entry_date": event.entry_date,
                "exit_date": event.exit_date,
            }
        )
        rows.append(frame)

    if not rows:
        return pd.DataFrame(), pd.DataFrame()

    stock_daily = pd.concat(rows, ignore_index=True)
    stock_daily = stock_daily.merge(returns, on=["date", "ticker"], how="left")
    for col in return_columns:
        stock_daily[f"missing_{col}"] = stock_daily[col].isna()
    stock_daily["missing_return"] = stock_daily[[f"missing_{col}" for col in return_columns]].any(axis=1)
    for col in return_columns:
        stock_daily[col] = stock_daily[col].fillna(0.0)

    weighted_frames: list[pd.DataFrame] = []
    for date, group in stock_daily.groupby("date", sort=True):
        active = group.copy()
        all_abs = active["side"].abs().sum()
        active["all_weight"] = np.where(all_abs > 0, active["side"] / all_abs * gross_exposure, 0.0)

        active["selected_weight"] = 0.0
        selected_mask = active["selected"].astype(bool)
        selected_abs = active.loc[selected_mask, "side"].abs().sum()
        if selected_abs > 0:
            active.loc[selected_mask, "selected_weight"] = (
                active.loc[selected_mask, "side"] / selected_abs * gross_exposure
            )

        active["unselected_weight"] = 0.0
        unselected_mask = ~selected_mask
        unselected_abs = active.loc[unselected_mask, "side"].abs().sum()
        if unselected_abs > 0:
            active.loc[unselected_mask, "unselected_weight"] = (
                active.loc[unselected_mask, "side"] / unselected_abs * gross_exposure
            )
        weighted_frames.append(active)

    stock_daily = pd.concat(weighted_frames, ignore_index=True)
    weight_cols = ["selected_weight", "unselected_weight", "all_weight"]
    for return_col in return_columns:
        label = RETURN_LABELS.get(return_col, return_col)
        for weight_col in weight_cols:
            prefix = weight_col.removesuffix("_weight")
            stock_daily[f"{prefix}_{label}_pnl"] = stock_daily[weight_col] * stock_daily[return_col]

    aggregations = {
        "active_sleeves": ("event_id", "nunique"),
        "active_tickers": ("ticker", "nunique"),
        "gross_exposure": ("all_weight", lambda s: float(s.abs().sum())),
        "net_exposure": ("all_weight", "sum"),
        "long_exposure": ("all_weight", lambda s: float(s[s > 0].sum())),
        "short_exposure": ("all_weight", lambda s: float(s[s < 0].sum())),
        "missing_return_rows": ("missing_return", "sum"),
    }
    for return_col in return_columns:
        aggregations[f"missing_{return_col}_rows"] = (f"missing_{return_col}", "sum")
    pnl_cols = [col for col in stock_daily.columns if col.endswith("_pnl")]
    for col in pnl_cols:
        aggregations[col] = (col, "sum")

    portfolio_daily = stock_daily.groupby("date", as_index=False).agg(**aggregations)
    for col in pnl_cols:
        equity_col = col.replace("_pnl", "_equity")
        drawdown_col = col.replace("_pnl", "_drawdown")
        portfolio_daily[equity_col] = np.exp(portfolio_daily[col].fillna(0.0).cumsum())
        portfolio_daily[drawdown_col] = (
            portfolio_daily[equity_col] / portfolio_daily[equity_col].cummax() - 1.0
        )
    return stock_daily.sort_values(["date", "event_id"]).reset_index(drop=True), portfolio_daily


def _summary_from_portfolio(
    portfolio_daily: pd.DataFrame,
    events: pd.DataFrame,
    pair: pd.DataFrame,
    basket: pd.DataFrame,
    quarter: str,
) -> pd.DataFrame:
    row: dict[str, object] = {
        "quarter": quarter,
        "event_count": len(events),
        "selected_event_count": int(events["selected"].sum()) if not events.empty else 0,
        "pair_count": int(pair["ticker"].nunique()) if not pair.empty else 0,
        "pair_feature_count": int(len(pair)) if not pair.empty else 0,
        "pair_selected_count": int(pair["pair_selected"].sum()) if not pair.empty else 0,
        "feature_count": int(pair["feature"].nunique()) if not pair.empty else 0,
        "basket_selected": bool(basket["basket_selected"].any()) if not basket.empty else False,
        "basket_selected_count": int(basket["basket_selected"].sum()) if not basket.empty else 0,
    }
    if portfolio_daily.empty:
        return pd.DataFrame([row])
    row["start_date"] = portfolio_daily["date"].min()
    row["end_date"] = portfolio_daily["date"].max()
    row["active_days"] = int(len(portfolio_daily))
    row["avg_gross_exposure"] = float(portfolio_daily["gross_exposure"].mean())
    for col in [col for col in portfolio_daily.columns if col.endswith("_pnl")]:
        returns = pd.to_numeric(portfolio_daily[col], errors="coerce").fillna(0.0)
        equity = np.exp(returns.cumsum())
        row[f"{col}_total_return"] = float(equity.iloc[-1] - 1.0)
        vol = float(returns.std(ddof=0) * np.sqrt(252)) if len(returns) else np.nan
        ann = float(equity.iloc[-1] ** (252 / len(returns)) - 1.0) if len(returns) else np.nan
        row[f"{col}_annualized_return"] = ann
        row[f"{col}_annualized_volatility"] = vol
        row[f"{col}_sharpe"] = ann / vol if vol else np.nan
        row[f"{col}_max_drawdown"] = float((equity / equity.cummax() - 1.0).min())
    return pd.DataFrame([row])


def run_quarterly_selection_backtest(
    cache: pd.DataFrame,
    equity_processed: pd.DataFrame,
    matrix_dir: Path,
    output_dir: Path,
    commodity: str,
    feature: str | list[str] | tuple[str, ...],
    tickers: list[str] | tuple[str, ...] | None = None,
    target_return_column: str = "residual_return_mktsec_w12m",
    horizon_days: int = 21,
    lookback_years: list[int] | tuple[int, ...] | None = None,
    min_nonoverlap_abs_t_stat: float = 1.5,
    min_effective_observations: int = 20,
    min_selected_lookbacks: int = 1,
    min_direction_share: float = 0.5,
    min_pairs: int = 2,
    basket_scope: str = "quarter",
    activation_z: float = 1.5,
    trigger_mode: str = "z-abs",
    activation_level: float | None = None,
    hold_days: int = 21,
    signal_lag_days: int = 1,
    gross_exposure: float = 1.0,
    return_columns: list[str] | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    commodity = commodity.upper().strip()
    features = _normalize_features(feature)
    feature_id = _feature_set_id(features)
    pair, basket = build_quarterly_feature_eligibility(
        matrix_dir=matrix_dir,
        commodity=commodity,
        feature=features,
        tickers=tickers,
        target_return_column=target_return_column,
        horizon_days=horizon_days,
        lookback_years=lookback_years,
        min_nonoverlap_abs_t_stat=min_nonoverlap_abs_t_stat,
        min_effective_observations=min_effective_observations,
        min_selected_lookbacks=min_selected_lookbacks,
        min_direction_share=min_direction_share,
        min_pairs=min_pairs,
        basket_scope=basket_scope,
    )
    events = build_quarterly_trigger_events(
        cache=cache,
        pair=pair,
        basket=basket,
        commodity=commodity,
        feature=features,
        tickers=tickers,
        activation_z=activation_z,
        trigger_mode=trigger_mode,
        activation_level=activation_level,
        hold_days=hold_days,
        signal_lag_days=signal_lag_days,
    )

    summary_frames: list[pd.DataFrame] = []
    stock_frames: list[pd.DataFrame] = []
    portfolio_frames: list[pd.DataFrame] = []
    quarters = sorted(set(pair["quarter"]).union(set(events["quarter"] if not events.empty else [])))
    for quarter in quarters:
        pair_q = pair[pair["quarter"].eq(quarter)].copy()
        basket_q = basket[basket["quarter"].eq(quarter)].copy()
        events_q = events[events["quarter"].eq(quarter)].copy() if not events.empty else pd.DataFrame()

        stock_q, portfolio_q = build_event_pnl(
            events=events_q,
            equity_processed=equity_processed,
            return_columns=return_columns,
            gross_exposure=gross_exposure,
        )
        summary_q = _summary_from_portfolio(
            portfolio_daily=portfolio_q,
            events=events_q,
            pair=pair_q,
            basket=basket_q,
            quarter=quarter,
        )

        base = output_dir / commodity
        _write_frame(pair_q, base / "eligibility" / f"{commodity}-{quarter}-eligibility.parquet")
        _write_frame(events_q, base / "events" / f"{commodity}-{quarter}-events.parquet")
        _write_frame(stock_q, base / "pnl" / f"{commodity}-{quarter}-stock_daily.parquet")
        _write_frame(portfolio_q, base / "pnl" / f"{commodity}-{quarter}-portfolio_daily.parquet")
        _write_frame(summary_q, base / "summary" / f"{commodity}-{quarter}-summary.csv")

        if not stock_q.empty:
            stock_frames.append(stock_q)
        if not portfolio_q.empty:
            portfolio_frames.append(portfolio_q)
        summary_frames.append(summary_q)

    summary = pd.concat(summary_frames, ignore_index=True) if summary_frames else pd.DataFrame()
    stock_daily = pd.concat(stock_frames, ignore_index=True) if stock_frames else pd.DataFrame()
    portfolio_daily = pd.concat(portfolio_frames, ignore_index=True) if portfolio_frames else pd.DataFrame()
    base = output_dir / commodity
    _write_frame(pair, base / f"{commodity}-{feature_id}-eligibility-all.parquet")
    _write_frame(events, base / f"{commodity}-{feature_id}-events-all.parquet")
    _write_frame(summary, base / f"{commodity}-{feature_id}-summary-all.csv")
    return pair, events, stock_daily, portfolio_daily


def run_quarterly_selection_backtest_from_paths(
    cache_path: Path,
    equity_processed_path: Path,
    matrix_dir: Path,
    output_dir: Path,
    commodity: str,
    feature: str | list[str] | tuple[str, ...],
    tickers: list[str] | tuple[str, ...] | None = None,
    target_return_column: str = "residual_return_mktsec_w12m",
    horizon_days: int = 21,
    lookback_years: list[int] | tuple[int, ...] | None = None,
    min_nonoverlap_abs_t_stat: float = 1.5,
    min_effective_observations: int = 20,
    min_selected_lookbacks: int = 1,
    min_direction_share: float = 0.5,
    min_pairs: int = 2,
    basket_scope: str = "quarter",
    activation_z: float = 1.5,
    trigger_mode: str = "z-abs",
    activation_level: float | None = None,
    hold_days: int = 21,
    signal_lag_days: int = 1,
    gross_exposure: float = 1.0,
    return_columns: list[str] | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    return run_quarterly_selection_backtest(
        cache=_read_frame(cache_path),
        equity_processed=_read_frame(equity_processed_path),
        matrix_dir=matrix_dir,
        output_dir=output_dir,
        commodity=commodity,
        feature=feature,
        tickers=tickers,
        target_return_column=target_return_column,
        horizon_days=horizon_days,
        lookback_years=lookback_years,
        min_nonoverlap_abs_t_stat=min_nonoverlap_abs_t_stat,
        min_effective_observations=min_effective_observations,
        min_selected_lookbacks=min_selected_lookbacks,
        min_direction_share=min_direction_share,
        min_pairs=min_pairs,
        basket_scope=basket_scope,
        activation_z=activation_z,
        trigger_mode=trigger_mode,
        activation_level=activation_level,
        hold_days=hold_days,
        signal_lag_days=signal_lag_days,
        gross_exposure=gross_exposure,
        return_columns=return_columns,
    )
