from __future__ import annotations

import pandas as pd


def _as_bool(series: pd.Series) -> pd.Series:
    if series.dtype == bool:
        return series
    return series.astype(str).str.lower().isin({"true", "1"})


def build_cluster_evolution_tables(
    assignments: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    required = {"year", "ticker", "cluster_id", "is_cluster_representative"}
    missing = required.difference(assignments.columns)
    if missing:
        raise ValueError(f"Assignments are missing columns: {sorted(missing)}")

    data = assignments.copy()
    data["year"] = pd.to_numeric(data["year"], errors="raise").astype(int)
    data["cluster_id"] = pd.to_numeric(data["cluster_id"], errors="raise").astype(int)
    data["ticker"] = data["ticker"].astype(str).str.upper().str.strip()
    data["is_cluster_representative"] = _as_bool(data["is_cluster_representative"])
    if "effective_year" not in data.columns:
        data["effective_year"] = data["year"] + 1

    long_rows: list[dict[str, object]] = []
    ticker_cells: list[dict[str, object]] = []
    for (year, cluster_id), group in data.groupby(["year", "cluster_id"], sort=True):
        group = group.sort_values(["seed_rank", "ticker"] if "seed_rank" in group.columns else ["ticker"])
        representatives = group.loc[group["is_cluster_representative"], "ticker"]
        representative = representatives.iloc[0] if len(representatives) else group.iloc[0]["ticker"]
        role_counts = (
            group["role"].fillna("unknown").astype(str).value_counts()
            if "role" in group.columns
            else pd.Series({"unknown": len(group)})
        )
        dominant_role = str(role_counts.index[0])
        members = group["ticker"].tolist()
        cluster_label = f"C{cluster_id:02d}/{representative}"
        long_rows.append(
            {
                "year": year,
                "effective_year": int(group["effective_year"].iloc[0]),
                "cluster": f"C{cluster_id:02d}",
                "representative": representative,
                "dominant_role": dominant_role,
                "cluster_size": len(group),
                "members": ", ".join(members),
                "display": f"{dominant_role} [{representative}]: {', '.join(members)}",
            }
        )
        for ticker in members:
            ticker_cells.append({"ticker": ticker, "year": year, "cluster": cluster_label})

    long_table = pd.DataFrame(long_rows).sort_values(["year", "cluster"]).reset_index(drop=True)
    annual_wide = long_table.pivot(index="year", columns="cluster", values="display").reset_index()
    annual_wide.columns.name = None
    effective = long_table.groupby("year")["effective_year"].first()
    annual_wide.insert(1, "effective_year", annual_wide["year"].map(effective).astype(int))
    cluster_counts = long_table.groupby("year")["cluster"].nunique()
    annual_wide.insert(2, "cluster_count", annual_wide["year"].map(cluster_counts).astype(int))

    ticker_wide = pd.DataFrame(ticker_cells).pivot(index="ticker", columns="year", values="cluster")
    ticker_wide = ticker_wide.reindex(sorted(ticker_wide.columns), axis=1).reset_index()
    ticker_wide.columns.name = None
    first_year = data.groupby("ticker")["year"].min()
    last_year = data.groupby("ticker")["year"].max()
    ticker_wide.insert(1, "first_year", ticker_wide["ticker"].map(first_year).astype(int))
    ticker_wide.insert(2, "last_year", ticker_wide["ticker"].map(last_year).astype(int))
    return long_table, annual_wide, ticker_wide


def render_cluster_evolution_markdown(long_table: pd.DataFrame) -> str:
    lines = [
        "# CL Annual Return Cluster Evolution, 2010-2025",
        "",
        "Cluster IDs are local to each estimation year and are not persistent sector identifiers. ",
        "A full-year classification for year Y is only usable without look-ahead from year Y+1.",
        "A blank ticker-year cell means the ticker was not included in that year's eligible PIT clustering universe; ",
        "it does not by itself mean the security was unavailable or delisted.",
        "",
        "| Estimation year | Effective year | Cluster | Representative | Dominant role | Size | Members |",
        "| ---: | ---: | :--- | :--- | :--- | ---: | :--- |",
    ]
    for row in long_table.itertuples(index=False):
        lines.append(
            f"| {row.year} | {row.effective_year} | {row.cluster} | {row.representative} | "
            f"{row.dominant_role} | {row.cluster_size} | {row.members} |"
        )
    return "\n".join(lines) + "\n"
