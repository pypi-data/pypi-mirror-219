# recorder.py

import warnings
import threading
import time
import datetime as dt
from typing import (
    Optional, Dict, Any, List, Iterable, Type, Union
)
from functools import partial
import asyncio

import pandas as pd

from represent import Modifiers, represent

from cryptofeed import FeedHandler
from cryptofeed.feed import Feed

from crypto_screening.validate import validate_exchange, validate_symbol
from crypto_screening.process import find_string_value
from crypto_screening.exchanges import EXCHANGES, EXCHANGE_NAMES
from crypto_screening.symbols import Separator
from crypto_screening.market.screeners.base import (
    BaseMultiScreener, BaseScreener
)

__all__ = [
    "MarketHandler",
    "ExchangeFeed",
    "FEED_GROUP_SIZE",
    "add_feeds",
    "MarketScreener",
    "structure_screeners_datasets",
    "structure_screener_datasets",
    "MarketRecorder",
    "validate_market"
]

class MarketHandler(FeedHandler):
    """A class to handle the market data feed."""

    def __init__(self) -> None:
        """Defines the class attributes."""

        super().__init__(
            config={'uvloop': False, 'log': {'disabled': True}}
        )
    # end __init__
# end MarketHandler

class ExchangeFeed(Feed):
    """A class to represent an exchange feed object."""

    handler: Optional[FeedHandler] = None

    running: bool = False

    def stop(self) -> None:
        """Stops the process."""

        self.running = False

        Feed.stop(self)
    # end stop

    def start(self, loop: asyncio.AbstractEventLoop) -> None:
        """
        Create tasks for exchange interfaces and backends.

        :param loop: The event loop for the process.
        """

        self.running = True

        Feed.start(self, loop=loop)
    # end start
# end ExchangeFeed


FEED_GROUP_SIZE = 20

def add_feeds(
        handler: FeedHandler,
        data: Dict[str, Iterable[str]],
        fixed: Optional[bool] = False,
        amount: Optional[int] = FEED_GROUP_SIZE,
        separator: Optional[str] = None,
        parameters: Optional[Union[Dict[str, Dict[str, Any]], Dict[str, Any]]] = None
) -> None:
    """
    Adds the symbols to the handler for each exchange.

    :param handler: The handler object.
    :param data: The data of the exchanges and symbols to add.
    :param parameters: The parameters for the exchanges.
    :param fixed: The value for fixed parameters to all exchanges.
    :param separator: The separator of the assets.
    :param amount: The maximum amount of symbols for each feed.
    """

    base_parameters = None

    if not fixed:
        parameters = parameters or {}

    else:
        base_parameters = parameters or {}
        parameters = {}
    # end if

    if separator is None:
        separator = Separator.value
    # end if

    for exchange, symbols in data.items():
        exchange = find_string_value(value=exchange, values=EXCHANGE_NAMES)

        symbols = [
            symbol.replace(separator, '-')
            for symbol in symbols
        ]

        if fixed:
            parameters.setdefault(exchange, base_parameters)
        # end if

        EXCHANGES[exchange]: Type[ExchangeFeed]

        packets = []

        for i in range(0, int(len(symbols) / amount) + len(symbols) % amount, amount):
            packets.append(symbols[i:])
        # end for

        for symbols_packet in packets:
            feed = EXCHANGES[exchange](
                symbols=symbols_packet,
                **(
                    parameters[exchange]
                    if (
                        (exchange in parameters) and
                        isinstance(parameters[exchange], dict) and
                        all(isinstance(key, str) for key in parameters)

                    ) else {}
                )
            )

            feed.start = partial(ExchangeFeed.start, feed)
            feed.stop = partial(ExchangeFeed.stop, feed)
            feed.handler = handler
            feed.running = False

            handler.add_feed(feed)
        # end for
    # end for
# end add_feeds

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

    >>> from crypto_screening.market.screeners.recorder import MarketRecorder
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

    @staticmethod
    def validate_market(data: Any) -> Market:
        """
        Validates the data.

        :param data: The data to validate.

        :return: The valid data.
        """

        return validate_market(data=data)
    # end validate_market

    def parameters(self) -> Dict[str, Any]:
        """
        Returns the order book parameters.

        :return: The order book parameters.
        """

        raise NotImplemented
    # end parameters

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

