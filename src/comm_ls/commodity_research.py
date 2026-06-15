from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from comm_ls.research_quality import _feature_commodity_direction, load_reviewed_features
from comm_ls.universe import load_commodity_exposure_map


DEFAULT_FEATURE_SELECTION_ROOT = Path("data/research/feature_selection")


def _write_frame(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".parquet":
        df.to_parquet(path, index=False)
    elif path.suffix == ".csv":
        df.to_csv(path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")


def _load_role_taxonomy(path: Path) -> pd.DataFrame:
    taxonomy = pd.read_csv(path)
    required = {"commodity", "exposure_role", "economic_channel", "alpha_priority", "deployable_default"}
    missing = required.difference(taxonomy.columns)
    if missing:
        raise ValueError(f"{path} is missing required columns: {sorted(missing)}")
    taxonomy = taxonomy.copy()
    taxonomy["commodity"] = taxonomy["commodity"].astype(str).str.upper().str.strip()
    taxonomy["exposure_role"] = taxonomy["exposure_role"].astype(str).str.strip()
    taxonomy["deployable_default"] = taxonomy["deployable_default"].astype(str).str.lower().isin(
        {"true", "1", "yes", "y"}
    )
    if "expected_prior_sign" in taxonomy.columns:
        taxonomy["expected_prior_sign"] = pd.to_numeric(taxonomy["expected_prior_sign"], errors="coerce")
    return taxonomy


def _matrix_paths(matrix_dir: Path, manifest_path: Path | None, commodity: str) -> list[Path]:
    if manifest_path is not None and manifest_path.exists():
        manifest = pd.read_csv(manifest_path)
        if "path" not in manifest.columns:
            raise ValueError(f"{manifest_path} is missing path column")
        paths = [Path(path) for path in manifest["path"].dropna().astype(str)]
    else:
        paths = sorted(matrix_dir.glob(f"{commodity}-Features-*-*.csv"))
    return [path for path in paths if path.exists() and not path.name.endswith("manifest.csv")]


def load_quarterly_feature_matrices(
    matrix_dir: Path,
    commodity: str,
    manifest_path: Path | None = None,
    quarters: list[str] | None = None,
) -> pd.DataFrame:
    commodity = commodity.upper().strip()
    paths = _matrix_paths(matrix_dir=matrix_dir, manifest_path=manifest_path, commodity=commodity)
    if not paths:
        raise FileNotFoundError(f"No quarterly feature matrix files found under {matrix_dir}")

    keep_quarters = {quarter.strip() for quarter in quarters} if quarters else None
    frames: list[pd.DataFrame] = []
    for path in paths:
        frame = pd.read_csv(path)
        if frame.empty:
            continue
        frame["source_file"] = str(path)
        if "commodity" in frame.columns:
            frame["commodity"] = frame["commodity"].astype(str).str.upper().str.strip()
            frame = frame[frame["commodity"].eq(commodity)].copy()
        if keep_quarters is not None and "quarter" in frame.columns:
            frame = frame[frame["quarter"].astype(str).isin(keep_quarters)].copy()
        if not frame.empty:
            frames.append(frame)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def _enabled_reviewed_features(path: Path | None, commodity: str) -> set[str] | None:
    if path is None or not path.exists():
        return None
    reviewed = load_reviewed_features(path)
    reviewed = reviewed[reviewed["default_enabled"]].copy()
    reviewed = reviewed[reviewed["commodity"].isin(["ALL", commodity])].copy()
    return set(reviewed["feature"].dropna().astype(str))


def _issue_list(row: pd.Series) -> str:
    issues = []
    for col, label in [
        ("flag_missing_exposure", "missing_exposure"),
        ("flag_missing_role_taxonomy", "missing_role_taxonomy"),
        ("flag_not_deployable_default", "not_deployable_default"),
        ("flag_low_priority_role", "low_priority_role"),
        ("flag_no_feature_direction", "no_feature_direction"),
        ("flag_direction_mismatch", "direction_mismatch"),
        ("flag_low_effective_observations", "low_effective_observations"),
        ("flag_weak_t_stat", "weak_t_stat"),
        ("flag_weak_nonoverlap", "weak_nonoverlap"),
        ("flag_unstable_sign", "unstable_sign"),
        ("flag_weak_hit_rate", "weak_hit_rate"),
        ("flag_commodity_neutral_decay", "commodity_neutral_decay"),
        ("flag_missing_commodity_neutral_diagnostic", "missing_commodity_neutral_diagnostic"),
    ]:
        if bool(row.get(col, False)):
            issues.append(label)
    return ",".join(issues)


def _priority_score(priority: object) -> float:
    return {"high": 1.0, "medium": 0.7, "low": 0.35}.get(str(priority).lower().strip(), 0.4)


def _aggregate_candidate_scores(
    matrix: pd.DataFrame,
    exposure_map: pd.DataFrame,
    role_taxonomy: pd.DataFrame,
    commodity: str,
    min_abs_t: float,
    min_nonoverlap_abs_t: float,
    min_effective_observations: int,
    min_hit_rate_edge: float,
    min_sign_stability: float,
    reviewed_features_path: Path | None,
    include_unreviewed_features: bool,
    diagnostic: pd.DataFrame | None,
    commodity_neutral_min_ratio: float,
) -> pd.DataFrame:
    if matrix.empty:
        return matrix.copy()

    df = matrix.copy()
    df["commodity"] = df["commodity"].astype(str).str.upper().str.strip()
    df["ticker"] = df["ticker"].astype(str).str.upper().str.strip()
    df["feature"] = df["feature"].astype(str).str.strip()
    if "target_return_column" not in df.columns:
        df["target_return_column"] = "residual_return"
    df["target_return_column"] = df["target_return_column"].astype(str).str.strip()
    df = df[df["commodity"].eq(commodity)].copy()
    if df.empty:
        return df

    enabled = _enabled_reviewed_features(reviewed_features_path, commodity)
    if enabled is not None and not include_unreviewed_features:
        df = df[df["feature"].isin(enabled)].copy()

    for col in [
        "lookback_years",
        "horizon_days",
        "observations",
        "effective_observations",
        "abs_t_stat",
        "nonoverlap_abs_t_stat",
        "beta_per_1z",
        "nonoverlap_beta_per_1z",
        "hit_rate",
        "nonoverlap_hit_rate",
        "residual_vol",
    ]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df["observed_beta_sign"] = np.sign(pd.to_numeric(df["beta_per_1z"], errors="coerce")).replace(0, np.nan)

    exposure = exposure_map.copy()
    exposure["commodity"] = exposure["commodity"].astype(str).str.upper().str.strip()
    exposure["ticker"] = exposure["ticker"].astype(str).str.upper().str.strip()
    exposure = exposure[exposure["commodity"].eq(commodity)].copy()

    taxonomy = role_taxonomy.copy()
    taxonomy["commodity"] = taxonomy["commodity"].astype(str).str.upper().str.strip()
    taxonomy = taxonomy[taxonomy["commodity"].eq(commodity)].copy()

    keys = [
        "quarter",
        "asof_date",
        "ticker",
        "commodity",
        "feature",
        "feature_family",
        "horizon_days",
        "target_return_column",
    ]
    grouped = (
        df.groupby(keys, dropna=False)
        .agg(
            lookback_count=("lookback_years", "nunique"),
            lookback_years=("lookback_years", lambda s: ",".join(str(int(v)) for v in sorted(s.dropna().unique()))),
            sample_start=("sample_start", "min"),
            sample_end=("sample_end", "max"),
            observations_min=("observations", "min"),
            observations_median=("observations", "median"),
            effective_observations_min=("effective_observations", "min"),
            effective_observations_median=("effective_observations", "median"),
            max_abs_t_stat=("abs_t_stat", "max"),
            median_abs_t_stat=("abs_t_stat", "median"),
            max_nonoverlap_abs_t_stat=("nonoverlap_abs_t_stat", "max"),
            median_nonoverlap_abs_t_stat=("nonoverlap_abs_t_stat", "median"),
            median_beta_per_1z=("beta_per_1z", "median"),
            median_nonoverlap_beta_per_1z=("nonoverlap_beta_per_1z", "median"),
            mean_hit_rate=("hit_rate", "mean"),
            mean_nonoverlap_hit_rate=("nonoverlap_hit_rate", "mean"),
            residual_vol=("residual_vol", "mean"),
            beta_sign_stability=("observed_beta_sign", lambda s: abs(float(s.dropna().mean())) if s.notna().any() else np.nan),
            beta_positive_count=("observed_beta_sign", lambda s: int((s > 0).sum())),
            beta_negative_count=("observed_beta_sign", lambda s: int((s < 0).sum())),
            theme=("theme", "last"),
            role=("role", "last"),
            region=("region", "last"),
            source_files=("source_file", lambda s: ",".join(sorted(set(s.astype(str))))),
        )
        .reset_index()
    )
    grouped["observed_beta_sign"] = np.sign(pd.to_numeric(grouped["median_beta_per_1z"], errors="coerce")).replace(
        0, np.nan
    )
    grouped["feature_commodity_direction"] = grouped["feature"].map(_feature_commodity_direction)

    grouped = grouped.merge(
        exposure[["ticker", "commodity", "exposure_role", "prior_weight", "notes"]].rename(
            columns={"notes": "exposure_notes"}
        ),
        on=["ticker", "commodity"],
        how="left",
    )
    grouped = grouped.merge(
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
    grouped["prior_weight"] = pd.to_numeric(grouped["prior_weight"], errors="coerce")
    grouped["expected_beta_sign"] = np.sign(grouped["prior_weight"] * grouped["feature_commodity_direction"]).replace(
        0, np.nan
    )

    if diagnostic is not None and not diagnostic.empty:
        diag = _aggregate_candidate_scores(
            matrix=diagnostic,
            exposure_map=exposure_map,
            role_taxonomy=role_taxonomy,
            commodity=commodity,
            min_abs_t=min_abs_t,
            min_nonoverlap_abs_t=min_nonoverlap_abs_t,
            min_effective_observations=min_effective_observations,
            min_hit_rate_edge=min_hit_rate_edge,
            min_sign_stability=min_sign_stability,
            reviewed_features_path=reviewed_features_path,
            include_unreviewed_features=include_unreviewed_features,
            diagnostic=None,
            commodity_neutral_min_ratio=commodity_neutral_min_ratio,
        )
        diag_cols = [
            "quarter",
            "ticker",
            "commodity",
            "feature",
            "horizon_days",
            "target_return_column",
            "max_abs_t_stat",
            "max_nonoverlap_abs_t_stat",
            "median_beta_per_1z",
            "selection_verdict",
        ]
        diag = diag[[col for col in diag_cols if col in diag.columns]].rename(
            columns={
                "max_abs_t_stat": "commodity_neutral_max_abs_t_stat",
                "max_nonoverlap_abs_t_stat": "commodity_neutral_max_nonoverlap_abs_t_stat",
                "median_beta_per_1z": "commodity_neutral_median_beta_per_1z",
                "selection_verdict": "commodity_neutral_selection_verdict",
            }
        )
        grouped = grouped.merge(
            diag,
            on=["quarter", "ticker", "commodity", "feature", "horizon_days", "target_return_column"],
            how="left",
        )
    else:
        grouped["commodity_neutral_max_abs_t_stat"] = np.nan
        grouped["commodity_neutral_max_nonoverlap_abs_t_stat"] = np.nan
        grouped["commodity_neutral_median_beta_per_1z"] = np.nan
        grouped["commodity_neutral_selection_verdict"] = pd.NA

    grouped["commodity_neutral_nonoverlap_ratio"] = (
        grouped["commodity_neutral_max_nonoverlap_abs_t_stat"] / grouped["max_nonoverlap_abs_t_stat"]
    )

    grouped["flag_missing_exposure"] = grouped["exposure_role"].isna()
    grouped["flag_missing_role_taxonomy"] = grouped["exposure_role"].notna() & grouped["taxonomy_bucket"].isna()
    grouped["flag_not_deployable_default"] = grouped["deployable_default"].eq(False)
    grouped["flag_low_priority_role"] = grouped["alpha_priority"].astype(str).str.lower().eq("low")
    grouped["flag_no_feature_direction"] = grouped["feature_commodity_direction"].eq(0)
    grouped["flag_direction_mismatch"] = (
        grouped["expected_beta_sign"].notna()
        & grouped["observed_beta_sign"].notna()
        & grouped["expected_beta_sign"].ne(grouped["observed_beta_sign"])
    )
    grouped["flag_low_effective_observations"] = (
        grouped["effective_observations_min"].fillna(0) < min_effective_observations
    )
    grouped["flag_weak_t_stat"] = grouped["max_abs_t_stat"].fillna(0) < min_abs_t
    grouped["flag_weak_nonoverlap"] = grouped["max_nonoverlap_abs_t_stat"].fillna(0) < min_nonoverlap_abs_t
    grouped["flag_unstable_sign"] = grouped["beta_sign_stability"].fillna(0) < min_sign_stability
    grouped["flag_weak_hit_rate"] = (grouped["mean_hit_rate"] - 0.5).abs().fillna(0) < min_hit_rate_edge
    grouped["flag_missing_commodity_neutral_diagnostic"] = diagnostic is None or diagnostic.empty
    grouped["flag_commodity_neutral_decay"] = (
        grouped["commodity_neutral_nonoverlap_ratio"].notna()
        & (grouped["commodity_neutral_nonoverlap_ratio"] < commodity_neutral_min_ratio)
    )

    hard_block = (
        grouped["flag_missing_exposure"]
        | grouped["flag_not_deployable_default"]
        | grouped["flag_low_effective_observations"]
        | grouped["flag_weak_t_stat"]
        | grouped["flag_weak_nonoverlap"]
        | grouped["flag_unstable_sign"]
    )
    soft_review = (
        grouped["flag_missing_role_taxonomy"]
        | grouped["flag_low_priority_role"]
        | grouped["flag_no_feature_direction"]
        | grouped["flag_direction_mismatch"]
        | grouped["flag_weak_hit_rate"]
        | grouped["flag_commodity_neutral_decay"]
        | grouped["flag_missing_commodity_neutral_diagnostic"]
    )
    grouped["selection_verdict"] = np.select([hard_block, soft_review], ["block", "weak_keep"], default="keep")
    grouped["selection_flags"] = grouped.apply(_issue_list, axis=1)
    grouped["role_priority_score"] = grouped["alpha_priority"].map(_priority_score)
    grouped["selection_score"] = (
        0.30 * (grouped["max_abs_t_stat"].clip(upper=6.0) / 6.0).fillna(0.0)
        + 0.25 * (grouped["max_nonoverlap_abs_t_stat"].clip(upper=3.0) / 3.0).fillna(0.0)
        + 0.15 * grouped["beta_sign_stability"].fillna(0.0).clip(0.0, 1.0)
        + 0.15 * (grouped["mean_hit_rate"].sub(0.5).abs().mul(5.0)).fillna(0.0).clip(0.0, 1.0)
        + 0.15 * grouped["role_priority_score"].fillna(0.0)
    )
    grouped.loc[grouped["selection_verdict"].eq("block"), "selection_score"] *= 0.25

    sort_cols = [
        "quarter",
        "target_return_column",
        "selection_verdict",
        "selection_score",
        "max_nonoverlap_abs_t_stat",
    ]
    grouped = grouped.sort_values(sort_cols, ascending=[True, True, True, False, False]).reset_index(drop=True)
    return grouped


def _trigger_role_results(candidate_scores: pd.DataFrame) -> pd.DataFrame:
    if candidate_scores.empty:
        return candidate_scores.copy()
    df = candidate_scores.copy()
    active = df[~df["selection_verdict"].eq("block")].copy()
    if active.empty:
        active = df.copy()
    grouped = (
        active.groupby(
            [
                "commodity",
                "quarter",
                "feature",
                "feature_family",
                "horizon_days",
                "target_return_column",
                "exposure_role",
            ],
            dropna=False,
        )
        .agg(
            candidate_count=("ticker", "nunique"),
            keep_count=("selection_verdict", lambda s: int((s == "keep").sum())),
            weak_keep_count=("selection_verdict", lambda s: int((s == "weak_keep").sum())),
            median_selection_score=("selection_score", "median"),
            median_beta_per_1z=("median_beta_per_1z", "median"),
            median_nonoverlap_abs_t_stat=("max_nonoverlap_abs_t_stat", "median"),
            median_hit_rate=("mean_hit_rate", "median"),
            positive_beta_count=("observed_beta_sign", lambda s: int((s > 0).sum())),
            negative_beta_count=("observed_beta_sign", lambda s: int((s < 0).sum())),
            tickers=("ticker", lambda s: ",".join(sorted(set(s.astype(str))))),
        )
        .reset_index()
    )
    grouped["dominant_direction"] = np.select(
        [grouped["positive_beta_count"] > grouped["negative_beta_count"], grouped["negative_beta_count"] > grouped["positive_beta_count"]],
        ["positive", "negative"],
        default="mixed",
    )
    return grouped.sort_values(
        ["commodity", "quarter", "target_return_column", "median_selection_score", "candidate_count"],
        ascending=[True, True, True, False, False],
    ).reset_index(drop=True)


def research_commodity_features_from_paths(
    commodity: str,
    matrix_dir: Path | None = None,
    manifest_path: Path | None = None,
    diagnostic_matrix_dir: Path | None = None,
    diagnostic_manifest_path: Path | None = None,
    exposure_map_path: Path = Path("config/commodity_exposure_map.csv"),
    role_taxonomy_path: Path = Path("config/commodity_role_taxonomy.csv"),
    reviewed_features_path: Path | None = Path("config/reviewed_commodity_features.csv"),
    output_dir: Path | None = None,
    quarters: list[str] | None = None,
    include_unreviewed_features: bool = False,
    min_abs_t: float = 2.0,
    min_nonoverlap_abs_t: float = 1.0,
    min_effective_observations: int = 20,
    min_hit_rate_edge: float = 0.03,
    min_sign_stability: float = 0.5,
    commodity_neutral_min_ratio: float = 0.5,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    commodity = commodity.upper().strip()
    matrix_dir = matrix_dir or Path(f"data/matrix/{commodity}")
    manifest_path = manifest_path or matrix_dir / f"{commodity}-Features-manifest.csv"
    output_dir = output_dir or DEFAULT_FEATURE_SELECTION_ROOT / commodity

    matrix = load_quarterly_feature_matrices(
        matrix_dir=matrix_dir,
        manifest_path=manifest_path if manifest_path.exists() else None,
        commodity=commodity,
        quarters=quarters,
    )
    diagnostic = None
    if diagnostic_matrix_dir is not None:
        diagnostic_manifest = diagnostic_manifest_path or diagnostic_matrix_dir / f"{commodity}-Features-manifest.csv"
        diagnostic = load_quarterly_feature_matrices(
            matrix_dir=diagnostic_matrix_dir,
            manifest_path=diagnostic_manifest if diagnostic_manifest.exists() else None,
            commodity=commodity,
            quarters=quarters,
        )

    exposure = load_commodity_exposure_map(exposure_map_path)
    taxonomy = _load_role_taxonomy(role_taxonomy_path)
    candidate_scores = _aggregate_candidate_scores(
        matrix=matrix,
        exposure_map=exposure,
        role_taxonomy=taxonomy,
        commodity=commodity,
        min_abs_t=min_abs_t,
        min_nonoverlap_abs_t=min_nonoverlap_abs_t,
        min_effective_observations=min_effective_observations,
        min_hit_rate_edge=min_hit_rate_edge,
        min_sign_stability=min_sign_stability,
        reviewed_features_path=reviewed_features_path,
        include_unreviewed_features=include_unreviewed_features,
        diagnostic=diagnostic,
        commodity_neutral_min_ratio=commodity_neutral_min_ratio,
    )
    selected = candidate_scores[~candidate_scores["selection_verdict"].eq("block")].copy()
    blocked = candidate_scores[candidate_scores["selection_verdict"].eq("block")].copy()
    role_results = _trigger_role_results(candidate_scores)

    _write_frame(candidate_scores, output_dir / "feature_candidate_scores.csv")
    _write_frame(selected, output_dir / "selected_features.csv")
    _write_frame(blocked, output_dir / "blocked_features.csv")
    _write_frame(role_results, output_dir / "trigger_role_results.csv")
    return candidate_scores, selected, blocked, role_results
