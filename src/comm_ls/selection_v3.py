from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from comm_ls.reaction import load_frame
from comm_ls.research_quality import _feature_commodity_direction, feature_hypothesis_family, state_hypothesis


DEFAULT_CURVE_STATES = {
    "curve_tightness",
    "curve_tightness_change",
}


def _write_frame(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix == ".parquet":
        df.to_parquet(output_path, index=False)
    elif output_path.suffix == ".csv":
        df.to_csv(output_path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")


def _quarter_start(label: str) -> pd.Timestamp:
    return pd.Period(label, freq="Q").start_time.normalize()


def _quarter_end(label: str) -> pd.Timestamp:
    return pd.Period(label, freq="Q").end_time.normalize()


def _next_quarter(label: str) -> str:
    period = pd.Period(label, freq="Q") + 1
    return f"{period.year}-Q{period.quarter}"


def _quarters_between(start_label: str, end_label: str) -> list[str]:
    start = pd.Period(start_label, freq="Q")
    end = pd.Period(end_label, freq="Q")
    if end < start:
        return []
    return [f"{period.year}-Q{period.quarter}" for period in pd.period_range(start, end, freq="Q")]


def _oos_quarters_for_selection(selection_quarter: str, mode: str, end_quarter: str | None = None) -> list[str]:
    if mode == "next-quarter":
        return [_next_quarter(selection_quarter)]
    if mode == "year-remainder":
        start = pd.Period(selection_quarter, freq="Q")
        if end_quarter is None:
            end_quarter = f"{start.year}-Q4"
        return _quarters_between(selection_quarter, end_quarter)
    raise ValueError(f"Unknown OOS mode: {mode}")


def _matrix_files(matrix_dir: Path, commodity: str) -> list[Path]:
    return sorted(matrix_dir.glob(f"{commodity.upper()}-Features-*-*.csv"))


def _direction_sign(row: pd.Series) -> float:
    if "direction_sign" in row.index and pd.notna(row["direction_sign"]):
        value = float(pd.to_numeric(row["direction_sign"], errors="coerce"))
        if value != 0:
            return float(np.sign(value))
    for col in ["nonoverlap_beta_per_1z", "beta_per_1z", "median_nonoverlap_beta_per_1z"]:
        if col in row.index and pd.notna(row[col]):
            value = float(pd.to_numeric(row[col], errors="coerce"))
            if value != 0:
                return float(np.sign(value))
    return 0.0


def _daily_pnl_stats(pnl: pd.Series) -> dict[str, float]:
    clean = pd.to_numeric(pnl, errors="coerce").replace([np.inf, -np.inf], np.nan).fillna(0.0)
    if clean.empty:
        return {
            "daily_observations": 0,
            "total_pnl": np.nan,
            "annualized_return": np.nan,
            "annualized_volatility": np.nan,
            "sharpe": np.nan,
            "max_drawdown": np.nan,
            "calmar": np.nan,
            "mean_daily_pnl": np.nan,
        }
    mean = float(clean.mean())
    std = float(clean.std(ddof=1))
    annualized_return = mean * 252.0
    annualized_volatility = std * np.sqrt(252.0) if std > 0 else np.nan
    cum = clean.cumsum()
    max_drawdown = float((cum.cummax() - cum).max())
    return {
        "daily_observations": int(len(clean)),
        "total_pnl": float(clean.sum()),
        "annualized_return": annualized_return,
        "annualized_volatility": annualized_volatility,
        "sharpe": float(mean / std * np.sqrt(252.0)) if std > 0 else np.nan,
        "max_drawdown": max_drawdown,
        "calmar": float(annualized_return / max_drawdown) if max_drawdown > 0 else np.nan,
        "mean_daily_pnl": mean,
    }


def _build_candidate_daily_pnl(
    cache: pd.DataFrame,
    ticker: str,
    feature: str,
    direction_sign: float,
    return_column: str,
    horizon_days: int,
    activation_z: float,
    sample_start: pd.Timestamp,
    sample_end: pd.Timestamp,
) -> tuple[pd.DataFrame, int]:
    feature_col = f"feature_z__{feature}"
    target_end_col = f"target_end_{horizon_days}d"
    needed = ["date", "ticker", return_column, feature_col, target_end_col]
    if any(col not in cache.columns for col in needed):
        return pd.DataFrame(), 0

    data = cache.loc[cache["ticker"].astype(str).str.upper().eq(ticker), needed].copy()
    if data.empty:
        return pd.DataFrame(), 0
    data["date"] = pd.to_datetime(data["date"], utc=False)
    data[target_end_col] = pd.to_datetime(data[target_end_col], utc=False)
    data[return_column] = pd.to_numeric(data[return_column], errors="coerce").fillna(0.0)
    data[feature_col] = pd.to_numeric(data[feature_col], errors="coerce")
    data = data[data["date"].between(sample_start, sample_end)].sort_values("date").reset_index(drop=True)
    if data.empty:
        return pd.DataFrame(), 0

    triggers = data[
        data[feature_col].abs().ge(activation_z)
        & data[target_end_col].notna()
        & data[target_end_col].le(sample_end)
    ].copy()
    events: list[pd.Series] = []
    last_end = pd.Timestamp.min
    for _, event in triggers.iterrows():
        if event["date"] <= last_end:
            continue
        events.append(event)
        last_end = pd.Timestamp(event[target_end_col])

    data["pos"] = 0.0
    for event in events:
        signal_date = pd.Timestamp(event["date"])
        target_end = pd.Timestamp(event[target_end_col])
        side = float(np.sign(float(event[feature_col])) * direction_sign)
        if side == 0:
            continue
        active = data["date"].ge(signal_date) & data["date"].lt(target_end)
        data.loc[active, "pos"] = side

    data["pnl"] = data["pos"].shift(1).fillna(0.0).mul(data[return_column])
    return data[["date", "pos", "pnl"]], len(events)


def _loyo_calmar_stats(daily: pd.DataFrame) -> dict[str, object]:
    if daily.empty:
        return {
            "full_calmar": np.nan,
            "loyo_min_calmar": np.nan,
            "loyo_worst_year": np.nan,
            "loyo_sign_flip": False,
            "dominant_year": np.nan,
            "dominant_year_share": np.nan,
        }

    full = _daily_pnl_stats(daily["pnl"])
    daily = daily.copy()
    daily["year"] = pd.to_datetime(daily["date"], utc=False).dt.year
    full_mean = float(full["mean_daily_pnl"]) if pd.notna(full["mean_daily_pnl"]) else 0.0
    full_sign = float(np.sign(full_mean)) if full_mean != 0 else 0.0

    loyo_rows: list[dict[str, object]] = []
    for year in sorted(daily["year"].dropna().unique()):
        holdout = daily[daily["year"] != year]
        stats = _daily_pnl_stats(holdout["pnl"])
        holdout_mean = float(stats["mean_daily_pnl"]) if pd.notna(stats["mean_daily_pnl"]) else 0.0
        loyo_rows.append(
            {
                "excluded_year": int(year),
                "loyo_calmar": stats["calmar"],
                "loyo_total_pnl": stats["total_pnl"],
                "loyo_mean_daily_pnl": holdout_mean,
                "loyo_sign": float(np.sign(holdout_mean)) if holdout_mean != 0 else 0.0,
            }
        )
    loyo = pd.DataFrame(loyo_rows)
    valid = loyo[pd.to_numeric(loyo["loyo_calmar"], errors="coerce").notna()].copy()
    if valid.empty:
        loyo_min_calmar = np.nan
        loyo_worst_year = np.nan
    else:
        worst_idx = valid["loyo_calmar"].idxmin()
        loyo_min_calmar = float(valid.loc[worst_idx, "loyo_calmar"])
        loyo_worst_year = int(valid.loc[worst_idx, "excluded_year"])

    if full_sign == 0:
        sign_flip = False
    else:
        sign_flip = bool((loyo["loyo_sign"].ne(0) & loyo["loyo_sign"].ne(full_sign)).any())

    yearly = daily.groupby("year")["pnl"].sum()
    positive_total = yearly[yearly > 0].sum()
    if positive_total > 0 and not yearly.empty:
        dominant_year = int(yearly.idxmax())
        dominant_year_share = float(yearly.max() / positive_total)
    else:
        dominant_year = np.nan
        dominant_year_share = np.nan

    all_calmars = [full["calmar"]]
    if pd.notna(loyo_min_calmar):
        all_calmars.append(loyo_min_calmar)
    robust_min = float(np.nanmin(all_calmars)) if any(pd.notna(v) for v in all_calmars) else np.nan

    return {
        "full_calmar": full["calmar"],
        "full_sharpe": full["sharpe"],
        "full_max_drawdown": full["max_drawdown"],
        "full_total_pnl": full["total_pnl"],
        "full_annualized_return": full["annualized_return"],
        "full_annualized_volatility": full["annualized_volatility"],
        "loyo_min_calmar": loyo_min_calmar,
        "robust_min_calmar": robust_min,
        "loyo_worst_year": loyo_worst_year,
        "loyo_sign_flip": sign_flip,
        "dominant_year": dominant_year,
        "dominant_year_share": dominant_year_share,
        "loyo_calmar_by_year": ";".join(
            f"{int(row.excluded_year)}:{float(row.loyo_calmar):.3f}"
            for row in loyo.itertuples(index=False)
            if pd.notna(row.loyo_calmar)
        ),
    }


def _load_curve_matrix_rows(
    matrix_dir: Path,
    commodity: str,
    quarters: list[str] | None,
    lookback_years: list[int] | None,
    target_return_column: str,
    allowed_states: set[str],
    min_nonoverlap_abs_t: float,
    min_effective_observations: int,
) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    quarter_set = set(quarters or [])
    lookback_set = set(lookback_years or [])
    for path in _matrix_files(matrix_dir, commodity):
        matrix = pd.read_csv(path)
        if matrix.empty:
            continue
        matrix["source_matrix_path"] = str(path)
        frames.append(matrix)
    if not frames:
        return pd.DataFrame()

    df = pd.concat(frames, ignore_index=True)
    df["commodity"] = df["commodity"].astype(str).str.upper().str.strip()
    df["ticker"] = df["ticker"].astype(str).str.upper().str.strip()
    df["feature"] = df["feature"].astype(str).str.strip()
    df = df[df["commodity"].eq(commodity.upper().strip())].copy()
    df = df[df["target_return_column"].astype(str).eq(target_return_column)].copy()
    if quarter_set:
        df = df[df["quarter"].astype(str).isin(quarter_set)].copy()
    if lookback_set:
        df = df[pd.to_numeric(df["lookback_years"], errors="coerce").isin(lookback_set)].copy()
    if df.empty:
        return df

    df["state_hypothesis"] = df["feature"].map(state_hypothesis)
    df["feature_hypothesis_family"] = df["feature"].map(feature_hypothesis_family)
    df = df[df["state_hypothesis"].isin(allowed_states)].copy()
    df["direction_sign"] = df.apply(_direction_sign, axis=1)
    for col in ["nonoverlap_abs_t_stat", "effective_observations", "horizon_days", "lookback_years"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df[
        df["direction_sign"].ne(0)
        & df["nonoverlap_abs_t_stat"].ge(min_nonoverlap_abs_t)
        & df["effective_observations"].ge(min_effective_observations)
    ].copy()
    if df.empty:
        return df
    sort_cols = ["quarter", "lookback_years", "nonoverlap_abs_t_stat", "effective_observations"]
    df = df.sort_values(sort_cols, ascending=[True, False, False, False])
    return df.drop_duplicates(["quarter", "lookback_years", "ticker", "feature", "horizon_days"]).reset_index(drop=True)


def select_curve_first_candidates(
    matrix_dir: Path,
    cache: pd.DataFrame,
    commodity: str,
    quarters: list[str] | None = None,
    lookback_years: list[int] | None = None,
    target_return_column: str = "residual_return_mktsec_w12m",
    activation_z: float = 1.5,
    allowed_states: set[str] | None = None,
    min_nonoverlap_abs_t: float = 1.0,
    min_effective_observations: int = 20,
    min_robust_calmar: float = 0.5,
    max_dominant_year_share: float = 0.5,
    max_candidates: int | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    states = allowed_states or set(DEFAULT_CURVE_STATES)
    candidates = _load_curve_matrix_rows(
        matrix_dir=matrix_dir,
        commodity=commodity,
        quarters=quarters,
        lookback_years=lookback_years,
        target_return_column=target_return_column,
        allowed_states=states,
        min_nonoverlap_abs_t=min_nonoverlap_abs_t,
        min_effective_observations=min_effective_observations,
    )
    if candidates.empty:
        return candidates.copy(), candidates.copy()

    if max_candidates is not None:
        candidates = candidates.head(max_candidates).copy()

    cache = cache.copy()
    cache["ticker"] = cache["ticker"].astype(str).str.upper().str.strip()
    cache["date"] = pd.to_datetime(cache["date"], utc=False)

    rows: list[dict[str, object]] = []
    for row in candidates.itertuples(index=False):
        sample_start = pd.Timestamp(getattr(row, "sample_start"))
        sample_end = pd.Timestamp(getattr(row, "asof_date"))
        ticker = str(getattr(row, "ticker"))
        feature = str(getattr(row, "feature"))
        horizon_days = int(getattr(row, "horizon_days"))
        direction_sign = float(getattr(row, "direction_sign"))
        daily, event_count = _build_candidate_daily_pnl(
            cache=cache,
            ticker=ticker,
            feature=feature,
            direction_sign=direction_sign,
            return_column=target_return_column,
            horizon_days=horizon_days,
            activation_z=activation_z,
            sample_start=sample_start,
            sample_end=sample_end,
        )
        stats = _loyo_calmar_stats(daily)
        record = {
            "v3_selected": False,
            "v3_flags": "",
            "commodity": getattr(row, "commodity"),
            "quarter": getattr(row, "quarter"),
            "asof_date": getattr(row, "asof_date"),
            "lookback_years": int(getattr(row, "lookback_years")),
            "sample_start": getattr(row, "sample_start"),
            "matrix_sample_end": getattr(row, "sample_end"),
            "pnl_end_date": sample_end.date().isoformat(),
            "ticker": ticker,
            "theme": getattr(row, "theme", ""),
            "role": getattr(row, "role", ""),
            "region": getattr(row, "region", ""),
            "feature": feature,
            "feature_family": getattr(row, "feature_family", ""),
            "feature_hypothesis_family": getattr(row, "feature_hypothesis_family"),
            "state_hypothesis": getattr(row, "state_hypothesis"),
            "horizon_days": horizon_days,
            "target_return_column": target_return_column,
            "direction_sign": direction_sign,
            "activation_z": activation_z,
            "event_count": event_count,
            "matrix_nonoverlap_abs_t_stat": float(getattr(row, "nonoverlap_abs_t_stat")),
            "matrix_nonoverlap_t_stat": float(getattr(row, "nonoverlap_t_stat")),
            "matrix_effective_observations": float(getattr(row, "effective_observations")),
            "matrix_nonoverlap_hit_rate": float(getattr(row, "nonoverlap_hit_rate")),
            "matrix_nonoverlap_beta_per_1z": float(getattr(row, "nonoverlap_beta_per_1z")),
            "source_matrix_path": getattr(row, "source_matrix_path"),
            **stats,
        }

        flags: list[str] = []
        if pd.isna(record["robust_min_calmar"]) or float(record["robust_min_calmar"]) < min_robust_calmar:
            flags.append("low_robust_calmar")
        if pd.isna(record["full_total_pnl"]) or float(record["full_total_pnl"]) <= 0:
            flags.append("nonpositive_total_pnl")
        if bool(record["loyo_sign_flip"]):
            flags.append("loyo_sign_flip")
        if (
            pd.notna(record["dominant_year_share"])
            and float(record["dominant_year_share"]) > max_dominant_year_share
        ):
            flags.append("dominant_year")
        record["v3_flags"] = ",".join(flags)
        record["v3_selected"] = not flags
        rows.append(record)

    scored = pd.DataFrame(rows)
    if scored.empty:
        return scored, scored
    scored = scored.sort_values(
        ["v3_selected", "robust_min_calmar", "full_calmar", "matrix_nonoverlap_abs_t_stat"],
        ascending=[False, False, False, False],
    ).reset_index(drop=True)
    selected = scored[scored["v3_selected"]].copy()
    if not selected.empty:
        selected = selected.drop_duplicates(
            ["quarter", "lookback_years", "ticker", "feature_hypothesis_family", "horizon_days"],
            keep="first",
        )
    selected = selected.reset_index(drop=True)
    return scored, selected


def select_curve_first_candidates_from_paths(
    matrix_dir: Path,
    cache_path: Path,
    output_path: Path,
    selected_output_path: Path | None,
    commodity: str,
    quarters: list[str] | None = None,
    lookback_years: list[int] | None = None,
    target_return_column: str = "residual_return_mktsec_w12m",
    activation_z: float = 1.5,
    allowed_states: list[str] | None = None,
    min_nonoverlap_abs_t: float = 1.0,
    min_effective_observations: int = 20,
    min_robust_calmar: float = 0.5,
    max_dominant_year_share: float = 0.5,
    max_candidates: int | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    cache = load_frame(cache_path)
    scored, selected = select_curve_first_candidates(
        matrix_dir=matrix_dir,
        cache=cache,
        commodity=commodity,
        quarters=quarters,
        lookback_years=lookback_years,
        target_return_column=target_return_column,
        activation_z=activation_z,
        allowed_states=set(allowed_states) if allowed_states else None,
        min_nonoverlap_abs_t=min_nonoverlap_abs_t,
        min_effective_observations=min_effective_observations,
        min_robust_calmar=min_robust_calmar,
        max_dominant_year_share=max_dominant_year_share,
        max_candidates=max_candidates,
    )
    _write_frame(scored, output_path)
    if selected_output_path is not None:
        _write_frame(selected, selected_output_path)
    return scored, selected


def review_curve_first_taxonomy(
    candidates: pd.DataFrame,
    exposure_map: pd.DataFrame,
    role_taxonomy: pd.DataFrame,
    block_low_priority: bool = False,
) -> pd.DataFrame:
    if candidates.empty:
        return candidates.copy()

    out = candidates.copy()
    out["ticker"] = out["ticker"].astype(str).str.upper().str.strip()
    out["commodity"] = out["commodity"].astype(str).str.upper().str.strip()

    exposure = exposure_map.copy()
    exposure["ticker"] = exposure["ticker"].astype(str).str.upper().str.strip()
    exposure["commodity"] = exposure["commodity"].astype(str).str.upper().str.strip()
    exposure = exposure.drop_duplicates(["ticker", "commodity"])

    taxonomy = role_taxonomy.copy()
    taxonomy["commodity"] = taxonomy["commodity"].astype(str).str.upper().str.strip()
    taxonomy["exposure_role"] = taxonomy["exposure_role"].astype(str).str.strip()
    taxonomy = taxonomy.drop_duplicates(["commodity", "exposure_role"])

    out = out.merge(
        exposure[["ticker", "commodity", "exposure_role", "prior_weight", "notes"]].rename(
            columns={"notes": "exposure_notes"}
        ),
        on=["ticker", "commodity"],
        how="left",
    )
    out = out.merge(
        taxonomy[
            [
                "commodity",
                "exposure_role",
                "taxonomy_bucket",
                "economic_channel",
                "expected_prior_sign",
                "alpha_priority",
                "deployable_default",
                "notes",
            ]
        ].rename(columns={"notes": "taxonomy_notes"}),
        on=["commodity", "exposure_role"],
        how="left",
    )

    out["prior_weight"] = pd.to_numeric(out["prior_weight"], errors="coerce")
    out["deployable_default"] = out["deployable_default"].astype("boolean")
    out["flag_missing_exposure"] = out["exposure_role"].isna()
    out["flag_missing_role_taxonomy"] = out["exposure_role"].notna() & out["taxonomy_bucket"].isna()
    out["flag_not_deployable_default"] = out["deployable_default"].eq(False)
    out["flag_low_priority_role"] = out["alpha_priority"].astype(str).str.lower().eq("low")
    out["feature_commodity_direction"] = out["feature"].map(_feature_commodity_direction)
    expected = np.sign(out["prior_weight"] * out["feature_commodity_direction"]).replace(0, np.nan)
    observed = pd.to_numeric(out["direction_sign"], errors="coerce").map(np.sign).replace(0, np.nan)
    out["flag_direction_mismatch"] = expected.notna() & observed.notna() & expected.ne(observed)

    hard_block = (
        out["flag_missing_exposure"]
        | out["flag_not_deployable_default"]
        | (out["flag_low_priority_role"] if block_low_priority else False)
    )
    review = (
        out["flag_missing_role_taxonomy"]
        | out["flag_low_priority_role"]
        | out["flag_direction_mismatch"]
    )
    out["v3_taxonomy_verdict"] = np.select([hard_block, review], ["block", "review"], default="pass")

    flag_cols = [
        "flag_missing_exposure",
        "flag_missing_role_taxonomy",
        "flag_not_deployable_default",
        "flag_low_priority_role",
        "flag_direction_mismatch",
    ]
    for col in flag_cols:
        out[col] = out[col].fillna(False).astype(bool)
    labels = {
        "flag_missing_exposure": "missing_exposure",
        "flag_missing_role_taxonomy": "missing_role_taxonomy",
        "flag_not_deployable_default": "not_deployable_default",
        "flag_low_priority_role": "low_priority_role",
        "flag_direction_mismatch": "direction_mismatch",
    }
    out["v3_taxonomy_flags"] = out.apply(
        lambda row: ",".join(labels[col] for col in flag_cols if bool(row.get(col, False))),
        axis=1,
    )

    front = [
        "v3_taxonomy_verdict",
        "v3_taxonomy_flags",
        "v3_selected",
        "v3_flags",
        "commodity",
        "quarter",
        "ticker",
        "feature",
        "feature_hypothesis_family",
        "state_hypothesis",
        "horizon_days",
        "direction_sign",
        "robust_min_calmar",
        "full_calmar",
        "event_count",
        "role",
        "exposure_role",
        "prior_weight",
        "taxonomy_bucket",
        "alpha_priority",
        "deployable_default",
        "economic_channel",
    ]
    cols = [col for col in front if col in out.columns] + [col for col in out.columns if col not in front]
    return out[cols].reset_index(drop=True)


def review_curve_first_taxonomy_from_paths(
    candidates_path: Path,
    exposure_map_path: Path,
    role_taxonomy_path: Path,
    output_path: Path,
    block_low_priority: bool = False,
) -> pd.DataFrame:
    candidates = load_frame(candidates_path)
    exposure_map = pd.read_csv(exposure_map_path)
    role_taxonomy = pd.read_csv(role_taxonomy_path)
    reviewed = review_curve_first_taxonomy(
        candidates=candidates,
        exposure_map=exposure_map,
        role_taxonomy=role_taxonomy,
        block_low_priority=block_low_priority,
    )
    _write_frame(reviewed, output_path)
    return reviewed


def _oos_active_dates(calendar: pd.Index, oos_quarter: str) -> pd.Index:
    start = _quarter_start(oos_quarter)
    end = _quarter_end(oos_quarter)
    return calendar[(calendar >= start) & (calendar <= end)]


def _build_oos_events_for_candidate(
    cache: pd.DataFrame,
    row: pd.Series,
    oos_quarter: str,
    return_column: str,
    activation_z: float,
) -> list[dict[str, object]]:
    ticker = str(row["ticker"]).upper().strip()
    feature = str(row["feature"]).strip()
    direction_sign = float(pd.to_numeric(row["direction_sign"], errors="coerce"))
    horizon_days = int(pd.to_numeric(row["horizon_days"], errors="coerce"))
    feature_col = f"feature_z__{feature}"
    if direction_sign == 0 or feature_col not in cache.columns:
        return []

    data = cache[cache["ticker"].astype(str).str.upper().eq(ticker)].copy()
    if data.empty:
        return []
    data["date"] = pd.to_datetime(data["date"], utc=False)
    data[feature_col] = pd.to_numeric(data[feature_col], errors="coerce")
    oos_dates = _oos_active_dates(pd.Index(sorted(data["date"].dropna().unique())), oos_quarter)
    if oos_dates.empty:
        return []
    oos_start = pd.Timestamp(oos_dates.min())
    oos_end = pd.Timestamp(oos_dates.max())
    triggers = data[
        data["date"].between(oos_start, oos_end)
        & data[feature_col].abs().ge(activation_z)
    ].sort_values("date")

    events: list[dict[str, object]] = []
    last_exit = pd.Timestamp.min
    for event in triggers.itertuples(index=False):
        signal_date = pd.Timestamp(event.date)
        if signal_date <= last_exit:
            continue
        future_dates = oos_dates[oos_dates > signal_date]
        if future_dates.empty:
            continue
        entry_date = pd.Timestamp(future_dates.min())
        planned_idx = min(oos_dates.get_loc(entry_date) + horizon_days - 1, len(oos_dates) - 1)
        planned_exit_date = pd.Timestamp(oos_dates[planned_idx])
        exit_date = min(planned_exit_date, oos_end)
        side = float(np.sign(float(getattr(event, feature_col))) * direction_sign)
        if side == 0:
            continue
        last_exit = exit_date
        events.append(
            {
                "event_id": "",
                "selection_quarter": str(row["quarter"]),
                "oos_quarter": oos_quarter,
                "signal_date": signal_date,
                "entry_date": entry_date,
                "planned_exit_date": planned_exit_date,
                "exit_date": exit_date,
                "ticker": ticker,
                "feature": feature,
                "feature_hypothesis_family": row.get("feature_hypothesis_family", ""),
                "state_hypothesis": row.get("state_hypothesis", ""),
                "horizon_days": horizon_days,
                "direction_sign": direction_sign,
                "feature_z": float(getattr(event, feature_col)),
                "side": side,
                "activation_z": activation_z,
                "return_column": return_column,
                "v3_taxonomy_verdict": row.get("v3_taxonomy_verdict", ""),
                "v3_taxonomy_flags": row.get("v3_taxonomy_flags", ""),
                "robust_min_calmar": row.get("robust_min_calmar", np.nan),
                "full_calmar": row.get("full_calmar", np.nan),
                "exposure_role": row.get("exposure_role", ""),
                "economic_channel": row.get("economic_channel", ""),
            }
        )
    return events


def _stats_from_daily_pnl(daily: pd.DataFrame, pnl_col: str) -> dict[str, object]:
    if daily.empty or pnl_col not in daily.columns:
        return {
            "active_days": 0,
            f"{pnl_col}_total_pnl": np.nan,
            f"{pnl_col}_sharpe": np.nan,
            f"{pnl_col}_max_drawdown": np.nan,
            f"{pnl_col}_calmar": np.nan,
            f"{pnl_col}_annualized_return": np.nan,
            f"{pnl_col}_annualized_volatility": np.nan,
        }
    stats = _daily_pnl_stats(daily[pnl_col])
    return {
        "active_days": int(len(daily)),
        f"{pnl_col}_total_pnl": stats["total_pnl"],
        f"{pnl_col}_sharpe": stats["sharpe"],
        f"{pnl_col}_max_drawdown": stats["max_drawdown"],
        f"{pnl_col}_calmar": stats["calmar"],
        f"{pnl_col}_annualized_return": stats["annualized_return"],
        f"{pnl_col}_annualized_volatility": stats["annualized_volatility"],
    }


def _merged_event_cluster(cluster: list[pd.Series]) -> dict[str, object]:
    frame = pd.DataFrame(cluster)
    frame["robust_min_calmar"] = pd.to_numeric(frame["robust_min_calmar"], errors="coerce")
    best_idx = frame["robust_min_calmar"].fillna(-np.inf).idxmax()
    best = frame.loc[best_idx].to_dict()
    best["signal_date"] = pd.to_datetime(frame["signal_date"], utc=False).min()
    best["entry_date"] = pd.to_datetime(frame["entry_date"], utc=False).min()
    best["planned_exit_date"] = pd.to_datetime(frame["planned_exit_date"], utc=False).max()
    best["exit_date"] = pd.to_datetime(frame["exit_date"], utc=False).max()
    best["merged_event_count"] = int(len(frame))
    best["dropped_duplicate_count"] = int(max(len(frame) - 1, 0))
    best["merged_features"] = ",".join(sorted(set(frame["feature"].astype(str))))
    return best


def _collapse_overlapping_events(events: pd.DataFrame) -> pd.DataFrame:
    if events.empty:
        return events.copy()
    events = events.copy()
    for col in ["signal_date", "entry_date", "planned_exit_date", "exit_date"]:
        events[col] = pd.to_datetime(events[col], utc=False)
    events["robust_min_calmar"] = pd.to_numeric(events["robust_min_calmar"], errors="coerce")

    rows: list[dict[str, object]] = []
    group_cols = ["oos_quarter", "ticker", "state_hypothesis", "side"]
    for _, group in events.sort_values(["entry_date", "exit_date"]).groupby(group_cols, dropna=False, sort=True):
        cluster: list[pd.Series] = []
        cluster_exit = pd.Timestamp.min
        for _, row in group.iterrows():
            entry = pd.Timestamp(row["entry_date"])
            exit_date = pd.Timestamp(row["exit_date"])
            if not cluster:
                cluster = [row]
                cluster_exit = exit_date
                continue
            if entry <= cluster_exit:
                cluster.append(row)
                cluster_exit = max(cluster_exit, exit_date)
                continue
            rows.append(_merged_event_cluster(cluster))
            cluster = [row]
            cluster_exit = exit_date
        if cluster:
            rows.append(_merged_event_cluster(cluster))

    return pd.DataFrame(rows).sort_values(["oos_quarter", "signal_date", "ticker", "feature"]).reset_index(drop=True)


def run_curve_first_oos(
    taxonomy_frames: list[pd.DataFrame],
    cache: pd.DataFrame,
    verdicts: set[str],
    return_columns: list[str],
    activation_z: float = 1.5,
    weighting: str = "equal",
    collapse_same_ticker_state: bool = True,
    oos_mode: str = "next-quarter",
    oos_end_quarter: str | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    if weighting != "equal":
        raise ValueError("Only equal weighting is currently supported")
    if not taxonomy_frames:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    candidates = pd.concat(taxonomy_frames, ignore_index=True)
    if candidates.empty:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    candidates["ticker"] = candidates["ticker"].astype(str).str.upper().str.strip()
    candidates = candidates[candidates["v3_taxonomy_verdict"].astype(str).isin(verdicts)].copy()
    if candidates.empty:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    oos_quarters = sorted(
        {
            quarter
            for selection_quarter in candidates["quarter"].dropna().astype(str)
            for quarter in _oos_quarters_for_selection(selection_quarter, oos_mode, oos_end_quarter)
        }
    )

    cache = cache.copy()
    cache["ticker"] = cache["ticker"].astype(str).str.upper().str.strip()
    cache["date"] = pd.to_datetime(cache["date"], utc=False)
    for col in return_columns:
        if col not in cache.columns:
            raise ValueError(f"Cache is missing return column: {col}")
        cache[col] = pd.to_numeric(cache[col], errors="coerce").fillna(0.0)

    event_rows: list[dict[str, object]] = []
    for _, row in candidates.iterrows():
        for oos_quarter in _oos_quarters_for_selection(str(row["quarter"]), oos_mode, oos_end_quarter):
            event_rows.extend(
                _build_oos_events_for_candidate(
                    cache=cache,
                    row=row,
                    oos_quarter=oos_quarter,
                    return_column=return_columns[0],
                    activation_z=activation_z,
                )
            )
    events = pd.DataFrame(event_rows)
    if events.empty:
        calendar_rows: list[pd.DataFrame] = []
        calendar = pd.Index(sorted(cache["date"].dropna().unique()))
        for quarter in oos_quarters:
            dates = _oos_active_dates(calendar, quarter)
            if dates.empty:
                continue
            calendar_rows.append(pd.DataFrame({"date": dates, "oos_quarter": quarter}))
        if not calendar_rows:
            return events, pd.DataFrame(), pd.DataFrame()
        portfolio_daily = pd.concat(calendar_rows, ignore_index=True)
        portfolio_daily["active_events"] = 0
        portfolio_daily["active_tickers"] = 0
        portfolio_daily["gross_exposure"] = 0.0
        portfolio_daily["net_exposure"] = 0.0
        pnl_cols = [f"pnl__{col}" for col in return_columns]
        for col in pnl_cols:
            portfolio_daily[col] = 0.0
        summary_rows: list[dict[str, object]] = []
        for quarter, group in portfolio_daily.groupby("oos_quarter", sort=True):
            row: dict[str, object] = {
                "oos_quarter": quarter,
                "start_date": group["date"].min(),
                "end_date": group["date"].max(),
                "event_count": 0,
                "ticker_count": 0,
                "avg_active_events": 0.0,
                "avg_active_tickers": 0.0,
            }
            for col in pnl_cols:
                row.update(_stats_from_daily_pnl(group, col))
            summary_rows.append(row)
        return events, portfolio_daily, pd.DataFrame(summary_rows)
    events = events.sort_values(["oos_quarter", "signal_date", "ticker", "feature"]).reset_index(drop=True)
    if collapse_same_ticker_state:
        events = _collapse_overlapping_events(events)
    else:
        events["merged_event_count"] = 1
        events["dropped_duplicate_count"] = 0
        events["merged_features"] = events["feature"].astype(str)
    events["event_id"] = [f"V3OOS-{i:06d}" for i in range(1, len(events) + 1)]

    daily_rows: list[pd.DataFrame] = []
    for event in events.itertuples(index=False):
        ticker_data = cache[cache["ticker"].eq(event.ticker)].copy()
        active = ticker_data[ticker_data["date"].between(event.entry_date, event.exit_date)].copy()
        if active.empty:
            continue
        frame = active[["date", "ticker", *return_columns]].copy()
        frame["event_id"] = event.event_id
        frame["selection_quarter"] = event.selection_quarter
        frame["oos_quarter"] = event.oos_quarter
        frame["feature"] = event.feature
        frame["feature_hypothesis_family"] = event.feature_hypothesis_family
        frame["state_hypothesis"] = event.state_hypothesis
        frame["side"] = event.side
        frame["entry_date"] = event.entry_date
        frame["exit_date"] = event.exit_date
        daily_rows.append(frame)

    if not daily_rows:
        return events, pd.DataFrame(), pd.DataFrame()
    stock_daily = pd.concat(daily_rows, ignore_index=True)
    weighted_frames: list[pd.DataFrame] = []
    for date, group in stock_daily.groupby("date", sort=True):
        g = group.copy()
        gross = g["side"].abs().sum()
        g["weight"] = np.where(gross > 0, g["side"] / gross, 0.0)
        for col in return_columns:
            g[f"pnl__{col}"] = g["weight"] * g[col]
        weighted_frames.append(g)
    stock_daily = pd.concat(weighted_frames, ignore_index=True)

    pnl_cols = [f"pnl__{col}" for col in return_columns]
    portfolio_daily = (
        stock_daily.groupby("date", as_index=False)
        .agg(
            oos_quarter=("oos_quarter", "last"),
            active_events=("event_id", "nunique"),
            active_tickers=("ticker", "nunique"),
            gross_exposure=("weight", lambda s: float(s.abs().sum())),
            net_exposure=("weight", "sum"),
            **{col: (col, "sum") for col in pnl_cols},
        )
        .sort_values("date")
        .reset_index(drop=True)
    )
    calendar = pd.Index(sorted(cache["date"].dropna().unique()))
    calendar_rows = []
    for quarter in oos_quarters:
        dates = _oos_active_dates(calendar, quarter)
        if dates.empty:
            continue
        calendar_rows.append(pd.DataFrame({"date": dates, "oos_quarter": quarter}))
    if calendar_rows:
        full_calendar = pd.concat(calendar_rows, ignore_index=True)
        portfolio_daily = full_calendar.merge(portfolio_daily, on=["date", "oos_quarter"], how="left")
        fill_zero_cols = ["active_events", "active_tickers", "gross_exposure", "net_exposure", *pnl_cols]
        for col in fill_zero_cols:
            portfolio_daily[col] = pd.to_numeric(portfolio_daily[col], errors="coerce").fillna(0.0)
        portfolio_daily["active_events"] = portfolio_daily["active_events"].astype(int)
        portfolio_daily["active_tickers"] = portfolio_daily["active_tickers"].astype(int)

    summary_rows: list[dict[str, object]] = []
    for quarter, group in portfolio_daily.groupby("oos_quarter", sort=True):
        row: dict[str, object] = {
            "oos_quarter": quarter,
            "start_date": group["date"].min(),
            "end_date": group["date"].max(),
            "event_count": int(events[events["oos_quarter"].eq(quarter)]["event_id"].nunique()),
            "ticker_count": int(events[events["oos_quarter"].eq(quarter)]["ticker"].nunique()),
            "avg_active_events": float(group["active_events"].mean()),
            "avg_active_tickers": float(group["active_tickers"].mean()),
        }
        for col in pnl_cols:
            row.update(_stats_from_daily_pnl(group, col))
        summary_rows.append(row)
    all_row: dict[str, object] = {
        "oos_quarter": "ALL",
        "start_date": portfolio_daily["date"].min(),
        "end_date": portfolio_daily["date"].max(),
        "event_count": int(events["event_id"].nunique()),
        "ticker_count": int(events["ticker"].nunique()),
        "avg_active_events": float(portfolio_daily["active_events"].mean()),
        "avg_active_tickers": float(portfolio_daily["active_tickers"].mean()),
    }
    for col in pnl_cols:
        all_row.update(_stats_from_daily_pnl(portfolio_daily, col))
    summary_rows.append(all_row)

    return events, portfolio_daily, pd.DataFrame(summary_rows)


def run_curve_first_oos_from_paths(
    taxonomy_paths: list[Path],
    cache_path: Path,
    events_output_path: Path,
    daily_output_path: Path,
    summary_output_path: Path,
    verdicts: list[str],
    return_columns: list[str],
    activation_z: float = 1.5,
    weighting: str = "equal",
    collapse_same_ticker_state: bool = True,
    oos_mode: str = "next-quarter",
    oos_end_quarter: str | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    frames = [load_frame(path) for path in taxonomy_paths]
    cache = load_frame(cache_path)
    events, daily, summary = run_curve_first_oos(
        taxonomy_frames=frames,
        cache=cache,
        verdicts=set(verdicts),
        return_columns=return_columns,
            activation_z=activation_z,
            weighting=weighting,
            collapse_same_ticker_state=collapse_same_ticker_state,
            oos_mode=oos_mode,
            oos_end_quarter=oos_end_quarter,
        )
    _write_frame(events, events_output_path)
    _write_frame(daily, daily_output_path)
    _write_frame(summary, summary_output_path)
    return events, daily, summary
