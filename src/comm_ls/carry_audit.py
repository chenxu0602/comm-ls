from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

from comm_ls.carry_builder import contract_sort_key


CORE_COMPARISON_COLUMNS = (
    "carry",
    "contango",
    "backwardation",
    "M0_settle",
    "M1_settle",
    "M2_settle",
    "m0_ret",
    "m1_ret",
    "m2_ret",
    "total_volume",
    "total_oi",
)


def _load(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path, low_memory=False)
    if "date" not in frame.columns:
        raise ValueError(f"Carry file has no date column: {path}")
    frame["date"] = pd.to_datetime(frame["date"], errors="coerce").dt.normalize()
    return frame.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)


def _contract_rank(value: object) -> float:
    try:
        year, month = contract_sort_key(str(value))
    except (TypeError, ValueError):
        return np.nan
    return float(year * 12 + month)


def _rollback_count(frame: pd.DataFrame) -> int:
    contract_columns = [
        column
        for column in frame.columns
        if column == "M0_con" or (len(column) == 5 and column.endswith("_con"))
    ]
    count = 0
    for column in contract_columns:
        ranks = frame[column].map(_contract_rank).dropna()
        count += int(ranks.diff().lt(0).sum())
    return count


def _correlation(left: pd.Series, right: pd.Series) -> float:
    if len(left) < 2 or left.nunique() < 2 or right.nunique() < 2:
        return np.nan
    return float(left.corr(right))


def _column_rows(
    symbol: str,
    reference: pd.DataFrame,
    candidate: pd.DataFrame,
) -> list[dict[str, object]]:
    shared = reference.merge(candidate, on="date", how="inner", suffixes=("__reference", "__candidate"))
    preferred = list(CORE_COMPARISON_COLUMNS)
    preferred.extend(
        column
        for column in candidate.columns
        if column.startswith("lis_carry_")
        or column.startswith("chain_")
        or (column.startswith("calendar_") and column.endswith("_annualized_carry"))
    )
    columns = sorted(set(preferred).intersection(reference.columns).intersection(candidate.columns))
    rows: list[dict[str, object]] = []
    for column in columns:
        ref_all = pd.to_numeric(reference[column], errors="coerce")
        cand_all = pd.to_numeric(candidate[column], errors="coerce")
        ref = pd.to_numeric(shared[f"{column}__reference"], errors="coerce")
        cand = pd.to_numeric(shared[f"{column}__candidate"], errors="coerce")
        both = ref.notna() & cand.notna()
        difference = cand.loc[both] - ref.loc[both]
        rows.append(
            {
                "symbol": symbol,
                "column": column,
                "reference_non_null": int(ref_all.notna().sum()),
                "candidate_non_null": int(cand_all.notna().sum()),
                "both_non_null": int(both.sum()),
                "correlation": _correlation(ref.loc[both], cand.loc[both]),
                "median_abs_difference": float(difference.abs().median()) if not difference.empty else np.nan,
                "max_abs_difference": float(difference.abs().max()) if not difference.empty else np.nan,
            }
        )
    return rows


def _latest_rows(
    symbol: str,
    reference: pd.DataFrame,
    candidate: pd.DataFrame,
) -> list[dict[str, object]]:
    shared_dates = sorted(set(reference["date"]).intersection(candidate["date"]))
    if not shared_dates:
        return []
    date = shared_dates[-1]
    ref = reference.loc[reference["date"].eq(date)].iloc[-1]
    cand = candidate.loc[candidate["date"].eq(date)].iloc[-1]
    columns = sorted(
        set(CORE_COMPARISON_COLUMNS)
        .union({"M0_con", "M1_con", "M2_con"})
        .union(
            column
            for column in candidate.columns
            if column.startswith("lis_carry_")
            or column.startswith("chain_")
            or (column.startswith("calendar_") and column.endswith("_annualized_carry"))
        )
        .intersection(reference.columns)
        .intersection(candidate.columns)
    )
    rows: list[dict[str, object]] = []
    for column in columns:
        ref_value = ref[column]
        candidate_value = cand[column]
        ref_number = pd.to_numeric(pd.Series([ref_value]), errors="coerce").iloc[0]
        candidate_number = pd.to_numeric(pd.Series([candidate_value]), errors="coerce").iloc[0]
        difference = (
            float(candidate_number - ref_number)
            if pd.notna(ref_number) and pd.notna(candidate_number)
            else np.nan
        )
        rows.append(
            {
                "symbol": symbol,
                "date": date,
                "column": column,
                "reference_value": ref_value,
                "candidate_value": candidate_value,
                "difference": difference,
            }
        )
    return rows


