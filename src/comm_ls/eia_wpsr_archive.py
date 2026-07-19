from __future__ import annotations

import csv
import hashlib
import html
import io
import json
import re
import time
import urllib.error
import urllib.request
from collections import defaultdict
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Callable


WPSR_ARCHIVE_SCHEMA_VERSION = "3"
DEFAULT_WPSR_PILOT_RELEASE_DATES = ("2025-01-08", "2025-01-15", "2025-01-23")
WPSR_ARCHIVE_BASE_URL = "https://www.eia.gov/petroleum/supply/weekly/archive"

RELEASE_COLUMNS = [
    "schema_version",
    "fetched_at",
    "requested_release_date",
    "parsed_release_date",
    "week_ending_date",
    "page_url",
    "table_url",
    "page_checksum",
    "table_checksum",
    "page_from_cache",
    "table_from_cache",
    "table_row_count",
    "current_observation_date",
    "previous_observation_date",
    "metadata_quality",
    "metadata_warning",
    "status",
    "error",
]

VALUE_COLUMNS = [
    "schema_version",
    "release_date",
    "week_ending_date",
    "observation_date",
    "observation_column",
    "row_number",
    "stub_1",
    "stub_2",
    "group_label",
    "stub_occurrence",
    "row_key",
    "value_raw",
    "value_numeric",
    "source_table_checksum",
]

COMPARISON_COLUMNS = [
    "schema_version",
    "older_release_date",
    "newer_release_date",
    "overlap_observation_date",
    "older_value_count",
    "newer_value_count",
    "common_key_count",
    "exact_match_count",
    "numeric_match_count",
    "revision_count",
    "missing_from_newer_count",
    "new_in_newer_count",
    "revision_share",
    "status",
]

REVISION_COLUMNS = [
    "schema_version",
    "older_release_date",
    "newer_release_date",
    "observation_date",
    "row_key",
    "stub_1",
    "stub_2",
    "older_value_raw",
    "newer_value_raw",
    "older_value_numeric",
    "newer_value_numeric",
]

SCHEMA_CHANGE_COLUMNS = [
    "schema_version",
    "older_release_date",
    "newer_release_date",
    "observation_date",
    "change_type",
    "row_key",
    "stub_1",
    "stub_2",
    "value_raw",
    "value_numeric",
]


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _iso_utc(value: datetime | None = None) -> str:
    return (value or _utc_now()).isoformat().replace("+00:00", "Z")


def _hash_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _atomic_write_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(content)
    temporary.replace(path)


