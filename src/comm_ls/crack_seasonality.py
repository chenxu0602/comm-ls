"""Past-year-only seasonal centering of same-contract crack features."""
import pandas as pd


def center_xb_contribution(original, xb_component, fields):
    """Subtract only XB's seasonal feature contribution; preserve raw volatility.

    xb_component contains crack-unit contributions (e.g. 1.26 * XB cents/gal
    for crack_03), computed within each fixed delivery contract.
    """
    if not original.date.equals(xb_component.date):
        raise ValueError('Original and XB component dates must match exactly')
    centered = seasonal_center(xb_component, fields)
    out = original.copy()
    for field in fields:
        baseline = centered[field + '_seasonal_mean']
        out[field + '_xb_component'] = xb_component[field]
        out[field + '_xb_seasonal_mean'] = baseline
        out[field + '_xb_seasonal_years'] = centered[field + '_seasonal_years']
        out[field + '_xb_sa'] = (original[field] - baseline).where(
            xb_component[field].notna())
    return out


def seasonal_center(frame, fields, years=5, min_years=3, min_days=5):
    """Equal-weight annual means within observation-month/delivery-month cells.

    Excludes the entire current year. Missing features remain missing. This is
    feature centering, not a reconstructed seasonally adjusted contract curve.
    """
    if not 1 <= min_years <= years or min_days < 1:
        raise ValueError('Require 1 <= min_years <= years and positive min_days')
    out = frame.copy()
    dates = pd.to_datetime(out['date'])
    if dates.duplicated().any() or not dates.is_monotonic_increasing:
        raise ValueError('Dates must be unique and sorted')
    for field in fields:
        side = 'near' if '_near_' in field else 'far' if '_far_' in field else None
        if side is None:
            raise ValueError(f'Expected near/far field: {field}')
        delivery = pd.to_datetime(out[f'quarterly_{side}_delivery_month'])
        x = pd.DataFrame({'year': dates.dt.year, 'month': dates.dt.month,
                          'delivery': delivery.dt.month,
                          'value': pd.to_numeric(out[field], errors='raise')})
        annual = x.groupby(['year', 'month', 'delivery']).value.agg(['mean', 'count'])
        annual = annual.loc[annual['count'].ge(min_days)].reset_index()
        baseline = pd.Series(float('nan'), index=out.index)
        count = pd.Series(0, index=out.index, dtype=int)
        for (year, month, contract_month), idx in x.groupby(['year', 'month', 'delivery']).groups.items():
            past = annual.loc[annual.year.between(year-years, year-1)
                              & annual.month.eq(month) & annual.delivery.eq(contract_month), 'mean']
            count.loc[idx] = len(past)
            if len(past) >= min_years:
                baseline.loc[idx] = past.mean()
        out[field + '_seasonal_mean'] = baseline
        out[field + '_seasonal_years'] = count
        out[field + '_sa'] = x.value - baseline
    return out
