from __future__ import annotations

import csv
import gzip
import hashlib
import json
import re
import urllib.error
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Callable


WPSR_ARCHIVE_INDEX_URL = "https://www.eia.gov/petroleum/supply/weekly/archive/"
WPSR_RELEASE_INDEX_SCHEMA_VERSION = "1"

RELEASE_DATE_COLUMNS = [
    "schema_version",
    "release_date",
    "status",
    "source",
    "archive_page_url",
    "official_release_time",
    "release_time_status",
    "index_checksum",
    "discovered_at",
    "notes",
]


def _iso_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


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


def parse_wpsr_release_index(content: bytes) -> list[dict[str, str]]:
    text = content.decode("utf-8", errors="replace")
    pattern = re.compile(
        r'href=["\'](?P<path>/petroleum/supply/weekly/archive/'
        r'(?P<year>\d{4})/(?P<stamp>\d{4}_\d{2}_\d{2})/'
        r'wpsr_(?P=stamp)\.php)["\']',
        re.IGNORECASE,
    )
    rows: dict[str, dict[str, str]] = {}
    for match in pattern.finditer(text):
        release_date = match.group("stamp").replace("_", "-")
        parsed = date.fromisoformat(release_date)
        if parsed.year != int(match.group("year")):
            raise ValueError(f"WPSR archive year/path mismatch: {match.group('path')}")
        rows[release_date] = {
            "release_date": release_date,
            "archive_page_url": f"https://www.eia.gov{match.group('path')}",
        }
    if not rows:
        raise ValueError("No WPSR release links found in the official archive index")
    return [rows[key] for key in sorted(rows)]


def _fetch(url: str, timeout_seconds: float, max_retries: int) -> bytes:
    request = urllib.request.Request(
        url,
        headers={"Accept": "text/html", "User-Agent": "comm-ls-eia-research/1"},
    )
    for attempt in range(max_retries + 1):
        try:
            with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
                return response.read()
        except (urllib.error.URLError, TimeoutError):
            if attempt >= max_retries:
                raise
    raise RuntimeError("unreachable")


def discover_wpsr_release_dates(
    *,
    output_path: Path = Path("config/eia_wpsr_release_dates.csv"),
    archive_index_url: str = WPSR_ARCHIVE_INDEX_URL,
    bronze_dir: Path = Path("data/external/eia/bronze/wpsr_release_index"),
    cache_dir: Path = Path("data/external/eia/request_cache"),
    start: str | None = None,
    end: str | None = None,
    timeout_seconds: float = 30.0,
    max_retries: int = 3,
    refresh_cache: bool = False,
    fetcher: Callable[[str], bytes] | None = None,
) -> dict[str, Any]:
    request_hash = hashlib.sha256(archive_index_url.encode()).hexdigest()
    cache_path = Path(cache_dir) / f"eia_wpsr_release_index_{request_hash}.json"
    from_cache = False
    if cache_path.exists() and not refresh_cache:
        pointer = json.loads(cache_path.read_text(encoding="utf-8"))
        response_path = Path(pointer["response_path"])
        with gzip.open(response_path, "rb") as handle:
            content = handle.read()
        from_cache = True
    else:
        content = fetcher(archive_index_url) if fetcher else _fetch(
            archive_index_url, timeout_seconds, max_retries
        )
        checksum = hashlib.sha256(content).hexdigest()
        response_path = Path(bronze_dir) / f"{checksum}.html.gz"
        response_path.parent.mkdir(parents=True, exist_ok=True)
        if not response_path.exists():
            temporary = response_path.with_suffix(response_path.suffix + ".tmp")
            with gzip.open(temporary, "wb") as handle:
                handle.write(content)
            temporary.replace(response_path)
        _atomic_write_json(
            cache_path,
            {
                "request_url": archive_index_url,
                "response_path": str(response_path),
                "response_checksum": checksum,
                "response_bytes": len(content),
                "cached_at": _iso_utc(),
            },
        )
    checksum = hashlib.sha256(content).hexdigest()
    discovered = parse_wpsr_release_index(content)
    start_date = date.fromisoformat(start) if start else None
    end_date = date.fromisoformat(end) if end else None
    discovered = [
        row
        for row in discovered
        if (start_date is None or date.fromisoformat(row["release_date"]) >= start_date)
        and (end_date is None or date.fromisoformat(row["release_date"]) <= end_date)
    ]
    if not discovered:
        raise ValueError("No WPSR releases remain after the requested date filter")

    existing = {row.get("release_date", ""): row for row in _read_csv(Path(output_path))}
    discovered_at = _iso_utc()
    output: list[dict[str, Any]] = []
    for row in discovered:
        prior = existing.get(row["release_date"], {})
        output.append(
            {
                "schema_version": WPSR_RELEASE_INDEX_SCHEMA_VERSION,
                "release_date": row["release_date"],
                "status": prior.get("status") or "official_archive_index",
                "source": "EIA WPSR official archive index",
                "archive_page_url": row["archive_page_url"],
                "official_release_time": prior.get("official_release_time", ""),
                "release_time_status": prior.get("release_time_status")
                or (
                    "standard_wednesday_1030_eastern"
                    if date.fromisoformat(row["release_date"]).weekday() == 2
                    else "holiday_exact_time_unresolved"
                ),
                "index_checksum": checksum,
                "discovered_at": discovered_at,
                "notes": prior.get("notes", ""),
            }
        )
    _atomic_write_csv(Path(output_path), output, RELEASE_DATE_COLUMNS)
    return {
        "release_count": len(output),
        "start_release_date": output[0]["release_date"],
        "end_release_date": output[-1]["release_date"],
        "from_cache": from_cache,
        "index_checksum": checksum,
        "output_path": str(output_path),
    }
