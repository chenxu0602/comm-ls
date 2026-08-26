from __future__ import annotations

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
