"""Operator-approved research chains; cutoff is delivery-month start minus 45 days.

This is NOT an exchange expiry calendar. Prices retain native CNY units.
"""
import numpy as np
import pandas as pd

CHINA_ACTIVE_MONTHS = {
    'RBT': (1,5,10),
    **{s:(1,5,9) for s in ('IOE','KEE','CKC','POL','PYL','PVC','SYR','LGE')},
    **{s:tuple(range(1,13)) for s in ('PXL','ZSY','ZME','PT')},
}


def select_china_front(panel, *, symbol, confirmation_observations=2,
                       allowed_months=None, max_maturity_years=.75):
    """Monotone OI leader, volume fallback; force next usable leader at cutoff.

    Missing settlement before cutoff retains the selected contract (exposes NaN).
    Missing settlement/leadership after cutoff emits NA, never an expired leg.
    Carried activity timestamps cannot count twice as confirmation evidence.
    """
    from comm_ls.carry_builder import contract_sort_key
    allowed = set(allowed_months or CHINA_ACTIVE_MONTHS[symbol])
    dates = pd.Index(sorted(panel.date.unique()),name='date')
    selected = pd.Series(pd.NA,index=dates,dtype='string')
    diag = pd.DataFrame(index=dates)
    diag['M0_roll_reason'] = 'hold'
    diag['M0_roll_candidate'] = pd.Series(pd.NA,index=dates,dtype='string')
    diag['M0_roll_signal_count'] = 0
    diag['M0_roll_activity_field'] = pd.Series(pd.NA,index=dates,dtype='string')
    diag['M0_roll_pending_review'] = False
    diag['M0_roll_cutoff'] = pd.NaT
    diag['M0_roll_days_to_cutoff'] = np.nan
    current = candidate = None
    count = 0
    evidence = None
    for date in dates:
        date = pd.Timestamp(date)
        day = panel.loc[panel.date.eq(date)].copy()
        cutoff = day.contract_month-pd.Timedelta(days=45)
        eligible = day.loc[day.contract_month.dt.month.isin(allowed)
            & cutoff.gt(date) & day.tm.lt(max_maturity_years)
            & day.settle.gt(0)].copy()
        forced = current is not None and date >= (
            pd.Timestamp(year=contract_sort_key(current)[0],month=contract_sort_key(current)[1],day=1)
            -pd.Timedelta(days=45))
        if current is not None:
            eligible = eligible.loc[eligible.contract.map(
                lambda value: contract_sort_key(value) >= contract_sort_key(current)).astype(bool)]
        if current is not None and not forced and current not in set(eligible.contract):
            selected.loc[date] = current
            diag.loc[date,'M0_roll_reason'] = 'missing_unexpired_front'
            candidate, count, evidence = None,0,None
        else:
            if forced:
                eligible = eligible.loc[eligible.contract.ne(current)]
            # Prefer genuinely positive OI; zero OI is not liquidity evidence.
            field = 'open_interest' if eligible.open_interest.gt(0).any() else 'volume'
            ranked = eligible.loc[eligible[field].gt(0)].copy()
            if not ranked.empty:
                ranked['_key'] = ranked.contract.map(contract_sort_key)
                ranked = ranked.sort_values([field,'_key'],ascending=[False,True])
            if ranked.empty:
                if forced or current is None:
                    diag.loc[date,'M0_roll_reason'] = 'blocked_no_liquid_forward_contract'
                else:
                    selected.loc[date] = current
                    diag.loc[date,'M0_roll_reason'] = 'hold_no_activity'
                candidate,count,evidence = None,0,None
            else:
                row = ranked.iloc[0]
                leader = str(row.contract)
                diag.loc[date,'M0_roll_activity_field'] = field
                if current is None or forced:
                    current = leader
                    selected.loc[date] = current
                    diag.loc[date,'M0_roll_reason'] = 'forced_45d_before_delivery' if forced else 'initialize_activity_leader'
                    candidate,count,evidence = None,0,None
                elif leader == current:
                    selected.loc[date] = current
                    candidate,count,evidence = None,0,None
                else:
                    current_row = eligible.loc[eligible.contract.eq(current)].iloc[0]
                    new_evidence = (field,row.get(f'{field}_asof_date',date),
                                    current_row.get(f'{field}_asof_date',date))
                    if candidate != leader:
                        candidate,count,evidence = leader,1,new_evidence
                    elif new_evidence != evidence:
                        count += 1
                        evidence = new_evidence
                    diag.loc[date,'M0_roll_candidate'] = candidate
                    diag.loc[date,'M0_roll_signal_count'] = count
                    if count >= confirmation_observations:
                        current = leader
                        candidate,count,evidence = None,0,None
                        diag.loc[date,'M0_roll_reason'] = 'confirmed_activity_roll'
                    else:
                        diag.loc[date,'M0_roll_reason'] = 'pending_confirmation'
                        diag.loc[date,'M0_roll_pending_review'] = True
                    selected.loc[date] = current
        if current is not None:
            year,month = contract_sort_key(current)
            deadline = pd.Timestamp(year=year,month=month,day=1)-pd.Timedelta(days=45)
            diag.loc[date,'M0_roll_cutoff'] = deadline
            diag.loc[date,'M0_roll_days_to_cutoff'] = (deadline-date).days
    return selected,diag


def load_china_feature_data(feature_name, symbol, *, root=None, start=None, end=None):
    """Notebook helper using _2 signals only, preserving source dates/arrival."""
    from pathlib import Path
    symbol = symbol.upper()
    if symbol not in CHINA_ACTIVE_MONTHS:
        raise ValueError(f'Not a configured China research symbol: {symbol}')
    root = Path(root) if root is not None else Path(__file__).resolve().parents[2]
    d = pd.read_parquet(root/'data/processed/commodity_signals_2.parquet')
    if feature_name not in d:
        raise KeyError(f'Unknown feature {feature_name}')
    d = d.loc[d.symbol.eq(symbol)].copy()
    if d.empty:
        raise ValueError('No China feature rows; run the China carry/signals refresh first')
    if d.date.duplicated().any():
        raise ValueError('Duplicate feature dates')
    d['date'] = pd.to_datetime(d.date)
    if start is not None:
        d = d.loc[d.date.ge(pd.Timestamp(start))]
    if end is not None:
        d = d.loc[d.date.le(pd.Timestamp(end))]
    columns = ['date','symbol']+(['arrival'] if 'arrival' in d else [])+[feature_name]
    out = d[columns].rename(columns={feature_name:'feature_value'}).sort_values('date')
    out['feature_name'] = feature_name
    out['feature_source_valid'] = out.feature_value.notna()
    return out.reset_index(drop=True)
