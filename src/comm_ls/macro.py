from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from comm_ls.reaction import load_frame


MACRO_REGIME_LABELS = [
    "vix_regime",
    "dxy_regime",
    "us10y_regime",
    "ovx_regime",
]


def _write_frame(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix == ".parquet":
        df.to_parquet(output_path, index=False)
    elif output_path.suffix == ".csv":
        df.to_csv(output_path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")


def _load_raw_series(raw_dir: Path, name: str) -> pd.Series:
    path = raw_dir / f"{name}.csv"
    df = pd.read_csv(path, index_col=0, parse_dates=True)
    col = "price" if "price" in df.columns else df.columns[0]
    series = pd.to_numeric(df[col], errors="coerce").dropna()
    series.index = pd.to_datetime(series.index, utc=False)
    return series.sort_index()


def _z_score(series: pd.Series, window: int = 252, min_periods: int = 63) -> pd.Series:
    roll_mean = series.rolling(window, min_periods=min_periods).mean()
    roll_std = series.rolling(window, min_periods=min_periods).std()
    return (series - roll_mean) / roll_std


def _percentile(series: pd.Series, window: int = 756, min_periods: int = 252) -> pd.Series:
    return series.rolling(window, min_periods=min_periods).apply(
        lambda x: (x.iloc[-1] > x.iloc[:-1]).mean(), raw=False
    )


def build_macro_regime_frame(raw_dir: Path | None = None) -> pd.DataFrame:
    if raw_dir is None:
        raw_dir = Path("data/macro/raw")

    vix = _load_raw_series(raw_dir, "vix")
    dxy = _load_raw_series(raw_dir, "dxy")
    us10y = _load_raw_series(raw_dir, "us10y")
    ovx = _load_raw_series(raw_dir, "ovx")

    vix_pct = _percentile(vix, window=756)
    dxy_pct = _percentile(dxy, window=756)
    us10y_z = _z_score(us10y)
    ovx_pct = _percentile(ovx, window=756)

    vix_chg_21 = vix.pct_change(21)

    dates = sorted(set(vix_pct.dropna().index) & set(dxy_pct.dropna().index))
    rows = []
    for d in dates:
        vp = float(vix_pct.get(d, np.nan))
        dp = float(dxy_pct.get(d, np.nan))
        uz = float(us10y_z.get(d, np.nan))
        op = float(ovx_pct.get(d, np.nan))
        vc = float(vix_chg_21.get(d, np.nan))

        rows.append({
            "date": d,
            "vix_close": float(vix.get(d, np.nan)),
            "vix_percentile_3y": vp,
            "vix_regime": "high_vol" if vp > 0.7 else ("low_vol" if vp < 0.3 else "normal_vol"),
            "vix_change_21d": vc,
            "vix_trend": "rising" if vc > 0.10 else ("falling" if vc < -0.10 else "stable"),
            "dxy_close": float(dxy.get(d, np.nan)),
            "dxy_percentile_3y": dp,
            "dxy_regime": "strong_usd" if dp > 0.7 else ("weak_usd" if dp < 0.3 else "neutral_usd"),
            "us10y_close": float(us10y.get(d, np.nan)),
            "us10y_z_1y": uz,
            "us10y_regime": "rising_rates" if uz > 1.5 else ("falling_rates" if uz < -1.5 else "stable_rates"),
            "ovx_close": float(ovx.get(d, np.nan)),
            "ovx_percentile_3y": op,
            "ovx_regime": "high_oil_vol" if op > 0.7 else ("low_oil_vol" if op < 0.3 else "normal_oil_vol"),
        })

    return pd.DataFrame(rows).sort_values("date").reset_index(drop=True)


def build_macro_regime_frame_from_paths(
    raw_dir: Path | None = None,
    output_path: Path | None = None,
) -> pd.DataFrame:
    if output_path is None:
        output_path = Path("data/processed/macro_regime.parquet")
    frame = build_macro_regime_frame(raw_dir=raw_dir)
    _write_frame(frame, output_path)
    return frame

