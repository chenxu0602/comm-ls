# trigger.py -- commodity curve extreme detection with layered confirmation
"""CL/HG extreme-curve trigger logic.

The trigger model asks three questions in order:

1. PRIMARY: is the commodity curve in an extreme state (backwardation / contango)?
2. CONFIRMATION: is the extreme accelerating or confirmed by momentum?
3. STRENGTH: how many confirmations are active?

Only when the primary gate passes do we proceed to stock selection.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Core commodities in scope.
CORE_COMMODITIES: list[str] = ["CL", "HG"]

# Primary gate: curve extreme thresholds.  Prefer backwardation steepness
# because its sign is intuitive: higher means the front of the curve is tighter.
STEEPNESS_EXTREME_Z: float = 1.5
CARRY_EXTREME_HIGH: float = 0.80
CARRY_EXTREME_LOW: float = 0.20

# front_third_spread = M0_settle / M2_settle - 1. Positive = backwardation.
# front_third_backwardation_steepness = -annualized carry. Positive = backwardation.
# Require a minimum magnitude to avoid noise around zero.
MIN_SPREAD_MAGNITUDE: float = 0.005  # 0.5%
MIN_STEEPNESS_MAGNITUDE: float = 0.01  # 1 annualized percentage point
MIN_STEEPNESS_CHG_21D: float = 0.01  # 1 annualized percentage point

# Confirmation: at least one must agree with the primary direction.
# - spread change (front_third_spread_chg_21d): curve shape change in last 21 days
# - ret z-score (ret_63d_z_252d): 63-day price momentum relative to history
CONFIRM_Z_THRESHOLD: float = 1.0  # |z| >= 1.0 for confirmation

# Stock scoring: minimum confidence / quality thresholds.
MIN_CONFIDENCE: str = "medium"  # "high" | "medium" | "low" — weaker candidates excluded
MIN_QUALITY_SCORE: float = 50.0  # quality_score floor from consolidation

# ---------------------------------------------------------------------------
# Data types
# ---------------------------------------------------------------------------


@dataclass
class TriggerSignal:
    """Result of trigger detection for one commodity on one date."""

    commodity: str
    as_of_date: str
    triggered: bool
    direction: str  # "bullish" | "bearish" | "none"
    strength: str  # "full" | "standard" | "none"
    carry_pctile: float
    spread: float
    spread_chg: float
    backwardation_steepness: float
    backwardation_steepness_z: float
    backwardation_steepness_chg: float
    ret_z: float
    primary_pass: bool
    confirm_spread: bool
    confirm_momentum: bool
    notes: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Trigger logic
# ---------------------------------------------------------------------------


def _latest_commodity_snapshot(
    signals: pd.DataFrame,
    commodity: str,
    as_of_date: str,
) -> dict[str, float]:
    """Extract the latest feature snapshot for one commodity up to as_of_date."""
    sig = signals.copy()
    sig["symbol"] = sig["symbol"].astype(str).str.upper().str.strip()
    sig = sig[sig["symbol"] == commodity.upper()].copy()
    if sig.empty:
        return {}

    sig["date"] = pd.to_datetime(sig["date"], utc=False)
    if "arrival" in sig.columns:
        sig["arrival"] = pd.to_datetime(sig["arrival"], utc=False)
        target = pd.Timestamp(as_of_date)
        sig = sig[sig["arrival"] <= target]
    else:
        target = pd.Timestamp(as_of_date)
        sig = sig[sig["date"] <= target]

    if sig.empty:
        return {}

    latest = sig.sort_values("date").iloc[-1]
    features = [
        "carry_pctile_252d",
        "front_third_spread",
        "front_third_spread_chg_21d",
        "front_third_backwardation_steepness",
        "front_third_backwardation_steepness_z_252d",
        "front_third_backwardation_steepness_chg_21d",
        "ret_63d_z_252d",
        "front_second_spread",
        "carry_z_252d",
    ]

    result: dict[str, float] = {}
    for col in features:
        if col in sig.columns:
            val = latest[col]
            result[col] = float(val) if pd.notna(val) else float("nan")
    return result


def detect_trigger(
    signals: pd.DataFrame,
    commodity: str,
    as_of_date: str,
    steepness_extreme_z: float = STEEPNESS_EXTREME_Z,
    carry_extreme_high: float = CARRY_EXTREME_HIGH,
    carry_extreme_low: float = CARRY_EXTREME_LOW,
    min_spread_magnitude: float = MIN_SPREAD_MAGNITUDE,
    min_steepness_magnitude: float = MIN_STEEPNESS_MAGNITUDE,
    min_steepness_chg_21d: float = MIN_STEEPNESS_CHG_21D,
    confirm_z: float = CONFIRM_Z_THRESHOLD,
) -> TriggerSignal:
    """Run the three-layer trigger check for one commodity."""

    snap = _latest_commodity_snapshot(signals, commodity, as_of_date)

    carry_pctile = snap.get("carry_pctile_252d", float("nan"))
    spread = snap.get("front_third_spread", float("nan"))
    spread_chg = snap.get("front_third_spread_chg_21d", float("nan"))
    steepness = snap.get("front_third_backwardation_steepness", float("nan"))
    steepness_z = snap.get("front_third_backwardation_steepness_z_252d", float("nan"))
    steepness_chg = snap.get("front_third_backwardation_steepness_chg_21d", float("nan"))
    ret_z = snap.get("ret_63d_z_252d", float("nan"))

    notes: list[str] = []

    # --- Layer 1: Primary gate (curve extreme) ---
    has_steepness = pd.notna(steepness) and pd.notna(steepness_z)
    if has_steepness:
        bullish_primary = steepness > min_steepness_magnitude and steepness_z >= steepness_extreme_z
        bearish_primary = steepness < -min_steepness_magnitude and steepness_z <= -steepness_extreme_z
    else:
        # Fallback for old commodity-signal files before steepness fields are rebuilt.
        bullish_primary = (
            pd.notna(carry_pctile)
            and carry_pctile >= carry_extreme_high
            and pd.notna(spread)
            and spread > min_spread_magnitude
        )
        bearish_primary = (
            pd.notna(carry_pctile)
            and carry_pctile <= carry_extreme_low
            and pd.notna(spread)
            and spread < -min_spread_magnitude
        )

    if not bullish_primary and not bearish_primary:
        if has_steepness:
            notes.append(f"no curve extreme: steepness={steepness:.4f} steepness_z={steepness_z:.2f}")
        elif pd.isna(carry_pctile):
            notes.append("curve steepness missing and carry_pctile_252d missing")
        else:
            notes.append(
                f"no curve extreme: carry_pctile={carry_pctile:.3f} spread={spread:.4f}"
            )
        return TriggerSignal(
            commodity=commodity,
            as_of_date=as_of_date,
            triggered=False,
            direction="none",
            strength="none",
            carry_pctile=carry_pctile,
            spread=spread,
            spread_chg=spread_chg,
            backwardation_steepness=steepness,
            backwardation_steepness_z=steepness_z,
            backwardation_steepness_chg=steepness_chg,
            ret_z=ret_z,
            primary_pass=False,
            confirm_spread=False,
            confirm_momentum=False,
            notes=notes,
        )

    direction = "bullish" if bullish_primary else "bearish"
    direction_sign = 1.0 if bullish_primary else -1.0

    # --- Layer 2: Confirmation ---
    if has_steepness:
        confirm_spread = (
            pd.notna(steepness_chg)
            and abs(steepness_chg) >= min_steepness_chg_21d
            and (steepness_chg * direction_sign) > 0
        )
    else:
        confirm_spread = (
            pd.notna(spread_chg) and abs(spread_chg) >= 0.001
            and (spread_chg * direction_sign) > 0
        )
    confirm_momentum = (
        pd.notna(ret_z) and abs(ret_z) >= confirm_z
        and (ret_z * direction_sign) > 0
    )

    if not confirm_spread:
        if has_steepness:
            notes.append(f"steepness_chg_21d={steepness_chg:.4f} does not confirm {direction}")
        else:
            notes.append(f"spread_chg_21d={spread_chg:.4f} does not confirm {direction}")
    if not confirm_momentum:
        notes.append(f"ret_63d_z={ret_z:.3f} does not confirm {direction}")

    confirm_count = sum([confirm_spread, confirm_momentum])
    if confirm_count == 0:
        notes.insert(0, "primary passed but no confirmation")
        return TriggerSignal(
            commodity=commodity,
            as_of_date=as_of_date,
            triggered=False,
            direction=direction,
            strength="none",
            carry_pctile=carry_pctile,
            spread=spread,
            spread_chg=spread_chg,
            backwardation_steepness=steepness,
            backwardation_steepness_z=steepness_z,
            backwardation_steepness_chg=steepness_chg,
            ret_z=ret_z,
            primary_pass=True,
            confirm_spread=False,
            confirm_momentum=False,
            notes=notes,
        )

    strength = "full" if confirm_count >= 2 else "standard"
    notes.insert(0, f"{commodity} {direction} trigger ({strength})")
    if strength == "full":
        notes.append("both confirmations active")
    else:
        notes.append("single confirmation active")

    return TriggerSignal(
        commodity=commodity,
        as_of_date=as_of_date,
        triggered=True,
        direction=direction,
        strength=strength,
        carry_pctile=carry_pctile,
        spread=spread,
        spread_chg=spread_chg,
        backwardation_steepness=steepness,
        backwardation_steepness_z=steepness_z,
        backwardation_steepness_chg=steepness_chg,
        ret_z=ret_z,
        primary_pass=True,
        confirm_spread=confirm_spread,
        confirm_momentum=confirm_momentum,
        notes=notes,
    )


def detect_all_triggers(
    signals: pd.DataFrame,
    as_of_date: str,
    commodities: list[str] | None = None,
) -> list[TriggerSignal]:
    """Run trigger detection for all core commodities."""
    commodities = commodities or CORE_COMMODITIES
    results: list[TriggerSignal] = []
    for commodity in commodities:
        result = detect_trigger(signals, commodity, as_of_date)
        results.append(result)
    return results


def format_trigger_report(triggers: list[TriggerSignal]) -> str:
    """Produce a human-readable one-line-per-commodity trigger summary."""
    lines: list[str] = []
    for t in triggers:
        if t.triggered:
            strength_mark = "FULL" if t.strength == "full" else "STD"
            lines.append(
                f"[{t.commodity}] {t.direction.upper()} {strength_mark} "
                f"steepness={t.backwardation_steepness:.4f} "
                f"steep_z={t.backwardation_steepness_z:.2f} "
                f"steep_chg={t.backwardation_steepness_chg:.4f} ret_z={t.ret_z:.2f}"
            )
        elif t.primary_pass:
            lines.append(
                f"[{t.commodity}] {t.direction.upper()} NO_CONFIRM "
                f"(steep_chg={t.backwardation_steepness_chg:.4f} ret_z={t.ret_z:.2f})"
            )
        else:
            lines.append(f"[{t.commodity}] NO_TRIGGER ({t.notes[0] if t.notes else 'inactive'})")
    return "\n".join(lines) if lines else "No commodities evaluated."
