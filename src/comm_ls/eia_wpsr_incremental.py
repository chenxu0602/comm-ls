from __future__ import annotations

import csv
import hashlib
import json
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Callable

from comm_ls.eia_wpsr_archive import (
    COMPARISON_COLUMNS,
    RELEASE_COLUMNS,
    REVISION_COLUMNS,
    SCHEMA_CHANGE_COLUMNS,
    VALUE_COLUMNS,
    compare_wpsr_release_values,
    run_wpsr_archive_pilot,
)


WPSR_INCREMENTAL_SCHEMA_VERSION = "1"


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


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def _release_dates(path: Path) -> tuple[str, ...]:
    if not path.exists():
        raise FileNotFoundError(path)
    text = path.read_text(encoding="utf-8")
    rows = list(csv.DictReader(text.splitlines()))
    if rows and "release_date" in rows[0]:
        values = [
            row.get("release_date", "")
            for row in rows
            if not row.get("status", "").strip().lower().startswith("exclude_")
        ]
    else:
        values = [line.strip().split(",")[0] for line in text.splitlines()]
        if values and values[0].lower() == "release_date":
            values = values[1:]
    normalized = sorted({date.fromisoformat(value).isoformat() for value in values if value})
    if not normalized:
        raise ValueError(f"No release dates found: {path}")
    return tuple(normalized)


def _merge_by_key(
    existing: list[dict[str, str]],
    incoming: list[dict[str, str]],
    key_columns: tuple[str, ...],
) -> list[dict[str, str]]:
    merged = {tuple(row.get(column, "") for column in key_columns): row for row in existing}
    for row in incoming:
        merged[tuple(row.get(column, "") for column in key_columns)] = row
    return [merged[key] for key in sorted(merged)]


def _chunks(values: list[str], size: int) -> list[list[str]]:
    return [values[index : index + size] for index in range(0, len(values), size)]


def update_wpsr_archive_incrementally(
    *,
    release_dates_path: Path = Path("config/eia_wpsr_release_dates.csv"),
    output_dir: Path = Path("data/external/eia/wpsr_archive"),
    bronze_dir: Path = Path("data/external/eia/bronze/wpsr_archive"),
    cache_dir: Path = Path("data/external/eia/request_cache"),
    manifest_dir: Path = Path("data/external/eia/manifests"),
    timeout_seconds: float = 30.0,
    max_retries: int = 3,
    request_delay_seconds: float = 0.2,
    progress_every_batches: int = 1,
    refresh_cache: bool = False,
    fetcher: Callable[[str], bytes] | None = None,
    progress: Callable[[str], None] | None = None,
) -> dict[str, Any]:
    if progress_every_batches < 1:
        raise ValueError("progress_every_batches must be at least 1")
    requested = _release_dates(Path(release_dates_path))
    output_dir = Path(output_dir)
    releases_path = output_dir / "wpsr_archive_releases.csv"
    values_path = output_dir / "wpsr_archive_values.csv"
    existing_releases = _read_csv(releases_path)
    existing_values = _read_csv(values_path)
    successful = {
        row.get("requested_release_date", "")
        for row in existing_releases
        if row.get("status") == "ok"
    }
    pending = [value for value in requested if refresh_cache or value not in successful]
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    batch_root = output_dir / "batches" / run_id
    incoming_releases: list[dict[str, str]] = []
    incoming_values: list[dict[str, str]] = []
    network_requests = 0

    batches = _chunks(pending, 5)
    if progress is not None:
        progress(
            f"WPSR incremental start: requested={len(requested):,}, "
            f"already_successful={len(successful):,}, pending={len(pending):,}, "
            f"batches={len(batches):,}"
        )

    for batch_number, batch in enumerate(batches, start=1):
        context_dates: list[str] = []
        if len(batch) == 1:
            available_context = sorted(successful | (set(requested) - set(batch)))
            if not available_context:
                raise ValueError("A one-date WPSR update requires at least one context release date")
            context_dates.append(min(available_context, key=lambda value: abs((date.fromisoformat(value) - date.fromisoformat(batch[0])).days)))
        pilot_dates = tuple(sorted(set(batch + context_dates)))
        batch_dir = batch_root / f"batch_{batch_number:04d}"
        summary = run_wpsr_archive_pilot(
            release_dates=pilot_dates,
            output_dir=batch_dir,
            bronze_dir=Path(bronze_dir),
            cache_dir=Path(cache_dir),
            manifest_dir=Path(manifest_dir),
            timeout_seconds=timeout_seconds,
            max_retries=max_retries,
            request_delay_seconds=request_delay_seconds,
            refresh_cache=refresh_cache,
            fetcher=fetcher,
        )
        network_requests += int(summary["network_requests"])
        incoming_releases.extend(_read_csv(batch_dir / "wpsr_archive_pilot_releases.csv"))
        incoming_values.extend(_read_csv(batch_dir / "wpsr_archive_pilot_values.csv"))
        if progress is not None and (
            batch_number % progress_every_batches == 0 or batch_number == len(batches)
        ):
            progress(
                f"WPSR batch {batch_number:,}/{len(batches):,}: "
                f"dates={batch[0]}..{batch[-1]}, "
                f"successful={summary['successful_release_count']:,}, "
                f"errors={summary['release_error_count']:,}, "
                f"values={summary['value_row_count']:,}, "
                f"network_requests_total={network_requests:,}"
            )

    releases = _merge_by_key(
        existing_releases,
        incoming_releases,
        ("requested_release_date",),
    )
    values = _merge_by_key(
        existing_values,
        incoming_values,
        ("release_date", "observation_date", "observation_column", "row_key"),
    )
    comparisons, revisions, schema_changes = compare_wpsr_release_values(values)
    comparisons_path = output_dir / "wpsr_archive_comparisons.csv"
    revisions_path = output_dir / "wpsr_archive_revisions.csv"
    schema_changes_path = output_dir / "wpsr_archive_schema_changes.csv"
    _atomic_write_csv(releases_path, releases, RELEASE_COLUMNS)
    _atomic_write_csv(values_path, values, VALUE_COLUMNS)
    _atomic_write_csv(comparisons_path, comparisons, COMPARISON_COLUMNS)
    _atomic_write_csv(revisions_path, revisions, REVISION_COLUMNS)
    _atomic_write_csv(schema_changes_path, schema_changes, SCHEMA_CHANGE_COLUMNS)

    outputs = [releases_path, values_path, comparisons_path, revisions_path, schema_changes_path]
    result = {
        "schema_version": WPSR_INCREMENTAL_SCHEMA_VERSION,
        "run_id": run_id,
        "requested_release_count": len(requested),
        "previous_successful_release_count": len(successful),
        "pending_release_count": len(pending),
        "successful_release_count": sum(row.get("status") == "ok" for row in releases),
        "release_error_count": sum(row.get("status") != "ok" for row in releases),
        "value_row_count": len(values),
        "revision_count": len(revisions),
        "schema_change_count": len(schema_changes),
        "network_requests": network_requests,
        "observation_backfill_authorized": False,
        "outputs": {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in outputs},
    }
    manifest_path = Path(manifest_dir) / f"wpsr_archive_incremental_{run_id}_summary.json"
    result["manifest_path"] = str(manifest_path)
    _atomic_write_json(manifest_path, result)
    return result
