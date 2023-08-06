# base.py

import datetime as dt
import time
from typing import (
    Optional, Union, Dict, Iterable, Any, List, Callable
)

import pandas as pd

from represent import Modifiers, represent

from multithreading import Caller, multi_threaded_call

from cryptofeed.defines import L2_BOOK

from crypto_screening.process import find_string_value
from crypto_screening.dataset import save_dataset, load_dataset, DATE_TIME
from crypto_screening.symbols import Separator
from crypto_screening.validate import validate_exchange, validate_symbol
from crypto_screening.market.foundation.state import WaitingState
from crypto_screening.market.foundation.waiting import (
    base_wait_for_initialization, base_wait_for_dynamic_initialization,
    base_wait_for_dynamic_update, base_wait_for_update
)
from crypto_screening.market.foundation.data import DataCollector

__all__ = [
    "BaseScreener",
    "BaseMultiScreener",
    "structure_screeners_datasets",
    "structure_screener_datasets",
    "create_market_dataframe",
    "MarketRecorder",
    "validate_market"
]

class BaseScreener(DataCollector):
    """
    A class to represent an asset price screener.

    Using this class, you can create a screener object to
    screen the market ask and bid data for a specific asset in
    a specific exchange at real time.

    Parameters:

    - symbol:
        The symbol of an asset to screen.

    - exchange:
        The name of the exchange platform to screen data from.

    - location:
        The saving location for the saved data of the screener.

    - cancel:
        The time to cancel screening process after no new data is fetched.

    - delay:
        The delay to wait between each data fetching.

    - market:
        The dataset of the market data.
    """

    __modifiers__ = Modifiers(**DataCollector.__modifiers__)
    __modifiers__.hidden.append("market")

    __slots__ = "symbol", "exchange", "market"

    def __init__(
            self,
            symbol: str,
            exchange: str,
            location: Optional[str] = None,
            cancel: Optional[Union[float, dt.timedelta]] = None,
            delay: Optional[Union[float, dt.timedelta]] = None,
            market: Optional[pd.DataFrame] = None,
    ) -> None:
        """
        Defines the class attributes.

        :param symbol: The symbol of the asset.
        :param exchange: The exchange to get source data from.
        :param location: The saving location for the data.
        :param delay: The delay for the process.
        :param cancel: The cancel time for the loops.
        :param market: The data for the market.
        """

        super().__init__(location=location, cancel=cancel, delay=delay)

        self.exchange = self.validate_exchange(exchange=exchange)
        self.symbol = self.validate_symbol(
            exchange=self.exchange, symbol=symbol
        )

        if market is None:
            market = create_market_dataframe()
        # end if

        self.market = market
    # end __init__

    def wait_for_initialization(
            self,
            stop: Optional[Union[bool, int]] = False,
            delay: Optional[Union[float, dt.timedelta]] = None,
            cancel: Optional[Union[float, dt.timedelta, dt.datetime]] = None
    ) -> WaitingState:
        """
        Waits for all the create_screeners to update.

        :param delay: The delay for the waiting.
        :param stop: The value to stop the screener objects.
        :param cancel: The time to cancel the waiting.

        :returns: The total delay.
        """

        return base_wait_for_initialization(
            self, stop=stop, delay=delay, cancel=cancel
        )
    # end base_wait_for_initialization

    def wait_for_update(
            self,
            stop: Optional[Union[bool, int]] = False,
            delay: Optional[Union[float, dt.timedelta]] = None,
            cancel: Optional[Union[float, dt.timedelta, dt.datetime]] = None
    ) -> WaitingState:
        """
        Waits for all the create_screeners to update.

        :param delay: The delay for the waiting.
        :param stop: The value to stop the screener objects.
        :param cancel: The time to cancel the waiting.

        :returns: The total delay.
        """

        return base_wait_for_update(
            self, stop=stop, delay=delay, cancel=cancel
        )
    # end base_wait_for_update

    @staticmethod
    def validate_exchange(exchange: str) -> str:
        """
        Validates the symbol value.

        :param exchange: The exchange name.

        :return: The validates symbol.
        """

        return validate_exchange(exchange=exchange)
    # end validate_exchange

    @staticmethod
    def validate_symbol(exchange: str, symbol: Any) -> str:
        """
        Validates the symbol value.

        :param exchange: The exchange name.
        :param symbol: The name of the symbol.

        :return: The validates symbol.
        """

        return validate_symbol(exchange=exchange, symbol=symbol)
    # end validate_symbol

    def dataset_path(self, location: Optional[str] = None) -> str:
        """
        Creates the path to the saving file for the screener object.

        :param location: The saving location of the dataset.

        :return: The saving path for the dataset.
        """

        location = location or self.location

        if location is None:
            location = "."
        # end if

        return (
            f"{location}/"
            f"{self.exchange.lower()}/"
            f"{self.symbol.replace(Separator.value, '-')}.csv"
        )
    # end dataset_path

    def save_dataset(self, location: Optional[str] = None) -> None:
        """
        Saves the data of the screener.

        :param location: The saving location of the dataset.
        """

        if len(self.market) == 0:
            return
        # end if

        save_dataset(
            dataset=self.market,
            path=self.dataset_path(location=location)
        )
    # end save_dataset

    def load_dataset(self, location: Optional[str] = None) -> None:
        """
        Saves the data of the screener.

        :param location: The saving location of the dataset.
        """

        data = load_dataset(path=self.dataset_path(location=location))

        for index, data in zip(data.index[:], data.loc[:]):
            self.market.loc[index] = data
        # end for
    # end load_dataset

    def saving_loop(self) -> None:
        """Runs the process of the price screening."""

        self._saving = True

        delay = self.delay

        if isinstance(self.delay, dt.timedelta):
            delay = delay.total_seconds()
        # end if

        while self.saving:
            start = time.time()

            self.save_dataset()

            end = time.time()

            time.sleep(max([delay - (end - start), 1]))
        # end while
    # end saving_loop
