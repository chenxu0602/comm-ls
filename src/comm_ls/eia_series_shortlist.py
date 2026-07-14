from __future__ import annotations

import csv
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from comm_ls.eia_release_validation import expected_point_in_time_status
from comm_ls.eia_series_selection import OVER_GRANULAR_TERMS


EIA_SERIES_SHORTLIST_SCHEMA_VERSION = "1"

SHORTLIST_COLUMNS = [
    "schema_version",
    "reviewed_at",
    "candidate_type",
    "route",
    "canonical_dataset_key",
    "release_product",
    "route_priority",
    "expected_frequency",
    "candidate_route_rank",
    "series_id",
    "series_name",
    "economic_concept",
    "state_family",
    "geography",
    "reported_unit",
    "canonical_unit_status",
    "strategy_tags",
    "candidate_assets",
    "decision",
    "decision_reason",
    "review_priority",
    "proposed_initial_core",
    "point_in_time_status",
    "approved_for_backfill",
    "revision_overlap_periods",
    "reviewer",
    "source_candidate_checksum",
]

ROUTE_CONCEPTS: dict[str, set[str]] = {
    "petroleum/stoc/wstk/": {
        "crude_inventory",
        "gasoline_inventory",
        "distillate_inventory",
        "jet_inventory",
    },
    "petroleum/pnp/wiup/": {
        "refinery_utilization",
        "refinery_throughput",
        "refinery_capacity",
    },
    "petroleum/pnp/wprodr/": {
        "gasoline_production",
        "distillate_production",
        "jet_production",
    },
    "petroleum/cons/wpsup/": {
        "gasoline_demand",
        "distillate_demand",
        "jet_demand",
    },
    "petroleum/move/wkly/": {
        "crude_flow",
        "gasoline_flow",
        "distillate_flow",
        "jet_flow",
    },
    "petroleum/pnp/crq/": {"crude_quality"},
    "petroleum/pnp/dwns/": {"fcc_feed", "hydrocracker_feed", "coker_feed"},
    "petroleum/pnp/inpt2/": {"refinery_throughput"},
    "petroleum/pnp/pct/": {
        "gasoline_yield",
        "distillate_yield",
        "jet_yield",
    },
    "petroleum/pnp/unc/": {
        "refinery_utilization",
        "refinery_throughput",
        "refinery_capacity",
    },
    "petroleum/pnp/refp2/": {
        "gasoline_production",
        "distillate_production",
        "jet_production",
    },
    "petroleum/move/netr/": {
        "crude_flow",
        "gasoline_flow",
        "distillate_flow",
        "jet_flow",
    },
    "petroleum/cons/psup/": {
        "gasoline_demand",
        "distillate_demand",
        "jet_demand",
    },
}

CONTEXT_ROUTES = {
    "petroleum/sum/snd/",
    "petroleum/sum/sndw/",
    "petroleum/stoc/typ/",
}

STATE_FAMILY = {
    "crude_inventory": "inventory_tightness",
    "gasoline_inventory": "inventory_tightness",
    "distillate_inventory": "inventory_tightness",
    "jet_inventory": "inventory_tightness",
    "refinery_utilization": "refinery_operating_pressure",
    "refinery_throughput": "refinery_operating_pressure",
    "refinery_capacity": "refinery_operating_pressure",
    "gasoline_production": "product_output",
    "distillate_production": "product_output",
    "jet_production": "product_output",
    "gasoline_demand": "product_demand",
    "distillate_demand": "product_demand",
    "jet_demand": "product_demand",
    "crude_flow": "regional_flow_stress",
    "gasoline_flow": "regional_flow_stress",
    "distillate_flow": "regional_flow_stress",
    "jet_flow": "regional_flow_stress",
    "crude_quality": "crude_slate",
    "fcc_feed": "complexity_use",
    "hydrocracker_feed": "complexity_use",
    "coker_feed": "complexity_use",
    "gasoline_yield": "product_slate",
    "distillate_yield": "product_slate",
    "jet_yield": "product_slate",
    "crude_import_sourcing": "company_crude_sourcing",
}

STOCK_CONCEPTS = {
    "crude_inventory",
    "gasoline_inventory",
    "distillate_inventory",
    "jet_inventory",
}

RATE_CONCEPTS = {
    "refinery_throughput",
    "gasoline_production",
    "distillate_production",
    "jet_production",
    "gasoline_demand",
    "distillate_demand",
    "jet_demand",
    "crude_flow",
    "gasoline_flow",
    "distillate_flow",
    "jet_flow",
    "fcc_feed",
    "hydrocracker_feed",
    "coker_feed",
}

