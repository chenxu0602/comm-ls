from __future__ import annotations

import csv
import gzip
import hashlib
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


EIA_CATALOG_SCHEMA_VERSION = "1"
EIA_CATALOG_SCORE_VERSION = "1"
DEFAULT_EIA_API_BASE_URL = "https://api.eia.gov/v2"
DEFAULT_EIA_CATALOG_ROOTS = ("petroleum", "crude-oil-imports")

ROUTE_COLUMNS = [
    "schema_version",
    "cataloged_at",
    "api_version",
    "route_id",
    "source_response_id",
    "route",
    "canonical_dataset_key",
    "parent_route",
    "depth",
    "name",
    "description",
    "is_leaf",
    "child_route_count",
    "frequency_ids",
    "start_period",
    "end_period",
    "default_frequency",
    "default_date_format",
    "measure_count",
    "facet_count",
    "source_update_ts",
]

MEASURE_COLUMNS = [
    "schema_version",
    "cataloged_at",
    "route",
    "canonical_dataset_key",
    "measure_id",
    "unit",
    "description",
    "measure_metadata_json",
]

FACET_COLUMNS = [
    "schema_version",
    "cataloged_at",
    "route",
    "canonical_dataset_key",
    "facet_id",
    "description",
    "estimated_cardinality",
    "cardinality_status",
]

ROUTE_SCORE_COLUMNS = [
    "score_version",
    "cataloged_at",
    "route",
    "canonical_dataset_key",
    "domain",
    "release_product_guess",
    "is_leaf",
    "frequency_ids",
    "strategy_tags",
    "priority_score",
    "point_in_time_status",
    "shortlist_status",
    "score_reason",
]

REQUEST_COLUMNS = [
    "request_id",
    "requested_at",
    "completed_at",
    "route",
    "request_url_redacted",
    "request_hash",
    "from_cache",
    "attempt_count",
    "http_status",
    "response_path",
    "response_checksum",
    "response_bytes",
    "api_version",
    "error_type",
    "error_message",
]

FACET_VALUE_COLUMNS = [
    "schema_version",
    "route",
    "canonical_dataset_key",
    "release_product",
    "priority",
    "facet_id",
    "facet_value_id",
    "facet_value_name",
    "first_seen_at",
    "last_seen_at",
    "is_current",
    "source_response_checksum",
]

FACET_VALUE_SUMMARY_COLUMNS = [
    "schema_version",
    "fetched_at",
    "route",
    "canonical_dataset_key",
    "release_product",
    "priority",
    "facet_id",
    "exact_cardinality",
    "response_total_facets",
    "count_matches_response_total",
    "fetch_status",
    "source_response_checksum",
]


class EiaCatalogError(RuntimeError):
    pass


class EiaFetchError(EiaCatalogError):
    def __init__(self, message: str, request_record: dict[str, Any]) -> None:
        super().__init__(message)
        self.request_record = request_record


class EiaCrawlError(EiaCatalogError):
    def __init__(self, message: str, request_records: list[dict[str, Any]]) -> None:
        super().__init__(message)
        self.request_records = request_records


@dataclass(frozen=True)
class EiaFetchResult:
    payload: dict[str, Any]
    request_record: dict[str, Any]


@dataclass(frozen=True)
class EiaCatalogBuild:
    routes: list[dict[str, Any]]
    measures: list[dict[str, Any]]
    facets: list[dict[str, Any]]
    route_scores: list[dict[str, Any]]
    requests: list[dict[str, Any]]
    roots: tuple[str, ...]
    truncated: bool
    cataloged_at: str


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _iso_utc(value: datetime | None = None) -> str:
    return (value or _utc_now()).isoformat().replace("+00:00", "Z")


def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).split())


def _normalize_route(route: str) -> str:
    value = str(route).strip()
    if value.startswith("http://") or value.startswith("https://"):
        value = urllib.parse.urlparse(value).path
    value = value.strip("/")
    if value.startswith("v2/"):
        value = value[3:]
    return f"{value}/" if value else ""


def _route_id(route: str) -> str:
    parts = [part for part in _normalize_route(route).split("/") if part]
    return parts[-1] if parts else ""


def _route_url(base_url: str, route: str) -> str:
    return f"{base_url.rstrip('/')}/{_normalize_route(route)}"


def _hash_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _hash_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _atomic_write_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(content)
    temporary.replace(path)


def _atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    content = json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True).encode("utf-8") + b"\n"
    _atomic_write_bytes(path, content)


