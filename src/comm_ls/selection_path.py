from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def _read_frame(path: Path) -> pd.DataFrame:
    if path.suffix == ".parquet":
        return pd.read_parquet(path)
    return pd.read_csv(path)


def _write_frame(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix == ".parquet":
        df.to_parquet(output_path, index=False)
    elif output_path.suffix == ".csv":
        df.to_csv(output_path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")


def _matrix_files(matrix_dir: Path, commodity: str) -> list[Path]:
    return sorted(matrix_dir.glob(f"{commodity.upper()}-Features-*-*.csv"))


def _normalize_tickers(tickers: list[str] | tuple[str, ...] | None) -> set[str] | None:
    if tickers is None:
        return None
    return {ticker.upper().strip() for ticker in tickers}


def _normalize_features(features: str | list[str] | tuple[str, ...]) -> list[str]:
    if isinstance(features, str):
        return [features.strip()]
    out = [feature.strip() for feature in features]
    if not out:
        raise ValueError("At least one feature is required")
    return out


def _dominant_direction(values: np.ndarray) -> tuple[float, float]:
    signs = values[np.isfinite(values)]
    signs = signs[signs != 0]
    if len(signs) == 0:
        return 0.0, 0.0
    positive = int((signs > 0).sum())
    negative = int((signs < 0).sum())
    if positive >= negative:
        return 1.0, positive / len(signs)
    return -1.0, negative / len(signs)


def _load_selection_rows(
    matrix_dir: Path,
    commodity: str,
    features: list[str],
    tickers: set[str] | None,
    target_return_column: str,
    horizon_days: int,
    lookback_years: set[int] | None,
) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for path in _matrix_files(matrix_dir, commodity):
        matrix = pd.read_csv(path)
        if matrix.empty:
            continue
        rows = matrix[
            matrix["feature"].astype(str).isin(features)
            & matrix["target_return_column"].astype(str).eq(target_return_column)
            & pd.to_numeric(matrix["horizon_days"], errors="coerce").eq(horizon_days)
        ].copy()
        if tickers is not None:
            rows = rows[rows["ticker"].astype(str).str.upper().isin(tickers)].copy()
        if lookback_years is not None:
            rows = rows[pd.to_numeric(rows["lookback_years"], errors="coerce").isin(lookback_years)].copy()
        if rows.empty:
            continue
        rows["source_matrix_path"] = str(path)
        frames.append(rows)
    if not frames:
        return pd.DataFrame()
    raw = pd.concat(frames, ignore_index=True)
    raw["commodity"] = raw["commodity"].astype(str).str.upper().str.strip()
    raw["quarter"] = raw["quarter"].astype(str)
    raw["ticker"] = raw["ticker"].astype(str).str.upper().str.strip()
    raw["feature"] = raw["feature"].astype(str).str.strip()
    raw["lookback_years"] = pd.to_numeric(raw["lookback_years"], errors="coerce")
    raw["nonoverlap_t_stat"] = pd.to_numeric(raw["nonoverlap_t_stat"], errors="coerce")
    raw["nonoverlap_abs_t_stat"] = pd.to_numeric(raw["nonoverlap_abs_t_stat"], errors="coerce")
    raw["effective_observations"] = pd.to_numeric(raw["effective_observations"], errors="coerce")
    raw["direction_sign"] = pd.to_numeric(raw["direction_sign"], errors="coerce")
    return raw.reset_index(drop=True)


def simulate_selection_path_stability(
    matrix_dir: Path,
    commodity: str,
    feature: str | list[str] | tuple[str, ...],
    tickers: list[str] | tuple[str, ...] | None = None,
    target_return_column: str = "residual_return_mktsec_w12m",
    horizon_days: int = 21,
    lookback_years: list[int] | tuple[int, ...] | None = None,
    min_nonoverlap_abs_t_stat: float = 1.5,
    min_effective_observations: int = 20,
    min_selected_lookbacks: int = 1,
    min_direction_share: float = 0.5,
    min_pairs: int = 2,
    basket_scope: str = "quarter",
    simulations: int = 500,
    t_stat_noise: float = 1.0,
    random_seed: int = 7,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    commodity = commodity.upper().strip()
    features = _normalize_features(feature)
    tickers_set = _normalize_tickers(tickers)
    lookbacks_set = set(lookback_years) if lookback_years is not None else None
    if basket_scope not in {"quarter", "feature"}:
        raise ValueError("basket_scope must be 'quarter' or 'feature'")
    if simulations <= 0:
        raise ValueError("simulations must be positive")

    raw = _load_selection_rows(
        matrix_dir=matrix_dir,
        commodity=commodity,
        features=features,
        tickers=tickers_set,
        target_return_column=target_return_column,
        horizon_days=horizon_days,
        lookback_years=lookbacks_set,
    )
    if raw.empty:
        return pd.DataFrame(), pd.DataFrame()

    keys = ["commodity", "quarter", "ticker", "feature", "target_return_column", "horizon_days"]
    grouped = [(key, group.reset_index(drop=True)) for key, group in raw.groupby(keys, dropna=False, sort=True)]
    rng = np.random.default_rng(random_seed)
    pair_counts: dict[tuple[object, ...], dict[str, object]] = {}
    basket_counts: dict[tuple[object, ...], dict[str, object]] = {}

    for _ in range(simulations):
        pair_rows: list[dict[str, object]] = []
        for key, group in grouped:
            base_t = group["nonoverlap_t_stat"].to_numpy(dtype=float)
            noisy_t = base_t + rng.normal(loc=0.0, scale=t_stat_noise, size=len(group))
            effective = group["effective_observations"].to_numpy(dtype=float)
            selected_mask = (np.abs(noisy_t) >= min_nonoverlap_abs_t_stat) & (
                effective >= min_effective_observations
            )
            selected_signs = np.sign(noisy_t[selected_mask])
            direction_source = selected_signs if len(selected_signs) else np.sign(noisy_t)
            direction_sign, direction_share = _dominant_direction(direction_source)
            selected_lookbacks = int(np.isfinite(group.loc[selected_mask, "lookback_years"]).sum())
            pair_selected = (
                selected_lookbacks >= min_selected_lookbacks
                and direction_sign != 0
                and direction_share >= min_direction_share
            )
            row = {
                "commodity": key[0],
                "quarter": key[1],
                "ticker": key[2],
                "feature": key[3],
                "target_return_column": key[4],
                "horizon_days": int(key[5]),
                "pair_selected": bool(pair_selected),
                "direction_sign": direction_sign,
                "selected_lookback_count": selected_lookbacks,
                "direction_share": direction_share,
            }
            pair_rows.append(row)
            pair_key = tuple(row[col] for col in keys)
            stats = pair_counts.setdefault(
                pair_key,
                {
                    "commodity": key[0],
                    "quarter": key[1],
                    "ticker": key[2],
                    "feature": key[3],
                    "target_return_column": key[4],
                    "horizon_days": int(key[5]),
                    "selected_count": 0,
                    "positive_count": 0,
                    "negative_count": 0,
                    "selected_lookback_sum": 0.0,
                    "direction_share_sum": 0.0,
                },
            )
            stats["selected_count"] += int(pair_selected)
            stats["positive_count"] += int(direction_sign > 0)
            stats["negative_count"] += int(direction_sign < 0)
            stats["selected_lookback_sum"] += selected_lookbacks
            stats["direction_share_sum"] += direction_share

        pair_sim = pd.DataFrame(pair_rows)
        basket_cols = ["commodity", "quarter"] if basket_scope == "quarter" else ["commodity", "quarter", "feature"]
        basket_sim = (
            pair_sim.groupby(basket_cols, as_index=False)
            .agg(
                selected_count=("pair_selected", "sum"),
                candidate_count=("ticker", "count"),
                ticker_count=("ticker", "nunique"),
                feature_count=("feature", "nunique"),
            )
        )
        basket_sim["basket_selected"] = basket_sim["selected_count"] >= min_pairs
        for row in basket_sim.itertuples(index=False):
            b_key = tuple(getattr(row, col) for col in basket_cols)
            stats = basket_counts.setdefault(
                b_key,
                {
                    **{col: getattr(row, col) for col in basket_cols},
                    "basket_selected_count": 0,
                    "selected_count_sum": 0.0,
                    "candidate_count": int(row.candidate_count),
                    "ticker_count": int(row.ticker_count),
                    "feature_count": int(row.feature_count),
                },
            )
            stats["basket_selected_count"] += int(row.basket_selected)
            stats["selected_count_sum"] += float(row.selected_count)

    pair_summary = pd.DataFrame(pair_counts.values())
    pair_summary["selection_probability"] = pair_summary["selected_count"] / simulations
    pair_summary["positive_direction_probability"] = pair_summary["positive_count"] / simulations
    pair_summary["negative_direction_probability"] = pair_summary["negative_count"] / simulations
    pair_summary["direction_flip_probability"] = np.minimum(
        pair_summary["positive_direction_probability"],
        pair_summary["negative_direction_probability"],
    )
    pair_summary["mean_selected_lookbacks"] = pair_summary["selected_lookback_sum"] / simulations
    pair_summary["mean_direction_share"] = pair_summary["direction_share_sum"] / simulations
    pair_summary["path_stability_verdict"] = np.select(
        [
            pair_summary["selection_probability"] >= 0.8,
            pair_summary["selection_probability"] >= 0.5,
            pair_summary["selection_probability"] > 0.0,
        ],
        ["stable", "fragile", "rarely_selected"],
        default="never_selected",
    )
    pair_summary["path_stability_flags"] = (
        pair_summary[["selection_probability", "direction_flip_probability"]]
        .apply(
            lambda row: ",".join(
                [
                    flag
                    for flag, active in {
                        "low_selection_probability": row["selection_probability"] < 0.5,
                        "direction_flip_risk": row["direction_flip_probability"] > 0.2,
                    }.items()
                    if active
                ]
            ),
            axis=1,
        )
    )

    basket_summary = pd.DataFrame(basket_counts.values())
    basket_summary["basket_selection_probability"] = basket_summary["basket_selected_count"] / simulations
    basket_summary["mean_selected_count"] = basket_summary["selected_count_sum"] / simulations
    basket_summary["basket_path_verdict"] = np.select(
        [
            basket_summary["basket_selection_probability"] >= 0.8,
            basket_summary["basket_selection_probability"] >= 0.5,
            basket_summary["basket_selection_probability"] > 0.0,
        ],
        ["stable", "fragile", "rarely_selected"],
        default="never_selected",
    )

    meta_cols = {
        "simulations": simulations,
        "t_stat_noise": t_stat_noise,
        "random_seed": random_seed,
        "min_nonoverlap_abs_t_stat": min_nonoverlap_abs_t_stat,
        "min_effective_observations": min_effective_observations,
        "min_selected_lookbacks": min_selected_lookbacks,
        "min_direction_share": min_direction_share,
        "min_pairs": min_pairs,
        "basket_scope": basket_scope,
    }
    for col, value in meta_cols.items():
        pair_summary[col] = value
        basket_summary[col] = value

    return (
        pair_summary.sort_values(["quarter", "feature", "ticker"]).reset_index(drop=True),
        basket_summary.sort_values([col for col in ["quarter", "feature"] if col in basket_summary.columns]).reset_index(
            drop=True
        ),
    )


def simulate_selection_path_stability_from_paths(
    matrix_dir: Path,
    output_pairs_path: Path,
    output_baskets_path: Path,
    commodity: str,
    feature: str | list[str] | tuple[str, ...],
    tickers: list[str] | tuple[str, ...] | None = None,
    target_return_column: str = "residual_return_mktsec_w12m",
    horizon_days: int = 21,
    lookback_years: list[int] | tuple[int, ...] | None = None,
    min_nonoverlap_abs_t_stat: float = 1.5,
    min_effective_observations: int = 20,
    min_selected_lookbacks: int = 1,
    min_direction_share: float = 0.5,
    min_pairs: int = 2,
    basket_scope: str = "quarter",
    simulations: int = 500,
    t_stat_noise: float = 1.0,
    random_seed: int = 7,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    pairs, baskets = simulate_selection_path_stability(
        matrix_dir=matrix_dir,
        commodity=commodity,
        feature=feature,
        tickers=tickers,
        target_return_column=target_return_column,
        horizon_days=horizon_days,
        lookback_years=lookback_years,
        min_nonoverlap_abs_t_stat=min_nonoverlap_abs_t_stat,
        min_effective_observations=min_effective_observations,
        min_selected_lookbacks=min_selected_lookbacks,
        min_direction_share=min_direction_share,
        min_pairs=min_pairs,
        basket_scope=basket_scope,
        simulations=simulations,
        t_stat_noise=t_stat_noise,
        random_seed=random_seed,
    )
    _write_frame(pairs, output_pairs_path)
    _write_frame(baskets, output_baskets_path)
    return pairs, baskets