class MarketScreener(BaseMultiScreener):
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

    - handler:
        The handler object to handle the data feed.

    - recorder:
        The recorder object to record the data of the market from the feed.
    """

    __modifiers__ = Modifiers(**BaseMultiScreener.__modifiers__)
    __modifiers__.excluded.extend(
        ['_run_parameters', '_feeds_parameters', 'handler']
    )

    __slots__ = (
        "handler", 'amount', "loop", "limited", "_feeds_parameters",
        "_run_parameters", 'refresh'
    )

    screeners: List[BaseScreener]
    recorder: MarketRecorder

    DELAY = 5
    AMOUNT = FEED_GROUP_SIZE

    REFRESH = dt.timedelta(minutes=5)

    def __init__(
            self,
            screeners: Optional[Iterable[BaseScreener]] = None,
            location: Optional[str] = None,
            cancel: Optional[Union[float, dt.timedelta]] = None,
            delay: Optional[Union[float, dt.timedelta]] = None,
            refresh: Optional[Union[float, dt.timedelta, bool]] = None,
            limited: Optional[bool] = None,
            handler: Optional[FeedHandler] = None,
            amount: Optional[int] = None,
            recorder: Optional[MarketRecorder] = None
    ) -> None:
        """
        Creates the class attributes.

        :param location: The saving location for the data.
        :param delay: The delay for the process.
        :param cancel: The cancel time for the loops.
        :param limited: The value to limit the screeners to active only.
        :param refresh: The refresh time for rerunning.
        :param handler: The handler object for the market data.
        :param amount: The maximum amount of symbols for each feed.
        :param recorder: The recorder object for recording the data.
        """

        super().__init__(
            location=location, cancel=cancel,
            delay=delay, screeners=screeners
        )

        if refresh is True:
            refresh = self.REFRESH
        # end if

        self.recorder = recorder
        self.handler = handler or MarketHandler()
        self.limited = limited or False
        self.amount = amount or self.AMOUNT
        self.refresh = refresh

        self.loop: Optional[asyncio.AbstractEventLoop] = None

        self._feeds_parameters: Optional[Dict[str, Any]] = None
        self._run_parameters: Optional[Dict[str, Any]] = None
    # end __init__

    def structure(self) -> Dict[str, List[str]]:
        """
        Returns the structure of the market data.

        :return: The structure of the market.
        """

        return self.recorder.structure()
    # end structure

    def add_feeds(
            self,
            data: Dict[str, Iterable[str]],
            fixed: Optional[bool] = True,
            separator: Optional[str] = None,
            amount: Optional[int] = None,
            parameters: Optional[Union[Dict[str, Dict[str, Any]], Dict[str, Any]]] = None
    ) -> None:
        """
        Adds the symbols to the handler for each exchange.

        :param data: The data of the exchanges and symbols to add.
        :param parameters: The parameters for the exchanges.
        :param fixed: The value for fixed parameters to all exchanges.
        :param amount: The maximum amount of symbols for each feed.
        :param separator: The separator of the assets.
        """

        self._feeds_parameters = dict(
            data=data, fixed=fixed, separator=separator,
            parameters=parameters
        )

        feed_params = self.recorder.parameters()
        feed_params.update(parameters or {})

        add_feeds(
            self.handler, data=data, fixed=fixed, separator=separator,
            parameters=feed_params, amount=amount or self.amount
        )
    # end add_feeds

    def refresh_feeds(self) -> None:
        """Refreshes the feed objects."""

        if self._feeds_parameters is None:
            warnings.warn(
                "Cannot refresh feeds as there was "
                "no feeds initialization to repeat."
            )

            return
        # end if

        self.handler.feeds.clear()

        self.add_feeds(**self._feeds_parameters)
    # end refresh

    def rerun(self) -> None:
        """Refreshes the process."""

        if self._run_parameters is None:
            warnings.warn(
                "Cannot rerun as there was "
                "no initial process to repeat."
            )

            return
        # end if

        self.terminate()
        self.refresh_feeds()
        self.run(**self._run_parameters)
    # end rerun

    def orderbook(self, exchange: str, symbol: str) -> pd.DataFrame:
        """
        Returns the market data of the symbol from the exchange.

        :param exchange: The source name of the exchange.
        :param symbol: The symbol of the pair.

        :return: The dataset of the spread data.
        """

        return self.recorder.orderbook(exchange=exchange, symbol=symbol)
    # end orderbook

    def screening_loop(
            self,
            start: Optional[bool] = True,
            loop: Optional[asyncio.AbstractEventLoop] = None
    ) -> None:
        """
        Runs the process of the price screening.

        :param start: The value to start the loop.
        :param loop: The event loop.
        """

        if loop is None:
            loop = asyncio.new_event_loop()
        # end if

        self.loop = loop

        asyncio.set_event_loop(loop)

        self._screening = True

        for screener in self.screeners:
            screener._screening = True
        # end for

        self.handler.run(
            start_loop=start and (not loop.is_running()),
            install_signal_handlers=False
        )
    # end screening_loop

    def saving_loop(self) -> None:
        """Runs the process of the price screening."""

        for screener in self.screeners:
            screener._saving_process = threading.Thread(
                target=screener.saving_loop
            )
            screener._saving_process.start()
        # end for
    # end saving_loop

    def update_loop(self) -> None:
        """Updates the state of the screeners."""

        self._updating = True

        refresh = self.refresh

        if isinstance(refresh, dt.timedelta):
            refresh = refresh.total_seconds()
        # end if

        start = time.time()

        while self.updating:
            s = time.time()

            if self.screening:
                self.update()

                current = time.time()

                if refresh and ((current - start) >= refresh):
                    self.rerun()

                    start = current
                # end if
            # end if

            time.sleep(max([self.delay - (time.time() - s), 0]))
        # end while
    # end update_loop

    def update(self) -> None:
        """Updates the state of the screeners."""

        for screener in self.screeners:
            for feed in self.handler.feeds:
                feed: ExchangeFeed

                if (
                    self.limited and
                    (screener.exchange.lower() == feed.id.lower()) and
                    (not feed.running)
                ):
                    screener.stop()
                # end if
            # end for
        # end for
    # end update

    def stop(self) -> None:
        """Stops the data handling loop."""

        super().stop()

        self.loop: asyncio.AbstractEventLoop

        async def stop() -> None:
            """Stops the handler."""

            self.handler.stop(self.loop)
            self.handler.close(self.loop)
        # end stop

        self.loop.create_task(stop())

        for task in asyncio.all_tasks(self.loop):
            task.cancel()
        # end for

        self.loop = None

        self.handler.running = False
    # end stop

    def start_screening(
            self,
            start: Optional[bool] = True,
            loop: Optional[asyncio.AbstractEventLoop] = None
    ) -> None:
        """
        Starts the screening process.

        :param start: The value to start the loop.
        :param loop: The event loop.
        """

        if self.screening:
            warnings.warn(f"Timeout process of {self} is already running.")

            return
        # end if

        self._screening_process = threading.Thread(
            target=lambda: self.screening_loop(loop=loop, start=start)
        )

        self._screening_process.start()
    # end start_screening

    def run(
            self,
            save: Optional[bool] = True,
            block: Optional[bool] = False,
            update: Optional[bool] = True,
            screen: Optional[bool] = True,
            loop: Optional[asyncio.AbstractEventLoop] = None,
            wait: Optional[Union[bool, float, dt.timedelta, dt.datetime]] = False,
            timeout: Optional[Union[float, dt.timedelta, dt.datetime]] = None,
    ) -> None:
        """
        Runs the program.

        :param save: The value to save the data.
        :param wait: The value to wait after starting to run the process.
        :param block: The value to block the execution.
        :param timeout: The valur to add a start_timeout to the process.
        :param update: The value to update the screeners.
        :param screen: The value to start the loop.
        :param loop: The event loop.

        :return: The start_timeout process.
        """

        self._run_parameters = dict(
            save=save, block=block, update=update, screen=screen,
            loop=loop, wait=wait, timeout=timeout
        )

        if not block:
            self.start_screening(loop=loop, start=screen)
        # end if

        super().run(
            screen=False, block=False, wait=wait,
            timeout=timeout, update=update, save=save
        )

        if block:
            self.screening_loop(loop=loop, start=screen)
        # end if
    # end run
# end MarketScreener

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