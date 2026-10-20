"""Effective-dated strategy handoff text for generated execution packages."""
import pandas as pd


def strategy_notes(target_date, *, cro_enabled=False, agri_aum=None,
                   cro_active=None, agri_active=None):
    day = pd.Timestamp(target_date)
    lines = ['## Strategy changes and allocation notes', '']
    if agri_aum is not None and day >= pd.Timestamp('2026-10-02'):
        lines += [
            f'- Agriculture v4.3 joined the main account effective 2026-10-02: ${agri_aum:,.0f} allocated AUM. Idle allocation remains cash and still counts in account AUM.',
            '- Agriculture uses component-specific hedges: crush_vol/crush_vol2/adm_bg2 use SPY + MOO; adm_bg/adm_tsn/bg_tsn use SPY only. Keep its virtual book separate.',
        ]
        if agri_active is not None:
            lines.append(f"- Agriculture stock target state for this package: {'active' if agri_active else 'flat'}. This is not a permanent suspension.")
    if cro_enabled and day >= pd.Timestamp('2026-10-06'):
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
