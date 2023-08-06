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
    BIDS, ASKS, BIDS_VOLUME, ASKS_VOLUME,
    OPEN, HIGH, LOW, CLOSE, VOLUME
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
    "validate_assets_market_state_prices_symbol",
    "assets_market_price",
    "is_symbol_in_assets_market_prices",
    "symbols_market_prices",
    "symbols_market_price",
    "assets_market_prices",
    "validate_symbols_market_state_prices_symbol",
    "is_exchange_in_market_prices",
    "is_symbol_in_symbols_market_prices",
    "symbol_to_assets_market_prices",
    "assets_to_symbol_market_prices",
    "assets_market_dataset_to_symbols_market_datasets",
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
    "ORDERBOOK_COLUMNS",
    "OHLCV_COLUMNS"
]

AssetsPrices = Dict[str, Dict[str, Dict[str, List[Tuple[dt.datetime, float]]]]]
SymbolsPrices = Dict[str, Dict[str, List[Tuple[dt.datetime, float]]]]

def is_exchange_in_market_prices(
        exchange: str,
        prices: Union[AssetsPrices, SymbolsPrices]
) -> None:
    """
    Checks if the exchange is in the prices.

    :param exchange: The exchange name.
    :param prices: The prices.

    :return: The boolean flag.
    """

    return exchange not in prices
# end is_exchange_in_market_prices

def is_symbol_in_assets_market_prices(
        exchange: str,
        symbol: str,
        prices: AssetsPrices,
        separator: Optional[str] = None
) -> bool:
    """
    Checks if the symbol is in the prices' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param prices: The price data to process.
    :param separator: The separator of the assets.

    :return: The validation value.
    """

    if not is_exchange_in_market_prices(exchange=exchange, prices=prices):
        return False
    # end if

    base, quote = symbol_to_parts(symbol=symbol, separator=separator)

    if base not in prices[exchange]:
        return False
    # end if

    if quote not in prices[exchange][base]:
        return False
    # end if

    return not np.isnan(prices[exchange][base][quote])
# end is_symbol_in_assets_market_prices

def is_symbol_in_symbols_market_prices(
        exchange: str,
        symbol: str,
        prices: SymbolsPrices
) -> bool:
    """
    Checks if the symbol is in the prices' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param prices: The price data to process.

    :return: The validation value.
    """

    if not is_exchange_in_market_prices(exchange=exchange, prices=prices):
        return False
    # end if

    if symbol not in prices[exchange]:
        return False
    # end if

    return not np.isnan(prices[exchange][symbol])
# end is_symbol_in_assets_market_prices

def validate_assets_market_state_prices_symbol(
        exchange: str,
        symbol: str,
        prices: AssetsPrices,
        separator: Optional[str] = None,
        provider: Optional[Any] = None
) -> None:
    """
    Checks if the symbol is in the prices' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param separator: The separator of the assets.
    :param prices: The price data to process.
    :param provider: The data provider.

    :return: The validation value.
    """

    base, quote = symbol_to_parts(symbol=symbol, separator=separator)

    if exchange not in prices:
        raise ValueError(
            f"exchange '{exchange}' is not found inside the prices of"
            f"{f' of {provider}' if provider is not None else ''}. "
            f"Found exchanges for are: {', '.join(prices.keys())}"
        )
    # end if

    if base not in prices[exchange]:
        raise ValueError(
            f"base asset '{base}' is not found in '{exchange}' prices of"
            f"{f' of {provider}' if provider is not None else ''}. "
            f"Found base '{exchange}' assets are: "
            f"{', '.join(prices[exchange].keys())}"
        )
    # end if

    if quote not in prices[exchange][base]:
        raise ValueError(
            f"quote asset '{quote}' is not found in the quote "
            f"assets of the '{base}' base asset in the prices"
            f"{f' of {provider}' if provider is not None else ''}. "
            f"Found quote assets for the '{base}' base asset in "
            f"the prices are: {', '.join(prices[exchange][base].keys())}"
        )
    # end if
# end validate_assets_market_state_prices_symbol

def validate_symbols_market_state_prices_symbol(
        exchange: str,
        symbol: str,
        prices: SymbolsPrices,
        provider: Optional[Any] = None
) -> None:
    """
    Checks if the symbol is in the prices' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param prices: The price data to process.
    :param provider: The data provider.

    :return: The validation value.
    """

    if exchange not in prices:
        raise ValueError(
            f"exchange '{exchange}' is not found inside the prices of"
            f"{f' of {provider}' if provider is not None else ''}. "
            f"Found exchanges for are: {', '.join(prices.keys())}"
        )
    # end if

    if symbol not in prices[exchange]:
        raise ValueError(
            f"symbol '{symbol}' is not found in '{exchange}' prices of"
            f"{f' of {provider}' if provider is not None else ''}. "
            f"Found symbols for '{exchange}' prices are: "
            f"{', '.join(prices[exchange].keys())}"
        )
    # end if
