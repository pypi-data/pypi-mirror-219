# orderbook.py

import datetime as dt
from typing import (
    Dict, Optional, Iterable, Any, Union, List
)

import pandas as pd

from cryptofeed import FeedHandler
from cryptofeed.types import OrderBook

from crypto_screening.dataset import (
    BIDS, ASKS, BIDS_VOLUME, ASKS_VOLUME
)
from crypto_screening.symbols import adjust_symbol
from crypto_screening.market.screeners.base import (
    BaseScreener, structure_screener_datasets
)
from crypto_screening.market.screeners.recorder import MarketScreener
from crypto_screening.market.screeners.base import (
    create_market_dataframe, MarketRecorder
)
from crypto_screening.process import find_string_value

__all__ = [
    "OrderbookMarketScreener",
    "OrderbookMarketRecorder",
    "OrderbookScreener",
    "create_orderbook_market",
    "orderbook_market_screener",
    "orderbook_market_recorder",
    "create_orderbook_dataframe"
]

Market = Dict[str, Dict[str, pd.DataFrame]]

def create_orderbook_dataframe() -> pd.DataFrame:
    """
    Creates a dataframe for the order book data.

    :return: The dataframe.
    """

    return create_market_dataframe(
        columns=OrderbookMarketRecorder.COLUMNS
    )
# end create_orderbook_dataframe

def create_orderbook_market(data: Dict[str, Iterable[str]]) -> Dict[str, Dict[str, pd.DataFrame]]:
    """
    Creates the dataframes of the market data.

    :param data: The market data.

    :return: The dataframes of the market data.
    """

    return {
        exchange.lower(): {
            symbol.upper(): create_orderbook_dataframe()
            for symbol in data[exchange]
        } for exchange in data
    }
# end create_orderbook_market

