# trades.py

from abc import ABCMeta
import datetime as dt
from typing import (
    Iterable, Dict, Optional, ClassVar, List, Tuple
)

from attrs import define

from represent import represent, Modifiers

import pandas as pd

from crypto_screening.market.screeners.base import BaseScreener
from crypto_screening.market.screeners.trades import (
    create_trades_dataframe
)
from crypto_screening.collect.market import (
    MarketBase, assets_market_values, assets_market_data,
    is_symbol_in_assets_market_values, symbols_market_values,
    is_symbol_in_symbols_market_values, symbols_market_data,
    assets_to_symbol_market_prices, assets_market_state,
    symbol_to_assets_market_prices, symbols_market_state,
    merge_assets_market_states, merge_symbols_market_states,
    TRADES_ATTRIBUTES
)

__all__ = [
    "symbols_trades_market_state",
    "merge_assets_trades_market_states",
    "merge_symbols_trades_market_states",
    "assets_trades_market_state",
    "AssetsTradesMarketState",
    "SymbolsTradesMarketState",
    "symbols_to_assets_trades_market_state",
    "assets_to_symbols_trades_market_state",
    "TRADES_ATTRIBUTES"
]

AssetsPrices = Dict[str, Dict[str, Dict[str, List[Tuple[dt.datetime, float]]]]]
SymbolsPrices = Dict[str, Dict[str, List[Tuple[dt.datetime, float]]]]
AssetsSides = Dict[str, Dict[str, Dict[str, List[Tuple[dt.datetime, str]]]]]
SymbolsSides = Dict[str, Dict[str, List[Tuple[dt.datetime, str]]]]

@define(repr=False)
@represent
class TradesMarketBase(MarketBase, metaclass=ABCMeta):
    """
    A class to represent the current market state.

    This object contains the state of the market, as Close,
    bids and asks values of specific assets, gathered from the network.

    attributes:

    - screeners:
        The screener objects to collect the values of the assets.
    """

    __modifiers__: ClassVar[Modifiers] = Modifiers(
        **MarketBase.__modifiers__
    )
    __modifiers__.excluded.extend(["amounts", "prices", "sides"])
# end OrderbookMarketBase

AssetsMarketData = Dict[str, Dict[str, Dict[str, List[Tuple[dt.datetime, Dict[str, float]]]]]]
AssetsMarketDatasets = Dict[str, Dict[str, Dict[str, pd.DataFrame]]]

