# market.py

from abc import ABCMeta
import datetime as dt
from typing import (
    Iterable, Dict, Optional, Union,
    Any, ClassVar, List, Tuple, TypeVar, Type
)

from attrs import define

from represent import represent, Modifiers

import numpy as np
import pandas as pd

from crypto_screening.dataset import (
    BIDS, ASKS, BIDS_VOLUME, ASKS_VOLUME, bid_ask_to_ohlcv,
    OPEN, HIGH, LOW, CLOSE, VOLUME, AMOUNT, SIDE, PRICE
)
from crypto_screening.market.screeners.base import BaseScreener
from crypto_screening.market.screeners.orderbook import OrderbookScreener
from crypto_screening.market.screeners.ohlcv import OHLCVScreener
from crypto_screening.dataset import dataset_to_json
from crypto_screening.symbols import symbol_to_parts, parts_to_symbol
from crypto_screening.collect.screeners import (
    find_screeners, screeners_to_assets_datasets,
    screeners_to_symbols_datasets
)

__all__ = [
    "validate_assets_market_state_values_symbol",
    "assets_market_value",
    "is_symbol_in_assets_market_values",
    "symbols_market_values",
    "symbols_market_value",
    "assets_market_values",
    "validate_symbols_market_state_values_symbol",
    "is_exchange_in_market_data",
    "is_symbol_in_symbols_market_values",
    "symbol_to_assets_market_prices",
    "assets_to_symbol_market_prices",
    "assets_to_symbols_market_datasets",
    "symbols_to_assets_market_datasets",
    "symbols_screeners",
    "symbols_market_datasets_to_symbols_screeners",
    "assets_screeners",
    "assets_market_datasets_to_assets_screeners",
    "assets_to_symbols_market_data",
    "add_symbols_data_to_screeners",
    "add_assets_data_to_screeners",
    "symbols_to_assets_market_data",
    "merge_symbols_market_data",
    "merge_assets_market_data",
    "dataset_to_data",
    "symbols_datasets_to_symbols_data",
    "assets_datasets_to_assets_data",
    "screeners_to_symbols_data",
    "screeners_to_assets_data",
    "MarketBase",
    "assets_market_data",
    "symbols_market_data",
    "assets_market_state",
    "symbols_market_state",
    "merge_assets_market_states",
    "merge_symbols_market_states",
    "ORDERBOOK_ATTRIBUTES",
    "assets_to_symbols_screeners",
    "symbols_to_assets_screeners",
    "OHLCV_ATTRIBUTES",
    "ORDERS_ATTRIBUTES",
    "TRADES_ATTRIBUTES"
]

_V = TypeVar("_V")

AssetsData = Dict[str, Dict[str, Dict[str, List[Tuple[dt.datetime, _V]]]]]
SymbolsData = Dict[str, Dict[str, List[Tuple[dt.datetime, _V]]]]

def is_exchange_in_market_data(
        exchange: str,
        values: Union[AssetsData, SymbolsData]
) -> None:
    """
    Checks if the exchange is in the values.

    :param exchange: The exchange name.
    :param values: The values.

    :return: The boolean flag.
    """

    return exchange not in values
# end is_exchange_in_market_prices

def is_symbol_in_assets_market_values(
        exchange: str,
        symbol: str,
        values: AssetsData,
        separator: Optional[str] = None
) -> bool:
    """
    Checks if the symbol is in the values' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param values: The price data to process.
    :param separator: The separator of the assets.

    :return: The validation value.
    """

    if not is_exchange_in_market_data(exchange=exchange, values=values):
        return False
    # end if

    base, quote = symbol_to_parts(symbol=symbol, separator=separator)

    if base not in values[exchange]:
        return False
    # end if

    if quote not in values[exchange][base]:
        return False
    # end if

    return not np.isnan(values[exchange][base][quote])
# end is_symbol_in_assets_market_prices

def is_symbol_in_symbols_market_values(
        exchange: str,
        symbol: str,
        values: SymbolsData
) -> bool:
    """
    Checks if the symbol is in the values' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param values: The price data to process.

    :return: The validation value.
    """

    if not is_exchange_in_market_data(exchange=exchange, values=values):
        return False
    # end if

    if symbol not in values[exchange]:
        return False
    # end if

    return not np.isnan(values[exchange][symbol])
# end is_symbol_in_assets_market_prices

