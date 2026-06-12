from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class EventRegimeWindow:
    name: str
    start: pd.Timestamp
    end: pd.Timestamp | None
    description: str


EVENT_REGIME_WINDOWS = [
    EventRegimeWindow(
        name="hormuz_crisis",
        start=pd.Timestamp("2026-02-28"),
        end=None,
        description="2026 Strait of Hormuz / Iran war supply chokepoint crisis",
    ),
]


def event_regime(date: pd.Timestamp | str) -> str:
    value = pd.Timestamp(date)
    for window in EVENT_REGIME_WINDOWS:
        if value >= window.start and (window.end is None or value <= window.end):
            return window.name
    return "none"


def add_event_regime(df: pd.DataFrame, date_column: str = "date") -> pd.DataFrame:
    if df.empty:
        out = df.copy()
        out["event_regime"] = pd.Series(dtype="object")
        return out
    out = df.copy()
    out[date_column] = pd.to_datetime(out[date_column], utc=False)
    out["event_regime"] = out[date_column].map(event_regime)
    return out


def event_window_table() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "event_regime": window.name,
                "start_date": window.start,
                "end_date": window.end,
                "description": window.description,
            }
            for window in EVENT_REGIME_WINDOWS
        ]
    )
