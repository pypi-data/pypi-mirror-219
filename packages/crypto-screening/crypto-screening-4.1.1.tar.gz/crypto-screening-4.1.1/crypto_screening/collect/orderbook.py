# orderbook.py

from abc import ABCMeta
import datetime as dt
from typing import (
    Iterable, Dict, Optional, ClassVar, List, Tuple
)

from attrs import define

from represent import represent, Modifiers

import pandas as pd

from crypto_screening.market.screeners.base import BaseScreener
from crypto_screening.market.screeners.orderbook import (
    create_orderbook_dataframe
)
from crypto_screening.collect.market import (
    MarketBase, assets_market_prices, assets_market_data,
    is_symbol_in_assets_market_prices, symbols_market_prices,
    is_symbol_in_symbols_market_prices, symbols_market_data,
    assets_to_symbol_market_prices, assets_market_state,
    symbol_to_assets_market_prices, symbols_market_state,
    merge_assets_market_states, merge_symbols_market_states,
    ORDERBOOK_COLUMNS
)

__all__ = [
    "symbols_orderbook_market_state",
    "merge_assets_orderbook_market_states",
    "merge_symbols_orderbook_market_states",
    "assets_orderbook_market_state",
    "AssetsOrderbookMarketState",
    "SymbolsOrderbookMarketState",
    "symbols_to_assets_orderbook_market_state",
    "assets_to_symbols_orderbook_market_state",
    "ORDERBOOK_COLUMNS"
]

AssetsPrices = Dict[str, Dict[str, Dict[str, List[Tuple[dt.datetime, float]]]]]
SymbolsPrices = Dict[str, Dict[str, List[Tuple[dt.datetime, float]]]]

@define(repr=False)
@represent
class OrderbookMarketBase(MarketBase, metaclass=ABCMeta):
    """
    A class to represent the current market state.

    This object contains the state of the market, as Close,
    bids and asks prices of specific assets, gathered from the network.

    attributes:

    - screeners:
        The screener objects to collect the prices of the assets.
    """

    __modifiers__: ClassVar[Modifiers] = Modifiers(
        **MarketBase.__modifiers__
    )
    __modifiers__.excluded.extend(["bids", "asks", "bids_volume", "asks_volume"])
# end OrderbookMarketBase

AssetsMarketData = Dict[str, Dict[str, Dict[str, List[Tuple[dt.datetime, Dict[str, float]]]]]]
AssetsMarketDatasets = Dict[str, Dict[str, Dict[str, pd.DataFrame]]]

