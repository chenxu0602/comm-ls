from __future__ import annotations

import csv
import difflib
import gzip
import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


WPSR_CROSSWALK_SCHEMA_VERSION = "2"
DEFAULT_WPSR_CROSSWALK_RELEASE_DATE = "2025-01-08"
DEFAULT_EIA_API_BASE_URL = "https://api.eia.gov/v2"

API_OBSERVATION_COLUMNS = [
    "schema_version",
    "release_date",
    "observation_date",
    "route",
    "series_id",
    "series_name",
    "state_family",
    "geography",
    "value_raw",
    "value_numeric",
    "unit",
    "source_response_checksum",
    "status",
    "error",
]

CROSSWALK_CANDIDATE_COLUMNS = [
    "schema_version",
    "release_date",
    "observation_date",
    "series_id",
    "series_name",
    "state_family",
    "geography",
    "api_value",
    "api_unit",
    "candidate_rank",
    "archive_row_key",
    "archive_stub_1",
    "archive_group_label",
    "archive_stub_2",
    "archive_value",
    "numeric_relation",
    "context_compatible",
    "semantic_score",
    "combined_score",
    "approved_crosswalk",
]

CROSSWALK_AUDIT_COLUMNS = [
    "schema_version",
    "release_date",
    "observation_date",
    "series_id",
    "series_name",
    "state_family",
    "geography",
    "api_value",
    "api_unit",
    "exact_numeric_candidate_count",
    "scaled_numeric_candidate_count",
    "top_archive_row_key",
    "top_numeric_relation",
    "top_context_compatible",
    "top_semantic_score",
    "top_combined_score",
    "score_margin",
    "crosswalk_status",
    "approved_crosswalk",
]

REQUEST_COLUMNS = [
    "schema_version",
    "requested_at",
    "route",
    "observation_date",
    "series_count",
    "request_url_redacted",
    "request_hash",
    "from_cache",
    "attempt_count",
    "response_checksum",
    "response_bytes",
    "status",
    "error",
]

STOP_WORDS = {
    "a",
    "and",
    "barrel",
    "barrels",
    "calendar",
    "day",
    "excluding",
    "finished",
    "in",
    "including",
    "into",
    "million",
    "of",
    "operable",
    "per",
    "refiner",
    "refineries",
    "refinery",
    "the",
    "thousand",
    "to",
    "total",
    "us",
}


