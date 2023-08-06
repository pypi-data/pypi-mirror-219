# exchanges.py

from cryptofeed.exchanges import EXCHANGE_MAP

__all__ = [
    "EXCHANGES",
    "EXCHANGE_NAMES"
]

EXCHANGES = {
    name.lower(): exchange
    for name, exchange in EXCHANGE_MAP.items()
}
EXCHANGE_NAMES = list(EXCHANGES.keys())