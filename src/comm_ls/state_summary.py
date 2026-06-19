from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from comm_ls.research_quality import state_hypothesis


def _write_frame(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".parquet":
        df.to_parquet(path, index=False)
    elif path.suffix == ".csv":
        df.to_csv(path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")


def _dominant_direction(positive: int, negative: int) -> str:
    if positive > negative:
        return "positive"
    if negative > positive:
        return "negative"
    return "mixed"


def summarize_state_role_clusters(
    candidates: pd.DataFrame,
    min_keep_count: int = 5,
    include_weak_keep: bool = True,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if candidates.empty:
        return pd.DataFrame(), pd.DataFrame()
    required = {
        "quarter",
        "commodity",
        "feature",
        "feature_family",
        "horizon_days",
        "target_return_column",
        "exposure_role",
        "selection_verdict",
        "ticker",
        "selection_score",
        "max_nonoverlap_abs_t_stat",
        "observed_beta_sign",
    }
    missing = required.difference(candidates.columns)
    if missing:
        raise ValueError(f"candidate file is missing required columns: {sorted(missing)}")

    df = candidates.copy()
    df["feature"] = df["feature"].astype(str).str.strip()
    if "state_hypothesis" not in df.columns:
        df["state_hypothesis"] = df["feature"].map(state_hypothesis)
    df["state_hypothesis"] = df["state_hypothesis"].astype(str).str.strip()
    df["selection_verdict"] = df["selection_verdict"].astype(str).str.strip()
    active_verdicts = {"keep", "weak_keep"} if include_weak_keep else {"keep"}
    active = df[df["selection_verdict"].isin(active_verdicts)].copy()
    if active.empty:
        return pd.DataFrame(), pd.DataFrame()

    for col in ["horizon_days", "selection_score", "max_nonoverlap_abs_t_stat", "observed_beta_sign"]:
        active[col] = pd.to_numeric(active[col], errors="coerce")

    detail_group_cols = [
        "commodity",
        "quarter",
        "state_hypothesis",
        "exposure_role",
        "horizon_days",
        "target_return_column",
    ]
    detail = (
        active.groupby(detail_group_cols, dropna=False)
        .agg(
            feature_count=("feature", "nunique"),
            supporting_features=("feature", lambda s: ",".join(sorted(set(s.astype(str))))),
            candidate_count=("ticker", "nunique"),
            keep_count=("selection_verdict", lambda s: int((s == "keep").sum())),
            weak_keep_count=("selection_verdict", lambda s: int((s == "weak_keep").sum())),
            median_selection_score=("selection_score", "median"),
            median_nonoverlap_abs_t_stat=("max_nonoverlap_abs_t_stat", "median"),
            median_beta_per_1z=("median_beta_per_1z", "median")
            if "median_beta_per_1z" in active.columns
            else ("observed_beta_sign", "median"),
            positive_beta_count=("observed_beta_sign", lambda s: int((s > 0).sum())),
            negative_beta_count=("observed_beta_sign", lambda s: int((s < 0).sum())),
            tickers=("ticker", lambda s: ",".join(sorted(set(s.astype(str))))),
        )
        .reset_index()
    )
    detail["dominant_direction"] = [
        _dominant_direction(int(pos), int(neg))
        for pos, neg in zip(detail["positive_beta_count"], detail["negative_beta_count"], strict=False)
    ]
    detail = detail[detail["keep_count"].fillna(0) >= min_keep_count].copy()

    if detail.empty:
        return pd.DataFrame(), detail.reset_index(drop=True)

    summary_group_cols = [
        "commodity",
        "state_hypothesis",
        "exposure_role",
        "horizon_days",
        "target_return_column",
    ]
    summary = (
        detail.groupby(summary_group_cols, dropna=False)
        .agg(
            quarters=("quarter", "nunique"),
            rows=("quarter", "size"),
            total_keep=("keep_count", "sum"),
            total_weak_keep=("weak_keep_count", "sum"),
            median_keep=("keep_count", "median"),
            max_keep=("keep_count", "max"),
            median_candidate_count=("candidate_count", "median"),
            median_feature_count=("feature_count", "median"),
            supporting_features=("supporting_features", lambda s: ",".join(sorted(set(",".join(s).split(","))))),
            median_score=("median_selection_score", "median"),
            median_t=("median_nonoverlap_abs_t_stat", "median"),
            median_beta_per_1z=("median_beta_per_1z", "median"),
            positive_beta_count=("positive_beta_count", "sum"),
            negative_beta_count=("negative_beta_count", "sum"),
            tickers=("tickers", lambda s: ",".join(sorted(set(",".join(s).split(","))))),
        )
        .reset_index()
    )
    summary["dominant_direction"] = [
        _dominant_direction(int(pos), int(neg))
        for pos, neg in zip(summary["positive_beta_count"], summary["negative_beta_count"], strict=False)
    ]
    summary["state_cluster_score"] = (
        np.log1p(summary["quarters"].fillna(0))
        * np.log1p(summary["total_keep"].fillna(0))
        * summary["median_score"].fillna(0)
    )
    summary = summary.sort_values(
        ["quarters", "total_keep", "state_cluster_score", "median_score"],
        ascending=[False, False, False, False],
    ).reset_index(drop=True)
    detail = detail.sort_values(
        ["keep_count", "median_selection_score", "candidate_count"],
        ascending=[False, False, False],
    ).reset_index(drop=True)
    return summary, detail


def summarize_state_role_clusters_from_paths(
    candidates_path: Path,
    output_path: Path | None = None,
    detail_output_path: Path | None = None,
    min_keep_count: int = 5,
    include_weak_keep: bool = True,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    summary, detail = summarize_state_role_clusters(
        candidates=pd.read_csv(candidates_path),
        min_keep_count=min_keep_count,
        include_weak_keep=include_weak_keep,
    )
    if output_path is not None:
        _write_frame(summary, output_path)
    if detail_output_path is not None:
        _write_frame(detail, detail_output_path)
    return summary, detail
