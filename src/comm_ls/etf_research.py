"""Isolated ETF research helpers; no production configuration mutations."""
from pathlib import Path
import re
import numpy as np
import pandas as pd

DEFAULT_ETFS = ('CRAK','XLB','XLE','XME','XES','OIH','IEZ','BOAT','COPX','PICK',
                'WGMI','DAPP','SPY','QQQ','XOP','IEO','XEG.TO','IYM','XRT','ITA',
                'XAR','BITQ','BLOK')

STOCK_BASKET_GROUPS = {
    'refiner1': ('VLO','MPC','PSX'),
    'refiner2': ('DINO','DK','PBF'),
    'refiner3': ('CVI','PARR'),
    'chemical1': ('LYB','WLK'),
    'chemical2': ('DOW',),
    'chemical3': ('EMN',),
    'producer1': ('COP','EOG','FANG'),
    'producer2': ('EOG','FANG'),
    'producer3': ('CNQ','SU','CVE'),
    'milling1': ('ADM',),
    'milling2': ('BG',),
    'protein1': ('PPC',),
    'protein2': ('CALM',),
    'protein3': ('SFD',),
    'protein_diversified': ('TSN',),
    # Backward-compatible notebook name.  TSN is a diversified protein
    # control, not the preferred direct feed-cost downstream leg.
    'farm': ('TSN',),
}


# Candidate lists are alternatives, not portfolio weights.  The first ETF is
# the default used by load_pair_research; callers can select another explicitly.
PAIR_RESEARCH_CONFIG = {
    'milling1_vs_farm': {
        'label': 'ADM milling vs TSN farm/protein',
        'basket_a': STOCK_BASKET_GROUPS['milling1'],
        'basket_b': STOCK_BASKET_GROUPS['farm'],
        'stock_a_group': 'milling1',
        'stock_b_group': 'farm',
        'etf_a': (),
        'etf_b': (),
        'futures': ('ZS','ZM','ZL'),
        'signals': 'soybean board crush; meal/oil/soybean calendar variants',
        'etf_quality': 'stock_baskets_only',
    },
    'milling2_vs_farm': {
        'label': 'BG milling vs TSN farm/protein',
        'basket_a': STOCK_BASKET_GROUPS['milling2'],
        'basket_b': STOCK_BASKET_GROUPS['farm'],
        'stock_a_group': 'milling2',
        'stock_b_group': 'farm',
        'etf_a': (),
        'etf_b': (),
        'futures': ('ZS','ZM','ZL'),
        'signals': 'soybean board crush; meal/oil/soybean calendar variants',
        'etf_quality': 'stock_baskets_only',
    },
    'milling1_vs_milling_2': {
        'label': 'ADM milling vs BG milling',
        'basket_a': STOCK_BASKET_GROUPS['milling1'],
        'basket_b': STOCK_BASKET_GROUPS['milling2'],
        'stock_a_group': 'milling1',
        'stock_b_group': 'milling2',
        'etf_a': (),
        'etf_b': (),
        'futures': ('ZS','ZM','ZL'),
        'signals': 'soybean board crush; meal/oil/soybean calendar variants',
        'etf_quality': 'stock_baskets_only',
    },
    'refiner_vs_refiner': {
        'label': 'Refiner group vs refiner group',
        'basket_a': STOCK_BASKET_GROUPS['refiner1'],
        'basket_b': STOCK_BASKET_GROUPS['refiner2'],
        'stock_a_group': 'refiner1',
        'stock_b_group': 'refiner2',
        'etf_a': (),
        'etf_b': (),
        'futures': ('CL','XB','HO'),
        'signals': 'refinery crack; CL curve; Brent-WTI companion features',
        'etf_quality': 'stock_baskets_only',
    },
    'refiner_vs_producer': {
        'label': 'Refiner vs producer',
        'basket_a': STOCK_BASKET_GROUPS['refiner1'],
        'basket_b': STOCK_BASKET_GROUPS['producer1'],
        'stock_a_group': 'refiner1',
        'stock_b_group': 'producer1',
        'stock_a_groups': ('refiner1','refiner2','refiner3'),
        'etf_a': ('CRAK',),
        'etf_b': ('IEO','XOP'),
        'futures': ('CL','XB','HO'),
        'signals': 'refinery crack; CL curve; Brent-WTI companion features',
        'etf_quality': 'good_with_business_overlap',
    },
    'refiner_vs_vlcc': {
        'label': 'Refiner vs VLCC',
        'basket_a': STOCK_BASKET_GROUPS['refiner1'],
        'basket_b': ('DHT','FRO'),
        'stock_a_group': 'refiner1',
        'stock_a_groups': ('refiner1','refiner2','refiner3'),
        'etf_a': ('CRAK',),
        'etf_b': ('BOAT',),
        'futures': ('CL','XB','HO'),
        'signals': 'refinery crack plus separately sourced VLCC freight/TCE',
        'etf_quality': 'poor_BOAT_is_broad_shipping',
    },
    'product_tanker_vs_vlcc': {
        'label': 'Product tanker vs crude tanker',
        'basket_a': ('STNG','TRMD'),
        'basket_b': ('DHT','FRO'),
        'etf_a': (),
        'etf_b': (),
        'futures': ('CL','XB','HO'),
        'signals': 'TC routes vs TD routes; product cracks as control',
        'etf_quality': 'no_clean_etf_pair',
    },
    'heavy_refiner_vs_canadian_heavy': {
        'label': 'Heavy-oil refiner vs Canadian heavy producer',
        'basket_a': STOCK_BASKET_GROUPS['refiner1'],
        'basket_b': STOCK_BASKET_GROUPS['producer3'],
        'stock_a_group': 'refiner1',
        'stock_b_group': 'producer3',
        'stock_a_groups': ('refiner1','refiner2','refiner3'),
        'etf_a': ('CRAK',),
        'etf_b': ('XEG.TO',),
        'futures': ('CL','XB','HO'),
        'signals': 'WTI-WCS required externally; CL curve and crack controls',
        'etf_quality': 'mixed_business_and_CAD_exposure',
    },
    'services_vs_producer': {
        'label': 'Oil services vs producer',
        'basket_a': ('SLB','HAL','FTI'),
        'basket_b': ('COP','EOG','FANG'),
        'etf_a': ('OIH','XES','IEZ'),
        'etf_b': ('IEO','XOP'),
        'futures': ('CL',),
        'signals': 'CL/Brent deferred prices; CAPEX, rigs and orders required externally',
        'etf_quality': 'good_but_futures_signal_is_incomplete',
    },
    'refiner_vs_chemical': {
        'label': 'Refiner vs chemical',
        'basket_a': STOCK_BASKET_GROUPS['refiner1'],
        'basket_b': STOCK_BASKET_GROUPS['chemical1'],
        'stock_a_group': 'refiner1',
        'stock_b_group': 'chemical1',
        'stock_a_groups': ('refiner1','refiner2','refiner3'),
        'stock_b_groups': ('chemical1','chemical2','chemical3'),
        'etf_a': ('CRAK',),
        'etf_b': ('XLB',),
        'futures': ('CL','XB','HO','NG'),
        'signals': 'cracks plus ethane/naphtha/petrochemical margins required externally',
        'etf_quality': 'poor_XLB_is_broad_materials',
    },
}