def _read_gzip_json(path: Path) -> dict[str, Any]:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise EiaCatalogError(f"Cached EIA response is not a JSON object: {path}")
    return payload


def _write_gzip_json(path: Path, payload: dict[str, Any]) -> None:
    content = json.dumps(payload, sort_keys=True, ensure_ascii=True).encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with gzip.open(temporary, "wb") as handle:
        handle.write(content)
    temporary.replace(path)


class EiaApiClient:
    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = DEFAULT_EIA_API_BASE_URL,
        bronze_dir: Path = Path("data/external/eia/bronze/catalog"),
        cache_dir: Path = Path("data/external/eia/request_cache"),
        timeout_seconds: float = 30.0,
        max_retries: int = 4,
        request_delay_seconds: float = 0.25,
        refresh_cache: bool = False,
    ) -> None:
        if not api_key:
            raise ValueError("EIA API key must not be empty")
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        if max_retries < 0:
            raise ValueError("max_retries must be non-negative")
        if request_delay_seconds < 0:
            raise ValueError("request_delay_seconds must be non-negative")
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.bronze_dir = Path(bronze_dir)
        self.cache_dir = Path(cache_dir)
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries
        self.request_delay_seconds = request_delay_seconds
        self.refresh_cache = refresh_cache

    def _request_identity(self, route: str) -> tuple[str, str]:
        redacted_url = _route_url(self.base_url, route)
        return redacted_url, _hash_text(redacted_url)

    def _cache_pointer_path(self, request_hash: str) -> Path:
        return self.cache_dir / f"{request_hash}.json"

    def _load_cached(self, request_hash: str) -> tuple[dict[str, Any], Path, str, int] | None:
        pointer_path = self._cache_pointer_path(request_hash)
        if self.refresh_cache or not pointer_path.exists():
            return None
        try:
            pointer = json.loads(pointer_path.read_text(encoding="utf-8"))
            response_path = Path(pointer["response_path"])
            payload = _read_gzip_json(response_path)
            checksum = str(pointer["response_checksum"])
            response_bytes = int(pointer["response_bytes"])
        except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError, EiaCatalogError):
            return None
        return payload, response_path, checksum, response_bytes

    def fetch_route(self, route: str) -> EiaFetchResult:
        normalized_route = _normalize_route(route)
        redacted_url, request_hash = self._request_identity(normalized_route)
        request_id = f"eia-{request_hash[:16]}-{_utc_now().strftime('%Y%m%dT%H%M%S%fZ')}"
        requested_at = _iso_utc()

        cached = self._load_cached(request_hash)
        if cached is not None:
            payload, response_path, checksum, response_bytes = cached
            api_version = _clean_text(payload.get("apiVersion"))
            return EiaFetchResult(
                payload=payload,
                request_record={
                    "request_id": request_id,
                    "requested_at": requested_at,
                    "completed_at": _iso_utc(),
                    "route": normalized_route,
                    "request_url_redacted": redacted_url,
                    "request_hash": request_hash,
                    "from_cache": True,
                    "attempt_count": 0,
                    "http_status": 200,
                    "response_path": str(response_path),
                    "response_checksum": checksum,
                    "response_bytes": response_bytes,
                    "api_version": api_version,
                    "error_type": "",
                    "error_message": "",
                },
            )

        query_url = f"{redacted_url}?{urllib.parse.urlencode({'api_key': self.api_key})}"
        last_error: Exception | None = None
        last_status = 0
        attempt_count = 0
        for attempt in range(1, self.max_retries + 2):
            attempt_count = attempt
            if self.request_delay_seconds:
                time.sleep(self.request_delay_seconds)
            request = urllib.request.Request(
                query_url,
                headers={"Accept": "application/json", "User-Agent": "comm-ls-eia-catalog/1"},
            )
            try:
                with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                    last_status = int(response.status)
                    raw = response.read()
                payload = json.loads(raw.decode("utf-8"))
                if not isinstance(payload, dict) or "response" not in payload:
                    raise EiaCatalogError(f"EIA response has no response object for route {normalized_route}")
                if payload.get("error"):
                    raise EiaCatalogError(f"EIA API error for route {normalized_route}: {payload['error']}")

                response_checksum = _hash_bytes(raw)
                ingestion_date = _utc_now().strftime("%Y-%m-%d")
                response_path = (
                    self.bronze_dir
                    / f"ingestion_date={ingestion_date}"
                    / f"{request_hash}-{response_checksum}.json.gz"
                )
                if not response_path.exists():
                    _write_gzip_json(response_path, payload)
                pointer = {
                    "request_hash": request_hash,
                    "request_url_redacted": redacted_url,
                    "response_path": str(response_path),
                    "response_checksum": response_checksum,
                    "response_bytes": len(raw),
                    "cached_at": _iso_utc(),
                }
                _atomic_write_json(self._cache_pointer_path(request_hash), pointer)
                return EiaFetchResult(
                    payload=payload,
                    request_record={
                        "request_id": request_id,
                        "requested_at": requested_at,
                        "completed_at": _iso_utc(),
                        "route": normalized_route,
                        "request_url_redacted": redacted_url,
                        "request_hash": request_hash,
                        "from_cache": False,
                        "attempt_count": attempt_count,
                        "http_status": last_status,
                        "response_path": str(response_path),
                        "response_checksum": response_checksum,
                        "response_bytes": len(raw),
                        "api_version": _clean_text(payload.get("apiVersion")),
                        "error_type": "",
                        "error_message": "",
                    },
                )
            except urllib.error.HTTPError as exc:
                last_status = int(exc.code)
                last_error = exc
                retryable = exc.code == 429 or 500 <= exc.code < 600
                if not retryable or attempt > self.max_retries:
                    break
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, EiaCatalogError) as exc:
                last_error = exc
                if attempt > self.max_retries:
                    break
            time.sleep(min(2 ** (attempt - 1), 30))

        error_type = type(last_error).__name__ if last_error is not None else "UnknownError"
        error_message = _clean_text(last_error)
        record = {
            "request_id": request_id,
            "requested_at": requested_at,
            "completed_at": _iso_utc(),
            "route": normalized_route,
            "request_url_redacted": redacted_url,
            "request_hash": request_hash,
            "from_cache": False,
            "attempt_count": attempt_count,
            "http_status": last_status,
            "response_path": "",
            "response_checksum": "",
            "response_bytes": 0,
            "api_version": "",
            "error_type": error_type,
            "error_message": error_message,
        }
        raise EiaFetchError(f"Failed to fetch EIA route {normalized_route}: {error_message}", record)


