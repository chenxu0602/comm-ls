from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from comm_ls.data_access import _read_frame
from comm_ls.trigger import detect_trigger


def _write_frame(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix == ".parquet":
        df.to_parquet(output_path, index=False)
    elif output_path.suffix == ".csv":
        df.to_csv(output_path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")


def _bool_from_any(value: object, default: bool = False) -> bool:
    if pd.isna(value):
        return default
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def _latest_shortability(shortability: pd.DataFrame, tickers: set[str], as_of_date: str) -> pd.DataFrame:
    if shortability.empty:
        return pd.DataFrame(columns=["ticker", "shortability_date", "can_short", "ssr_active", "adv_63d"])
    out = shortability.copy()
    out["date"] = pd.to_datetime(out["date"], utc=False)
    out["ticker"] = out["ticker"].astype(str).str.upper().str.strip()
    out = out[(out["ticker"].isin(tickers)) & (out["date"] <= pd.Timestamp(as_of_date))].copy()
    if out.empty:
        return pd.DataFrame(columns=["ticker", "shortability_date", "can_short", "ssr_active", "adv_63d"])
    out = out.sort_values(["ticker", "date"]).groupby("ticker", as_index=False).tail(1).copy()
    out = out.rename(columns={"date": "shortability_date"})
    keep = ["ticker", "shortability_date", "can_short", "ssr_active", "adv_63d", "borrow_fee_rate", "hard_to_borrow"]
    for col in keep:
        if col not in out.columns:
            out[col] = np.nan
    return out[keep].reset_index(drop=True)


def _join_falsification(candidates: pd.DataFrame, falsification: pd.DataFrame) -> pd.DataFrame:
    if falsification.empty:
        out = candidates.copy()
        out["falsification_verdict"] = "missing"
        out["falsification_flags"] = pd.NA
        out["peer_breadth_multiplier"] = np.nan
        out["peer_breadth_count"] = np.nan
        out["peer_same_direction_share"] = np.nan
        return out

    audit = falsification.copy()
    audit["ticker"] = audit["ticker"].astype(str).str.upper().str.strip()
    audit["commodity"] = audit["commodity"].astype(str).str.upper().str.strip()
    audit["feature"] = audit["feature"].astype(str).str.strip()
    if "horizon_days" in audit.columns:
        audit["preferred_horizon"] = pd.to_numeric(audit["horizon_days"], errors="coerce")
    else:
        audit["preferred_horizon"] = np.nan
    audit_cols = [
        "ticker",
        "commodity",
        "feature",
        "preferred_horizon",
        "falsification_verdict",
        "falsification_flags",
        "peer_breadth_count",
        "peer_same_direction_share",
        "peer_breadth_multiplier",
    ]
    audit = audit[[col for col in audit_cols if col in audit.columns]].drop_duplicates(
        ["ticker", "commodity", "feature", "preferred_horizon"]
    )

    out = candidates.merge(
        audit,
        on=["ticker", "commodity", "feature", "preferred_horizon"],
        how="left",
    )
    out["falsification_verdict"] = out["falsification_verdict"].fillna("missing")
    if "peer_breadth_multiplier" not in out.columns:
        out["peer_breadth_multiplier"] = np.nan
    if "peer_breadth_count" not in out.columns:
        out["peer_breadth_count"] = np.nan
    if "peer_same_direction_share" not in out.columns:
        out["peer_same_direction_share"] = np.nan
    return out


def _add_candidate_peer_breadth(candidates: pd.DataFrame) -> pd.DataFrame:
    out = candidates.copy()
    if "exposure_role" not in out.columns or "feature_family" not in out.columns:
        out["candidate_peer_breadth_count"] = np.nan
        out["candidate_peer_same_direction_share"] = np.nan
        out["candidate_peer_breadth_multiplier"] = 1.0
        return out

    mapped = out[out["exposure_role"].notna()].copy()
    mapped["direction_sign"] = pd.to_numeric(mapped.get("direction_sign"), errors="coerce")
    mapped = mapped[mapped["direction_sign"].ne(0) & mapped["direction_sign"].notna()].copy()
    if mapped.empty:
        out["candidate_peer_breadth_count"] = np.nan
        out["candidate_peer_same_direction_share"] = np.nan
        out["candidate_peer_breadth_multiplier"] = 1.0
        return out

    keys = ["commodity", "exposure_role", "feature_family", "preferred_horizon"]
    breadth = (
        mapped.groupby(keys, dropna=False)
        .agg(
            candidate_peer_breadth_count=("ticker", "nunique"),
            peer_positive=("direction_sign", lambda s: int((s > 0).sum())),
            peer_negative=("direction_sign", lambda s: int((s < 0).sum())),
        )
        .reset_index()
    )
    breadth["candidate_peer_same_direction_share"] = breadth[["peer_positive", "peer_negative"]].max(axis=1) / breadth[
        "candidate_peer_breadth_count"
    ]
    breadth["candidate_peer_breadth_multiplier"] = np.select(
        [
            (breadth["candidate_peer_breadth_count"] >= 5) & (breadth["candidate_peer_same_direction_share"] >= 0.8),
            (breadth["candidate_peer_breadth_count"] >= 3) & (breadth["candidate_peer_same_direction_share"] >= 0.7),
            (breadth["candidate_peer_breadth_count"] >= 3) & (breadth["candidate_peer_same_direction_share"] >= 0.6),
        ],
        [1.50, 1.30, 1.15],
        default=1.0,
    )
    out = out.merge(
        breadth[
            keys
            + [
                "candidate_peer_breadth_count",
                "candidate_peer_same_direction_share",
                "candidate_peer_breadth_multiplier",
            ]
        ],
        on=keys,
        how="left",
    )
    out["candidate_peer_breadth_multiplier"] = out["candidate_peer_breadth_multiplier"].fillna(1.0)
    return out


def build_precision_event_candidates(
    candidates: pd.DataFrame,
    commodity_signals: pd.DataFrame,
    exposure_map: pd.DataFrame,
    role_taxonomy: pd.DataFrame,
    as_of_date: str,
    falsification_audit: pd.DataFrame | None = None,
    shortability: pd.DataFrame | None = None,
    require_trigger: bool = True,
    allow_low_priority_roles: bool = False,
    max_names: int | None = None,
) -> pd.DataFrame:
    if candidates.empty:
        return candidates.copy()

    rows = candidates.copy()
    rows["ticker"] = rows["ticker"].astype(str).str.upper().str.strip()
    rows["commodity"] = rows["commodity"].astype(str).str.upper().str.strip()
    rows["feature"] = rows["feature"].astype(str).str.strip()
    rows["preferred_horizon"] = pd.to_numeric(rows.get("preferred_horizon"), errors="coerce")
    rows["direction_sign"] = pd.to_numeric(rows.get("direction_sign"), errors="coerce")

    exposure = exposure_map.copy()
    exposure["ticker"] = exposure["ticker"].astype(str).str.upper().str.strip()
    exposure["commodity"] = exposure["commodity"].astype(str).str.upper().str.strip()
    exposure["exposure_role"] = exposure["exposure_role"].astype(str).str.strip()
    exposure["prior_weight"] = pd.to_numeric(exposure["prior_weight"], errors="coerce")
    rows = rows.merge(
        exposure[["ticker", "commodity", "exposure_role", "prior_weight"]].drop_duplicates(["ticker", "commodity"]),
        on=["ticker", "commodity"],
        how="left",
    )

    taxonomy = role_taxonomy.copy()
    taxonomy["commodity"] = taxonomy["commodity"].astype(str).str.upper().str.strip()
    taxonomy["exposure_role"] = taxonomy["exposure_role"].astype(str).str.strip()
    taxonomy["deployable_default"] = taxonomy["deployable_default"].map(_bool_from_any)
    rows = rows.merge(
        taxonomy[
            [
                "commodity",
                "exposure_role",
                "taxonomy_bucket",
                "economic_channel",
                "alpha_priority",
                "deployable_default",
            ]
        ],
        on=["commodity", "exposure_role"],
        how="left",
    )

    rows = _join_falsification(rows, falsification_audit if falsification_audit is not None else pd.DataFrame())
    rows = _add_candidate_peer_breadth(rows)

    trigger_rows: list[dict[str, object]] = []
    for commodity in sorted(rows["commodity"].dropna().unique()):
        trigger = detect_trigger(commodity_signals, commodity=commodity, as_of_date=as_of_date)
        trigger_rows.append(
            {
                "commodity": commodity,
                "triggered": trigger.triggered,
                "trigger_direction": trigger.direction,
                "trigger_strength": trigger.strength,
                "trigger_notes": "; ".join(trigger.notes),
            }
        )
    trigger_frame = pd.DataFrame(trigger_rows)
    rows = rows.merge(trigger_frame, on="commodity", how="left")
    rows["trigger_gate_pass"] = rows["triggered"].fillna(False).astype(bool) | (not require_trigger)

    trigger_sign = rows["trigger_direction"].map({"bullish": 1.0, "bearish": -1.0}).fillna(0.0)
    rows["trade_direction_sign"] = np.sign(trigger_sign * rows["direction_sign"].fillna(0.0))
    rows["trade_side"] = np.select(
        [rows["trade_direction_sign"] > 0, rows["trade_direction_sign"] < 0],
        ["long", "short"],
        default="none",
    )

    rows["economic_channel_gate_pass"] = (
        rows["exposure_role"].notna()
        & rows["deployable_default"].fillna(False).astype(bool)
        & (allow_low_priority_roles | rows["alpha_priority"].isin(["high", "medium"]))
    )
    rows["falsification_gate_pass"] = ~rows["falsification_verdict"].eq("reject_or_retest")

    if shortability is not None and not shortability.empty:
        short = _latest_shortability(shortability, set(rows["ticker"]), as_of_date=as_of_date)
        rows = rows.merge(short, on="ticker", how="left")
    else:
        rows["shortability_date"] = pd.NaT
        rows["can_short"] = np.nan
        rows["ssr_active"] = np.nan
        rows["adv_63d"] = np.nan
        rows["borrow_fee_rate"] = np.nan
        rows["hard_to_borrow"] = np.nan

    can_short = rows["can_short"].map(lambda value: _bool_from_any(value, default=False))
    ssr_active = rows["ssr_active"].map(lambda value: _bool_from_any(value, default=False))
    rows["execution_gate_pass"] = np.where(
        rows["trade_side"].eq("short"),
        np.where(rows["can_short"].isna(), True, can_short & ~ssr_active),
        rows["trade_side"].eq("long"),
    )

    hard_gates = ["trigger_gate_pass", "economic_channel_gate_pass", "falsification_gate_pass", "execution_gate_pass"]
    rows["failed_precision_gates"] = rows[hard_gates].apply(
        lambda row: ",".join([col.removesuffix("_gate_pass") for col, value in row.items() if not bool(value)]),
        axis=1,
    )

    review_flags = []
    for _, row in rows.iterrows():
        flags: list[str] = []
        if row.get("falsification_verdict") == "missing":
            flags.append("missing_falsification_audit")
        if row.get("falsification_verdict") == "review":
            flags.append("falsification_review")
        if row.get("trade_side") == "short" and pd.isna(row.get("can_short")):
            flags.append("manual_borrow_check")
        if pd.to_numeric(pd.Series([row.get("candidate_peer_breadth_count")]), errors="coerce").iloc[0] < 3:
            flags.append("weak_peer_breadth")
        if row.get("alpha_priority") == "low":
            flags.append("low_priority_role")
        review_flags.append(",".join(flags))
    rows["precision_review_flags"] = review_flags

    base = pd.to_numeric(rows.get("candidate_priority"), errors="coerce")
    if base.isna().all():
        base = pd.to_numeric(rows.get("quality_score"), errors="coerce") / 250.0
    base = base.fillna(0.25).clip(lower=0.0, upper=1.5)
    role_mult = rows["alpha_priority"].map({"high": 1.0, "medium": 0.85, "low": 0.65}).fillna(0.4)
    fals_mult = rows["falsification_verdict"].map({"pass": 1.0, "review": 0.8, "missing": 0.7}).fillna(0.0)
    trigger_mult = rows["trigger_strength"].map({"full": 1.15, "standard": 1.0, "none": 0.0}).fillna(0.0)
    peer_mult = pd.to_numeric(rows["peer_breadth_multiplier"], errors="coerce").fillna(
        pd.to_numeric(rows["candidate_peer_breadth_multiplier"], errors="coerce")
    ).fillna(1.0)
    gate_mult = rows[hard_gates].all(axis=1).map({True: 1.0, False: 0.0})
    rows["precision_score"] = base * role_mult * fals_mult * trigger_mult * peer_mult * gate_mult

    rows["precision_verdict"] = np.select(
        [
            rows[hard_gates].all(axis=1) & rows["precision_review_flags"].eq(""),
            rows[hard_gates].all(axis=1),
        ],
        ["deployable_candidate", "review_candidate"],
        default="blocked",
    )

    verdict_rank = {"deployable_candidate": 0, "review_candidate": 1, "blocked": 2}
    rows["_precision_verdict_rank"] = rows["precision_verdict"].map(verdict_rank).fillna(9).astype(int)
    rows = rows.sort_values(
        ["_precision_verdict_rank", "precision_score", "candidate_priority"],
        ascending=[True, False, False],
    ).drop(columns=["_precision_verdict_rank"]).reset_index(drop=True)
    if max_names is not None and max_names > 0:
        rows = rows.head(max_names).copy()
    return rows


def build_precision_event_candidates_from_paths(
    candidates_path: Path,
    commodity_signals_path: Path,
    exposure_map_path: Path,
    role_taxonomy_path: Path,
    output_path: Path,
    as_of_date: str,
    falsification_audit_path: Path | None = None,
    shortability_path: Path | None = None,
    require_trigger: bool = True,
    allow_low_priority_roles: bool = False,
    max_names: int | None = None,
) -> pd.DataFrame:
    falsification = (
        _read_frame(falsification_audit_path)
        if falsification_audit_path is not None and falsification_audit_path.exists()
        else None
    )
    shortability = (
        _read_frame(shortability_path)
        if shortability_path is not None and shortability_path.exists()
        else None
    )
    out = build_precision_event_candidates(
        candidates=_read_frame(candidates_path),
        commodity_signals=_read_frame(commodity_signals_path),
        exposure_map=pd.read_csv(exposure_map_path),
        role_taxonomy=pd.read_csv(role_taxonomy_path),
        falsification_audit=falsification,
        shortability=shortability,
        as_of_date=as_of_date,
        require_trigger=require_trigger,
        allow_low_priority_roles=allow_low_priority_roles,
        max_names=max_names,
    )
    _write_frame(out, output_path)
    return out