PERCENT_CONCEPTS = {
    "refinery_utilization",
    "gasoline_yield",
    "distillate_yield",
    "jet_yield",
}


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


def _reported_unit(series_name: str) -> str:
    match = re.search(r"\(([^()]*)\)\s*$", series_name)
    return match.group(1).strip() if match else ""


def _canonical_unit_status(concept: str, unit: str) -> tuple[str, str]:
    lowered = unit.lower()
    if concept in STOCK_CONCEPTS:
        valid = "barrel" in lowered and "per day" not in lowered
        return ("canonical", "stock_level") if valid else ("noncanonical", "stock_requires_level_unit")
    if concept in RATE_CONCEPTS:
        valid = "per day" in lowered
        return ("canonical", "daily_rate") if valid else ("noncanonical", "flow_requires_daily_rate")
    if concept in PERCENT_CONCEPTS:
        valid = "percent" in lowered or not unit
        return ("canonical", "percentage") if valid else ("noncanonical", "state_requires_percentage")
    if concept == "crude_quality":
        valid = any(token in lowered for token in ("degree", "percent"))
        return ("canonical", "quality_measure") if valid else ("noncanonical", "quality_unit_unrecognized")
    if concept == "refinery_capacity":
        valid = "per day" in lowered or "calendar day" in lowered
        return ("canonical", "capacity_rate") if valid else ("noncanonical", "capacity_unit_unrecognized")
    return "not_applicable", "unit_not_gated"


def review_eia_series_candidate(row: dict[str, str]) -> dict[str, str]:
    route = row["route"]
    concept = row["economic_concept"]
    geography = row["geography"]
    candidate_type = row["candidate_type"]
    unit = _reported_unit(row["series_name"])
    unit_status, unit_reason = _canonical_unit_status(concept, unit)
    state_family = STATE_FAMILY.get(concept, "unassigned")

    if candidate_type == "dataset_scope":
        return {
            "state_family": state_family,
            "reported_unit": unit,
            "canonical_unit_status": unit_status,
            "decision": "defer",
            "decision_reason": "requires_refinery_owner_history_and_release_validation",
            "review_priority": "2",
        }
    if route in CONTEXT_ROUTES:
        return {
            "state_family": state_family,
            "reported_unit": unit,
            "canonical_unit_status": unit_status,
            "decision": "defer",
            "decision_reason": "context_or_reconciliation_route_not_primary_source",
            "review_priority": "3",
        }
    if route == "petroleum/move/wimpc/":
        return {
            "state_family": state_family,
            "reported_unit": unit,
            "canonical_unit_status": unit_status,
            "decision": "defer",
            "decision_reason": "preliminary_ranked_origin_series_requires_stability_review",
            "review_priority": "3",
        }
    if any(term in row["series_name"].lower() for term in OVER_GRANULAR_TERMS):
        return {
            "state_family": state_family,
            "reported_unit": unit,
            "canonical_unit_status": unit_status,
            "decision": "reject",
            "decision_reason": "over_granular_or_noncanonical_product_definition",
            "review_priority": "4",
        }
    if concept not in ROUTE_CONCEPTS.get(route, set()):
        return {
            "state_family": state_family,
            "reported_unit": unit,
            "canonical_unit_status": unit_status,
            "decision": "reject",
            "decision_reason": "outside_registered_route_state",
            "review_priority": "4",
        }
    if geography in {"OTHER", "REFINING_DISTRICT"}:
        return {
            "state_family": state_family,
            "reported_unit": unit,
            "canonical_unit_status": unit_status,
            "decision": "defer",
            "decision_reason": "geography_requires_company_asset_mapping",
            "review_priority": "3",
        }
    if unit_status == "noncanonical":
        return {
            "state_family": state_family,
            "reported_unit": unit,
            "canonical_unit_status": unit_status,
            "decision": "defer",
            "decision_reason": unit_reason,
            "review_priority": "3",
        }
    if row["release_product"] == "PSM":
        primary_geographies = {"PADD_2", "PADD_3", "PADD_4"}
        primary_structural_states = {
            "crude_slate",
            "complexity_use",
            "product_slate",
            "refinery_operating_pressure",
        }
        review_priority = (
            "1"
            if geography in primary_geographies
            and state_family in primary_structural_states
            and concept != "refinery_throughput"
            else "2"
        )
    else:
        primary_geographies = {"US", "PADD_2", "PADD_3", "PADD_4", "CUSHING"}
        review_priority = "1" if geography in primary_geographies else "2"
    return {
        "state_family": state_family,
        "reported_unit": unit,
        "canonical_unit_status": unit_status,
        "decision": "keep",
        "decision_reason": "canonical_series_for_registered_state",
        "review_priority": review_priority,
    }


