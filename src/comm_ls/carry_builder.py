from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np
import pandas as pd

from comm_ls.commodity import (
    ACTIVE_CONTRACT_MONTHS_BY_SYMBOL,
    ALL_CONTRACT_MONTHS,
    FUTURES_MONTH_CODES,
    FUTURES_MONTH_NUMBERS,
    LIVE_PRICE_SCALE_BY_SYMBOL,
)


DAYS_IN_YEAR = 365.25
CRYPTO_SYMBOLS = frozenset({"BTC", "DCR", "QSO"})
ENERGY_SYMBOLS = frozenset({"CL", "CO", "NG", "HO", "XB"})
MONTHLY_STEPWISE_FRONT_SYMBOLS = ENERGY_SYMBOLS | frozenset(
    {"SCO", "LC", "IS", "PS", "PD", "PT"}
)
CARRY_OUTPUT_SYMBOL_BY_SOURCE = {"DCR": "ETH", "QSO": "SOL"}

DEFAULT_LIS_TARGETS = (0.30,)
CRYPTO_LIS_TARGETS = (0.10,)
ENERGY_LIS_TARGETS = (0.10, 0.30, 0.50, 1.00)
MAX_LIS_LEG_GAP_YEARS = 0.35
MAX_LIVE_SETTLEMENT_LAST_GAP = 0.10

ANCHOR_MONTHS_BY_SYMBOL: dict[str, tuple[int, ...]] = {
    "CL": (1, 2, 3, 6, 9, 12),
    "CO": (1, 2, 3, 6, 9, 12),
    "NG": (1, 2, 3, 6, 9, 12),
    "HO": (1, 2, 3, 6, 9, 12),
    "XB": (1, 2, 3, 6, 9, 12),
    "GC": (2, 4, 6, 8, 10, 12),
    "SI": (1, 3, 5, 7, 9, 12),
    "HG": (1, 3, 5, 7, 9, 12),
    "PA": (3, 6, 9, 12),
    "PL": (1, 4, 7, 10),
    "BTC": (3, 6, 9, 12),
    "DCR": (3, 6, 9, 12),
    "QSO": (3, 6, 9, 12),
}

ENERGY_CALENDAR_PAIRS = ((3, 6), (6, 9), (9, 12), (12, 3), (6, 12), (12, 12))


@dataclass(frozen=True)
class CarryBuildConfig:
    symbol: str
    commodity_dir: Path = Path("data/comm")
    volume_staleness_sessions: int = 2
    oi_staleness_sessions: int = 5
    roll_confirmation_observations: int = 2
    lis_ratio: float = 0.60
    activity_threshold: float = 0.005
    arrival_hour_utc: int = 8

    @property
    def normalized_symbol(self) -> str:
        return self.symbol.upper().strip()

    @property
    def lis_targets(self) -> tuple[float, ...]:
        symbol = self.normalized_symbol
        if symbol in ENERGY_SYMBOLS:
            return ENERGY_LIS_TARGETS
        if symbol in CRYPTO_SYMBOLS:
            return CRYPTO_LIS_TARGETS
        return DEFAULT_LIS_TARGETS

    @property
    def legacy_carry_target(self) -> float:
        return 0.10 if self.normalized_symbol in CRYPTO_SYMBOLS else 0.30


def contract_sort_key(contract: str) -> tuple[int, int]:
    text = str(contract).strip().upper()
    if len(text) < 5 or text[-1] not in FUTURES_MONTH_CODES:
        raise ValueError(f"Invalid futures contract: {contract!r}")
    return int(text[:-1]), FUTURES_MONTH_CODES[text[-1]]


def contract_month_start(contract: str) -> pd.Timestamp:
    year, month = contract_sort_key(contract)
    return pd.Timestamp(year=year, month=month, day=1)


def _valid_contract_name(value: object) -> bool:
    if not isinstance(value, str):
        return False
    text = value.strip().upper()
    return len(text) >= 5 and text[:-1].isdigit() and text[-1] in FUTURES_MONTH_CODES


def _numeric(frame: pd.DataFrame, column: str, scale: float = 1.0) -> pd.Series:
    if column not in frame.columns:
        return pd.Series(np.nan, index=frame.index, dtype=float)
    return pd.to_numeric(frame[column], errors="coerce") * scale


