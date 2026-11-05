"""Hindsight monthly crack research using observed terminal dates, NOT PIT expiry."""
import pandas as pd
from comm_ls.commodity import FUTURES_MONTH_NUMBERS


def code(month):
    return f'{month.year}{FUTURES_MONTH_NUMBERS[month.month]}'


def observed_expiries(markets, snapshot_date):
    """Future delivery months are censored, not expired at their last quote.

    Even uncensored terminal dates are only proxies: incomplete archives can
    end early. Users must inspect the emitted audit before using the results.
    """
    numbers = {v: k for k, v in FUTURES_MONTH_NUMBERS.items()}
    rows = []
    for symbol, data in markets.items():
        for contract, group in data.groupby('contract'):
            delivery = pd.Timestamp(int(contract[:4]), numbers[contract[-1]], 1)
            last = group.date.max()
            completed = delivery <= pd.Timestamp(snapshot_date)
            rows.append(dict(symbol=symbol, contract=contract, delivery=delivery,
                last_record_date=last, expiry=last if completed else pd.NaT,
                censored=not completed))
    return pd.DataFrame(rows)


def monthly_schedule(sessions, expiries, roll_days=15):
    if roll_days < 0:
        raise ValueError('roll_days must be nonnegative')
    expiry = expiries.pivot(index='contract', columns='symbol', values='expiry').reindex(columns=['CL','HO','XB'])
    common = expiry.min(axis=1).where(expiry.notna().all(axis=1))
    rows = []
    for date in pd.DatetimeIndex(sessions):
        # Same-month delivery is already past CL expiry; start next month.
        near = date.to_period('M').to_timestamp() + pd.DateOffset(months=1)
        status = 'ok'
        while True:
            exp = common.get(code(near), pd.NaT)
            if pd.isna(exp):
                status = 'unknown_near_expiry'
                break
            if date < exp - pd.Timedelta(days=roll_days):
                break
            near += pd.DateOffset(months=1)
        target = near + pd.DateOffset(months=6)
        far = target
        # Fixed coverage policy, never choose a month based on today's quotes.
        while far.year > date.year and far.month not in (1,2,3,6,9,12):
            far += pd.DateOffset(months=1)
        valid = status == 'ok'
        rows.append(dict(date=date,
            quarterly_near_contract=code(near) if valid else None,
            quarterly_far_contract=code(far) if valid else None,
            quarterly_near_delivery_month=near if valid else pd.NaT,
            quarterly_far_delivery_month=far if valid else pd.NaT,
            quarterly_near_days_to_delivery=(near-date).days if valid else float('nan'),
            quarterly_far_days_to_delivery=(far-date).days if valid else float('nan'),
            monthly_candidate_near=code(near), monthly_status=status,
            monthly_near_expiry=exp, monthly_roll_date=exp-pd.Timedelta(days=roll_days),
            monthly_far_target_month=target,
            monthly_actual_span_months=(far.year-near.year)*12+far.month-near.month if valid else float('nan')))
    return pd.DataFrame(rows).set_index('date')
