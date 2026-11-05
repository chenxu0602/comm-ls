"""Approved 2026-11-02 quarterly refiner state; SPY + XLE, full balance."""
from pathlib import Path
import numpy as np
import pandas as pd
from comm_ls.cl_v32_strategy import SleeveConfig

RE_C03_CONFIG = SleeveConfig(weight=.20, tickers=('DINO','MPC','VLO'),
    feature_symbol='REFINERY_QUARTERLY', feature='re_c03_state', threshold=1.,
    side_mult=1, position_mode='sign', hold_days=None, rolling_days=None,
    sector_hedge='XLE', internal_weights={'DINO':.2,'MPC':.3,'VLO':.5},
    signal_rule='re_c03_precomputed')
INPUTS = ['crack_03_quarterly_near_ma_gap_3d_30d',
          'crack_03_quarterly_far_change_5d',
          'crack_03_quarterly_far_same_contract_std_30']


def re_c03_signal(frame):
    """Exact notebook assignment precedence; missing history does not fabricate updates."""
    entry, exit_, vol = (pd.to_numeric(frame[c],errors='raise') for c in INPUTS)
    long = pd.Series(np.nan,index=frame.index)
    short = long.copy()
    long.loc[entry > vol] = 1.
    long.loc[exit_ < vol*.5] = 0.
    short.loc[entry < -vol] = -1.
    short.loc[exit_ > -vol*.5] = 0.
    return long.ffill().fillna(0.) + short.ffill().fillna(0.)


def load_inputs(root):
    root = Path(root)
    from comm_ls.etf_research import load_refinery_crack_data
    crack = load_refinery_crack_data(root=root,include_quarterly=True)
    cache = pd.read_parquet(root/'data/cache/feature_return_observation_v1/HO-multi_return_2.parquet',
        columns=['date','ticker','feature_alignment_mode'])
    cache = cache.loc[cache.ticker.isin(RE_C03_CONFIG.tickers)].copy()
    cache['date'] = pd.to_datetime(cache.date).dt.normalize()
    if cache.duplicated(['date','ticker']).any():
        raise ValueError('Duplicate re_c03 stock calendar rows')
    if set(cache.feature_alignment_mode.dropna()) != {'stock_observation_asof'}:
        raise ValueError('re_c03 requires stock_observation_asof HO calendar')
    return crack, cache


def load_re_c03_features(root):
    crack, cache = load_inputs(root)
    calendar = pd.DatetimeIndex(cache.loc[cache.ticker.eq('DINO'),'date']).sort_values()
    if calendar.empty:
        raise ValueError('Missing DINO re_c03 calendar')
    source = crack.reindex(calendar)
    out = re_c03_signal(source).to_frame('re_c03_state')
    out['__feature_observed__re_c03_state'] = source[INPUTS].notna().all(axis=1)
    return out.loc[:crack.index.max()]


def validate_live_inputs(root, as_of, target_date):
    crack, cache = load_inputs(root)
    day, target = pd.Timestamp(as_of), pd.Timestamp(target_date)
    if day not in crack.index or not np.isfinite(crack.loc[day,INPUTS].astype(float)).all():
        raise ValueError('Missing/nonfinite current re_c03 quarterly inputs')
    if crack.at[day,INPUTS[2]] <= 0:
        raise ValueError('Nonpositive re_c03 volatility')
    opening = target.tz_localize('America/New_York') + pd.Timedelta(hours=9,minutes=30)
    known = pd.Timestamp(crack.at[day,'quarterly_arrival'])
    if pd.isna(known):
        raise ValueError('Missing re_c03 arrival')
    if known.tzinfo is None:
        known = known.tz_localize('Asia/Hong_Kong')
    if known > opening:
        raise ValueError('re_c03 quarterly inputs arrive after target open')
    rows = []
    for ticker in RE_C03_CONFIG.tickers:
        calendar = pd.DatetimeIndex(cache.loc[cache.ticker.eq(ticker) & cache.date.le(day),'date']).sort_values()
        if calendar.empty or calendar[-1] != day:
            raise ValueError(f'Stale re_c03 stock calendar: {ticker}')
        state = re_c03_signal(crack.reindex(calendar))
        rows.append(dict(instrument=ticker,as_of=day,target_date=target,
            signal=float(state.iloc[-1]),arrival=str(known),
            **crack.loc[day,INPUTS].to_dict()))
    if len({r['signal'] for r in rows}) != 1:
        raise ValueError('re_c03 native-calendar states disagree')
    return pd.DataFrame(rows)