@define(repr=False)
@represent
class AssetsOrderbookMarketState(OrderbookMarketBase):
    """
    A class to represent the current market state.

    This object contains the state of the market, as Close,
    bids and asks prices of specific assets, gathered from the network.

    attributes:

    - screeners:
        The screener objects to collect the prices of the assets.

    - bids:
        The bids prices of the assets.

    - asks:
        The asks prices of the assets.

    - bids_volume:
        The bids volume prices of the assets.

    - asks_volume:
        The asks volume prices of the assets.

    >>> from crypto_screening.collect.orderbook import assets_orderbook_market_state
    >>>
    >>> state = assets_orderbook_market_state(...)
    """

    bids: AssetsPrices
    asks: AssetsPrices
    bids_volume: AssetsPrices
    asks_volume: AssetsPrices

    def bid(
            self, exchange: str, symbol: str, separator: Optional[str] = None
    ) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the bid price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its bid price.
        :param separator: The separator of the assets.

        :return: The bid price for the symbol.
        """

        return assets_market_prices(
            exchange=exchange, symbol=symbol, prices=self.bids,
            separator=separator, provider=self
        )
    # end bid

    def ask(
            self, exchange: str, symbol: str, separator: Optional[str] = None
    ) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.
        :param separator: The separator of the assets.

        :return: The ask price for the symbol.
        """

        return assets_market_prices(
            exchange=exchange, symbol=symbol, prices=self.asks,
            separator=separator, provider=self
        )
    # end ask

    def bid_volume(
            self, exchange: str, symbol: str, separator: Optional[str] = None
    ) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the bid price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its bid price.
        :param separator: The separator of the assets.

        :return: The bid price for the symbol.
        """

        return assets_market_prices(
            exchange=exchange, symbol=symbol, prices=self.bids_volume,
            separator=separator, provider=self
        )
    # end bid_volume

    def ask_volume(
            self, exchange: str, symbol: str, separator: Optional[str] = None
    ) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.
        :param separator: The separator of the assets.

        :return: The ask price for the symbol.
        """

        return assets_market_prices(
            exchange=exchange, symbol=symbol, prices=self.asks_volume,
            separator=separator, provider=self
        )
    # end ask_volume

    def in_bids_prices(
            self,
            exchange: str,
            symbol: str,
            separator: Optional[str] = None
    ) -> bool:
        """
        Checks if the symbol is in the prices' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.
        :param separator: The separator of the assets.

        :return: The validation value.
        """

        return is_symbol_in_assets_market_prices(
            exchange=exchange, symbol=symbol,
            separator=separator, prices=self.bids
        )
    # end in_bids_prices

    def in_asks_prices(
            self,
            exchange: str,
            symbol: str,
            separator: Optional[str] = None
    ) -> bool:
        """
        Checks if the symbol is in the prices' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.
        :param separator: The separator of the assets.

        :return: The validation value.
        """

        return is_symbol_in_assets_market_prices(
            exchange=exchange, symbol=symbol,
            separator=separator, prices=self.asks
        )
    # end in_asks_prices

    def in_bids_volume_prices(
            self,
            exchange: str,
            symbol: str,
            separator: Optional[str] = None
    ) -> bool:
        """
        Checks if the symbol is in the prices' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.
        :param separator: The separator of the assets.

        :return: The validation value.
        """

        return is_symbol_in_assets_market_prices(
            exchange=exchange, symbol=symbol,
            separator=separator, prices=self.bids_volume
        )
    # end in_bids_volume_prices

    def in_asks_volume_prices(
            self,
            exchange: str,
            symbol: str,
            separator: Optional[str] = None
    ) -> bool:
        """
        Checks if the symbol is in the prices' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.
        :param separator: The separator of the assets.

        :return: The validation value.
        """

        return is_symbol_in_assets_market_prices(
            exchange=exchange, symbol=symbol,
            separator=separator, prices=self.asks_volume
        )
    # end in_asks_volume_prices

    def data(self) -> AssetsMarketData:
        """
        Returns the structured data of the state.

        :return: The data of the state.
        """

        return assets_market_data(
            columns=ORDERBOOK_COLUMNS,
            prices={name: getattr(self, name) for name in ORDERBOOK_COLUMNS}
        )
    # end data

    def datasets(self) -> AssetsMarketDatasets:
        """
        Rebuilds the dataset from the market state.

        :return: The dataset of the state data.
        """

        datasets: AssetsMarketDatasets = {}

        for exchange, bases in self.data().items():
            for base, quotes in bases.items():
                for quote, rows in quotes.items():
                    dataset = create_orderbook_dataframe()

                    for time, row in rows:
                        dataset.loc[time] = row
                    # end for
                # end for
            # end for
        # end for

        return datasets
    # end assets_market_state_to_datasets
# end AssetsMarketStates

def assets_orderbook_market_state(
        screeners: Optional[Iterable[BaseScreener]] = None,
        separator: Optional[str] = None,
        length: Optional[int] = None,
        adjust: Optional[bool] = True
) -> AssetsOrderbookMarketState:
    """
    Fetches the prices and relations between the assets.

    :param screeners: The price screeners.
    :param separator: The separator of the assets.
    :param length: The length of the prices.
    :param adjust: The value to adjust the length of the sequences.

    :return: The prices of the assets.
    """

    return AssetsOrderbookMarketState(
        screeners=screeners,
        **assets_market_state(
            columns=ORDERBOOK_COLUMNS,
            screeners=screeners, separator=separator,
            length=length, adjust=adjust
        )
    )
