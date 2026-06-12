from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


OPENBB_NUMERIC_METRICS = [
    "market_cap",
    "pe_ratio",
    "forward_pe",
    "peg_ratio",
    "peg_ratio_ttm",
    "enterprise_to_ebitda",
    "enterprise_to_revenue",
    "revenue_growth",
    "quick_ratio",
    "current_ratio",
    "debt_to_equity",
    "gross_margin",
    "operating_margin",
    "ebitda_margin",
    "profit_margin",
    "return_on_assets",
    "return_on_equity",
    "payout_ratio",
    "price_to_book",
    "overall_risk",
    "beta",
    "price_return_1y",
    "earnings_growth",
    "earnings_growth_quarterly",
    "dividend_yield",
]

FUNDAMENTAL_SNAPSHOT_COLUMNS = [
    "symbol",
    "snapshot_date",
    "tradable_after",
    "source_name",
    "provider",
    "currency",
    "market_cap",
    "enterprise_value",
    "revenue_growth",
    "earnings_growth",
    "gross_margin",
    "operating_margin",
    "profit_margin",
    "return_on_assets",
    "return_on_equity",
    "current_ratio",
    "quick_ratio",
    "debt_to_equity",
    "forward_pe",
    "enterprise_to_ebitda",
    "enterprise_to_revenue",
    "price_to_book",
    "dividend_yield_normalized",
    "valuation_score",
    "quality_score",
    "growth_score",
    "balance_sheet_score",
    "dividend_short_cost_score",
    "fundamental_score",
    "fundamental_gate",
    "fundamental_flags",
    "primary_commodity",
    "primary_exposure_role",
    "primary_prior_weight",
    "primary_taxonomy_bucket",
    "primary_alpha_priority",
    "commodity_roles",
    "edgar_metric_count",
]

FUNDAMENTAL_FACTOR_COLUMNS = [
    "symbol",
    "date",
    "tradable_after",
    "source_name",
    "provider",
    "metric",
    "value",
    "unit",
    "source_detail",
    "quality_flag",
]

AGRICULTURE_EVENT_COLUMNS = [
    "event_date",
    "tradable_after",
    "source_name",
    "source_type",
    "report_type",
    "commodity",
    "metric",
    "metric_detail",
    "value",
    "unit",
    "reference",
    "series_id",
    "value_yoy_change",
    "value_vs_trailing_avg",
    "value_vs_five_year_avg",
    "value_vs_previous_year",
    "commodity_pressure",
    "timestamp_quality",
    "publication_url",
]

COMMODITY_CONFIRMATION_COLUMNS = [
    "commodity",
    "date",
    "tradable_after",
    "source_type",
    "source_name",
    "metric",
    "value",
    "unit",
    "weekly_change",
    "seasonal_surprise",
    "seasonal_zscore",
    "positioning_percentile_3y",
    "confirmation_pressure",
    "confirmation_strength",
    "confirmation_flag",
    "timestamp_quality",
    "source_detail",
]


def _read_optional_frame(path: Path | None) -> pd.DataFrame:
    if path is None or not path.exists():
        return pd.DataFrame()
    if path.suffix == ".parquet":
        return pd.read_parquet(path)
    if path.suffix == ".json":
        return pd.read_json(path)
    return pd.read_csv(path)