# end validate_symbols_market_state_prices_symbol

def assets_market_price(
        exchange: str,
        symbol: str,
        prices: AssetsPrices,
        separator: Optional[str] = None,
        provider: Optional[Any] = None
) -> Tuple[dt.datetime, float]:
    """
    Checks if the symbol is in the prices' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param separator: The separator of the assets.
    :param prices: The price data to process.
    :param provider: The data provider.

    :return: The validation value.
    """

    validate_assets_market_state_prices_symbol(
        symbol=symbol, prices=prices, exchange=exchange,
        separator=separator, provider=provider
    )

    base, quote = symbol_to_parts(symbol=symbol, separator=separator)

    data = list(prices[exchange][base][quote])

    return data[-1][0], float(data[-1][-1])
# end assets_market_price

def symbols_market_price(
        exchange: str,
        symbol: str,
        prices: SymbolsPrices,
        provider: Optional[Any] = None
) -> Tuple[dt.datetime, float]:
    """
    Checks if the symbol is in the prices' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param prices: The price data to process.
    :param provider: The data provider.

    :return: The validation value.
    """

    validate_symbols_market_state_prices_symbol(
        exchange=exchange, symbol=symbol,
        prices=prices, provider=provider
    )

    data = list(prices[exchange][symbol])

    return data[-1][0], float(data[-1][-1])
# end symbols_market_price

def symbols_market_prices(
        exchange: str,
        symbol: str,
        prices: SymbolsPrices,
        provider: Optional[Any] = None
) -> List[Tuple[dt.datetime, float]]:
    """
    Checks if the symbol is in the prices' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param prices: The price data to process.
    :param provider: The data provider.

    :return: The validation value.
    """

    validate_symbols_market_state_prices_symbol(
        exchange=exchange, symbol=symbol,
        prices=prices, provider=provider
    )

    return [(time, float(value)) for time, value in prices[exchange][symbol]]
# end symbols_market_prices

def assets_market_prices(
        exchange: str,
        symbol: str,
        prices: AssetsPrices,
        separator: Optional[str] = None,
        provider: Optional[Any] = None
) -> List[Tuple[dt.datetime, float]]:
    """
    Checks if the symbol is in the prices' data.

    :param exchange: The exchange name.
    :param symbol: The symbol to search.
    :param separator: The separator of the assets.
    :param prices: The price data to process.
    :param provider: The data provider.

    :return: The validation value.
    """

    validate_assets_market_state_prices_symbol(
        symbol=symbol, prices=prices, exchange=exchange,
        separator=separator, provider=provider
    )

    base, quote = symbol_to_parts(symbol=symbol, separator=separator)

    return [(time, float(value)) for time, value in prices[exchange][base][quote]]
# end assets_market_prices