# Direct feed-cost downstream candidates for soybean-crush research.  Keep
# each company separate so poultry/egg/hog-specific shocks are visible rather
# than hidden inside a combined basket.  SFD has short public-price history;
# the ordinary loader leaves the unavailable history missing.
for _milling_group in ('milling1', 'milling2'):
    for _protein_group in (
        'protein1', 'protein2', 'protein3', 'protein_diversified'
    ):
        _pair_name = f'{_milling_group}_vs_{_protein_group}'
        PAIR_RESEARCH_CONFIG[_pair_name] = {
            'label': f'{_milling_group} vs {_protein_group}',
            'basket_a': STOCK_BASKET_GROUPS[_milling_group],
            'basket_b': STOCK_BASKET_GROUPS[_protein_group],
            'stock_a_group': _milling_group,
            'stock_b_group': _protein_group,
            'etf_a': (),
            'etf_b': (),
            'futures': ('ZS','ZM','ZL'),
            'signals': (
                'soybean board crush; meal/oil/soybean calendar variants; '
                'inspect soybean-meal/feed-cost channel separately'
            ),
            'etf_quality': 'stock_baskets_only',
        }

PAIR_ALIASES = {
    '1': 'refiner_vs_producer', '2': 'refiner_vs_vlcc',
    '3': 'product_tanker_vs_vlcc', '4': 'heavy_refiner_vs_canadian_heavy',
    '5': 'services_vs_producer', '6': 'refiner_vs_chemical',
}


def project_root():
    return Path(__file__).resolve().parents[2]


