# container.py

from typing import Iterable, List

from represent import Modifiers

from crypto_screening.market.screeners.base import (
    BaseScreener, structure_screener_datasets
)
from crypto_screening.market.screeners import (
    MarketRecorder, OrderbookScreener, OHLCVScreener
)

class ScreenersContainer(MarketRecorder):
    """
    A class to represent a multi-exchange multi-pairs crypto data screener.
    Using this class enables extracting screener objects and screeners
    data by the exchange name and the symbol of the pair.

    parameters:

    - screeners:
        The screener objects.

    - data:
        The structure of the screeners, by exchanges and symbols.

    >>> from crypto_screening.market.screeners.container import ScreenersContainer
    >>> from crypto_screening.market.screeners.base import BaseScreener
    >>>
    >>> dynamic_screener = ScreenersContainer(
    >>>     screeners=[BaseScreener(exchange="binance", symbol="BTC/USDT")]
    >>> )
    >>>
    >>> dynamic_screener.find_screener(exchange="binance", symbol="BTC/USDT"))
    >>> dynamic_screener.data(exchange="binance", symbol="BTC/USDT", length=10))
    """

    __slots__ = "screeners",

    __modifiers__ = Modifiers(**MarketRecorder.__modifiers__)
    __modifiers__.hidden.append("screeners")

    def __init__(self, screeners: Iterable[BaseScreener]) -> None:
        """
        Defines the class attributes.

        :param screeners: The data screener object.
        """

        super().__init__(market=structure_screener_datasets(screeners=screeners))

        self.screeners = screeners
    # end __init__

    def find_screeners(self, exchange: str, symbol: str) -> List[BaseScreener]:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.

        :return: The data.
        """

        if not self.in_market(exchange=exchange, symbol=symbol):
            raise ValueError(
                f"Screener object for symbol - {symbol} and "
                f"exchange - {exchange} cannot be found in {self}."
            )
        # end if

        screeners = []

        for screener in self.screeners:
            if (screener.exchange == exchange) and (screener.symbol == symbol):
                screeners.append(screener)
            # end if
        # end for

        return screeners
    # end find_screeners

    def find_orderbook_screener(self, exchange: str, symbol: str) -> OrderbookScreener:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.

        :return: The data.
        """

        for screener in self.screeners:
            if (
                (screener.exchange == exchange) and
                (screener.symbol == symbol) and
                isinstance(screener, OrderbookScreener)
            ):
                return screener
            # end if
        # end for

        raise ValueError(
            f"Orderbook Screener object for symbol - {symbol} and "
            f"exchange - {exchange} cannot be found in {self}."
        )
    # end find_orderbook_screener

    def find_orderbook_screeners(self, exchange: str, symbol: str) -> List[OrderbookScreener]:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.

        :return: The data.
        """

        screeners = []

        for screener in self.screeners:
            if (
                (screener.exchange == exchange) and
                (screener.symbol == symbol) and
                isinstance(screener, OrderbookScreener)
            ):
                screeners.append(screener)
            # end if
        # end for

        return screeners
    # end find_orderbook_screener

    def find_ohlcv_screener(
            self, exchange: str, symbol: str, interval: str
    ) -> OHLCVScreener:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.
        :param interval: The interval for the dataset.

        :return: The data.
        """

        for screener in self.screeners:
            if (
                (screener.exchange == exchange) and
                (screener.symbol == symbol) and
                (screener.interval == interval) and
                isinstance(screener, OHLCVScreener)
            ):
                return screener
            # end if
        # end for

        raise ValueError(
            f"OHLCV Screener object for symbol - {symbol} and "
            f"exchange - {exchange} cannot be found in {self}."
        )
    # end find_screeners

    def find_ohlcv_screeners(
            self, exchange: str, symbol: str, interval: str
    ) -> List[OHLCVScreener]:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.
        :param interval: The interval for the datasets.

        :return: The data.
        """

        screeners = []

        for screener in self.screeners:
            if (
                (screener.exchange == exchange) and
                (screener.symbol == symbol) and
                (screener.interval == interval) and
                isinstance(screener, OHLCVScreener)
            ):
                screeners.append(screener)
            # end if
        # end for

        return screeners
    # end find_orderbook_screener
# end ScreenersContainer