"""2026-11-04 operator-approved L/PP chemical exit, source-date calendar."""
from pathlib import Path
import numpy as np
import pandas as pd

TICKERS = ('DOW', 'LYB', 'WLK', 'CE')
FEATURE = 'chemical_lp_state'


def chemical_lp_signal(frame):
    carry, l, p = (frame[c] for c in ('carry', 'l_ret', 'p_ret'))
    th = carry.diff().rolling(252, min_periods=100).std()
    lc = l.rolling(35, min_periods=10).sum()
    pc = p.rolling(35, min_periods=10).sum()
    ls = l.rolling(30, min_periods=10).std() * 7
    ps = p.rolling(30, min_periods=10).std() * 7
    long = pd.Series(np.nan, index=frame.index)
    short = long.copy()
    long.loc[(carry.diff(30) < -th) & (carry > th)] = 1.
    long.loc[(carry < 0) | (lc < -ls) | (pc < -ps)] = 0.
    short.loc[(carry.diff(30) > th) & (carry < -th)] = -1.
    short.loc[(carry > 0) | (lc > ls) | (pc > ps)] = 0.
    long.loc[carry.isna()] = short.loc[carry.isna()] = 0.
    return long.ffill().fillna(0) + short.ffill().fillna(0)


def load_frames(root):
    root = Path(root)
    cache = pd.read_parquet(root/'data/cache/feature_return_observation_v1/CL-multi_return_2.parquet',
                           columns=['date', 'ticker', 'feature_value__carry'])
    futures = {}
    for name, symbol in [('l_ret', 'POL'), ('p_ret', 'PYL')]:
        f = pd.read_csv(root/f'data/comm/carry_data_2/{symbol}.csv',
                        parse_dates=['date'], low_memory=False).set_index('date').sort_index()
        if f.index.has_duplicates:
            raise ValueError(f'Duplicate {symbol} dates')
        futures[name] = pd.to_numeric(f.m0_ret, errors='raise')
    frames = {}
    for ticker in TICKERS:
        f = cache.loc[cache.ticker.eq(ticker)].copy()
        f['date'] = pd.to_datetime(f.date)
        f = f.set_index('date').sort_index().rename(columns={'feature_value__carry': 'carry'})
        if f.empty or f.index.has_duplicates:
            raise ValueError(f'Invalid chemical calendar: {ticker}')
        for name, series in futures.items():
            f[name] = series.reindex(f.index)
        frames[ticker] = f
    return frames


def load_chemical_lp_features(root):
    frames = load_frames(root)
    reference = frames['DOW']
    state = chemical_lp_signal(reference)
    # The shared production feature must reproduce every native stock calendar.
    for ticker, frame in frames.items():
        other = chemical_lp_signal(frame)
        # DOW's listing warmup differs in 2019. This dated live feature is
        # not a replacement for native-calendar historical research returns.
        common = state.index.intersection(other.index)
        common = common[common >= pd.Timestamp('2020-01-01')]
        if len(common) == 0 or not state.loc[common].equals(other.loc[common]):
            raise ValueError(f'Chemical native-calendar state mismatch: {ticker}')
    out = state.to_frame(FEATURE)
    out[f'__feature_observed__{FEATURE}'] = reference[['carry','l_ret','p_ret']].notna().all(axis=1)
    return out


def validate_live_inputs(root, as_of):
    rows = []
    for ticker, frame in load_frames(root).items():
        frame = frame.loc[:pd.Timestamp(as_of)]
        if frame.empty or frame.index[-1] != pd.Timestamp(as_of):
            raise ValueError(f'Stale chemical calendar: {ticker}')
        if not np.isfinite(frame.iloc[-1][['carry','l_ret','p_ret']].astype(float)).all():
            raise ValueError(f'Missing current chemical inputs: {ticker}')
        if frame[['l_ret','p_ret']].tail(30).count().min() < 10:
            raise ValueError(f'Insufficient chemical exit history: {ticker}')
        rows.append(dict(instrument=ticker, as_of=as_of,
                         signal=chemical_lp_signal(frame).iloc[-1],
                         **frame.iloc[-1][['carry','l_ret','p_ret']].to_dict()))
    return pd.DataFrame(rows)
