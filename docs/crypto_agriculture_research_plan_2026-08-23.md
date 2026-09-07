# Crypto and Agriculture Equity-Alpha Research Plan

Date: 2026-08-23

Status: research design only. Nothing in this document is approved for live
trading. The purpose is to freeze the initial scope and provide a common basis
for later data engineering, feature research, falsification and portfolio
design discussions.

## 1. Shared research objective

Both projects follow the existing comm-ls architecture:

```text
futures settlements and contract activity
    -> timestamp-safe curve and state features
    -> economically mapped equity roles
    -> market/sector residual validation
    -> commodity-beta falsification
    -> explicit tradable hedge simulation
    -> integer execution and capacity review
```

Statistical significance alone is insufficient. A candidate needs a plausible
economic channel, peer support, point-in-time data, OOS persistence and a
realistic explicit-hedge bridge.

## 2. Crypto data currently available

The current local dataset contains CME daily contract data and chained
`carry_data` for BTC, ETH and SOL.

| Symbol | Available history | Initial use |
| --- | --- | --- |
| BTC | 2017-12-15 onward, about 2,198 sessions | Primary research commodity |
| ETH | 2021-02-05 onward, about 1,403 sessions | Selective satellite |
| SOL | 2025-03-14 onward, about 369 sessions | Monitoring only |

SOL does not yet support robust curve research. Deferred settlements are often
missing and its history is too short for credible OOS validation. Preserve the
data but do not promote SOL signals.

Crypto settlement timing requires special care. A CME observation known after
the US equity close must map to the next eligible US stock session. Weekend
spot moves are not present in the daily CME settlement feature and must not be
silently backfilled into it. A future weekend-spot overlay would be a separate
timestamped input.

## 3. Initial crypto feature scope

Do not scan every generated commodity column indiscriminately. Start with a
small mechanism-based set.

### 3.1 Price, momentum and regime

- `ret_5d_v2`
- `ret_21d_v2`
- `ret_63d_v2`
- `ret_accel_21d_vs_63d_v2`
- `drawdown_63d`
- `breakout_252d`
- sustained high/low price regime features where sufficient history exists

These features test nonlinear equity responses to crypto price trends and
turning points rather than merely estimating contemporaneous BTC beta.

### 3.2 Futures basis and curve

Priority features:

- `front_second_annualized_carry`
- `front_third_annualized_carry`
- `liquid_deferred_annualized_carry`
- `activity_deferred_annualized_carry`
- their 21-day changes
- `carry_z_252d`
- `carry_pctile_252d`
- `front_third_annualized_carry_same_contract_chg_21d`

For crypto, curve states can represent financing demand, leverage, futures
participation and institutional positioning. Prefer activity/liquidity-selected
deferred contracts. Do not prioritize generic named-calendar features such as
June-December unless a specific seasonal hypothesis justifies them.

### 3.3 Volatility state

- `realized_vol_20d`
- `realized_vol_63d`
- `vol_chg_20d`
- `abs_ret_z_252d`
- `large_move_2sigma`

Volatility may be more relevant than direction for exchanges and brokers
because it can affect customer engagement and trading revenue.

### 3.4 Futures participation

- `volume_z_252d`
- `oi_z_252d`
- `volume_shock_63d`
- `oi_shock_63d`
- `price_volume_confirm_21d`
- `price_oi_confirm_21d`

Price and OI should also be interpreted jointly. Price appreciation with
rising OI is different from a price rally driven by falling OI and short
covering.

### 3.5 Cross-crypto features for a later phase

- ETH/BTC relative return over 21 and 63 days
- ETH carry minus BTC carry
- ETH volatility minus BTC volatility
- BTC/ETH curve-state agreement or disagreement
- SOL/ETH momentum as monitoring only

All cross-crypto features must align observations by actual known timestamp,
not settlement-date labels alone.

## 4. Crypto equity roles and initial universe

Do not pool all crypto equities into one homogeneous basket.

### 4.1 Relatively pure BTC miners

Initial research basket:

- MARA
- RIOT
- CLSK
- CIFR
- BTDR

Primary candidate mechanisms are BTC momentum, carry/basis, volatility and
futures OI/volume. Mining economics are also affected by difficulty, hash rate,
power price, fleet efficiency, dilution and financing; these variables are not
yet in the daily futures feature set.

### 4.2 Hybrid miner/data-center companies

Keep these in a separate cohort:

- IREN
- WULF
- CORZ
- HUT
- HIVE
- APLD

AI and data-center transitions create role drift and can break the peer logic
of a pure miner basket. Their effective-dated business mix should eventually
be recorded in the fundamental exposure registry.