@define(repr=False)
@represent
class MarketBase(metaclass=ABCMeta):
    """
    A class to represent the current market state.

    This object contains the state of the market, as Close,
    bids and asks prices of specific assets, gathered from the network.

    attributes:

    - screeners:
        The screener objects to collect the prices of the assets.
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

def dataset_to_data(dataset: pd.DataFrame) -> List[Tuple[dt.datetime, Dict[str, float]]]:
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
    :param sort: The value to sort the prices by the time.

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
    :param sort: The value to sort the prices by the time.

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

def assets_market_dataset_to_symbols_market_datasets(
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
# end assets_market_dataset_to_symbols_market_datasets

def assets_to_symbol_market_prices(
        prices: AssetsPrices, separator: Optional[str] = None
) -> SymbolsPrices:
    """
    Converts an assets market prices into a symbols market prices.

    :param prices: The source prices.
    :param separator: The separator for the symbols.

    :return: The result prices.
    """

    symbols_prices: SymbolsPrices = {}

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
        prices: SymbolsPrices, separator: Optional[str] = None
) -> AssetsPrices:
    """
    Converts a symbols market prices into an assets market prices.

    :param prices: The source prices.
    :param separator: The separator for the symbols.

    :return: The result prices.
    """

    assets_prices: AssetsPrices = {}

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

_ST = TypeVar("_ST", Type[BaseScreener], Type[OrderbookScreener])

AssetsScreeners = Dict[str, Dict[str, Dict[str, Union[BaseScreener, _ST]]]]

def assets_market_datasets_to_assets_screeners(
        datasets: AssetsMarketDatasets,
        base: Optional[_ST] = None,
        screeners: Optional[BaseScreener] = None,
        separator: Optional[str] = None
) -> AssetsScreeners:
    """
    Builds the screeners from the assets market datasets structure.

    :param datasets: The datasets for the screeners.
    :param base: The base type for a screener.
    :param screeners: screeners to insert datasets into.
    :param separator: The separator for the symbols.

    :return: The screeners.
    """

    if screeners is None:
        screeners = []
    # end if

    screener_base = base or OrderbookScreener

    new_screeners: AssetsScreeners = {}

    for exchange, bases in datasets.items():
        for base, quotes in bases.items():
            for quote, dataset in quotes.items():
                symbol = parts_to_symbol(base, quote, separator=separator)
                for screener in screeners:
                    if not (
                        (screener.exchange.lower() == exchange.lower()) and
                        (screener.symbol.lower() == symbol.lower())
                    ):
                        screener = screener_base(
                            symbol=symbol, exchange=exchange, market=dataset
                        )

                    else:
                        screener.market = dataset
                    # end if

                    (
                        new_screeners.setdefault(exchange, {}).
                        setdefault(base, {}).
                        setdefault(quote, screener)
                    )
                # end for
            # end for
        # end for
    # end for

    return new_screeners
# end assets_market_datasets_to_assets_screeners

SymbolsScreeners = Dict[str, Dict[str, Union[BaseScreener, _ST]]]

def symbols_market_datasets_to_symbols_screeners(
        datasets: SymbolsMarketDatasets,
        base: Optional[_ST] = None,
        screeners: Optional[BaseScreener] = None
) -> SymbolsScreeners:
    """
    Builds the screeners from the assets market datasets structure.

    :param datasets: The datasets for the screeners.
    :param base: The base type for a screener.
    :param screeners: screeners to insert datasets into.

    :return: The screeners.
    """

    if screeners is None:
        screeners = []
    # end if

    screener_base = base or OrderbookScreener

    new_screeners: SymbolsScreeners = {}

    for exchange, symbols in datasets.items():
        for symbol, dataset in symbols.items():
            for screener in screeners:
                if not (
                    (screener.exchange.lower() == exchange.lower()) and
                    (screener.symbol.lower() == symbol.lower())
                ):
                    screener = screener_base(
                        symbol=symbol, exchange=exchange, market=dataset
                    )

                else:
                    screener.market = dataset
                # end if

                (
                    new_screeners.setdefault(exchange, {}).
                    setdefault(symbol, screener)
                )
            # end for
        # end for
    # end for

    return new_screeners
# end symbols_market_datasets_to_symbols_screeners

def assets_screeners(screeners: AssetsScreeners) -> List[Union[BaseScreener, _ST]]:
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

def symbols_screeners(screeners: SymbolsScreeners) -> List[Union[BaseScreener, _ST]]:
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

            if not found_screeners and not adjust:
                raise ValueError(
                    f"Unable to find a screener with exchange "
                    f"'{exchange}' and symbol '{symbol}' to update its data. "
                    f"Consider setting the 'adjust' parameter to True, ignore."
                )
            # end if

            screener = found_screeners[0]

            for time, row in rows:
                screener.market.loc[time] = row
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

ORDERBOOK_COLUMNS = {
    "bids": BIDS, "asks": ASKS,
    "bids_volume": BIDS_VOLUME, "asks_volume": ASKS_VOLUME
}

OHLCV_COLUMNS = {
    "opens": OPEN, "highs": HIGH, "lows": LOW,
    "closes": CLOSE, "volumes": VOLUME
}

def assets_market_data(
        columns: Dict[str, str],
        prices: Optional[Dict[str, AssetsPrices]] = None
) -> AssetsMarketData:
    """
    Returns the structured data of the state.

    :param prices: The prices for the data collection.
    :param columns: The columns for the data.

    :return: The data of the state.
    """

    prices = prices or {name: {} for name in columns}

    datasets: Dict[str, Dict[str, Dict[str, Dict[dt.datetime, Dict[str, float]]]]] = {}

    for name in columns:
        for exchange, bases in prices[name].items():
            for base, quotes in bases.items():
                for quote, symbols_prices in quotes.items():
                    for i, (time, price) in enumerate(symbols_prices):
                        try:
                            if isinstance(time, str):
                                time = dt.datetime.fromisoformat(time)

                            elif isinstance(time, int):
                                time = dt.datetime.fromtimestamp(time)
                            # end if

                        except (Type, ValueError):
                            pass
                        # end try

                        (
                            datasets.
                            setdefault(exchange, {}).
                            setdefault(base, {}).
                            setdefault(quote, {}).
                            setdefault(time, {})
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
        prices: Optional[Dict[str, SymbolsPrices]] = None
) -> SymbolsMarketData:
    """
    Returns the structured data of the state.

    :param prices: The prices for the data collection.
    :param columns: The columns for the data.

    :return: The data of the state.
    """

    datasets: Dict[str, Dict[str, Dict[dt.datetime, Dict[str, float]]]] = {}

    for name in columns:
        for exchange, symbols in prices[name].items():
            for symbol, symbols_prices in symbols.items():
                for i, (time, price) in enumerate(symbols_prices):
                    try:
                        if isinstance(time, str):
                            time = dt.datetime.fromisoformat(time)

                        elif isinstance(time, int):
                            time = dt.datetime.fromtimestamp(time)

                    except (Type, ValueError):
                        pass
                    # end try

                    (
                        datasets.
                        setdefault(exchange, {}).
                        setdefault(symbol, {}).
                        setdefault(time, {})
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

def assets_market_state(
        columns: Dict[str, str],
        prices: Optional[Dict[str, AssetsPrices]] = None,
        screeners: Optional[Iterable[BaseScreener]] = None,
        separator: Optional[str] = None,
        length: Optional[int] = None,
        adjust: Optional[bool] = True
) -> Dict[str, AssetsPrices]:
    """
    Fetches the prices and relations between the assets.

    :param prices: The prices for the data collection.
    :param columns: The columns for the data.
    :param screeners: The price screeners.
    :param separator: The separator of the assets.
    :param length: The length of the prices.
    :param adjust: The value to adjust the length of the sequences.

    :return: The prices of the assets.
    """

    prices = prices or {name: {} for name in columns}

    if (length is None) and (not adjust):
        length = min(
            [
                len(
                    screener.base_market
                    if (
                        (columns == ORDERBOOK_COLUMNS) and
                        isinstance(screener, OHLCVScreener)
                    ) else
                    screener.market
                )
                for screener in screeners
            ]
        )
    # end if

    for screener in screeners:
        market = screener.market

        if (columns == ORDERBOOK_COLUMNS) and isinstance(screener, OHLCVScreener):
            market = screener.base_market
        # end if

        if adjust and (length is None):
            length = len(market)

        elif adjust:
            length = min([len(market), length])
        # end if

        if length > len(market):
            raise ValueError(
                f"Data of '{screener.exchange}' "
                f"symbol in '{screener.symbol}' exchange "
                f"is not long enough for the requested length: {length}. "
                f"Consider using the 'adjust' parameter as {True}, "
                f"to adjust to the actual length of the data."
            )
        # end if

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
        prices: Optional[Dict[str, SymbolsPrices]] = None,
        screeners: Optional[Iterable[BaseScreener]] = None,
        length: Optional[int] = None,
        adjust: Optional[bool] = True
) -> Dict[str, SymbolsPrices]:
    """
    Fetches the prices and relations between the assets.

    :param prices: The prices for the data collection.
    :param columns: The columns for the data.
    :param screeners: The price screeners.
    :param length: The length of the prices.
    :param adjust: The value to adjust the length of the sequences.

    :return: The prices of the assets.
    """

    prices = prices or {name: {} for name in columns}

    if (length is None) and (not adjust):
        length = min(
            [
                len(
                    screener.base_market
                    if (
                        (columns == ORDERBOOK_COLUMNS) and
                        isinstance(screener, OHLCVScreener)
                    ) else
                    screener.market
                )
                for screener in screeners
            ]
        )
    # end if

    for screener in screeners:
        market = screener.market

        if (columns == ORDERBOOK_COLUMNS) and isinstance(screener, OHLCVScreener):
            market = screener.base_market
        # end if

        if adjust and (length is None):
            length = len(market)

        elif adjust:
            length = min([len(market), length])
        # end if

        if length > len(market):
            raise ValueError(
                f"Data of '{screener.exchange}' symbol in '{screener.symbol}' exchange "
                f"is not long enough for the requested length: {length}. "
                f"Consider using the 'adjust' parameter as {True}, "
                f"to adjust to the actual length of the data."
            )
        # end if

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
        prices: Dict[str, AssetsPrices],
        sort: Optional[bool] = True
) -> Dict[str, AssetsPrices]:
    """
    Concatenates the states of the market.

    :param prices: The prices for the data collection.
    :param states: The states to concatenate.
    :param sort: The value to sort the prices by the time.

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
        prices: Dict[str, SymbolsPrices],
        sort: Optional[bool] = True
) -> Dict[str, SymbolsPrices]:
    """
    Concatenates the states of the market.

    :param prices: The prices for the data collection.
    :param states: The states to concatenate.
    :param sort: The value to sort the prices by the time.

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