def validate_assets_market_state_values_symbol(
        exchange: str,
        symbol: str,
        values: AssetsData,
        separator: Optional[str] = None,
        provider: Optional[Any] = None
) -> None:
    """
    Checks if the symbol is in the values' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param separator: The separator of the assets.
    :param values: The price data to process.
    :param provider: The data provider.

    :return: The validation value.
    """

    base, quote = symbol_to_parts(symbol=symbol, separator=separator)

    if exchange not in values:
        raise ValueError(
            f"exchange '{exchange}' is not found inside the values of"
            f"{f' of {provider}' if provider is not None else ''}. "
            f"Found exchanges for are: {', '.join(values.keys())}"
        )
    # end if

    if base not in values[exchange]:
        raise ValueError(
            f"base asset '{base}' is not found in '{exchange}' values of"
            f"{f' of {provider}' if provider is not None else ''}. "
            f"Found base '{exchange}' assets are: "
            f"{', '.join(values[exchange].keys())}"
        )
    # end if

    if quote not in values[exchange][base]:
        raise ValueError(
            f"quote asset '{quote}' is not found in the quote "
            f"assets of the '{base}' base asset in the values"
            f"{f' of {provider}' if provider is not None else ''}. "
            f"Found quote assets for the '{base}' base asset in "
            f"the values are: {', '.join(values[exchange][base].keys())}"
        )
    # end if
# end validate_assets_market_state_prices_symbol

def validate_symbols_market_state_values_symbol(
        exchange: str,
        symbol: str,
        values: SymbolsData,
        provider: Optional[Any] = None
) -> None:
    """
    Checks if the symbol is in the values' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param values: The price data to process.
    :param provider: The data provider.

    :return: The validation value.
    """

    if exchange not in values:
        raise ValueError(
            f"exchange '{exchange}' is not found inside the values of"
            f"{f' of {provider}' if provider is not None else ''}. "
            f"Found exchanges for are: {', '.join(values.keys())}"
        )
    # end if

    if symbol not in values[exchange]:
        raise ValueError(
            f"symbol '{symbol}' is not found in '{exchange}' values of"
            f"{f' of {provider}' if provider is not None else ''}. "
            f"Found symbols for '{exchange}' values are: "
            f"{', '.join(values[exchange].keys())}"
        )
    # end if
# end validate_symbols_market_state_prices_symbol

def assets_market_value(
        exchange: str,
        symbol: str,
        values: AssetsData,
        separator: Optional[str] = None,
        provider: Optional[Any] = None
) -> Tuple[dt.datetime, _V]:
    """
    Checks if the symbol is in the values' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param separator: The separator of the assets.
    :param values: The price data to process.
    :param provider: The data provider.

    :return: The validation value.
    """

    validate_assets_market_state_values_symbol(
        symbol=symbol, values=values, exchange=exchange,
        separator=separator, provider=provider
    )

    base, quote = symbol_to_parts(symbol=symbol, separator=separator)

    data = list(values[exchange][base][quote])

    return data[-1][0], data[-1][-1]
# end assets_market_price

def symbols_market_value(
        exchange: str,
        symbol: str,
        values: SymbolsData,
        provider: Optional[Any] = None
) -> Tuple[dt.datetime, _V]:
    """
    Checks if the symbol is in the values' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param values: The price data to process.
    :param provider: The data provider.

    :return: The validation value.
    """

    validate_symbols_market_state_values_symbol(
        exchange=exchange, symbol=symbol,
        values=values, provider=provider
    )

    data = list(values[exchange][symbol])

    return data[-1][0], data[-1][-1]
# end symbols_market_price

def symbols_market_values(
        exchange: str,
        symbol: str,
        values: SymbolsData,
        provider: Optional[Any] = None
) -> List[Tuple[dt.datetime, _V]]:
    """
    Checks if the symbol is in the values' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param values: The price data to process.
    :param provider: The data provider.

    :return: The validation value.
    """

    validate_symbols_market_state_values_symbol(
        exchange=exchange, symbol=symbol,
        values=values, provider=provider
    )

    return values[exchange][symbol]
# end symbols_market_prices

def assets_market_values(
        exchange: str,
        symbol: str,
        values: AssetsData,
        separator: Optional[str] = None,
        provider: Optional[Any] = None
) -> List[Tuple[dt.datetime, _V]]:
    """
    Checks if the symbol is in the values' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param separator: The separator of the assets.
    :param values: The price data to process.
    :param provider: The data provider.

    :return: The validation value.
    """

    validate_assets_market_state_values_symbol(
        symbol=symbol, values=values, exchange=exchange,
        separator=separator, provider=provider
    )

    base, quote = symbol_to_parts(symbol=symbol, separator=separator)

    return values[exchange][base][quote]
# end assets_market_prices

@define(repr=False)
@represent
class MarketBase(metaclass=ABCMeta):
    """
    A class to represent the current market state.

    This object contains the state of the market, as Close,
    bids and asks values of specific assets, gathered from the network.

    attributes:

    - screeners:
        The screener objects to collect the values of the assets.
    """

    screeners: Iterable[BaseScreener]

    __modifiers__: ClassVar[Modifiers] = Modifiers(excluded=["screeners"])

    def __hash__(self) -> int:
        """
        Returns the hash of the object.

        :return: The hash of the object.
        """

        return id(self)
    # end __hash__
