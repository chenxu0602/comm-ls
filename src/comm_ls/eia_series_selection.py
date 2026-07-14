from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


EIA_SERIES_SELECTION_SCHEMA_VERSION = "1"

CANDIDATE_COLUMNS = [
    "schema_version",
    "built_at",
    "candidate_type",
    "route",
    "canonical_dataset_key",
    "release_product",
    "route_priority",
    "expected_frequency",
    "series_id",
    "series_name",
    "economic_concept",
    "geography",
    "strategy_tags",
    "candidate_assets",
    "auto_score",
    "route_rank",
    "selection_reason",
    "status",
    "approved_for_backfill",
    "point_in_time_status",
    "revision_overlap_periods",
    "source_facet_checksum",
]

AUDIT_COLUMNS = [
    "schema_version",
    "built_at",
    "route",
    "release_product",
    "route_priority",
    "candidate_type",
    "available_series_values",
    "emitted_candidates",
    "max_series_per_route",
    "minimum_emitted_score",
    "status",
]

CONCEPT_TERMS: tuple[tuple[str, tuple[str, ...], int], ...] = (
    ("refinery_utilization", ("percent utilization", "utilization rate"), 48),
    (
        "refinery_throughput",
        ("gross inputs", "refiner net input of crude oil", "refinery net input of crude oil"),
        44,
    ),
    ("crude_quality", ("api gravity", "sulfur content"), 44),
    ("fcc_feed", ("catalytic cracking",), 42),
    ("hydrocracker_feed", ("hydrocracking",), 42),
    ("coker_feed", ("coking units",), 42),
    ("refinery_capacity", ("operating crude oil distillation capacity", "operable crude oil distillation capacity"), 40),
    ("crude_inventory", ("stocks excluding spr of crude oil", "stocks of crude oil"), 38),
    ("gasoline_inventory", ("stocks of finished motor gasoline",), 36),
    ("distillate_inventory", ("stocks of distillate fuel oil",), 36),
    ("jet_inventory", ("stocks of kerosene-type jet fuel", "stocks of jet fuel"), 36),
    ("gasoline_production", ("production of finished motor gasoline",), 34),
    ("distillate_production", ("production of distillate fuel oil",), 34),
    ("jet_production", ("production of kerosene-type jet fuel",), 34),
    ("gasoline_demand", ("product supplied of finished motor gasoline", "product supplied of motor gasoline"), 34),
    ("distillate_demand", ("product supplied of distillate fuel oil",), 34),
    ("jet_demand", ("product supplied of kerosene-type jet fuel",), 34),
    ("crude_flow", ("imports of crude oil", "exports of crude oil", "receipts of crude oil"), 32),
    ("gasoline_flow", ("imports of motor gasoline", "exports of motor gasoline", "receipts of motor gasoline"), 30),
    ("distillate_flow", ("imports of distillate fuel oil", "exports of distillate fuel oil", "receipts of distillate fuel oil"), 30),
    ("jet_flow", ("imports of kerosene-type jet fuel", "exports of kerosene-type jet fuel", "receipts of kerosene-type jet fuel"), 30),
    ("gasoline_yield", ("refinery yield of finished motor gasoline", "refinery yield of motor gasoline"), 38),
    ("distillate_yield", ("refinery yield of distillate fuel oil",), 38),
    ("jet_yield", ("refinery yield of kerosene-type jet fuel", "refinery yield of jet fuel"), 38),
    ("product_yield", ("refinery yield", "percent yield"), 28),
)

PRODUCT_FALLBACKS: tuple[tuple[str, tuple[str, ...], int], ...] = (
    ("crude_state", ("crude oil",), 20),
    ("gasoline_state", ("motor gasoline", "gasoline"), 18),
    ("distillate_state", ("distillate fuel oil", "distillate"), 18),
    ("jet_state", ("kerosene-type jet fuel", "jet fuel"), 18),
)

OVER_GRANULAR_TERMS = (
    "greater than 15 to 500 ppm",
    "greater than 500 ppm",
    "0 to 15 ppm sulfur",
    "gasoline blending components",
    "other oils",
)

STRATEGIC_ORIGIN_TERMS = (
    "from canada",
    "from mexico",
    "from saudi arabia",
    "from colombia",
    "from brazil",
    "from iraq",
    "from ecuador",
    "from venezuela",
)


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


def _geography(name: str) -> tuple[str, int, str]:
    lowered = name.lower()
    if "cushing" in lowered:
        return "CUSHING", 22, "geo:cushing"
    for padd in range(1, 6):
        if f"padd {padd}" in lowered or f"pad {padd}" in lowered:
            bonus = 20 if padd in {2, 3, 4} else 16
            return f"PADD_{padd}", bonus, f"geo:padd_{padd}"
    if "refining district" in lowered or "refinery district" in lowered:
        return "REFINING_DISTRICT", 10, "geo:refining_district"
    if "u.s." in lowered or "u. s." in lowered or "united states" in lowered:
        return "US", 14, "geo:us"
    return "OTHER", -8, "geo:other"