# end assets_orderbook_market_state

SymbolsMarketData = Dict[str, Dict[str, List[Tuple[dt.datetime, Dict[str, float]]]]]
SymbolsMarketDatasets = Dict[str, Dict[str, pd.DataFrame]]

@define(repr=False)
@represent
class SymbolsOrderbookMarketState(OrderbookMarketBase):
    """
    A class to represent the current market state.

    This object contains the state of the market, as Close,
    bids and asks prices of specific assets, gathered from the network.

    attributes:

    - screeners:
        The screener objects to collect the prices of the assets.

    - bids:
        The bids prices of the assets.

    - asks:
        The asks prices of the assets.

    - bids_volume:
        The bids volume prices of the assets.

    - asks_volume:
        The asks volume prices of the assets.

    >>> from crypto_screening.collect.orderbook import assets_orderbook_market_state
    >>>
    >>> state = assets_orderbook_market_state(...)
    """

    bids: SymbolsPrices
    asks: SymbolsPrices
    bids_volume: SymbolsPrices
    asks_volume: SymbolsPrices

    def bid(self, exchange: str, symbol: str) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the bid price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its bid price.

        :return: The bid price for the symbol.
        """

        return symbols_market_prices(
            exchange=exchange, symbol=symbol,
            prices=self.bids, provider=self
        )
    # end bid

    def ask(self, exchange: str, symbol: str) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.

        :return: The ask price for the symbol.
        """

        return symbols_market_prices(
            exchange=exchange, symbol=symbol,
            prices=self.asks, provider=self
        )
    # end ask

    def bid_volume(self, exchange: str, symbol: str) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the bid price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its bid price.

        :return: The bid price for the symbol.
        """

        return symbols_market_prices(
            exchange=exchange, symbol=symbol,
            prices=self.bids_volume, provider=self
        )
    # end bid_volume

    def ask_volume(self, exchange: str, symbol: str) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.

        :return: The ask price for the symbol.
        """

        return symbols_market_prices(
            exchange=exchange, symbol=symbol,
            prices=self.asks_volume, provider=self
        )
    # end ask_volume

    def in_bids_prices(self, exchange: str, symbol: str) -> bool:
        """
        Checks if the symbol is in the prices' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.

        :return: The validation value.
        """

        return is_symbol_in_symbols_market_prices(
            exchange=exchange, symbol=symbol, prices=self.bids
        )
    # end in_bids_prices

    def in_asks_prices(self, exchange: str, symbol: str) -> bool:
        """
        Checks if the symbol is in the prices' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.

        :return: The validation value.
        """

        return is_symbol_in_symbols_market_prices(
            exchange=exchange, symbol=symbol, prices=self.asks
        )
    # end in_asks_prices

    def in_bids_volume_prices(self, exchange: str, symbol: str) -> bool:
        """
        Checks if the symbol is in the prices' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.

        :return: The validation value.
        """

        return is_symbol_in_symbols_market_prices(
            exchange=exchange, symbol=symbol, prices=self.bids_volume
        )
    # end in_bids_volume_prices

    def in_asks_volume_prices(self, exchange: str, symbol: str) -> bool:
        """
        Checks if the symbol is in the prices' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.

        :return: The in_asks_volume_prices value.
        """

        return is_symbol_in_symbols_market_prices(
            exchange=exchange, symbol=symbol, prices=self.asks_volume
        )
    # end in_asks_prices

    def data(self) -> SymbolsMarketData:
        """
        Returns the structured data of the state.

        :return: The data of the state.
        """

        return symbols_market_data(
            columns=ORDERBOOK_COLUMNS,
            prices={name: getattr(self, name) for name in ORDERBOOK_COLUMNS}
        )
    # end data

    def datasets(self) -> SymbolsMarketDatasets:
        """
        Rebuilds the dataset from the market state.

        :return: The dataset of the state data.
        """

        datasets: SymbolsMarketDatasets = {}

        for exchange, symbols in self.data().items():
            for symbol, rows in symbols.items():
                dataset = create_orderbook_dataframe()

                for time, row in rows:
                    dataset.loc[time] = row
                # end for
            # end for
        # end for

        return datasets
    # end symbols_market_state_to_datasets
