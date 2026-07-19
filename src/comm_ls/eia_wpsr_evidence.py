from __future__ import annotations

import csv
import statistics
from pathlib import Path
from typing import Any, Callable

from comm_ls.eia_wpsr_crosswalk import run_wpsr_crosswalk_validation


EVIDENCE_COLUMNS = [
    "series_id",
    "series_name",
    "state_family",
    "geography",
    "archive_row_key",
    "archive_stub_1",
    "archive_group_label",
    "archive_stub_2",
    "release_count",
    "numeric_match_release_count",
    "exact_match_release_count",
    "scaled_match_release_count",
    "context_compatible_release_count",
    "mean_semantic_score",
    "mean_combined_score",
]

EVIDENCE_AUDIT_COLUMNS = [
    "series_id",
    "series_name",
    "state_family",
    "geography",
    "release_count",
    "top_archive_row_key",
    "top_numeric_match_release_count",
    "top_context_compatible_release_count",
    "runner_up_numeric_match_release_count",
    "evidence_status",
    "approved_crosswalk",
]


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return [dict(row) for row in csv.DictReader(handle)]


def _atomic_write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def aggregate_wpsr_crosswalk_evidence(
    candidate_rows: list[dict[str, str]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = {}
    series_releases: dict[str, set[str]] = {}
    for row in candidate_rows:
        key = (row.get("series_id", ""), row.get("archive_row_key", ""))
        grouped.setdefault(key, []).append(row)
        series_releases.setdefault(key[0], set()).add(row.get("release_date", ""))

    evidence: list[dict[str, Any]] = []
    for (series_id, row_key), rows in grouped.items():
        relations = [row.get("numeric_relation", "") for row in rows]
        numeric = [relation in {"exact", "api_div_1000", "api_mul_1000"} for relation in relations]
        evidence.append(
            {
                "series_id": series_id,
                "series_name": rows[0].get("series_name", ""),
                "state_family": rows[0].get("state_family", ""),
                "geography": rows[0].get("geography", ""),
                "archive_row_key": row_key,
                "archive_stub_1": rows[0].get("archive_stub_1", ""),
                "archive_group_label": rows[0].get("archive_group_label", ""),
                "archive_stub_2": rows[0].get("archive_stub_2", ""),
                "release_count": len(series_releases.get(series_id, set())),
                "numeric_match_release_count": sum(numeric),
                "exact_match_release_count": relations.count("exact"),
                "scaled_match_release_count": sum(
                    relation in {"api_div_1000", "api_mul_1000"} for relation in relations
                ),
                "context_compatible_release_count": sum(
                    str(row.get("context_compatible", "")).lower() == "true" for row in rows
                ),
                "mean_semantic_score": statistics.fmean(
                    float(row.get("semantic_score") or 0.0) for row in rows
                ),
                "mean_combined_score": statistics.fmean(
                    float(row.get("combined_score") or 0.0) for row in rows
                ),
            }
        )
    evidence.sort(
        key=lambda row: (
            row["series_id"],
            -row["numeric_match_release_count"],
            -row["context_compatible_release_count"],
            -row["mean_semantic_score"],
            row["archive_row_key"],
        )
    )

    audit: list[dict[str, Any]] = []
    by_series: dict[str, list[dict[str, Any]]] = {}
    for row in evidence:
        by_series.setdefault(row["series_id"], []).append(row)
    for series_id, rows in sorted(by_series.items()):
        top = rows[0]
        runner_up = rows[1] if len(rows) > 1 else {}
        release_count = int(top["release_count"])
        matches = int(top["numeric_match_release_count"])
        compatible = int(top["context_compatible_release_count"])
        runner_matches = int(runner_up.get("numeric_match_release_count", 0))
        if release_count >= 2 and matches == release_count and compatible == release_count:
            status = (
                "multi_release_unique_candidate_manual_review"
                if matches > runner_matches
                else "multi_release_ambiguous_manual_review"
            )
        elif matches > 0 and compatible == matches:
            status = "partial_numeric_evidence_manual_review"
        elif matches > 0:
            status = "subcategory_conflict"
        else:
            status = "unresolved_no_numeric_evidence"
        audit.append(
            {
                "series_id": series_id,
                "series_name": top["series_name"],
                "state_family": top["state_family"],
                "geography": top["geography"],
                "release_count": release_count,
                "top_archive_row_key": top["archive_row_key"],
                "top_numeric_match_release_count": matches,
                "top_context_compatible_release_count": compatible,
                "runner_up_numeric_match_release_count": runner_matches,
                "evidence_status": status,
                "approved_crosswalk": False,
            }
        )
    return evidence, audit


def validate_wpsr_crosswalk_evidence(
    *,
    release_dates: tuple[str, ...],
    shortlist_path: Path = Path("config/eia_series_shortlist.csv"),
    archive_releases_path: Path = Path(
        "data/external/eia/wpsr_archive/wpsr_archive_releases.csv"
    ),
    archive_values_path: Path = Path(
        "data/external/eia/wpsr_archive/wpsr_archive_values.csv"
    ),
    output_dir: Path = Path("data/external/eia/wpsr_crosswalk_evidence"),
    api_key: str | None = None,
    api_key_env: str = "EIA_API_KEY",
    base_url: str = "https://api.eia.gov/v2",
    bronze_dir: Path = Path("data/external/eia/bronze/wpsr_crosswalk"),
    cache_dir: Path = Path("data/external/eia/request_cache"),
    manifest_dir: Path = Path("data/external/eia/manifests"),
    timeout_seconds: float = 30.0,
    max_retries: int = 3,
    request_delay_seconds: float = 0.25,
    refresh_cache: bool = False,
    top_n: int = 5,
    fetcher: Callable[[str], bytes] | None = None,
) -> dict[str, Any]:
    if len(set(release_dates)) < 2:
        raise ValueError("Multi-release WPSR evidence requires at least two release dates")
    output_dir = Path(output_dir)
    all_candidates: list[dict[str, str]] = []
    network_requests = 0
    errors = 0
    for release_date in sorted(set(release_dates)):
        release_output = output_dir / "releases" / f"release_date={release_date}"
        summary = run_wpsr_crosswalk_validation(
            release_date=release_date,
            shortlist_path=shortlist_path,
            archive_releases_path=archive_releases_path,
            archive_values_path=archive_values_path,
            output_dir=release_output,
            api_key=api_key,
            api_key_env=api_key_env,
            base_url=base_url,
            bronze_dir=bronze_dir,
            cache_dir=cache_dir,
            manifest_dir=manifest_dir,
            timeout_seconds=timeout_seconds,
            max_retries=max_retries,
            request_delay_seconds=request_delay_seconds,
            refresh_cache=refresh_cache,
            top_n=top_n,
            fetcher=fetcher,
        )
        network_requests += int(summary["network_requests"])
        errors += int(summary["request_error_count"]) + int(summary["api_missing_count"])
        all_candidates.extend(_read_csv(release_output / "wpsr_crosswalk_candidates.csv"))
    evidence, audit = aggregate_wpsr_crosswalk_evidence(all_candidates)
    evidence_path = output_dir / "wpsr_crosswalk_multi_release_evidence.csv"
    audit_path = output_dir / "wpsr_crosswalk_multi_release_audit.csv"
    _atomic_write_csv(evidence_path, evidence, EVIDENCE_COLUMNS)
    _atomic_write_csv(audit_path, audit, EVIDENCE_AUDIT_COLUMNS)
    return {
        "release_count": len(set(release_dates)),
        "series_count": len(audit),
        "evidence_row_count": len(evidence),
        "strong_candidate_count": sum(
            row["evidence_status"] == "multi_release_unique_candidate_manual_review"
            for row in audit
        ),
        "error_count": errors,
        "network_requests": network_requests,
        "approved_crosswalk_count": 0,
        "evidence_path": str(evidence_path),
        "audit_path": str(audit_path),
    }

