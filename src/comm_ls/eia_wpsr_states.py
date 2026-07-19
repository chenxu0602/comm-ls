from __future__ import annotations

import csv
import hashlib
from datetime import date, datetime, time, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
from pandas.tseries.holiday import (
    AbstractHolidayCalendar,
    GoodFriday,
    Holiday,
    USLaborDay,
    USMartinLutherKingJr,
    USMemorialDay,
    USPresidentsDay,
    USThanksgivingDay,
    nearest_workday,
)
from pandas.tseries.offsets import CustomBusinessDay


WPSR_SILVER_SCHEMA_VERSION = "1"

SILVER_COLUMNS = [
    "schema_version",
    "canonical_dataset_key",
    "release_product",
    "series_id",
    "series_name",
    "state_family",
    "geography",
    "archive_row_key",
    "observation_period",
    "observation_period_semantics",
    "source_vintage",
    "release_ts",
    "first_seen_ts",
    "known_at",
    "tradable_after",
    "value",
    "unit",
    "revision_number",
    "is_latest_vintage",
    "point_in_time_available",
    "timestamp_quality",
    "source_table_checksum",
    "source_review_checksum",
    "row_hash",
]

GOLD_COLUMNS = [
    "schema_version",
    "release_product",
    "feature_id",
    "feature_version",
    "series_id",
    "series_name",
    "state_family",
    "geography",
    "observation_period",
    "source_vintage",
    "known_at",
    "tradable_after",
    "value",
    "change_1_release",
    "change_4_releases",
    "seasonal_mean_prior",
    "seasonal_std_prior",
    "seasonal_z",
    "physical_state_value",
    "physical_state_direction",
    "seasonal_observation_count",
    "point_in_time_available",
    "source_row_hash",
]


class _NyseHolidayCalendar(AbstractHolidayCalendar):
    rules = [
        Holiday("New Year's Day", month=1, day=1, observance=nearest_workday),
        USMartinLutherKingJr,
        USPresidentsDay,
        GoodFriday,
        USMemorialDay,
        Holiday(
            "Juneteenth National Independence Day",
            month=6,
            day=19,
            start_date="2022-06-19",
            observance=nearest_workday,
        ),
        Holiday("Independence Day", month=7, day=4, observance=nearest_workday),
        USLaborDay,
        USThanksgivingDay,
        Holiday("Christmas Day", month=12, day=25, observance=nearest_workday),
    ]


_NYSE_BUSINESS_DAY = CustomBusinessDay(calendar=_NyseHolidayCalendar())


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


