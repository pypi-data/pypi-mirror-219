# combined.py

import datetime as dt
from typing import (
    Dict, Optional, Iterable, Any,
    Union, List, Callable, Type
)

import pandas as pd

from cryptofeed import FeedHandler

from crypto_screening.market.screeners.orderbook import (
    orderbook_market_screener, OrderbookScreener,
    OrderbookMarketRecorder
)
from crypto_screening.market.screeners.ohlcv import (
    ohlcv_market_screener, OHLCVScreener,
    OHLCVMarketRecorder
)
from crypto_screening.market.screeners.trades import (
    trades_market_screener, TradesScreener,
    TradesMarketRecorder
)
from crypto_screening.market.screeners.orders import (
    orders_market_screener, OrdersScreener,
    OrdersMarketRecorder
)
from crypto_screening.market.screeners.recorder import MarketScreener

__all__ = [
    "CombinedMarketRecorder",
    "CombinedMarketScreener",
    "combined_market_screener",
    "CATEGORIES",
    "RECORDERS",
    "Category",
    "OrderbookCategory",
    "TradesCategory",
    "OrdersCategory",
    "OHLCVCategory"
]

Market = Dict[str, Dict[str, pd.DataFrame]]

RecorderParameters = Dict[str, Union[Iterable[str], Dict[str, Callable]]]

class Category:
    """A class to represent a category."""

    __slots__ = ()
# end Category

class OrderbookCategory(Category):
    """A class to represent a category."""

    __slots__ = ()
# end OrderbookCategory

class OrdersCategory(Category):
    """A class to represent a category."""

    __slots__ = ()
# end OrdersCategory

class TradesCategory(Category):
    """A class to represent a category."""

    __slots__ = ()
# end TradesCategory

class OHLCVCategory(Category):
    """A class to represent a category."""

    __slots__ = ()
# end OHLCVCategory

RECORDERS = (
    OHLCVMarketRecorder,
    TradesMarketRecorder,
    OrderbookMarketRecorder,
    OrdersMarketRecorder
)
CATEGORIES = (
    OHLCVCategory,
    TradesCategory,
    OrdersCategory,
    OrderbookCategory
)

Recorder = Union[*RECORDERS]
CategoryBase = Union[*CATEGORIES]

MarketRecorders = Union[
    Iterable[Type[CategoryBase]],
    Iterable[Recorder],
    Dict[Type[CategoryBase], Iterable[Recorder]]
]

def gather(recorders: Iterable):
    """
    Gathers the functions to record the data.

    :param recorders: The data recorders.

    :return: The new data recorder function.
    """

    async def record(data: Any, timestamp: float) -> bool:
        """
        Records the data for the screeners.

        :param data: The data to record.
        :param timestamp: The timestamp of the data.

        :return: The boolean flag.
        """

        for recorder in recorders:
            await recorder(data, timestamp)
        # end for

        return True
    # end record

    return record
# end gather

