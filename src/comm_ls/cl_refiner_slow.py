"""Approved slow refiner state, shared by live inputs and parity diagnostics."""
from pathlib import Path

import numpy as np
import pandas as pd

from comm_ls.cl_v32_strategy import SleeveConfig

REFINER_BLEND_EFFECTIVE_DATE = '2026-10-26'
REFINER_SLOW_CONFIG = SleeveConfig(
    weight=.10, tickers=('DINO', 'DK', 'PBF', 'PSX'),
    feature_symbol='REFINER_SLOW', feature='refiner_slow_state', threshold=1.25,
    side_mult=1, position_mode='sign', hold_days=None, rolling_days=None,
    sector_hedge='XLE', internal_weights={'DK': .3, 'DINO': .2, 'PBF': .3, 'PSX': .2},
    signal_rule='refiner_slow_precomputed')
HO_FEATURE = 'feature_value__front_third_annualized_carry'


def refiner_slow_signal(carry, cl_m1_return, *, updated=False):
    """Exact executed notebook rule; 50 lookback, no fixed hold or smoothing.

    Historical missing CL returns follow the notebook's zero substitution.
    Live decision lookbacks are independently fail-closed by validate_live_inputs.
    """
    carry = pd.to_numeric(carry, errors='raise').sort_index()
    cl = pd.to_numeric(cl_m1_return, errors='raise').reindex(carry.index).fillna(0.)
    momentum = cl.rolling(10, min_periods=5).sum()
    cl_vol = cl.rolling(20, min_periods=10).std()
    sd = carry.rolling(60, min_periods=30).std()
    long = pd.Series(np.nan, index=carry.index)
    short = long.copy()
    change = carry.ffill().diff(50) if updated else carry.diff(50)
    long.loc[(change > sd*1.25) & (momentum > -cl_vol*.5)] = 1.
    long.loc[carry.ffill().diff(50) < sd*.95] = 0.
    short.loc[(change < -sd*1.25) & (momentum < cl_vol*.5)] = -1.
    short.loc[carry.ffill().diff(50) > -sd*.95] = 0.
    long.loc[carry.isna()] = 0.
    short.loc[carry.isna()] = 0.
    return long.ffill().fillna(0.) + short.ffill().fillna(0.)


def load_inputs(root, gate_symbol='CL'):
    root = Path(root)
    cache = pd.read_parquet(root/'data/cache/feature_return_observation_v1/HO-multi_return_2.parquet',
        columns=['date', 'ticker', HO_FEATURE, 'feature_alignment_mode', 'commodity_arrival'])
    cache = cache[cache.ticker.isin(REFINER_SLOW_CONFIG.tickers)].copy()
    cache['date'] = pd.to_datetime(cache.date).dt.normalize()
    if cache.duplicated(['date', 'ticker']).any():
        raise ValueError('Duplicate refiner_slow HO cache dates/tickers')
    if set(cache.feature_alignment_mode.dropna()) != {'stock_observation_asof'}:
        raise ValueError('refiner_slow requires HO _2 stock_observation_asof inputs')
    cl = pd.read_csv(root/f'data/comm/carry_data/{gate_symbol}.csv',
                     usecols=['date', 'm0_ret', 'm1_ret', 'arrival'], parse_dates=['date'])
    if cl.date.duplicated().any():
        raise ValueError('Duplicate refiner_slow CL carry dates')
    return cache.sort_values('date'), cl.set_index('date').sort_index()


def load_refiner_slow_features(root, *, updated=False, ho_gate=False):
    cache, cl = load_inputs(root, gate_symbol='HO') if ho_gate else load_inputs(root)
    carry = cache.loc[cache.ticker.eq('DINO')].set_index('date')[HO_FEATURE]
    if carry.empty:
        raise ValueError('Missing DINO HO feature history for refiner_slow')
    feature = 'refiner_slow_state_v3' if ho_gate else ('refiner_slow_state_v2' if updated else 'refiner_slow_state')
    state = refiner_slow_signal(carry, cl.m1_ret if ho_gate else (cl.m0_ret if updated else cl.m1_ret),
                                updated=updated or ho_gate).to_frame(feature)
    state['__feature_observed__' + feature] = True
    return state


def validate_live_inputs(root, as_of, target_date):
    """Current native-stock-calendar lookbacks must be complete and known by entry."""
    day = pd.Timestamp(as_of).normalize()
    target = pd.Timestamp(target_date).normalize()
    ho_gate = target >= pd.Timestamp('2026-11-02')
    cache, cl = load_inputs(root, gate_symbol='HO') if ho_gate else load_inputs(root)
    updated = target >= pd.Timestamp('2026-10-28')
    return_column = 'm0_ret' if updated and not ho_gate else 'm1_ret'
    opening = target.tz_localize('America/New_York') + pd.Timedelta(hours=9, minutes=30)
    rows = []
    for ticker in REFINER_SLOW_CONFIG.tickers:
        if ho_gate and ticker == 'PSX':
            continue
        local = cache.loc[cache.ticker.eq(ticker)].set_index('date').loc[:day]
        lookback = local.tail(60)
        if (len(lookback) < 60 or lookback.index[-1] != day
                or not np.isfinite(lookback[HO_FEATURE]).all()):
            raise ValueError(f'Incomplete refiner_slow HO decision lookback for {ticker} at {day.date()}')
        gate = cl.reindex(local.index).tail(20)
        if len(gate) != 20 or not np.isfinite(gate[return_column]).all():
            raise ValueError(f'Incomplete refiner_slow CL {return_column} decision lookback for {ticker}')
        for label, arrivals in [('HO', lookback.commodity_arrival), ('CL', gate.arrival)]:
            known = pd.to_datetime(arrivals)
            if known.dt.tz is None:
                known = known.dt.tz_localize('Asia/Hong_Kong')
            if known.isna().any() or (known > opening).any():
                raise ValueError(f'Late/missing {label} arrival for refiner_slow {ticker}')
        state = refiner_slow_signal(local[HO_FEATURE], cl[return_column], updated=updated)
        rows.append(dict(instrument=ticker, as_of=day, target_date=target,
                         gate_symbol='HO' if ho_gate else 'CL',
                         ho_carry=local[HO_FEATURE].iloc[-1],
                         cl_return_column=return_column,
                         cl_return=gate[return_column].iloc[-1], signal=state.iloc[-1]))
    if len({row['signal'] for row in rows}) != 1:
        raise ValueError('refiner_slow current ticker states disagree; review native-calendar histories')
    return pd.DataFrame(rows)