# end OrderbookMarketBase

AssetsMarketData = Dict[str, Dict[str, Dict[str, List[Tuple[dt.datetime, Dict[str, float]]]]]]
AssetsMarketDatasets = Dict[str, Dict[str, Dict[str, pd.DataFrame]]]

SymbolsMarketData = Dict[str, Dict[str, List[Tuple[dt.datetime, Dict[str, float]]]]]
SymbolsMarketDatasets = Dict[str, Dict[str, pd.DataFrame]]

def dataset_to_data(dataset: pd.DataFrame) -> List[Tuple[dt.datetime, Dict[str, Any]]]:
    """
    Converts the dataset into the data of the rows.

    :param dataset: The dataset.

    :return: The data structure.
    """

    data = dataset_to_json(dataset)

    return [
        (index, value)
        for index, (_, value) in zip(dataset.index, data)
    ]
# end dataset_to_data

def symbols_datasets_to_symbols_data(
        datasets: Dict[str, Dict[str, pd.DataFrame]]
) -> SymbolsMarketData:
    """
    Converts the datasets structure to the structure of the data rows.

    :param datasets: The datasets to convert.

    :return: The new data.
    """

    return {
        exchange: {
            symbol: dataset_to_data(dataset=dataset)
            for symbol, dataset in symbols.items()
        } for exchange, symbols in datasets.items()
    }
# end symbols_datasets_to_symbols_data

def assets_datasets_to_assets_data(
        datasets: Dict[str, Dict[str, Dict[str, pd.DataFrame]]]
) -> AssetsMarketData:
    """
    Converts the datasets structure to the structure of the data rows.

    :param datasets: The datasets to convert.

    :return: The new data.
    """

    return {
        exchange: {
            base: {
                quote: dataset_to_data(dataset=dataset)
                for quote, dataset in quotes.items()
            } for base, quotes in bases.items()
        } for exchange, bases in datasets.items()
    }
# end assets_datasets_to_assets_data

def screeners_to_assets_data(
        screeners: Iterable[BaseScreener],
        separator: Optional[str] = None
) -> AssetsMarketData:
    """
    Converts the datasets structure to the structure of the data rows.

    :param screeners: The screeners to process.
    :param separator: The separator for the symbols.

    :return: The new data.
    """

    return assets_datasets_to_assets_data(
        screeners_to_assets_datasets(
            screeners=screeners, separator=separator
        )
    )
# end screeners_to_assets_data

def screeners_to_symbols_data(screeners: Iterable[BaseScreener]) -> SymbolsMarketData:
    """
    Converts the datasets structure to the structure of the data rows.

    :param screeners: The screeners to process.

    :return: The new data.
    """

    return symbols_datasets_to_symbols_data(
        screeners_to_symbols_datasets(screeners=screeners)
    )
# end screeners_to_symbols_data

def merge_symbols_market_data(
        *data: SymbolsMarketData, sort: Optional[bool] = True
) -> SymbolsMarketData:
    """
    Concatenates the states of the market.

    :param data: The states to concatenate.
    :param sort: The value to sort the values by the time.

    :return: The states object.
    """

    new_data: SymbolsMarketData = {}

    for data_packet in data:
        for exchange, symbols in data_packet.items():
            for symbol, prices in symbols.items():
                (
                    new_data.setdefault(exchange, {}).
                    setdefault(symbol, []).
                    extend(prices)
                )
            # end for
        # end for
    # end for

    if sort:
        for exchange, symbols in new_data.items():
            for symbol, prices in symbols.items():
                prices.sort(key=lambda pair: pair[0])
            # end for
        # end for
    # end if

    return new_data
# end merge_symbols_ohlcv_market_states

def merge_assets_market_data(
        *data: AssetsMarketData, sort: Optional[bool] = True
) -> AssetsMarketData:
    """
    Concatenates the states of the market.

    :param data: The states to concatenate.
    :param sort: The value to sort the values by the time.

    :return: The states object.
    """

    new_data: AssetsMarketData = {}

    for data_packet in data:
        for exchange, bases in data_packet.items():
            for base, quotes in bases.items():
                for quote, prices in quotes.items():
                    (
                        new_data.setdefault(exchange, {}).
                        setdefault(base, {}).
                        setdefault(quote, []).
                        extend(prices)
                    )
                # end for
        # end for
    # end for

    if sort:
        for exchange, bases in new_data.items():
            for base, quotes in bases.items():
                for quote, prices in quotes.items():
                    prices.sort(key=lambda pair: pair[0])
                # end for
            # end for
        # end for
    # end if

    return new_data
# end merge_assets_ohlcv_market_states

