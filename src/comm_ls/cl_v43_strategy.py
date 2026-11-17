from __future__ import annotations

from dataclasses import replace
import pandas as pd

from comm_ls.cl_v42_strategy import (
    CL_V42_MAX_SINGLE_NAME_WEIGHT,
    CL_V42_SHIPPING_VETO_CONFIG,
    CL_V42_SLEEVE_CONFIG,
)


# v4.3 keeps the v4.2 strategy and veto rules unchanged.  Only the commodity
# observation-to-stock-session alignment changes, and production is pinned to
# the independently built _2 shadow input family.
CL_V43_MAX_SINGLE_NAME_WEIGHT = CL_V42_MAX_SINGLE_NAME_WEIGHT
CL_V43_CACHE_SUFFIX = "_2"
CL_V43_FEATURE_ALIGNMENT_MODE = "stock_observation_asof"
CL_V43_EFFECTIVE_TARGET_DATE = "2026-08-26"
CL_V43_SLEEVE_CONFIG = dict(CL_V42_SLEEVE_CONFIG)
CL_V43_SHIPPING_VETO_CONFIG = CL_V42_SHIPPING_VETO_CONFIG

CL_V43_RISK_REDUCTION_DATE = "2026-10-23"
CL_V43_CHEMICAL_PAUSE_REFINER_CUT_DATE = "2026-10-28"


def live_config_for_target(config, target_date):
    """Operator risk reduction; preserve historical/research configuration."""
    out = dict(config)
    if pd.Timestamp(target_date) >= pd.Timestamp(CL_V43_RISK_REDUCTION_DATE):
        out['chemical'] = replace(out['chemical'], weight=.14)
        out['psx_ref'] = replace(out['psx_ref'], weight=0.)
    from comm_ls.cl_refiner_slow import REFINER_BLEND_EFFECTIVE_DATE, REFINER_SLOW_CONFIG
    if pd.Timestamp(target_date) >= pd.Timestamp(REFINER_BLEND_EFFECTIVE_DATE):
        out['refiner'] = replace(out['refiner'], weight=.05)
        out['refiner_slow'] = REFINER_SLOW_CONFIG
    if pd.Timestamp(target_date) >= pd.Timestamp(CL_V43_CHEMICAL_PAUSE_REFINER_CUT_DATE):
        out['chemical'] = replace(out['chemical'], weight=0.)
        out['refiner'] = replace(out['refiner'], weight=.025)
        out['refiner_slow'] = replace(out['refiner_slow'], weight=.05,
            feature='refiner_slow_state_v2',
            internal_weights={'DK': .3, 'DINO': .25, 'PBF': .25, 'PSX': .2})
    if pd.Timestamp(target_date) >= pd.Timestamp('2026-11-02'):
        from comm_ls.cl_re_c03 import RE_C03_CONFIG
        weights = dict(chemical=0., shipping=.20, refiner=.03,
                       refiner_slow=.10, psx_ref=0., services=.20,
                       metals=0., bwt=.02, fuel=0., cro=0.)
        for name, weight in weights.items():
            if name in out:
                out[name] = replace(out[name], weight=weight)
        # Retain the historical slow component identifier for ownership continuity.
        out['refiner'] = replace(out['refiner'],
            internal_weights={'DK': .3, 'DINO': .4, 'PBF': .3})
        out['refiner_slow'] = replace(out['refiner_slow'],
            feature='refiner_slow_state_v3', tickers=('DINO','DK','PBF'),
            internal_weights={'DK': .4, 'DINO': .3, 'PBF': .3})
        out.pop('cro', None)
        out['re_c03'] = RE_C03_CONFIG
    if pd.Timestamp(target_date) >= pd.Timestamp('2026-11-04'):
        from comm_ls.cl_cro import CRO_CONFIG
        out['chemical'] = replace(out['chemical'], weight=.20,
            tickers=('DOW','LYB','WLK','CE'),
            internal_weights={'DOW':.3,'LYB':.3,'WLK':.1,'CE':.3},
            feature_symbol='CHEMICAL_LP', feature='chemical_lp_state',
            signal_rule='chemical_lp_precomputed', position_mode='fixed_hold',
            hold_days=2, rolling_days=None)
        out['refiner_slow'] = replace(out['refiner_slow'], weight=.08)
        out['re_c03'] = replace(out['re_c03'], weight=.10)
        # Notebook weights sum to .9; state_v2 retains that idle capacity
        # while satisfying the normalized within-basket config invariant.
        out['cro'] = replace(CRO_CONFIG, weight=.20, feature='cro_state_v2',
            internal_weights={'VLO': 1/3, 'MPC': 2/9, 'PSX': 2/9, 'PBF': 2/9},
            tickers=('VLO', 'MPC', 'PSX', 'PBF'))
    if pd.Timestamp(target_date) >= pd.Timestamp('2026-11-06'):
        # Operator drawdown risk override; released capacity is not reallocated.
        out['shipping'] = replace(out['shipping'], weight=.10)
        out['refiner_slow'] = replace(out['refiner_slow'], feature='refiner_slow_state_v4')
    if pd.Timestamp(target_date) >= pd.Timestamp('2026-11-09'):
        for name, weight in {'chemical':.15, 'shipping':.10, 'services':.10}.items():
            out[name] = replace(out[name], weight=weight)
    return out
