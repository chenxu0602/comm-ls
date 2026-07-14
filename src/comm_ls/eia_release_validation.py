from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


EIA_RELEASE_VALIDATION_SCHEMA_VERSION = "1"

RELEASE_CALENDAR_REQUIRED_COLUMNS = {
    "release_product",
    "frequency",
    "timezone",
    "normal_release_rule",
    "release_time_status",
    "official_release_calendar_url",
    "product_page_url",
    "revision_policy_url",
    "release_timestamp_source",
    "historical_vintage_status",
    "point_in_time_status",
    "research_backfill_status",
    "deployable_backtest_status",
    "tradable_after_rule",
}

ALLOWED_RELEASE_TIME_STATUSES = {"official_exact", "first_seen_required"}
ALLOWED_HISTORICAL_VINTAGE_STATUSES = {
    "release_archive_reconstruction_required",
    "latest_revised_history_only",
}

AUDIT_COLUMNS = [
    "schema_version",
    "audited_at",
    "release_product",
    "shortlist_rows",
    "initial_core_rows",
    "release_calendar_present",
    "release_time_status",
    "historical_vintage_status",
    "point_in_time_status",
    "research_backfill_status",
    "deployable_backtest_status",
    "approved_for_backfill_rows",
    "pit_status_mismatch_rows",
    "error_count",
    "errors",
]


def _iso_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(path)
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


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def _file_checksum(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _truthy(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes"}


def _is_official_eia_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme == "https" and parsed.hostname in {"eia.gov", "www.eia.gov"}


def expected_point_in_time_status(release_product: str) -> str:
    statuses = {
        "WPSR": "historical_release_archive_required",
        "PSM": "forward_capture_required_latest_history_revised",
        "COMPANY_CRUDE_IMPORTS": "forward_capture_required_final_history_revised",
    }
    return statuses.get(release_product, "release_validation_required")


def audit_eia_release_readiness(
    *,
    release_calendar_path: Path = Path("config/eia_release_calendar.csv"),
    series_shortlist_path: Path = Path("config/eia_series_shortlist.csv"),
    output_path: Path = Path("data/external/eia/catalog/release_readiness_audit.csv"),
    manifest_dir: Path = Path("data/external/eia/manifests"),
) -> dict[str, Any]:
    calendar_rows = _read_csv(Path(release_calendar_path))
    shortlist_rows = _read_csv(Path(series_shortlist_path))
    if not calendar_rows:
        raise ValueError(f"EIA release calendar is empty: {release_calendar_path}")
    if not shortlist_rows:
        raise ValueError(f"EIA series shortlist is empty: {series_shortlist_path}")

    missing_columns = RELEASE_CALENDAR_REQUIRED_COLUMNS - set(calendar_rows[0])
    if missing_columns:
        raise ValueError(f"EIA release calendar missing columns: {sorted(missing_columns)}")

    calendar_by_product: dict[str, dict[str, str]] = {}
    duplicate_products: set[str] = set()
    for row in calendar_rows:
        product = row["release_product"]
        if product in calendar_by_product:
            duplicate_products.add(product)
        calendar_by_product[product] = row

    audited_at = _iso_utc()
    audit_rows: list[dict[str, Any]] = []
    products = sorted({row["release_product"] for row in shortlist_rows} | set(calendar_by_product))
    for product in products:
        rows = [row for row in shortlist_rows if row["release_product"] == product]
        calendar = calendar_by_product.get(product)
        errors: list[str] = []
        if calendar is None:
            errors.append("missing_release_calendar_row")
            calendar = {}
        if product in duplicate_products:
            errors.append("duplicate_release_calendar_row")

        release_time_status = calendar.get("release_time_status", "")
        historical_vintage_status = calendar.get("historical_vintage_status", "")
        if calendar and release_time_status not in ALLOWED_RELEASE_TIME_STATUSES:
            errors.append("invalid_release_time_status")
        if calendar and historical_vintage_status not in ALLOWED_HISTORICAL_VINTAGE_STATUSES:
            errors.append("invalid_historical_vintage_status")
        if calendar and calendar.get("timezone") != "America/New_York":
            errors.append("timezone_must_be_America_New_York")
        for field in ("official_release_calendar_url", "product_page_url", "revision_policy_url"):
            if calendar and not _is_official_eia_url(calendar.get(field, "")):
                errors.append(f"non_official_or_missing_url:{field}")

        expected_status = calendar.get("point_in_time_status", "")
        mismatch_count = sum(row.get("point_in_time_status") != expected_status for row in rows)
        approved_count = sum(_truthy(row.get("approved_for_backfill", "")) for row in rows)
        if mismatch_count:
            errors.append("shortlist_point_in_time_status_mismatch")
        if approved_count:
            errors.append("observation_backfill_not_authorized_at_release_validation_stage")
        if calendar.get("deployable_backtest_status") == "approved":
            errors.append("deployable_backtest_cannot_be_approved_before_vintage_reconstruction")

        audit_rows.append(
            {
                "schema_version": EIA_RELEASE_VALIDATION_SCHEMA_VERSION,
                "audited_at": audited_at,
                "release_product": product,
                "shortlist_rows": len(rows),
                "initial_core_rows": sum(_truthy(row.get("proposed_initial_core", "")) for row in rows),
                "release_calendar_present": bool(calendar),
                "release_time_status": release_time_status,
                "historical_vintage_status": historical_vintage_status,
                "point_in_time_status": expected_status,
                "research_backfill_status": calendar.get("research_backfill_status", ""),
                "deployable_backtest_status": calendar.get("deployable_backtest_status", ""),
                "approved_for_backfill_rows": approved_count,
                "pit_status_mismatch_rows": mismatch_count,
                "error_count": len(errors),
                "errors": "|".join(errors),
            }
        )

    _atomic_write_csv(Path(output_path), audit_rows, AUDIT_COLUMNS)
    error_count = sum(int(row["error_count"]) for row in audit_rows)
    result = {
        "schema_version": EIA_RELEASE_VALIDATION_SCHEMA_VERSION,
        "audited_at": audited_at,
        "release_product_count": len(audit_rows),
        "shortlist_row_count": len(shortlist_rows),
        "initial_core_row_count": sum(
            _truthy(row.get("proposed_initial_core", "")) for row in shortlist_rows
        ),
        "approved_for_backfill_count": sum(
            _truthy(row.get("approved_for_backfill", "")) for row in shortlist_rows
        ),
        "error_count": error_count,
        "network_requests": 0,
        "observation_rows_downloaded": 0,
        "inputs": {
            str(release_calendar_path): _file_checksum(Path(release_calendar_path)),
            str(series_shortlist_path): _file_checksum(Path(series_shortlist_path)),
        },
        "output_path": str(output_path),
        "output_sha256": _file_checksum(Path(output_path)),
    }
    run_id = datetime.fromisoformat(audited_at.replace("Z", "+00:00")).strftime(
        "%Y%m%dT%H%M%S%fZ"
    )
    manifest_path = Path(manifest_dir) / f"release_readiness_{run_id}_summary.json"
    result["manifest_path"] = str(manifest_path)
    _atomic_write_json(manifest_path, result)
    return result