# end SymbolsMarketStates

def symbols_orderbook_market_state(
        screeners: Optional[Iterable[BaseScreener]] = None,
        length: Optional[int] = None,
        adjust: Optional[bool] = True
) -> SymbolsOrderbookMarketState:
    """
    Fetches the prices and relations between the assets.

    :param screeners: The price screeners.
    :param length: The length of the prices.
    :param adjust: The value to adjust the length of the sequences.

    :return: The prices of the assets.
    """

    return SymbolsOrderbookMarketState(
        screeners=screeners,
        **symbols_market_state(
            columns=ORDERBOOK_COLUMNS, screeners=screeners,
            length=length, adjust=adjust
        )
    )
# end symbols_orderbook_market_state

def merge_symbols_orderbook_market_states(
        *states: SymbolsOrderbookMarketState, sort: Optional[bool] = True
) -> SymbolsOrderbookMarketState:
    """
    Concatenates the states of the market.

    :param states: The states to concatenate.
    :param sort: The value to sort the prices by the time.

    :return: The states object.
    """

    screeners = []

    for state in states:
        screeners.extend(state.screeners)
    # end for

    return SymbolsOrderbookMarketState(
        screeners=set(screeners),
        **merge_symbols_market_states(
            *states, prices={name: {} for name in ORDERBOOK_COLUMNS}, sort=sort
        )
    )
# end merge_symbols_ohlcv_market_states

def merge_assets_orderbook_market_states(
        *states: AssetsOrderbookMarketState, sort: Optional[bool] = True
) -> AssetsOrderbookMarketState:
    """
    Concatenates the states of the market.

    :param states: The states to concatenate.
    :param sort: The value to sort the prices by the time.

    :return: The states object.
    """

    screeners = []

    for state in states:
        screeners.extend(state.screeners)
    # end for

    return AssetsOrderbookMarketState(
        screeners=set(screeners),
        **merge_assets_market_states(
            *states, prices={name: {} for name in ORDERBOOK_COLUMNS}, sort=sort
        )
    )
# end merge_assets_ohlcv_market_states

def assets_to_symbols_orderbook_market_state(
        state: AssetsOrderbookMarketState,
        separator: Optional[str] = None
) -> SymbolsOrderbookMarketState:
    """
    Converts an assets market state into a symbols market state.

    :param state: The source state.
    :param separator: The separator for the symbols.

    :return: The results state.
    """

    return SymbolsOrderbookMarketState(
        **{
            name: assets_to_symbol_market_prices(
                prices=getattr(state, name), separator=separator
            ) for name in ORDERBOOK_COLUMNS
        }
    )
# end assets_to_symbols_ohlcv_market_state

def symbols_to_assets_orderbook_market_state(
        state: SymbolsOrderbookMarketState,
        separator: Optional[str] = None
) -> AssetsOrderbookMarketState:
    """
    Converts a symbols market state into an assets market state.

    :param state: The source state.
    :param separator: The separator for the symbols.

    :return: The results state.
    """

    return AssetsOrderbookMarketState(
        **{
            name: symbol_to_assets_market_prices(
                prices=getattr(state, name), separator=separator
            ) for name in ORDERBOOK_COLUMNS
        }
    )
# end symbols_to_assets_ohlcv_market_state