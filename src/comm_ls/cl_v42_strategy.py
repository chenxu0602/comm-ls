from __future__ import annotations

import numpy as np
import pandas as pd

from comm_ls.cl_v32_strategy import SleeveConfig, position_from_signal, signal_from_features
from comm_ls.cl_v41_strategy import CL_V41_MAX_SINGLE_NAME_WEIGHT, CL_V41_SLEEVE_CONFIG


CL_V42_MAX_SINGLE_NAME_WEIGHT = CL_V41_MAX_SINGLE_NAME_WEIGHT
CL_V42_CACHE_SUFFIX = ""
CL_V42_EFFECTIVE_TARGET_DATE = "2026-08-24"

# v4.2 changes exactly one strategy rule relative to v4.1: the existing CL
# tanker position is flattened whenever the independently delayed NG state has
# the opposite sign. All ordinary commodity features use canonical caches.
CL_V42_SLEEVE_CONFIG = dict(CL_V41_SLEEVE_CONFIG)

CL_V42_SHIPPING_VETO_CONFIG = SleeveConfig(
    weight=0.0,
    tickers=("DHT", "FRO", "TNK", "STNG", "INSW"),
    feature_symbol="NG",
    feature="jun_dec_annualized_carry_v2",
    threshold=1.0,
    side_mult=1,
    position_mode="sign",
    hold_days=None,
    rolling_days=None,
    sector_hedge=None,
    internal_weights={
        "DHT": 0.20,
        "FRO": 0.20,
        "TNK": 0.20,
        "STNG": 0.20,
        "INSW": 0.20,
    },
    signal_rule="asymmetric_hysteresis",
    feature_scale="z",
)


def shipping_veto_position(features: pd.DataFrame) -> pd.Series:
    """Return the one-session-delayed NG state used to veto tanker exposure."""
    signal = signal_from_features(features, CL_V42_SHIPPING_VETO_CONFIG)
    return position_from_signal(signal, CL_V42_SHIPPING_VETO_CONFIG)


def apply_shipping_opposition_veto(
    shipping_position: pd.Series,
    ng_position: pd.Series,
) -> tuple[pd.Series, pd.Series]:
    """Flatten shipping only when the CL and NG position signs oppose."""
    shipping, ng = shipping_position.align(ng_position, join="left")
    opposed = np.sign(shipping) * np.sign(ng.fillna(0.0)) < 0
    return shipping.mask(opposed, 0.0), opposed.astype(bool)