def _normalize_source_frame(
    frame: pd.DataFrame,
    *,
    source: str,
    contract: str | None = None,
    price_scale: float = 1.0,
) -> pd.DataFrame:
    if "date" not in frame.columns:
        return pd.DataFrame()

    out = pd.DataFrame(index=frame.index)
    out["date"] = pd.to_datetime(frame["date"], errors="coerce", utc=False).dt.normalize()
    if contract is None:
        if "contract" not in frame.columns:
            return pd.DataFrame()
        out["contract"] = frame["contract"].astype("string").str.strip().str.upper()
    else:
        out["contract"] = contract.strip().upper()

    prices = {
        column: _numeric(frame, column, price_scale)
        for column in ("open", "high", "low", "px_last", "px_settle")
    }
    row_scale = pd.Series(1.0, index=frame.index)
    if source == "live":
        reference = prices["px_settle"].fillna(prices["px_last"])
        daily_median = reference.where(reference.gt(0)).groupby(out["date"]).transform("median")
        low_outlier = reference.gt(0) & (daily_median / reference).between(20.0, 200.0)
        high_outlier = daily_median.gt(0) & (reference / daily_median).between(20.0, 200.0)
        row_scale = row_scale.mask(low_outlier, 100.0).mask(high_outlier, 0.01)
        for column in prices:
            prices[column] = prices[column] * row_scale

    settle = prices["px_settle"]
    last = prices["px_last"]
    invalid_live_settlement = pd.Series(False, index=frame.index)
    if source == "live":
        comparable = settle.gt(0) & last.gt(0)
        invalid_live_settlement = comparable & (settle / last - 1.0).abs().gt(
            MAX_LIVE_SETTLEMENT_LAST_GAP
        )
    usable_settle = settle.mask(invalid_live_settlement)
    out["settle"] = usable_settle.fillna(last)
    out["settle_kind"] = np.select(
        [
            invalid_live_settlement & last.notna(),
            usable_settle.notna() & row_scale.ne(1.0),
            usable_settle.notna(),
            usable_settle.isna() & last.notna(),
        ],
        ["last_invalid_settlement", "settlement_scaled", "settlement", "last"],
        default=pd.NA,
    )
    for column in ("open", "high", "low"):
        out[column] = prices[column]
    out["price_scale_adjustment"] = price_scale * row_scale
    out["volume"] = _numeric(frame, "volume")
    out["open_interest"] = _numeric(frame, "open int")
    out["source"] = source
    out = out[out["contract"].map(_valid_contract_name)].dropna(subset=["date"])
    if out.empty:
        return out

    # Keep the last supplied row for an accidental duplicate, but choose
    # settlement before last within that row above.
    return out.drop_duplicates(["date", "contract"], keep="last").reset_index(drop=True)