def symbols_to_assets_market_datasets(
        datasets: SymbolsMarketDatasets, separator: Optional[str] = None
) -> AssetsMarketDatasets:
    """
    Converts the datasets structure from symbols to assets.

    :param datasets: The datasets to convert.
    :param separator: The separator for the symbols.

    :return: The result structure.
    """

    assets_datasets: AssetsMarketDatasets = {}

    for exchange, symbols in datasets.items():
        for symbol, dataset in symbols.items():
            base, quote = symbol_to_parts(symbol, separator=separator)
            (
                assets_datasets.
                setdefault(exchange, {}).
                setdefault(base, {}).
                setdefault(quote, dataset)
            )
        # end for
    # end for

    return assets_datasets
# end symbols_to_assets_market_datasets

def assets_to_symbols_market_datasets(
        datasets: AssetsMarketDatasets, separator: Optional[str] = None
) -> SymbolsMarketDatasets:
    """
    Converts the datasets structure from assets to symbols.

    :param datasets: The datasets to convert.
    :param separator: The separator for the symbols.

    :return: The result structure.
    """

    symbols_datasets: SymbolsMarketDatasets = {}

    for exchange, bases in datasets.items():
        for base, quotes in bases.items():
            for quote, dataset in quotes.items():
                symbol = parts_to_symbol(base, quote, separator=separator)
                (
                    symbols_datasets.
                    setdefault(exchange, {}).
                    setdefault(symbol, dataset)
                )
        # end for
    # end for

    return symbols_datasets
# end assets_to_symbols_market_datasets

def assets_to_symbol_market_prices(
        prices: AssetsData, separator: Optional[str] = None
) -> SymbolsData:
    """
    Converts an assets market values into a symbols market values.

    :param prices: The source values.
    :param separator: The separator for the symbols.

    :return: The result values.
    """

    symbols_prices: SymbolsData = {}

    for exchange, bases in prices.items():
        for base, quotes in bases.items():
            for quote, data in quotes.items():
                for time, price in data:
                    (
                        symbols_prices.
                        setdefault(exchange, {}).
                        setdefault(
                            parts_to_symbol(base, quote, separator=separator)
                        )
                    ).append((time, price))
                # end for
            # end for
        # end for
    # end for

    return symbols_prices
# end assets_to_symbol_market_prices

def symbol_to_assets_market_prices(
        prices: SymbolsData, separator: Optional[str] = None
) -> AssetsData:
    """
    Converts a symbols market values into an assets market values.

    :param prices: The source values.
    :param separator: The separator for the symbols.

    :return: The result values.
    """

    assets_prices: AssetsData = {}

    for exchange, symbols in prices.items():
        for symbol, data in symbols.items():
            base, quote = symbol_to_parts(symbol, separator=separator)

            for time, price in data:
                (
                    assets_prices.
                    setdefault(exchange, {}).
                    setdefault(base, {}).
                    setdefault(quote, [])
                ).append((time, price))
            # end for
        # end for
    # end for

    return assets_prices
# end symbol_to_assets_market_prices

def assets_to_symbols_market_data(
        data: AssetsMarketData,
        separator: Optional[str] = None
) -> SymbolsMarketData:
    """
    Converts the structure of the market data from assets to symbols.

    :param data: The data to convert.
    :param separator: The separator for the symbols.

    :return: The data in the new structure
    """

    symbols_data: SymbolsMarketData = {}

    for exchange, bases in data.items():
        for base, quotes in bases.items():
            for quote, data in quotes.items():
                symbol = parts_to_symbol(base, quote, separator=separator)

                (
                    symbols_data.
                    setdefault(exchange, {}).
                    setdefault(symbol, data)
                )
            # end for
    # end for

    return symbols_data
# end assets_to_symbols_market_data

def symbols_to_assets_market_data(
        data: SymbolsMarketData,
        separator: Optional[str] = None
) -> AssetsMarketData:
    """
    Converts the structure of the market data from assets to symbols.

    :param data: The data to convert.
    :param separator: The separator for the symbols.

    :return: The data in the new structure
    """

    assets_data: AssetsMarketData = {}

    for exchange, symbols in data.items():
        for symbol, data in symbols.items():
            base, quote = symbol_to_parts(symbol, separator=separator)

            (
                assets_data.
                setdefault(exchange, {}).
                setdefault(base, {}).
                setdefault(quote, data)
            )
            # end for
        # end for
    # end for

    return assets_data
# end assets_to_symbols_market_data

_S = TypeVar("_S", BaseScreener, OrderbookScreener)

AssetsScreeners = Dict[str, Dict[str, Dict[str, Union[BaseScreener, _S]]]]

