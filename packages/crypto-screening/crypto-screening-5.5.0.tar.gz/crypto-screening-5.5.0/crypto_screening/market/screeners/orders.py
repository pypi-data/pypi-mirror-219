# orders.py

import datetime as dt
from typing import (
    Dict, Optional, Iterable, Any, Union, List, Callable
)

import pandas as pd

from cryptofeed import FeedHandler
from cryptofeed.types import Ticker
from cryptofeed.defines import TICKER

from crypto_screening.symbols import adjust_symbol
from crypto_screening.process import find_string_value
from crypto_screening.dataset import (
    BIDS, ASKS, ORDERS_COLUMNS, create_market_dataframe,
    load_dataset, save_dataset
)
from crypto_screening.market.screeners.base import BaseScreener
from crypto_screening.market.screeners.recorder import (
    MarketScreener, structure_screener_datasets, MarketRecorder
)

__all__ = [
    "OrdersMarketScreener",
    "OrdersMarketRecorder",
    "OrdersScreener",
    "create_orders_market",
    "orders_market_screener",
    "orders_market_recorder",
    "create_orders_dataframe",
    "record_orders"
]

Market = Dict[str, Dict[str, pd.DataFrame]]

def create_orders_dataframe() -> pd.DataFrame:
    """
    Creates a dataframe for the order book data.

    :return: The dataframe.
    """

    return create_market_dataframe(
        columns=OrdersMarketRecorder.COLUMNS
    )
# end create_orderbook_dataframe

def create_orders_market(data: Dict[str, Iterable[str]]) -> Market:
    """
    Creates the dataframes of the market data.

    :param data: The market data.

    :return: The dataframes of the market data.
    """

    return {
        exchange.lower(): {
            symbol.upper(): create_orders_dataframe()
            for symbol in data[exchange]
        } for exchange in data
    }
# end create_orders_market

