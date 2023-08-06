# dynamic.py

from typing import Optional, Iterable, List, Union, Dict

from represent import Modifiers

import pandas as pd

from crypto_screening.market.screeners import OrderbookScreener, OHLCVScreener
from crypto_screening.collect.screeners import exchanges_symbols_screeners
from crypto_screening.collect.orderbook import (
    assets_orderbook_market_state, symbols_orderbook_market_state,
    SymbolsOrderbookMarketState, AssetsOrderbookMarketState
)
from crypto_screening.collect.ohlcv import (
    assets_ohlcv_market_state, symbols_ohlcv_market_state,
    SymbolsOHLCVMarketState, AssetsOHLCVMarketState
)
from crypto_screening.market.screeners.container import ScreenersContainer

__all__ = [
    "DynamicScreener"
]

class DynamicScreener(ScreenersContainer):
    """
    A class to represent a multi-exchange multi-pairs crypto data screener.
    Using this class enables extracting screener objects and screeners
    data by the exchange name and the symbol of the pair.

    parameters:

    - screeners:
        The screener objects.

    >>> from crypto_screening.market.dynamic import DynamicScreener
    >>> from crypto_screening.market.screeners.base import BaseScreener
    >>>
    >>> dynamic_screener = DynamicScreener(
    >>>     screeners=[BaseScreener(exchange="binance", symbol="BTC/USDT")]
    >>> )
    >>>
    >>> dynamic_screener.find_screener(exchange="binance", symbol="BTC/USDT"))
    >>> dynamic_screener.data(exchange="binance", symbol="BTC/USDT", length=10))
    """

    __modifiers__ = Modifiers(**ScreenersContainer.__modifiers__)
    __modifiers__.excluded.append("exchanges")

    def find_dataset(
            self,
            exchange: str,
            symbol: str,
            length: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.
        :param length: The length of the data.

        :return: The data.
        """

        screener = self.find_screener(exchange=exchange, symbol=symbol)

        length = min(length or 0, len(screener.market))

        return screener.market.iloc[-length:]
    # end find_dataset

    def find_datasets(
            self,
            exchange: str,
            symbol: str,
            length: Optional[int] = None
    ) -> List[pd.DataFrame]:
        """
        Returns the data by according to the parameters.

        :param exchange: The exchange name.
        :param symbol: The ticker name.
        :param length: The length of the data.

        :return: The data.
        """

        screeners = self.find_screeners(exchange=exchange, symbol=symbol)

        return [
            screener.market.iloc[-min(length or 0, len(screener.market)):]
            for screener in screeners
        ]
    # end find_dataset

    def assets_orderbook_market_state(
            self,
            exchanges: Optional[Iterable[str]] = None,
            separator: Optional[str] = None,
            length: Optional[int] = None,
            adjust: Optional[bool] = True,
            bases: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            quotes: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            included: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None
    ) -> AssetsOrderbookMarketState:
        """
        Fetches the prices and relations between the assets.

        :param length: The length of the prices.
        :param adjust: The value to adjust the length of the sequences.
        :param exchanges: The exchanges.
        :param quotes: The quotes of the asset pairs.
        :param excluded: The excluded symbols.
        :param adjust: The value to adjust the invalid exchanges.
        :param separator: The separator of the assets.
        :param included: The symbols to include.
        :param bases: The bases of the asset pairs.

        :return: The prices of the assets.
        """

        screeners = [
            screener for screener in self.screeners
            if isinstance(screener, OrderbookScreener)
        ]

        screeners = exchanges_symbols_screeners(
            screeners=screeners, exchanges=exchanges,
            separator=separator, bases=bases, quotes=quotes,
            included=included, excluded=excluded, adjust=adjust
        )

        return assets_orderbook_market_state(
            screeners=screeners, separator=separator,
            length=length, adjust=adjust
        )
    # end assets_orderbook_market_state

    def symbols_orderbook_market_state(
            self,
            exchanges: Optional[Iterable[str]] = None,
            separator: Optional[str] = None,
            length: Optional[int] = None,
            adjust: Optional[bool] = True,
            bases: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            quotes: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            included: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None
    ) -> SymbolsOrderbookMarketState:
        """
        Fetches the prices and relations between the assets.

        :param length: The length of the prices.
        :param adjust: The value to adjust the length of the sequences.
        :param exchanges: The exchanges.
        :param quotes: The quotes of the asset pairs.
        :param excluded: The excluded symbols.
        :param adjust: The value to adjust the invalid exchanges.
        :param separator: The separator of the assets.
        :param included: The symbols to include.
        :param bases: The bases of the asset pairs.

        :return: The prices of the assets.
        """

        screeners = [
            screener for screener in self.screeners
            if isinstance(screener, OrderbookScreener)
        ]

        screeners = exchanges_symbols_screeners(
            screeners=screeners, exchanges=exchanges,
            separator=separator, bases=bases, quotes=quotes,
            included=included, excluded=excluded, adjust=adjust
        )

        return symbols_orderbook_market_state(
            screeners=screeners, length=length, adjust=adjust
        )
    # end symbols_orderbook_market_state

    def assets_ohlcv_market_state(
            self,
            exchanges: Optional[Iterable[str]] = None,
            separator: Optional[str] = None,
            length: Optional[int] = None,
            adjust: Optional[bool] = True,
            bases: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            quotes: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            included: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None
    ) -> AssetsOHLCVMarketState:
        """
        Fetches the prices and relations between the assets.

        :param length: The length of the prices.
        :param adjust: The value to adjust the length of the sequences.
        :param exchanges: The exchanges.
        :param quotes: The quotes of the asset pairs.
        :param excluded: The excluded symbols.
        :param adjust: The value to adjust the invalid exchanges.
        :param separator: The separator of the assets.
        :param included: The symbols to include.
        :param bases: The bases of the asset pairs.

        :return: The prices of the assets.
        """

        screeners = [
            screener for screener in self.screeners
            if isinstance(screener, OHLCVScreener)
        ]

        screeners = exchanges_symbols_screeners(
            screeners=screeners, exchanges=exchanges,
            separator=separator, bases=bases, quotes=quotes,
            included=included, excluded=excluded, adjust=adjust
        )

        return assets_ohlcv_market_state(
            screeners=screeners, separator=separator,
            length=length, adjust=adjust
        )
    # end assets_ohlcv_market_state

    def symbols_ohlcv_market_state(
            self,
            exchanges: Optional[Iterable[str]] = None,
            separator: Optional[str] = None,
            length: Optional[int] = None,
            adjust: Optional[bool] = True,
            bases: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            quotes: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            included: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None,
            excluded: Optional[Union[Dict[str, Iterable[str]], Iterable[str]]] = None
    ) -> SymbolsOHLCVMarketState:
        """
        Fetches the prices and relations between the assets.

        :param length: The length of the prices.
        :param adjust: The value to adjust the length of the sequences.
        :param exchanges: The exchanges.
        :param quotes: The quotes of the asset pairs.
        :param excluded: The excluded symbols.
        :param adjust: The value to adjust the invalid exchanges.
        :param separator: The separator of the assets.
        :param included: The symbols to include.
        :param bases: The bases of the asset pairs.

        :return: The prices of the assets.
        """

        screeners = [
            screener for screener in self.screeners
            if isinstance(screener, OHLCVScreener)
        ]

        screeners = exchanges_symbols_screeners(
            screeners=screeners, exchanges=exchanges,
            separator=separator, bases=bases, quotes=quotes,
            included=included, excluded=excluded, adjust=adjust
        )

        return symbols_ohlcv_market_state(
            screeners=screeners, length=length, adjust=adjust
        )
    # end symbols_ohlcv_market_state
# end DynamicScreener