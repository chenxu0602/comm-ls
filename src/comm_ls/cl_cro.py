"""Pinned refiner-only live extension; original CL sleeves are not rescaled."""
import numpy as np
import pandas as pd

from comm_ls.cl_v32_strategy import SleeveConfig

CRO_EFFECTIVE_DATE = '2026-10-06'
CRO_CONFIG = SleeveConfig(
    weight=.10, tickers=('VLO','MPC','PSX'), feature_symbol='REFINERY_CRACK',
    feature='cro_state', threshold=1., side_mult=1, position_mode='sign',
    hold_days=None, rolling_days=None, sector_hedge=None,
    internal_weights={'VLO':.3,'MPC':.4,'PSX':.3}, signal_rule='cro_precomputed')


def cro_signal(crack, calendar):
    """Notebook CRO: sig_lb=30, vol_lb=30/min20, exits +/-0.5 vol, balance .5."""
    crack = pd.to_numeric(crack,errors='raise').sort_index()
    vol = crack.rolling(30,min_periods=20).std()
    level = crack.reindex(calendar).ffill()
    vol = vol.reindex(calendar).ffill()
    long = pd.Series(np.nan,index=calendar)
    short = long.copy()
    long.loc[level.diff(30) > vol] = 1.
    long.loc[level.diff(5) < vol*.5] = 0.
    short.loc[level.diff(30) < -vol] = -1.
    short.loc[level.diff(5) > -vol*.5] = 0.
    return .5*(long.ffill().fillna(0)+short.ffill().fillna(0))


def load_cro_features(root):
    frame = pd.read_parquet(root/'data/processed/refinery_crack_signals.parquet',
                            columns=['date','arrival','crack_03'])
    frame['date'] = pd.to_datetime(frame.date).dt.normalize()
    if frame.date.duplicated().any():
        raise ValueError('Duplicate CRO crack source dates')
    spy = pd.read_csv(root/'data/equity/yfinance/SPY.csv',usecols=['date','adj_close'])
    calendar = pd.DatetimeIndex(pd.to_datetime(spy.loc[spy.adj_close.notna(),'date'])).sort_values()
    # Do not allow a settlement observation to become a next-session target
    # before its recorded arrival. Dates/arrivals follow the repo HKT convention.
    source = frame.set_index('date').sort_index()
    opening = (source.index + pd.offsets.BDay(1)).tz_localize('America/New_York') + pd.Timedelta(hours=9,minutes=30)
    arrival = pd.to_datetime(source.arrival).dt.tz_localize('Asia/Hong_Kong')
    late = arrival.to_numpy() > opening.tz_convert('Asia/Hong_Kong').to_numpy()
    if late.any():
        raise ValueError('CRO crack arrival is after next-session open; review timestamp alignment')
    out = cro_signal(source.crack_03,calendar).to_frame('cro_state')
    # Fail closed on stale current source, rather than silently carrying a state.
    out = out.loc[out.index <= source.crack_03.last_valid_index()]
    out['__feature_observed__cro_state'] = True
    return out


def cap_component_legs(legs, cap, aum):
    out = legs.copy()
    total = out.groupby('instrument').target_weight.sum()
    scales = (cap/total.abs().replace(0,np.nan)).clip(upper=1).fillna(1)
    scale = out.instrument.map(scales)
    out['target_weight'] *= scale
    out['target_notional'] = out.target_weight*aum
    out['target_shares'] = out.target_notional/out.previous_close
    out['target_weight_adjustment'] = out.target_weight-out.research_target_weight
    return out


def executable_component_hedges(targets, betas, aum, market):
    """Preserve component hedge methods after account stock netting/child caps.

    Allocate executed net stock weight proportionally to desired component
    weights. A net-zero virtual stock keeps its distinct component hedges.
    Ambiguous nonzero inventory against a zero target fails for manual review.
    """
    hedges = {market:0.}
    stocks = targets.loc[targets.instrument_type.eq('stock')].set_index('instrument')
    for ticker, group in betas.groupby('instrument'):
        desired = group.target_weight.astype(float)
        total = desired.sum()
        actual = float(stocks.loc[ticker,'post_child_shares'])*float(stocks.loc[ticker,'previous_close'])/aum
        if abs(total) < 1e-12:
            if abs(actual) > 1e-12:
                raise ValueError(f'Net-zero mixed hedge with remaining {ticker} inventory; review fills')
            allocated = desired
        else:
            allocated = desired*actual/total
        for i, row in group.iterrows():
            weight = allocated.loc[i]
            if weight == 0:
                continue
            if not np.isfinite(row.market_beta):
                raise ValueError(f'Missing component market beta: {ticker}:{row.component}')
            hedges[market] -= weight*row.market_beta
            if row.sector_hedge:
                if not np.isfinite(row.sector_beta):
                    raise ValueError(f'Missing component sector beta: {ticker}:{row.component}')
                hedges[row.sector_hedge] = hedges.get(row.sector_hedge,0)-weight*row.sector_beta
    return hedges