def _iso_utc(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _release_timestamp(
    release_date: str,
    release_metadata: dict[str, str] | None = None,
) -> tuple[datetime, str]:
    eastern = ZoneInfo("America/New_York")
    release_day = date.fromisoformat(release_date)
    official_time = (release_metadata or {}).get("official_release_time", "").strip()
    if official_time:
        parsed_time = time.fromisoformat(official_time)
        return (
            datetime.combine(release_day, parsed_time, tzinfo=eastern),
            "official_archived_release_date_and_reviewed_time",
        )
    if release_day.weekday() == 2:
        return (
            datetime.combine(release_day, time(10, 30), tzinfo=eastern),
            "official_archived_release_date_standard_wednesday_time",
        )
    return (
        datetime.combine(release_day, time(23, 59, 59), tzinfo=eastern),
        "official_archived_release_date_conservative_end_of_day",
    )


def _load_session_dates(path: Path) -> list[date]:
    if not path.exists():
        return []
    if path.suffix.lower() == ".parquet":
        frame = pd.read_parquet(path, columns=["date"])
        values = pd.to_datetime(frame["date"], errors="coerce").dropna().dt.date
        return sorted(set(values))
    rows = _read_csv(path)
    return sorted(
        {
            pd.Timestamp(row.get("session_date") or row.get("date")).date()
            for row in rows
            if row.get("session_date") or row.get("date")
        }
    )


def _tradable_after(release_ts: datetime, sessions: list[date]) -> str:
    next_session = next((session for session in sessions if session > release_ts.date()), None)
    if next_session is None:
        next_session = (pd.Timestamp(release_ts.date()) + _NYSE_BUSINESS_DAY).date()
    eastern = ZoneInfo("America/New_York")
    return _iso_utc(datetime.combine(next_session, time(9, 30), tzinfo=eastern))


def _transform_archive_value(value: float, relation: str) -> float:
    if relation == "exact":
        return value
    if relation == "api_div_1000":
        return value * 1000.0
    if relation == "api_mul_1000":
        return value / 1000.0
    raise ValueError(f"Unsupported WPSR numeric relation: {relation}")


def _row_hash(row: dict[str, Any]) -> str:
    payload = "|".join(str(row.get(column, "")) for column in SILVER_COLUMNS[:-1])
    return hashlib.sha256(payload.encode()).hexdigest()


def build_wpsr_silver(
    *,
    crosswalk_path: Path = Path("config/eia_wpsr_crosswalk.csv"),
    archive_releases_path: Path = Path(
        "data/external/eia/wpsr_archive/wpsr_archive_releases.csv"
    ),
    archive_values_path: Path = Path(
        "data/external/eia/wpsr_archive/wpsr_archive_values.csv"
    ),
    release_dates_path: Path = Path("config/eia_wpsr_release_dates.csv"),
    session_dates_path: Path = Path("data/processed/equity_processed.parquet"),
    vintage_output_path: Path = Path("data/processed/eia/observations_vintage.csv"),
    latest_output_path: Path = Path("data/processed/eia/observations_latest.csv"),
) -> dict[str, Any]:
    crosswalk = _read_csv(Path(crosswalk_path))
    releases = _read_csv(Path(archive_releases_path))
    values = _read_csv(Path(archive_values_path))
    release_dates = _read_csv(Path(release_dates_path))
    sessions = _load_session_dates(Path(session_dates_path))
    if not Path(crosswalk_path).exists():
        raise FileNotFoundError(crosswalk_path)
    if crosswalk and (not releases or not values):
        raise ValueError("Approved WPSR crosswalk requires archive releases and values")

    release_index = {
        row.get("requested_release_date", ""): row
        for row in releases
        if row.get("status") == "ok"
    }
    release_metadata_index = {
        row.get("release_date", ""): row for row in release_dates if row.get("release_date")
    }
    map_index = {row.get("archive_row_key", ""): row for row in crosswalk}
    output: list[dict[str, Any]] = []
    for value_row in values:
        mapping = map_index.get(value_row.get("row_key", ""))
        release = release_index.get(value_row.get("release_date", ""))
        if mapping is None or release is None or value_row.get("value_numeric", "") == "":
            continue
        release_ts, timestamp_quality = _release_timestamp(
            value_row["release_date"],
            release_metadata_index.get(value_row["release_date"]),
        )
        first_seen = release.get("fetched_at", "")
        row = {
            "schema_version": WPSR_SILVER_SCHEMA_VERSION,
            "canonical_dataset_key": mapping["canonical_dataset_key"],
            "release_product": "WPSR",
            "series_id": mapping["series_id"],
            "series_name": mapping["series_name"],
            "state_family": mapping["state_family"],
            "geography": mapping["geography"],
            "archive_row_key": mapping["archive_row_key"],
            "observation_period": value_row["observation_date"],
            "observation_period_semantics": "week_ending_friday_0700_America/New_York",
            "source_vintage": value_row["release_date"],
            "release_ts": _iso_utc(release_ts),
            "first_seen_ts": first_seen,
            "known_at": _iso_utc(release_ts),
            "tradable_after": _tradable_after(release_ts, sessions),
            "value": _transform_archive_value(
                float(value_row["value_numeric"]), mapping["numeric_relation"]
            ),
            "unit": mapping["api_unit"],
            "revision_number": 0,
            "is_latest_vintage": False,
            "point_in_time_available": True,
            "timestamp_quality": timestamp_quality,
            "source_table_checksum": value_row.get("source_table_checksum", ""),
            "source_review_checksum": mapping.get("source_review_checksum", ""),
        }
        row["row_hash"] = _row_hash(row)
        output.append(row)

    output.sort(
        key=lambda row: (row["series_id"], row["observation_period"], row["source_vintage"])
    )
    groups: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for row in output:
        groups.setdefault((row["series_id"], row["observation_period"]), []).append(row)
    latest: list[dict[str, Any]] = []
    for rows in groups.values():
        for revision, row in enumerate(rows):
            row["revision_number"] = revision
            row["is_latest_vintage"] = revision == len(rows) - 1
            row["row_hash"] = _row_hash(row)
        latest.append(rows[-1])

    duplicate_count = len(output) - len(
        {
            (row["series_id"], row["observation_period"], row["source_vintage"])
            for row in output
        }
    )
    if duplicate_count:
        raise ValueError(f"Duplicate WPSR Silver primary keys: {duplicate_count}")
    missing_tradable_after = sum(not row["tradable_after"] for row in output)
    _atomic_write_csv(Path(vintage_output_path), output, SILVER_COLUMNS)
    _atomic_write_csv(
        Path(latest_output_path),
        sorted(latest, key=lambda row: (row["series_id"], row["observation_period"])),
        SILVER_COLUMNS,
    )
    return {
        "crosswalk_count": len(crosswalk),
        "vintage_row_count": len(output),
        "latest_row_count": len(latest),
        "missing_tradable_after_count": missing_tradable_after,
        "duplicate_count": duplicate_count,
        "vintage_output_path": str(vintage_output_path),
        "latest_output_path": str(latest_output_path),
    }


def _prior_seasonal(values: pd.DataFrame, row: pd.Series) -> pd.Series:
    week = int(row["iso_week"])
    year = int(row["iso_year"])
    distance = (values["iso_week"] - week).abs()
    distance = np.minimum(distance, 53 - distance)
    return values[(values["iso_year"] < year) & (distance <= 2)]["value"]


def build_wpsr_gold_states(
    *,
    latest_path: Path = Path("data/processed/eia/observations_latest.csv"),
    feature_registry_path: Path = Path("config/eia_feature_registry.csv"),
    output_path: Path = Path("data/processed/eia/feature_states/wpsr_physical_states.csv"),
    min_seasonal_observations: int = 3,
) -> dict[str, Any]:
    rows = _read_csv(Path(latest_path))
    if not Path(latest_path).exists():
        raise FileNotFoundError(latest_path)
    if not rows:
        _atomic_write_csv(Path(output_path), [], GOLD_COLUMNS)
        return {"input_row_count": 0, "output_row_count": 0, "output_path": str(output_path)}

    registry = {
        row.get("economic_state", ""): row
        for row in _read_csv(Path(feature_registry_path))
        if row.get("release_product") == "WPSR"
        and row.get("status") == "research_physical_state_only"
    }
    if not registry:
        raise ValueError(f"No active WPSR physical states found: {feature_registry_path}")

    frame = pd.DataFrame(rows)
    frame["value"] = pd.to_numeric(frame["value"], errors="coerce")
    frame["observation_period"] = pd.to_datetime(frame["observation_period"])
    iso = frame["observation_period"].dt.isocalendar()
    frame["iso_year"] = iso.year.astype(int)
    frame["iso_week"] = iso.week.astype(int)
    output: list[dict[str, Any]] = []
    for _, group in frame.groupby("series_id", sort=True):
        group = group.sort_values(["known_at", "observation_period"]).copy()
        group["change_1_release"] = group["value"].diff(1)
        group["change_4_releases"] = group["value"].diff(4)
        for _, row in group.iterrows():
            feature = registry.get(row["state_family"])
            if feature is None:
                continue
            prior = _prior_seasonal(group, row).dropna()
            mean = float(prior.mean()) if len(prior) else np.nan
            std = float(prior.std(ddof=1)) if len(prior) > 1 else np.nan
            z = (
                float((row["value"] - mean) / std)
                if len(prior) >= min_seasonal_observations and std > 0
                else np.nan
            )
            direction = "unsigned_physical_state"
            physical_value = z
            if row["state_family"] == "inventory_tightness" and not np.isnan(z):
                physical_value = -z
                direction = "higher_means_tighter_inventory"
            elif row["state_family"] == "refinery_operating_pressure":
                direction = "higher_means_higher_utilization_or_input_pressure"
            elif row["state_family"] == "product_demand":
                direction = "higher_means_stronger_reported_product_demand"
            output.append(
                {
                    "schema_version": WPSR_SILVER_SCHEMA_VERSION,
                    "release_product": "WPSR",
                    "feature_id": feature["feature_id"],
                    "feature_version": feature["feature_version"],
                    "series_id": row["series_id"],
                    "series_name": row["series_name"],
                    "state_family": row["state_family"],
                    "geography": row["geography"],
                    "observation_period": row["observation_period"].date().isoformat(),
                    "source_vintage": row["source_vintage"],
                    "known_at": row["known_at"],
                    "tradable_after": row["tradable_after"],
                    "value": row["value"],
                    "change_1_release": row["change_1_release"],
                    "change_4_releases": row["change_4_releases"],
                    "seasonal_mean_prior": mean,
                    "seasonal_std_prior": std,
                    "seasonal_z": z,
                    "physical_state_value": physical_value,
                    "physical_state_direction": direction,
                    "seasonal_observation_count": len(prior),
                    "point_in_time_available": row["point_in_time_available"],
                    "source_row_hash": row["row_hash"],
                }
            )
    _atomic_write_csv(Path(output_path), output, GOLD_COLUMNS)
    return {
        "input_row_count": len(frame),
        "output_row_count": len(output),
        "seasonal_z_available_count": sum(
            not pd.isna(row["seasonal_z"]) for row in output
        ),
        "output_path": str(output_path),
    }