def _frequency_ids(response: dict[str, Any]) -> list[str]:
    frequencies = response.get("frequency") or []
    return [str(item.get("id", "")).strip() for item in frequencies if str(item.get("id", "")).strip()]


def _measure_rows(
    response: dict[str, Any], route: str, cataloged_at: str
) -> list[dict[str, Any]]:
    data = response.get("data") or {}
    if not isinstance(data, dict):
        return []
    rows: list[dict[str, Any]] = []
    for measure_id, metadata in sorted(data.items(), key=lambda item: str(item[0])):
        metadata_dict = metadata if isinstance(metadata, dict) else {}
        rows.append(
            {
                "schema_version": EIA_CATALOG_SCHEMA_VERSION,
                "cataloged_at": cataloged_at,
                "route": route,
                "canonical_dataset_key": route.rstrip("/"),
                "measure_id": str(measure_id),
                "unit": _clean_text(metadata_dict.get("units")),
                "description": _clean_text(metadata_dict.get("description")),
                "measure_metadata_json": json.dumps(metadata_dict, sort_keys=True, separators=(",", ":")),
            }
        )
    return rows


def _facet_rows(
    response: dict[str, Any], route: str, cataloged_at: str
) -> list[dict[str, Any]]:
    facets = response.get("facets") or []
    rows: list[dict[str, Any]] = []
    for facet in facets:
        facet_id = str(facet.get("id", "")).strip()
        if not facet_id:
            continue
        rows.append(
            {
                "schema_version": EIA_CATALOG_SCHEMA_VERSION,
                "cataloged_at": cataloged_at,
                "route": route,
                "canonical_dataset_key": route.rstrip("/"),
                "facet_id": facet_id,
                "description": _clean_text(facet.get("description")),
                "estimated_cardinality": "",
                "cardinality_status": "not_requested",
            }
        )
    return rows


def _guess_domain(route: str) -> str:
    root = route.rstrip("/").split("/", maxsplit=1)[0]
    if root == "crude-oil-imports":
        return "petroleum"
    return root.replace("-", "_")