# end BaseScreener

def create_market_dataframe(columns: Optional[Iterable[str]] = None) -> pd.DataFrame:
    """
    Creates a dataframe for the order book data.

    :param columns: The dataset columns.

    :return: The dataframe.
    """

    market = pd.DataFrame(
        {column: [] for column in columns or []}, index=[]
    )
    market.index.name = DATE_TIME

    return market
# end create_market_dataframe

RecorderParameters = Dict[str, Union[Iterable[str], Dict[str, Callable]]]

Market = Dict[str, Dict[str, Any]]

def validate_market(data: Any) -> Market:
    """
    Validates the data.

    :param data: The data to validate.

    :return: The valid data.
    """

    try:
        if not isinstance(data, dict):
            raise ValueError
        # end if

        for exchange, values in data.items():
            if not (
                isinstance(exchange, str) and
                (
                    isinstance(values, dict) and
                    all(
                        isinstance(symbol, str)
                        for symbol, _ in values.items()
                    )
                )
            ):
                raise ValueError
            # end if
        # end for

    except (TypeError, ValueError):
        raise ValueError(
            f"Data must be of type {Market}, not: {data}."
        )
    # end try

    return data
# end validate_market

@represent
class MarketRecorder:
    """
    A class to represent a crypto data feed recorder.
    This object passes the record method to the handler object to record
    the data fetched by the handler.

    Parameters:

    - market:
        The market structure of the data to store the fetched data in.
        This structure is a dictionary with exchange names as keys
        and dictionaries as values, where their keys are symbols,
        and their values are the dataframes to record the data.

    >>> from crypto_screening.market.screeners.base import MarketRecorder
    >>>
    >>> market = {'binance': ['BTC/USDT'], 'bittrex': ['ETH/USDT']}
    >>>
    >>> recorder = MarketRecorder(data=market)

    """

    __modifiers__ = Modifiers()
    __modifiers__.hidden.append("market")

    __slots__ = "market",

    def __init__(self, market: Market) -> None:
        """
        Defines the class attributes.

        :param market: The object to fill with the crypto feed record.
        """

        self.market = self.validate_market(data=market)
    # end __init__

    def parameters(self) -> RecorderParameters:
        """
        Returns the order book parameters.

        :return: The order book parameters.
        """

        return dict(
            channels=[L2_BOOK],
            callbacks={L2_BOOK: self.record},
            max_depth=1
        )
    # end parameters

    @staticmethod
    def validate_market(data: Any) -> Market:
        """
        Validates the data.

        :param data: The data to validate.

        :return: The valid data.
        """

        return validate_market(data=data)
    # end validate_market

    def structure(self) -> Dict[str, List[str]]:
        """
        Returns the structure of the market data.

        :return: The structure of the market.
        """

        return {
            exchange: list(symbols.keys())
            for exchange, symbols in self.market.items()
        }
    # end structure

    def data(self, exchange: str, symbol: str) -> Any:
        """
        Returns the market data of the symbol from the exchange.

        :param exchange: The source name of the exchange.
        :param symbol: The symbol of the pair.

        :return: The dataset of the spread data.
        """

        exchange = find_string_value(
            value=exchange, values=self.market.keys()
        )

        validate_exchange(
            exchange=exchange,
            exchanges=self.market.keys(),
            provider=self
        )

        validate_symbol(
            symbol=symbol,
            exchange=exchange,
            exchanges=self.market.keys(),
            symbols=self.market[exchange],
            provider=self
        )

        return self.market[exchange][symbol]
    # end data

    def in_market(self, exchange: str, symbol: str) -> bool:
        """
        Returns the market data of the symbol from the exchange.

        :param exchange: The source name of the exchange.
        :param symbol: The symbol of the pair.

        :return: The dataset of the spread data.
        """

        try:
            self.data(exchange=exchange, symbol=symbol)

            return True

        except ValueError:
            return False
        # end try
    # end in_market
# end MarketRecorder

