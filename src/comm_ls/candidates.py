from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from comm_ls.reaction import load_frame
from comm_ls.universe import load_seed_universe


def _economic_label(row: pd.Series) -> str:
    commodity = str(row["commodity"])
    feature = str(row["feature"])
    theme = str(row.get("theme", ""))
    role = str(row.get("role", ""))
    direction = str(row["direction"])

    if commodity == "CL" and theme == "crude" and role == "consumer" and direction == "negative":
        return "oil_up_cost_pressure"
    if commodity == "CL" and theme == "crude" and role in {"producer", "services", "midstream"} and direction == "positive":
        return "oil_up_energy_beneficiary"
    if commodity == "NG" and role in {"producer", "midstream"} and direction == "positive":
        return "gas_up_energy_beneficiary"
    if commodity in {"GC", "SI"} and theme in {"gold", "silver"}:
        return "precious_metals_linked"
    if commodity in {"HG", "SCO"} and theme in {"copper", "steel", "aluminum", "iron_ore"}:
        return "industrial_metals_linked"
    if "volume" in feature or "oi_" in feature:
        return "participation_shock"
    if "vol" in feature or "atr" in feature or "abs_ret" in feature:
        return "volatility_shock"
    if "regime" in feature or "backwardation" in feature or "contango" in feature:
        return "curve_regime"
    if "carry" in feature or "spread" in feature:
        return "curve_or_carry_proxy"
    if "ret" in feature or "breakout" in feature or "drawdown" in feature or "up_days" in feature:
        return "price_momentum"
    return "statistical_candidate"


def _confidence(row: pd.Series) -> str:
    abs_t = max(abs(row["tstat_5d"]), abs(row["tstat_10d"]), abs(row["tstat_21d"]))
    hit = row["preferred_hit_rate"]
    events = row["preferred_event_count"]
    if abs_t >= 4 and hit >= 0.65 and events >= 30:
        return "high"
    if abs_t >= 3 and hit >= 0.58 and events >= 30:
        return "medium"
    return "low"


def build_candidate_signals(
    reactions: pd.DataFrame,
    seed_universe: pd.DataFrame | None = None,
    min_events: int = 30,
    min_abs_t: float = 3.0,
    min_same_direction_horizons: int = 2,
    horizon_columns: tuple[int, int, int] = (5, 10, 21),
) -> pd.DataFrame:
    df = reactions.copy()
    df["ticker"] = df["ticker"].astype(str).str.upper().str.strip()

    if seed_universe is not None:
        meta_cols = [col for col in ["ticker", "theme", "role", "region"] if col in seed_universe.columns]
        df = df.merge(seed_universe[meta_cols].drop_duplicates("ticker"), on="ticker", how="left")

    df = df[df["event_count"] >= min_events].copy()
    if df.empty:
        return pd.DataFrame()

    index_cols = ["as_of_date", "commodity", "feature", "ticker"]
    for col in ["theme", "role", "region"]:
        if col in df.columns:
            index_cols.append(col)

    tstats = df.pivot_table(index=index_cols, columns="horizon_days", values="reaction_tstat")
    means = df.pivot_table(index=index_cols, columns="horizon_days", values="mean_signed_return")
    hits = df.pivot_table(index=index_cols, columns="horizon_days", values="hit_rate")
    events = df.pivot_table(index=index_cols, columns="horizon_days", values="event_count")
    corrs = df.pivot_table(index=index_cols, columns="horizon_days", values="feature_return_corr")

    required = list(horizon_columns)
    tstats = tstats.dropna(subset=required)
    if tstats.empty:
        return pd.DataFrame()

    rows: list[dict[str, object]] = []
    for idx, row in tstats.iterrows():
        values = row[required]
        pos_count = int((values >= 2.0).sum())
        neg_count = int((values <= -2.0).sum())
        max_abs_t = float(values.abs().max())

        if pos_count >= min_same_direction_horizons and max_abs_t >= min_abs_t:
            direction = "positive"
        elif neg_count >= min_same_direction_horizons and max_abs_t >= min_abs_t:
            direction = "negative"
        else:
            continue

        preferred_horizon = int(values.abs().idxmax())
        record = dict(zip(index_cols, idx if isinstance(idx, tuple) else (idx,), strict=False))
        record.update(
            {
                "direction": direction,
                "preferred_horizon": preferred_horizon,
                "preferred_event_count": float(events.loc[idx, preferred_horizon]),
                "preferred_mean_signed_return": float(means.loc[idx, preferred_horizon]),
                "preferred_hit_rate": float(hits.loc[idx, preferred_horizon]),
                "preferred_feature_return_corr": float(corrs.loc[idx, preferred_horizon]),
                "tstat_5d": float(row.get(5, np.nan)),
                "tstat_10d": float(row.get(10, np.nan)),
                "tstat_21d": float(row.get(21, np.nan)),
                "max_abs_tstat": max_abs_t,
                "avg_tstat": float(values.mean()),
                "same_direction_horizons": pos_count if direction == "positive" else neg_count,
            }
        )
        rows.append(record)

    out = pd.DataFrame(rows)
    if out.empty:
        return out

    out["economic_label"] = out.apply(_economic_label, axis=1)
    out["confidence"] = out.apply(_confidence, axis=1)
    return out.sort_values(
        ["confidence", "max_abs_tstat", "preferred_hit_rate"],
        ascending=[True, False, False],
    ).reset_index(drop=True)


def build_candidate_signals_from_paths(
    reactions_path: Path,
    universe_path: Path,
    output_path: Path,
    min_events: int = 30,
    min_abs_t: float = 3.0,
    min_same_direction_horizons: int = 2,
) -> pd.DataFrame:
    reactions = load_frame(reactions_path)
    seed = load_seed_universe(universe_path)
    candidates = build_candidate_signals(
        reactions=reactions,
        seed_universe=seed,
        min_events=min_events,
        min_abs_t=min_abs_t,
        min_same_direction_horizons=min_same_direction_horizons,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix == ".parquet":
        candidates.to_parquet(output_path, index=False)
    elif output_path.suffix == ".csv":
        candidates.to_csv(output_path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")
    return candidates