### 4.3 Exchanges and financial platforms

- COIN
- HOOD
- GLXY

This group should emphasize volatility, volume, OI and BTC/ETH relative-state
features. It should not share a signal rule automatically with miners.

### 4.4 Treasury/control name

- MSTR

MSTR is primarily a BTC treasury and financing vehicle. Without a direct BTC
or spot-BTC-ETF hedge, it is difficult to isolate residual stock alpha. Treat
it as a control rather than an initial deployable sleeve.

## 5. Crypto liquidity and capacity observations

The local equity panel through 2026-08-21 gives the following approximate
stressed ADV values. The project definition is the 25th percentile of the
trailing 252 observations of lagged 63-day median dollar volume.

| Ticker | Approximate stressed ADV | Comment |
| --- | ---: | --- |
| MARA | USD 441m | Liquid initial miner |
| CIFR | USD 390m | Liquid initial miner |
| RIOT | USD 281m | Liquid initial miner |
| CLSK | USD 230m | Liquid initial miner |
| BTDR | USD 63m | Lower-capacity initial miner |
| HIVE | USD 29m | Second tier |
| BTBT | USD 41m | Low-price/execution concerns |
| IREN | USD 1.42bn | Liquid but hybrid exposure |
| WULF | USD 408m | Liquid but hybrid exposure |
| CORZ | USD 191m | Hybrid exposure |
| HUT | USD 226m | Hybrid exposure |

BITF is deferred because the current equity source does not provide a usable
price history in the processed panel. It is not required for cache validation
and should only be reconsidered after its ticker/history continuity is
resolved.

At pilot size, miner stock volume is not the main constraint. Borrow
availability and fees, overnight/weekend gaps, dilution, corporate actions and
the liquidity of the hedge ETF may be more important. Refresh the capacity
audit before any deployment because crypto-equity liquidity changes quickly.

## 6. Crypto hedge research convention (2026-08-24)

The agreed research architecture has five distinct layers. Do not collapse
them into one reported PnL series:

| Layer | Construction | Purpose | Tradable interpretation |
| --- | --- | --- | --- |
| Baseline | SPY-only residual | Main equity-alpha research unit | Diagnostic residual, not an executed portfolio |
| Direct futures falsification | SPY + CME BTC futures-beta residual | Test survival after stripping direct BTC beta without an ETF intermediary | Diagnostic only; BTC futures will not be traded as the hedge |
| Candidate | SPY + BITO residual | Test whether a tradable ETF removes common BTC exposure more realistically | Research candidate from BITO inception onward |
| Incremental falsification | SPY + BITO + CME-BTC residual | Test whether CME BTC removes exposure left after the ETF factor | Diagnostic only |
| Final simulation | Raw stocks + explicit SPY and BTC ETF positions | Measure implementable PnL, costs, rounding and capacity | Required bridge before any live approval |

The strategy will not trade BTC, ETH, other cryptocurrencies or BTC futures as
hedges. A liquid BTC ETF may be traded as the explicit hedge if it passes the
research and execution review below.

### 6.1 Implemented return-column convention

The isolated crypto processed panel maps every crypto equity to:

```text
market_ticker = SPY
sector_ticker = BITO
```

This comes from `config/crypto_theme_sector_hedges.csv`, which is used only by
the crypto research build. The return columns now have distinct meanings:

- `residual_return_mkt_w12m`: SPY-only baseline;
- `residual_return_mktcomm_w12m`: joint SPY + CME commodity-futures residual (BTC in the isolated BTC panel, ETH in the isolated ETH panel);
- `residual_return_mktsec_w12m`: joint SPY + BITO research residual;
- `residual_return_mktseccomm_w12m`: SPY + BITO + CME-BTC falsification.

The mapping applies to all five notebook groups:

- `miners_core`
- `miners_hybrid`
- `platforms`
- `treasury_control`
- `monitor_only`

The notebook group name does not select a hedge. `load_stock_data()` merely
loads the hedge mapping and return columns already embedded in the chosen
feature-return cache.

### 6.2 BTC ETF candidate layer

The working hypothesis is to test one liquid BTC ETF across all crypto groups,
while estimating hedge coefficients separately by stock or economic role. A
common ETF does not imply a common hedge notional.

BITO is the provisional research ETF because its 2021 inception permits the
2022+ strategy sample. It is not a live hedge approval. Before promotion,
compare it with the liquid spot-BTC ETFs on:

- point-in-time return history and inception date;
- ADV, spread and expected market impact;
- borrow availability and fee when the required hedge is short;
- tracking difference versus CME BTC and the relevant US-session timing;
- operational availability in the IB account.