@define(repr=False)
@represent
class AssetsTradesMarketState(TradesMarketBase):
    """
    A class to represent the current market state.

    This object contains the state of the market, as Close,
    bids and asks values of specific assets, gathered from the network.

    attributes:

    - screeners:
        The screener objects to collect the values of the assets.

    - bids:
        The bids values of the assets.

    - asks:
        The asks values of the assets.

    >>> from crypto_screening.collect.orderbook import assets_orderbook_market_state
    >>>
    >>> state = assets_orderbook_market_state(...)
    """

    amounts: AssetsPrices
    prices: AssetsPrices
    sides: AssetsSides

    def amount(
            self, exchange: str, symbol: str, separator: Optional[str] = None
    ) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the bid price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its bid price.
        :param separator: The separator of the assets.

        :return: The bid price for the symbol.
        """

        return assets_market_values(
            exchange=exchange, symbol=symbol, values=self.amounts,
            separator=separator, provider=self
        )
    # end amount

    def price(
            self, exchange: str, symbol: str, separator: Optional[str] = None
    ) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.
        :param separator: The separator of the assets.

        :return: The ask price for the symbol.
        """

        return assets_market_values(
            exchange=exchange, symbol=symbol, values=self.pricess,
            separator=separator, provider=self
        )
    # end price

    def side(
            self, exchange: str, symbol: str, separator: Optional[str] = None
    ) -> List[Tuple[dt.datetime, str]]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.
        :param separator: The separator of the assets.

        :return: The ask price for the symbol.
        """

        return assets_market_values(
            exchange=exchange, symbol=symbol, values=self.sides,
            separator=separator, provider=self
        )
    # end side

    def in_amounts_prices(
            self,
            exchange: str,
            symbol: str,
            separator: Optional[str] = None
    ) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.
        :param separator: The separator of the assets.

        :return: The validation value.
        """

        return is_symbol_in_assets_market_values(
            exchange=exchange, symbol=symbol,
            separator=separator, values=self.amounts
        )
    # end in_amounts_prices

    def in_prices_prices(
            self,
            exchange: str,
            symbol: str,
            separator: Optional[str] = None
    ) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.
        :param separator: The separator of the assets.

        :return: The validation value.
        """

        return is_symbol_in_assets_market_values(
            exchange=exchange, symbol=symbol,
            separator=separator, values=self.prices
        )
    # end in_prices_prices

    def in_sides_prices(
            self,
            exchange: str,
            symbol: str,
            separator: Optional[str] = None
    ) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.
        :param separator: The separator of the assets.

        :return: The validation value.
        """

        return is_symbol_in_assets_market_values(
            exchange=exchange, symbol=symbol,
            separator=separator, values=self.sides
        )
    # end in_sides_prices

    def data(self) -> AssetsMarketData:
        """
        Returns the structured data of the state.

        :return: The data of the state.
        """

        return assets_market_data(
            columns=TRADES_ATTRIBUTES,
            prices={name: getattr(self, name) for name in TRADES_ATTRIBUTES}
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
                    dataset = create_trades_dataframe()

                    for time, row in rows:
                        dataset.loc[time] = row
                    # end for
                # end for
            # end for
        # end for

        return datasets
    # end assets_market_state_to_datasets
# end AssetsMarketStates

def assets_trades_market_state(
        screeners: Optional[Iterable[BaseScreener]] = None,
        separator: Optional[str] = None,
        length: Optional[int] = None,
        adjust: Optional[bool] = True
) -> AssetsTradesMarketState:
    """
    Fetches the values and relations between the assets.

    :param screeners: The price screeners.
    :param separator: The separator of the assets.
    :param length: The length of the values.
    :param adjust: The value to adjust the length of the sequences.

    :return: The values of the assets.
    """

    return AssetsTradesMarketState(
        screeners=screeners,
        **assets_market_state(
            columns=TRADES_ATTRIBUTES,
            screeners=screeners, separator=separator,
            length=length, adjust=adjust
        )
    )
# end assets_orders_market_state

SymbolsMarketData = Dict[str, Dict[str, List[Tuple[dt.datetime, Dict[str, float]]]]]
SymbolsMarketDatasets = Dict[str, Dict[str, pd.DataFrame]]

@define(repr=False)
@represent
class SymbolsTradesMarketState(TradesMarketBase):
    """
    A class to represent the current market state.

    This object contains the state of the market, as Close,
    bids and asks values of specific assets, gathered from the network.

    attributes:

    - screeners:
        The screener objects to collect the values of the assets.

    - bids:
        The bids values of the assets.

    - asks:
        The asks values of the assets.

    - bids_volume:
        The bids volume values of the assets.

    - asks_volume:
        The asks volume values of the assets.

    >>> from crypto_screening.collect.orderbook import assets_orderbook_market_state
    >>>
    >>> state = assets_orderbook_market_state(...)
    """

    amounts: SymbolsPrices
    prices: SymbolsPrices
    sides: SymbolsSides

    def amount(self, exchange: str, symbol: str) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.

        :return: The ask price for the symbol.
        """

        return symbols_market_values(
            exchange=exchange, symbol=symbol, values=self.amounts,
            provider=self
        )
    # end amount

    def price(self, exchange: str, symbol: str) -> List[Tuple[dt.datetime, float]]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.

        :return: The ask price for the symbol.
        """

        return symbols_market_values(
            exchange=exchange, symbol=symbol, values=self.pricess,
            provider=self
        )
    # end price

    def side(self, exchange: str, symbol: str) -> List[Tuple[dt.datetime, str]]:
        """
        Returns the ask price for the symbol.

        :param exchange: The exchange name.
        :param symbol: The symbol to find its ask price.

        :return: The ask price for the symbol.
        """

        return symbols_market_values(
            exchange=exchange, symbol=symbol,
            values=self.sides, provider=self
        )
    # end side

    def in_amounts_prices(self, exchange: str, symbol: str) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.

        :return: The validation value.
        """

        return is_symbol_in_symbols_market_values(
            exchange=exchange, symbol=symbol, values=self.amounts
        )
    # end in_amounts_prices

    def in_prices_prices(self, exchange: str, symbol: str) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.

        :return: The validation value.
        """

        return is_symbol_in_symbols_market_values(
            exchange=exchange, symbol=symbol, values=self.prices
        )
    # end in_prices_prices

    def in_sides_prices(self, exchange: str, symbol: str) -> bool:
        """
        Checks if the symbol is in the values' data.

        :param exchange: The exchange name.
        :param symbol: The symbol to search.

        :return: The validation value.
        """

        return is_symbol_in_symbols_market_values(
            exchange=exchange, symbol=symbol, values=self.sides
        )
    # end in_sides_prices

    def data(self) -> SymbolsMarketData:
        """
        Returns the structured data of the state.

        :return: The data of the state.
        """

        return symbols_market_data(
            columns=TRADES_ATTRIBUTES,
            prices={name: getattr(self, name) for name in TRADES_ATTRIBUTES}
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
                dataset = create_trades_dataframe()

                for time, row in rows:
                    dataset.loc[time] = row
                # end for
            # end for
        # end for

        return datasets
    # end symbols_market_state_to_datasets
# end SymbolsMarketStates

def symbols_trades_market_state(
        screeners: Optional[Iterable[BaseScreener]] = None,
        length: Optional[int] = None,
        adjust: Optional[bool] = True
) -> SymbolsTradesMarketState:
    """
    Fetches the values and relations between the assets.

    :param screeners: The price screeners.
    :param length: The length of the values.
    :param adjust: The value to adjust the length of the sequences.

    :return: The values of the assets.
    """

    return SymbolsTradesMarketState(
        screeners=screeners,
        **symbols_market_state(
            columns=TRADES_ATTRIBUTES, screeners=screeners,
            length=length, adjust=adjust
        )
    )
# end symbols_orders_market_state

def merge_symbols_trades_market_states(
        *states: SymbolsTradesMarketState, sort: Optional[bool] = True
) -> SymbolsTradesMarketState:
    """
    Concatenates the states of the market.

    :param states: The states to concatenate.
    :param sort: The value to sort the values by the time.

    :return: The states object.
    """

    screeners = []

    for state in states:
        screeners.extend(state.screeners)
    # end for

    return SymbolsTradesMarketState(
        screeners=set(screeners),
        **merge_symbols_market_states(
            *states, prices={name: {} for name in TRADES_ATTRIBUTES}, sort=sort
        )
    )
# end merge_symbols_orders_market_states

def merge_assets_trades_market_states(
        *states: AssetsTradesMarketState, sort: Optional[bool] = True
) -> AssetsTradesMarketState:
    """
    Concatenates the states of the market.

    :param states: The states to concatenate.
    :param sort: The value to sort the values by the time.

    :return: The states object.
    """

    screeners = []

    for state in states:
        screeners.extend(state.screeners)
    # end for

    return AssetsTradesMarketState(
        screeners=set(screeners),
        **merge_assets_market_states(
            *states, prices={name: {} for name in TRADES_ATTRIBUTES}, sort=sort
        )
    )
# end merge_assets_orders_market_states

def assets_to_symbols_trades_market_state(
        state: AssetsTradesMarketState,
        separator: Optional[str] = None
) -> SymbolsTradesMarketState:
    """
    Converts an assets market state into a symbols market state.

    :param state: The source state.
    :param separator: The separator for the symbols.

    :return: The results state.
    """

    return SymbolsTradesMarketState(
        **{
            name: assets_to_symbol_market_prices(
                prices=getattr(state, name), separator=separator
            ) for name in TRADES_ATTRIBUTES
        }
    )
# end assets_to_symbols_orders_market_state

def symbols_to_assets_trades_market_state(
        state: SymbolsTradesMarketState,
        separator: Optional[str] = None
) -> AssetsTradesMarketState:
    """
    Converts a symbols market state into an assets market state.

    :param state: The source state.
    :param separator: The separator for the symbols.

    :return: The results state.
    """

    return AssetsTradesMarketState(
        **{
            name: symbol_to_assets_market_prices(
                prices=getattr(state, name), separator=separator
            ) for name in TRADES_ATTRIBUTES
        }
    )
# end symbols_to_assets_orders_market_state