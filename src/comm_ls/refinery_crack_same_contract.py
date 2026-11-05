"""Isolated June-crack research: fixed-contract lags, never stitched differences."""
from pathlib import Path

import numpy as np
import pandas as pd

from comm_ls.commodity import _load_contract_market_data


def contract_features(curves, selected, sessions, lags=(5, 20, 30), windows=(30,)):
    """Curves indexed by session, columns by contract; selection is already PIT.

    Lag = XNYS sessions, not non-null observations. Std uses ddof=1 and the
    notebook's min_periods=floor(window/3)*2; no quote forward filling.
    """
    if selected.index.has_duplicates or sessions.has_duplicates:
        raise ValueError('Duplicate dates')
    out = pd.DataFrame(index=sessions)
    out['june_contract'] = selected.reindex(sessions)
    for field, curve in curves.items():
        curve = curve.reindex(sessions)
        def select(frame):
            result = pd.Series(np.nan, index=sessions)
            for contract in frame.columns:
                mask = out.june_contract.eq(contract)
                result.loc[mask] = frame.loc[mask, contract]
            return result
        out[field] = select(curve)
        for lag in lags:
            out[f'{field}_same_contract_lag_{lag}'] = select(curve.shift(lag))
        for window in windows:
            out[f'{field}_same_contract_std_{window}'] = select(
                curve.rolling(window, min_periods=window//3*2).std())
    return out


def build_same_contract(canonical, commodity_dir, sessions, lags, windows):
    if canonical.date.duplicated().any() or not canonical.roll_mode.eq('point_in_time').all():
        raise ValueError('Requires unique PIT canonical crack data')
    source = canonical.set_index('date').sort_index()
    legs = {}
    for symbol in ['CL','HO','XB']:
        data = _load_contract_market_data(Path(commodity_dir)/symbol)
        data = data.loc[data.contract.isin(source.june_contract.unique())]
        if data.duplicated(['date','contract']).any():
            raise ValueError(f'Duplicate {symbol} quotes')
        legs[symbol] = data.pivot(index='date',columns='contract',values='settle').reindex(sessions)
    cl, ho, xb = legs['CL'], legs['HO']*.42, legs['XB']*.42
    curves = {'crack_01':ho-cl,'crack_02':2*xb+ho-3*cl,'crack_03':3*xb+2*ho-5*cl}
    # Drop absent canonical dates rather than carrying a contract selection over a gap.
    out = contract_features(curves, source.june_contract, sessions, lags, windows)
    for field in curves:
        expected = source[field].reindex(sessions)
        comparable = expected.notna() & out[field].notna()
        if not np.allclose(expected[comparable],out.loc[comparable,field],atol=1e-8):
            raise ValueError('Source snapshot differs from canonical; rebuild canonical first')
        if (expected.notna() & out[field].isna()).any():
            raise ValueError('Canonical price cannot be reproduced from source snapshot')
    # Preserve conservative source arrivals, including historical late arrivals in
    # any feature window. Never publish a derived feature before its inputs.
    arrival = pd.to_datetime(source.arrival.reindex(sessions))
    terms = [arrival]
    terms.extend(arrival.shift(lag) for lag in lags)
    for window in windows:
        terms.extend(arrival.shift(k) for k in range(window))
    out['arrival'] = pd.concat(terms,axis=1).max(axis=1)
    out['source_arrival'] = arrival
    out = out.loc[out.june_contract.notna()].copy()
    out['roll_mode'] = 'point_in_time'
    return out.rename_axis('date').reset_index()


def align_at_stock_open(crack_data, stock_dates):
    """Align whole feature rows, without independent-column forward filling."""
    right = crack_data.reset_index().copy()
    right['known_at'] = pd.to_datetime(right.arrival)
    if right.known_at.dt.tz is None:
        right['known_at'] = right.known_at.dt.tz_localize('Asia/Hong_Kong')
    right['known_at'] = right.known_at.dt.tz_convert('UTC')
    right = right.sort_values(['known_at','date']).drop_duplicates('known_at',keep='last')
    left = pd.DataFrame({'stock_date':pd.DatetimeIndex(stock_dates).sort_values()})
    left['known_at'] = (left.stock_date.dt.tz_localize('America/New_York')
                        + pd.Timedelta(hours=9,minutes=30)).dt.tz_convert('UTC')
    out = pd.merge_asof(left,right,on='known_at',direction='backward')
    # Do not keep an old signal alive indefinitely when data updates cease.
    stale = (out.stock_date-out.date).dt.days.gt(7)
    features = [c for c in out if c.startswith('crack_')]
    out.loc[stale,features] = np.nan
    return out.set_index('stock_date').reindex(stock_dates)


def calc_crack_ls_same_contract(*, load_stock_data, rolling_betas, crack_data,
        start='2010-01-01', field='crack_03', sig_lb=20, vol_lb=30,
        ret_col='residual_return_mkt_w12m', long_weights, short_weights,
        long_balance=.5, short_balance=-.5, beta_adjusted=False, signal_smoothing=0,
        alignment='source_date'):
    """Notebook research defaults to exact same-date stock/futures alignment.

    This convention is not an execution-time availability assertion. Existing
    downstream position/PnL lags are left unchanged; production is independent.
    """
    if alignment not in {'source_date', 'arrival_open'}:
        raise ValueError('Unknown alignment')
    if set(long_weights) & set(short_weights):
        raise ValueError('Long/short ticker overlap')
    required = [field, f'{field}_same_contract_lag_{sig_lb}',
                f'{field}_same_contract_lag_5', f'{field}_same_contract_std_{vol_lb}']
    missing = set(required)-set(crack_data)
    if missing:
        raise ValueError(f'Rebuild same-contract research data for requested horizons: {missing}')
    signals, returns, weighted = {}, {}, {}
    for ticker in sorted(set(long_weights)|set(short_weights)):
        df = load_stock_data(ticker).set_index('date').sort_index()
        f = (crack_data.reindex(df.index) if alignment == 'source_date'
             else align_at_stock_open(crack_data, df.index))
        change = f[field]-f[required[1]]
        change5 = f[field]-f[required[2]]
        vol = f[required[3]]
        long = pd.Series(np.nan,index=df.index)
        short = long.copy()
        long.loc[change>vol] = 1.
        long.loc[change5<vol*.5] = 0.
        short.loc[change< -vol] = -1.
        short.loc[change5> -vol*.5] = 0.
        invalid = f[required].isna().any(axis=1) | vol.le(0)
        long.loc[invalid] = short.loc[invalid] = 0.
        signal = long.ffill().fillna(0)+short.ffill().fillna(0)
        weight = long_weights[ticker] if ticker in long_weights else short_weights[ticker]
        balance = long_balance if ticker in long_weights else short_balance
        signals[ticker] = signal*weight*balance
        returns[ticker] = df[ret_col]
        weighted[ticker] = df[ret_col]*weight*abs(balance)
    ret, sig, wret = pd.DataFrame(returns),pd.DataFrame(signals),pd.DataFrame(weighted)
    if beta_adjusted:
        if not long_weights or not short_weights:
            raise ValueError('Beta adjustment requires both baskets')
        beta = rolling_betas(wret[list(long_weights)].fillna(0).sum(axis=1),
            wret[list(short_weights)].fillna(0).sum(axis=1).to_frame('short'),
            window=252,min_obs=126,lag=1)['beta_short']
        sig[list(short_weights)] = sig[list(short_weights)].mul(beta,axis=0)
    if signal_smoothing>1:
        sig = sig.rolling(signal_smoothing).mean()
    return sig.sort_index().loc[start:],ret.sort_index().loc[start:]