class CombinedMarketRecorder:
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

    >>> from crypto_screening.market.screeners import orderbook_market_recorder
    >>>
    >>> market = {'binance': ['BTC/USDT'], 'bittrex': ['ETH/USDT']}
    >>>
    >>> recorder = orderbook_market_recorder(data=market)
    """

    def __init__(self, recorders: Iterable[Recorder]) -> None:
        """
        Defines the class attributes.

        :param recorders: The categories for the market screener.
        """

        structure: Dict[str, List[str]] = {}

        for recorder in recorders:
            structure.update(recorder.structure())
        # end for

        self.recorders = list(recorders)
        self._structure = structure
    # end __init__

    def structure(self) -> Dict[str, List[str]]:
        """
        Returns the structure of the market data.

        :return: The structure of the market.
        """

        return {
            exchange: list(symbols)
            for exchange, symbols in self._structure.items()
        }
    # end structure

    def parameters(self) -> RecorderParameters:
        """
        Returns the order book parameters.

        :return: The order book parameters.
        """

        channels = []
        callback_recorders = {}

        for recorder in self.recorders:
            channels.extend(recorder.parameters()["channels"])

            for key, value in recorder.parameters()["callbacks"].items():
                (
                    callback_recorders.
                    setdefault(key, []).
                    append(value)
                )
        # end for

        callbacks = {}

        for key, recorders in callback_recorders.items():
            callbacks[key] = gather(recorders)
        # end for

        return dict(
            channels=list(set(channels)),
            callbacks=callbacks,
            max_depth=1
        )
    # end parameters
# end CombinedMarketRecorder

Screener = Union[OrderbookScreener, OHLCVScreener, TradesScreener, OrdersScreener]

class CombinedMarketScreener(MarketScreener):
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

    >>> from crypto_screening.market.screeners import orderbook_market_screener
    >>>
    >>> structure = {'binance': ['BTC/USDT'], 'bittrex': ['ETH/USDT']}
    >>>
    >>> screener = orderbook_market_screener(data=structure)
    >>> screener.run()
    """

    recorder: CombinedMarketRecorder

    def __init__(
            self,
            markets: Iterable[MarketScreener],
            location: Optional[str] = None,
            cancel: Optional[Union[float, dt.timedelta]] = None,
            delay: Optional[Union[float, dt.timedelta]] = None,
            refresh: Optional[Union[float, dt.timedelta, bool]] = None,
            limited: Optional[bool] = None,
            handler: Optional[FeedHandler] = None,
            amount: Optional[int] = None,
            recorder: Optional[CombinedMarketRecorder] = None
    ) -> None:
        """
        Creates the class attributes.

        :param location: The saving location for the data.
        :param markets: The market screeners.
        :param delay: The delay for the process.
        :param cancel: The cancel time for the loops.
        :param limited: The value to limit the screeners to active only.
        :param refresh: The refresh time for rerunning.
        :param handler: The handler object for the market data.
        :param amount: The maximum amount of symbols for each feed.
        :param recorder: The recorder object for recording the data.
        """

        screeners = []

        for market in markets:
            screeners.extend(market.screeners)
        # end for

        super().__init__(
            location=location, cancel=cancel,
            delay=delay, recorder=recorder or CombinedMarketRecorder(
                recorders=[market.recorder for market in markets]
            ),
            screeners=screeners, handler=handler, limited=limited,
            amount=amount, refresh=refresh
        )

        self.markets = list(markets)
        self.screeners = list(screeners)
    # end __init__

    @property
    def orderbook_screeners(self) -> List[OrderbookScreener]:
        """
        Returns a list of all the order-book screeners.

        :return: The order-book screeners.
        """

        return [
            screener for screener in self.screeners
            if isinstance(screener, OrderbookScreener)
        ]
    # end orderbook_screeners

    @property
    def orders_screeners(self) -> List[OrdersScreener]:
        """
        Returns a list of all the order-book screeners.

        :return: The orders screeners.
        """

        return [
            screener for screener in self.screeners
            if isinstance(screener, OrdersScreener)
        ]
    # end orders_screeners

    @property
    def ohlcv_screeners(self) -> List[OHLCVScreener]:
        """
        Returns a list of all the order-book screeners.

        :return: The OHLCV screeners.
        """

        return [
            screener for screener in self.screeners
            if isinstance(screener, OHLCVScreener)
        ]
    # end ohlcv_screeners

    @property
    def trades_screeners(self) -> List[TradesScreener]:
        """
        Returns a list of all the order-book screeners.

        :return: The trades screeners.
        """

        return [
            screener for screener in self.screeners
            if isinstance(screener, TradesScreener)
        ]
    # end trades_screeners

    def connect_screeners(self) -> None:
        """Connects the screeners to the recording object."""

        for market in self.markets:
            market.connect_screeners()
        # end for
    # end connect_screeners
# end CombinedMarketScreener

CATEGORY_RECORDER_CONSTRUCTOR_MATCHES = {
    OrderbookCategory: orderbook_market_screener,
    OHLCVCategory: ohlcv_market_screener,
    TradesCategory: trades_market_screener,
    OrdersCategory: orders_market_screener
}

def combined_market_screener(
        data: Dict[str, Iterable[str]],
        categories: Optional[Type[CategoryBase]] = None,
        location: Optional[str] = None,
        cancel: Optional[Union[float, dt.timedelta]] = None,
        delay: Optional[Union[float, dt.timedelta]] = None,
        limited: Optional[bool] = None,
        handler: Optional[FeedHandler] = None,
        amount: Optional[int] = None,
        refresh: Optional[Union[float, dt.timedelta, bool]] = None,
        recorder: Optional[OrderbookMarketRecorder] = None,
        fixed: Optional[bool] = True,
        separator: Optional[str] = None,
        parameters: Optional[Union[Dict[str, Dict[str, Any]], Dict[str, Any]]] = None
) -> CombinedMarketScreener:
    """
    Creates the market screener object for the data.

    :param data: The market data.
    :param categories: The categories for the markets.
    :param handler: The handler object for the market data.
    :param limited: The value to limit the screeners to active only.
    :param parameters: The parameters for the exchanges.
    :param fixed: The value for fixed parameters to all exchanges.
    :param refresh: The refresh time for rerunning.
    :param amount: The maximum amount of symbols for each feed.
    :param separator: The separator of the assets.
    :param recorder: The recorder object for recording the data.
    :param location: The saving location for the data.
    :param delay: The delay for the process.
    :param cancel: The cancel time for the loops.

    :return: The market screener object.
    """

    if categories is None:
        categories = CATEGORIES
    # end if

    markets = [
        CATEGORY_RECORDER_CONSTRUCTOR_MATCHES[category](
            recorder=recorder, handler=handler, data=data,
            location=location, amount=amount, cancel=cancel,
            delay=delay, limited=limited, refresh=refresh,
            fixed=fixed, separator=separator, parameters=parameters
        )
        for category in set(categories)
    ]

    screener = CombinedMarketScreener(
        markets=markets, recorder=recorder, handler=handler,
        location=location, amount=amount, cancel=cancel,
        delay=delay, limited=limited, refresh=refresh
    )

    screener.add_feeds(
        data=screener.recorder.structure(), fixed=fixed,
        separator=separator, parameters=parameters
    )

    return screener
# end combined_market_screener