ORDERBOOK_ATTRIBUTES = {
    "bids": BIDS,
    "asks": ASKS,
    "bids_volume": BIDS_VOLUME,
    "asks_volume": ASKS_VOLUME
}
OHLCV_ATTRIBUTES = {
    "open": OPEN,
    "high": HIGH,
    "low": LOW,
    "close": CLOSE,
    "volume": VOLUME
}
ORDERS_ATTRIBUTES = {
    "bids": BIDS,
    "asks": ASKS
}
TRADES_ATTRIBUTES = {
    "amount": AMOUNT,
    "price": PRICE,
    "side": SIDE
}

def set_screener_dataset(
        screener: _S,
        dataset: pd.DataFrame,
        clean: Optional[bool] = False,
        replace: Optional[bool] = False
) -> None:
    """
    Sets the dataset for the screener, and return the screener.

    :param dataset: The dataset to insert to the screener.
    :param screener: The screener object.
    :param clean: The value to clean the dataset.
    :param replace: The value to replace the dataset.

    :return: The screener object.
    """

    if (
        isinstance(screener, OHLCVScreener) and
        (set(dataset.columns) == set(ORDERBOOK_ATTRIBUTES.values()))
    ):
        spread_dataset = dataset

        if (screener.base_market is not None) and clean:
            screener.base_market.drop(screener.base_market.index, inplace=True)
        # end if

        if (screener.base_market is None) or replace:
            screener.base_market = spread_dataset

        else:
            for index, row in spread_dataset.iterrows():
                screener.base_market[index] = row
            # end for
        # end if

        if (screener.market is not None) and clean:
            screener.market.drop(screener.market.index, inplace=True)
        # end if

        ohlcv_dataset = bid_ask_to_ohlcv(spread_dataset, interval=screener.interval)

        if (screener.market is None) or replace:
            screener.market = ohlcv_dataset

        else:
            for index, row in ohlcv_dataset:
                screener.market[index] = row
            # end for
        # end if

    elif (
        isinstance(screener, OrderbookScreener) and
        (set(dataset.columns) != set(ORDERBOOK_ATTRIBUTES.values()))
    ):
        raise ValueError(
            f"Unable to set dataset with columns: "
            f"{dataset.columns} to {type(screener)} object of "
            f"'{screener.exchange}' and symbol '{screener.symbol}' to update its data. "
            f"Consider setting the 'adjust' parameter to True, ignore."
        )

    else:
        if (screener.market is not None) and clean:
            screener.market.drop(screener.market.index, inplace=True)
        # end if

        if (screener.market is None) or replace:
            screener.market = dataset

        else:
            for index, row in dataset:
                screener.market[index] = row
            # end for
        # end if
    # end if
# end set_screener_dataset

def assets_market_datasets_to_assets_screeners(
        datasets: AssetsMarketDatasets,
        adjust: Optional[bool] = True,
        base: Optional[Type[_S]] = None,
        screeners: Optional[Iterable[_S]] = None,
        separator: Optional[str] = None
) -> AssetsScreeners:
    """
    Builds the screeners from the assets market datasets structure.

    :param datasets: The datasets for the screeners.
    :param adjust: The value to adjust the data.
    :param base: The base type for a screener.
    :param screeners: screeners to insert datasets into.
    :param separator: The separator for the symbols.

    :return: The screeners.
    """

    return symbols_to_assets_screeners(
        screeners=symbols_market_datasets_to_symbols_screeners(
            datasets=assets_to_symbols_market_datasets(
                datasets=datasets, separator=separator
            ), adjust=adjust, base=base, screeners=screeners
        ), separator=separator
    )
# end assets_market_datasets_to_assets_screeners

SymbolsScreeners = Dict[str, Dict[str, Union[BaseScreener, _S]]]

def symbols_market_datasets_to_symbols_screeners(
        datasets: SymbolsMarketDatasets,
        adjust: Optional[bool] = True,
        base: Optional[Type[_S]] = None,
        screeners: Optional[Iterable[_S]] = None
) -> SymbolsScreeners:
    """
    Builds the screeners from the assets market datasets structure.

    :param datasets: The datasets for the screeners.
    :param adjust: The value to adjust the data.
    :param base: The base type for a screener.
    :param screeners: screeners to insert datasets into.

    :return: The screeners.
    """

    if screeners is None:
        screeners = []
    # end if

    screener_base = base or OHLCVScreener

    new_screeners: SymbolsScreeners = {}

    for exchange, symbols in datasets.items():
        for symbol, dataset in symbols.items():
            try:
                found_screeners = find_screeners(
                    screeners, exchange=exchange, symbol=symbol
                )

            except IndexError:
                found_screeners = [
                    screener_base(symbol=symbol, exchange=exchange)
                ]
            # end try

            for screener in found_screeners:
                try:
                    set_screener_dataset(screener=screener, dataset=dataset)

                except ValueError as e:
                    if adjust:
                        continue

                    else:
                        raise e
                    # end if
                # end try

                (
                    new_screeners.setdefault(exchange, {}).
                    setdefault(symbol, screener)
                )
            # end for
        # end for
    # end for

    return new_screeners
