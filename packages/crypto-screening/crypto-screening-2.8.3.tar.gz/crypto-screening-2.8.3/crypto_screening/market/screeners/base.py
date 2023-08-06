# base.py

import datetime as dt
import time
from typing import (
    Optional, Union, Dict, Iterable, Any, List
)

import pandas as pd

from represent import Modifiers

from multithreading import Caller, multi_threaded_call

from crypto_screening.dataset import save_dataset, load_dataset
from crypto_screening.symbols import Separator
from crypto_screening.validate import validate_exchange, validate_symbol
from crypto_screening.market.foundation.state import WaitingState
from crypto_screening.market.foundation.waiting import (
    base_wait_for_initialization, base_wait_for_dynamic_initialization,
    base_wait_for_dynamic_update, base_wait_for_update
)
from crypto_screening.market.foundation.data import DataCollector
from crypto_screening.market.screeners.recorder import (
    MarketRecorder, create_market_dataframe
)

__all__ = [
    "BaseScreener",
    "BaseMultiScreener",
    "structure_screeners_datasets",
    "structure_screener_datasets"
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
            screeners: Optional[Iterable[BaseScreener]] = None,
            recorder: Optional[MarketRecorder] = None,
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

        self.recorder = recorder or MarketRecorder(
            market=structure_screener_datasets(screeners=self.screeners)
        )
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