def _iso_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _hash_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


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
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def _write_gzip(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with gzip.open(temporary, "wb") as handle:
        handle.write(content)
    temporary.replace(path)


def _truthy(value: Any) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def _number(value: Any) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(str(value).replace(",", ""))
    except ValueError:
        return None


def _normalized_text(value: str) -> str:
    lowered = value.lower().replace("u.s.", "us")
    lowered = lowered.replace("rocky mountains", "rocky mountain")
    lowered = lowered.replace("kerosene type", "kerosene-type")
    lowered = re.sub(r"\bok\b", "oklahoma", lowered)
    return " ".join(re.findall(r"[a-z0-9]+", lowered))


def _tokens(value: str) -> set[str]:
    return {token for token in _normalized_text(value).split() if token not in STOP_WORDS}


def _semantic_score(series_name: str, archive_text: str) -> float:
    series_tokens = _tokens(series_name)
    archive_tokens = _tokens(archive_text)
    union = series_tokens | archive_tokens
    token_score = len(series_tokens & archive_tokens) / len(union) if union else 0.0
    sequence_score = difflib.SequenceMatcher(
        None,
        _normalized_text(series_name),
        _normalized_text(archive_text),
    ).ratio()
    return round(100.0 * (0.7 * token_score + 0.3 * sequence_score), 6)


def _numeric_relation(api_value: float | None, archive_value: float | None) -> str:
    if api_value is None or archive_value is None:
        return "none"
    tolerance = max(1e-9, abs(api_value) * 1e-9)
    if abs(api_value - archive_value) <= tolerance:
        return "exact"
    if abs(api_value / 1000.0 - archive_value) <= tolerance:
        return "api_div_1000"
    if abs(api_value * 1000.0 - archive_value) <= max(1e-9, abs(api_value * 1000.0) * 1e-9):
        return "api_mul_1000"
    return "none"


def _context_compatible(series_name: str, group_label: str) -> bool:
    series = _normalized_text(series_name)
    group = _normalized_text(group_label)
    if group == "other" and "other" not in series:
        return False
    subtype_phrases = (
        "conventional",
        "reformulated",
        "ed55 and lower",
        "greater than ed55",
        "15 ppm sulfur",
        "greater than 15 ppm sulfur",
        "blending components",
    )
    return all(phrase not in group or phrase in series for phrase in subtype_phrases)


def rank_wpsr_crosswalk_candidates(
    api_observation: dict[str, Any],
    archive_rows: list[dict[str, Any]],
    *,
    top_n: int = 5,
) -> list[dict[str, Any]]:
    if top_n <= 0:
        raise ValueError("top_n must be positive")
    api_value = _number(api_observation.get("value_numeric"))
    ranked: list[dict[str, Any]] = []
    for row in archive_rows:
        archive_value = _number(row.get("value_numeric"))
        relation = _numeric_relation(api_value, archive_value)
        archive_text = " ".join(
            str(row.get(column, ""))
            for column in ("stub_1", "group_label", "stub_2")
        )
        semantic = _semantic_score(str(api_observation.get("series_name", "")), archive_text)
        context_compatible = _context_compatible(
            str(api_observation.get("series_name", "")),
            str(row.get("group_label", "")),
        )
        semantically_compatible = semantic >= 25.0
        numeric_bonus = {
            "exact": 100.0 if semantically_compatible else 15.0,
            "api_div_1000": 85.0 if semantically_compatible else 10.0,
            "api_mul_1000": 85.0 if semantically_compatible else 10.0,
            "none": 0.0,
        }[relation]
        combined = numeric_bonus + semantic
        ranked.append(
            {
                "archive_row_key": row.get("row_key", ""),
                "archive_stub_1": row.get("stub_1", ""),
                "archive_group_label": row.get("group_label", ""),
                "archive_stub_2": row.get("stub_2", ""),
                "archive_value": archive_value,
                "numeric_relation": relation,
                "context_compatible": context_compatible,
                "semantic_score": semantic,
                "combined_score": round(combined, 6),
            }
        )
    ranked.sort(
        key=lambda row: (
            -float(row["combined_score"]),
            -float(row["semantic_score"]),
            str(row["archive_row_key"]),
        )
    )
    return ranked[:top_n]


def _resolve_api_key(api_key: str | None, api_key_env: str) -> str:
    value = api_key or os.environ.get(api_key_env, "")
    if not value:
        raise ValueError(f"EIA API key is required via --api-key or {api_key_env}")
    return value


def _request_urls(
    *,
    base_url: str,
    route: str,
    series_ids: list[str],
    observation_date: str,
    api_key: str,
) -> tuple[str, str]:
    path = f"{base_url.rstrip('/')}/{route.strip('/')}/data/"
    public_params: list[tuple[str, str]] = [
        ("frequency", "weekly"),
        ("data[0]", "value"),
        ("start", observation_date),
        ("end", observation_date),
        ("length", str(max(50, len(series_ids) * 2))),
    ]
    public_params.extend(("facets[series][]", series_id) for series_id in sorted(series_ids))
    redacted_url = f"{path}?{urllib.parse.urlencode(public_params)}"
    query_url = f"{path}?{urllib.parse.urlencode([('api_key', api_key), *public_params])}"
    return redacted_url, query_url


def _fetch_bytes(url: str, timeout_seconds: float, max_retries: int) -> tuple[bytes, int]:
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": "comm-ls-eia-research/1"},
    )
    for attempt in range(1, max_retries + 2):
        try:
            with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
                return response.read(), attempt
        except (urllib.error.URLError, TimeoutError):
            if attempt > max_retries:
                raise
            time.sleep(min(2 ** (attempt - 1), 8))
    raise RuntimeError("unreachable")


