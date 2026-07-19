from __future__ import annotations

import csv
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


WPSR_REVIEW_SCHEMA_VERSION = "1"

REVIEW_COLUMNS = [
    "schema_version",
    "series_id",
    "series_name",
    "state_family",
    "geography",
    "api_unit",
    "crosswalk_status",
    "evidence_status",
    "evidence_release_count",
    "evidence_numeric_match_count",
    "auto_recommendation",
    "auto_confidence",
    "auto_reason",
    "selected_archive_row_key",
    "selected_numeric_relation",
    "selected_context_compatible",
    "candidate_1",
    "candidate_2",
    "candidate_3",
    "reviewer_decision",
    "reviewer",
    "reviewed_at",
    "reviewer_notes",
]

CANONICAL_COLUMNS = [
    "schema_version",
    "canonical_dataset_key",
    "release_product",
    "series_id",
    "series_name",
    "state_family",
    "geography",
    "api_unit",
    "archive_row_key",
    "archive_stub_1",
    "archive_group_label",
    "archive_stub_2",
    "numeric_relation",
    "value_transform",
    "reviewer",
    "reviewed_at",
    "reviewer_notes",
    "source_review_checksum",
]

APPROVAL_AUDIT_COLUMNS = [
    "series_id",
    "reviewer_decision",
    "selected_archive_row_key",
    "status",
    "error",
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


def _file_checksum(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _iso_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _recommendation(status: str) -> tuple[str, str, str]:
    if status == "unique_exact_candidate_manual_review":
        return (
            "approve_after_label_check",
            "high",
            "One exact numeric candidate; verify measure, product, geography, and unit labels.",
        )
    if status == "ranked_numeric_candidates_manual_review":
        return (
            "inspect_ranked_candidates",
            "medium",
            "Several numeric candidates exist; confirm the selected archive row by semantics.",
        )
    if status == "ambiguous_numeric_candidates_manual_review":
        return (
            "defer_until_nonzero_multi_release_evidence",
            "low",
            "The candidates are numerically ambiguous, commonly because the observed value is zero.",
        )
    if status == "unresolved_subcategory_mismatch":
        return (
            "reject_current_candidate",
            "high",
            "The best numeric match has an incompatible product subcategory.",
        )
    if status == "unresolved_no_numeric_confirmation":
        return (
            "defer_definition_review",
            "low",
            "No archived row reproduces the API value under an allowed unit transform.",
        )
    return ("defer", "low", "The automated crosswalk did not establish a safe mapping.")


def _candidate_text(row: dict[str, str]) -> str:
    if not row:
        return ""
    labels = " | ".join(
        value
        for value in (
            row.get("archive_stub_1", ""),
            row.get("archive_group_label", ""),
            row.get("archive_stub_2", ""),
        )
        if value
    )
    return (
        f"{row.get('archive_row_key', '')} :: {labels} :: "
        f"relation={row.get('numeric_relation', '')} :: "
        f"context={row.get('context_compatible', '')} :: "
        f"score={row.get('combined_score', '')}"
    )


def build_wpsr_crosswalk_review(
    *,
    audit_path: Path = Path("data/external/eia/archive_pilot/wpsr_crosswalk_audit.csv"),
    candidates_path: Path = Path(
        "data/external/eia/archive_pilot/wpsr_crosswalk_candidates.csv"
    ),
    evidence_audit_path: Path = Path(
        "data/external/eia/wpsr_crosswalk_evidence/wpsr_crosswalk_multi_release_audit.csv"
    ),
    output_path: Path = Path("config/eia_wpsr_crosswalk_review.csv"),
) -> dict[str, Any]:
    audits = _read_csv(Path(audit_path))
    candidates = _read_csv(Path(candidates_path))
    if not audits:
        raise ValueError(f"No WPSR crosswalk audit rows found: {audit_path}")

    by_series: dict[str, list[dict[str, str]]] = {}
    for row in candidates:
        by_series.setdefault(row.get("series_id", ""), []).append(row)
    for rows in by_series.values():
        rows.sort(key=lambda row: int(row.get("candidate_rank") or 999))

    existing = {row.get("series_id", ""): row for row in _read_csv(Path(output_path))}
    evidence = {
        row.get("series_id", ""): row for row in _read_csv(Path(evidence_audit_path))
    }
    output: list[dict[str, Any]] = []
    for audit in sorted(audits, key=lambda row: row.get("series_id", "")):
        series_id = audit.get("series_id", "")
        ranked = by_series.get(series_id, [])
        top = ranked[0] if ranked else {}
        recommendation, confidence, reason = _recommendation(
            audit.get("crosswalk_status", "")
        )
        prior = existing.get(series_id, {})
        support = evidence.get(series_id, {})
        evidence_status = support.get("evidence_status", "")
        if evidence_status == "multi_release_unique_candidate_manual_review":
            recommendation = "approve_after_multi_release_label_check"
            confidence = "high"
            reason = "The same compatible archive row matches every tested release; verify labels."
        elif evidence_status == "multi_release_ambiguous_manual_review":
            recommendation = "defer_ambiguous_multi_release_candidates"
            confidence = "low"
            reason = "Multiple archive rows remain numerically tied across tested releases."
        preserve = {
            column: prior.get(column, "")
            for column in ("reviewer_decision", "reviewer", "reviewed_at", "reviewer_notes")
        }
        output.append(
            {
                "schema_version": WPSR_REVIEW_SCHEMA_VERSION,
                "series_id": series_id,
                "series_name": audit.get("series_name", ""),
                "state_family": audit.get("state_family", ""),
                "geography": audit.get("geography", ""),
                "api_unit": audit.get("api_unit", ""),
                "crosswalk_status": audit.get("crosswalk_status", ""),
                "evidence_status": evidence_status,
                "evidence_release_count": support.get("release_count", ""),
                "evidence_numeric_match_count": support.get(
                    "top_numeric_match_release_count", ""
                ),
                "auto_recommendation": recommendation,
                "auto_confidence": confidence,
                "auto_reason": reason,
                "selected_archive_row_key": prior.get("selected_archive_row_key")
                or support.get("top_archive_row_key")
                or top.get("archive_row_key", ""),
                "selected_numeric_relation": top.get("numeric_relation", ""),
                "selected_context_compatible": top.get("context_compatible", ""),
                "candidate_1": _candidate_text(ranked[0]) if len(ranked) > 0 else "",
                "candidate_2": _candidate_text(ranked[1]) if len(ranked) > 1 else "",
                "candidate_3": _candidate_text(ranked[2]) if len(ranked) > 2 else "",
                **preserve,
            }
        )

    _atomic_write_csv(Path(output_path), output, REVIEW_COLUMNS)
    return {
        "row_count": len(output),
        "high_confidence_count": sum(row["auto_confidence"] == "high" for row in output),
        "manual_decision_count": sum(bool(row["reviewer_decision"]) for row in output),
        "output_path": str(output_path),
    }


def _value_transform(relation: str) -> str:
    return {
        "exact": "archive_value",
        "api_div_1000": "archive_value * 1000",
        "api_mul_1000": "archive_value / 1000",
    }.get(relation, "")


def approve_wpsr_crosswalk(
    *,
    review_path: Path = Path("config/eia_wpsr_crosswalk_review.csv"),
    candidates_path: Path = Path(
        "data/external/eia/archive_pilot/wpsr_crosswalk_candidates.csv"
    ),
    output_path: Path = Path("config/eia_wpsr_crosswalk.csv"),
    audit_output_path: Path = Path(
        "data/external/eia/catalog/wpsr_crosswalk_approval_audit.csv"
    ),
) -> dict[str, Any]:
    reviews = _read_csv(Path(review_path))
    candidates = _read_csv(Path(candidates_path))
    if not reviews:
        raise ValueError(f"No WPSR crosswalk review rows found: {review_path}")
    candidate_index = {
        (row.get("series_id", ""), row.get("archive_row_key", "")): row
        for row in candidates
    }
    review_checksum = _file_checksum(Path(review_path))

    canonical: list[dict[str, Any]] = []
    audit: list[dict[str, Any]] = []
    for review in reviews:
        decision = review.get("reviewer_decision", "").strip().lower()
        series_id = review.get("series_id", "")
        row_key = review.get("selected_archive_row_key", "")
        status = "not_approved"
        error = ""
        if decision not in {"", "approve", "reject", "defer"}:
            status = "error"
            error = "reviewer_decision must be approve, reject, defer, or blank"
        elif decision == "approve":
            candidate = candidate_index.get((series_id, row_key))
            if candidate is None:
                status = "error"
                error = "selected archive row is not present in the candidate file"
            elif candidate.get("numeric_relation") not in {
                "exact",
                "api_div_1000",
                "api_mul_1000",
            }:
                status = "error"
                error = "selected archive row has no approved numeric relation"
            elif str(candidate.get("context_compatible", "")).lower() != "true":
                status = "error"
                error = "selected archive row has an incompatible product subcategory"
            elif not review.get("reviewer", "").strip() or not review.get(
                "reviewed_at", ""
            ).strip():
                status = "error"
                error = "approved rows require reviewer and reviewed_at"
            else:
                status = "approved"
                relation = candidate["numeric_relation"]
                canonical.append(
                    {
                        "schema_version": WPSR_REVIEW_SCHEMA_VERSION,
                        "canonical_dataset_key": "eia/wpsr/table9",
                        "release_product": "WPSR",
                        "series_id": series_id,
                        "series_name": review.get("series_name", ""),
                        "state_family": review.get("state_family", ""),
                        "geography": review.get("geography", ""),
                        "api_unit": review.get("api_unit", ""),
                        "archive_row_key": row_key,
                        "archive_stub_1": candidate.get("archive_stub_1", ""),
                        "archive_group_label": candidate.get("archive_group_label", ""),
                        "archive_stub_2": candidate.get("archive_stub_2", ""),
                        "numeric_relation": relation,
                        "value_transform": _value_transform(relation),
                        "reviewer": review.get("reviewer", ""),
                        "reviewed_at": review.get("reviewed_at", ""),
                        "reviewer_notes": review.get("reviewer_notes", ""),
                        "source_review_checksum": review_checksum,
                    }
                )
        audit.append(
            {
                "series_id": series_id,
                "reviewer_decision": decision,
                "selected_archive_row_key": row_key,
                "status": status,
                "error": error,
            }
        )

    duplicate_keys = len({row["archive_row_key"] for row in canonical}) != len(canonical)
    if duplicate_keys:
        raise ValueError("One archived WPSR row cannot be approved for multiple API series")
    _atomic_write_csv(Path(output_path), canonical, CANONICAL_COLUMNS)
    _atomic_write_csv(Path(audit_output_path), audit, APPROVAL_AUDIT_COLUMNS)
    errors = [row for row in audit if row["status"] == "error"]
    return {
        "review_row_count": len(reviews),
        "approved_count": len(canonical),
        "rejected_count": sum(row["reviewer_decision"] == "reject" for row in audit),
        "deferred_count": sum(row["reviewer_decision"] == "defer" for row in audit),
        "error_count": len(errors),
        "output_path": str(output_path),
        "audit_output_path": str(audit_output_path),
        "built_at": _iso_utc(),
    }