def _load_source_frames(symbol: str, commodity_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    symbol = symbol.upper()
    symbol_dir = commodity_dir / symbol
    history_frames: list[pd.DataFrame] = []
    if symbol_dir.exists():
        for path in sorted(symbol_dir.glob("*.csv")):
            normalized = _normalize_source_frame(
                pd.read_csv(path),
                source="history",
                contract=path.stem,
            )
            if not normalized.empty:
                history_frames.append(normalized)

    live_symbol = CARRY_OUTPUT_SYMBOL_BY_SOURCE.get(symbol, symbol)
    live_path = commodity_dir / "live_data" / f"{live_symbol}.csv"
    if live_path.exists():
        live = _normalize_source_frame(
            pd.read_csv(live_path),
            source="live",
            price_scale=LIVE_PRICE_SCALE_BY_SYMBOL.get(symbol, 1.0),
        )
    else:
        live = pd.DataFrame()

    history = pd.concat(history_frames, ignore_index=True) if history_frames else pd.DataFrame()
    return history, live


def _history_first_field(
    merged: pd.DataFrame,
    *,
    field: str,
) -> tuple[pd.Series, pd.Series]:
    history = merged.get(f"{field}__history", pd.Series(np.nan, index=merged.index))
    live = merged.get(f"{field}__live", pd.Series(np.nan, index=merged.index))
    value = history.fillna(live)
    source = pd.Series(pd.NA, index=merged.index, dtype="string")
    source.loc[history.notna()] = "history"
    source.loc[history.isna() & live.notna()] = "live_fallback"
    return value, source


def _history_first_settle(
    merged: pd.DataFrame,
) -> tuple[pd.Series, pd.Series, pd.Series]:
    """Select settlement-first prices while keeping history authoritative.

    An official live settlement may fill a historical row whose official
    settlement is absent. A historical last price is only used after both
    sources' official settlements have been considered.
    """
    history = merged.get("settle__history", pd.Series(np.nan, index=merged.index))
    live = merged.get("settle__live", pd.Series(np.nan, index=merged.index))
    history_kind = merged.get(
        "settle_kind__history", pd.Series(pd.NA, index=merged.index, dtype="string")
    ).astype("string")
    live_kind = merged.get(
        "settle_kind__live", pd.Series(pd.NA, index=merged.index, dtype="string")
    ).astype("string")

    official_kinds = {"settlement", "settlement_scaled"}
    history_official = history.notna() & history_kind.isin(official_kinds)
    live_official = live.notna() & live_kind.isin(official_kinds)
    conditions = [
        history_official,
        ~history_official & live_official,
        ~history_official & ~live_official & history.notna(),
        ~history_official & ~live_official & history.isna() & live.notna(),
    ]
    value = pd.Series(np.nan, index=merged.index, dtype=float)
    source = pd.Series(pd.NA, index=merged.index, dtype="string")
    kind = pd.Series(pd.NA, index=merged.index, dtype="string")
    for condition, selected, selected_source, selected_kind in zip(
        conditions,
        (history, live, history, live),
        ("history", "live_fallback", "history_last", "live_last_fallback"),
        (history_kind, live_kind, history_kind, live_kind),
    ):
        value.loc[condition] = selected.loc[condition]
        source.loc[condition] = selected_source
        kind.loc[condition] = selected_kind.loc[condition]
    return value, source, kind


def _session_age(
    dates: pd.Series,
    asof_dates: pd.Series,
    session_rank: dict[pd.Timestamp, int],
) -> pd.Series:
    date_rank = dates.map(session_rank)
    asof_rank = asof_dates.map(session_rank)
    return (date_rank - asof_rank).astype("Float64")


def _fill_activity_from_recent_history(
    panel: pd.DataFrame,
    history: pd.DataFrame,
    *,
    field: str,
    max_age_sessions: int,
    session_rank: dict[pd.Timestamp, int],
) -> pd.DataFrame:
    value_column = field
    source_column = f"{field}_source"
    asof_column = f"{field}_asof_date"
    age_column = f"{field}_age_sessions"
    estimated_column = f"{field}_is_estimated"

    out = panel.copy()
    out[asof_column] = out["date"].where(out[value_column].notna())
    out[age_column] = pd.Series(0.0, index=out.index).where(out[value_column].notna())
    out[estimated_column] = False

    if history.empty or field not in history.columns:
        return out

    missing = out[value_column].isna()
    if not missing.any():
        return out

    observations = history.loc[history[field].notna(), ["date", "contract", field]].copy()
    if observations.empty:
        return out
    observations = observations.rename(columns={"date": asof_column, field: "estimated_value"})

    left = out.loc[missing, ["date", "contract"]].sort_values(["date", "contract"])
    right = observations.sort_values([asof_column, "contract"])
    left["contract"] = left["contract"].astype(str)
    right["contract"] = right["contract"].astype(str)
    # pandas requires the as-of key to be globally monotone even when `by` is
    # supplied, hence date is the primary sort key above.
    estimated = pd.merge_asof(
        left,
        right,
        left_on="date",
        right_on=asof_column,
        by="contract",
        direction="backward",
        allow_exact_matches=False,
    )
    estimated[age_column] = _session_age(
        estimated["date"], estimated[asof_column], session_rank
    )
    valid = estimated[age_column].between(1, max_age_sessions, inclusive="both")
    if not valid.any():
        return out

    estimated = estimated.loc[valid]
    keyed = pd.MultiIndex.from_frame(out[["date", "contract"]])
    estimate_keys = pd.MultiIndex.from_frame(estimated[["date", "contract"]])
    positions = keyed.get_indexer(estimate_keys)
    out.iloc[positions, out.columns.get_loc(value_column)] = estimated["estimated_value"].to_numpy()
    out.iloc[positions, out.columns.get_loc(source_column)] = "history_estimate"
    out.iloc[positions, out.columns.get_loc(asof_column)] = estimated[asof_column].to_numpy()
    out.iloc[positions, out.columns.get_loc(age_column)] = estimated[age_column].to_numpy()
    out.iloc[positions, out.columns.get_loc(estimated_column)] = True
    return out


def load_contract_panel(config: CarryBuildConfig) -> pd.DataFrame:
    """Load a timestamp-safe, field-level merged contract panel."""
    symbol = config.normalized_symbol
    history, live = _load_source_frames(symbol, config.commodity_dir)
    if history.empty and live.empty:
        raise FileNotFoundError(f"No contract data found for {symbol} under {config.commodity_dir}")

    index_columns = ["date", "contract"]
    history_indexed = history.set_index(index_columns).add_suffix("__history") if not history.empty else None
    live_indexed = live.set_index(index_columns).add_suffix("__live") if not live.empty else None
    if history_indexed is None:
        merged = live_indexed.reset_index()
    elif live_indexed is None:
        merged = history_indexed.reset_index()
    else:
        merged = history_indexed.join(live_indexed, how="outer").reset_index()

    merged = merged.sort_values(index_columns).reset_index(drop=True)
    out = merged[index_columns].copy()
    out["settle"], out["settle_source"], out["settle_kind"] = _history_first_settle(
        merged
    )
    for field in ("open", "high", "low", "volume", "open_interest"):
        out[field], out[f"{field}_source"] = _history_first_field(
            merged,
            field=field,
        )

    all_dates = sorted(pd.Timestamp(value) for value in out["date"].dropna().unique())
    session_rank = {date: rank for rank, date in enumerate(all_dates)}
    out = _fill_activity_from_recent_history(
        out,
        history,
        field="volume",
        max_age_sessions=config.volume_staleness_sessions,
        session_rank=session_rank,
    )
    out = _fill_activity_from_recent_history(
        out,
        history,
        field="open_interest",
        max_age_sessions=config.oi_staleness_sessions,
        session_rank=session_rank,
    )

    out["contract_month"] = out["contract"].map(contract_month_start)
    maturity = {
        contract: contract_maturity(contract, symbol=symbol, observed_history=history)
        for contract in out["contract"].dropna().unique()
    }
    out["maturity"] = out["contract"].map(maturity)
    out["tm"] = (out["maturity"] - out["date"]).dt.days / DAYS_IN_YEAR
    out = out.sort_values(["contract", "date"]).reset_index(drop=True)
    positive = out["settle"].gt(0)
    prior = out.groupby("contract", observed=True)["settle"].shift(1)
    contract_ratio = (out["settle"] / prior).where(positive & prior.gt(0))
    out["contract_ret"] = np.log(contract_ratio)
    out["ret_std_20"] = out.groupby("contract", observed=True)["contract_ret"].transform(
        lambda values: values.rolling(20, min_periods=20).std()
    )
    out["close_diff_30d"] = out.groupby("contract", observed=True)["settle"].diff(30)
    prior_close = out.groupby("contract", observed=True)["settle"].shift(1)
    true_range = pd.concat(
        [
            (out["high"] - out["low"]).abs(),
            (out["high"] - prior_close).abs(),
            (out["low"] - prior_close).abs(),
        ],
        axis=1,
    ).max(axis=1)
    out["atr_14"] = true_range.groupby(out["contract"], observed=True).transform(
        lambda values: values.rolling(14, min_periods=14).mean()
    )
    return out.sort_values(["date", "contract"]).reset_index(drop=True)


def _last_business_day(year: int, month: int) -> pd.Timestamp:
    return pd.Timestamp(year=year, month=month, day=1) + pd.offsets.BMonthEnd(0)


def _nth_business_day_before(date: pd.Timestamp, count: int) -> pd.Timestamp:
    return date - pd.offsets.BDay(count)


def _convention_maturity(contract: str, symbol: str) -> pd.Timestamp:
    year, month = contract_sort_key(contract)
    symbol = symbol.upper()
    month_start = pd.Timestamp(year=year, month=month, day=1)

    if symbol == "CL":
        prior_month_25 = month_start - pd.offsets.MonthBegin(1) + pd.Timedelta(days=24)
        # Approximate the NYMEX rule used in the legacy source: three business
        # days before the 25th, with an extra day when the 25th is not a weekday.
        count = 3 if prior_month_25.weekday() < 5 else 4
        return _nth_business_day_before(prior_month_25, count)
    if symbol == "CO":
        second_prior = month_start - pd.offsets.MonthBegin(2)
        return _last_business_day(second_prior.year, second_prior.month)
    if symbol == "NG":
        return _nth_business_day_before(month_start, 3)
    if symbol in {"HO", "XB"}:
        prior = month_start - pd.offsets.MonthBegin(1)
        return _last_business_day(prior.year, prior.month)
    if symbol in {"GC", "SI", "HG", "PA", "PL"}:
        return _nth_business_day_before(_last_business_day(year, month), 2)
    if symbol in CRYPTO_SYMBOLS:
        month_end = pd.Timestamp(year=year, month=month, day=1) + pd.offsets.MonthEnd(0)
        return month_end - pd.Timedelta(days=(month_end.weekday() - 4) % 7)
    return _nth_business_day_before(_last_business_day(year, month), 4)


def contract_maturity(
    contract: str,
    *,
    symbol: str,
    observed_history: pd.DataFrame | None = None,
) -> pd.Timestamp:
    """Return an approximate last-trade maturity without live-data lookahead."""
    convention = _convention_maturity(contract, symbol)
    known_symbols = ENERGY_SYMBOLS | CRYPTO_SYMBOLS | {"GC", "SI", "HG", "PA", "PL"}
    if symbol.upper() in known_symbols or observed_history is None or observed_history.empty:
        return convention

    rows = observed_history.loc[
        observed_history["contract"].eq(contract) & observed_history["settle"].notna(),
        "date",
    ]
    if rows.empty:
        return convention
    observed_last = pd.Timestamp(rows.max()).normalize()
    history_end = pd.Timestamp(observed_history["date"].max()).normalize()
    if observed_last < history_end - pd.Timedelta(days=30) and abs((observed_last - convention).days) <= 62:
        return observed_last
    return convention


def _eligible_months(symbol: str) -> tuple[int, ...]:
    return ACTIVE_CONTRACT_MONTHS_BY_SYMBOL.get(symbol.upper(), ALL_CONTRACT_MONTHS)


def _evidence_key(row: pd.Series, field: str) -> tuple[object]:
    # A carried-forward observation does not become fresh evidence merely
    # because its source label changes from history to history_estimate.
    return (row.get(f"{field}_asof_date"),)


def select_front_contracts(
    panel: pd.DataFrame,
    *,
    symbol: str,
    confirmation_observations: int = 2,
    allowed_months: Sequence[int] | None = None,
    max_maturity_years: float = 0.75,
    initialize_from_nearest: bool = False,
    stepwise: bool = True,
) -> pd.Series:
    """Select a no-lookahead, monotone front chain with roll hysteresis."""
    allowed = set(allowed_months or _eligible_months(symbol))
    working = panel.loc[
        panel["contract_month"].dt.month.isin(allowed)
        & panel["settle"].notna()
        & panel["tm"].between(0, max_maturity_years, inclusive="neither")
    ].copy()
    dates = sorted(panel["date"].dropna().unique())
    selected = pd.Series(pd.NA, index=pd.Index(dates, name="date"), dtype="string")
    maturity_by_contract = panel.groupby("contract")["maturity"].max()

    current: str | None = None
    candidate: str | None = None
    confirmations = 0
    last_evidence: tuple[object, ...] | None = None

    for date in dates:
        day = working.loc[working["date"].eq(date)].copy()
        if day.empty:
            selected.loc[date] = current if current is not None else pd.NA
            continue
        day["sort_key"] = day["contract"].map(contract_sort_key)
        day = day.sort_values("sort_key")

        if current is not None and current not in set(day["contract"]):
            current_maturity = maturity_by_contract.get(current, pd.NaT)
            if pd.notna(current_maturity) and pd.Timestamp(date) < pd.Timestamp(
                current_maturity
            ):
                # Missing settlement is not evidence that an unexpired
                # contract ceased trading. Keep the contract and expose a
                # missing chained price instead of jumping across several
                # temporarily absent intermediate contracts.
                candidate = None
                confirmations = 0
                last_evidence = None
                selected.loc[date] = current
                continue
            current_key = contract_sort_key(current)
            later = day.loc[
                day["contract"].map(lambda value: contract_sort_key(value) > current_key)
            ]
            if not later.empty:
                current = str(later.iloc[0]["contract"])
            else:
                selected.loc[date] = current
                continue
            candidate = None
            confirmations = 0
            last_evidence = None

        if current is None:
            if initialize_from_nearest:
                current = str(day.iloc[0]["contract"])
            else:
                use_oi = day["open_interest"].notna().any()
                initial_field = "open_interest" if use_oi else "volume"
                ranked = day.loc[day[initial_field].notna()].sort_values(
                    [initial_field, "sort_key"],
                    ascending=[False, True],
                    kind="mergesort",
                )
                current = (
                    str(ranked.iloc[0]["contract"])
                    if not ranked.empty
                    else str(day.iloc[0]["contract"])
                )

        current_key = contract_sort_key(current)
        current_rows = day.loc[day["contract"].eq(current)]
        if stepwise:
            comparison = current_rows
            nearest = str(day.iloc[0]["contract"])
            # A voluntary roll may put the chain one contract ahead of the
            # nearest still-usable month. Freeze there until that older month
            # disappears; otherwise repeated two-day confirmations can walk a
            # monthly chain several contracts forward long before expiry.
            if current == nearest:
                later_rows = day.loc[
                    day["contract"].map(lambda value: contract_sort_key(value) > current_key)
                ]
                if not later_rows.empty:
                    comparison = pd.concat(
                        [comparison, later_rows.iloc[[0]]], ignore_index=False
                    )
        else:
            comparison = day

        use_oi = comparison["open_interest"].notna().any()
        field = "open_interest" if use_oi else "volume"
        ranked = comparison.loc[comparison[field].notna()].sort_values(
            [field, "sort_key"], ascending=[False, True], kind="mergesort"
        )
        if ranked.empty:
            leader = current
            leader_row = current_rows.iloc[0]
        else:
            leader_row = ranked.iloc[0]
            leader = str(leader_row["contract"])

        if contract_sort_key(leader) > current_key:
            current_rows = day.loc[day["contract"].eq(current)]
            current_row = current_rows.iloc[0] if not current_rows.empty else leader_row
            evidence = (
                field,
                *_evidence_key(leader_row, field),
                *_evidence_key(current_row, field),
            )
            if candidate != leader:
                candidate = leader
                confirmations = 1
                last_evidence = evidence
            elif evidence != last_evidence:
                confirmations += 1
                last_evidence = evidence
            if confirmations >= confirmation_observations:
                current = leader
                candidate = None
                confirmations = 0
                last_evidence = None
        else:
            candidate = None
            confirmations = 0
            last_evidence = None

        selected.loc[date] = current

    return selected


def _next_contracts(
    front: pd.Series,
    *,
    contract_universe: Sequence[str],
    count: int,
) -> pd.DataFrame:
    ordered = sorted(set(contract_universe), key=contract_sort_key)
    positions = {contract: index for index, contract in enumerate(ordered)}
    output: dict[str, list[object]] = {f"M{leg}_con": [] for leg in range(1, count + 1)}
    for contract in front:
        position = positions.get(str(contract))
        for leg in range(1, count + 1):
            target = position + leg if position is not None else None
            output[f"M{leg}_con"].append(ordered[target] if target is not None and target < len(ordered) else pd.NA)
    return pd.DataFrame(output, index=front.index)


def _extract_chain_fields(
    panel: pd.DataFrame,
    contracts: pd.Series,
    *,
    prefix: str,
) -> pd.DataFrame:
    selector = pd.DataFrame(
        {"date": contracts.index, "contract": contracts.to_numpy()},
    )
    fields = [
        "date",
        "contract",
        "settle",
        "settle_source",
        "settle_kind",
        "volume",
        "volume_source",
        "volume_asof_date",
        "volume_age_sessions",
        "volume_is_estimated",
        "open_interest",
        "open_interest_source",
        "open_interest_asof_date",
        "open_interest_age_sessions",
        "open_interest_is_estimated",
        "contract_ret",
        "ret_std_20",
        "close_diff_30d",
        "atr_14",
        "high",
        "low",
        "maturity",
    ]
    merged = selector.merge(panel[fields], on=["date", "contract"], how="left")
    merged.index = contracts.index
    return merged.rename(
        columns={
            "contract": f"{prefix}_con",
            "settle": f"{prefix}_settle",
            "settle_source": f"{prefix}_settle_source",
            "settle_kind": f"{prefix}_settle_kind",
            "volume": f"{prefix}_volume",
            "volume_source": f"{prefix}_volume_source",
            "volume_asof_date": f"{prefix}_volume_asof_date",
            "volume_age_sessions": f"{prefix}_volume_age_sessions",
            "volume_is_estimated": f"{prefix}_volume_is_estimated",
            "open_interest": f"{prefix}_open_interest",
            "open_interest_source": f"{prefix}_open_interest_source",
            "open_interest_asof_date": f"{prefix}_open_interest_asof_date",
            "open_interest_age_sessions": f"{prefix}_open_interest_age_sessions",
            "open_interest_is_estimated": f"{prefix}_open_interest_is_estimated",
            "contract_ret": f"{prefix.lower()}_ret",
            "ret_std_20": f"{prefix}_ret_std_20",
            "close_diff_30d": f"{prefix}_close_diff_30d",
            "atr_14": f"{prefix}_atr_14",
            "high": f"{prefix}_high",
            "low": f"{prefix}_low",
            "maturity": f"{prefix}_maturity",
        }
    ).drop(columns="date")


def _best_monotonic_path(day: pd.DataFrame, *, non_decreasing: bool) -> list[int]:
    """Return one deterministic best LIS path without enumerating ties."""
    if day.empty:
        return []
    prices = day["settle"].to_numpy(dtype=float)
    oi = day["open_interest"].fillna(0.0).to_numpy(dtype=float)
    volume = day["volume"].fillna(0.0).to_numpy(dtype=float)
    contracts = day["contract"].astype(str).tolist()
    paths: list[tuple[int, ...]] = []
    scores: list[tuple[int, float, float]] = []

    for i in range(len(day)):
        best_path = (i,)
        best_score = (1, oi[i], volume[i])
        for j in range(i):
            monotonic = prices[j] <= prices[i] if non_decreasing else prices[j] >= prices[i]
            if not monotonic:
                continue
            candidate_path = (*paths[j], i)
            candidate_score = (scores[j][0] + 1, scores[j][1] + oi[i], scores[j][2] + volume[i])
            if candidate_score > best_score:
                best_path, best_score = candidate_path, candidate_score
            elif candidate_score == best_score:
                old_names = tuple(contracts[k] for k in best_path)
                new_names = tuple(contracts[k] for k in candidate_path)
                if new_names < old_names:
                    best_path = candidate_path
        paths.append(best_path)
        scores.append(best_score)

    best = 0
    for i in range(1, len(paths)):
        if scores[i] > scores[best]:
            best = i
        elif scores[i] == scores[best]:
            if tuple(contracts[k] for k in paths[i]) < tuple(contracts[k] for k in paths[best]):
                best = i
    return list(paths[best])


def _carry_from_curve(curve: pd.DataFrame, target: float) -> float:
    if len(curve) < 2:
        return np.nan
    times = curve["tm"].to_numpy(dtype=float)
    insertion = int(np.searchsorted(times, target, side="left"))
    if insertion <= 0:
        left, right = 0, 1
    elif insertion >= len(times):
        left, right = len(times) - 2, len(times) - 1
    else:
        left, right = insertion - 1, insertion
    time_gap = times[right] - times[left]
    near = float(curve.iloc[left]["settle"])
    far = float(curve.iloc[right]["settle"])
    if time_gap <= 0 or time_gap > MAX_LIS_LEG_GAP_YEARS or near <= 0 or far <= 0:
        return np.nan
    return float(np.log(far / near) / time_gap)


def calculate_lis_carries(
    panel: pd.DataFrame,
    *,
    symbol: str,
    targets: Iterable[float],
    ratio: float = 0.60,
    activity_threshold: float = 0.005,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    allowed = set(_eligible_months(symbol))
    for date, raw_day in panel.groupby("date", sort=True):
        day = raw_day.loc[
            raw_day["contract_month"].dt.month.isin(allowed)
            & raw_day["tm"].gt(0)
            & raw_day["settle"].gt(0)
        ].sort_values(["maturity", "contract"]).copy()
        field = "volume" if day["volume"].fillna(0).sum() > 0 else "open_interest"
        total_activity = day[field].fillna(0).sum()
        if total_activity > 0:
            day = day.loc[day[field].fillna(0).ge(total_activity * activity_threshold)].copy()
        else:
            day = day.iloc[0:0]

        contango_idx = _best_monotonic_path(day, non_decreasing=True)
        backwardation_idx = _best_monotonic_path(day, non_decreasing=False)
        contango = day.iloc[contango_idx] if contango_idx else day.iloc[0:0]
        backwardation = day.iloc[backwardation_idx] if backwardation_idx else day.iloc[0:0]
        n = len(day)
        curve = day.iloc[0:0]
        direction = "none"
        if n and len(contango) / n >= ratio:
            curve = contango
            direction = "contango"
        elif n and len(backwardation) / n >= ratio:
            curve = backwardation
            direction = "backwardation"

        row: dict[str, object] = {
            "date": date,
            "contango": len(contango),
            "backwardation": len(backwardation),
            "lis_curve_contracts": "|".join(curve["contract"].astype(str)),
            "lis_curve_direction": direction,
            "lis_activity_field": field,
        }
        for target in targets:
            label = f"lis_carry_{target:.2f}y".replace(".", "p")
            row[label] = _carry_from_curve(curve, target)
        rows.append(row)
    return pd.DataFrame(rows).set_index("date")


def _annualized_carry(
    near_price: pd.Series,
    far_price: pd.Series,
    near_maturity: pd.Series,
    far_maturity: pd.Series,
) -> pd.Series:
    years = (pd.to_datetime(far_maturity) - pd.to_datetime(near_maturity)).dt.days / DAYS_IN_YEAR
    ratio = pd.to_numeric(far_price, errors="coerce") / pd.to_numeric(near_price, errors="coerce")
    return np.log(ratio.where(ratio.gt(0))) / years.where(years.gt(0))


def _anchor_months(symbol: str) -> tuple[int, ...]:
    return ANCHOR_MONTHS_BY_SYMBOL.get(symbol.upper(), (3, 6, 9, 12))


def _anchor_pairs(symbol: str, months: Sequence[int]) -> tuple[tuple[int, int], ...]:
    if symbol.upper() in ENERGY_SYMBOLS:
        return ENERGY_CALENDAR_PAIRS
    adjacent = list(zip(months, months[1:]))
    adjacent.append((months[-1], months[0]))
    if 12 in months:
        adjacent.append((12, 12))
    return tuple(adjacent)


def build_carry_frame(config: CarryBuildConfig) -> pd.DataFrame:
    panel = load_contract_panel(config)
    symbol = config.normalized_symbol
    dates = pd.Index(sorted(panel["date"].unique()), name="date")
    active = set(_eligible_months(symbol))
    universe = sorted(
        {
            contract
            for contract in panel["contract"].astype(str)
            if contract_sort_key(contract)[1] in active
        },
        key=contract_sort_key,
    )

    m0 = select_front_contracts(
        panel,
        symbol=symbol,
        confirmation_observations=config.roll_confirmation_observations,
        initialize_from_nearest=symbol in MONTHLY_STEPWISE_FRONT_SYMBOLS,
        stepwise=symbol in MONTHLY_STEPWISE_FRONT_SYMBOLS,
    ).reindex(dates)
    chain_contracts = pd.DataFrame({"M0_con": m0}, index=dates)
    chain_contracts = chain_contracts.join(
        _next_contracts(m0, contract_universe=universe, count=11)
    )

    output = pd.DataFrame(index=dates)
    for leg in range(3):
        output = output.join(
            _extract_chain_fields(panel, chain_contracts[f"M{leg}_con"], prefix=f"M{leg}")
        )

    output["M0_ret"] = output["m0_ret"].cumsum()
    output["M1_ret"] = output["m1_ret"].cumsum()
    output["M2_ret"] = output["m2_ret"].cumsum()
    output["high"] = output["M0_high"]
    output["low"] = output["M0_low"]

    valid_panel = panel.loc[
        panel["contract_month"].dt.month.isin(active) & panel["tm"].gt(0)
    ]
    totals = valid_panel.groupby("date", observed=True).agg(
        total_volume=("volume", lambda values: values.sum(min_count=1)),
        total_oi=("open_interest", lambda values: values.sum(min_count=1)),
    )
    output = output.join(totals)

    lis = calculate_lis_carries(
        panel,
        symbol=symbol,
        targets=config.lis_targets,
        ratio=config.lis_ratio,
        activity_threshold=config.activity_threshold,
    )
    output = output.join(lis)
    legacy_label = f"lis_carry_{config.legacy_carry_target:.2f}y".replace(".", "p")
    output["carry"] = output[legacy_label]

    for far_leg, label in ((1, "front_second"), (2, "front_third"), (5, "front_sixth"), (11, "front_twelfth")):
        far = _extract_chain_fields(panel, chain_contracts[f"M{far_leg}_con"], prefix=f"X{far_leg}")
        output[f"chain_{label}_annualized_carry"] = _annualized_carry(
            output["M0_settle"],
            far[f"X{far_leg}_settle"],
            output["M0_maturity"],
            far[f"X{far_leg}_maturity"],
        )
    output["chain_second_third_annualized_carry"] = _annualized_carry(
        output["M1_settle"],
        output["M2_settle"],
        output["M1_maturity"],
        output["M2_maturity"],
    )

    anchor_contracts: dict[int, pd.Series] = {}
    anchor_columns: dict[str, pd.Series] = {}
    for month in _anchor_months(symbol):
        code = FUTURES_MONTH_NUMBERS[month]
        selected = select_front_contracts(
            panel,
            symbol=symbol,
            confirmation_observations=config.roll_confirmation_observations,
            allowed_months=(month,),
            max_maturity_years=1.50,
            initialize_from_nearest=True,
            stepwise=True,
        ).reindex(dates)
        anchor_contracts[month] = selected
        anchor = _extract_chain_fields(panel, selected, prefix=code)
        anchor_columns[f"{code}_con"] = anchor[f"{code}_con"]
        anchor_columns[f"{code}_settle"] = anchor[f"{code}_settle"]
        anchor_columns[f"{code}_ret"] = anchor[f"{code.lower()}_ret"]
        anchor_columns[f"{code}_settle_source"] = anchor[f"{code}_settle_source"]
        anchor_columns[f"{code}_settle_kind"] = anchor[f"{code}_settle_kind"]
        anchor_columns[f"{code}_volume"] = anchor[f"{code}_volume"]
        anchor_columns[f"{code}_volume_source"] = anchor[f"{code}_volume_source"]
        anchor_columns[f"{code}_volume_asof_date"] = anchor[f"{code}_volume_asof_date"]
        anchor_columns[f"{code}_volume_age_sessions"] = anchor[f"{code}_volume_age_sessions"]
        anchor_columns[f"{code}_volume_is_estimated"] = anchor[f"{code}_volume_is_estimated"]
        anchor_columns[f"{code}_open_interest"] = anchor[f"{code}_open_interest"]
        anchor_columns[f"{code}_open_interest_source"] = anchor[f"{code}_open_interest_source"]
        anchor_columns[f"{code}_open_interest_asof_date"] = anchor[
            f"{code}_open_interest_asof_date"
        ]
        anchor_columns[f"{code}_open_interest_age_sessions"] = anchor[
            f"{code}_open_interest_age_sessions"
        ]
        anchor_columns[f"{code}_open_interest_is_estimated"] = anchor[
            f"{code}_open_interest_is_estimated"
        ]
        anchor_columns[f"{code}_maturity"] = anchor[f"{code}_maturity"]

    output = pd.concat([output, pd.DataFrame(anchor_columns, index=dates)], axis=1)

    universe_set = set(panel["contract"].astype(str))
    calendar_columns: dict[str, pd.Series] = {}
    for near_month, far_month in _anchor_pairs(symbol, tuple(anchor_contracts)):
        near_code = FUTURES_MONTH_NUMBERS[near_month]
        far_code = FUTURES_MONTH_NUMBERS[far_month]
        near_contract = anchor_contracts[near_month]
        far_contract_values: list[object] = []
        for contract in near_contract:
            if pd.isna(contract):
                far_contract_values.append(pd.NA)
                continue
            year, month = contract_sort_key(str(contract))
            far_year = year + int(far_month <= month)
            candidate = f"{far_year}{far_code}"
            far_contract_values.append(candidate if candidate in universe_set else pd.NA)
        far_contract = pd.Series(far_contract_values, index=dates, dtype="string")
        pair = f"calendar_{near_code}_{far_code}"
        calendar_columns[f"{pair}_near_con"] = near_contract
        calendar_columns[f"{pair}_far_con"] = far_contract
        far_selector = pd.DataFrame({"date": dates, "contract": far_contract.to_numpy()})
        far_values = far_selector.merge(
            panel[["date", "contract", "settle", "maturity"]],
            on=["date", "contract"],
            how="left",
        ).set_index("date")
        calendar_columns[f"{pair}_annualized_carry"] = _annualized_carry(
            output[f"{near_code}_settle"],
            far_values["settle"],
            output[f"{near_code}_maturity"],
            far_values["maturity"],
        )

    output = pd.concat([output, pd.DataFrame(calendar_columns, index=dates)], axis=1)
    output = output.copy()

    output["carry_360_perc"] = output["carry"].rolling(360, min_periods=30).rank(pct=True)
    output["arrival"] = (
        pd.Series(output.index, index=output.index).dt.normalize()
        + pd.Timedelta(days=1, hours=config.arrival_hour_utc)
    )

    # Keep the legacy columns first; append richer diagnostics after them.
    legacy_first = [
        "carry",
        "contango",
        "backwardation",
        "m0_ret",
        "m1_ret",
        "m2_ret",
        "M0_ret",
        "M1_ret",
        "M2_ret",
        "M0_con",
        "M1_con",
        "M2_con",
        "M0_settle",
        "M1_settle",
        "M2_settle",
        "M0_volume",
        "M1_volume",
        "M2_volume",
        "high",
        "low",
        "M0_ret_std_20",
        "M1_ret_std_20",
        "M2_ret_std_20",
        "M0_close_diff_30d",
        "M1_close_diff_30d",
        "M2_close_diff_30d",
        "M0_atr_14",
        "M1_atr_14",
        "M2_atr_14",
        "total_volume",
        "total_oi",
        "carry_360_perc",
        "arrival",
    ]
    ordered = [column for column in legacy_first if column in output]
    ordered.extend(column for column in output.columns if column not in ordered)
    return output[ordered].reset_index()


def write_carry_frame(frame: pd.DataFrame, output_path: Path, *, overwrite: bool = False) -> Path:
    if output_path.exists() and not overwrite:
        raise FileExistsError(f"Refusing to overwrite existing carry file: {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    out = frame.copy().sort_values("date", ascending=False)
    out["date"] = pd.to_datetime(out["date"]).dt.strftime("%Y-%m-%d")
    out.to_csv(output_path, index=False, float_format="%.8f")
    return output_path