def _cached_api_fetch(
    *,
    redacted_url: str,
    query_url: str,
    route: str,
    observation_date: str,
    series_count: int,
    cache_dir: Path,
    bronze_dir: Path,
    refresh_cache: bool,
    fetch: Callable[[str], bytes] | None,
    timeout_seconds: float,
    max_retries: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    request_hash = hashlib.sha256(redacted_url.encode()).hexdigest()
    pointer_path = cache_dir / f"eia_wpsr_crosswalk_{request_hash}.json"
    requested_at = _iso_utc()
    if not refresh_cache and pointer_path.exists():
        pointer = json.loads(pointer_path.read_text(encoding="utf-8"))
        response_path = Path(pointer["response_path"])
        with gzip.open(response_path, "rt", encoding="utf-8") as handle:
            payload = json.load(handle)
        return payload, {
            "schema_version": WPSR_CROSSWALK_SCHEMA_VERSION,
            "requested_at": requested_at,
            "route": route,
            "observation_date": observation_date,
            "series_count": series_count,
            "request_url_redacted": redacted_url,
            "request_hash": request_hash,
            "from_cache": True,
            "attempt_count": 0,
            "response_checksum": pointer["response_checksum"],
            "response_bytes": pointer["response_bytes"],
            "status": "ok",
            "error": "",
        }

    if fetch is None:
        content, attempts = _fetch_bytes(query_url, timeout_seconds, max_retries)
    else:
        content, attempts = fetch(query_url), 1
    payload = json.loads(content.decode("utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("response"), dict):
        raise ValueError(f"Malformed EIA response for {route}")
    if payload.get("error"):
        raise ValueError(f"EIA API error for {route}: {payload['error']}")
    checksum = _hash_bytes(content)
    response_path = bronze_dir / f"observation_date={observation_date}" / f"{checksum}.json.gz"
    if not response_path.exists():
        _write_gzip(response_path, content)
    _atomic_write_json(
        pointer_path,
        {
            "request_hash": request_hash,
            "request_url_redacted": redacted_url,
            "response_path": str(response_path),
            "response_checksum": checksum,
            "response_bytes": len(content),
            "cached_at": _iso_utc(),
        },
    )
    return payload, {
        "schema_version": WPSR_CROSSWALK_SCHEMA_VERSION,
        "requested_at": requested_at,
        "route": route,
        "observation_date": observation_date,
        "series_count": series_count,
        "request_url_redacted": redacted_url,
        "request_hash": request_hash,
        "from_cache": False,
        "attempt_count": attempts,
        "response_checksum": checksum,
        "response_bytes": len(content),
        "status": "ok",
        "error": "",
    }


def _audit_row(
    observation: dict[str, Any],
    ranked: list[dict[str, Any]],
    *,
    release_date: str,
    observation_date: str,
) -> dict[str, Any]:
    exact_count = sum(row["numeric_relation"] == "exact" for row in ranked)
    scaled_count = sum(
        row["numeric_relation"] in {"api_div_1000", "api_mul_1000"} for row in ranked
    )
    top = ranked[0] if ranked else {}
    margin = (
        float(ranked[0]["combined_score"]) - float(ranked[1]["combined_score"])
        if len(ranked) > 1
        else ""
    )
    top_relation = top.get("numeric_relation")
    top_semantic = float(top.get("semantic_score", 0.0))
    if top_relation == "none":
        status = "unresolved_no_numeric_confirmation"
    elif not top.get("context_compatible", False):
        status = "unresolved_subcategory_mismatch"
    elif top_semantic < 25.0:
        status = "unresolved_low_semantic_compatibility"
    elif margin != "" and float(margin) < 5.0:
        status = "ambiguous_numeric_candidates_manual_review"
    elif exact_count == 1 and top_relation == "exact":
        status = "unique_exact_candidate_manual_review"
    elif top_relation in {"exact", "api_div_1000", "api_mul_1000"}:
        status = "ranked_numeric_candidates_manual_review"
    else:
        status = "unresolved"
    return {
        "schema_version": WPSR_CROSSWALK_SCHEMA_VERSION,
        "release_date": release_date,
        "observation_date": observation_date,
        "series_id": observation["series_id"],
        "series_name": observation["series_name"],
        "state_family": observation["state_family"],
        "geography": observation["geography"],
        "api_value": observation["value_numeric"],
        "api_unit": observation["unit"],
        "exact_numeric_candidate_count": exact_count,
        "scaled_numeric_candidate_count": scaled_count,
        "top_archive_row_key": top.get("archive_row_key", ""),
        "top_numeric_relation": top.get("numeric_relation", ""),
        "top_context_compatible": top.get("context_compatible", ""),
        "top_semantic_score": top.get("semantic_score", ""),
        "top_combined_score": top.get("combined_score", ""),
        "score_margin": margin,
        "crosswalk_status": status,
        "approved_crosswalk": False,
    }


def run_wpsr_crosswalk_validation(
    *,
    release_date: str = DEFAULT_WPSR_CROSSWALK_RELEASE_DATE,
    shortlist_path: Path = Path("config/eia_series_shortlist.csv"),
    archive_releases_path: Path = Path(
        "data/external/eia/archive_pilot/wpsr_archive_pilot_releases.csv"
    ),
    archive_values_path: Path = Path(
        "data/external/eia/archive_pilot/wpsr_archive_pilot_values.csv"
    ),
    output_dir: Path = Path("data/external/eia/archive_pilot"),
    api_key: str | None = None,
    api_key_env: str = "EIA_API_KEY",
    base_url: str = DEFAULT_EIA_API_BASE_URL,
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
    if top_n <= 0:
        raise ValueError("top_n must be positive")
    api_key_value = _resolve_api_key(api_key, api_key_env)
    shortlist = _read_csv(Path(shortlist_path))
    releases = _read_csv(Path(archive_releases_path))
    archive_values = _read_csv(Path(archive_values_path))
    core = [
        row
        for row in shortlist
        if row.get("release_product") == "WPSR"
        and row.get("decision") == "keep"
        and _truthy(row.get("proposed_initial_core"))
    ]
    if not core:
        raise ValueError("No WPSR proposed_initial_core series found")
    release = next(
        (
            row
            for row in releases
            if row.get("requested_release_date") == release_date and row.get("status") == "ok"
        ),
        None,
    )
    if release is None:
        raise ValueError(f"Successful archived WPSR release is missing: {release_date}")
    observation_date = str(release["week_ending_date"])
    archive_rows = [
        row
        for row in archive_values
        if row.get("release_date") == release_date
        and row.get("observation_date") == observation_date
        and row.get("observation_column") == "current"
    ]
    if not archive_rows:
        raise ValueError(f"Archived WPSR current values are missing for {release_date}")
    if "group_label" not in archive_rows[0]:
        raise ValueError("Archived WPSR values predate group_label; rerun test-eia-wpsr-archive")

    by_route: defaultdict[str, list[dict[str, str]]] = defaultdict(list)
    for row in core:
        by_route[str(row["route"])].append(row)

    request_rows: list[dict[str, Any]] = []
    api_rows: list[dict[str, Any]] = []
    network_requests = 0
    for route in sorted(by_route):
        selected = by_route[route]
        series_ids = [str(row["series_id"]) for row in selected]
        redacted_url, query_url = _request_urls(
            base_url=base_url,
            route=route,
            series_ids=series_ids,
            observation_date=observation_date,
            api_key=api_key_value,
        )
        if request_delay_seconds:
            time.sleep(request_delay_seconds)
        try:
            payload, request_row = _cached_api_fetch(
                redacted_url=redacted_url,
                query_url=query_url,
                route=route,
                observation_date=observation_date,
                series_count=len(series_ids),
                cache_dir=Path(cache_dir),
                bronze_dir=Path(bronze_dir),
                refresh_cache=refresh_cache,
                fetch=fetcher,
                timeout_seconds=timeout_seconds,
                max_retries=max_retries,
            )
            request_rows.append(request_row)
            network_requests += int(not request_row["from_cache"])
            source_checksum = str(request_row["response_checksum"])
            response_data = payload["response"].get("data") or []
            returned = {str(row.get("series", "")): row for row in response_data}
            metadata = {str(row["series_id"]): row for row in selected}
            for series_id in series_ids:
                source = returned.get(series_id)
                candidate = metadata[series_id]
                if source is None:
                    api_rows.append(
                        {
                            "schema_version": WPSR_CROSSWALK_SCHEMA_VERSION,
                            "release_date": release_date,
                            "observation_date": observation_date,
                            "route": route,
                            "series_id": series_id,
                            "series_name": candidate["series_name"],
                            "state_family": candidate["state_family"],
                            "geography": candidate["geography"],
                            "value_raw": "",
                            "value_numeric": "",
                            "unit": "",
                            "source_response_checksum": source_checksum,
                            "status": "missing",
                            "error": "No API row returned for observation date",
                        }
                    )
                    continue
                api_rows.append(
                    {
                        "schema_version": WPSR_CROSSWALK_SCHEMA_VERSION,
                        "release_date": release_date,
                        "observation_date": observation_date,
                        "route": route,
                        "series_id": series_id,
                        "series_name": candidate["series_name"],
                        "state_family": candidate["state_family"],
                        "geography": candidate["geography"],
                        "value_raw": source.get("value", ""),
                        "value_numeric": _number(source.get("value")),
                        "unit": source.get("units", ""),
                        "source_response_checksum": source_checksum,
                        "status": "ok",
                        "error": "",
                    }
                )
        except Exception as exc:
            error = f"{type(exc).__name__}: {exc}"
            request_rows.append(
                {
                    "schema_version": WPSR_CROSSWALK_SCHEMA_VERSION,
                    "requested_at": _iso_utc(),
                    "route": route,
                    "observation_date": observation_date,
                    "series_count": len(series_ids),
                    "request_url_redacted": redacted_url,
                    "request_hash": hashlib.sha256(redacted_url.encode()).hexdigest(),
                    "from_cache": False,
                    "attempt_count": 0,
                    "response_checksum": "",
                    "response_bytes": 0,
                    "status": "error",
                    "error": error,
                }
            )
            for candidate in selected:
                api_rows.append(
                    {
                        "schema_version": WPSR_CROSSWALK_SCHEMA_VERSION,
                        "release_date": release_date,
                        "observation_date": observation_date,
                        "route": route,
                        "series_id": candidate["series_id"],
                        "series_name": candidate["series_name"],
                        "state_family": candidate["state_family"],
                        "geography": candidate["geography"],
                        "value_raw": "",
                        "value_numeric": "",
                        "unit": "",
                        "source_response_checksum": "",
                        "status": "error",
                        "error": error,
                    }
                )

    candidate_rows: list[dict[str, Any]] = []
    audit_rows: list[dict[str, Any]] = []
    for observation in api_rows:
        if observation["status"] != "ok":
            audit_rows.append(
                {
                    "schema_version": WPSR_CROSSWALK_SCHEMA_VERSION,
                    "release_date": release_date,
                    "observation_date": observation_date,
                    "series_id": observation["series_id"],
                    "series_name": observation["series_name"],
                    "state_family": observation["state_family"],
                    "geography": observation["geography"],
                    "api_value": "",
                    "api_unit": "",
                    "exact_numeric_candidate_count": 0,
                    "scaled_numeric_candidate_count": 0,
                    "top_archive_row_key": "",
                    "top_numeric_relation": "",
                    "top_semantic_score": "",
                    "top_combined_score": "",
                    "score_margin": "",
                    "crosswalk_status": "missing_api_observation",
                    "approved_crosswalk": False,
                }
            )
            continue
        ranked = rank_wpsr_crosswalk_candidates(
            observation,
            archive_rows,
            top_n=len(archive_rows),
        )
        for rank, candidate in enumerate(ranked[:top_n], start=1):
            candidate_rows.append(
                {
                    "schema_version": WPSR_CROSSWALK_SCHEMA_VERSION,
                    "release_date": release_date,
                    "observation_date": observation_date,
                    "series_id": observation["series_id"],
                    "series_name": observation["series_name"],
                    "state_family": observation["state_family"],
                    "geography": observation["geography"],
                    "api_value": observation["value_numeric"],
                    "api_unit": observation["unit"],
                    "candidate_rank": rank,
                    **candidate,
                    "approved_crosswalk": False,
                }
            )
        audit_rows.append(
            _audit_row(
                observation,
                ranked,
                release_date=release_date,
                observation_date=observation_date,
            )
        )

    output_dir = Path(output_dir)
    observations_path = output_dir / "wpsr_crosswalk_api_observations.csv"
    candidates_path = output_dir / "wpsr_crosswalk_candidates.csv"
    audit_path = output_dir / "wpsr_crosswalk_audit.csv"
    requests_path = output_dir / "wpsr_crosswalk_requests.csv"
    _atomic_write_csv(observations_path, api_rows, API_OBSERVATION_COLUMNS)
    _atomic_write_csv(candidates_path, candidate_rows, CROSSWALK_CANDIDATE_COLUMNS)
    _atomic_write_csv(audit_path, audit_rows, CROSSWALK_AUDIT_COLUMNS)
    _atomic_write_csv(requests_path, request_rows, REQUEST_COLUMNS)

    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    summary = {
        "schema_version": WPSR_CROSSWALK_SCHEMA_VERSION,
        "run_id": run_id,
        "release_date": release_date,
        "observation_date": observation_date,
        "initial_core_count": len(core),
        "route_count": len(by_route),
        "api_observation_count": sum(row["status"] == "ok" for row in api_rows),
        "api_missing_count": sum(row["status"] != "ok" for row in api_rows),
        "request_error_count": sum(row["status"] != "ok" for row in request_rows),
        "candidate_row_count": len(candidate_rows),
        "unresolved_count": sum(
            str(row["crosswalk_status"]).startswith("unresolved")
            or row["crosswalk_status"] == "missing_api_observation"
            for row in audit_rows
        ),
        "ambiguous_count": sum(
            str(row["crosswalk_status"]).startswith("ambiguous") for row in audit_rows
        ),
        "approved_crosswalk_count": 0,
        "network_requests": network_requests,
        "observation_backfill_authorized": False,
        "outputs": [
            str(observations_path),
            str(candidates_path),
            str(audit_path),
            str(requests_path),
        ],
    }
    manifest_path = Path(manifest_dir) / f"wpsr_crosswalk_{run_id}_summary.json"
    summary["manifest_path"] = str(manifest_path)
    _atomic_write_json(manifest_path, summary)
    return summary