def _ticker(value):
    value = value.upper().strip()
    if value == 'XYM':
        raise ValueError('XYM is not assumed to mean XME; use XME explicitly for metals/mining.')
    if not value or any(c not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-' for c in value):
        raise ValueError('Invalid ticker')
    return value


def _read(path):
    frame = pd.read_csv(path, low_memory=False)
    frame['date'] = pd.to_datetime(frame.date, errors='raise').dt.normalize()
    if frame.date.duplicated().any():
        raise ValueError(f'Duplicate dates: {path}')
    return frame.set_index('date').sort_index()


def _load_adjusted_data(ticker, directory, *, calendar_ticker='SPY', start=None, end=None):
    ticker = _ticker(ticker); directory = Path(directory)
    path = directory / f'{ticker}.csv'
    calendar_path = directory / f'{_ticker(calendar_ticker)}.csv'
    if not path.exists():
        raise FileNotFoundError(f'Missing {ticker} prices: {path}')
    if not calendar_path.exists():
        raise FileNotFoundError(f'Missing US calendar prices: {calendar_path}')
    calendar = _read(calendar_path).index
    frame = _read(path)
    for col in ['close','adj_close','volume']:
        if col not in frame:
            raise KeyError(f'{path} is missing {col}')
        frame[col] = pd.to_numeric(frame[col], errors='coerce')
    if (frame[['close','adj_close']] <= 0).any().any():
        raise ValueError(f'{ticker}: nonpositive price')
    if not frame.adj_close.notna().any():
        raise ValueError(f'{ticker}: no adjusted close')
    frame = frame.reindex(calendar)
    frame['raw_return'] = np.log(frame.adj_close).diff()
    frame['simple_return'] = frame.adj_close.pct_change(fill_method=None)
    frame['dollar_volume'] = frame.close * frame.volume
    frame['adv20_usd'] = frame.dollar_volume.rolling(20, min_periods=20).mean()
    frame['price_missing'] = frame.adj_close.isna()
    frame.attrs.update(ticker=ticker, price_source=str(directory))
    return frame.loc[start:end]


def load_etf_data(ticker, *, root=None, price_dir=None, start=None, end=None):
    """Adjusted log returns on observed SPY sessions; never fill missing prices.

    start/end filter AFTER returns; source SPY.csv defines the US calendar.
    No silent fallback to unadjusted close or a production price file.
    """
    directory = Path(price_dir) if price_dir else Path(root or project_root()) / 'data/research/etf_prices'
    return _load_adjusted_data(ticker, directory, start=start, end=end)


def load_stock_price_data(ticker, *, root=None, price_dir=None, start=None, end=None):
    """Load a stock from the canonical yfinance directory on observed SPY sessions."""
    directory = Path(price_dir) if price_dir else Path(root or project_root()) / 'data/equity/yfinance'
    return _load_adjusted_data(ticker, directory, start=start, end=end)


def load_equal_weight_basket(tickers, *, root=None, price_dir=None, kind='stock',
                             weights=None, start=None, end=None):
    """Load a basket; basket returns require every component and are never zero-filled."""
    tickers = tuple(_ticker(t) for t in tickers)
    if not tickers or len(set(tickers)) != len(tickers):
        raise ValueError('Basket tickers must be nonempty and unique')
    loader = load_stock_price_data if kind == 'stock' else load_etf_data
    frames = {t: loader(t,root=root,price_dir=price_dir,end=end) for t in tickers}
    if weights is None:
        weight = pd.Series(1/len(tickers),index=tickers)
    else:
        weight = pd.Series(weights,dtype=float).reindex(tickers)
        if weight.isna().any() or not np.isclose(weight.sum(),1):
            raise ValueError('Weights must cover tickers and sum to one')
    raw = pd.DataFrame({t:f.raw_return for t,f in frames.items()})
    simple = pd.DataFrame({t:f.simple_return for t,f in frames.items()})
    result = pd.concat({'raw':raw,'simple':simple},axis=1)
    result['basket','raw_return'] = raw.mul(weight).sum(axis=1,min_count=len(tickers))
    result['basket','simple_return'] = simple.mul(weight).sum(axis=1,min_count=len(tickers))
    result['basket','component_count'] = raw.notna().sum(axis=1)
    result.attrs.update(tickers=tickers,weights=weight.to_dict(),kind=kind)
    return result.loc[start:end]


def rolling_betas(stock, factors, *, window=252, min_obs=126, lag=1):
    """OLS with intercept, same complete-observation covariance formula as live.

    Each estimate uses the last window jointly valid log returns; lag counts
    rows of the supplied stock (US session) calendar. Intercept is NOT removed
    from residual return, matching live hedge PnL. No ridge/clipping.
    """
    if not 2 <= min_obs <= window or lag < 1:
        raise ValueError('Require 2 <= min_obs <= window and lag >= 1')
    if not stock.index.is_unique or not stock.index.is_monotonic_increasing:
        raise ValueError('Stock calendar must be sorted and unique')
    if factors.shape[1] not in (1,2) or not factors.columns.is_unique:
        raise ValueError('Provide one or two distinct hedge factors')
    factors = factors.reindex(stock.index)
    data = pd.concat([stock.rename('__stock'), factors], axis=1).replace([np.inf,-np.inf],np.nan).dropna()
    y = data.iloc[:,0]; x = data.iloc[:,1]
    cov = y.rolling(window,min_periods=min_obs).cov(x)
    vx = x.rolling(window,min_periods=min_obs).var()
    if factors.shape[1] == 1:
        estimates = (cov / vx.where(vx > 0)).to_frame(factors.columns[0])
    else:
        z = data.iloc[:,2]
        vz = z.rolling(window,min_periods=min_obs).var()
        xz = x.rolling(window,min_periods=min_obs).cov(z)
        yz = y.rolling(window,min_periods=min_obs).cov(z)
        det = vx*vz-xz*xz
        # Fail closed for singular/numerically collinear factors.
        det = det.where((det > 1e-12*vx*vz) & (vx > 0) & (vz > 0))
        estimates = pd.DataFrame({factors.columns[0]:(cov*vz-yz*xz)/det,
                                  factors.columns[1]:(yz*vx-cov*xz)/det})
    # Carry an estimate only over missing observation dates, not singular fits.
    estimates = estimates.reindex(stock.index, method='ffill').shift(lag)
    estimates.columns = ['beta_'+str(c) for c in estimates.columns]
    counts = pd.Series(np.minimum(np.arange(1,len(data)+1),window),index=data.index)
    estimates['beta_observations'] = counts.reindex(stock.index,method='ffill').shift(lag)
    return estimates


def residual_returns(stock, factors, betas):
    """Return r_stock - sum(beta_lagged * r_hedge), preserving missing data."""
    f = factors.reindex(stock.index)
    b = betas.reindex(stock.index)[['beta_'+str(c) for c in f.columns]].copy()
    b.columns = f.columns
    hedge = (b*f).sum(axis=1,min_count=len(f.columns))
    return (stock-hedge).rename('residual_return')


def inverse_beta_basket(raw_returns, market_return, *, window=252,
                        min_obs=126, lag=1):
    """Long-only basket with weights proportional to inverse absolute SPY beta.

    Stock betas use the same lagged rolling estimator as the other research
    helpers.  All components must have a finite nonzero beta and return; rows
    that cannot form the complete basket remain missing.
    """
    raw = pd.DataFrame(raw_returns,dtype=float).sort_index()
    if raw.empty or not raw.columns.is_unique:
        raise ValueError('raw_returns must contain distinct basket components')
    market = pd.Series(market_return,dtype=float).reindex(raw.index).rename('SPY')
    betas = pd.DataFrame(index=raw.index,columns=raw.columns,dtype=float)
    for ticker in raw:
        estimate = rolling_betas(
            raw[ticker],market.to_frame(),window=window,min_obs=min_obs,lag=lag
        )
        betas[ticker] = estimate.beta_SPY
    inverse = 1.0 / betas.abs().where(betas.abs() > 1e-12)
    complete = inverse.notna().all(axis=1) & raw.notna().all(axis=1)
    weights = inverse.div(inverse.sum(axis=1),axis=0).where(complete)
    basket = raw.mul(weights).sum(axis=1,min_count=len(raw.columns))
    basket.name = 'return_eq_beta'
    return basket, weights, betas


def load_etf_research(ticker, hedges=('SPY',), *, root=None, price_dir=None,
                      start=None, end=None, window=252, min_obs=126):
    """One-line loader. CRAK + ('SPY','XLE') gives two jointly estimated betas."""
    ticker = _ticker(ticker); hedges = tuple(_ticker(h) for h in hedges)
    if ticker in hedges or len(set(hedges)) != len(hedges):
        raise ValueError('Self/duplicate hedge is not allowed; use load_etf_data for SPY alone')
    frame = load_etf_data(ticker,root=root,price_dir=price_dir,end=end)
    f = pd.DataFrame({h:load_etf_data(h,root=root,price_dir=price_dir,end=end).raw_return for h in hedges})
    b = rolling_betas(frame.raw_return,f,window=window,min_obs=min_obs)
    frame = frame.join(b)
    frame['residual_return'] = residual_returns(frame.raw_return,f,b)
    for h in hedges:
        frame['hedge_return_'+h] = f[h]
    frame.attrs.update(ticker=ticker,hedges=hedges,window=window,beta_lag=1)
    return frame.loc[start:end]


def load_fut_continuous_data(ticker, *, root=None, family='_2', start=None, end=None):
    """Read chained futures incl original m0_ret/arrival; never diff rolled settle.

    Dates are source dates, NOT equity signal timestamps. User must respect
    arrival/known timestamps before using these features in ETF signals.
    """
    if family not in ('','_2'):
        raise ValueError('family must be canonical empty string or _2')
    ticker = _ticker(ticker)
    # The repository uses XB for NYMEX RBOB; accept the common RB shorthand.
    if ticker == 'RB':
        ticker = 'XB'
    frame = _read(Path(root or project_root()) / f'data/comm/carry_data{family}' / f'{ticker}.csv')
    frame.attrs.update(symbol=ticker,family=family)
    return frame.loc[start:end]


def load_futures_bundle(symbols, *, root=None, family='_2', start=None, end=None):
    """Load several continuous-futures tables without merging their source dates."""
    return {('XB' if _ticker(s) == 'RB' else _ticker(s)):
            load_fut_continuous_data(s,root=root,family=family,start=start,end=end)
            for s in symbols}


def load_refinery_crack_data(*, root=None, start=None, end=None):
    """Load canonical point-in-time crack signals with their availability timestamp."""
    path = Path(root or project_root())/'data/processed/refinery_crack_signals.parquet'
    frame = pd.read_parquet(path)
    frame['date'] = pd.to_datetime(frame.date,errors='raise').dt.normalize()
    frame['arrival'] = pd.to_datetime(frame.arrival,errors='raise')
    if frame.date.duplicated().any():
        raise ValueError(f'Duplicate crack dates: {path}')
    return frame.set_index('date').sort_index().loc[start:end]


def load_refinery_crack_seasonality_adjusted_data(
        *, root=None, start=None, end=None, lookback_years=8,
        smooth_window=10, smooth_min_periods=5):
    """Load an independent seasonality-adjusted copy of canonical crack data."""
    from comm_ls.refinery_crack import build_seasonality_adjusted_crack_signals

    # Load full history first: filtering before adjustment would remove the
    # prior delivery years needed to form the historical median.
    raw = load_refinery_crack_data(root=root).reset_index()
    adjusted = build_seasonality_adjusted_crack_signals(
        raw,
        lookback_years=lookback_years,
        smooth_window=smooth_window,
        smooth_min_periods=smooth_min_periods,
    )
    return adjusted.set_index('date').sort_index().loc[start:end]


_CRUSH_MONTHS = {
    'ZM': ('F','H','K','N','Q','U','V','Z'),
    'ZL': ('F','H','K','N','Q','U','V','Z'),
    'ZS': ('F','H','K','N','Q','U','X','X'),
}
_CRUSH_SCHEDULES = {
    # These are the three executed backtest_agri_v43 calendar constructions.
    'crush_01': (('12-10','02-10','04-10','06-10','07-10','08-10','09-10','10-10'), 1),
    'crush_02': (('10-10','12-10','02-10','04-10','05-10','06-10','07-10','08-10'), 2),
    'crush_03': (('07-10','09-10','11-10','01-10','02-10','03-10','04-10','05-10'), 3),
}
_CRUSH_HORIZONS = (5,10,21,30,42,50,60,90)


def _contract_settle(path):
    frame = pd.read_csv(path,usecols=['date','px_settle'])
    frame['date'] = pd.to_datetime(frame.date,errors='raise').dt.normalize()
    if frame.date.duplicated().any():
        raise ValueError(f'Duplicate dates: {path}')
    return pd.Series(pd.to_numeric(frame.px_settle,errors='coerce').to_numpy(),
                     index=frame.date,name='px_settle').sort_index()


def _calendar_crush_variant(root, expiries, previous_year_count):
    """Port the executed backtest_agri_v43 generate_crush calendar stitching."""
    data_dir = Path(root)/'data/comm'
    years = sorted({int(path.stem[:4]) for path in (data_dir/'ZM').glob('?????.csv')
                    if len(path.stem)==5 and path.stem[:4].isdigit()
                    and int(path.stem[:4]) >= 2010})
    pieces=[]; previous_end=None
    for year in years:
        for i, expiry_mmdd in enumerate(expiries):
            names = {symbol:f'{year}{_CRUSH_MONTHS[symbol][i]}'
                     for symbol in ('ZM','ZL','ZS')}
            paths = {symbol:data_dir/symbol/f'{contract}.csv'
                     for symbol,contract in names.items()}
            if not all(path.exists() for path in paths.values()):
                continue
            legs = pd.concat({symbol.lower():_contract_settle(path)
                              for symbol,path in paths.items()},axis=1)
            expiry_year = year-1 if i < previous_year_count else year
            expiry = pd.Timestamp(f'{expiry_year}-{expiry_mmdd}')
            eligible = legs.index < expiry if previous_end is None else (
                (legs.index > previous_end) & (legs.index <= expiry)
            )
            piece = legs.loc[eligible].copy()
            if not piece.empty:
                piece['contract_zm'] = names['ZM']
                piece['contract_zl'] = names['ZL']
                piece['contract_zs'] = names['ZS']
                pieces.append(piece)
            previous_end = expiry
    if not pieces:
        raise ValueError('No complete notebook-style ZS/ZM/ZL calendar segments found')
    frame = pd.concat(pieces).sort_index()
    if frame.index.duplicated().any():
        raise ValueError('Duplicate dates in notebook-style crush calendar')
    frame['crush'] = .022*frame.zm + .11*frame.zl - .01*frame.zs
    return frame


def load_soybean_crush_data(*, root=None, family='_2', start=None, end=None):
    """Load point-in-time matched crush plus the three agri-notebook variants.

    Output mirrors ``load_refinery_crack_data``: one date-indexed auxiliary
    frame with an ``arrival`` timestamp.  ``crush_01``/``02``/``03`` preserve
    the notebook calendar definitions; ``matched_soybean_crush_spread`` is the
    operational liquidity-selected series and should remain a separate test.
    """
    if family not in ('','_2'):
        raise ValueError("family must be canonical empty string or _2")
    root = Path(root or project_root())
    suffix = family
    path = root/f'data/processed/soybean_complex_signals{suffix}.parquet'
    if not path.exists():
        raise FileNotFoundError(
            f'Missing soybean crush signals: {path}. Run the post-carry refresh.'
        )
    signals = pd.read_parquet(path)
    signals['date'] = pd.to_datetime(signals.date,errors='raise').dt.normalize()
    signals['arrival'] = pd.to_datetime(signals.arrival,errors='raise')
    soybean = signals.loc[signals.symbol.astype(str).str.upper().isin(('ZS','ZM','ZL'))]
    fields = ['matched_soybean_crush_contract','matched_soybean_crush_spread']
    fields += [f'matched_soybean_crush_spread_chg_{horizon}d'
               for horizon in (5,10,21,30,42,63)]
    missing = set(fields).difference(soybean.columns)
    if missing:
        raise KeyError(f'{path} is missing crush columns: {sorted(missing)}')
    # Derived crush values are identical on ZS/ZM/ZL rows. Fail rather than
    # silently selecting a conflicting duplicate.
    value_nunique = soybean.groupby('date')[fields[1:]].nunique(dropna=True)
    if value_nunique.gt(1).any().any():
        raise ValueError('Conflicting matched crush values across soybean symbols')
    matched = soybean.groupby('date')[fields].first()
    matched['arrival'] = soybean.groupby('date').arrival.max()

    output = matched.copy()
    for name,(expiries,previous_year_count) in _CRUSH_SCHEDULES.items():
        variant = _calendar_crush_variant(root,expiries,previous_year_count)
        output[name] = variant.crush
        output[f'{name}_contract_zm'] = variant.contract_zm
        output[f'{name}_contract_zl'] = variant.contract_zl
        output[f'{name}_contract_zs'] = variant.contract_zs
        for horizon in _CRUSH_HORIZONS:
            # Exact notebook convention: row difference after stitching.
            output[f'{name}_chg_{horizon}d'] = variant.crush.diff(horizon)
    from comm_ls.soybean_complex import build_seasonality_adjusted_soybean_crush

    seasonal = build_seasonality_adjusted_soybean_crush(
        root/'data/comm', output.index
    )
    output = output.join(seasonal)
    zs = load_fut_continuous_data('ZS',root=root,family=family)['M0_settle']
    output['zs'] = pd.to_numeric(zs,errors='coerce')
    for column in ('raw','median','adjusted'):
        output[f'{column}_zs'] = output[column].div(
            output['zs'].replace(0,np.nan)
        )*1000
    output.attrs.update(source=str(path),family=family,
                        calendar_source='backtest_agri_v43 generate_crush',
                        seasonal_source='backtest_agri_v43 prior-year median')
    return output.sort_index().loc[start:end]


def load_vlcc_weekly_data(*, root=None, start=None, end=None):
    """Load reviewed Baltic VLCC observations indexed by first usable date.

    Weekly values are not expanded or forward-filled to daily sessions.
    Missing/approximate route observations remain explicit in quality columns.
    """
    path = Path(root or project_root())/'data/baltic/baltic_vlcc_weekly_spot_model.csv'
    frame = pd.read_csv(path)
    frame['usable_from_date'] = pd.to_datetime(frame.usable_from_date,errors='raise').dt.normalize()
    unavailable = int(frame.usable_from_date.isna().sum())
    frame = frame.loc[frame.usable_from_date.notna()].copy()
    if frame.usable_from_date.duplicated().any():
        raise ValueError(f'Duplicate Baltic usable dates: {path}')
    frame = frame.set_index('usable_from_date').sort_index().loc[start:end]
    frame.attrs.update(source=str(path),excluded_without_usable_date=unavailable)
    return frame


def describe_pair_research():
    """Compact table of registered pair hypotheses and available proxies."""
    rows=[]
    for name,cfg in PAIR_RESEARCH_CONFIG.items():
        rows.append({'pair':name,'label':cfg['label'],
                     'basket_a':','.join(cfg['basket_a']),'basket_b':','.join(cfg['basket_b']),
                     'etf_a':','.join(cfg['etf_a']),'etf_b':','.join(cfg['etf_b']),
                     'futures':','.join(cfg['futures']),'etf_quality':cfg['etf_quality'],
                     'signals':cfg['signals']})
    return pd.DataFrame(rows).set_index('pair')


def _resolve_pair_config(pair):
    """Resolve the original one-argument API, including named stock groups."""
    requested = PAIR_ALIASES.get(str(pair),str(pair)).lower().strip()
    if requested == 'milling1_vs_milling2':
        requested = 'milling1_vs_milling_2'
    if requested == 'refiner_vs_refiner':
        return requested, PAIR_RESEARCH_CONFIG[requested]
    match = re.fullmatch(r'refiner([123])_vs_refiner([123])',requested)
    if match:
        left = f"refiner{match.group(1)}"
        right = f"refiner{match.group(2)}"
        if left == right:
            raise ValueError('Refiner relative-value pair requires two different groups')
        cfg = dict(PAIR_RESEARCH_CONFIG['refiner_vs_refiner'])
        cfg['label'] = f'{left} vs {right}'
        cfg['basket_a'] = STOCK_BASKET_GROUPS[left]
        cfg['basket_b'] = STOCK_BASKET_GROUPS[right]
        cfg['stock_a_group'] = left
        cfg['stock_b_group'] = right
        return requested, cfg
    match = re.fullmatch(r'refiner([123]?)_vs_chemical([123]?)',requested)
    if match:
        refiner = f"refiner{match.group(1) or '1'}"
        chemical = f"chemical{match.group(2) or '1'}"
        cfg = dict(PAIR_RESEARCH_CONFIG['refiner_vs_chemical'])
        cfg['basket_a'] = STOCK_BASKET_GROUPS[refiner]
        cfg['basket_b'] = STOCK_BASKET_GROUPS[chemical]
        cfg['stock_a_group'] = refiner
        cfg['stock_b_group'] = chemical
        return requested, cfg
    match = re.fullmatch(r'refiner([123]?)_vs_producer([123]?)',requested)
    if match:
        cfg = dict(PAIR_RESEARCH_CONFIG['refiner_vs_producer'])
        refiner = f"refiner{match.group(1) or '1'}"
        producer = f"producer{match.group(2) or '1'}"
        cfg['basket_a'] = STOCK_BASKET_GROUPS[refiner]
        cfg['basket_b'] = STOCK_BASKET_GROUPS[producer]
        cfg['stock_a_group'] = refiner
        cfg['stock_b_group'] = producer
        return requested, cfg
    match = re.fullmatch(r'refiner([123])_vs_vlcc',requested)
    if match:
        cfg = dict(PAIR_RESEARCH_CONFIG['refiner_vs_vlcc'])
        refiner = f"refiner{match.group(1)}"
        cfg['basket_a'] = STOCK_BASKET_GROUPS[refiner]
        cfg['stock_a_group'] = refiner
        return requested, cfg
    if requested not in PAIR_RESEARCH_CONFIG:
        raise KeyError(
            f'Unknown pair {pair!r}; choose {sorted(PAIR_RESEARCH_CONFIG)} or a named '
            'refinerN_vs_chemicalM pair'
        )
    return requested, PAIR_RESEARCH_CONFIG[requested]


def build_pair_spread(a_return, b_return, *, market_return=None,
                      window=252, min_obs=126, lag=1):
    """Build 1:1, pair-beta-neutral and optional pair+SPY residual returns.

    Betas are estimated only on jointly observed rows and lagged by one supplied
    US-session row.  The pair+SPY result needs three tradable legs; it is not a
    two-leg dollar-neutral spread.
    """
    a = pd.Series(a_return,dtype=float).rename('a_return')
    b = pd.Series(b_return,dtype=float).reindex(a.index).rename('b_return')
    result = pd.concat([a,b],axis=1)
    result['spread_1to1'] = a-b
    pair_factor = b.rename('B').to_frame()
    pair_beta = rolling_betas(a,pair_factor,window=window,min_obs=min_obs,lag=lag)
    result['beta_B_pair'] = pair_beta.beta_B
    result['spread_pair_beta'] = residual_returns(a,pair_factor,pair_beta)
    if market_return is not None:
        market = pd.Series(market_return,dtype=float).reindex(a.index).rename('SPY')
        market_factor = market.to_frame()
        a_market_beta = rolling_betas(
            a, market_factor, window=window, min_obs=min_obs, lag=lag
        )
        b_market_beta = rolling_betas(
            b, market_factor, window=window, min_obs=min_obs, lag=lag
        )
        result['beta_A_SPY'] = a_market_beta.beta_SPY
        result['beta_B_SPY'] = b_market_beta.beta_SPY
        result['a_return_spy'] = residual_returns(a,market_factor,a_market_beta)
        result['b_return_spy'] = residual_returns(b,market_factor,b_market_beta)
        joint_factors = pd.concat([b.rename('B'),market],axis=1)
        joint_beta = rolling_betas(a,joint_factors,window=window,min_obs=min_obs,lag=lag)
        result['market_return'] = market
        result['beta_B_joint'] = joint_beta.beta_B
        result['beta_SPY_joint'] = joint_beta.beta_SPY
        result['spread_pair_spy'] = residual_returns(a,joint_factors,joint_beta)
        result['beta_observations_joint'] = joint_beta.beta_observations
    result.attrs.update(window=window,min_obs=min_obs,beta_lag=lag)
    return result


def load_pair_research(pair, *, mode='stocks', etf_a=None, etf_b=None,
                       root=None, start=None, end=None, family='_2',
                       window=252, min_obs=126, include_futures=True,
                       include_auxiliary=True):
    """One-line loader for a registered stock-basket or ETF relative-value pair.

    Returns ``a``, ``b``, ``spread``, ``futures``, ``auxiliary`` and ``config``.
    ETF candidate tuples are alternatives; selecting one never blends them.
    """
    key, cfg = _resolve_pair_config(pair)
    if mode not in ('stocks','etfs'):
        raise ValueError("mode must be 'stocks' or 'etfs'")
    if mode == 'stocks':
        a = load_equal_weight_basket(cfg['basket_a'],root=root,end=end,kind='stock')
        b = load_equal_weight_basket(cfg['basket_b'],root=root,end=end,kind='stock')
        a_ret = a['basket','raw_return']; b_ret = b['basket','raw_return']
        spy = load_stock_price_data('SPY',root=root,end=end).raw_return
        a_eq_beta, a_eq_weights, a_stock_betas = inverse_beta_basket(
            a['raw'],spy,window=window,min_obs=min_obs
        )
        b_eq_beta, b_eq_weights, b_stock_betas = inverse_beta_basket(
            b['raw'],spy,window=window,min_obs=min_obs
        )
        for ticker in a_eq_weights:
            a['eq_beta_weight',ticker] = a_eq_weights[ticker]
            a['spy_beta',ticker] = a_stock_betas[ticker]
        for ticker in b_eq_weights:
            b['eq_beta_weight',ticker] = b_eq_weights[ticker]
            b['spy_beta',ticker] = b_stock_betas[ticker]
        a['basket','return_eq_beta'] = a_eq_beta
        b['basket','return_eq_beta'] = b_eq_beta
        selected = {'a':cfg['basket_a'],'b':cfg['basket_b']}
        if cfg.get('stock_a_group'):
            selected['stock_a_group'] = cfg['stock_a_group']
        if cfg.get('stock_b_group'):
            selected['stock_b_group'] = cfg['stock_b_group']
    else:
        if not cfg['etf_a'] or not cfg['etf_b']:
            raise ValueError(f"{key} has no clean ETF pair; use mode='stocks'")
        left = _ticker(etf_a or cfg['etf_a'][0]); right = _ticker(etf_b or cfg['etf_b'][0])
        if left not in cfg['etf_a'] or right not in cfg['etf_b']:
            raise ValueError(f"ETF choices must be A={cfg['etf_a']}, B={cfg['etf_b']}")
        try:
            a = load_etf_data(left,root=root,end=end)
            b = load_etf_data(right,root=root,end=end)
        except FileNotFoundError as exc:
            raise FileNotFoundError(
                f'{exc}. Run: uv run python scripts/refresh_etf_research.py --as-of YYYY-MM-DD'
            ) from exc
        a_ret=a.raw_return; b_ret=b.raw_return
        spy=load_etf_data('SPY',root=root,end=end).raw_return
        selected={'a':left,'b':right}
    spread = build_pair_spread(a_ret,b_ret,market_return=spy,
                               window=window,min_obs=min_obs).loc[start:end]
    if mode == 'stocks':
        equal_beta_spread = build_pair_spread(
            a_eq_beta,b_eq_beta,market_return=spy,window=window,min_obs=min_obs
        )
        rename = {
            'a_return':'a_return_eq_beta',
            'b_return':'b_return_eq_beta',
            'spread_1to1':'spread_1to1_eq_beta',
            'beta_B_pair':'beta_B_pair_eq_beta',
            'spread_pair_beta':'spread_pair_beta_eq_beta',
            'beta_A_SPY':'beta_A_SPY_eq_beta',
            'beta_B_SPY':'beta_B_SPY_eq_beta',
            'a_return_spy':'a_return_spy_eq_beta',
            'b_return_spy':'b_return_spy_eq_beta',
            'beta_B_joint':'beta_B_joint_eq_beta',
            'beta_SPY_joint':'beta_SPY_joint_eq_beta',
            'spread_pair_spy':'spread_pair_spy_eq_beta',
            'beta_observations_joint':'beta_observations_joint_eq_beta',
        }
        spread = spread.join(equal_beta_spread.rename(columns=rename)[list(rename.values())])
    futures = (load_futures_bundle(cfg['futures'],root=root,family=family,
                                   start=start,end=end) if include_futures else {})
    auxiliary = {}
    named_refiner_pair = re.fullmatch(
        r'refiner[123]?_vs_(refiner[123]?|producer[123]?|vlcc|chemical[123]?)', key
    )
    if include_auxiliary and (
        named_refiner_pair is not None
        or key == 'heavy_refiner_vs_canadian_heavy'
    ):
        auxiliary['refinery_crack'] = load_refinery_crack_data(
            root=root,start=start,end=end)
        auxiliary['refinery_crack_seasonality_adjusted'] = (
            load_refinery_crack_seasonality_adjusted_data(
                root=root,start=start,end=end)
        )
    soybean_pair = (
        key in {'milling1_vs_farm','milling2_vs_farm','milling1_vs_milling_2'}
        or re.fullmatch(
            r'milling[12]_vs_protein(?:[123]|_diversified)', key
        ) is not None
    )
    if include_auxiliary and soybean_pair:
        auxiliary['soybean_crush'] = load_soybean_crush_data(
            root=root,family=family,start=start,end=end)
    named_refiner_vlcc = re.fullmatch(r'refiner[123]?_vs_vlcc',key)
    if include_auxiliary and (
        named_refiner_vlcc is not None or key == 'product_tanker_vs_vlcc'
    ):
        auxiliary['vlcc_weekly'] = load_vlcc_weekly_data(
            root=root,start=start,end=end)
    return {'a':a.loc[start:end],'b':b.loc[start:end],'spread':spread,
            'futures':futures,'auxiliary':auxiliary,
            'config':dict(cfg),'selected':selected,
            'mode':mode,'pair':key}


def explicit_etf_pnl(frame, signal, hedges=('SPY',), *, delay=1, cost_bps=25):
    """Continuous-weight approximation using simple adjusted returns, both-leg costs.

    signal is close-known stock weight. Daily hedge rebalancing costs included.
    No share rounding, borrow, financing or intraday execution model.
    """
    if delay < 1 or cost_bps < 0:
        raise ValueError('delay >= 1, cost_bps >= 0 required')
    weight = signal.reindex(frame.index).shift(delay).fillna(0.)
    weights = pd.DataFrame({'stock':weight})
    returns = pd.DataFrame({'stock':frame.simple_return})
    for h in hedges:
        weights[h] = (-weight*frame['beta_'+h]).where(weight.ne(0),0.)
        returns[h] = np.expm1(frame['hedge_return_'+h])
    if (weights.isna() | (weights.ne(0) & returns.isna())).any().any():
        raise ValueError('Active position has missing beta/return; restrict to valid coverage')
    legs = (weights*returns).where(weights.ne(0),0.)
    turnover = weights.diff(); turnover.iloc[0] = weights.iloc[0]
    cost = turnover.abs().sum(axis=1)*cost_bps/10000
    return pd.DataFrame({'gross':legs.sum(axis=1),'cost':cost,'net':legs.sum(axis=1)-cost})
