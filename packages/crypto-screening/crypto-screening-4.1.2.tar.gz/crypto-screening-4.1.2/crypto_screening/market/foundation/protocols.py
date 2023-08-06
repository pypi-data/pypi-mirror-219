# protocols.py

import datetime as dt
from typing import Protocol, Dict, List, Union

import pandas as pd

__all__ = [
    "BaseScreenerProtocol",
    "BaseMultiScreenerProtocol",
    "DataCollectorProtocol"
]

class DataCollectorProtocol(Protocol):
    """A class for the base data collector protocol."""

    location: str

    delay: Union[float, dt.timedelta]
    cancel: Union[float, dt.timedelta]
# end DataCollectorProtocol

class BaseScreenerProtocol(DataCollectorProtocol):
    """A class for the base screener protocol."""

    symbol: str
    exchange: str

    market: pd.DataFrame
# end BaseScreenerProtocol

class BaseMultiScreenerProtocol(DataCollectorProtocol):
    """A class for the base multi-screener protocol."""

    market: Dict[str, Dict[str, pd.DataFrame]]
    screeners: List[BaseScreenerProtocol]
# end BaseMultiScreenerProtocol