def _write_frame(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix == ".parquet":
        df.to_parquet(output_path, index=False)
    elif output_path.suffix == ".csv":
        df.to_csv(output_path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")


def _empty_frame(columns: list[str]) -> pd.DataFrame:
    return pd.DataFrame(columns=columns)


def _clean_symbol(series: pd.Series) -> pd.Series:
    return series.astype(str).str.upper().str.strip()


def _to_numeric(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    out = df.copy()
    for col in columns:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")
    return out


def _coerce_datetime(series: pd.Series) -> pd.Series:
    dt = pd.to_datetime(series, errors="coerce", utc=True)
    if isinstance(dt, pd.Series):
        return dt.dt.tz_convert(None)
    return pd.Series(dt).dt.tz_convert(None)


def _robust_z(series: pd.Series) -> pd.Series:
    x = pd.to_numeric(series, errors="coerce")
    median = x.median(skipna=True)
    mad = (x - median).abs().median(skipna=True)
    if pd.isna(median) or pd.isna(mad) or mad == 0:
        std = x.std(skipna=True)
        if pd.isna(std) or std == 0:
            return pd.Series(np.nan, index=series.index)
        return (x - x.mean(skipna=True)) / std
    return (x - median) / (1.4826 * mad)


def _mean_existing(df: pd.DataFrame, columns: list[str]) -> pd.Series:
    existing = [col for col in columns if col in df.columns]
    if not existing:
        return pd.Series(np.nan, index=df.index)
    return df[existing].mean(axis=1, skipna=True)


def _normalize_dividend_yield(value: object) -> float:
    number = pd.to_numeric(pd.Series([value]), errors="coerce").iloc[0]
    if pd.isna(number):
        return np.nan
    # OpenBB/yfinance can return either 0.012 or 1.2 for 1.2%.
    # Values between 0.2 and 1.0 are implausibly high as decimals for this
    # universe and are usually percentage points, for example 0.37 = 0.37%.
    if number > 0.2:
        return float(number) / 100.0
    return float(number)


def _latest_by_symbol(df: pd.DataFrame, date_column: str) -> pd.DataFrame:
    if df.empty or "symbol" not in df.columns:
        return pd.DataFrame()
    out = df.copy()
    if date_column in out.columns:
        out[date_column] = _coerce_datetime(out[date_column])
        out = out.sort_values(["symbol", date_column])
    return out.drop_duplicates("symbol", keep="last").reset_index(drop=True)


def _exposure_summary(exposure_map: pd.DataFrame, role_taxonomy: pd.DataFrame | None) -> pd.DataFrame:
    if exposure_map.empty or "ticker" not in exposure_map.columns:
        return pd.DataFrame(columns=["symbol"])

    exposure = exposure_map.copy()
    exposure["symbol"] = _clean_symbol(exposure["ticker"])
    exposure["commodity"] = exposure["commodity"].astype(str).str.upper().str.strip()
    exposure["exposure_role"] = exposure["exposure_role"].astype(str).str.strip()
    exposure["prior_weight"] = pd.to_numeric(exposure["prior_weight"], errors="coerce")
    exposure["abs_prior_weight"] = exposure["prior_weight"].abs()
    exposure = exposure.sort_values(["symbol", "abs_prior_weight"], ascending=[True, False])

    primary = exposure.drop_duplicates("symbol", keep="first")[
        ["symbol", "commodity", "exposure_role", "prior_weight"]
    ].rename(
        columns={
            "commodity": "primary_commodity",
            "exposure_role": "primary_exposure_role",
            "prior_weight": "primary_prior_weight",
        }
    )

    roles = (
        exposure.groupby("symbol")
        .apply(
            lambda g: ";".join(
                f"{row.commodity}:{row.exposure_role}:{row.prior_weight:g}"
                for row in g.itertuples(index=False)
            ),
            include_groups=False,
        )
        .reset_index(name="commodity_roles")
    )

    out = primary.merge(roles, on="symbol", how="left")
    if role_taxonomy is not None and not role_taxonomy.empty:
        taxonomy = role_taxonomy.copy()
        taxonomy["commodity"] = taxonomy["commodity"].astype(str).str.upper().str.strip()
        taxonomy["exposure_role"] = taxonomy["exposure_role"].astype(str).str.strip()
        taxonomy = taxonomy.rename(
            columns={
                "commodity": "primary_commodity",
                "exposure_role": "primary_exposure_role",
                "taxonomy_bucket": "primary_taxonomy_bucket",
                "alpha_priority": "primary_alpha_priority",
            }
        )
        out = out.merge(
            taxonomy[
                [
                    "primary_commodity",
                    "primary_exposure_role",
                    "primary_taxonomy_bucket",
                    "primary_alpha_priority",
                ]
            ].drop_duplicates(),
            on=["primary_commodity", "primary_exposure_role"],
            how="left",
        )
    return out


def _build_openbb_factors(openbb: pd.DataFrame) -> pd.DataFrame:
    if openbb.empty or "symbol" not in openbb.columns:
        return _empty_frame(FUNDAMENTAL_FACTOR_COLUMNS)

    factors: list[pd.DataFrame] = []
    base = openbb.copy()
    base["symbol"] = _clean_symbol(base["symbol"])
    source_name = base.get("source_name", "openbb_equity_fundamental_metrics")
    provider = base.get("provider", "openbb")
    tradable_after = _coerce_datetime(base["fetched_at"]) if "fetched_at" in base.columns else pd.NaT
    date = pd.Series(tradable_after).dt.normalize() if not isinstance(tradable_after, pd.Timestamp) else tradable_after

    numeric_cols = [col for col in OPENBB_NUMERIC_METRICS if col in base.columns]
    for metric in numeric_cols:
        factor = pd.DataFrame(
            {
                "symbol": base["symbol"],
                "date": date,
                "tradable_after": tradable_after,
                "source_name": source_name,
                "provider": provider,
                "metric": metric,
                "value": pd.to_numeric(base[metric], errors="coerce"),
                "unit": "",
                "source_detail": "openbb_equity_fundamental_metrics",
                "quality_flag": "",
            }
        )
        factors.append(factor)

    if not factors:
        return _empty_frame(FUNDAMENTAL_FACTOR_COLUMNS)
    out = pd.concat(factors, ignore_index=True)
    return out[FUNDAMENTAL_FACTOR_COLUMNS].dropna(subset=["value"]).reset_index(drop=True)


def _build_edgar_factors(edgar: pd.DataFrame) -> pd.DataFrame:
    if edgar.empty or not {"symbol", "metric", "value"}.issubset(edgar.columns):
        return _empty_frame(FUNDAMENTAL_FACTOR_COLUMNS)

    out = pd.DataFrame(
        {
            "symbol": _clean_symbol(edgar["symbol"]),
            "date": _coerce_datetime(edgar["source_end"]) if "source_end" in edgar.columns else pd.NaT,
            "tradable_after": _coerce_datetime(edgar["availability_date"])
            if "availability_date" in edgar.columns
            else pd.NaT,
            "source_name": "edgar_companyfacts",
            "provider": "sec_companyfacts",
            "metric": edgar["metric"].astype(str),
            "value": pd.to_numeric(edgar["value"], errors="coerce"),
            "unit": "",
            "source_detail": edgar["source_concept"].astype(str) if "source_concept" in edgar.columns else "",
            "quality_flag": "",
        }
    )
    return out[FUNDAMENTAL_FACTOR_COLUMNS].dropna(subset=["value"]).reset_index(drop=True)


def _build_snapshot_from_openbb(
    openbb: pd.DataFrame,
    exposure_map: pd.DataFrame,
    role_taxonomy: pd.DataFrame,
    edgar_factors: pd.DataFrame,
    min_market_cap: float,
) -> pd.DataFrame:
    if openbb.empty or "symbol" not in openbb.columns:
        snapshot = pd.DataFrame()
    else:
        openbb = openbb.copy()
        openbb["symbol"] = _clean_symbol(openbb["symbol"])
        openbb = _to_numeric(openbb, OPENBB_NUMERIC_METRICS + ["enterprise_value"])
        date_col = "fetched_at" if "fetched_at" in openbb.columns else "symbol"
        snapshot = _latest_by_symbol(openbb, date_col)
        if "fetched_at" in snapshot.columns:
            snapshot["tradable_after"] = _coerce_datetime(snapshot["fetched_at"])
            snapshot["snapshot_date"] = snapshot["tradable_after"].dt.normalize()
        else:
            snapshot["tradable_after"] = pd.NaT
            snapshot["snapshot_date"] = pd.NaT

        snapshot["source_name"] = snapshot.get("source_name", "openbb_equity_fundamental_metrics")
        snapshot["provider"] = snapshot.get("provider", "openbb")
        snapshot["dividend_yield_normalized"] = snapshot.get("dividend_yield", np.nan).map(_normalize_dividend_yield)

        snapshot["forward_earnings_yield"] = np.where(
            snapshot.get("forward_pe", np.nan) > 0,
            1.0 / snapshot.get("forward_pe", np.nan),
            np.nan,
        )
        snapshot["ev_ebitda_yield"] = np.where(
            snapshot.get("enterprise_to_ebitda", np.nan) > 0,
            1.0 / snapshot.get("enterprise_to_ebitda", np.nan),
            np.nan,
        )
        snapshot["ev_sales_yield"] = np.where(
            snapshot.get("enterprise_to_revenue", np.nan) > 0,
            1.0 / snapshot.get("enterprise_to_revenue", np.nan),
            np.nan,
        )

        score = snapshot.copy()
        for col in [
            "forward_earnings_yield",
            "ev_ebitda_yield",
            "ev_sales_yield",
            "gross_margin",
            "operating_margin",
            "profit_margin",
            "return_on_assets",
            "return_on_equity",
            "revenue_growth",
            "earnings_growth",
            "earnings_growth_quarterly",
            "current_ratio",
            "quick_ratio",
            "debt_to_equity",
            "dividend_yield_normalized",
        ]:
            if col in score.columns:
                score[f"{col}_z"] = _robust_z(score[col]).clip(-3.0, 3.0)

        snapshot["valuation_score"] = _mean_existing(
            score,
            ["forward_earnings_yield_z", "ev_ebitda_yield_z", "ev_sales_yield_z"],
        )
        snapshot["quality_score"] = _mean_existing(
            score,
            [
                "gross_margin_z",
                "operating_margin_z",
                "profit_margin_z",
                "return_on_assets_z",
                "return_on_equity_z",
            ],
        )
        snapshot["growth_score"] = _mean_existing(
            score,
            ["revenue_growth_z", "earnings_growth_z", "earnings_growth_quarterly_z"],
        )
        snapshot["balance_sheet_score"] = _mean_existing(
            score.assign(debt_to_equity_inverse_z=-score.get("debt_to_equity_z", np.nan)),
            ["current_ratio_z", "quick_ratio_z", "debt_to_equity_inverse_z"],
        )
        snapshot["dividend_short_cost_score"] = -score.get("dividend_yield_normalized_z", np.nan)
        snapshot["fundamental_score"] = (
            0.25 * snapshot["valuation_score"].fillna(0.0)
            + 0.35 * snapshot["quality_score"].fillna(0.0)
            + 0.25 * snapshot["growth_score"].fillna(0.0)
            + 0.15 * snapshot["balance_sheet_score"].fillna(0.0)
        )

        flags: list[list[str]] = []
        gates: list[str] = []
        for row in snapshot.itertuples(index=False):
            row_flags: list[str] = []
            market_cap = getattr(row, "market_cap", np.nan)
            if pd.notna(market_cap) and market_cap < min_market_cap:
                row_flags.append("small_market_cap")
            current_ratio = getattr(row, "current_ratio", np.nan)
            debt_to_equity = getattr(row, "debt_to_equity", np.nan)
            if pd.notna(current_ratio) and current_ratio < 0.8:
                row_flags.append("weak_current_ratio")
            if pd.notna(debt_to_equity) and debt_to_equity > 250:
                row_flags.append("high_debt_to_equity")
            profit_margin = getattr(row, "profit_margin", np.nan)
            operating_margin = getattr(row, "operating_margin", np.nan)
            if pd.notna(profit_margin) and pd.notna(operating_margin) and profit_margin < -0.2 and operating_margin < -0.2:
                row_flags.append("deep_negative_margins")
            ev_sales = getattr(row, "enterprise_to_revenue", np.nan)
            if pd.notna(ev_sales) and pd.notna(profit_margin) and ev_sales > 20 and profit_margin < 0.05:
                row_flags.append("valuation_requires_narrative")
            dividend_yield = getattr(row, "dividend_yield_normalized", np.nan)
            if pd.notna(dividend_yield) and dividend_yield > 0.04:
                row_flags.append("high_dividend_short_cost")

            if any(flag in row_flags for flag in ["small_market_cap", "deep_negative_margins"]):
                gates.append("block")
            elif row_flags:
                gates.append("review")
            else:
                gates.append("pass")
            flags.append(row_flags)

        snapshot["fundamental_gate"] = gates
        snapshot["fundamental_flags"] = [";".join(items) for items in flags]

    edgar_counts = pd.DataFrame(columns=["symbol", "edgar_metric_count"])
    if not edgar_factors.empty and "symbol" in edgar_factors.columns:
        edgar_counts = (
            edgar_factors.assign(symbol=_clean_symbol(edgar_factors["symbol"]))
            .groupby("symbol")["metric"]
            .nunique()
            .reset_index(name="edgar_metric_count")
        )
        if snapshot.empty:
            snapshot = edgar_counts[["symbol"]].copy()
            snapshot["snapshot_date"] = pd.NaT
            snapshot["tradable_after"] = pd.NaT
            snapshot["source_name"] = "edgar_companyfacts"
            snapshot["provider"] = "sec_companyfacts"
            snapshot["fundamental_gate"] = "review"
            snapshot["fundamental_flags"] = "edgar_only_no_openbb_metrics"

    exposure = _exposure_summary(exposure_map, role_taxonomy)
    if not snapshot.empty and not exposure.empty:
        snapshot = snapshot.merge(exposure, on="symbol", how="left")
    if not snapshot.empty and not edgar_counts.empty:
        snapshot = snapshot.merge(edgar_counts, on="symbol", how="left")

    for col in FUNDAMENTAL_SNAPSHOT_COLUMNS:
        if col not in snapshot.columns:
            snapshot[col] = np.nan
    snapshot["edgar_metric_count"] = pd.to_numeric(snapshot["edgar_metric_count"], errors="coerce").fillna(0).astype(int)
    return snapshot[FUNDAMENTAL_SNAPSHOT_COLUMNS].sort_values("symbol").reset_index(drop=True)


def build_fundamental_snapshot_from_paths(
    openbb_metrics_path: Path | None,
    edgar_factors_path: Path | None,
    exposure_map_path: Path,
    role_taxonomy_path: Path | None,
    output_snapshot_path: Path,
    output_factors_path: Path,
    min_market_cap: float = 500_000_000.0,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    openbb = _read_optional_frame(openbb_metrics_path)
    edgar = _read_optional_frame(edgar_factors_path)
    exposure_map = _read_optional_frame(exposure_map_path)
    role_taxonomy = _read_optional_frame(role_taxonomy_path)

    openbb_factors = _build_openbb_factors(openbb)
    edgar_factor_rows = _build_edgar_factors(edgar)
    factors = pd.concat([openbb_factors, edgar_factor_rows], ignore_index=True)
    if factors.empty:
        factors = _empty_frame(FUNDAMENTAL_FACTOR_COLUMNS)
    else:
        factors = factors[FUNDAMENTAL_FACTOR_COLUMNS].sort_values(["symbol", "metric", "tradable_after"])

    snapshot = _build_snapshot_from_openbb(
        openbb=openbb,
        exposure_map=exposure_map,
        role_taxonomy=role_taxonomy,
        edgar_factors=edgar_factor_rows,
        min_market_cap=min_market_cap,
    )

    _write_frame(snapshot, output_snapshot_path)
    _write_frame(factors, output_factors_path)
    return snapshot, factors


def _pressure_from_nass(row: pd.Series) -> float:
    metric = str(row.get("metric", "")).lower()
    surprise = pd.to_numeric(row.get("value_vs_trailing_avg"), errors="coerce")
    if pd.isna(surprise):
        surprise = pd.to_numeric(row.get("value_yoy_change"), errors="coerce")
    if pd.isna(surprise) or surprise == 0:
        return np.nan
    if metric in {"yield", "production", "area_harvested", "stocks"}:
        return -float(np.sign(surprise))
    return np.nan


def _normalize_nass(nass: pd.DataFrame) -> pd.DataFrame:
    if nass.empty:
        return _empty_frame(AGRICULTURE_EVENT_COLUMNS)

    out = pd.DataFrame(
        {
            "event_date": _coerce_datetime(nass["date"]) if "date" in nass.columns else pd.NaT,
            "tradable_after": _coerce_datetime(nass["load_time"]) if "load_time" in nass.columns else pd.NaT,
            "source_name": "nass_quickstats",
            "source_type": "nass",
            "report_type": nass.get("reference_period_desc", "nass").astype(str),
            "commodity": nass["commodity"].astype(str).str.upper().str.strip(),
            "metric": nass["metric"].astype(str),
            "metric_detail": nass.get("metric_detail", "").astype(str),
            "value": pd.to_numeric(nass["value"], errors="coerce"),
            "unit": nass.get("unit", "").astype(str),
            "reference": nass.get("short_desc", "").astype(str),
            "series_id": nass.get("series_id", "").astype(str),
            "value_yoy_change": pd.to_numeric(nass.get("value_yoy_change", np.nan), errors="coerce"),
            "value_vs_trailing_avg": pd.to_numeric(nass.get("value_vs_trailing_avg", np.nan), errors="coerce"),
            "value_vs_five_year_avg": np.nan,
            "value_vs_previous_year": np.nan,
            "timestamp_quality": np.where(nass.get("load_time", pd.Series(index=nass.index)).notna(), "load_time", "date_only"),
            "publication_url": "",
        }
    )
    out["commodity_pressure"] = out.apply(_pressure_from_nass, axis=1)
    return out[AGRICULTURE_EVENT_COLUMNS].dropna(subset=["value"]).reset_index(drop=True)


def _normalize_usda_reports(usda: pd.DataFrame, tradable_hour_utc: int = 18) -> pd.DataFrame:
    if usda.empty:
        return _empty_frame(AGRICULTURE_EVENT_COLUMNS)

    base = usda.copy()
    base["event_date"] = _coerce_datetime(base["report_date"]) if "report_date" in base.columns else pd.NaT
    base["tradable_after"] = base["event_date"] + pd.to_timedelta(tradable_hour_utc, unit="h")
    base["commodity"] = base["commodity"].astype(str).str.upper().str.strip()
    base["metric"] = base["metric"].astype(str)
    base["value"] = pd.to_numeric(base["value"], errors="coerce")
    base["base_metric"] = base["metric"].str.replace(
        "_(current|five_year_avg|previous_year|previous_week)$",
        "",
        regex=True,
    )
    base["value_vs_five_year_avg"] = np.nan
    base["value_vs_previous_year"] = np.nan

    keys = ["event_date", "source_name", "report_type", "commodity", "period", "reference", "base_metric"]
    for idx, row in base.iterrows():
        metric = str(row.metric)
        if not metric.endswith("_current"):
            continue
        mask = pd.Series(True, index=base.index)
        for key in keys:
            mask &= base[key].astype(str).eq(str(row[key]))
        peers = base[mask]
        five_year = peers[peers["metric"].str.endswith("_five_year_avg")]["value"]
        previous_year = peers[peers["metric"].str.endswith("_previous_year")]["value"]
        value = row["value"]
        base.loc[idx, "value_vs_five_year_avg"] = value - five_year.iloc[0] if not five_year.empty else np.nan
        base.loc[idx, "value_vs_previous_year"] = value - previous_year.iloc[0] if not previous_year.empty else np.nan

    out = pd.DataFrame(
        {
            "event_date": base["event_date"],
            "tradable_after": base["tradable_after"],
            "source_name": base.get("source_name", "usda_report").astype(str),
            "source_type": "usda_report",
            "report_type": base.get("report_type", "").astype(str),
            "commodity": base["commodity"],
            "metric": base["metric"],
            "metric_detail": base["base_metric"],
            "value": base["value"],
            "unit": base.get("unit", "").astype(str),
            "reference": base.get("reference", "").astype(str),
            "series_id": base.get("series_id", "").astype(str),
            "value_yoy_change": np.nan,
            "value_vs_trailing_avg": np.nan,
            "value_vs_five_year_avg": base["value_vs_five_year_avg"],
            "value_vs_previous_year": base["value_vs_previous_year"],
            "timestamp_quality": "date_plus_default_report_hour",
            "publication_url": base.get("publication_url", "").astype(str),
        }
    )

    out["commodity_pressure"] = np.nan
    surprise = out["value_vs_five_year_avg"].fillna(out["value_vs_previous_year"])
    metric_lower = out["metric_detail"].astype(str).str.lower()
    supply_good = metric_lower.str.contains("condition_good|condition_excellent|planted|emerged|harvested", regex=True)
    supply_bad = metric_lower.str.contains("condition_poor|condition_very_poor", regex=True)
    out.loc[supply_good & surprise.notna(), "commodity_pressure"] = -np.sign(surprise[supply_good & surprise.notna()])
    out.loc[supply_bad & surprise.notna(), "commodity_pressure"] = np.sign(surprise[supply_bad & surprise.notna()])
    return out[AGRICULTURE_EVENT_COLUMNS].dropna(subset=["value"]).reset_index(drop=True)


def build_agriculture_fundamental_events_from_paths(
    nass_factors_path: Path | None,
    usda_report_factors_path: Path | None,
    output_path: Path,
    usda_tradable_hour_utc: int = 18,
) -> pd.DataFrame:
    nass = _read_optional_frame(nass_factors_path)
    usda = _read_optional_frame(usda_report_factors_path)
    events = pd.concat(
        [
            _normalize_nass(nass),
            _normalize_usda_reports(usda, tradable_hour_utc=usda_tradable_hour_utc),
        ],
        ignore_index=True,
    )
    if events.empty:
        events = _empty_frame(AGRICULTURE_EVENT_COLUMNS)
    else:
        events = events[AGRICULTURE_EVENT_COLUMNS].sort_values(
            ["commodity", "tradable_after", "source_type", "metric"]
        )
    _write_frame(events, output_path)
    return events


def _eia_pressure(field_name: str, seasonal_zscore: float, weekly_change: float) -> float:
    field = str(field_name).lower()
    score = seasonal_zscore
    if pd.isna(score):
        score = weekly_change
    if pd.isna(score) or score == 0:
        return np.nan
    sign = float(np.sign(score))
    if "stocks" in field or "storage" in field or "imports" in field or "production" in field:
        return -sign
    if "exports" in field or "product_supplied" in field or "utilization" in field:
        return sign
    if "price" in field:
        return sign
    return np.nan


def _normalize_eia_confirmation(eia: pd.DataFrame, tradable_lag_days: int = 1) -> pd.DataFrame:
    if eia.empty:
        return _empty_frame(COMMODITY_CONFIRMATION_COLUMNS)

    base = eia.copy()
    if "asset_link" not in base.columns:
        base["asset_link"] = "CL"
    base["commodity"] = base["asset_link"].astype(str).str.upper().str.strip()
    base["date"] = _coerce_datetime(base["date"]) if "date" in base.columns else pd.NaT
    base["tradable_after"] = base["date"] + pd.to_timedelta(tradable_lag_days, unit="D")
    base["field_name"] = base.get("field_name", "").astype(str)
    base["seasonal_zscore"] = pd.to_numeric(base.get("seasonal_zscore", np.nan), errors="coerce")
    base["weekly_change"] = pd.to_numeric(base.get("weekly_change", np.nan), errors="coerce")
    out = pd.DataFrame(
        {
            "commodity": base["commodity"],
            "date": base["date"],
            "tradable_after": base["tradable_after"],
            "source_type": "eia",
            "source_name": base.get("source_name", "eia_series_core").astype(str),
            "metric": base["field_name"],
            "value": pd.to_numeric(base.get("value", np.nan), errors="coerce"),
            "unit": base.get("units", "").astype(str),
            "weekly_change": base["weekly_change"],
            "seasonal_surprise": pd.to_numeric(base.get("seasonal_surprise", np.nan), errors="coerce"),
            "seasonal_zscore": base["seasonal_zscore"],
            "positioning_percentile_3y": np.nan,
            "confirmation_flag": "",
            "timestamp_quality": "date_plus_eia_lag",
            "source_detail": base.get("series_description", "").astype(str),
        }
    )
    out["confirmation_pressure"] = [
        _eia_pressure(field, zscore, weekly)
        for field, zscore, weekly in zip(base["field_name"], base["seasonal_zscore"], base["weekly_change"], strict=False)
    ]
    out["confirmation_strength"] = out["seasonal_zscore"].abs().fillna(out["weekly_change"].abs())
    return out[COMMODITY_CONFIRMATION_COLUMNS].dropna(subset=["value"]).reset_index(drop=True)


def _normalize_cftc_confirmation(cftc: pd.DataFrame, tradable_lag_days: int = 3) -> pd.DataFrame:
    if cftc.empty:
        return _empty_frame(COMMODITY_CONFIRMATION_COLUMNS)

    base = cftc.copy()
    base["commodity"] = base.get("symbol", "CL").astype(str).str.upper().str.strip()
    base["date"] = _coerce_datetime(base["report_date"]) if "report_date" in base.columns else pd.NaT
    base["tradable_after"] = base["date"] + pd.to_timedelta(tradable_lag_days, unit="D")
    metrics = [
        ("managed_money_net_oi_share", "managed_money_net_percentile_3y"),
        ("producer_merchant_net_oi_share", "producer_merchant_net_percentile_3y"),
        ("swap_dealer_net_oi_share", "swap_dealer_net_percentile_3y"),
        ("other_reportable_net_oi_share", "other_reportable_net_percentile_3y"),
        ("nonreportable_net_oi_share", "nonreportable_net_percentile_3y"),
    ]
    rows: list[pd.DataFrame] = []
    for metric, percentile_col in metrics:
        if metric not in base.columns:
            continue
        percentile = pd.to_numeric(base.get(percentile_col, np.nan), errors="coerce")
        value = pd.to_numeric(base[metric], errors="coerce")
        frame = pd.DataFrame(
            {
                "commodity": base["commodity"],
                "date": base["date"],
                "tradable_after": base["tradable_after"],
                "source_type": "cftc",
                "source_name": "cftc_disaggregated_futures",
                "metric": metric,
                "value": value,
                "unit": "oi_share",
                "weekly_change": pd.to_numeric(base.get(metric.replace("_oi_share", "_weekly_change"), np.nan), errors="coerce"),
                "seasonal_surprise": np.nan,
                "seasonal_zscore": np.nan,
                "positioning_percentile_3y": percentile,
                "confirmation_flag": "",
                "timestamp_quality": "report_date_plus_cftc_lag",
                "source_detail": base.get("market_and_exchange_names", "").astype(str),
            }
        )
        frame["confirmation_pressure"] = np.sign(value)
        frame["confirmation_strength"] = (percentile - 0.5).abs() * 2.0
        rows.append(frame)

    if not rows:
        return _empty_frame(COMMODITY_CONFIRMATION_COLUMNS)
    out = pd.concat(rows, ignore_index=True)
    crowded_long = (out["metric"].eq("managed_money_net_oi_share")) & (out["positioning_percentile_3y"] >= 0.9)
    crowded_short = (out["metric"].eq("managed_money_net_oi_share")) & (out["positioning_percentile_3y"] <= 0.1)
    out.loc[crowded_long, "confirmation_flag"] = "managed_money_crowded_long"
    out.loc[crowded_short, "confirmation_flag"] = "managed_money_crowded_short"
    return out[COMMODITY_CONFIRMATION_COLUMNS].dropna(subset=["value"]).reset_index(drop=True)


def build_commodity_confirmation_events_from_paths(
    eia_factors_path: Path | None,
    cftc_factors_path: Path | None,
    output_path: Path,
    commodity: str = "CL",
    eia_tradable_lag_days: int = 1,
    cftc_tradable_lag_days: int = 3,
) -> pd.DataFrame:
    keep = commodity.upper().strip()
    eia = _read_optional_frame(eia_factors_path)
    cftc = _read_optional_frame(cftc_factors_path)
    events = pd.concat(
        [
            _normalize_eia_confirmation(eia, tradable_lag_days=eia_tradable_lag_days),
            _normalize_cftc_confirmation(cftc, tradable_lag_days=cftc_tradable_lag_days),
        ],
        ignore_index=True,
    )
    if events.empty:
        events = _empty_frame(COMMODITY_CONFIRMATION_COLUMNS)
    else:
        events = events[events["commodity"].astype(str).str.upper().str.strip() == keep].copy()
        events = events[COMMODITY_CONFIRMATION_COLUMNS].sort_values(["commodity", "tradable_after", "source_type", "metric"])
    _write_frame(events, output_path)
    return events