class OrderbookScreener(BaseScreener):
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
        The dataset of the market data as BID/ASK spread.
    """
# end OrderBookScreener

def validate_orderbook_market(data: Any) -> Market:
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
                        isinstance(symbol, str) and
                        isinstance(dataset, pd.DataFrame)
                        for symbol, dataset in values.items()
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
# end validate_orderbook_market

class OrderbookMarketRecorder(MarketRecorder):
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

    COLUMNS = (BIDS, ASKS, BIDS_VOLUME, ASKS_VOLUME)

    @staticmethod
    def validate_market(data: Any) -> Market:
        """
        Validates the data.

        :param data: The data to validate.

        :return: The valid data.
        """

        return validate_orderbook_market(data=data)
    # end validate_market

    def orderbook(self, exchange: str, symbol: str) -> pd.DataFrame:
        """
        Returns the market data of the symbol from the exchange.

        :param exchange: The source name of the exchange.
        :param symbol: The symbol of the pair.

        :return: The dataset of the spread data.
        """

        return self.data(exchange=exchange, symbol=symbol)
    # end orderbook

    async def record(self, data: OrderBook, timestamp: float) -> None:
        """
        Records the data from the crypto feed into the dataset.

        :param data: The data from the exchange.
        :param timestamp: The time of the request.
        """

        exchange = find_string_value(
            value=data.exchange, values=self.market.keys()
        )
        symbol = find_string_value(
            value=adjust_symbol(symbol=data.symbol),
            values=exchange
        )

        dataset = (
            self.market.
            setdefault(exchange, {}).
            setdefault(symbol, create_orderbook_dataframe())
        )

        bids = data.book.bids.to_list()
        asks = data.book.asks.to_list()

        try:
            dataset.loc[dt.datetime.fromtimestamp(timestamp)] = {
                BIDS: float(bids[0][0]),
                ASKS: float(asks[0][0]),
                BIDS_VOLUME: float(bids[0][1]),
                ASKS_VOLUME: float(asks[0][1])
            }

        except IndexError:
            pass
        # end try
    # end record
# end MarketOrderbookRecorder

class OrderbookMarketScreener(MarketScreener):
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

    screeners: List[OrderbookScreener]
    recorder: OrderbookMarketRecorder

    COLUMNS = OrderbookMarketRecorder.COLUMNS

    def __init__(
            self,
            screeners: Optional[Iterable[OrderbookScreener]] = None,
            location: Optional[str] = None,
            cancel: Optional[Union[float, dt.timedelta]] = None,
            delay: Optional[Union[float, dt.timedelta]] = None,
            refresh: Optional[Union[float, dt.timedelta, bool]] = None,
            limited: Optional[bool] = None,
            handler: Optional[FeedHandler] = None,
            amount: Optional[int] = None,
            recorder: Optional[OrderbookMarketRecorder] = None
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
            delay=delay, recorder=recorder or OrderbookMarketRecorder(
                market=structure_screener_datasets(screeners=screeners)
            ),
            screeners=screeners, handler=handler, limited=limited,
            amount=amount, refresh=refresh
        )

        self.screeners[:] = self.screeners or self.create_orderbook_screeners()
    # end __init__

    def create_orderbook_screener(
            self,
            symbol: str,
            exchange: str,
            location: Optional[str] = None,
            cancel: Optional[Union[float, dt.timedelta]] = None,
            delay: Optional[Union[float, dt.timedelta]] = None,
            container: Optional[Dict[str, Dict[str, OrderbookScreener]]] = None
    ) -> OrderbookScreener:
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

        screener = OrderbookScreener(
            symbol=symbol, exchange=exchange, delay=delay,
            location=location, cancel=cancel, market=(
                self.orderbook(exchange=exchange, symbol=symbol)
                if self.in_market(symbol=symbol, exchange=exchange)
                else None
            )
        )

        container.setdefault(exchange, {})[symbol] = screener

        return screener
    # end create_orderbook_screener

    def create_orderbook_screeners(
            self,
            location: Optional[str] = None,
            cancel: Optional[Union[float, dt.timedelta]] = None,
            delay: Optional[Union[float, dt.timedelta]] = None,
            container: Optional[Dict[str, Dict[str, OrderbookScreener]]] = None
    ) -> List[OrderbookScreener]:
        """
        Defines the class attributes.

        :param location: The saving location for the data.
        :param cancel: The time to cancel the waiting.
        :param delay: The delay for the process.
        :param container: The container to contain the new screeners.
        """

        screeners = []

        for exchange in self.market:
            for symbol in self.market[exchange]:
                screeners.append(
                    self.create_orderbook_screener(
                        symbol=symbol, exchange=exchange, delay=delay,
                        location=location, cancel=cancel, container=container
                    )
                )
            # end for
        # end for

        return screeners
    # end create_orderbook_screeners
# end MarketOrderbookScreener

def orderbook_market_recorder(data: Dict[str, Iterable[str]]) -> OrderbookMarketRecorder:
    """
    Creates the market recorder object for the data.

    :param data: The market data.

    :return: The market recorder object.
    """

    return OrderbookMarketRecorder(
        market=create_orderbook_market(data=data)
    )
# end orderbook_market_recorder

def orderbook_market_screener(
        data: Dict[str, Iterable[str]],
        location: Optional[str] = None,
        cancel: Optional[Union[float, dt.timedelta]] = None,
        delay: Optional[Union[float, dt.timedelta]] = None,
        limited: Optional[bool] = None,
        handler: Optional[FeedHandler] = None,
        market: Optional[Market] = None,
        amount: Optional[int] = None,
        refresh: Optional[Union[float, dt.timedelta, bool]] = None,
        recorder: Optional[OrderbookMarketRecorder] = None,
        fixed: Optional[bool] = True,
        separator: Optional[str] = None,
        parameters: Optional[Union[Dict[str, Dict[str, Any]], Dict[str, Any]]] = None
) -> OrderbookMarketScreener:
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

    screener = OrderbookMarketScreener(
        recorder=recorder or OrderbookMarketRecorder(
            market=market or create_orderbook_market(data=data)
        ),
        handler=handler, location=location, amount=amount,
        cancel=cancel, delay=delay, limited=limited, refresh=refresh
    )

    screener.add_feeds(
        data=screener.recorder.structure(), fixed=fixed,
        separator=separator, parameters=parameters
    )

    return screener
# end orderbook_market_recorder