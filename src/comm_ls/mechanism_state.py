from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from comm_ls.reaction import load_frame


PRIORITY_WEIGHT = {
    "high": 1.0,
    "medium": 0.6,
    "low": 0.3,
}


def _write_frame(df: pd.DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.suffix == ".parquet":
        df.to_parquet(output_path, index=False)
    elif output_path.suffix == ".csv":
        df.to_csv(output_path, index=False)
    else:
        raise ValueError("Output path must end with .parquet or .csv")


def _clean_commodity(value: object) -> str:
    return str(value).upper().strip()


def _num(row: pd.Series, col: str) -> float:
    if col not in row.index:
        return np.nan
    return float(pd.to_numeric(row[col], errors="coerce"))


def _direction_label(sign: float) -> str:
    if sign > 0:
        return "commodity_tight_or_up"
    if sign < 0:
        return "commodity_loose_or_down"
    return "neutral"


def _state_rows_for_snapshot(
    row: pd.Series,
    curve_z_threshold: float,
    momentum_z_threshold: float,
    price_regime_share_threshold: float,
    vol_z_threshold: float,
    participation_z_threshold: float,
    min_spread_abs: float,
    min_spread_chg_abs: float,
) -> list[dict[str, object]]:
    commodity = _clean_commodity(row["symbol"])
    date = row["date"]
    arrival = row.get("arrival", pd.NaT)
    rows: list[dict[str, object]] = []

    spread = _num(row, "front_third_spread")
    spread_z = _num(row, "front_third_spread_z_252d")
    spread_chg = _num(row, "front_third_spread_chg_21d")
    momentum_z = _num(row, "ret_63d_z_252d")
    vol_z = _num(row, "realized_vol_20d_z_252d")
    abs_ret_z = _num(row, "abs_ret_z_252d")
    volume_z = _num(row, "volume_z_252d")
    oi_z = _num(row, "oi_z_252d")
    high_price_share = _num(row, "front_price_high_share_100d_q80_3y")
    low_price_share = _num(row, "front_price_low_share_100d_q20_3y")

    base = {
        "date": date,
        "arrival": arrival,
        "commodity": commodity,
    }

    if pd.notna(spread) and pd.notna(spread_z):
        if spread >= min_spread_abs and spread_z >= curve_z_threshold:
            rows.append(
                {
                    **base,
                    "mechanism_state": "curve_tight_backwardation",
                    "state_family": "curve_structure",
                    "transmission_channel": "inventory_pressure",
                    "state_direction_sign": 1.0,
                    "state_direction": _direction_label(1.0),
                    "state_strength": abs(spread_z),
                    "state_trigger_value": spread,
                    "state_trigger_z": spread_z,
                    "mechanism_half_life_prior": "medium",
                    "mechanism_notes": "front curve backwardation/tightness with matching z-score",
                }
            )
        if spread <= -min_spread_abs and spread_z <= -curve_z_threshold:
            rows.append(
                {
                    **base,
                    "mechanism_state": "curve_loose_contango",
                    "state_family": "curve_structure",
                    "transmission_channel": "inventory_glut",
                    "state_direction_sign": -1.0,
                    "state_direction": _direction_label(-1.0),
                    "state_strength": abs(spread_z),
                    "state_trigger_value": spread,
                    "state_trigger_z": spread_z,
                    "mechanism_half_life_prior": "medium",
                    "mechanism_notes": "front curve contango/looseness with matching z-score",
                }
            )

    if pd.notna(spread_chg):
        if spread_chg >= min_spread_chg_abs:
            rows.append(
                {
                    **base,
                    "mechanism_state": "curve_tightening_impulse",
                    "state_family": "curve_change",
                    "transmission_channel": "inventory_flow",
                    "state_direction_sign": 1.0,
                    "state_direction": _direction_label(1.0),
                    "state_strength": abs(spread_chg),
                    "state_trigger_value": spread_chg,
                    "state_trigger_z": np.nan,
                    "mechanism_half_life_prior": "fast",
                    "mechanism_notes": "21-day front curve spread tightening impulse",
                }
            )
        if spread_chg <= -min_spread_chg_abs:
            rows.append(
                {
                    **base,
                    "mechanism_state": "curve_loosening_impulse",
                    "state_family": "curve_change",
                    "transmission_channel": "inventory_flow",
                    "state_direction_sign": -1.0,
                    "state_direction": _direction_label(-1.0),
                    "state_strength": abs(spread_chg),
                    "state_trigger_value": spread_chg,
                    "state_trigger_z": np.nan,
                    "mechanism_half_life_prior": "fast",
                    "mechanism_notes": "21-day front curve spread loosening impulse",
                }
            )

    if pd.notna(momentum_z):
        if momentum_z >= momentum_z_threshold:
            rows.append(
                {
                    **base,
                    "mechanism_state": "price_momentum_up",
                    "state_family": "price_momentum",
                    "transmission_channel": "macro_demand_liquidity",
                    "state_direction_sign": 1.0,
                    "state_direction": _direction_label(1.0),
                    "state_strength": abs(momentum_z),
                    "state_trigger_value": _num(row, "ret_63d"),
                    "state_trigger_z": momentum_z,
                    "mechanism_half_life_prior": "medium",
                    "mechanism_notes": "63-day commodity momentum is high versus its own history",
                }
            )
        if momentum_z <= -momentum_z_threshold:
            rows.append(
                {
                    **base,
                    "mechanism_state": "price_momentum_down",
                    "state_family": "price_momentum",
                    "transmission_channel": "macro_demand_liquidity",
                    "state_direction_sign": -1.0,
                    "state_direction": _direction_label(-1.0),
                    "state_strength": abs(momentum_z),
                    "state_trigger_value": _num(row, "ret_63d"),
                    "state_trigger_z": momentum_z,
                    "mechanism_half_life_prior": "medium",
                    "mechanism_notes": "63-day commodity momentum is low versus its own history",
                }
            )

    if pd.notna(high_price_share) and high_price_share >= price_regime_share_threshold:
        rows.append(
            {
                **base,
                "mechanism_state": "sustained_high_price_regime",
                "state_family": "price_regime",
                "transmission_channel": "equilibrium_margin_shift",
                "state_direction_sign": 1.0,
                "state_direction": _direction_label(1.0),
                "state_strength": high_price_share,
                "state_trigger_value": high_price_share,
                "state_trigger_z": np.nan,
                "mechanism_half_life_prior": "slow",
                "mechanism_notes": "front price spent enough time above its trailing high-price threshold",
            }
        )
    if pd.notna(low_price_share) and low_price_share >= price_regime_share_threshold:
        rows.append(
            {
                **base,
                "mechanism_state": "sustained_low_price_regime",
                "state_family": "price_regime",
                "transmission_channel": "equilibrium_margin_shift",
                "state_direction_sign": -1.0,
                "state_direction": _direction_label(-1.0),
                "state_strength": low_price_share,
                "state_trigger_value": low_price_share,
                "state_trigger_z": np.nan,
                "mechanism_half_life_prior": "slow",
                "mechanism_notes": "front price spent enough time below its trailing low-price threshold",
            }
        )

    if pd.notna(vol_z) and vol_z >= vol_z_threshold:
        direction = np.sign(momentum_z) if pd.notna(momentum_z) and momentum_z != 0 else np.sign(_num(row, "ret_21d"))
        direction = float(direction) if direction != 0 else 0.0
        rows.append(
            {
                **base,
                "mechanism_state": "volatility_shock",
                "state_family": "volatility",
                "transmission_channel": "risk_premium_and_hedging_pressure",
                "state_direction_sign": direction,
                "state_direction": _direction_label(direction),
                "state_strength": max(abs(vol_z), abs(abs_ret_z) if pd.notna(abs_ret_z) else 0.0),
                "state_trigger_value": _num(row, "realized_vol_20d"),
                "state_trigger_z": vol_z,
                "mechanism_half_life_prior": "fast",
                "mechanism_notes": "commodity volatility shock; directional mapping requires review",
            }
        )

    participation_inputs = [
        abs(value)
        for value in [volume_z, oi_z]
        if pd.notna(value)
    ]
    participation_strength = max(participation_inputs) if participation_inputs else np.nan
    if pd.notna(participation_strength) and participation_strength >= participation_z_threshold:
        direction = np.sign(momentum_z) if pd.notna(momentum_z) and momentum_z != 0 else np.sign(spread_chg)
        direction = float(direction) if direction != 0 else 0.0
        rows.append(
            {
                **base,
                "mechanism_state": "participation_shock",
                "state_family": "participation",
                "transmission_channel": "positioning_and_hedging_flow",
                "state_direction_sign": direction,
                "state_direction": _direction_label(direction),
                "state_strength": participation_strength,
                "state_trigger_value": max(volume_z if pd.notna(volume_z) else -np.inf, oi_z if pd.notna(oi_z) else -np.inf),
                "state_trigger_z": participation_strength,
                "mechanism_half_life_prior": "fast",
                "mechanism_notes": "volume/open-interest shock; can be positioning rather than fundamental pressure",
            }
        )

    return rows


def _prepare_role_taxonomy(role_taxonomy: pd.DataFrame) -> pd.DataFrame:
    required = {"commodity", "exposure_role", "expected_prior_sign", "alpha_priority", "deployable_default"}
    missing = required.difference(role_taxonomy.columns)
    if missing:
        raise ValueError(f"role taxonomy is missing required columns: {sorted(missing)}")
    taxonomy = role_taxonomy.copy()
    taxonomy["commodity"] = taxonomy["commodity"].astype(str).str.upper().str.strip()
    taxonomy["exposure_role"] = taxonomy["exposure_role"].astype(str).str.strip()
    taxonomy["expected_prior_sign"] = pd.to_numeric(taxonomy["expected_prior_sign"], errors="coerce")
    taxonomy["alpha_priority"] = taxonomy["alpha_priority"].astype(str).str.lower().str.strip()
    taxonomy["deployable_default"] = taxonomy["deployable_default"].astype(str).str.lower().isin(
        ["true", "1", "yes", "y"]
    )
    if "economic_channel" not in taxonomy.columns:
        taxonomy["economic_channel"] = ""
    if "taxonomy_bucket" not in taxonomy.columns:
        taxonomy["taxonomy_bucket"] = ""
    return taxonomy


def _prepare_exposure_map(exposure_map: pd.DataFrame) -> pd.DataFrame:
    if exposure_map.empty:
        return pd.DataFrame(columns=["ticker", "commodity", "exposure_role", "prior_weight", "notes"])
    exposure = exposure_map.copy()
    exposure["ticker"] = exposure["ticker"].astype(str).str.upper().str.strip()
    exposure["commodity"] = exposure["commodity"].astype(str).str.upper().str.strip()
    exposure["exposure_role"] = exposure["exposure_role"].astype(str).str.strip()
    exposure["prior_weight"] = pd.to_numeric(exposure["prior_weight"], errors="coerce")
    if "notes" not in exposure.columns:
        exposure["notes"] = ""
    return exposure


def _mechanism_verdict(row: pd.Series, min_role_tickers: int) -> str:
    if int(row["mapped_ticker_count"]) < min_role_tickers:
        return "block"
    if not bool(row["deployable_default"]):
        return "review"
    if str(row["alpha_priority"]).lower() == "low":
        return "review"
    if str(row["state_family"]) in {"volatility", "participation"}:
        return "review"
    if float(row["state_direction_sign"]) == 0.0:
        return "review"
    return "pass"


def build_mechanism_state_model(
    commodity_signals: pd.DataFrame,
    exposure_map: pd.DataFrame,
    role_taxonomy: pd.DataFrame,
    commodity: str | None = None,
    as_of_date: str | None = None,
    curve_z_threshold: float = 1.5,
    momentum_z_threshold: float = 1.0,
    price_regime_share_threshold: float = 0.6,
    vol_z_threshold: float = 1.0,
    participation_z_threshold: float = 1.0,
    min_spread_abs: float = 0.005,
    min_spread_chg_abs: float = 0.01,
    min_role_tickers: int = 1,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if commodity_signals.empty:
        return pd.DataFrame(), pd.DataFrame()
    required = {"date", "symbol"}
    missing = required.difference(commodity_signals.columns)
    if missing:
        raise ValueError(f"commodity signals is missing required columns: {sorted(missing)}")

    signals = commodity_signals.copy()
    signals["symbol"] = signals["symbol"].astype(str).str.upper().str.strip()
    signals["date"] = pd.to_datetime(signals["date"], utc=False)
    if "arrival" in signals.columns:
        signals["arrival"] = pd.to_datetime(signals["arrival"], utc=False)
    else:
        signals["arrival"] = signals["date"]
    if commodity:
        signals = signals[signals["symbol"].eq(commodity.upper().strip())].copy()
    if as_of_date:
        cutoff = pd.Timestamp(as_of_date)
        signals = signals[signals["arrival"].le(cutoff)].copy()
        signals = signals.sort_values(["symbol", "date"]).groupby("symbol", as_index=False, sort=False).tail(1)

    state_rows: list[dict[str, object]] = []
    for _, row in signals.sort_values(["symbol", "date"]).iterrows():
        state_rows.extend(
            _state_rows_for_snapshot(
                row=row,
                curve_z_threshold=curve_z_threshold,
                momentum_z_threshold=momentum_z_threshold,
                price_regime_share_threshold=price_regime_share_threshold,
                vol_z_threshold=vol_z_threshold,
                participation_z_threshold=participation_z_threshold,
                min_spread_abs=min_spread_abs,
                min_spread_chg_abs=min_spread_chg_abs,
            )
        )

    states = pd.DataFrame(state_rows)
    if states.empty:
        return states, pd.DataFrame()

    taxonomy = _prepare_role_taxonomy(role_taxonomy)
    exposure = _prepare_exposure_map(exposure_map)
    states = states.merge(taxonomy, on="commodity", how="left")
    if "notes" in states.columns:
        states = states.rename(columns={"notes": "role_taxonomy_notes"})
    states["state_direction_sign"] = pd.to_numeric(states["state_direction_sign"], errors="coerce")
    states["expected_prior_sign"] = pd.to_numeric(states["expected_prior_sign"], errors="coerce")
    states["expected_role_response_sign"] = states["state_direction_sign"] * states["expected_prior_sign"]
    states["mechanism_priority_weight"] = states["alpha_priority"].map(PRIORITY_WEIGHT).fillna(0.1)
    states["mechanism_role_score"] = states["state_strength"] * states["mechanism_priority_weight"]

    ticker_counts = (
        exposure.groupby(["commodity", "exposure_role"], dropna=False)["ticker"]
        .nunique()
        .rename("mapped_ticker_count")
        .reset_index()
    )
    states = states.merge(ticker_counts, on=["commodity", "exposure_role"], how="left")
    states["mapped_ticker_count"] = states["mapped_ticker_count"].fillna(0).astype(int)
    states["mechanism_verdict"] = states.apply(_mechanism_verdict, axis=1, min_role_tickers=min_role_tickers)
    states["mechanism_flags"] = ""
    states.loc[states["mapped_ticker_count"].lt(min_role_tickers), "mechanism_flags"] += "insufficient_mapped_tickers,"
    states.loc[~states["deployable_default"].fillna(False), "mechanism_flags"] += "not_deployable_default,"
    states.loc[states["alpha_priority"].eq("low"), "mechanism_flags"] += "low_priority_role,"
    states.loc[states["state_family"].isin(["volatility", "participation"]), "mechanism_flags"] += "fast_flow_state,"
    states.loc[states["state_direction_sign"].eq(0.0), "mechanism_flags"] += "direction_requires_review,"
    states["mechanism_flags"] = states["mechanism_flags"].str.rstrip(",")
    states["mechanism_flags"] = states["mechanism_flags"].replace("", np.nan)

    ticker_detail = states.merge(
        exposure,
        on=["commodity", "exposure_role"],
        how="left",
        suffixes=("", "_exposure"),
    )
    if "notes" in ticker_detail.columns:
        ticker_detail = ticker_detail.rename(columns={"notes": "exposure_notes"})
    ticker_detail["expected_ticker_response_sign"] = (
        ticker_detail["state_direction_sign"] * np.sign(ticker_detail["prior_weight"])
    )
    ticker_detail["expected_ticker_response_weight"] = (
        ticker_detail["state_strength"] * ticker_detail["prior_weight"].abs() * ticker_detail["mechanism_priority_weight"]
    )

    role_front = [
        "mechanism_verdict",
        "mechanism_flags",
        "date",
        "arrival",
        "commodity",
        "mechanism_state",
        "state_family",
        "transmission_channel",
        "state_direction",
        "state_direction_sign",
        "state_strength",
        "exposure_role",
        "expected_role_response_sign",
        "alpha_priority",
        "deployable_default",
        "mapped_ticker_count",
        "mechanism_half_life_prior",
        "economic_channel",
        "taxonomy_bucket",
        "role_taxonomy_notes",
        "mechanism_notes",
    ]
    ticker_front = role_front + [
        "ticker",
        "prior_weight",
        "expected_ticker_response_sign",
        "expected_ticker_response_weight",
        "exposure_notes",
    ]
    states = states[[col for col in role_front if col in states.columns] + [col for col in states.columns if col not in role_front]]
    ticker_detail = ticker_detail[
        [col for col in ticker_front if col in ticker_detail.columns]
        + [col for col in ticker_detail.columns if col not in ticker_front]
    ]
    return (
        states.sort_values(["date", "commodity", "mechanism_state", "exposure_role"]).reset_index(drop=True),
        ticker_detail.sort_values(["date", "commodity", "mechanism_state", "exposure_role", "ticker"]).reset_index(
            drop=True
        ),
    )


def build_mechanism_state_model_from_paths(
    commodity_signals_path: Path,
    exposure_map_path: Path,
    role_taxonomy_path: Path,
    output_path: Path,
    ticker_output_path: Path | None = None,
    commodity: str | None = None,
    as_of_date: str | None = None,
    curve_z_threshold: float = 1.5,
    momentum_z_threshold: float = 1.0,
    price_regime_share_threshold: float = 0.6,
    vol_z_threshold: float = 1.0,
    participation_z_threshold: float = 1.0,
    min_spread_abs: float = 0.005,
    min_spread_chg_abs: float = 0.01,
    min_role_tickers: int = 1,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    role_states, ticker_detail = build_mechanism_state_model(
        commodity_signals=load_frame(commodity_signals_path),
        exposure_map=pd.read_csv(exposure_map_path),
        role_taxonomy=pd.read_csv(role_taxonomy_path),
        commodity=commodity,
        as_of_date=as_of_date,
        curve_z_threshold=curve_z_threshold,
        momentum_z_threshold=momentum_z_threshold,
        price_regime_share_threshold=price_regime_share_threshold,
        vol_z_threshold=vol_z_threshold,
        participation_z_threshold=participation_z_threshold,
        min_spread_abs=min_spread_abs,
        min_spread_chg_abs=min_spread_chg_abs,
        min_role_tickers=min_role_tickers,
    )
    _write_frame(role_states, output_path)
    if ticker_output_path is not None:
        _write_frame(ticker_detail, ticker_output_path)
    return role_states, ticker_detail