class BaseMultiScreener(DataCollector):
    """
    A class to represent an asset price screener.

    Using this class, you can create a screener object to
    screen the market ask and bid data for a specific asset in
    a specific exchange at real time.

    Parameters:

    - location:
        The saving location for the saved data of the screener.

    - cancel:
        The time to cancel screening process after no new data is fetched.

    - delay:
        The delay to wait between each data fetching.
    """

    __modifiers__ = Modifiers(**DataCollector.__modifiers__)
    __modifiers__.hidden.extend(["screeners", 'recorder'])

    screeners: List[BaseScreener]

    __slots__ = 'recorder', 'screeners'

    def __init__(
            self,
            recorder: MarketRecorder,
            screeners: Optional[Iterable[BaseScreener]] = None,
            location: Optional[str] = None,
            cancel: Optional[Union[float, dt.timedelta]] = None,
            delay: Optional[Union[float, dt.timedelta]] = None
    ) -> None:
        """
        Defines the class attributes.

        :param location: The saving location for the data.
        :param delay: The delay for the process.
        :param cancel: The cancel time for the loops.
        """

        super().__init__(location=location, cancel=cancel, delay=delay)

        self.screeners = list(screeners or [])

        self.recorder = recorder
    # end __init__

    @property
    def market(self) -> Dict[str, Dict[str, pd.DataFrame]]:
        """
        Returns the market to hold the recorder data.

        :return: The market object.
        """

        return self.recorder.market
    # end market

    def wait_for_initialization(
            self,
            stop: Optional[Union[bool, int]] = False,
            delay: Optional[Union[float, dt.timedelta]] = None,
            cancel: Optional[Union[float, dt.timedelta, dt.datetime]] = None
    ) -> WaitingState:
        """
        Waits for all the create_screeners to update.

        :param delay: The delay for the waiting.
        :param stop: The value to stop the screener objects.
        :param cancel: The time to cancel the waiting.

        :returns: The total delay.
        """

        return base_wait_for_dynamic_initialization(
            self.screeners, stop=stop, delay=delay, cancel=cancel
        )
    # end base_wait_for_initialization

    def wait_for_update(
            self,
            stop: Optional[Union[bool, int]] = False,
            delay: Optional[Union[float, dt.timedelta]] = None,
            cancel: Optional[Union[float, dt.timedelta, dt.datetime]] = None
    ) -> WaitingState:
        """
        Waits for all the create_screeners to update.

        :param delay: The delay for the waiting.
        :param stop: The value to stop the screener objects.
        :param cancel: The time to cancel the waiting.

        :returns: The total delay.
        """

        return base_wait_for_dynamic_update(
            self.screeners, stop=stop, delay=delay, cancel=cancel
        )
    # end base_wait_for_update

    def connect_screeners(self) -> None:
        """Connects the screeners to the recording object."""

        for screener in self.screeners:
            screener.market = self.recorder.data(
                exchange=screener.exchange, symbol=screener.symbol
            )
        # end for
    # end connect_screeners

    def in_market(self, exchange: str, symbol: str) -> bool:
        """
        Returns the market data of the symbol from the exchange.

        :param exchange: The source name of the exchange.
        :param symbol: The symbol of the pair.

        :return: The dataset of the spread data.
        """

        return self.recorder.in_market(exchange=exchange, symbol=symbol)
    # end in_market

    def save_datasets(self, location: Optional[str] = None) -> None:
        """
        Runs the data handling loop.

        :param location: The saving location.
        """

        callers = []

        for screener in self.screeners:
            location = location or screener.location or self.location

            callers.append(
                Caller(
                    target=screener.save_dataset,
                    kwargs=dict(location=location)
                )
            )
        # end for

        multi_threaded_call(callers=callers)
    # end save_datasets

    def load_datasets(self, location: Optional[str] = None) -> None:
        """
        Runs the data handling loop.

        :param location: The saving location.
        """

        callers = []

        for screener in self.screeners:
            location = location or screener.location or self.location

            callers.append(
                Caller(
                    target=screener.load_dataset,
                    kwargs=dict(location=location)
                )
            )
        # end for

        multi_threaded_call(callers=callers)
    # end load_datasets
# end BaseScreener

def structure_screeners_datasets(
        screeners: Iterable[BaseScreener]
) -> Dict[str, Dict[str, List[pd.DataFrame]]]:
    """
    Structures the screener objects by exchanges and symbols

    :param screeners: The screeners to structure.

    :return: The structure of the screeners.
    """

    structure = {}

    for screener in screeners:
        (
            structure.
            setdefault(screener.exchange, {}).
            setdefault(screener.symbol, [])
        ).append(screener.market)
    # end for

    return structure
# end structure_screeners_datasets

def structure_screener_datasets(
        screeners: Iterable[BaseScreener]
) -> Dict[str, Dict[str, pd.DataFrame]]:
    """
    Structures the screener objects by exchanges and symbols

    :param screeners: The screeners to structure.

    :return: The structure of the screeners.
    """

    structure = {}

    for screener in screeners:
        (
            structure.
            setdefault(screener.exchange, {}).
            setdefault(screener.symbol, screener.market)
        )
    # end for

    return structure
# end structure_screener_datasets