# end symbols_market_datasets_to_symbols_screeners

def assets_screeners(screeners: AssetsScreeners) -> List[Union[BaseScreener, _S]]:
    """
    Collects the screeners from the assets screeners structure.

    :param screeners: The screeners structure.

    :return: The screeners' collection.
    """

    screeners_collection = []

    for exchange, bases in screeners.items():
        for base, quotes in bases.items():
            for quote, screener in quotes.items():
                screeners_collection.append(screener)
            # end for
        # end for
    # end for

    return screeners_collection
# end assets_screeners

def symbols_to_assets_screeners(
        screeners: SymbolsScreeners,
        separator: Optional[str] = None
) -> AssetsScreeners:
    """
    Collects the screeners from the assets screeners structure.

    :param screeners: The screeners structure.
    :param separator: The separator for the symbols.

    :return: The screeners' collection.
    """

    data: AssetsScreeners = {}

    for exchange, symbols in screeners.items():
        for symbol, screener in symbols.items():
            base, quote = symbol_to_parts(symbol, separator=separator)
            (
                data.
                setdefault(exchange, {}).
                setdefault(base, {}).
                setdefault(quote, screener)
            )
            # end for
        # end for
    # end for

    return data
# end assets_screeners

def assets_to_symbols_screeners(
        screeners: AssetsScreeners,
        separator: Optional[str] = None
) -> SymbolsScreeners:
    """
    Collects the screeners from the assets screeners structure.

    :param screeners: The screeners structure.
    :param separator: The separator for the symbols.

    :return: The screeners' collection.
    """

    data: SymbolsScreeners = {}

    for exchange, bases in screeners.items():
        for base, quotes in bases.items():
            for quote, screener in quotes.items():
                (
                    data.
                    setdefault(exchange, {}).
                    setdefault(
                        parts_to_symbol(base, quote, separator=separator),
                        screener
                    )
                )
            # end for
        # end for
    # end for

    return data
# end assets_screeners

def symbols_screeners(screeners: SymbolsScreeners) -> List[Union[BaseScreener, _S]]:
    """
    Collects the screeners from the symbols screeners structure.

    :param screeners: The screeners structure.

    :return: The screeners' collection.
    """

    screeners_collection = []

    for exchange, symbols in screeners.items():
        for symbol, screener in symbols.items():
            screeners_collection.append(screener)
        # end for
    # end for

    return screeners_collection
# end symbols_screeners

def add_symbols_data_to_screeners(
        screeners: Iterable[BaseScreener],
        data: SymbolsMarketData,
        adjust: Optional[bool] = True
) -> None:
    """
    Updates the data of the screeners with the symbols data.

    :param screeners: The screeners to update.
    :param data: The new data to add to the screeners.
    :param adjust: The value to adjust with screeners that are not found.
    """

    for exchange, symbols in data.items():
        for symbol, rows in symbols.items():
            found_screeners = find_screeners(
                screeners, exchange=exchange, symbol=symbol
            )

            if (not found_screeners) and (not adjust):
                raise ValueError(
                    f"Unable to find a screener with exchange "
                    f"'{exchange}' and symbol '{symbol}' to update its data. "
                    f"Consider setting the 'adjust' parameter to True, ignore."
                )
            # end if

            for screener in found_screeners:
                for index, row in rows:
                    if (
                        isinstance(screener, OHLCVScreener) and
                        (set(row.keys()) == set(ORDERBOOK_ATTRIBUTES.values()))
                    ):
                        screener.base_market.loc[index] = row

                    else:
                        screener.market.loc[index] = row
                    # end if
                # end for
            # end for
        # end for
    # end for
# end add_symbols_data_to_screeners

def add_assets_data_to_screeners(
        screeners: Iterable[BaseScreener],
        data: AssetsMarketData,
        adjust: Optional[bool] = True
) -> None:
    """
    Updates the data of the screeners with the symbols data.

    :param screeners: The screeners to update.
    :param data: The new data to add to the screeners.
    :param adjust: The value to adjust with screeners that are not found.
    """

    return add_symbols_data_to_screeners(
        screeners=screeners,
        data=assets_to_symbols_market_data(data=data),
        adjust=adjust
    )
# end add_assets_data_to_screeners

def index_to_datetime(index: Any) -> dt.datetime:
    """
    Converts the index into a datetime object.

    :param index: The value to convert.

    :return: The datetime object.
    """

    try:
        if isinstance(index, str):
            index = dt.datetime.fromisoformat(index)

        elif isinstance(index, int):
            index = dt.datetime.fromtimestamp(index)
        # end if

    except (Type, ValueError):
        pass
    # end try

    return index