def _atomic_write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    _atomic_write_bytes(
        path,
        (json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n").encode(),
    )


def _file_checksum(path: Path) -> str:
    return _hash_bytes(path.read_bytes())


def _clean_html_text(content: bytes) -> str:
    text = content.decode("utf-8", errors="replace")
    text = re.sub(r"<script\b[^>]*>.*?</script>", " ", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<style\b[^>]*>.*?</style>", " ", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    return " ".join(html.unescape(text).replace("\xa0", " ").split())


def parse_wpsr_archive_page(content: bytes) -> tuple[str, str]:
    text = _clean_html_text(content)
    match = re.search(
        r"Data for week ending\s+([A-Z][a-z]+ \d{1,2}, \d{4})\s*\|\s*"
        r"Release Date:\s*([A-Z][a-z]+ \d{1,2}, \d{4})",
        text,
    )
    if not match:
        raise ValueError("WPSR archive page does not contain release/week-ending metadata")
    week_ending = datetime.strptime(match.group(1), "%B %d, %Y").date().isoformat()
    release_date = datetime.strptime(match.group(2), "%B %d, %Y").date().isoformat()
    return release_date, week_ending


def _parse_archive_date(value: str, release_year: int) -> str:
    parsed = datetime.strptime(value.strip(), "%m/%d/%y").date()
    if abs(parsed.year - release_year) > 2:
        raise ValueError(f"Unexpected WPSR table date {value!r} for release year {release_year}")
    return parsed.isoformat()


def _numeric(value: str) -> float | None:
    cleaned = value.strip().replace(",", "")
    if not cleaned or cleaned in {"--", "NA", "N/A", "�"}:
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None


def _table_header_dates(content: bytes, release_date: str) -> tuple[str, str]:
    decoded = content.decode("utf-8", errors="replace")
    rows = csv.reader(io.StringIO(decoded))
    header = next(rows, [])
    if len(header) < 4:
        raise ValueError("WPSR table9 CSV is missing expected header columns")
    release_year = date.fromisoformat(release_date).year
    return (
        _parse_archive_date(header[2], release_year),
        _parse_archive_date(header[3], release_year),
    )


def _validate_table_timing(
    release_date: str,
    current_observation_date: str,
    previous_observation_date: str,
) -> None:
    release_day = date.fromisoformat(release_date)
    current_day = date.fromisoformat(current_observation_date)
    previous_day = date.fromisoformat(previous_observation_date)
    lag_days = (release_day - current_day).days
    if current_day.weekday() != 4:
        raise ValueError(
            f"WPSR current observation is not Friday: {current_observation_date}"
        )
    if (current_day - previous_day).days != 7:
        raise ValueError(
            "WPSR current/previous observations are not seven days apart: "
            f"current={current_observation_date}, previous={previous_observation_date}"
        )
    if not 5 <= lag_days <= 10:
        raise ValueError(
            "WPSR release/table timing is implausible: "
            f"release={release_date}, current={current_observation_date}, lag={lag_days}d"
        )


def parse_wpsr_table9(
    content: bytes,
    *,
    release_date: str,
    week_ending_date: str,
    source_checksum: str,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    decoded = content.decode("utf-8", errors="replace")
    rows = list(csv.reader(io.StringIO(decoded)))
    if len(rows) < 2 or len(rows[0]) < 4:
        raise ValueError("WPSR table9 CSV is missing expected rows or columns")
    header = rows[0]
    current_date = _parse_archive_date(header[2], date.fromisoformat(release_date).year)
    previous_date = _parse_archive_date(header[3], date.fromisoformat(release_date).year)
    if current_date != week_ending_date:
        raise ValueError(
            f"WPSR page/table week-ending mismatch: page={week_ending_date}, table={current_date}"
        )

    occurrences: defaultdict[tuple[str, str], int] = defaultdict(int)
    group_by_stub: dict[str, str] = {}
    values: list[dict[str, Any]] = []
    for row_number, row in enumerate(rows[1:], start=2):
        if len(row) < 4:
            continue
        stub_1 = " ".join(row[0].split())
        stub_2 = " ".join(row[1].split())
        is_geography_detail = bool(
            re.search(r"\bPADD\s+\d[A-Z]?\b", stub_2, flags=re.IGNORECASE)
            or stub_2 in {"Cushing, Oklahoma", "Alaska In-Transit"}
        )
        if is_geography_detail:
            group_label = group_by_stub.get(stub_1, "")
        else:
            group_label = stub_2
            group_by_stub[stub_1] = stub_2
        key = (stub_1, stub_2)
        occurrences[key] += 1
        occurrence = occurrences[key]
        row_key = f"{stub_1}|{stub_2}|{occurrence}"
        for column_name, observation_date, column_index in (
            ("current", current_date, 2),
            ("previous", previous_date, 3),
        ):
            raw = row[column_index].strip()
            values.append(
                {
                    "schema_version": WPSR_ARCHIVE_SCHEMA_VERSION,
                    "release_date": release_date,
                    "week_ending_date": week_ending_date,
                    "observation_date": observation_date,
                    "observation_column": column_name,
                    "row_number": row_number,
                    "stub_1": stub_1,
                    "stub_2": stub_2,
                    "group_label": group_label,
                    "stub_occurrence": occurrence,
                    "row_key": row_key,
                    "value_raw": raw,
                    "value_numeric": _numeric(raw),
                    "source_table_checksum": source_checksum,
                }
            )
    return {
        "table_row_count": len(rows) - 1,
        "current_observation_date": current_date,
        "previous_observation_date": previous_date,
    }, values


def compare_wpsr_release_values(
    values: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    releases = sorted({str(row["release_date"]) for row in values})
    comparisons: list[dict[str, Any]] = []
    revisions: list[dict[str, Any]] = []
    schema_changes: list[dict[str, Any]] = []
    for older_release, newer_release in zip(releases, releases[1:], strict=False):
        older = {
            str(row["row_key"]): row
            for row in values
            if row["release_date"] == older_release and row["observation_column"] == "current"
        }
        newer = {
            str(row["row_key"]): row
            for row in values
            if row["release_date"] == newer_release and row["observation_column"] == "previous"
        }
        older_dates = {str(row["observation_date"]) for row in older.values()}
        newer_dates = {str(row["observation_date"]) for row in newer.values()}
        overlap_dates = older_dates & newer_dates
        common = sorted(set(older) & set(newer))
        missing_from_newer = sorted(set(older) - set(newer))
        new_in_newer = sorted(set(newer) - set(older))
        exact = 0
        numeric = 0
        revised = 0
        if len(overlap_dates) == 1:
            for key in common:
                left = older[key]
                right = newer[key]
                if left["value_raw"] == right["value_raw"]:
                    exact += 1
                    continue
                left_number = left["value_numeric"]
                right_number = right["value_numeric"]
                if left_number is not None and right_number is not None and left_number == right_number:
                    numeric += 1
                    continue
                revised += 1
                revisions.append(
                    {
                        "schema_version": WPSR_ARCHIVE_SCHEMA_VERSION,
                        "older_release_date": older_release,
                        "newer_release_date": newer_release,
                        "observation_date": next(iter(overlap_dates)),
                        "row_key": key,
                        "stub_1": left["stub_1"],
                        "stub_2": left["stub_2"],
                        "older_value_raw": left["value_raw"],
                        "newer_value_raw": right["value_raw"],
                        "older_value_numeric": left["value_numeric"],
                        "newer_value_numeric": right["value_numeric"],
                    }
                )
            observation_date = next(iter(overlap_dates))
            for change_type, keys, rows in (
                ("missing_from_newer", missing_from_newer, older),
                ("new_in_newer", new_in_newer, newer),
            ):
                for key in keys:
                    row = rows[key]
                    schema_changes.append(
                        {
                            "schema_version": WPSR_ARCHIVE_SCHEMA_VERSION,
                            "older_release_date": older_release,
                            "newer_release_date": newer_release,
                            "observation_date": observation_date,
                            "change_type": change_type,
                            "row_key": key,
                            "stub_1": row["stub_1"],
                            "stub_2": row["stub_2"],
                            "value_raw": row["value_raw"],
                            "value_numeric": row["value_numeric"],
                        }
                    )
        status = "ok" if len(overlap_dates) == 1 else "nonconsecutive_or_schema_mismatch"
        comparisons.append(
            {
                "schema_version": WPSR_ARCHIVE_SCHEMA_VERSION,
                "older_release_date": older_release,
                "newer_release_date": newer_release,
                "overlap_observation_date": next(iter(overlap_dates)) if len(overlap_dates) == 1 else "",
                "older_value_count": len(older),
                "newer_value_count": len(newer),
                "common_key_count": len(common),
                "exact_match_count": exact,
                "numeric_match_count": numeric,
                "revision_count": revised,
                "missing_from_newer_count": len(missing_from_newer),
                "new_in_newer_count": len(new_in_newer),
                "revision_share": revised / len(common) if common else "",
                "status": status,
            }
        )
    return comparisons, revisions, schema_changes


def _fetch_url(url: str, timeout_seconds: float, max_retries: int) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "comm-ls-eia-research/1.0"})
    for attempt in range(max_retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
                return response.read()
        except (urllib.error.URLError, TimeoutError):
            if attempt >= max_retries:
                raise
            time.sleep(min(2**attempt, 8))
    raise RuntimeError("unreachable")


def _archive_urls(release_date: str) -> tuple[str, str]:
    parsed = date.fromisoformat(release_date)
    slug = parsed.strftime("%Y_%m_%d")
    base = f"{WPSR_ARCHIVE_BASE_URL}/{parsed.year}/{slug}"
    return f"{base}/wpsr_{slug}.php", f"{base}/csv/table9.csv"


def _cached_fetch(
    url: str,
    *,
    cache_dir: Path,
    bronze_dir: Path,
    suffix: str,
    refresh_cache: bool,
    fetch: Callable[[str], bytes],
) -> tuple[bytes, str, bool, Path]:
    request_hash = hashlib.sha256(url.encode()).hexdigest()
    pointer = cache_dir / f"wpsr_archive_{request_hash}.json"
    if not refresh_cache and pointer.exists():
        metadata = json.loads(pointer.read_text(encoding="utf-8"))
        response_path = Path(metadata["response_path"])
        if response_path.exists():
            content = response_path.read_bytes()
            return content, _hash_bytes(content), True, response_path

    content = fetch(url)
    checksum = _hash_bytes(content)
    response_path = bronze_dir / f"{checksum}{suffix}"
    if not response_path.exists():
        _atomic_write_bytes(response_path, content)
    _atomic_write_json(
        pointer,
        {
            "schema_version": WPSR_ARCHIVE_SCHEMA_VERSION,
            "url": url,
            "fetched_at": _iso_utc(),
            "response_path": str(response_path),
            "response_checksum": checksum,
            "response_bytes": len(content),
        },
    )
    return content, checksum, False, response_path


def run_wpsr_archive_pilot(
    *,
    release_dates: tuple[str, ...] = DEFAULT_WPSR_PILOT_RELEASE_DATES,
    output_dir: Path = Path("data/external/eia/archive_pilot"),
    bronze_dir: Path = Path("data/external/eia/bronze/wpsr_archive"),
    cache_dir: Path = Path("data/external/eia/request_cache"),
    manifest_dir: Path = Path("data/external/eia/manifests"),
    timeout_seconds: float = 30.0,
    max_retries: int = 3,
    request_delay_seconds: float = 0.0,
    refresh_cache: bool = False,
    fetcher: Callable[[str], bytes] | None = None,
) -> dict[str, Any]:
    normalized_dates = tuple(sorted({date.fromisoformat(value).isoformat() for value in release_dates}))
    if not 2 <= len(normalized_dates) <= 5:
        raise ValueError("WPSR archive pilot requires 2 to 5 distinct explicit release dates")
    if request_delay_seconds < 0:
        raise ValueError("request_delay_seconds must be non-negative")
    fetched_at = _iso_utc()
    network_requests = 0

    def fetch(url: str) -> bytes:
        nonlocal network_requests
        if request_delay_seconds:
            time.sleep(request_delay_seconds)
        network_requests += 1
        if fetcher is not None:
            return fetcher(url)
        return _fetch_url(url, timeout_seconds, max_retries)

    release_rows: list[dict[str, Any]] = []
    all_values: list[dict[str, Any]] = []
    for release_date in normalized_dates:
        page_url, table_url = _archive_urls(release_date)
        release_bronze = Path(bronze_dir) / release_date
        try:
            page, page_checksum, page_cached, _ = _cached_fetch(
                page_url,
                cache_dir=Path(cache_dir),
                bronze_dir=release_bronze,
                suffix=".html",
                refresh_cache=refresh_cache,
                fetch=fetch,
            )
            table, table_checksum, table_cached, _ = _cached_fetch(
                table_url,
                cache_dir=Path(cache_dir),
                bronze_dir=release_bronze,
                suffix=".csv",
                refresh_cache=refresh_cache,
                fetch=fetch,
            )
            current_observation, previous_observation = _table_header_dates(
                table, release_date
            )
            _validate_table_timing(
                release_date, current_observation, previous_observation
            )
            metadata_quality = "page_and_table_timing_verified"
            metadata_warning = ""
            try:
                parsed_release, page_week_ending = parse_wpsr_archive_page(page)
            except ValueError as exc:
                parsed_release = ""
                page_week_ending = ""
                metadata_quality = "page_metadata_missing_table_timing_verified"
                metadata_warning = str(exc)
            else:
                if (
                    parsed_release != release_date
                    or page_week_ending != current_observation
                ):
                    metadata_quality = "page_metadata_anomaly_table_timing_verified"
                    metadata_warning = (
                        f"page_release={parsed_release}, requested_release={release_date}, "
                        f"page_week_ending={page_week_ending}, "
                        f"table_week_ending={current_observation}"
                    )
            table_summary, values = parse_wpsr_table9(
                table,
                release_date=release_date,
                week_ending_date=current_observation,
                source_checksum=table_checksum,
            )
            all_values.extend(values)
            release_rows.append(
                {
                    "schema_version": WPSR_ARCHIVE_SCHEMA_VERSION,
                    "fetched_at": fetched_at,
                    "requested_release_date": release_date,
                    "parsed_release_date": parsed_release,
                    "week_ending_date": current_observation,
                    "page_url": page_url,
                    "table_url": table_url,
                    "page_checksum": page_checksum,
                    "table_checksum": table_checksum,
                    "page_from_cache": page_cached,
                    "table_from_cache": table_cached,
                    **table_summary,
                    "metadata_quality": metadata_quality,
                    "metadata_warning": metadata_warning,
                    "status": "ok",
                    "error": "",
                }
            )
        except Exception as exc:
            release_rows.append(
                {
                    "schema_version": WPSR_ARCHIVE_SCHEMA_VERSION,
                    "fetched_at": fetched_at,
                    "requested_release_date": release_date,
                    "parsed_release_date": "",
                    "week_ending_date": "",
                    "page_url": page_url,
                    "table_url": table_url,
                    "page_checksum": "",
                    "table_checksum": "",
                    "page_from_cache": False,
                    "table_from_cache": False,
                    "table_row_count": 0,
                    "current_observation_date": "",
                    "previous_observation_date": "",
                    "metadata_quality": "failed_validation",
                    "metadata_warning": "",
                    "status": "error",
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )

    comparisons, revisions, schema_changes = compare_wpsr_release_values(all_values)
    output_dir = Path(output_dir)
    releases_path = output_dir / "wpsr_archive_pilot_releases.csv"
    values_path = output_dir / "wpsr_archive_pilot_values.csv"
    comparisons_path = output_dir / "wpsr_archive_pilot_comparisons.csv"
    revisions_path = output_dir / "wpsr_archive_pilot_revisions.csv"
    schema_changes_path = output_dir / "wpsr_archive_pilot_schema_changes.csv"
    _atomic_write_csv(releases_path, release_rows, RELEASE_COLUMNS)
    _atomic_write_csv(values_path, all_values, VALUE_COLUMNS)
    _atomic_write_csv(comparisons_path, comparisons, COMPARISON_COLUMNS)
    _atomic_write_csv(revisions_path, revisions, REVISION_COLUMNS)
    _atomic_write_csv(schema_changes_path, schema_changes, SCHEMA_CHANGE_COLUMNS)

    error_count = sum(row["status"] != "ok" for row in release_rows)
    comparison_error_count = sum(row["status"] != "ok" for row in comparisons)
    result = {
        "schema_version": WPSR_ARCHIVE_SCHEMA_VERSION,
        "run_id": datetime.fromisoformat(fetched_at.replace("Z", "+00:00")).strftime(
            "%Y%m%dT%H%M%S%fZ"
        ),
        "fetched_at": fetched_at,
        "requested_release_dates": list(normalized_dates),
        "release_count": len(release_rows),
        "successful_release_count": len(release_rows) - error_count,
        "release_error_count": error_count,
        "comparison_count": len(comparisons),
        "comparison_error_count": comparison_error_count,
        "revision_count": len(revisions),
        "schema_change_count": len(schema_changes),
        "value_row_count": len(all_values),
        "network_requests": network_requests,
        "observation_backfill_authorized": False,
        "outputs": {
            str(path): _file_checksum(path)
            for path in (
                releases_path,
                values_path,
                comparisons_path,
                revisions_path,
                schema_changes_path,
            )
        },
    }
    manifest_path = Path(manifest_dir) / f"wpsr_archive_pilot_{result['run_id']}_summary.json"
    result["manifest_path"] = str(manifest_path)
    _atomic_write_json(manifest_path, result)
    return result
