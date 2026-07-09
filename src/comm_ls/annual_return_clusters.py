from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class AnnualClusterConfig:
    return_column: str = "residual_return_mkt_w12m"
    min_observations: int = 150
    min_cl_overlap: int = 120
    min_pair_overlap: int = 120
    winsor_quantile: float = 0.01
    seed_pool_size: int = 0
    min_clusters: int = 8
    max_clusters: int = 12
    max_singleton_share: float = 0.20


@dataclass
class AnnualClusterResult:
    assignments: pd.DataFrame
    cluster_summary: pd.DataFrame
    model_selection: pd.DataFrame
    universe_audit: pd.DataFrame
    correlation: pd.DataFrame
    distance: pd.DataFrame


def load_q1_point_in_time_universe(universe_dir: Path, year: int) -> pd.DataFrame:
    path = universe_dir / f"CL-Univ-{year}-Q1.csv"
    if not path.exists():
        raise FileNotFoundError(f"Missing point-in-time universe: {path}")

    frame = pd.read_csv(path)
    required = {"ticker", "quarter", "asof_date"}
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"{path} is missing columns: {sorted(missing)}")

    out = frame.copy()
    out["ticker"] = out["ticker"].astype(str).str.upper().str.strip()
    out["asof_date"] = pd.to_datetime(out["asof_date"], errors="coerce")
    expected_quarter = f"{year}-Q1"
    if not out["quarter"].astype(str).eq(expected_quarter).all():
        raise ValueError(f"{path} contains rows outside {expected_quarter}")
    if out["asof_date"].isna().any() or out["asof_date"].max() >= pd.Timestamp(f"{year}-01-01"):
        raise ValueError(f"{path} is not point-in-time as of the prior year end")

    if "is_tradeable" in out.columns:
        tradeable = out["is_tradeable"].astype(str).str.lower().isin({"true", "1"})
        out = out[tradeable]
    if "selected" in out.columns:
        selected = out["selected"].astype(str).str.lower().isin({"true", "1"})
        out = out[selected]
    return out.drop_duplicates("ticker", keep="first").reset_index(drop=True)


def load_cl_simple_returns(path: Path, year: int) -> pd.Series:
    frame = pd.read_csv(path, usecols=["date", "m0_ret"])
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce")
    frame["m0_ret"] = pd.to_numeric(frame["m0_ret"], errors="coerce")
    frame = frame[frame["date"].dt.year.eq(year)].dropna().drop_duplicates("date", keep="last")
    result = pd.Series(
        np.expm1(frame["m0_ret"].to_numpy(dtype=float)),
        index=pd.DatetimeIndex(frame["date"].to_numpy()),
        name="cl_return",
    )
    return result.sort_index()