# end index_to_datetime

def assets_market_data(
        columns: Dict[str, str],
        prices: Optional[Dict[str, AssetsData]] = None
) -> AssetsMarketData:
    """
    Returns the structured data of the state.

    :param prices: The values for the data collection.
    :param columns: The columns for the data.

    :return: The data of the state.
    """

    prices = prices or {name: {} for name in columns}

    datasets: Dict[str, Dict[str, Dict[str, Dict[dt.datetime, Dict[str, float]]]]] = {}

    for name in columns:
        for exchange, bases in prices[name].items():
            for base, quotes in bases.items():
                for quote, symbols_prices in quotes.items():
                    for i, (index, price) in enumerate(symbols_prices):
                        index = index_to_datetime(index)

                        (
                            datasets.
                            setdefault(exchange, {}).
                            setdefault(base, {}).
                            setdefault(quote, {}).
                            setdefault(index, {})
                        )[columns[name]] = price
                    # end for
            # end for
        # end for
    # end for

    new_datasets: AssetsMarketData = {}

    for exchange, bases in datasets.items():
        for base, quotes in bases.items():
            for quote, symbols_prices in quotes.items():
                (
                    new_datasets.
                    setdefault(exchange, {}).
                    setdefault(base, {})
                )[quote] = sorted(
                    list(symbols_prices.items()), key=lambda pair: pair[0]
                )
            # end for
        # end for
    # end for

    return new_datasets
# end assets_market_data

def symbols_market_data(
        columns: Dict[str, str],
        prices: Optional[Dict[str, SymbolsData]] = None
) -> SymbolsMarketData:
    """
    Returns the structured data of the state.

    :param prices: The values for the data collection.
    :param columns: The columns for the data.

    :return: The data of the state.
    """

    datasets: Dict[str, Dict[str, Dict[dt.datetime, Dict[str, float]]]] = {}

    for name in columns:
        for exchange, symbols in prices[name].items():
            for symbol, symbols_prices in symbols.items():
                for i, (index, price) in enumerate(symbols_prices):
                    index = index_to_datetime(index)

                    (
                        datasets.
                        setdefault(exchange, {}).
                        setdefault(symbol, {}).
                        setdefault(index, {})
                    )[columns[name]] = price
                # end for
            # end for
        # end for
    # end for

    new_datasets: SymbolsMarketData = {}

    for exchange, symbols in datasets.items():
        for symbol, symbols_prices in symbols.copy().items():
            new_datasets.setdefault(exchange, {})[symbol] = sorted(
                list(symbols_prices.items()), key=lambda pair: pair[0]
            )
        # end for
    # end for

    return new_datasets
# end symbols_market_data

def screener_dataset(
        columns: Dict[str, str], screener: BaseScreener
) -> pd.DataFrame:
    """
    Finds the minimum common length of all datasets.

    :param columns: The columns for the data.
    :param screener: The price screener.

    :return: The minimum common length.
    """

    return (
        screener.base_market
        if (
            (columns == ORDERBOOK_ATTRIBUTES) and
            isinstance(screener, OHLCVScreener)
        ) else
        screener.market
    )
# end screener_dataset

def minimum_common_dataset_length(
        columns: Dict[str, str], screeners: Iterable[BaseScreener]
) -> int:
    """
    Finds the minimum common length of all datasets.

    :param columns: The columns for the data.
    :param screeners: The price screeners.

    :return: The minimum common length.
    """

    return min(
        [
            len(screener_dataset(columns=columns, screener=screener))
            for screener in screeners
        ]
    )
# end minimum_common_dataset_length

def adjusted_dataset_length(
        dataset: pd.DataFrame,
        length: Optional[int] = None,
        adjust: Optional[bool] = True
) -> int:
    """
    Finds the minimum common length of all datasets.

    :param dataset: The price dataset.
    :param length: The base length.
    :param adjust: The value to adjust the length.

    :return: The minimum common length.
    """

    if adjust and (length is None):
        length = len(dataset)

    elif adjust:
        length = min([len(dataset), length])
        # end if

    if length > len(dataset):
        raise ValueError(
            f"Data is not long enough for the requested length: {length}. "
            f"Consider using the 'adjust' parameter as {True}, "
            f"to adjust to the actual length of the data."
        )
    # end if

    return length
# end adjusted_dataset_length

