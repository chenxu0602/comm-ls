from __future__ import annotations

from pathlib import Path

import pandas as pd


DEFAULT_DIRECT_OIL_ROLES = ("producer", "services", "drilling", "refiner")


def _write_frame(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".parquet":
        df.to_parquet(path, index=False)
    elif path.suffix == ".csv":
        df.to_csv(path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")


def summarize_cross_product_clusters_from_paths(
    trigger_role_results_path: Path,
    output_path: Path | None = None,
    detail_output_path: Path | None = None,
    min_keep_count: int = 5,
    excluded_roles: list[str] | tuple[str, ...] | None = DEFAULT_DIRECT_OIL_ROLES,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = pd.read_csv(trigger_role_results_path)
    required = {
        "quarter",
        "feature",
        "feature_family",
        "horizon_days",
        "exposure_role",
        "candidate_count",
        "keep_count",
        "weak_keep_count",
        "median_selection_score",
        "median_nonoverlap_abs_t_stat",
        "dominant_direction",
        "tickers",
    }
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"{trigger_role_results_path} is missing required columns: {sorted(missing)}")

    out = df.copy()
    for col in [
        "horizon_days",
        "candidate_count",
        "keep_count",
        "weak_keep_count",
        "median_selection_score",
        "median_nonoverlap_abs_t_stat",
    ]:
        out[col] = pd.to_numeric(out[col], errors="coerce")
    out["exposure_role"] = out["exposure_role"].astype(str).str.strip()
    out = out[out["keep_count"].fillna(0) >= min_keep_count].copy()

    if out.empty:
        summary = pd.DataFrame()
        detail = pd.DataFrame()
    else:
        group_cols = ["feature_family", "exposure_role", "horizon_days"]
        summary = (
            out.groupby(group_cols, dropna=False)
            .agg(
                quarters=("quarter", "nunique"),
                rows=("quarter", "size"),
                total_keep=("keep_count", "sum"),
                median_keep=("keep_count", "median"),
                max_keep=("keep_count", "max"),
                median_candidate_count=("candidate_count", "median"),
                median_score=("median_selection_score", "median"),
                median_t=("median_nonoverlap_abs_t_stat", "median"),
            )
            .reset_index()
            .sort_values(
                ["quarters", "total_keep", "median_score"],
                ascending=[False, False, False],
            )
            .reset_index(drop=True)
        )

        excluded = {role.strip() for role in (excluded_roles or [])}
        detail = out[~out["exposure_role"].isin(excluded)].copy()
        detail = detail.sort_values(
            ["keep_count", "median_selection_score", "candidate_count"],
            ascending=[False, False, False],
        ).reset_index(drop=True)

    if output_path is not None:
        _write_frame(summary, output_path)
    if detail_output_path is not None:
        _write_frame(detail, detail_output_path)
    return summary, detail