def _score_route(row: dict[str, Any]) -> dict[str, Any]:
    route = str(row["route"])
    text = " ".join([route, str(row.get("name", "")), str(row.get("description", ""))]).lower()
    frequencies = json.loads(str(row.get("frequency_ids") or "[]"))
    tags: list[str] = []
    reasons: list[str] = []
    score = 0.0

    keyword_groups = {
        "refiner": ["refiner", "refining", "refinery", "utilization", "cracking", "coking", "hydrocrack"],
        "fuel": ["gasoline", "distillate", "jet fuel", "product supplied", "consumption", "sales"],
        "flow": ["import", "export", "movement", "origin", "destination", "grade"],
        "inventory": ["stock", "inventory", "cushing"],
    }
    for tag, keywords in keyword_groups.items():
        if any(keyword in text for keyword in keywords):
            tags.append(tag)
            score += 1.5
            reasons.append(tag)

    if bool(row.get("is_leaf")):
        score += 2.0
        reasons.append("leaf")
    if "weekly" in frequencies:
        score += 1.0
        reasons.append("weekly")
    if "monthly" in frequencies:
        score += 1.0
        reasons.append("monthly")

    root = route.rstrip("/").split("/", maxsplit=1)[0]
    if root == "crude-oil-imports":
        release_product_guess = "company_crude_imports"
        score += 3.0
        reasons.append("phase1_company_imports")
    elif root == "petroleum" and "weekly" in frequencies:
        release_product_guess = "WPSR_candidate"
        score += 2.0
        reasons.append("phase1_weekly_petroleum")
    elif root == "petroleum" and "monthly" in frequencies:
        release_product_guess = "PSM_candidate"
        score += 2.0
        reasons.append("phase1_monthly_petroleum")
    else:
        release_product_guess = "unclassified"

    return {
        "score_version": EIA_CATALOG_SCORE_VERSION,
        "cataloged_at": row["cataloged_at"],
        "route": route,
        "canonical_dataset_key": row["canonical_dataset_key"],
        "domain": _guess_domain(route),
        "release_product_guess": release_product_guess,
        "is_leaf": row["is_leaf"],
        "frequency_ids": row["frequency_ids"],
        "strategy_tags": "|".join(sorted(set(tags))),
        "priority_score": score,
        "point_in_time_status": "unreviewed",
        "shortlist_status": "review",
        "score_reason": "|".join(reasons),
    }


def crawl_eia_catalog(
    roots: list[str] | tuple[str, ...],
    fetch_route: Callable[[str], EiaFetchResult],
    *,
    max_routes: int | None = None,
    max_depth: int | None = None,
) -> EiaCatalogBuild:
    normalized_roots = tuple(dict.fromkeys(_normalize_route(root) for root in roots))
    if not normalized_roots:
        raise ValueError("At least one EIA catalog root is required")
    if max_routes is not None and max_routes <= 0:
        raise ValueError("max_routes must be positive")
    if max_depth is not None and max_depth < 0:
        raise ValueError("max_depth must be non-negative")

    cataloged_at = _iso_utc()
    queue: deque[tuple[str, str, int, str, str]] = deque(
        (root, "", 0, _route_id(root), "") for root in normalized_roots
    )
    visited: set[str] = set()
    routes: list[dict[str, Any]] = []
    measures: list[dict[str, Any]] = []
    facets: list[dict[str, Any]] = []
    requests: list[dict[str, Any]] = []
    truncated = False

    while queue:
        if max_routes is not None and len(routes) >= max_routes:
            truncated = True
            break
        route, parent_route, depth, hint_name, hint_description = queue.popleft()
        if route in visited:
            continue
        visited.add(route)
        try:
            fetched = fetch_route(route)
        except EiaFetchError as exc:
            requests.append(exc.request_record)
            raise EiaCrawlError(str(exc), requests.copy()) from exc
        requests.append(fetched.request_record)
        payload = fetched.payload
        response = payload.get("response") or {}
        if not isinstance(response, dict):
            raise EiaCatalogError(f"EIA response is not an object for route {route}")

        children = response.get("routes") or []
        frequencies = _frequency_ids(response)
        route_measures = _measure_rows(response, route, cataloged_at)
        route_facets = _facet_rows(response, route, cataloged_at)
        is_leaf = len(children) == 0
        routes.append(
            {
                "schema_version": EIA_CATALOG_SCHEMA_VERSION,
                "cataloged_at": cataloged_at,
                "api_version": _clean_text(payload.get("apiVersion")),
                "route_id": _route_id(route),
                "source_response_id": _clean_text(response.get("id")),
                "route": route,
                "canonical_dataset_key": route.rstrip("/"),
                "parent_route": parent_route,
                "depth": depth,
                "name": _clean_text(response.get("name")) or _clean_text(hint_name),
                "description": _clean_text(response.get("description")) or _clean_text(hint_description),
                "is_leaf": is_leaf,
                "child_route_count": len(children),
                "frequency_ids": json.dumps(frequencies, separators=(",", ":")),
                "start_period": _clean_text(response.get("startPeriod")),
                "end_period": _clean_text(response.get("endPeriod")),
                "default_frequency": _clean_text(response.get("defaultFrequency")),
                "default_date_format": _clean_text(response.get("defaultDateFormat")),
                "measure_count": len(route_measures),
                "facet_count": len(route_facets),
                "source_update_ts": "",
            }
        )
        measures.extend(route_measures)
        facets.extend(route_facets)

        if max_depth is not None and depth >= max_depth:
            if children:
                truncated = True
            continue
        for child in children:
            child_id = str(child.get("id", "")).strip()
            if not child_id:
                continue
            child_route = f"{route}{child_id}/"
            queue.append(
                (
                    child_route,
                    route,
                    depth + 1,
                    _clean_text(child.get("name")) or child_id,
                    _clean_text(child.get("description")),
                )
            )

    routes.sort(key=lambda row: str(row["route"]))
    measures.sort(key=lambda row: (str(row["route"]), str(row["measure_id"])))
    facets.sort(key=lambda row: (str(row["route"]), str(row["facet_id"])))
    route_scores = sorted(
        (_score_route(row) for row in routes),
        key=lambda row: (-float(row["priority_score"]), str(row["route"])),
    )
    return EiaCatalogBuild(
        routes=routes,
        measures=measures,
        facets=facets,
        route_scores=route_scores,
        requests=requests,
        roots=normalized_roots,
        truncated=truncated,
        cataloged_at=cataloged_at,
    )