def assets_market_state(
        columns: Dict[str, str],
        screeners: Iterable[BaseScreener],
        prices: Optional[Dict[str, AssetsData]] = None,
        separator: Optional[str] = None,
        length: Optional[int] = None,
        adjust: Optional[bool] = True
) -> Dict[str, AssetsData]:
    """
    Fetches the values and relations between the assets.

    :param prices: The values for the data collection.
    :param columns: The columns for the data.
    :param screeners: The price screeners.
    :param separator: The separator of the assets.
    :param length: The length of the values.
    :param adjust: The value to adjust the length of the sequences.

    :return: The values of the assets.
    """

    prices = prices or {name: {} for name in columns}

    if (length is None) and (not adjust):
        length = minimum_common_dataset_length(
            columns=columns, screeners=screeners
        )
    # end if

    for screener in screeners:
        market = screener_dataset(columns=columns, screener=screener)

        try:
            length = adjusted_dataset_length(
                dataset=market, adjust=adjust, length=length
            )

        except ValueError as e:
            raise ValueError(
                f"Data of '{screener.exchange}' "
                f"symbol in '{screener.symbol}' exchange: {e}"
            )
        # end try

        base, quote = symbol_to_parts(
            symbol=screener.symbol, separator=separator
        )

        for name in columns:
            (
                prices[name].
                setdefault(screener.exchange, {}).
                setdefault(base, {}).
                setdefault(
                    quote,
                    list(
                        zip(
                            list(market.index[-length:]),
                            list(market[columns[name]][-length:])
                        )
                    )
                )
            )
    # end for

    return prices
# end assets_market_state

def symbols_market_state(
        columns: Dict[str, str],
        prices: Optional[Dict[str, SymbolsData]] = None,
        screeners: Optional[Iterable[BaseScreener]] = None,
        length: Optional[int] = None,
        adjust: Optional[bool] = True
) -> Dict[str, SymbolsData]:
    """
    Fetches the values and relations between the assets.

    :param prices: The values for the data collection.
    :param columns: The columns for the data.
    :param screeners: The price screeners.
    :param length: The length of the values.
    :param adjust: The value to adjust the length of the sequences.

    :return: The values of the assets.
    """

    prices = prices or {name: {} for name in columns}

    if (length is None) and (not adjust):
        length = minimum_common_dataset_length(
            columns=columns, screeners=screeners
        )
    # end if

    for screener in screeners:
        market = screener_dataset(columns=columns, screener=screener)

        try:
            length = adjusted_dataset_length(
                dataset=market, adjust=adjust, length=length
            )

        except ValueError as e:
            raise ValueError(
                f"Data of '{screener.exchange}' "
                f"symbol in '{screener.symbol}' exchange: {e}"
            )
        # end try

        for name in columns:
            (
                prices[name].
                setdefault(screener.exchange, {}).
                setdefault(
                    screener.symbol,
                    list(
                        zip(
                            list(market.index[-length:]),
                            list(market[columns[name]][-length:])
                        )
                    )
                )
            )
        # end for
    # end for

    return prices
# end symbols_market_state

def merge_assets_market_states(
        *states: MarketBase,
        prices: Dict[str, AssetsData],
        sort: Optional[bool] = True
) -> Dict[str, AssetsData]:
    """
    Concatenates the states of the market.

    :param prices: The values for the data collection.
    :param states: The states to concatenate.
    :param sort: The value to sort the values by the time.

    :return: The states object.
    """

    for state in states:
        for name in prices:
            for exchange, bases in getattr(state, name).items():
                for base, quotes in bases.items():
                    for quote, quote_prices in quotes.items():
                        (
                            prices[name].setdefault(exchange, {}).
                            setdefault(base, {}).
                            setdefault(quote, []).
                            extend(quote_prices)
                        )
                # end for
            # end for
        # end for
    # end for

    if sort:
        for prices_data in prices.values():
            for exchange, bases in prices_data.items():
                for base, quotes in bases.items():
                    for quote_prices in quotes.values():
                        quote_prices.sort(key=lambda pair: pair[0])
                    # end for
                # end for
            # end for
        # end for
    # end if

    return prices
# end merge_assets_market_states

def merge_symbols_market_states(
        *states: MarketBase,
        prices: Dict[str, SymbolsData],
        sort: Optional[bool] = True
) -> Dict[str, SymbolsData]:
    """
    Concatenates the states of the market.

    :param prices: The values for the data collection.
    :param states: The states to concatenate.
    :param sort: The value to sort the values by the time.

    :return: The states object.
    """

    for state in states:
        for name in prices:
            for exchange, symbols in getattr(state, name).items():
                for symbol, symbol_prices in symbols.items():
                    (
                        prices[name].setdefault(exchange, {}).
                        setdefault(symbol, []).
                        extend(symbol_prices)
                    )
                # end for
            # end for
        # end for
    # end for

    if sort:
        for prices_data in prices.values():
            for exchange, symbols in prices_data.items():
                for symbol_prices in symbols.values():
                    symbol_prices.sort(key=lambda pair: pair[0])
                # end for
            # end for
        # end for
    # end if

    return prices
# end merge_symbols_market_states