def audit_carry_directories(
    *,
    reference_dir: Path,
    candidate_dir: Path,
    output_dir: Path,
    symbols: Iterable[str] | None = None,
    overwrite: bool = False,
) -> dict[str, int]:
    """Compare a shadow carry build with the operational reference directory."""
    if reference_dir.resolve() == candidate_dir.resolve():
        raise ValueError("Reference and candidate carry directories must be different")
    if output_dir.exists() and any(output_dir.iterdir()) and not overwrite:
        raise FileExistsError(f"Refusing to replace non-empty audit directory: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)

    reference_paths = {path.stem.upper(): path for path in reference_dir.glob("*.csv")}
    candidate_paths = {path.stem.upper(): path for path in candidate_dir.glob("*.csv")}
    selected_symbols = (
        sorted({str(symbol).upper().strip() for symbol in symbols})
        if symbols is not None
        else sorted(set(reference_paths).union(candidate_paths))
    )

    summary_rows: list[dict[str, object]] = []
    column_rows: list[dict[str, object]] = []
    latest_rows: list[dict[str, object]] = []
    mismatch_frames: list[pd.DataFrame] = []
    source_rows: list[dict[str, object]] = []

    for symbol in selected_symbols:
        reference_path = reference_paths.get(symbol)
        candidate_path = candidate_paths.get(symbol)
        if reference_path is None or candidate_path is None:
            summary_rows.append(
                {
                    "symbol": symbol,
                    "status": "reference_missing" if reference_path is None else "candidate_missing",
                    "reference_rows": np.nan,
                    "candidate_rows": np.nan,
                }
            )
            continue

        reference = _load(reference_path)
        candidate = _load(candidate_path)
        common_dates = sorted(set(reference["date"]).intersection(candidate["date"]))
        contract_match_count = 0
        contract_both_count = 0
        if "M0_con" in reference.columns and "M0_con" in candidate.columns:
            contracts = reference[["date", "M0_con"]].merge(
                candidate[["date", "M0_con"]],
                on="date",
                how="inner",
                suffixes=("__reference", "__candidate"),
            )
            both = contracts["M0_con__reference"].notna() & contracts["M0_con__candidate"].notna()
            contract_both_count = int(both.sum())
            matches = contracts["M0_con__reference"].eq(contracts["M0_con__candidate"])
            contract_match_count = int((both & matches).sum())
            mismatches = contracts.loc[both & ~matches].copy()
            if not mismatches.empty:
                mismatches.insert(0, "symbol", symbol)
                mismatch_frames.append(mismatches)

        numeric_candidate = candidate.select_dtypes(include=[np.number])
        summary_rows.append(
            {
                "symbol": symbol,
                "status": "compared",
                "reference_rows": len(reference),
                "candidate_rows": len(candidate),
                "reference_start": reference["date"].min(),
                "candidate_start": candidate["date"].min(),
                "reference_end": reference["date"].max(),
                "candidate_end": candidate["date"].max(),
                "common_dates": len(common_dates),
                "candidate_duplicate_dates": int(candidate["date"].duplicated().sum()),
                "candidate_infinite_values": int(np.isinf(numeric_candidate.to_numpy()).sum()),
                "candidate_contract_rollbacks": _rollback_count(candidate),
                "m0_contract_both": contract_both_count,
                "m0_contract_matches": contract_match_count,
                "m0_contract_match_rate": (
                    contract_match_count / contract_both_count if contract_both_count else np.nan
                ),
            }
        )
        column_rows.extend(_column_rows(symbol, reference, candidate))
        latest_rows.extend(_latest_rows(symbol, reference, candidate))

        source_columns = [column for column in candidate.columns if column.endswith("_source")]
        for column in source_columns:
            counts = candidate[column].astype("string").value_counts(dropna=False)
            for value, count in counts.items():
                source_rows.append(
                    {
                        "symbol": symbol,
                        "column": column,
                        "source": value,
                        "count": int(count),
                        "share": float(count / len(candidate)) if len(candidate) else np.nan,
                    }
                )

    pd.DataFrame(summary_rows).to_csv(output_dir / "summary.csv", index=False)
    pd.DataFrame(column_rows).to_csv(output_dir / "column_comparison.csv", index=False)
    pd.DataFrame(latest_rows).to_csv(output_dir / "latest_comparison.csv", index=False)
    pd.DataFrame(source_rows).to_csv(output_dir / "source_usage.csv", index=False)
    mismatches = pd.concat(mismatch_frames, ignore_index=True) if mismatch_frames else pd.DataFrame()
    mismatches.to_csv(output_dir / "m0_contract_mismatches.csv", index=False)
    return {
        "symbols": len(selected_symbols),
        "compared": sum(row["status"] == "compared" for row in summary_rows),
        "candidate_missing": sum(row["status"] == "candidate_missing" for row in summary_rows),
        "reference_missing": sum(row["status"] == "reference_missing" for row in summary_rows),
    }