def score_eia_series(name: str, release_product: str, route_priority: int) -> dict[str, Any]:
    lowered = " ".join(name.lower().split())
    score = max(0, 24 - 4 * (route_priority - 1))
    reasons = [f"route_priority:{route_priority}"]
    concept = "unclassified"
    concept_score = 0
    for candidate_concept, terms, weight in CONCEPT_TERMS:
        if any(term in lowered for term in terms) and weight > concept_score:
            concept = candidate_concept
            concept_score = weight
    if concept_score == 0:
        for candidate_concept, terms, weight in PRODUCT_FALLBACKS:
            if any(term in lowered for term in terms) and weight > concept_score:
                concept = candidate_concept
                concept_score = weight
    score += concept_score
    if concept_score:
        reasons.append(f"concept:{concept}")
    else:
        reasons.append("concept:unclassified")

    geography, geography_score, geography_reason = _geography(name)
    score += geography_score
    reasons.append(geography_reason)

    if release_product.upper() == "WPSR":
        score += 12
        reasons.append("frequency:weekly")
    elif release_product.upper() == "PSM":
        score += 6
        reasons.append("frequency:monthly")

    penalties = [term for term in OVER_GRANULAR_TERMS if term in lowered]
    if penalties:
        score -= 12
        reasons.append("penalty:over_granular_product")
    if any(term in lowered for term in STRATEGIC_ORIGIN_TERMS):
        score += 18
        reasons.append("origin:strategic_us_crude_supplier")
    return {
        "auto_score": score,
        "economic_concept": concept,
        "geography": geography,
        "selection_reason": "|".join(reasons),
    }


