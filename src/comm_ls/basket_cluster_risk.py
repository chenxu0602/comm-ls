from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from comm_ls.curve_diagnostics import covid_time_regime
from comm_ls.reaction import load_frame


def _write_frame(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix == ".parquet":
        df.to_parquet(output_path, index=False)
    elif output_path.suffix == ".csv":
        df.to_csv(output_path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")


def _quarter_start(label: str) -> pd.Timestamp:
    return pd.Period(str(label), freq="Q").start_time.normalize()


def _effective_count(weights: pd.Series) -> float:
    values = pd.to_numeric(weights, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    if values.empty or values.sum() <= 0:
        return 0.0
    shares = values / values.sum()
    hhi = float((shares * shares).sum())
    return 0.0 if hhi <= 0 else float(1.0 / hhi)


def _max_share(frame: pd.DataFrame, group_col: str, weight_col: str) -> tuple[str | None, float]:
    if frame.empty:
        return None, np.nan
    weights = frame.groupby(group_col, dropna=False)[weight_col].sum()
    total = weights.sum()
    if total <= 0:
        return None, np.nan
    top_key = weights.idxmax()
    return str(top_key), float(weights.max() / total)


def build_basket_cluster_risk_audit(
    selection_pairs: pd.DataFrame,
    exposure_map: pd.DataFrame | None = None,
    candidates: pd.DataFrame | None = None,
    min_selection_probability: float = 0.8,
    max_direction_flip_probability: float = 0.1,
    min_tickers: int = 5,
    min_roles: int = 2,
    min_effective_tickers: float = 4.0,
    min_effective_roles: float = 1.5,
    max_ticker_share: float = 0.35,
    max_role_share: float = 0.65,
    max_unknown_role_share: float = 0.25,
    group_by_feature: bool = False,
    macro_regime_review: bool = True,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if selection_pairs.empty:
        return selection_pairs.copy(), pd.DataFrame()
    required = {"commodity", "quarter", "ticker", "feature", "selection_probability", "direction_flip_probability"}
    missing = required.difference(selection_pairs.columns)
    if missing:
        raise ValueError(f"selection_pairs is missing required columns: {sorted(missing)}")

    pairs = selection_pairs.copy()
    pairs["commodity"] = pairs["commodity"].astype(str).str.upper().str.strip()
    pairs["quarter"] = pairs["quarter"].astype(str)
    pairs["ticker"] = pairs["ticker"].astype(str).str.upper().str.strip()
    pairs["feature"] = pairs["feature"].astype(str).str.strip()
    pairs["selection_probability"] = pd.to_numeric(pairs["selection_probability"], errors="coerce")
    pairs["direction_flip_probability"] = pd.to_numeric(pairs["direction_flip_probability"], errors="coerce")

    if exposure_map is not None and not exposure_map.empty:
        exposure = exposure_map.copy()
        exposure["ticker"] = exposure["ticker"].astype(str).str.upper().str.strip()
        exposure["commodity"] = exposure["commodity"].astype(str).str.upper().str.strip()
        exposure_cols = ["ticker", "commodity", "exposure_role", "prior_weight"]
        pairs = pairs.merge(
            exposure[[col for col in exposure_cols if col in exposure.columns]].drop_duplicates(
                ["ticker", "commodity"]
            ),
            on=["ticker", "commodity"],
            how="left",
        )

    if candidates is not None and not candidates.empty:
        cand = candidates.copy()
        cand["ticker"] = cand["ticker"].astype(str).str.upper().str.strip()
        cand["commodity"] = cand["commodity"].astype(str).str.upper().str.strip()
        candidate_cols = ["ticker", "commodity", "theme", "role"]
        pairs = pairs.merge(
            cand[[col for col in candidate_cols if col in cand.columns]].drop_duplicates(["ticker", "commodity"]),
            on=["ticker", "commodity"],
            how="left",
            suffixes=("", "_candidate"),
        )

    if "exposure_role" not in pairs.columns:
        pairs["exposure_role"] = np.nan
    if "role" not in pairs.columns:
        pairs["role"] = np.nan
    pairs["cluster_role"] = pairs["exposure_role"].fillna(pairs["role"]).fillna("unknown").astype(str)
    pairs["stable_pair"] = (
        pairs["selection_probability"].ge(min_selection_probability)
        & pairs["direction_flip_probability"].le(max_direction_flip_probability)
    )
    pairs["selection_weight"] = np.where(pairs["stable_pair"], pairs["selection_probability"], 0.0)

    group_cols = ["commodity", "quarter", "feature"] if group_by_feature else ["commodity", "quarter"]
    summary_rows: list[dict[str, object]] = []
    detail_rows: list[pd.DataFrame] = []

    for key, group in pairs.groupby(group_cols, dropna=False, sort=True):
        key_values = dict(zip(group_cols, key if isinstance(key, tuple) else (key,), strict=False))
        stable = group[group["stable_pair"]].copy()
        quarter_start = _quarter_start(str(key_values["quarter"]))
        time_regime = covid_time_regime(quarter_start)
        ticker_weights = stable.groupby("ticker", dropna=False)["selection_weight"].sum()
        role_weights = stable.groupby("cluster_role", dropna=False)["selection_weight"].sum()
        dominant_ticker, max_ticker = _max_share(stable, "ticker", "selection_weight")
        dominant_role, max_role = _max_share(stable, "cluster_role", "selection_weight")
        total_weight = stable["selection_weight"].sum()
        unknown_weight = stable.loc[stable["cluster_role"].eq("unknown"), "selection_weight"].sum()
        unknown_role_share = float(unknown_weight / total_weight) if total_weight > 0 else np.nan
        ticker_count = int(stable["ticker"].nunique())
        role_count = int(stable["cluster_role"].nunique())
        effective_tickers = _effective_count(ticker_weights)
        effective_roles = _effective_count(role_weights)

        flags = {
            "no_stable_pairs": stable.empty,
            "insufficient_ticker_breadth": ticker_count < min_tickers,
            "insufficient_role_breadth": role_count < min_roles,
            "low_effective_tickers": effective_tickers < min_effective_tickers,
            "low_effective_roles": effective_roles < min_effective_roles,
            "ticker_concentration": pd.notna(max_ticker) and max_ticker > max_ticker_share,
            "role_concentration": pd.notna(max_role) and max_role > max_role_share,
            "unknown_role_concentration": pd.notna(unknown_role_share)
            and unknown_role_share > max_unknown_role_share,
            "macro_regime_review": macro_regime_review and time_regime == "covid_macro",
        }
        hard_flags = [
            "no_stable_pairs",
            "insufficient_ticker_breadth",
            "low_effective_tickers",
            "ticker_concentration",
        ]
        review_flags = [
            "insufficient_role_breadth",
            "low_effective_roles",
            "role_concentration",
            "unknown_role_concentration",
            "macro_regime_review",
        ]
        if any(flags[name] for name in hard_flags):
            verdict = "block"
        elif any(flags[name] for name in review_flags):
            verdict = "review"
        else:
            verdict = "pass"

        summary_rows.append(
            {
                **key_values,
                "basket_cluster_verdict": verdict,
                "basket_cluster_flags": ",".join([name for name, active in flags.items() if bool(active)]),
                "time_regime": time_regime,
                "candidate_pair_count": int(len(group)),
                "stable_pair_count": int(len(stable)),
                "ticker_count": ticker_count,
                "role_count": role_count,
                "effective_ticker_count": effective_tickers,
                "effective_role_count": effective_roles,
                "dominant_ticker": dominant_ticker,
                "max_ticker_share": max_ticker,
                "dominant_role": dominant_role,
                "max_role_share": max_role,
                "unknown_role_share": unknown_role_share,
                "mean_selection_probability": float(stable["selection_probability"].mean()) if len(stable) else np.nan,
                "max_direction_flip_probability": float(stable["direction_flip_probability"].max())
                if len(stable)
                else np.nan,
                "min_selection_probability": min_selection_probability,
                "max_allowed_direction_flip_probability": max_direction_flip_probability,
                "min_tickers": min_tickers,
                "min_roles": min_roles,
                "min_effective_tickers": min_effective_tickers,
                "min_effective_roles": min_effective_roles,
                "max_allowed_ticker_share": max_ticker_share,
                "max_allowed_role_share": max_role_share,
                "max_allowed_unknown_role_share": max_unknown_role_share,
            }
        )

        if not stable.empty:
            detail = stable.copy()
            total_weight = detail["selection_weight"].sum()
            detail["basket_weight_share"] = detail["selection_weight"] / total_weight if total_weight > 0 else np.nan
            detail["basket_cluster_verdict"] = verdict
            detail["basket_cluster_flags"] = summary_rows[-1]["basket_cluster_flags"]
            detail_rows.append(detail)

    summary = pd.DataFrame(summary_rows)
    detail = pd.concat(detail_rows, ignore_index=True) if detail_rows else pd.DataFrame()
    if not summary.empty:
        front = [
            "basket_cluster_verdict",
            "basket_cluster_flags",
            "commodity",
            "quarter",
            "feature",
            "time_regime",
            "stable_pair_count",
            "ticker_count",
            "role_count",
            "effective_ticker_count",
            "effective_role_count",
            "dominant_ticker",
            "max_ticker_share",
            "dominant_role",
            "max_role_share",
            "unknown_role_share",
        ]
        cols = [col for col in front if col in summary.columns] + [col for col in summary.columns if col not in front]
        summary = summary[cols].sort_values(["quarter", "basket_cluster_verdict"]).reset_index(drop=True)
    return summary, detail


def build_basket_cluster_risk_audit_from_paths(
    selection_pairs_path: Path,
    output_path: Path,
    detail_output_path: Path | None = None,
    exposure_map_path: Path | None = None,
    candidates_path: Path | None = None,
    min_selection_probability: float = 0.8,
    max_direction_flip_probability: float = 0.1,
    min_tickers: int = 5,
    min_roles: int = 2,
    min_effective_tickers: float = 4.0,
    min_effective_roles: float = 1.5,
    max_ticker_share: float = 0.35,
    max_role_share: float = 0.65,
    max_unknown_role_share: float = 0.25,
    group_by_feature: bool = False,
    macro_regime_review: bool = True,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    exposure = (
        pd.read_csv(exposure_map_path)
        if exposure_map_path is not None and exposure_map_path.exists()
        else pd.DataFrame()
    )
    candidates = load_frame(candidates_path) if candidates_path is not None and candidates_path.exists() else pd.DataFrame()
    summary, detail = build_basket_cluster_risk_audit(
        selection_pairs=load_frame(selection_pairs_path),
        exposure_map=exposure,
        candidates=candidates,
        min_selection_probability=min_selection_probability,
        max_direction_flip_probability=max_direction_flip_probability,
        min_tickers=min_tickers,
        min_roles=min_roles,
        min_effective_tickers=min_effective_tickers,
        min_effective_roles=min_effective_roles,
        max_ticker_share=max_ticker_share,
        max_role_share=max_role_share,
        max_unknown_role_share=max_unknown_role_share,
        group_by_feature=group_by_feature,
        macro_regime_review=macro_regime_review,
    )
    _write_frame(summary, output_path)
    if detail_output_path is not None:
        _write_frame(detail, detail_output_path)
    return summary, detail
