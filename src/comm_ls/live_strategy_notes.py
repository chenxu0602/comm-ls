"""Effective-dated strategy handoff text for generated execution packages."""
import pandas as pd


def strategy_notes(target_date, *, cro_enabled=False, agri_aum=None,
                   cro_active=None, agri_active=None):
    day = pd.Timestamp(target_date)
    lines = ['## Strategy changes and allocation notes', '']
    if day >= pd.Timestamp('2026-11-16'):
        lines.append('- Metals reweight from target2026-11-16: hg_gc_gap15/accel20/SCO-vol25/copper15/miners25%; alloys0 and notebook-only hg_gc_gap_gc_carry_iron_2=0. Nominal100%, no normalization; copper10->15 uses the previously idle5pp. AUM5000, legacy DAILY SPY+XME hedges, signal rules,12% name cap and execution controls unchanged. See docs/metals_reweight_2026-11-16.md.')
    if day >= pd.Timestamp('2026-10-23'):
        lines += [
            '- CL operator risk reduction effective target session 2026-10-23: chemical allocation reduced from 28% to 14%; psx_ref allocation reduced from 5% to 0% (suspended). At that decision, released 19 percentage points remained cash; no renormalization. Later dated decisions below supersede allocation details.',
            '- At that decision other sleeves were unchanged. CL AUM $15,000 and legacy daily beta remain unchanged. CRO retains its own PSX leg and SPY-only hedge: clearing psx_ref does NOT mean flattening all account PSX. Recompute net stocks and component hedges.',
            '- Chemical is halved BEFORE the existing 5% net single-name cap; previously capped names need not fall by exactly half. Allocation migration turnover is not a signal change.',
            '- Chemical decision rationale: operator questioned the economic clarity of asymmetric exits plus renewing hold-21 and potential historical overfitting, not only recent losses. Rules are deterministic and unchanged; overfitting is a concern, not an established finding. Review parameter robustness, simpler exits, hedge/cost attribution and a 28% counterfactual before any restoration. See docs/cl_risk_reduction_2026-10-23.md.',
        ]
    if pd.Timestamp('2026-10-26') <= day < pd.Timestamp('2026-10-28'):
        lines += [
            '- APPROVED refiner blend effective target session 2026-10-26: refiner_slow 10% + refiner 5%; psx_ref remains suspended at 0%. This raises live combined refiner allocation from 10% to 15%, using 5 percentage points of idle capacity, not a change in CL AUM or automatic renormalization.',
            '- refiner_slow basket DK/DINO/PBF/PSX = 30/20/30/20%; existing refiner DK/DINO/PBF = 50/20/30%. Both hedge with SPY + XLE using retained legacy DAILY beta. CRO remains separate and SPY-only; preserve component ownership before account netting.',
            '- Slow rule: HO front_third_annualized_carry change over 50 stock observations; carry-level std 60/min30; entry 1.25 std, exit 0.95 std; CL m1 10-session return gate versus 0.5 times daily 20/min10 std. No fixed 10-day hold, no rolling-5 smoothing. Current input lookbacks and arrivals fail closed.',
            '- Chemical remains TEMPORARILY 14% in production as an operator stop-loss-like risk-budget override; notebook/research remains 28%. Restoration requires a new operator decision after a clear risk reduction; no numeric trigger, date or automatic restoration is authorized. Do not return it to 28% as part of this refiner change.',
            '- Full aligned refiner stock gross can reach 14.5% after the DK 5% net-name cap, before separate CRO. Size reduction or new sleeve orders caused by this change are allocation migration, not a new commodity signal. See docs/cl_refiner_blend_production_2026-10-26.md.',
        ]
    if pd.Timestamp('2026-10-28') <= day < pd.Timestamp('2026-11-02'):
        lines += [
            '- CURRENT CL risk override effective target session 2026-10-28 supersedes earlier allocations: chemical 14% -> 0% (suspended), refiner 5% -> 2.5%, refiner_slow 10% -> 5%. Released 21.5 percentage points stay cash; no renormalization. CL AUM remains $15,000.',
            '- Chemical suspension reflects unresolved exit-rule economics pending chemical input/output commodity research; refiner reduction limits drawdown risk. Neither is proof of alpha failure or an optimized historical improvement. Notebook/research chemical remains 28%; no signal rules changed. Restoration requires renewed operator approval; no automatic restoration.',
            '- psx_ref remains 0%; CRO remains 10% allocation with SPY-only hedging. Old/slow refiner retain SPY/XLE legacy DAILY beta; the slow basket sync is recorded below. Other books and AUM are unchanged. Do not flatten all PSX or remove shared ETF hedges independently of component targets.',
            '- Refiner_slow notebook sync effective 2026-10-28: DK/DINO/PBF/PSX = 30/25/25/20%; CL momentum/vol gate uses carry_data CL m0_ret, not m1_ret; carry change uses ffill then diff(50). Slow allocation remains 5%, old refiner 2.5%; no fixed hold or smoothing. Earlier basket descriptions are superseded.',
            '- Recompute component hedges and account-netted orders from actual inventories; allocation migration is separate from signal turnover. Stock execution caps may leave remaining positions for later sessions. See docs/cl_risk_reduction_2026-10-28.md.',
        ]
    if agri_aum is not None and day >= pd.Timestamp('2026-10-02'):
        lines += [
            f'- Agriculture v4.3 joined the main account effective 2026-10-02: ${agri_aum:,.0f} allocated AUM. Idle allocation remains cash and still counts in account AUM.',
            '- Agriculture uses component-specific hedges: narrow-sector residual sleeves use SPY + MOO for ADM/BG; adm_bg/adm_tsn/bg_tsn use SPY only. Keep its virtual book separate.',
        ]
        if agri_active is not None:
            lines.append(f"- Agriculture stock target state for this package: {'active' if agri_active else 'flat'}. This is not a permanent suspension.")
        if day >= pd.Timestamp('2026-11-16'):
            lines.append('- Agriculture notebook basket weights: crush_vol ADM60/BG40; crush_vol2 ADM70/BG30; crush_vol3 ADM100; adm_tsn equal/opposite ADM/TSN. Each sleeve allocation25%, no extra normalization.')
            lines.append('- ADM/TSN rule and allocation sync from 2026-11-16: crush_02 momentum with ADM-minus-TSN adjusted-price distance entry gates; equal/opposite dollar legs, no rolling pair-beta sizing. Operator allocation25% (previously15%); crush_vol25/crush_vol2 25%/ADM-only crush_vol3 25%, adm_bg/adm_bg2/bg_tsn0. Nominal100%, no normalization; AUM2000 unchanged. crush_vol3 uses adjusted_zs volatility with MA50 entry constraints and SPY + MOO explicit hedges. See docs/agri_crush_vol3_sync_2026-11-16.md.')
    if pd.Timestamp('2026-11-02') <= day < pd.Timestamp('2026-11-04'):
        lines += [
            '- CURRENT CL from 2026-11-02: chemical 0% (25% research dummy is NOT live), shipping 20%, refiner 3%, refiner_slow/re_slow 10%, services 20%, bwt 2%, re_c03 20%, others including CRO 0%. Budget 75%; no renormalization; all book AUMs unchanged.',
            '- re_c03 replaces CRO: DINO/MPC/VLO 20/30/50%, full balance, quarterly near MA3-MA30 entry, far change5 exit, far std30 thresholds. SPY + XLE legacy DAILY hedges; old CRO half-balance/SPY-only retired.',
            '- Refiner DK/DINO/PBF 30/40/30%; slow DK/DINO/PBF 40/30/30%, HO m1 momentum gate and carry ffill.diff50. Other algorithms unchanged. Track allocation/hedge migration separately. See docs/cl_reallocation_2026-11-02.md.',
        ]
    if pd.Timestamp('2026-11-04') <= day < pd.Timestamp('2026-11-06'):
        lines += [
            '- CURRENT CL from 2026-11-04: chemical20/shipping20/refiner3/refiner_slow8/services20/bwt2/CRO20/re_c03 10%; nominal budget103%, no renormalization. AUM and legacy DAILY beta unchanged.',
            '- CRO restored alongside re_c03, not CRP: VLO/MPC/PSX/PBF=30/20/20/20%, basket total90%, half-balance, SPY-only. Idle basket capacity is preserved. re_c03 retains SPY+XLE hedging.',
            '- Chemical re-enabled by operator: DOW/LYB/WLK/CE 30/30/10/30%, CL carry entry, L and PP own-vol exits, hold2, SPY+XLE. Current flat signal is not a permanent pause; future signals may open positions. See docs/cl_chemical_lp_2026-11-04.md.',
        ]
    if pd.Timestamp('2026-11-06') <= day < pd.Timestamp('2026-11-09'):
        lines += [
            '- CURRENT CL from 2026-11-06: shipping20->10% operator risk reduction; chemical20/refiner3/refiner_slow8/services20/bwt2/CRO20/re_c03 10% unchanged. Nominal budget93%, no normalization; released10 percentage points stay cash. No automatic shipping restoration.',
            '- Operator corrected notebook: chemical retains hold2 (NOT direct signal, NOT hold21). Slow HO m1 gate reads carry_data_2 from Nov06 to match notebook default loader, with strict lookback/arrival validation, no canonical fallback. L/PP exits and baskets unchanged. CRO remains half-balance SPY-only; re_c03 SPY+XLE. AUM and legacy DAILY beta unchanged. See docs/cl_shipping_reduction_2026-11-06.md.',
        ]
    if day >= pd.Timestamp('2026-11-09'):
        lines += [
            '- CURRENT FINAL CL from 2026-11-09: operator chemical20->15%, services20->10%, shipping STAYS10% (initial20% package superseded before execution); refiner3/slow8/bwt2/CRO20/re_c03 10% unchanged. Nominal budget78%, no normalization. AUM and legacy DAILY beta unchanged.',
            '- Rules unchanged: chemical hold2 and L/PP exits; slow HO m1 gate carry_data_2; CRO half-balance SPY-only, re_c03 SPY+XLE. Track allocation migration separately from signal changes. See docs/cl_reweight_2026-11-09.md.',
        ]
    if cro_enabled and pd.Timestamp('2026-10-06') <= day < pd.Timestamp('2026-11-02'):
        lines += [
            '- CRO (crack refiner-only) added effective 2026-10-06: 10% allocation from unused CL capacity. CL AUM remains $15,000; existing sleeve weights are NOT reduced or renormalized.',
            '- CRO stocks: VLO/MPC/PSX = 30/40/30%; crack_03; signal lookback 30 sessions; volatility lookback 30 (minimum 20); no signal smoothing; balance=0.5 (maximum CRO stock gross 5% of CL AUM).',
            '- CRO explicit hedge is SPY ONLY, not XLE. Preserve component hedge ownership when PSX overlaps existing sleeves; net single-name cap and execution constraints still apply.',
            '- This addition is refiner-only CRO, NOT the refiner-producer CRP, refiner-VLCC CRV, or refiner-chemical CRC research strategies.',
        ]
        if cro_active is not None:
            lines.append(f"- CRO stock target state for this package: {'active' if cro_active else 'flat'}. Flat CRO must not create reallocation trades under identical inputs.")
    if day >= pd.Timestamp('2026-09-17'):
        lines.append('- Existing live suspensions remain: CL fuel and metals; standalone Metals sco_specialty_alloys. Released weights stay in cash.')
    lines += [
        '- Execute only the combined account orders, not standalone strategy order files. Hedge netting uses post-stock executable ETF targets when available, not stale continuous rounded ETF targets.',
        '- Target generation is not evidence of OOS validity or guaranteed live performance; review borrow, earnings/corporate events and confirmed fills.',
    ]
    return '\n'.join(lines)
