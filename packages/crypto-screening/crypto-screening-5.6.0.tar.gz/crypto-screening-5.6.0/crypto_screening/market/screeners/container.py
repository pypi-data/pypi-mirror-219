# container.py

from typing import Iterable, List, Type, TypeVar, Optional

from represent import Modifiers

from crypto_screening.market.screeners.recorder import (
    structure_screener_datasets, MarketRecorder
)
from crypto_screening.market.screeners.base import BaseScreener
from crypto_screening.market.screeners.ohlcv import OHLCVScreener
from crypto_screening.market.screeners.orderbook import OrderbookScreener
from crypto_screening.market.screeners.trades import TradesScreener
from crypto_screening.market.screeners.orders import OrdersScreener

_S = TypeVar("_S")

class ScreenersContainer(MarketRecorder):
    """
    A class to represent a multi-exchange multi-pairs crypto data screener.
    Using this class enables extracting screener objects and screeners
    data by the exchange name and the symbol of the pair.

    parameters:

    - screeners:
        The screener objects.

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

    def find_screener(
            self, exchange: str, symbol: str, base: Optional[Type[_S]] = None
    ) -> _S:
        """
        Returns the data by according to the parameters.

        :param base: The base type of the screener.
        :param exchange: The exchange name.
        :param symbol: The ticker name.

        :return: The data.
        """

        for screener in self.screeners:
            if (
                (screener.exchange == exchange) and
                (screener.symbol == symbol) and
                isinstance(screener, base or BaseScreener)
            ):
                return screener
            # end if
        # end for

        raise ValueError(
            f"{base} Screener object for symbol - {symbol} and "
            f"exchange - {exchange} cannot be found in {repr(self)}."
        )
    # end find_orderbook_screener

    def find_screeners(
            self, exchange: str, symbol: str, base: Optional[Type[_S]] = None
    ) -> List[_S]:
        """
        Returns the data by according to the parameters.

        :param base: The base type of the screener.
        :param exchange: The exchange name.
        :param symbol: The ticker name.

        :return: The data.
        """

        screeners = []

        for screener in self.screeners:
            if (
                (screener.exchange == exchange) and
                (screener.symbol == symbol) and
                isinstance(screener, base or BaseScreener)
            ):
                screeners.append(screener)
            # end if
        # end for

        return screeners
    # end find_screeners

    def screener_in_market(
            self, exchange: str, symbol: str, base: Optional[Type[_S]] = None
    ) -> bool:
        """
        Returns the data by according to the parameters.

        :param base: The base type of the screener.
        :param exchange: The exchange name.
        :param symbol: The ticker name.

        :return: The data.
        """

        try:
            self.find_screener(
                exchange=exchange, symbol=symbol, base=base
            )

            return True

        except ValueError:
            return False
        # end try
    # end screener_in_market

    def orderbook_screener_in_market(self, exchange: str, symbol: str) -> bool:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.

        :return: The data.
        """

        return self.screener_in_market(
            exchange=exchange, symbol=symbol, base=OrderbookScreener
        )
    # end orderbook_screener_in_market

    def orders_screener_in_market(self, exchange: str, symbol: str) -> bool:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.

        :return: The data.
        """

        return self.screener_in_market(
            exchange=exchange, symbol=symbol, base=OrdersScreener
        )
    # end orders_screener_in_market

    def find_orderbook_screener(self, exchange: str, symbol: str) -> OrderbookScreener:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.

        :return: The data.
        """

        return self.find_screener(
            exchange=exchange, symbol=symbol, base=OrderbookScreener
        )
    # end find_orderbook_screener

    def find_orders_screener(self, exchange: str, symbol: str) -> OrdersScreener:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.

        :return: The data.
        """

        return self.find_screener(
            exchange=exchange, symbol=symbol, base=OrdersScreener
        )
    # end find_orders_screener

    def find_orderbook_screeners(self, exchange: str, symbol: str) -> List[OrderbookScreener]:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.

        :return: The data.
        """

        return self.find_screeners(
            exchange=exchange, symbol=symbol, base=OrderbookScreener
        )
    # end find_orderbook_screener

    def find_orders_screeners(self, exchange: str, symbol: str) -> List[OrdersScreener]:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.

        :return: The data.
        """

        return self.find_screeners(
            exchange=exchange, symbol=symbol, base=OrdersScreener
        )
    # end find_orders_screeners

    def ohlcv_screener_in_market(
            self, exchange: str, symbol: str, interval: str
    ) -> bool:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.
        :param interval: The interval for the dataset.

        :return: The data.
        """

        try:
            self.find_ohlcv_screener(
                exchange=exchange, symbol=symbol, interval=interval
            )

            return True

        except ValueError:
            return False
    # end ohlcv_screener_in_market

    def trades_screener_in_market(self, exchange: str, symbol: str) -> bool:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.

        :return: The data.
        """

        return self.screener_in_market(
            exchange=exchange, symbol=symbol, base=TradesScreener
        )
    # end trades_screener_in_market

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
                isinstance(screener, OHLCVScreener) and
                (screener.interval == interval)
            ):
                return screener
            # end if
        # end for

        raise ValueError(
            f"OHLCV Screener object for symbol - {symbol} and "
            f"exchange - {exchange} cannot be found in {repr(self)}."
        )
    # end find_screeners

    def find_trades_screener(self, exchange: str, symbol: str) -> TradesScreener:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.

        :return: The data.
        """

        return self.find_screener(
            exchange=exchange, symbol=symbol, base=TradesScreener
        )
    # end find_trades_screener

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
    # end find_ohlcv_screeners

    def find_trades_screeners(self, exchange: str, symbol: str) -> List[TradesScreener]:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.

        :return: The data.
        """

        return self.find_screeners(
            exchange=exchange, symbol=symbol, base=TradesScreener
        )
    # end find_trades_screeners
# end ScreenersContainer