def _write_csv(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns, extrasaction="raise")
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def _file_checksum(path: Path) -> str:
    return _hash_bytes(path.read_bytes())


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_eia_catalog_build(
    build: EiaCatalogBuild,
    *,
    output_dir: Path,
    manifest_dir: Path,
) -> dict[str, Any]:
    output_dir = Path(output_dir)
    manifest_dir = Path(manifest_dir)
    routes_path = output_dir / "routes.csv"
    measures_path = output_dir / "measures.csv"
    facets_path = output_dir / "facets.csv"
    scores_path = output_dir / "route_scores.csv"
    _write_csv(routes_path, build.routes, ROUTE_COLUMNS)
    _write_csv(measures_path, build.measures, MEASURE_COLUMNS)
    _write_csv(facets_path, build.facets, FACET_COLUMNS)
    _write_csv(scores_path, build.route_scores, ROUTE_SCORE_COLUMNS)

    run_id = datetime.fromisoformat(build.cataloged_at.replace("Z", "+00:00")).strftime("%Y%m%dT%H%M%S%fZ")
    requests_path = manifest_dir / f"catalog_{run_id}_requests.csv"
    summary_path = manifest_dir / f"catalog_{run_id}_summary.json"
    _write_csv(requests_path, build.requests, REQUEST_COLUMNS)
    summary = {
        "schema_version": EIA_CATALOG_SCHEMA_VERSION,
        "run_id": run_id,
        "cataloged_at": build.cataloged_at,
        "roots": list(build.roots),
        "truncated": build.truncated,
        "route_count": len(build.routes),
        "leaf_count": sum(bool(row["is_leaf"]) for row in build.routes),
        "measure_count": len(build.measures),
        "facet_count": len(build.facets),
        "request_count": len(build.requests),
        "cache_hit_count": sum(bool(row["from_cache"]) for row in build.requests),
        "outputs": {
            str(routes_path): {"rows": len(build.routes), "sha256": _file_checksum(routes_path)},
            str(measures_path): {"rows": len(build.measures), "sha256": _file_checksum(measures_path)},
            str(facets_path): {"rows": len(build.facets), "sha256": _file_checksum(facets_path)},
            str(scores_path): {"rows": len(build.route_scores), "sha256": _file_checksum(scores_path)},
            str(requests_path): {"rows": len(build.requests), "sha256": _file_checksum(requests_path)},
        },
    }
    _atomic_write_json(summary_path, summary)
    return summary


