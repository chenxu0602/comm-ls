from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from comm_ls.reaction import load_frame
from comm_ls.year_stability import _extract_signed_returns, _t_stat


def _write_frame(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix == ".parquet":
        df.to_parquet(output_path, index=False)
    elif output_path.suffix == ".csv":
        df.to_csv(output_path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")


def _direction(row: pd.Series) -> float:
    if "direction_sign" in row.index and pd.notna(row["direction_sign"]):
        v = float(pd.to_numeric(row["direction_sign"], errors="coerce"))
        if v != 0:
            return float(np.sign(v))
    beta = row.get("median_nonoverlap_beta_per_1z", row.get("median_beta_per_1z", np.nan))
    return float(np.sign(beta)) if pd.notna(beta) and float(beta) != 0 else 1.0


def build_peer_expansion(
    primary_candidates: pd.DataFrame,
    selected_features: pd.DataFrame,
    cache: pd.DataFrame,
    commodity: str | None = None,
    return_column: str = "residual_return_mktsec_w12m",
    activation_z: float = 1.5,
    min_peer_nonoverlap_abs_t: float = 1.0,
    min_peer_events: int = 10,
    min_peer_event_sum: float = 0.0,
) -> pd.DataFrame:
    if primary_candidates.empty or selected_features.empty:
        return pd.DataFrame()

    cache = cache.copy()
    cache["ticker"] = cache["ticker"].astype(str).str.upper().str.strip()
    cache["commodity"] = cache["commodity"].astype(str).str.upper().str.strip()
    cache["date"] = pd.to_datetime(cache["date"], utc=False)

    sf = selected_features.copy()
    sf["ticker"] = sf["ticker"].astype(str).str.upper().str.strip()
    sf["commodity"] = sf["commodity"].astype(str).str.upper().str.strip()
    if "target_return_column" in sf.columns:
        sf = sf[sf["target_return_column"].astype(str).eq(return_column)].copy()
    if commodity:
        sf = sf[sf["commodity"].eq(commodity.upper())].copy()

    primary = primary_candidates.copy()
    primary["ticker"] = primary["ticker"].astype(str).str.upper().str.strip()
    primary_tickers = set(primary["ticker"].unique())

    peer_groups: dict[tuple[str, str], set[str]] = {}
    for _, r in primary.iterrows():
        state = str(r.get("state_hypothesis", ""))
        role = str(r.get("exposure_role", ""))
        if not state or not role:
            continue
        key = (state, role)
        if key not in peer_groups:
            peer_groups[key] = set()
        peer_groups[key].add(r["ticker"])

    rows: list[dict[str, object]] = []
    for (state, role), primaries in sorted(peer_groups.items()):
        peers = sf[
            (sf["state_hypothesis"].astype(str).eq(state))
            & (sf["exposure_role"].astype(str).eq(role))
            & (~sf["ticker"].isin(primary_tickers))
        ].copy()
        if peers.empty:
            continue

        peers["_tnon"] = pd.to_numeric(peers["median_nonoverlap_abs_t_stat"], errors="coerce")
        peers = peers[peers["_tnon"] >= min_peer_nonoverlap_abs_t]
        peers = peers[peers["selection_verdict"].isin(["keep", "weak_keep"])]
        peers = peers[peers["commodity_neutral_selection_verdict"].ne("block")]
        if peers.empty:
            continue

        peer_tickers = sorted(peers["ticker"].unique())
        for ticker in peer_tickers:
            sub = peers[peers["ticker"] == ticker].copy()
            best_t = -999.0
            best_row: dict[str, object] = {}
            for _, p in sub.iterrows():
                feat = str(p["feature"])
                h = int(p["horizon_days"])
                d = _direction(p)
                ccode = str(p["commodity"])
                signed = _extract_signed_returns(cache, ticker, ccode, feat, d, return_column, h, activation_z)
                if signed.empty:
                    continue
                n = len(signed)
                s = float(signed["signed_return"].sum())
                t = float(_t_stat(signed["signed_return"]))
                if n < min_peer_events or s <= min_peer_event_sum:
                    continue
                if t > best_t:
                    best_t = t
                    best_row = {
                        "ticker": ticker,
                        "commodity": ccode,
                        "feature": feat,
                        "state_hypothesis": state,
                        "feature_family": str(p.get("feature_family", "")),
                        "exposure_role": role,
                        "horizon_days": h,
                        "direction_sign": d,
                        "activation_z": activation_z,
                        "return_column": return_column,
                        "matrix_nonoverlap_abs_t_stat": float(p["_tnon"]),
                        "matrix_selection_score": float(p["selection_score"]),
                        "matrix_selection_verdict": str(p["selection_verdict"]),
                        "events": n,
                        "event_sum_return": s,
                        "event_t_stat": t,
                        "event_hit_rate": float((signed["signed_return"] > 0).mean()),
                        "peer_group_state": state,
                        "peer_group_role": role,
                        "peer_group_primaries": "+".join(sorted(primaries)),
                    }
            if best_row:
                rows.append(best_row)

    if not rows:
        return pd.DataFrame()
    out = pd.DataFrame(rows).sort_values("event_t_stat", ascending=False).reset_index(drop=True)
    front = [
        "ticker", "commodity", "feature", "state_hypothesis", "exposure_role",
        "horizon_days", "direction_sign", "peer_group_primaries",
        "event_t_stat", "event_sum_return", "events", "event_hit_rate",
        "matrix_nonoverlap_abs_t_stat", "matrix_selection_score", "matrix_selection_verdict",
    ]
    cols = [c for c in front if c in out.columns] + [c for c in out.columns if c not in front]
    return out[cols]


def build_peer_expansion_from_paths(
    candidates_path: Path,
    selected_features_path: Path,
    cache_path: Path,
    output_path: Path | None = None,
    commodity: str | None = None,
    return_column: str = "residual_return_mktsec_w12m",
    activation_z: float = 1.5,
    min_peer_nonoverlap_abs_t: float = 1.0,
    min_peer_events: int = 10,
    min_peer_event_sum: float = 0.0,
) -> pd.DataFrame:
    primary = load_frame(candidates_path)
    sf = load_frame(selected_features_path)
    cache = load_frame(cache_path)
    peers = build_peer_expansion(
        primary_candidates=primary, selected_features=sf, cache=cache,
        commodity=commodity, return_column=return_column, activation_z=activation_z,
        min_peer_nonoverlap_abs_t=min_peer_nonoverlap_abs_t,
        min_peer_events=min_peer_events, min_peer_event_sum=min_peer_event_sum,
    )
    if output_path is not None:
        _write_frame(peers, output_path)
    return peers