Spot-BTC ETFs have shorter histories than CME BTC futures. Do not splice a
futures proxy into the pre-inception ETF series and label the result an ETF
backtest. Report the actual ETF-history result separately from any longer
futures-based diagnostic.

### 6.3 Group-specific interpretation

Apply the same four-layer comparison to every group, but do not assume equal
BTC sensitivity or linearity:

- pure miners have operating leverage, power-cost and difficulty exposure;
- hybrid miners/data centers have effective-dated business-mix drift;
- platforms respond to volatility and trading activity as well as BTC price;
- MSTR is a treasury and financing vehicle with especially large and possibly
  nonlinear BTC sensitivity;
- monitoring names must not be promoted merely because an ETF hedge improves
  their historical curve.

WGMI, BKCH and DAPP remain secondary crypto-equity/industry ETF comparisons.
They are not the default candidate layer and must not silently replace the BTC
ETF experiment.

### 6.4 Required comparison and terminology

For each ticker and role basket, retain these outputs:

1. SPY-only `residual_return_mkt_w12m`;
2. SPY + BTC futures `residual_return_mktcomm_w12m` falsification;
3. SPY + BITO `residual_return_mktsec_w12m` over BITO's actual history;
4. SPY + BITO + BTC futures `residual_return_mktseccomm_w12m` incremental falsification;
5. raw-stock PnL plus continuous explicit SPY/BTC-ETF hedges;
6. integer-rounded explicit PnL after stock and hedge turnover costs, borrow,
   dividends and execution delay.

If the signal works only in the SPY-only baseline, classify it as BTC beta
transmission until evidence shows otherwise. Survival after futures-beta
stripping is stronger stock-specific-alpha evidence. Regardless of the
residual result, only the raw-stock plus explicit-ETF simulation is tradable.

This section records a research convention, not a production promotion. No
crypto sleeve, hedge coefficient or live allocation is currently approved;
BITO remains a provisional research choice.

## 7. Agriculture initial commodity scope

The first agriculture data phase contains seven products organized into three
economic chains:

1. ZC: CBOT Corn
2. ZS: CBOT Soybeans
3. ZM: CBOT Soybean Meal
4. ZL: CBOT Soybean Oil
5. HE: CME Lean Hogs
6. PRK: CME Pork Cutout
7. KC: ICE Futures U.S. Coffee C

ZS/ZM/ZL support the matched soybean crush; ZC/ZM/HE/PRK support feed,
hog-production and pork-packer margin states; KC is an independent Arabica
input-cost chain. PRK is a short-history, potentially sparse contract and must
remain shadow-quality until settlement, volume, open-interest and stale-price
checks pass. KC requires a separate ICE adapter but must normalize into the
same contract-level and known-time schema.

ZW, LE, SB and CT are deferred. GF remains lower priority because it has no
clean listed US feedlot equity mapping. Add a product only after its equity
channel and contract-month mapping are reviewed.

## 8. Agriculture feature families

### 8.1 Standard features

- 5/21/63-day same-contract returns
- return acceleration
- drawdown and breakout states
- realized volatility
- volume/OI z-scores and shocks
- activity-selected deferred carry

### 8.2 Crop-calendar curve features

Agriculture must be organized by crop year and harvest cycle rather than only
M0/M1/M2.

- old-crop/new-crop spread
- old-crop/new-crop annualized carry
- 5/21-day spread change
- same-contract changes
- crop-season or contract-season z-scores
- nearby versus deferred crop-year states

Examples include July versus December for corn and July versus November for
soybeans. Each product needs its own reviewed contract calendar.

### 8.3 Cross-commodity economic features

- Corn/Soybeans relative-price ratio for acreage economics
- Corn plus Soybean Meal feed-cost basket
- soybean meal versus soybean oil product-value composition
- matched soybean crush margin

## 9. Soybean crush decision

The complete crush feature is included in phase one. It requires ZS, ZM and
ZL; a ZS/ZM-only measure must not be labelled soybean crush.

After normalizing exchange quotations, a simplified board crush proxy in USD
per soybean bushel is:

```text
crush_usd_per_bushel
    = 0.022 * ZM_usd_per_short_ton
    + 0.11  * ZL_cents_per_lb
    - 0.01  * ZS_cents_per_bushel
```

The coefficients represent approximately 44 pounds of meal and 11 pounds of
oil per soybean bushel. This is a standardized board proxy, not a company-level
realized margin.

Required feature variants:

- matched crush level
- 5-day and 21-day crush change
- crop-season crush z-score
- nearby versus deferred crush margin
- meal and oil contribution shares
- crush state confirmed by futures volume/OI