def _write_failed_crawl_manifest(
    *,
    manifest_dir: Path,
    roots: list[str] | tuple[str, ...],
    request_records: list[dict[str, Any]],
    error: Exception,
) -> None:
    failed_at = _iso_utc()
    run_id = datetime.fromisoformat(failed_at.replace("Z", "+00:00")).strftime("%Y%m%dT%H%M%S%fZ")
    requests_path = Path(manifest_dir) / f"catalog_{run_id}_failed_requests.csv"
    summary_path = Path(manifest_dir) / f"catalog_{run_id}_failed_summary.json"
    _write_csv(requests_path, request_records, REQUEST_COLUMNS)
    summary = {
        "schema_version": EIA_CATALOG_SCHEMA_VERSION,
        "run_id": run_id,
        "status": "failed",
        "failed_at": failed_at,
        "roots": [_normalize_route(root) for root in roots],
        "request_count": len(request_records),
        "cache_hit_count": sum(bool(row["from_cache"]) for row in request_records),
        "error_type": type(error).__name__,
        "error_message": _clean_text(error),
        "requests_path": str(requests_path),
        "requests_sha256": _file_checksum(requests_path),
    }
    _atomic_write_json(summary_path, summary)


def _shortlist_rows(
    shortlist_path: Path,
    *,
    allowed_statuses: tuple[str, ...],
    max_priority: int | None,
    release_products: tuple[str, ...] | None,
    selected_routes: tuple[str, ...] | None,
) -> list[dict[str, str]]:
    rows = _read_csv(Path(shortlist_path))
    if not rows:
        raise EiaCatalogError(f"EIA route shortlist is empty or missing: {shortlist_path}")
    allowed = set(allowed_statuses)
    release_filter = {value.upper() for value in release_products} if release_products else None
    route_filter = {_normalize_route(value) for value in selected_routes} if selected_routes else None
    selected: list[dict[str, str]] = []
    for row in rows:
        route = _normalize_route(row.get("route", ""))
        if not route or row.get("status", "") not in allowed:
            continue
        priority = int(row.get("priority", "999") or 999)
        release_product = row.get("release_product", "").upper()
        if max_priority is not None and priority > max_priority:
            continue
        if release_filter is not None and release_product not in release_filter:
            continue
        if route_filter is not None and route not in route_filter:
            continue
        normalized = dict(row)
        normalized["route"] = route
        normalized["priority"] = str(priority)
        normalized["release_product"] = release_product
        selected.append(normalized)
    if not selected:
        raise EiaCatalogError("No EIA shortlist routes matched the requested filters")
    selected.sort(key=lambda row: (int(row["priority"]), row["release_product"], row["route"]))
    return selected


def _facet_definitions_by_route(facets_path: Path) -> dict[str, list[dict[str, str]]]:
    rows = _read_csv(Path(facets_path))
    if not rows:
        raise EiaCatalogError(f"EIA facet catalog is empty or missing: {facets_path}")
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        route = _normalize_route(row.get("route", ""))
        facet_id = row.get("facet_id", "").strip()
        if not route or not facet_id:
            continue
        grouped.setdefault(route, []).append(row)
    for route_rows in grouped.values():
        route_rows.sort(key=lambda row: row["facet_id"])
    return grouped


def _merge_facet_values(
    existing_rows: list[dict[str, str]],
    fetched_rows: list[dict[str, Any]],
    fetched_groups: set[tuple[str, str]],
) -> list[dict[str, Any]]:
    key_columns = ("route", "facet_id", "facet_value_id")
    merged: dict[tuple[str, str, str], dict[str, Any]] = {}
    for row in existing_rows:
        key = tuple(str(row.get(column, "")) for column in key_columns)
        if not all(key):
            continue
        normalized: dict[str, Any] = {column: row.get(column, "") for column in FACET_VALUE_COLUMNS}
        if (key[0], key[1]) in fetched_groups:
            normalized["is_current"] = False
        merged[key] = normalized

    for row in fetched_rows:
        key = tuple(str(row[column]) for column in key_columns)
        previous = merged.get(key)
        if previous is not None and previous.get("first_seen_at"):
            row["first_seen_at"] = previous["first_seen_at"]
        merged[key] = row
    return sorted(
        merged.values(),
        key=lambda row: (str(row["route"]), str(row["facet_id"]), str(row["facet_value_id"])),
    )


