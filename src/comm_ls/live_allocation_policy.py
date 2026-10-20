"""Operator-approved target-session allocation changes (not signal dates)."""
import pandas as pd

ALLOCATION_EFFECTIVE_DATE = pd.Timestamp("2026-10-12")
CRYPTO_REVIEW_DATE = pd.Timestamp("2026-11-12")


def crypto_aum_for_target(target_date) -> float:
    return 4000.0 if pd.Timestamp(target_date).normalize() >= ALLOCATION_EFFECTIVE_DATE else 3000.0