def build_eia_series_shortlist(
    *,
    candidates_path: Path = Path("data/external/eia/catalog/series_candidates.csv"),
    output_path: Path = Path("config/eia_series_shortlist.csv"),
    audit_output_path: Path = Path("data/external/eia/catalog/series_shortlist_audit.csv"),
    manifest_dir: Path = Path("data/external/eia/manifests"),
) -> dict[str, Any]:
    candidates = _read_csv(Path(candidates_path))
    if not candidates:
        raise ValueError(f"EIA series candidates are empty or missing: {candidates_path}")
    reviewed_at = _iso_utc()
    source_checksum = _file_checksum(Path(candidates_path))
    reviewed: list[dict[str, Any]] = []
    for row in candidates:
        decision = review_eia_series_candidate(row)
        candidate_route_rank = int(row.get("route_rank", "999") or 999)
        initial_rank_limit = 15 if row["release_product"] == "WPSR" else 20
        proposed_initial_core = (
            decision["decision"] == "keep"
            and decision["review_priority"] == "1"
            and candidate_route_rank <= initial_rank_limit
        )
        reviewed.append(
            {
                "schema_version": EIA_SERIES_SHORTLIST_SCHEMA_VERSION,
                "reviewed_at": reviewed_at,
                "candidate_type": row["candidate_type"],
                "route": row["route"],
                "canonical_dataset_key": row["canonical_dataset_key"],
                "release_product": row["release_product"],
                "route_priority": row["route_priority"],
                "expected_frequency": row["expected_frequency"],
                "candidate_route_rank": candidate_route_rank,
                "series_id": row["series_id"],
                "series_name": row["series_name"],
                "economic_concept": row["economic_concept"],
                **decision,
                "geography": row["geography"],
                "strategy_tags": row["strategy_tags"],
                "candidate_assets": row["candidate_assets"],
                "point_in_time_status": expected_point_in_time_status(row["release_product"]),
                "proposed_initial_core": proposed_initial_core,
                "approved_for_backfill": False,
                "revision_overlap_periods": row["revision_overlap_periods"],
                "reviewer": "comm-ls-policy-v1",
                "source_candidate_checksum": source_checksum,
            }
        )
    reviewed.sort(
        key=lambda row: (
            {"keep": 0, "defer": 1, "reject": 2}[str(row["decision"])],
            int(row["review_priority"]),
            int(row["route_priority"]),
            str(row["route"]),
            str(row["series_id"]),
        )
    )
    _atomic_write_csv(Path(output_path), reviewed, SHORTLIST_COLUMNS)

    audit_groups: dict[tuple[str, str, str], int] = {}
    for row in reviewed:
        key = (str(row["release_product"]), str(row["route"]), str(row["decision"]))
        audit_groups[key] = audit_groups.get(key, 0) + 1
    audit_rows = [
        {
            "schema_version": EIA_SERIES_SHORTLIST_SCHEMA_VERSION,
            "reviewed_at": reviewed_at,
            "release_product": key[0],
            "route": key[1],
            "decision": key[2],
            "row_count": count,
        }
        for key, count in sorted(audit_groups.items())
    ]
    audit_columns = ["schema_version", "reviewed_at", "release_product", "route", "decision", "row_count"]
    _atomic_write_csv(Path(audit_output_path), audit_rows, audit_columns)

    run_id = datetime.fromisoformat(reviewed_at.replace("Z", "+00:00")).strftime("%Y%m%dT%H%M%S%fZ")
    result = {
        "schema_version": EIA_SERIES_SHORTLIST_SCHEMA_VERSION,
        "run_id": run_id,
        "reviewed_at": reviewed_at,
        "row_count": len(reviewed),
        "keep_count": sum(row["decision"] == "keep" for row in reviewed),
        "defer_count": sum(row["decision"] == "defer" for row in reviewed),
        "reject_count": sum(row["decision"] == "reject" for row in reviewed),
        "proposed_initial_core_count": sum(bool(row["proposed_initial_core"]) for row in reviewed),
        "approved_for_backfill_count": 0,
        "network_requests": 0,
        "observation_rows_downloaded": 0,
        "inputs": {str(candidates_path): source_checksum},
        "output_path": str(output_path),
        "output_sha256": _file_checksum(Path(output_path)),
        "audit_output_path": str(audit_output_path),
        "audit_output_sha256": _file_checksum(Path(audit_output_path)),
    }
    manifest_path = Path(manifest_dir) / f"series_shortlist_{run_id}_summary.json"
    result["manifest_path"] = str(manifest_path)
    _atomic_write_json(manifest_path, result)
    return result