def _merge_facet_summaries(
    existing_rows: list[dict[str, str]],
    fetched_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    merged: dict[tuple[str, str], dict[str, Any]] = {}
    for row in existing_rows:
        key = (row.get("route", ""), row.get("facet_id", ""))
        if all(key):
            merged[key] = {column: row.get(column, "") for column in FACET_VALUE_SUMMARY_COLUMNS}
    for row in fetched_rows:
        merged[(str(row["route"]), str(row["facet_id"]))] = row
    return sorted(merged.values(), key=lambda row: (str(row["route"]), str(row["facet_id"])))


def fetch_eia_shortlist_facets_from_api(
    *,
    shortlist_path: Path = Path("config/eia_route_shortlist.csv"),
    facets_path: Path = Path("data/external/eia/catalog/facets.csv"),
    output_dir: Path = Path("data/external/eia/catalog"),
    api_key: str | None = None,
    api_key_env: str = "EIA_API_KEY",
    base_url: str = DEFAULT_EIA_API_BASE_URL,
    bronze_dir: Path = Path("data/external/eia/bronze/facets"),
    cache_dir: Path = Path("data/external/eia/request_cache"),
    manifest_dir: Path = Path("data/external/eia/manifests"),
    allowed_statuses: tuple[str, ...] = ("approved_facet_discovery",),
    max_priority: int | None = None,
    release_products: tuple[str, ...] | None = None,
    selected_routes: tuple[str, ...] | None = None,
    timeout_seconds: float = 30.0,
    max_retries: int = 4,
    request_delay_seconds: float = 0.25,
    refresh_cache: bool = False,
    progress_every: int = 10,
    progress: Callable[[str], None] | None = None,
) -> dict[str, Any]:
    if progress_every <= 0:
        raise ValueError("progress_every must be positive")
    resolved_api_key = api_key or os.environ.get(api_key_env, "")
    if not resolved_api_key:
        raise EiaCatalogError(
            f"No EIA API key found. Set {api_key_env} or pass an API key explicitly."
        )
    shortlist = _shortlist_rows(
        shortlist_path,
        allowed_statuses=allowed_statuses,
        max_priority=max_priority,
        release_products=release_products,
        selected_routes=selected_routes,
    )
    facets_by_route = _facet_definitions_by_route(facets_path)
    missing_routes = [row["route"] for row in shortlist if row["route"] not in facets_by_route]
    if missing_routes:
        raise EiaCatalogError(f"Shortlisted routes have no cataloged facets: {missing_routes}")

    work: list[tuple[dict[str, str], dict[str, str]]] = []
    for shortlist_row in shortlist:
        work.extend((shortlist_row, facet) for facet in facets_by_route[shortlist_row["route"]])

    client = EiaApiClient(
        resolved_api_key,
        base_url=base_url,
        bronze_dir=bronze_dir,
        cache_dir=cache_dir,
        timeout_seconds=timeout_seconds,
        max_retries=max_retries,
        request_delay_seconds=request_delay_seconds,
        refresh_cache=refresh_cache,
    )
    fetched_at = _iso_utc()
    requests: list[dict[str, Any]] = []
    fetched_values: list[dict[str, Any]] = []
    fetched_summaries: list[dict[str, Any]] = []
    fetched_groups: set[tuple[str, str]] = set()

    for index, (shortlist_row, facet) in enumerate(work, start=1):
        route = shortlist_row["route"]
        facet_id = facet["facet_id"]
        facet_route = f"{route}facet/{facet_id}/"
        try:
            fetched = client.fetch_route(facet_route)
        except EiaFetchError as exc:
            requests.append(exc.request_record)
            _write_failed_crawl_manifest(
                manifest_dir=manifest_dir,
                roots=[item[0]["route"] for item in work],
                request_records=requests,
                error=exc,
            )
            raise
        requests.append(fetched.request_record)
        response = fetched.payload.get("response") or {}
        values = response.get("facets") or []
        if not isinstance(values, list):
            raise EiaCatalogError(f"Facet response is not a list for {route} {facet_id}")
        response_total = response.get("totalFacets", "")
        response_checksum = fetched.request_record["response_checksum"]
        group = (route, facet_id)
        fetched_groups.add(group)
        group_value_ids: set[str] = set()
        for value in values:
            value_id = str(value.get("id", "")).strip()
            if not value_id or value_id in group_value_ids:
                continue
            group_value_ids.add(value_id)
            fetched_values.append(
                {
                    "schema_version": EIA_CATALOG_SCHEMA_VERSION,
                    "route": route,
                    "canonical_dataset_key": route.rstrip("/"),
                    "release_product": shortlist_row["release_product"],
                    "priority": shortlist_row["priority"],
                    "facet_id": facet_id,
                    "facet_value_id": value_id,
                    "facet_value_name": _clean_text(value.get("name")),
                    "first_seen_at": fetched_at,
                    "last_seen_at": fetched_at,
                    "is_current": True,
                    "source_response_checksum": response_checksum,
                }
            )
        parsed_count = len(group_value_ids)
        total_numeric = int(response_total) if str(response_total).isdigit() else None
        fetched_summaries.append(
            {
                "schema_version": EIA_CATALOG_SCHEMA_VERSION,
                "fetched_at": fetched_at,
                "route": route,
                "canonical_dataset_key": route.rstrip("/"),
                "release_product": shortlist_row["release_product"],
                "priority": shortlist_row["priority"],
                "facet_id": facet_id,
                "exact_cardinality": parsed_count,
                "response_total_facets": response_total,
                "count_matches_response_total": total_numeric is None or parsed_count == total_numeric,
                "fetch_status": "complete",
                "source_response_checksum": response_checksum,
            }
        )
        if progress is not None and (index == 1 or index % progress_every == 0 or index == len(work)):
            progress(
                f"[fetch-eia-shortlist-facets] {index}/{len(work)} "
                f"route={route} facet={facet_id} values={parsed_count:,}"
            )

    output_dir = Path(output_dir)
    values_path = output_dir / "facet_values.csv"
    summary_path = output_dir / "facet_value_summary.csv"
    merged_values = _merge_facet_values(_read_csv(values_path), fetched_values, fetched_groups)
    merged_summaries = _merge_facet_summaries(_read_csv(summary_path), fetched_summaries)
    _write_csv(values_path, merged_values, FACET_VALUE_COLUMNS)
    _write_csv(summary_path, merged_summaries, FACET_VALUE_SUMMARY_COLUMNS)

    run_id = datetime.fromisoformat(fetched_at.replace("Z", "+00:00")).strftime("%Y%m%dT%H%M%S%fZ")
    requests_path = Path(manifest_dir) / f"facets_{run_id}_requests.csv"
    run_summary_path = Path(manifest_dir) / f"facets_{run_id}_summary.json"
    _write_csv(requests_path, requests, REQUEST_COLUMNS)
    result = {
        "schema_version": EIA_CATALOG_SCHEMA_VERSION,
        "run_id": run_id,
        "fetched_at": fetched_at,
        "shortlist_route_count": len(shortlist),
        "facet_count": len(work),
        "current_facet_value_count": sum(str(row["is_current"]).lower() == "true" for row in merged_values),
        "total_facet_value_rows": len(merged_values),
        "request_count": len(requests),
        "cache_hit_count": sum(bool(row["from_cache"]) for row in requests),
        "outputs": {
            str(values_path): {"rows": len(merged_values), "sha256": _file_checksum(values_path)},
            str(summary_path): {"rows": len(merged_summaries), "sha256": _file_checksum(summary_path)},
            str(requests_path): {"rows": len(requests), "sha256": _file_checksum(requests_path)},
        },
    }
    _atomic_write_json(run_summary_path, result)
    return result


def catalog_eia_routes_from_api(
    *,
    roots: list[str] | tuple[str, ...] = DEFAULT_EIA_CATALOG_ROOTS,
    api_key: str | None = None,
    api_key_env: str = "EIA_API_KEY",
    base_url: str = DEFAULT_EIA_API_BASE_URL,
    output_dir: Path = Path("data/external/eia/catalog"),
    bronze_dir: Path = Path("data/external/eia/bronze/catalog"),
    cache_dir: Path = Path("data/external/eia/request_cache"),
    manifest_dir: Path = Path("data/external/eia/manifests"),
    timeout_seconds: float = 30.0,
    max_retries: int = 4,
    request_delay_seconds: float = 0.25,
    refresh_cache: bool = False,
    max_routes: int | None = None,
    max_depth: int | None = None,
) -> dict[str, Any]:
    resolved_api_key = api_key or os.environ.get(api_key_env, "")
    if not resolved_api_key:
        raise EiaCatalogError(
            f"No EIA API key found. Set {api_key_env} or pass an API key explicitly."
        )
    client = EiaApiClient(
        resolved_api_key,
        base_url=base_url,
        bronze_dir=bronze_dir,
        cache_dir=cache_dir,
        timeout_seconds=timeout_seconds,
        max_retries=max_retries,
        request_delay_seconds=request_delay_seconds,
        refresh_cache=refresh_cache,
    )
    try:
        build = crawl_eia_catalog(
            roots,
            client.fetch_route,
            max_routes=max_routes,
            max_depth=max_depth,
        )
    except EiaCrawlError as exc:
        _write_failed_crawl_manifest(
            manifest_dir=manifest_dir,
            roots=roots,
            request_records=exc.request_records,
            error=exc,
        )
        raise
    return write_eia_catalog_build(build, output_dir=output_dir, manifest_dir=manifest_dir)