Contracts must be delivery-matched using a reviewed mapping. Do not combine
three unrelated front contracts. For example, a soybean month without an
identical meal/oil delivery month needs an explicit documented matching rule.

High board crush is a plausible positive state for processors, but ADM and BG
also depend on local basis, merchandising, logistics, hedges, capacity and
utilization. Direction must be validated rather than assumed.

## 10. Initial agriculture equity universe

The maintained research universe is
`config/agriculture_equity_universe.csv`. Inclusion is not production approval;
all candidates remain blocked from deployment until timestamp-safe data,
point-in-time selection, OOS validation and an explicit-hedge bridge pass.

### 10.1 Grain processors

- ADM
- BG

Primary mechanisms: crush margin, basis/curve state, exports, merchandising
and processing utilization.

### 10.2 Feed and protein chain

- PPC
- TSN
- SFD
- JBS

PPC primarily maps to the ZC/ZM feed basket. TSN, SFD and JBS require separate
feed, hog-production and pork-packer states. SFD has only short Nasdaq history
and JBS only short NYSE history; both are forward-research names, not
long-history backtest evidence.

### 10.3 Coffee consumers

- SBUX
- KDP
- BROS

Primary mechanism: KC Arabica input cost versus inventory, hedging and delayed
retail price pass-through. KDP is more staples-like; SBUX and BROS carry more
consumer-discretionary and store-growth exposure.

### 10.4 Deferred-data names

- GIL: CT cotton input cost
- CSAN: SB sugar/ethanol, BRL, oil and logistics
- AGRO: SB sugar/ethanol and regional agriculture production

These names belong in the equity universe now but cannot enter feature
selection until CT or SB data and their economic-state definitions exist.

### 10.5 Hedge research convention

Agriculture hedge selection is not frozen. Use SPY-only residuals as the
baseline and compare MOO, PBJ, XLP and XLY by economic group using
`config/agriculture_hedge_candidates.csv`. The exact ticker-level narrow and
liquid candidates are recorded in
`config/agriculture_ticker_hedge_candidates.csv`: MOO versus XLP for ADM/BG;
PBJ versus XLP for PPC/TSN/SFD/JBS/KDP; and PEJ versus XLY for SBUX/BROS. Do
not silently use one agriculture ETF for every group. In particular, KDP is
staples-like while SBUX/BROS are more discretionary, and MOO does not remove
the Brazil/FX exposure in CSAN or AGRO. ETF constituent overlap with target
stocks must be measured before an explicit tradable hedge is approved.

The beta build keeps two sector mappings as separate research panels, neither
of which is live hedge approval. The narrow panel is
`data/processed/equity_processed_agriculture_sector.parquet`, configured by
`config/agriculture_ticker_sector_hedges.csv`: ADM/BG use MOO;
PPC/TSN/SFD/JBS/KDP use PBJ; SBUX/BROS use PEJ; GIL uses XLY; and CSAN/AGRO
use MOO. The liquid panel is
`data/processed/equity_processed_agriculture_liquid_sector.parquet`, configured
by `config/agriculture_ticker_liquid_sector_hedges.csv`: ADM/BG and the
protein/KDP group use XLP; SBUX/BROS/GIL use XLY; CSAN/AGRO remain on MOO until
a reviewed liquid alternative exists. Every stock also receives a SPY market
beta. In both panels `residual_return_mkt_w12m` is the identical SPY-only
baseline; `residual_return_mktsec_w12m` differs by the selected sector ETF.

The operator workflow also combines those sources into
`data/processed/equity_processed_agriculture.parquet`. In that canonical
Agriculture research panel, `residual_return_mktsec_w12m` and
`residual_return_mktsec_narrow_w12m` are exact aliases of the narrow-sector
result, while `residual_return_mktsec_liquid_w12m` records the liquid-sector
alternative. Likewise, `sector_ticker` aliases `sector_ticker_narrow`, and
`sector_ticker_liquid` is explicit. Existing non-Agriculture return-column
conventions are unchanged. The canonical alias must never be switched based on
which hedge has the better in-sample result.

The current twelve-name research universe is ADM, BG, PPC, TSN, SFD, JBS,
SBUX, KDP, BROS, GIL, CSAN and AGRO.

## 11. Separate agriculture futures module

Agriculture should not be forced into the existing energy/metals carry logic.
Create a dedicated package:

```text
src/comm_ls/agriculture/
    contracts.py
    ingest.py
    curve.py
    features.py
    validation.py
```

### `contracts.py`

- exchange symbols and active months
- quote units and conversion factors
- crop-year definitions
- old-crop/new-crop anchors
- soybean crush contract matching