def build_annual_return_panel(
    processed: pd.DataFrame,
    universe: pd.DataFrame,
    year: int,
    config: AnnualClusterConfig,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    required = {"date", "ticker", config.return_column}
    missing = required.difference(processed.columns)
    if missing:
        raise ValueError(f"Processed data is missing columns: {sorted(missing)}")

    tickers = universe["ticker"].astype(str).str.upper().unique()
    data = processed.loc[:, list(required)].copy()
    data["date"] = pd.to_datetime(data["date"], errors="coerce")
    data["ticker"] = data["ticker"].astype(str).str.upper().str.strip()
    data[config.return_column] = pd.to_numeric(data[config.return_column], errors="coerce")
    data = data[data["date"].dt.year.eq(year) & data["ticker"].isin(tickers)]
    panel = data.pivot_table(
        index="date", columns="ticker", values=config.return_column, aggfunc="last"
    ).sort_index()

    observations = panel.notna().sum().reindex(tickers, fill_value=0).astype(int)
    audit = universe.copy()
    audit["year"] = year
    audit["return_observations"] = audit["ticker"].map(observations).fillna(0).astype(int)
    audit["included_for_cl_scoring"] = audit["return_observations"].ge(config.min_observations)
    audit["exclusion_reason"] = np.where(
        audit["included_for_cl_scoring"], "", "insufficient_return_observations"
    )

    keep = observations[observations.ge(config.min_observations)].index.tolist()
    panel = panel.reindex(columns=keep)
    q = config.winsor_quantile
    if q > 0 and not panel.empty:
        lower = panel.quantile(q)
        upper = panel.quantile(1.0 - q)
        panel = panel.clip(lower=lower, upper=upper, axis="columns")
    return panel, audit


def score_cl_relevance(
    panel: pd.DataFrame,
    cl_returns: pd.Series,
    min_overlap: int,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for ticker in panel.columns:
        pair = pd.concat([panel[ticker], cl_returns], axis=1).dropna()
        corr = float(pair.iloc[:, 0].corr(pair.iloc[:, 1])) if len(pair) >= min_overlap else np.nan
        rows.append(
            {
                "ticker": ticker,
                "cl_overlap": int(len(pair)),
                "cl_correlation": corr,
                "cl_abs_correlation": abs(corr) if np.isfinite(corr) else np.nan,
            }
        )
    result = pd.DataFrame(rows)
    return result.sort_values(
        ["cl_abs_correlation", "ticker"], ascending=[False, True], na_position="last"
    ).reset_index(drop=True)


def select_cl_seed_pool(scores: pd.DataFrame, size: int) -> pd.DataFrame:
    eligible = scores.dropna(subset=["cl_correlation"]).copy()
    eligible = eligible.sort_values(
        ["cl_abs_correlation", "ticker"], ascending=[False, True]
    )
    if size > 0:
        eligible = eligible.head(size)
    eligible["seed_rank"] = np.arange(1, len(eligible) + 1)
    eligible["in_seed_pool"] = True
    return eligible.reset_index(drop=True)


def _drop_incomplete_pair_tickers(
    panel: pd.DataFrame, min_pair_overlap: int
) -> tuple[pd.DataFrame, list[str]]:
    work = panel.copy()
    dropped: list[str] = []
    while len(work.columns) > 1:
        valid = work.notna().astype(int)
        overlap = valid.T @ valid
        incomplete = overlap.lt(min_pair_overlap)
        for diagonal_index in range(len(incomplete)):
            incomplete.iat[diagonal_index, diagonal_index] = False
        if not incomplete.to_numpy().any():
            break
        counts = incomplete.sum(axis=1)
        worst_count = counts.max()
        candidates = counts[counts.eq(worst_count)].index
        observations = work[candidates].notna().sum()
        drop_ticker = sorted(
            observations[observations.eq(observations.min())].index.astype(str)
        )[0]
        dropped.append(drop_ticker)
        work = work.drop(columns=drop_ticker)
    return work, dropped


def correlation_and_distance(
    panel: pd.DataFrame, min_pair_overlap: int
) -> tuple[pd.DataFrame, pd.DataFrame, list[str]]:
    complete, dropped = _drop_incomplete_pair_tickers(panel, min_pair_overlap)
    correlation = complete.corr(min_periods=min_pair_overlap).clip(-1.0, 1.0)
    if correlation.isna().to_numpy().any():
        raise ValueError("Correlation matrix still contains missing values after overlap filtering")
    distance = np.sqrt(np.maximum(0.0, 0.5 * (1.0 - correlation)))
    for diagonal_index in range(len(distance)):
        distance.iat[diagonal_index, diagonal_index] = 0.0
    return correlation, distance, dropped


def average_linkage(distance: pd.DataFrame) -> np.ndarray:
    names = list(distance.index)
    n = len(names)
    if n < 2:
        return np.empty((0, 4), dtype=float)

    clusters: dict[int, list[int]] = {i: [i] for i in range(n)}
    pair_distances: dict[tuple[int, int], float] = {
        (i, j): float(distance.iloc[i, j]) for i in range(n) for j in range(i + 1, n)
    }
    linkage_rows: list[list[float]] = []
    next_id = n
    while len(clusters) > 1:
        left, right = min(pair_distances, key=lambda key: (pair_distances[key], key))
        merge_distance = pair_distances[(left, right)]
        left_size = len(clusters[left])
        right_size = len(clusters[right])
        linkage_rows.append([left, right, merge_distance, left_size + right_size])

        others = [cluster_id for cluster_id in clusters if cluster_id not in {left, right}]
        new_distances: dict[int, float] = {}
        for other in others:
            left_key = tuple(sorted((left, other)))
            right_key = tuple(sorted((right, other)))
            new_distances[other] = (
                left_size * pair_distances[left_key] + right_size * pair_distances[right_key]
            ) / (left_size + right_size)

        pair_distances = {
            key: value
            for key, value in pair_distances.items()
            if left not in key and right not in key
        }
        merged_members = clusters.pop(left) + clusters.pop(right)
        clusters[next_id] = merged_members
        for other, value in new_distances.items():
            pair_distances[tuple(sorted((next_id, other)))] = value
        next_id += 1
    return np.asarray(linkage_rows, dtype=float)


def cut_linkage(linkage: np.ndarray, tickers: list[str], cluster_count: int) -> pd.Series:
    n = len(tickers)
    if not 1 <= cluster_count <= n:
        raise ValueError("cluster_count must be between 1 and the number of tickers")
    clusters: dict[int, set[int]] = {i: {i} for i in range(n)}
    for merge_index, row in enumerate(linkage[: n - cluster_count]):
        left, right = int(row[0]), int(row[1])
        clusters[n + merge_index] = clusters.pop(left) | clusters.pop(right)

    ordered = sorted(clusters.values(), key=lambda members: min(tickers[i] for i in members))
    labels: dict[str, int] = {}
    for cluster_id, members in enumerate(ordered, start=1):
        for member in members:
            labels[tickers[member]] = cluster_id
    return pd.Series(labels, name="cluster_id").sort_index()


def silhouette_score(distance: pd.DataFrame, labels: pd.Series) -> float:
    labels = labels.reindex(distance.index)
    values: list[float] = []
    for ticker in distance.index:
        own = labels[ticker]
        own_members = labels[(labels == own) & (labels.index != ticker)].index
        if len(own_members) == 0:
            values.append(0.0)
            continue
        a = float(distance.loc[ticker, own_members].mean())
        other_means = [
            float(distance.loc[ticker, labels[labels == other].index].mean())
            for other in sorted(labels.unique())
            if other != own
        ]
        b = min(other_means)
        denominator = max(a, b)
        values.append((b - a) / denominator if denominator > 0 else 0.0)
    return float(np.mean(values)) if values else np.nan


def choose_cluster_count(
    distance: pd.DataFrame,
    linkage: np.ndarray,
    config: AnnualClusterConfig,
) -> tuple[int, pd.DataFrame]:
    n = len(distance)
    low = min(config.min_clusters, n)
    high = min(config.max_clusters, n)
    rows: list[dict[str, object]] = []
    for k in range(low, high + 1):
        labels = cut_linkage(linkage, list(distance.index), k)
        sizes = labels.value_counts()
        singleton_count = int(sizes.eq(1).sum())
        rows.append(
            {
                "cluster_count": k,
                "silhouette": silhouette_score(distance, labels),
                "singleton_count": singleton_count,
                "singleton_share": singleton_count / k,
                "min_cluster_size": int(sizes.min()),
                "max_cluster_size": int(sizes.max()),
            }
        )
    scores = pd.DataFrame(rows)
    eligible = scores[scores["singleton_share"].le(config.max_singleton_share)]
    candidates = eligible if not eligible.empty else scores
    best = candidates.sort_values(
        ["silhouette", "cluster_count"], ascending=[False, True]
    ).iloc[0]
    scores["selected"] = scores["cluster_count"].eq(int(best["cluster_count"]))
    return int(best["cluster_count"]), scores


def analyze_annual_clusters(
    processed: pd.DataFrame,
    universe: pd.DataFrame,
    cl_returns: pd.Series,
    year: int,
    config: AnnualClusterConfig,
) -> AnnualClusterResult:
    panel, audit = build_annual_return_panel(processed, universe, year, config)
    scores = score_cl_relevance(panel, cl_returns, config.min_cl_overlap)
    seed_pool = select_cl_seed_pool(scores, config.seed_pool_size)
    seed_panel = panel.reindex(columns=seed_pool["ticker"])
    correlation, distance, overlap_drops = correlation_and_distance(
        seed_panel, config.min_pair_overlap
    )
    if len(distance) < config.min_clusters:
        raise ValueError(
            f"{year} has only {len(distance)} eligible seed stocks, fewer than "
            f"min_clusters={config.min_clusters}"
        )

    linkage = average_linkage(distance)
    selected_k, model_selection = choose_cluster_count(distance, linkage, config)
    labels = cut_linkage(linkage, list(distance.index), selected_k)

    metadata_columns = [
        col for col in ["ticker", "theme", "role", "region", "exposure_role", "prior_weight", "notes"]
        if col in universe.columns
    ]
    assignments = seed_pool.merge(universe[metadata_columns], on="ticker", how="left")
    assignments = assignments[assignments["ticker"].isin(distance.index)].copy()
    assignments["year"] = year
    assignments["effective_year"] = year + 1
    assignments["cluster_id"] = assignments["ticker"].map(labels).astype(int)
    assignments["return_observations"] = assignments["ticker"].map(panel.notna().sum()).astype(int)
    assignments["is_cluster_representative"] = False
    representative_index = assignments.groupby("cluster_id")["cl_abs_correlation"].idxmax()
    assignments.loc[representative_index, "is_cluster_representative"] = True

    summary_rows: list[dict[str, object]] = []
    for cluster_id, group in assignments.groupby("cluster_id", sort=True):
        members = sorted(group["ticker"])
        sub_corr = correlation.loc[members, members]
        upper = sub_corr.to_numpy()[np.triu_indices(len(members), k=1)]
        representative = group.loc[group["is_cluster_representative"]].iloc[0]
        role_counts = group.get("role", pd.Series(dtype=str)).fillna("unknown").value_counts()
        summary_rows.append(
            {
                "year": year,
                "effective_year": year + 1,
                "cluster_id": int(cluster_id),
                "cluster_size": len(group),
                "representative_ticker": representative["ticker"],
                "representative_cl_correlation": representative["cl_correlation"],
                "mean_within_correlation": float(np.mean(upper)) if len(upper) else np.nan,
                "dominant_role": role_counts.index[0] if len(role_counts) else "unknown",
                "dominant_role_share": float(role_counts.iloc[0] / len(group)) if len(role_counts) else np.nan,
                "members": "+".join(members),
            }
        )

    audit = audit.merge(scores, on="ticker", how="left")
    audit = audit.merge(seed_pool[["ticker", "seed_rank", "in_seed_pool"]], on="ticker", how="left")
    audit["in_seed_pool"] = audit["in_seed_pool"].fillna(False).astype(bool)
    audit["included_in_clustering"] = audit["ticker"].isin(distance.index)
    audit.loc[audit["ticker"].isin(overlap_drops), "exclusion_reason"] = "insufficient_pair_overlap"
    audit.loc[
        audit["included_for_cl_scoring"] & ~audit["in_seed_pool"], "exclusion_reason"
    ] = "missing_cl_overlap_or_outside_seed_limit"
    audit.loc[audit["included_in_clustering"], "exclusion_reason"] = ""

    model_selection.insert(0, "year", year)
    model_selection.insert(1, "effective_year", year + 1)
    model_selection["seed_pool_count"] = len(distance)
    model_selection["selected_cluster_count"] = selected_k
    audit["effective_year"] = year + 1
    assignments = assignments.sort_values(["cluster_id", "seed_rank"]).reset_index(drop=True)
    return AnnualClusterResult(
        assignments=assignments,
        cluster_summary=pd.DataFrame(summary_rows),
        model_selection=model_selection,
        universe_audit=audit,
        correlation=correlation,
        distance=distance,
    )