def _select_diverse_series(scored: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    remaining = list(scored)
    selected: list[dict[str, Any]] = []
    concept_counts: dict[str, int] = {}
    geography_counts: dict[str, int] = {}
    pair_counts: dict[tuple[str, str], int] = {}
    while remaining and len(selected) < limit:
        def adjusted_key(row: dict[str, Any]) -> tuple[int, int, str]:
            concept = str(row["economic_concept"])
            geography = str(row["geography"])
            adjusted = (
                int(row["auto_score"])
                - 8 * concept_counts.get(concept, 0)
                - 3 * geography_counts.get(geography, 0)
                - 40 * pair_counts.get((concept, geography), 0)
            )
            return adjusted, int(row["auto_score"]), str(row["facet_value_id"])

        best = max(remaining, key=adjusted_key)
        remaining.remove(best)
        selected.append(best)
        concept = str(best["economic_concept"])
        geography = str(best["geography"])
        concept_counts[concept] = concept_counts.get(concept, 0) + 1
        geography_counts[geography] = geography_counts.get(geography, 0) + 1
        pair = (concept, geography)
        pair_counts[pair] = pair_counts.get(pair, 0) + 1
    return selected


def build_eia_series_candidates(
    *,
    shortlist_path: Path = Path("config/eia_route_shortlist.csv"),
    facet_values_path: Path = Path("data/external/eia/catalog/facet_values.csv"),
    output_path: Path = Path("data/external/eia/catalog/series_candidates.csv"),
    audit_output_path: Path = Path("data/external/eia/catalog/series_candidate_audit.csv"),
    manifest_dir: Path = Path("data/external/eia/manifests"),
    max_series_per_route: int = 20,
) -> dict[str, Any]:
    if max_series_per_route <= 0:
        raise ValueError("max_series_per_route must be positive")
    shortlist = _read_csv(Path(shortlist_path))
    facets = _read_csv(Path(facet_values_path))
    if not shortlist:
        raise ValueError(f"EIA route shortlist is empty or missing: {shortlist_path}")
    if not facets:
        raise ValueError(f"EIA facet values are empty or missing: {facet_values_path}")

    built_at = _iso_utc()
    current_series: dict[str, list[dict[str, str]]] = {}
    for row in facets:
        if row.get("facet_id") != "series" or row.get("is_current", "").lower() != "true":
            continue
        current_series.setdefault(row.get("route", ""), []).append(row)

    candidates: list[dict[str, Any]] = []
    audits: list[dict[str, Any]] = []
    for route_row in sorted(shortlist, key=lambda row: (int(row["priority"]), row["route"])):
        if route_row.get("status") != "approved_facet_discovery":
            continue
        route = route_row["route"]
        release_product = route_row["release_product"]
        route_priority = int(route_row["priority"])
        route_series = current_series.get(route, [])
        candidate_type = "series"
        selected: list[dict[str, Any]] = []
        if route_series:
            scored: list[dict[str, Any]] = []
            for value in route_series:
                score = score_eia_series(value["facet_value_name"], release_product, route_priority)
                scored.append({**value, **score})
            selected = _select_diverse_series(scored, max_series_per_route)
            for rank, row in enumerate(selected, start=1):
                candidates.append(
                    {
                        "schema_version": EIA_SERIES_SELECTION_SCHEMA_VERSION,
                        "built_at": built_at,
                        "candidate_type": candidate_type,
                        "route": route,
                        "canonical_dataset_key": route_row["canonical_dataset_key"],
                        "release_product": release_product,
                        "route_priority": route_priority,
                        "expected_frequency": route_row["expected_frequency"],
                        "series_id": row["facet_value_id"],
                        "series_name": row["facet_value_name"],
                        "economic_concept": row["economic_concept"],
                        "geography": row["geography"],
                        "strategy_tags": route_row["strategy_tags"],
                        "candidate_assets": route_row["candidate_assets"],
                        "auto_score": row["auto_score"],
                        "route_rank": rank,
                        "selection_reason": row["selection_reason"],
                        "status": "needs_manual_review",
                        "approved_for_backfill": False,
                        "point_in_time_status": "unverified",
                        "revision_overlap_periods": 8 if release_product == "WPSR" else 6,
                        "source_facet_checksum": row["source_response_checksum"],
                    }
                )
        else:
            candidate_type = "dataset_scope"
            candidates.append(
                {
                    "schema_version": EIA_SERIES_SELECTION_SCHEMA_VERSION,
                    "built_at": built_at,
                    "candidate_type": candidate_type,
                    "route": route,
                    "canonical_dataset_key": route_row["canonical_dataset_key"],
                    "release_product": release_product,
                    "route_priority": route_priority,
                    "expected_frequency": route_row["expected_frequency"],
                    "series_id": "",
                    "series_name": "Multidimensional dataset scope",
                    "economic_concept": "crude_import_sourcing",
                    "geography": "REFINERY_OR_PORT_DESTINATION",
                    "strategy_tags": route_row["strategy_tags"],
                    "candidate_assets": route_row["candidate_assets"],
                    "auto_score": 90,
                    "route_rank": 1,
                    "selection_reason": "dataset_scope:no_series_facet|requires_owner_history_mapping",
                    "status": "needs_manual_review",
                    "approved_for_backfill": False,
                    "point_in_time_status": "unverified",
                    "revision_overlap_periods": 6,
                    "source_facet_checksum": "",
                }
            )

        audits.append(
            {
                "schema_version": EIA_SERIES_SELECTION_SCHEMA_VERSION,
                "built_at": built_at,
                "route": route,
                "release_product": release_product,
                "route_priority": route_priority,
                "candidate_type": candidate_type,
                "available_series_values": len(route_series),
                "emitted_candidates": len(selected) if route_series else 1,
                "max_series_per_route": max_series_per_route,
                "minimum_emitted_score": min((int(row["auto_score"]) for row in selected), default=90),
                "status": "complete",
            }
        )

    candidates.sort(key=lambda row: (int(row["route_priority"]), row["route"], int(row["route_rank"])))
    _atomic_write_csv(Path(output_path), candidates, CANDIDATE_COLUMNS)
    _atomic_write_csv(Path(audit_output_path), audits, AUDIT_COLUMNS)
    run_id = datetime.fromisoformat(built_at.replace("Z", "+00:00")).strftime("%Y%m%dT%H%M%S%fZ")
    result = {
        "schema_version": EIA_SERIES_SELECTION_SCHEMA_VERSION,
        "run_id": run_id,
        "built_at": built_at,
        "candidate_count": len(candidates),
        "series_candidate_count": sum(row["candidate_type"] == "series" for row in candidates),
        "dataset_scope_count": sum(row["candidate_type"] == "dataset_scope" for row in candidates),
        "route_count": len(audits),
        "approved_for_backfill_count": sum(bool(row["approved_for_backfill"]) for row in candidates),
        "output_path": str(output_path),
        "output_sha256": _file_checksum(Path(output_path)),
        "audit_output_path": str(audit_output_path),
        "audit_output_sha256": _file_checksum(Path(audit_output_path)),
        "inputs": {
            str(shortlist_path): _file_checksum(Path(shortlist_path)),
            str(facet_values_path): _file_checksum(Path(facet_values_path)),
        },
        "max_series_per_route": max_series_per_route,
        "network_requests": 0,
        "observation_rows_downloaded": 0,
    }
    manifest_path = Path(manifest_dir) / f"series_candidates_{run_id}_summary.json"
    result["manifest_path"] = str(manifest_path)
    _atomic_write_json(manifest_path, result)
    return result