### `ingest.py`

- settlement, high/low, volume and OI normalization
- source priority and overlap rules
- known timestamp and arrival mapping
- duplicate and revision handling

### `curve.py`

- product-specific liquidity selection
- crop-year-aware curve construction
- roll hysteresis
- same-contract returns
- old/new-crop curves

### `features.py`

- standard momentum/carry/volatility features
- seasonal and crop-calendar features
- corn/soy ratio
- feed-cost basket
- matched soybean crush

### `validation.py`

- quote-unit invariants
- contract-month and crop-year checks
- crush-leg matching
- no-lookahead and arrival checks
- holiday continuity
- roll-gap-free return checks
- missing settlement fail-closed behavior

Proposed data layout:

```text
data/comm/agriculture/{SYMBOL}/{CONTRACT}.csv
data/comm/agriculture/curve_data/{SYMBOL}.parquet
data/processed/agriculture_signals.parquet
```

Proposed initial CLI boundary:

```bash
uv run comm-ls build-agriculture-curve-data
uv run comm-ls build-agriculture-signals
```

The normalized raw contract schema may reuse common project utilities, but
crop-year selection, seasonal features and crush construction belong inside
the agriculture package.

## Current Crypto implementation handoff

For the production/research state effective with the 2026-09-08 target,
including the USD 3,000 AUM decision and HG-carry plus NG-power sleeve, read
`docs/current_crypto_status_2026-09-08.md` before making changes.

At a glance:

- Crypto is a separate IB book with USD 3,000 AUM; do not net its SPY hedge
  with CL/Metals.
- Production weights are Platforms/BTC/ETH/HG+NG = 20%/30%/20%/30%, replacing
  the prior 30%/35%/35% allocation.
- The new shared sleeve uses HG `carry_chg_20d` together with the 20- and
  5-session changes of NG `calendar_U_Z_annualized_carry`, followed by a
  two-session rolling-mean smoothing and the existing one-session target
  delay.
- Its internal MARA/RIOT/CLSK/COIN/HOOD/HIVE weights are
  15%/20%/20%/20%/15%/10%.
- Production implementation is in `src/comm_ls/crypto_strategy.py`; HG and NG
  are independently aligned from `commodity_signals_2.parquet` to the MARA
  calendar under `stock_observation_asof`. They are signal drivers, never
  crypto-equity return sources.
- The 2026-09-04 HG+NG signal is zero. The frozen 2026-09-08 package has 20%
  gross short stock exposure, +67.14% continuous SPY hedge, and only three
  stock orders: buy 2 CLSK, buy 7 HIVE, buy 1 MARA. Existing three SPY shares
  remain unchanged under executable integer rounding.
- The standalone residual backtest Sharpe is 1.388 and the revised displayed
  portfolio Sharpe is 2.634, but BTC-beta residual falsification, true OOS,
  multiple-testing review, explicit-hedge simulation, and live reconciliation
  remain open. This is not a fully validated deployment promotion.

## 12. Proposed research sequence

### Crypto

1. Audit and effective-date the BTC/ETH equity taxonomy.
2. Separate pure miners, hybrid data-center miners and financial platforms.
3. Build a focused BTC feature-return cache.
4. Run role-specific diagnostics on both residual targets.
5. Freeze train/OOS periods and directions before portfolio comparison.
6. Test SPY plus WGMI for miners and SPY plus DAPP/BKCH for platforms.
7. Audit ETF point-in-time holdings, ADV, spread and borrow before deployment.
8. Keep ETH selective and SOL monitoring-only.

### Agriculture

1. Freeze ZC/ZS/ZM/ZL contract specifications and source policy.
2. Implement the dedicated agriculture module and validation tests.
3. Build crop-year curves before building generic features.
4. Validate soybean crush units and contract matching independently.
5. Build the feed-cost, crop-economics and processor feature groups.
6. Map each feature group only to economically relevant equity roles.
7. Run point-in-time residual and commodity-beta falsification after sufficient
   history is available.

## 13. Open decisions for the next discussion

- Whether spot-crypto ETFs remain permanently prohibited or only excluded from
  the first hedge comparison.
- WGMI versus another miner ETF after point-in-time holdings and liquidity
  review.
- DAPP versus BKCH for the platform sleeve, or whether a transparent peer
  basket is preferable to either ETF.
- Exact BTC/ETH OOS split given ETH's shorter history.
- Agriculture source policy and minimum historical start date.
- Reviewed crop-year and contract-matching tables for ZC/ZS/ZM/ZL.
- Whether USDA, weather and export data remain confirmation overlays or become
  separate event gates after the futures-only baseline is frozen.
