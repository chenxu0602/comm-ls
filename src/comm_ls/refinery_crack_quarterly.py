"""Isolated same-delivery-quarter crack research, without stitched differences."""
from pathlib import Path

import numpy as np
import pandas as pd

from comm_ls.commodity import FUTURES_MONTH_NUMBERS, _load_contract_market_data
from comm_ls.refinery_crack import _arrival_by_date


def quarterly_contracts(dates, min_days=45):
    """Pure calendar selection, independent of quote presence or future liquidity.

    At exactly 45 calendar days to delivery-month FIRST day the quarter remains
    eligible; switch on the first observation with fewer than 45 days remaining.
    """
    if min_days < 1:
        raise ValueError('min_days must be positive')
    rows=[]
    for date in pd.DatetimeIndex(dates):
        quarters=[pd.Timestamp(year=year,month=month,day=1)
                  for year in range(date.year,date.year+3) for month in (3,6,9,12)]
        near=next(q for q in quarters if (q-date).days>=min_days)
        far=quarters[quarters.index(near)+1]
        rows.append(dict(date=date,
            quarterly_near_contract=f'{near.year}{FUTURES_MONTH_NUMBERS[near.month]}',
            quarterly_far_contract=f'{far.year}{FUTURES_MONTH_NUMBERS[far.month]}',
            quarterly_near_delivery_month=near,quarterly_far_delivery_month=far,
            quarterly_near_days_to_delivery=(near-date).days,
            quarterly_far_days_to_delivery=(far-date).days))
    return pd.DataFrame(rows).set_index('date')


def pick_contract(panel, selected):
    out=pd.Series(np.nan,index=selected.index,dtype=float)
    for contract in selected.dropna().unique():
        if contract in panel:
            mask=selected.eq(contract)
            out.loc[mask]=panel[contract].reindex(out.index).loc[mask]
    return out


def build_quarterly_crack(markets, sessions, *, lags=(5,20,30), windows=(30,),
                          ma_windows=(1,2,3,5,30,50), min_days=45, commodity_signals=None,
                          contract_schedule=None):
    sessions=pd.DatetimeIndex(sessions)
    if sessions.has_duplicates or not sessions.is_monotonic_increasing:
        raise ValueError('Sessions must be unique and increasing')
    if not len(sessions) or min([*lags,*windows,*ma_windows])<1:
        raise ValueError('Nonempty sessions and positive windows required')
    schedule=quarterly_contracts(sessions,min_days) if contract_schedule is None else contract_schedule.copy()
    if not schedule.index.equals(sessions):
        raise ValueError('Contract schedule must match sessions exactly')
    legs={}
    for symbol in ('CL','HO','XB'):
        data=markets[symbol]
        if data.duplicated(['date','contract']).any():
            raise ValueError(f'Duplicate date/contract: {symbol}')
        for column in ('settle','volume','open_interest'):
            legs[symbol,column]=data.pivot(index='date',columns='contract',values=column).reindex(sessions)
    cl=legs['CL','settle'];ho=legs['HO','settle']*.42;xb=legs['XB','settle']*.42
    # All arithmetic aligns EXACT delivery-contract columns and source dates.
    curves={'crack_01':ho-cl,'crack_02':2*xb+ho-3*cl,'crack_03':3*xb+2*ho-5*cl}
    out=schedule.copy()
    for side in ('near','far'):
        selected=schedule[f'quarterly_{side}_contract']
        for (symbol,column),panel in legs.items():
            out[f'quarterly_{side}_{symbol.lower()}_{column}']=pick_contract(panel,selected)
        out[f'quarterly_{side}_complete_quotes']=out[
            [f'quarterly_{side}_{s}_settle' for s in ('cl','ho','xb')]].notna().all(axis=1)
        for field,curve in curves.items():
            name=f'{field}_quarterly_{side}'
            out[name]=pick_contract(curve,selected)
            for lag in lags:
                out[f'{name}_same_contract_lag_{lag}']=pick_contract(curve.shift(lag),selected)
                out[f'{name}_change_{lag}d']=out[name]-out[f'{name}_same_contract_lag_{lag}']
            for window in windows:
                out[f'{name}_same_contract_std_{window}']=pick_contract(
                    curve.rolling(window,min_periods=max(2,window//3*2)).std(),selected)
            for window in ma_windows:
                # Keep legacy MA3 unchanged; new MA1/2/5 require full windows.
                minimum=window if window in (1,2,5) else (1 if window==3 else max(1,window//2))
                out[f'{name}_ma_{window}']=pick_contract(
                    curve.rolling(window,min_periods=minimum).mean(),selected)
            for fast,slow in ((1,30),(2,30),(3,30),(5,30),(3,50)):
                if fast in ma_windows and slow in ma_windows:
                    out[f'{name}_ma_gap_{fast}d_{slow}d']=out[f'{name}_ma_{fast}']-out[f'{name}_ma_{slow}']
    for field in curves:
        near=f'{field}_quarterly_near';far=f'{field}_quarterly_far'
        slope=f'{field}_quarterly_slope'
        out[slope]=out[near]-out[far]
        for lag in lags:
            out[f'{slope}_same_contract_lag_{lag}']=(out[f'{near}_same_contract_lag_{lag}']
                                                   -out[f'{far}_same_contract_lag_{lag}'])
            out[f'{slope}_change_{lag}d']=out[slope]-out[f'{slope}_same_contract_lag_{lag}']
    source_arrival=_arrival_by_date(pd.Series(sessions,index=sessions),commodity_signals)
    terms=[source_arrival]
    terms.extend(source_arrival.shift(lag) for lag in lags)
    terms.extend(source_arrival.shift(k) for k in range(max([*windows,*ma_windows])))
    out['quarterly_source_arrival']=source_arrival
    out['quarterly_arrival']=pd.concat(terms,axis=1).max(axis=1)
    out['quarterly_calendar']='XNYS'
    out['quarterly_selection_rule']=f'delivery_month_start_at_least_{min_days}_calendar_days'
    return out.rename_axis('date').reset_index()


def read_quarterly_markets(commodity_dir, as_of):
    return {s:_load_contract_market_data(Path(commodity_dir)/s).loc[
        lambda d:d.date.le(pd.Timestamp(as_of)) & d.contract.str[-1].isin(['H','M','U','Z'])]
        for s in ('CL','HO','XB')}