class OrdersScreener(BaseScreener):
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
        The dataset of the market data as orders.
    """

    @property
    def orders_market(self) -> pd.DataFrame:
        """
        Returns the market to hold the recorder data.

        :return: The market object.
        """

        return self.market
    # end orders_market

    def orders_dataset_path(self, location: Optional[str] = None) -> str:
        """
        Creates the path to the saving file for the screener object.

        :param location: The saving location of the dataset.

        :return: The saving path for the dataset.
        """

        return (
            self.dataset_path(location=location).
            replace(".csv", f"-ORDERS.csv")
        )
    # end orders_dataset_path

    def save_orders_dataset(self, location: Optional[str] = None) -> None:
        """
        Saves the data of the screener.

        :param location: The saving location of the dataset.
        """

        if len(self.orders_market) > 0:
            save_dataset(
                dataset=self.orders_market,
                path=self.orders_dataset_path(location=location)
            )
        # end if
    # end save_orders_dataset

    def save_dataset(self, location: Optional[str] = None) -> None:
        """
        Saves the data of the screener.

        :param location: The saving location of the dataset.
        """

        self.save_orders_dataset(location=location)
    # end save_dataset

    def load_orders_dataset(self, location: Optional[str] = None) -> None:
        """
        Saves the data of the screener.

        :param location: The saving location of the dataset.
        """

        data = load_dataset(path=self.orders_dataset_path(location=location))

        for index, data in zip(data.index[:], data.loc[:]):
            self.orders_market.loc[index] = data
        # end for
    # end load_orders_dataset

    def load_dataset(self, location: Optional[str] = None) -> None:
        """
        Saves the data of the screener.

        :param location: The saving location of the dataset.
        """

        self.load_orders_dataset(location=location)
    # end load_dataset
# end OrdersScreener

def record_orders(market: Market, data: Ticker, timestamp: float) -> bool:
    """
    Records the data from the crypto feed into the dataset.

    :param market: The market structure.
    :param data: The data from the exchange.
    :param timestamp: The time of the request.
    """

    exchange = find_string_value(
        value=data.exchange, values=market.keys()
    )
    symbol = find_string_value(
        value=adjust_symbol(symbol=data.symbol),
        values=exchange
    )

    dataset = (
        market.
        setdefault(exchange, {}).
        setdefault(symbol, create_orders_dataframe())
    )

    try:
        dataset.loc[dt.datetime.fromtimestamp(timestamp)] = {
            BIDS: float(data.bid),
            ASKS: float(data.ask)
        }

        return True

    except IndexError:
        return False
    # end try
# end record_orders

RecorderParameters = Dict[str, Union[Iterable[str], Dict[str, Callable]]]

class OrdersMarketRecorder(MarketRecorder):
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

    COLUMNS = ORDERS_COLUMNS

    @property
    def orders_market(self) -> Market:
        """
        Returns the market to hold the recorder data.

        :return: The market object.
        """

        return self.market
    # end orders_market

    def parameters(self) -> RecorderParameters:
        """
        Returns the order book parameters.

        :return: The order book parameters.
        """

        return dict(
            channels=[TICKER],
            callbacks={TICKER: self.record},
            max_depth=1
        )
    # end parameters

    def orders(self, exchange: str, symbol: str) -> pd.DataFrame:
        """
        Returns the market data of the symbol from the exchange.

        :param exchange: The source name of the exchange.
        :param symbol: The symbol of the pair.

        :return: The dataset of the spread data.
        """

        return self.data(exchange=exchange, symbol=symbol)
    # end orders

    def orders_in_market(self, exchange: str, symbol: str) -> bool:
        """
        Returns the market data of the symbol from the exchange.

        :param exchange: The source name of the exchange.
        :param symbol: The symbol of the pair.

        :return: The dataset of the spread data.
        """

        try:
            self.orders(exchange=exchange, symbol=symbol)

            return True

        except ValueError:
            return False
        # end try
    # end orders_in_market

    async def record(self, data: Ticker, timestamp: float) -> bool:
        """
        Records the data from the crypto feed into the dataset.

        :param data: The data from the exchange.
        :param timestamp: The time of the request.
        """

        return record_orders(
            market=self.market, data=data, timestamp=timestamp
        )
    # end record
# end MarketOrdersRecorder

class OrdersMarketScreener(MarketScreener):
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

    screeners: List[OrdersScreener]
    recorder: OrdersMarketRecorder

    COLUMNS = OrdersMarketRecorder.COLUMNS

    def __init__(
            self,
            screeners: Optional[Iterable[OrdersScreener]] = None,
            location: Optional[str] = None,
            cancel: Optional[Union[float, dt.timedelta]] = None,
            delay: Optional[Union[float, dt.timedelta]] = None,
            refresh: Optional[Union[float, dt.timedelta, bool]] = None,
            limited: Optional[bool] = None,
            handler: Optional[FeedHandler] = None,
            amount: Optional[int] = None,
            recorder: Optional[OrdersMarketRecorder] = None
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
            delay=delay, recorder=recorder or OrdersMarketRecorder(
                market=structure_screener_datasets(screeners=screeners)
            ),
            screeners=screeners, handler=handler, limited=limited,
            amount=amount, refresh=refresh
        )

        self.screeners[:] = screeners or self.create_orders_screeners()
    # end __init__

    @property
    def orders_market(self) -> Market:
        """
        Returns the market to hold the recorder data.

        :return: The market object.
        """

        return self.recorder.orders_market
    # end orders_market

    @property
    def orderbook_screeners(self) -> List[OrdersScreener]:
        """
        Returns a list of all the order-book screeners.

        :return: The order-book screeners.
        """

        return [
            screener for screener in self.screeners
            if isinstance(screener, OrdersScreener)
        ]
    # end orders_screeners

    def connect_screeners(self) -> None:
        """Connects the screeners to the recording object."""

        for screener in self.screeners:
            if isinstance(screener, OrdersScreener):
                screener.market = self.orders(
                    exchange=screener.exchange, symbol=screener.symbol
                )
            # end if
        # end for
    # end connect_screeners

    def orders(self, exchange: str, symbol: str) -> pd.DataFrame:
        """
        Returns the market data of the symbol from the exchange.

        :param exchange: The source name of the exchange.
        :param symbol: The symbol of the pair.

        :return: The dataset of the spread data.
        """

        return self.recorder.orders(exchange=exchange, symbol=symbol)
    # end orders

    def orders_in_market(self, exchange: str, symbol: str) -> bool:
        """
        Returns the market data of the symbol from the exchange.

        :param exchange: The source name of the exchange.
        :param symbol: The symbol of the pair.

        :return: The dataset of the spread data.
        """

        return self.recorder.orders_in_market(exchange=exchange, symbol=symbol)
    # end orders_in_market

    def create_orders_screener(
            self,
            symbol: str,
            exchange: str,
            location: Optional[str] = None,
            cancel: Optional[Union[float, dt.timedelta]] = None,
            delay: Optional[Union[float, dt.timedelta]] = None,
            container: Optional[Dict[str, Dict[str, OrdersScreener]]] = None
    ) -> OrdersScreener:
        """
        Defines the class attributes.

        :param symbol: The symbol of the asset.
        :param exchange: The exchange to get source data from.
        :param location: The saving location for the data.
        :param cancel: The time to cancel the waiting.
        :param delay: The delay for the process.
        :param container: The container to contain the new screener.
        """

        if container is None:
            container = {}
        # end if

        if cancel is None:
            cancel = self.cancel
        # end if

        if delay is None:
            delay = self.delay
        # end if

        screener = OrdersScreener(
            symbol=symbol, exchange=exchange, delay=delay,
            location=location, cancel=cancel, market=(
                self.orders(exchange=exchange, symbol=symbol)
                if self.orders_in_market(symbol=symbol, exchange=exchange)
                else None
            )
        )

        container.setdefault(exchange, {})[symbol] = screener

        return screener
    # end create_orders_screener

    def create_orders_screeners(
            self,
            location: Optional[str] = None,
            cancel: Optional[Union[float, dt.timedelta]] = None,
            delay: Optional[Union[float, dt.timedelta]] = None,
            container: Optional[Dict[str, Dict[str, OrdersScreener]]] = None
    ) -> List[OrdersScreener]:
        """
        Defines the class attributes.

        :param location: The saving location for the data.
        :param cancel: The time to cancel the waiting.
        :param delay: The delay for the process.
        :param container: The container to contain the new screeners.
        """

        screeners = []

        for exchange, symbols in self.structure().items():
            for symbol in symbols:
                screeners.append(
                    self.create_orders_screener(
                        symbol=symbol, exchange=exchange, delay=delay,
                        location=location, cancel=cancel, container=container
                    )
                )
            # end for
        # end for

        return screeners
    # end create_orders_screeners
# end MarketOrderbookScreener

def orders_market_recorder(data: Dict[str, Iterable[str]]) -> OrdersMarketRecorder:
    """
    Creates the market recorder object for the data.

    :param data: The market data.

    :return: The market recorder object.
    """

    return OrdersMarketRecorder(
        market=create_orders_market(data=data)
    )
# end orders_market_recorder

def orders_market_screener(
        data: Dict[str, Iterable[str]],
        location: Optional[str] = None,
        cancel: Optional[Union[float, dt.timedelta]] = None,
        delay: Optional[Union[float, dt.timedelta]] = None,
        limited: Optional[bool] = None,
        handler: Optional[FeedHandler] = None,
        market: Optional[Market] = None,
        amount: Optional[int] = None,
        refresh: Optional[Union[float, dt.timedelta, bool]] = None,
        recorder: Optional[OrdersMarketRecorder] = None,
        fixed: Optional[bool] = True,
        separator: Optional[str] = None,
        parameters: Optional[Union[Dict[str, Dict[str, Any]], Dict[str, Any]]] = None
) -> OrdersMarketScreener:
    """
    Creates the market screener object for the data.

    :param data: The market data.
    :param handler: The handler object for the market data.
    :param limited: The value to limit the screeners to active only.
    :param parameters: The parameters for the exchanges.
    :param market: The object to fill with the crypto feed record.
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

    screener = OrdersMarketScreener(
        recorder=recorder or OrdersMarketRecorder(
            market=market or create_orders_market(data=data)
        ),
        handler=handler, location=location, amount=amount,
        cancel=cancel, delay=delay, limited=limited, refresh=refresh
    )

    screener.add_feeds(
        data=screener.recorder.structure(), fixed=fixed,
        separator=separator, parameters=parameters
    )

    return screener
# end orders_market_screener