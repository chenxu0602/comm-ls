"""Contract history moved under raw_data; live/policy paths remain at comm root."""
from pathlib import Path

# Keys are Bloomberg/history symbols; values are live CSV exchange symbols.
LIVE_SYMBOL_BY_HISTORY = {
    'DCR':'ETH', 'QSO':'SOL',
    'RBT':'RB', 'PXL':'PX', 'ZSY':'SA', 'SHY':'SH', 'ZME':'MA', 'PT':'TA',
    'IOE':'I', 'KEE':'JM', 'CKC':'J', 'POL':'L', 'PYL':'PP',
    'PVC':'V', 'SYR':'EB', 'LGE':'EG',
}


def live_symbol(symbol: str) -> str:
    symbol = symbol.upper().strip()
    return LIVE_SYMBOL_BY_HISTORY.get(symbol,symbol)


def commodity_root_from_symbol(symbol_dir: Path) -> Path:
    symbol_dir = Path(symbol_dir)
    parent = symbol_dir.parent
    return parent.parent if parent.name == 'raw_data' else parent


def history_root(commodity_dir: Path) -> Path:
    root = Path(commodity_dir)
    if root.name == 'raw_data':
        return root
    return root/'raw_data' if (root/'raw_data').is_dir() else root


def history_symbol_dir(symbol_dir: Path) -> Path:
    symbol_dir = Path(symbol_dir)
    return history_root(commodity_root_from_symbol(symbol_dir))/symbol_dir.name
