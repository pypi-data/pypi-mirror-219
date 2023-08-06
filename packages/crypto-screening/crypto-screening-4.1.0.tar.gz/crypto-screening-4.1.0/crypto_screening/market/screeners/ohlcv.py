# ohlcv.py

import datetime as dt
from typing import (
    Dict, Optional, Iterable, Any, Union, List
)

import pandas as pd

from represent import Modifiers

from cryptofeed import FeedHandler
from cryptofeed.types import OrderBook

from crypto_screening.process import find_string_value
from crypto_screening.interval import interval_to_total_time
from crypto_screening.dataset import (
    OHLCV_COLUMNS, VOLUME, BIDS, BIDS_VOLUME,
    load_dataset, save_dataset, OHLC_COLUMNS, create_market_dataframe
)
from crypto_screening.validate import validate_interval
from crypto_screening.symbols import adjust_symbol
from crypto_screening.market.screeners.base import BaseScreener
from crypto_screening.market.screeners.recorder import (
    structure_screener_datasets, MarketRecorder, validate_market
)
from crypto_screening.market.screeners.orderbook import (
    create_orderbook_dataframe, OrderbookScreener, record_orderbook,
    OrderbookMarketScreener, create_orderbook_market, OrderbookMarketRecorder
)

__all__ = [
    "OHLCVMarketScreener",
    "OHLCVMarketRecorder",
    "OHLCVScreener",
    "create_ohlcv_market",
    "ohlcv_market_screener",
    "ohlcv_market_recorder",
    "create_ohlcv_dataframe",
    "validate_intervals",
    "structure_screener_intervals",
    "datasets_to_intervals_datasets",
    "validate_ohlcv_market",
    "create_ohlcv_market_recorder_initializers",
    "structure_screeners_intervals"
]

OHLCVMarket = Dict[str, Dict[str, Dict[str, pd.DataFrame]]]
Market = Dict[str, Dict[str, Any]]
Intervals = Dict[str, Dict[str, Iterable[str]]]
Indexes = Dict[str, Dict[str, Dict[str, int]]]

def create_ohlcv_dataframe() -> pd.DataFrame:
    """
    Creates a dataframe for the order book data.

    :return: The dataframe.
    """

    return create_market_dataframe(
        columns=OHLCVMarketRecorder.COLUMNS
    )
# end create_ohlcv_dataframe

def datasets_to_intervals_datasets(
        data: Dict[str, Iterable[str]],
        interval: Optional[str] = None
) -> Dict[str, Dict[str, List[str]]]:
    """
    Creates the dataframes of the market data.

    :param data: The market data.
    :param interval: The interval for the structure.

    :return: The dataframes of the market data.
    """

    interval = interval or OHLCVScreener.INTERVAL

    return {
        exchange.lower(): {
            symbol.upper(): [interval]
            for symbol in symbols
        } for exchange, symbols in data.items()
    }
# end datasets_to_intervals_datasets

class OHLCVScreener(BaseScreener):
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

    - interval:
        The interval for the data structure of OHLCV.

    - market:
        The dataset of the market data as OHLCV.

    - base_market:
        The dataset of the market data as BID/ASK spread.
    """

    INTERVAL = "1m"

    def __init__(
            self,
            symbol: str,
            exchange: str,
            interval: Optional[str] = None,
            location: Optional[str] = None,
            cancel: Optional[Union[float, dt.timedelta]] = None,
            delay: Optional[Union[float, dt.timedelta]] = None,
            market: Optional[pd.DataFrame] = None,
            base_market: Optional[pd.DataFrame] = None
    ) -> None:
        """
        Defines the class attributes.

        :param symbol: The symbol of the asset.
        :param interval: The interval for the data.
        :param exchange: The exchange to get source data from.
        :param location: The saving location for the data.
        :param delay: The delay for the process.
        :param cancel: The cancel time for the loops.
        :param market: The data for the market.
        :param base_market: The base market dataset.
        """

        super().__init__(
            symbol=symbol, exchange=exchange, location=location,
            cancel=cancel, delay=delay, market=market
        )

        self.interval = self.validate_interval(interval or self.INTERVAL)

        self.base_market = base_market
    # end __init__

    @staticmethod
    def validate_interval(interval: str) -> str:
        """
        Validates the symbol value.

        :param interval: The interval for the data.

        :return: The validates symbol.
        """

        return validate_interval(interval=interval)
    # end validate_symbol

    @property
    def orderbook_market(self) -> pd.DataFrame:
        """
        Returns the market to hold the recorder data.

        :return: The market object.
        """

        return self.base_market
    # end orderbook_market

    @property
    def ohlcv_market(self) -> pd.DataFrame:
        """
        Returns the market to hold the recorder data.

        :return: The market object.
        """

        return self.market
    # end ohlcv_market

    def orderbook_dataset_path(self, location: Optional[str] = None) -> str:
        """
        Creates the path to the saving file for the screener object.

        :param location: The saving location of the dataset.

        :return: The saving path for the dataset.
        """

        return self.dataset_path(location=location)
    # end orderbook_dataset_path

    def save_orderbook_dataset(self, location: Optional[str] = None) -> None:
        """
        Saves the data of the screener.

        :param location: The saving location of the dataset.
        """

        if len(self.orderbook_market) > 0:
            save_dataset(
                dataset=self.orderbook_market,
                path=self.orderbook_dataset_path(location=location)
            )
        # end if
    # end save_orderbook_dataset

    def ohlcv_dataset_path(self, location: Optional[str] = None) -> str:
        """
        Creates the path to the saving file for the screener object.

        :param location: The saving location of the dataset.

        :return: The saving path for the dataset.
        """

        return (
            self.dataset_path(location=location).
            replace(".csv", f"-{self.interval}.csv")
        )
    # end ohlcv_dataset_path

    def save_ohlcv_dataset(self, location: Optional[str] = None) -> None:
        """
        Saves the data of the screener.

        :param location: The saving location of the dataset.
        """

        if len(self.ohlcv_market) > 0:
            save_dataset(
                dataset=self.ohlcv_market,
                path=self.ohlcv_dataset_path(location=location)
            )
        # end if
    # end save_ohlcv_dataset

    def save_datasets(self, location: Optional[str] = None) -> None:
        """
        Saves the data of the screener.

        :param location: The saving location of the dataset.
        """

        self.save_ohlcv_dataset(location=location)
        self.save_orderbook_dataset(location=location)
    # end save_datasets

    def save_dataset(self, location: Optional[str] = None) -> None:
        """
        Saves the data of the screener.

        :param location: The saving location of the dataset.
        """

        self.save_datasets(location=location)
    # end save_dataset

    def load_ohlcv_dataset(self, location: Optional[str] = None) -> None:
        """
        Saves the data of the screener.

        :param location: The saving location of the dataset.
        """

        data = load_dataset(path=self.ohlcv_dataset_path(location=location))

        for index, data in zip(data.index[:], data.loc[:]):
            self.ohlcv_market.loc[index] = data
        # end for
    # end load_ohlcv_dataset

    def load_orderbook_dataset(self, location: Optional[str] = None) -> None:
        """
        Saves the data of the screener.

        :param location: The saving location of the dataset.
        """

        data = load_dataset(path=self.orderbook_dataset_path(location=location))

        for index, data in zip(data.index[:], data.loc[:]):
            self.orderbook_market.loc[index] = data
        # end for
    # end load_orderbook_dataset

    def load_datasets(self, location: Optional[str] = None) -> None:
        """
        Saves the data of the screener.

        :param location: The saving location of the dataset.
        """

        self.load_ohlcv_dataset(location=location)
        self.load_orderbook_dataset(location=location)
    # end load_datasets

    def load_dataset(self, location: Optional[str] = None) -> None:
        """
        Saves the data of the screener.

        :param location: The saving location of the dataset.
        """

        self.load_datasets(location=location)
    # end load_dataset

    def orderbook_screener(self) -> OrderbookScreener:
        """
        Creates the orderbook screener object.

        :return: The orderbook screener.
        """

        return OrderbookScreener(
            symbol=self.symbol, exchange=self.exchange, location=self.location,
            cancel=self.cancel, delay=self.delay, market=self.base_market
        )
    # end orderbook_screener
# end OHLCVScreener

def validate_intervals(data: Any) -> Intervals:
    """
    Validates the data.

    :param data: The data to validate.

    :return: The valid data.
    """

    try:
        if not isinstance(data, dict):
            raise ValueError
        # end if

        for exchange, symbols in data.items():
            if not (
                isinstance(exchange, str) and
                (
                    isinstance(symbols, dict) and
                    all(
                        all(isinstance(interval, str) for interval in intervals)
                        for symbol, intervals in symbols.items()
                    )
                )
            ):
                raise ValueError
            # end if
        # end for

    except (TypeError, ValueError):
        raise ValueError(
            f"Data must be of type {Intervals}, not: {data}."
        )
    # end try

    return data
# end validate_intervals

def validate_ohlcv_market(data: Any) -> OHLCVMarket:
    """
    Validates the data.

    :param data: The data to validate.

    :return: The valid data.
    """

    try:
        if not isinstance(data, dict):
            raise ValueError
        # end if

        for exchange, symbols in data.items():
            if not (
                isinstance(exchange, str) and
                (
                    isinstance(symbols, dict) and
                    all(
                        all(
                            isinstance(interval, str) and
                            isinstance(dataset, pd.DataFrame)
                            for interval, dataset in intervals.items()
                        )
                        for symbol, intervals in symbols.items()
                    )
                )
            ):
                raise ValueError
            # end if
        # end for

    except (TypeError, ValueError):
        raise ValueError(
            f"Data must be of type {OHLCVMarket}, not: {data}."
        )
    # end try

    return data
# end validate_ohlcv_market

def create_ohlcv_market(data: Intervals) -> Dict[str, Dict[str, Dict[str, pd.DataFrame]]]:
    """
    Creates the dataframes of the market data.

    :param data: The market data.

    :return: The dataframes of the market data.
    """

    return {
        exchange.lower(): {
            symbol.upper(): {
                interval: create_ohlcv_dataframe()
                for interval in intervals
            }
            for symbol, intervals in symbols.items()
        } for exchange, symbols in data.items()
    }
# end create_ohlcv_market

def create_ohlcv_market_recorder_initializers(
        intervals: Optional[Intervals] = None,
        market: Optional[Market] = None,
        ohlcv_market: Optional[OHLCVMarket] = None
) -> Dict[str, Union[Market, OHLCVMarket, Intervals]]:
    """
    Defines the class attributes.

    :param market: The object to fill with the crypto feed record.
    :param intervals: The intervals for the datasets.
    :param ohlcv_market: The OHLCV market structure.

    :return: The valid data.
    """

    if (ohlcv_market, market, intervals) == (None, None, None):
        raise ValueError(
            f"No data given to initialize {OHLCVMarketRecorder}"
        )
    # end if

    if (ohlcv_market is not None) and (intervals is None):
        validate_ohlcv_market(ohlcv_market)

        intervals: Dict[str, Dict[str, List[str]]] = {}

        for exchange, symbols in ohlcv_market.items():
            for symbol, symbol_intervals in symbols.items():
                for interval in symbol_intervals:
                    (
                        intervals.
                        setdefault(exchange, {}).
                        setdefault(symbol, []).
                        append(interval)
                    )
                # end for
            # end for
        # end for
    # end if

    if (market is not None) and (intervals is None):
        validate_market(market)

        intervals: Dict[str, Dict[str, List[str]]] = {}

        for exchange, symbols in market.items():
            for symbol in symbols:
                (
                    intervals.
                    setdefault(exchange, {}).
                    setdefault(symbol, []).
                    append(OHLCVMarketRecorder.INTERVAL)
                )
            # end for
        # end for
    # end if

    if (ohlcv_market is None) and intervals:
        validate_intervals(intervals)

        ohlcv_market = create_ohlcv_market(data=intervals)
    # end if

    if (market is None) and (ohlcv_market is not None):
        validate_ohlcv_market(ohlcv_market)

        market: Market = {}

        for exchange, symbols in ohlcv_market.items():
            for symbol, symbol_intervals in symbols.items():
                (
                    market.
                    setdefault(exchange, {}).
                    setdefault(symbol, create_orderbook_dataframe())
                )
            # end for
        # end for
    # end if

    return dict(
        market=market,
        ohlcv_market=ohlcv_market,
        intervals=intervals
    )
# end create_ohlcv_market_recorder_initializers

def record_ohlcv(
        market: Market,
        ohlcv_market: OHLCVMarket,
        indexes: Indexes,
        data: OrderBook,
        timestamp: float
) -> bool:
    """
    Records the data from the crypto feed into the dataset.

    :param market: The market structure.
    :param ohlcv_market: The OHLCV market structure.
    :param indexes: The indexes of the OHLCV market.
    :param data: The data from the exchange.
    :param timestamp: The time of the request.
    """

    if not record_orderbook(market=market, data=data, timestamp=timestamp):
        return False
    # end if

    exchange = find_string_value(
        value=data.exchange, values=market.keys()
    )
    symbol = find_string_value(
        value=adjust_symbol(symbol=data.symbol),
        values=exchange
    )

    spread = market[exchange][symbol]

    for interval, ohlcv_dataset in ohlcv_market[exchange][symbol].items():
        dataset_index = (
            indexes.
            setdefault(exchange, {}).
            setdefault(symbol, {}).
            setdefault(interval, 0)
        )

        span: dt.timedelta = spread.index[-1] - spread.index[dataset_index]

        interval_total_time = interval_to_total_time(interval)

        if (span >= interval_total_time) or (dataset_index == 0):
            interval_total_minutes = interval_total_time.total_seconds() // 60
            adjuster = f'{interval_total_minutes}Min'

            ohlcv: pd.DataFrame = spread[BIDS].resample(adjuster).ohlc()
            ohlcv.columns = list(OHLC_COLUMNS)
            volume: pd.DataFrame = spread[BIDS_VOLUME].resample(adjuster).ohlc()
            ohlcv[VOLUME] = volume[list(volume.columns)[-1]]

            for index, row in ohlcv.iterrows():
                ohlcv_dataset.loc[index] = row
            # end for

            indexes[exchange][symbol][interval] += 1
        # end for
    # end for

    return True
# end record_ohlcv

class OHLCVMarketRecorder(OrderbookMarketRecorder):
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

    - intervals:
        The structure to set a specific interval to the dataset
        of each symbol in each exchange, matching the market data.

    >>> from crypto_screening.market.screeners import ohlcv_market_recorder
    >>>
    >>> market = {'binance': ['BTC/USDT'], 'bittrex': {'1m': 'ETH/USDT'}}
    >>>
    >>> recorder = ohlcv_market_recorder(data=market)
    """

    __modifiers__ = Modifiers(**MarketRecorder.__modifiers__)
    __modifiers__.hidden.extend(["intervals", "ohlcv_market"])

    __slots__ = "_indexes", "ohlcv_market", "intervals"

    COLUMNS = OHLCV_COLUMNS
    INTERVAL = OHLCVScreener.INTERVAL

    def __init__(
            self,
            intervals: Optional[Intervals] = None,
            market: Optional[Market] = None,
            ohlcv_market: Optional[OHLCVMarket] = None
    ) -> None:
        """
        Defines the class attributes.

        :param market: The object to fill with the crypto feed record.
        :param intervals: The intervals for the datasets.
        :param ohlcv_market: The OHLCV market structure.
        """

        data = create_ohlcv_market_recorder_initializers(
            market=market, ohlcv_market=ohlcv_market, intervals=intervals
        )

        market = data["market"]
        intervals = data["intervals"]
        ohlcv_market = data["ohlcv_market"]

        super().__init__(market=market)

        self.intervals = self.validate_intervals(intervals)
        self.ohlcv_market = self.validate_ohlcv_market(ohlcv_market)

        self._indexes: Indexes = {}
    # end __init__

    @staticmethod
    def validate_ohlcv_market(data: Any) -> OHLCVMarket:
        """
        Validates the data.

        :param data: The data to validate.

        :return: The valid data.
        """

        return validate_ohlcv_market(data=data)
    # end validate_ohlcv_market

    @staticmethod
    def validate_intervals(data: Any) -> Intervals:
        """
        Validates the data.

        :param data: The data to validate.

        :return: The valid data.
        """

        return validate_intervals(data=data)
    # end validate_market

    def ohlcv(self, exchange: str, symbol: str, interval: str) -> pd.DataFrame:
        """
        Returns the market data of the symbol from the exchange.

        :param exchange: The source name of the exchange.
        :param symbol: The symbol of the pair.
        :param interval: The interval for the dataset.

        :return: The dataset of the spread data.
        """

        self.data(exchange=exchange, symbol=symbol)

        intervals = self.ohlcv_market[exchange][symbol]

        interval = find_string_value(value=interval, values=intervals)

        if interval not in intervals:
            raise ValueError(
                f"'{interval}' is not a valid "
                f"interval for the symbol '{symbol}' of '{exchange}' exchange. "
                f"Valid symbols: {', '.join(intervals.keys() or [])} for {self}."
            )
        # end if

        return intervals[interval]
    # end ohlcv

    def ohlcv_in_market(self, exchange: str, symbol: str, interval: str) -> bool:
        """
        Returns the market data of the symbol from the exchange.

        :param exchange: The source name of the exchange.
        :param symbol: The symbol of the pair.
        :param interval: The interval for the dataset.

        :return: The dataset of the spread data.
        """

        try:
            self.ohlcv(exchange=exchange, symbol=symbol, interval=interval)

            return True

        except ValueError:
            return False
        # end try
    # end ohlcv_in_market

    async def record(self, data: OrderBook, timestamp: float) -> bool:
        """
        Records the data from the crypto feed into the dataset.

        :param data: The data from the exchange.
        :param timestamp: The time of the request.
        """

        return record_ohlcv(
            market=self.market, ohlcv_market=self.ohlcv_market,
            indexes=self._indexes, data=data, timestamp=timestamp
        )
    # end record
# end MarketOHLCVRecorder

def structure_screener_intervals(
        screeners: Iterable[OHLCVScreener]
) -> Dict[str, Dict[str, List[str]]]:
    """
    Structures the screener objects by exchanges and symbols

    :param screeners: The screeners to structure.

    :return: The structure of the screeners.
    """

    structure: Dict[str, Dict[str, List[str]]] = {}

    for screener in screeners:
        (
            structure.
            setdefault(screener.exchange, {}).
            setdefault(screener.symbol, []).
            append(screener.interval)
        )
    # end for

    return structure
# end structure_screener_intervals

def structure_screeners_intervals(
        screeners: Iterable[OHLCVScreener]
) -> OHLCVMarket:
    """
    Structures the screener objects by exchanges and symbols

    :param screeners: The screeners to structure.

    :return: The structure of the screeners.
    """

    structure = {}

    for screener in screeners:
        (
            structure.
            setdefault(screener.exchange, {}).
            setdefault(screener.symbol, {}).
            setdefault(screener.interval, screeners)
        )
    # end for

    return structure
# end structure_screeners_intervals

class OHLCVMarketScreener(OrderbookMarketScreener):
    """
    A class to represent an asset price screener.

    Using this class, you can create a screener object to
    screen the market ask and bid data for a specific asset in
    a specific exchange at real time.

    Parameters:

    - screeners:
        The screeners to connect to the market screener.

    - intervals:
        The structure to set a specific interval to the dataset
        of each symbol in each exchange, matching the market data.

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

    screeners: List[Union[OHLCVScreener, OrderbookScreener]]
    recorder: OHLCVMarketRecorder

    COLUMNS = OHLCVMarketRecorder.COLUMNS
    INTERVAL = OHLCVMarketRecorder.INTERVAL

    def __init__(
            self,
            intervals: Optional[Intervals] = None,
            market: Optional[Market] = None,
            ohlcv_market: Optional[OHLCVMarket] = None,
            screeners: Optional[Iterable[Union[OHLCVScreener, OrderbookScreener]]] = None,
            location: Optional[str] = None,
            cancel: Optional[Union[float, dt.timedelta]] = None,
            delay: Optional[Union[float, dt.timedelta]] = None,
            refresh: Optional[Union[float, dt.timedelta, bool]] = None,
            limited: Optional[bool] = None,
            handler: Optional[FeedHandler] = None,
            amount: Optional[int] = None,
            recorder: Optional[OHLCVMarketRecorder] = None
    ) -> None:
        """
        Creates the class attributes.

        :param location: The saving location for the data.
        :param intervals: The intervals for the datasets.
        :param delay: The delay for the process.
        :param cancel: The cancel time for the loops.
        :param limited: The value to limit the screeners to active only.
        :param refresh: The refresh time for rerunning.
        :param handler: The handler object for the market data.
        :param amount: The maximum amount of symbols for each feed.
        :param recorder: The recorder object for recording the data.
        """

        screeners = screeners or []

        data = create_ohlcv_market_recorder_initializers(
            market=market or structure_screener_datasets(screeners=screeners),
            intervals=intervals or structure_screener_intervals(screeners=screeners),
            ohlcv_market=ohlcv_market
        )

        market = data["market"]
        intervals = data["intervals"]
        ohlcv_market = data["ohlcv_market"]

        super().__init__(
            location=location, cancel=cancel,
            delay=delay, recorder=recorder or OHLCVMarketRecorder(
                market=market, intervals=intervals, ohlcv_market=ohlcv_market
            ),
            screeners=screeners, handler=handler, limited=limited,
            amount=amount, refresh=refresh
        )

        self.screeners[:] = screeners or self.create_ohlcv_screeners()
    # end __init__

    @property
    def ohlcv_market(self) -> OHLCVMarket:
        """
        Returns the market to hold the recorder data.

        :return: The market object.
        """

        return self.recorder.ohlcv_market
    # end ohlcv_market

    @property
    def ohlcv_screeners(self) -> List[OHLCVScreener]:
        """
        Returns a list of all the ohlcv screeners.

        :return: The ohlcv screeners.
        """

        return [
            screener for screener in self.screeners
            if isinstance(screener, OHLCVScreener)
        ]
    # end ohlcv_screeners

    def connect_screeners(self) -> None:
        """Connects the screeners to the recording object."""

        super().connect_screeners()

        for screener in self.screeners:
            if isinstance(screener, OHLCVScreener):
                screener.base_market = self.recorder.orderbook(
                    exchange=screener.exchange, symbol=screener.symbol
                )
                screener.market = self.recorder.ohlcv(
                    exchange=screener.exchange, symbol=screener.symbol,
                    interval=screener.interval
                )
        # end for
    # end connect_screeners

    def ohlcv(self, exchange: str, symbol: str, interval: str) -> pd.DataFrame:
        """
        Returns the market data of the symbol from the exchange.

        :param exchange: The source name of the exchange.
        :param symbol: The symbol of the pair.
        :param interval: The interval for the dataset.

        :return: The dataset of the spread data.
        """

        return self.recorder.ohlcv(
            exchange=exchange, symbol=symbol, interval=interval
        )
    # end orderbook

    def ohlcv_in_market(self, exchange: str, symbol: str, interval: str) -> bool:
        """
        Returns the market data of the symbol from the exchange.

        :param exchange: The source name of the exchange.
        :param symbol: The symbol of the pair.
        :param interval: The interval for the dataset.

        :return: The dataset of the spread data.
        """

        return self.recorder.ohlcv_in_market(
            exchange=exchange, symbol=symbol, interval=interval
        )
    # end ohlcv_in_market

    def create_ohlcv_screener(
            self,
            symbol: str,
            exchange: str,
            interval: Optional[str] = None,
            location: Optional[str] = None,
            cancel: Optional[Union[float, dt.timedelta]] = None,
            delay: Optional[Union[float, dt.timedelta]] = None,
            container: Optional[Dict[str, Dict[str, OHLCVScreener]]] = None
    ) -> OHLCVScreener:
        """
        Defines the class attributes.

        :param symbol: The symbol of the asset.
        :param exchange: The exchange to get source data from.
        :param location: The saving location for the data.
        :param cancel: The time to cancel the waiting.
        :param delay: The delay for the process.
        :param container: The container to contain the new screener.
        :param interval: The interval for the dataset.
        """

        if interval is None:
            interval = self.INTERVAL
        # end if

        if container is None:
            container = {}
        # end if

        if cancel is None:
            cancel = self.cancel
        # end if

        if delay is None:
            delay = self.delay
        # end if

        screener = OHLCVScreener(
            symbol=symbol, exchange=exchange, delay=delay,
            location=location, cancel=cancel, market=(
                self.ohlcv(
                    exchange=exchange, symbol=symbol, interval=interval
                ) if self.ohlcv_in_market(
                    symbol=symbol, exchange=exchange, interval=interval
                ) else None
            ),
            base_market=(
                self.orderbook(exchange=exchange, symbol=symbol)
                if self.orderbook_in_market(symbol=symbol, exchange=exchange)
                else None
            )
        )

        container.setdefault(exchange, {})[symbol] = screener

        return screener
    # end create_ohlcv_screener

    def create_ohlcv_screeners(
            self,
            interval: Optional[str] = None,
            intervals: Optional[Intervals] = None,
            location: Optional[str] = None,
            cancel: Optional[Union[float, dt.timedelta]] = None,
            delay: Optional[Union[float, dt.timedelta]] = None,
            container: Optional[Dict[str, Dict[str, OHLCVScreener]]] = None
    ) -> List[OHLCVScreener]:
        """
        Defines the class attributes.

        :param interval: The interval for the dataset.
        :param intervals: The intervals for the screeners.
        :param location: The saving location for the data.
        :param cancel: The time to cancel the waiting.
        :param delay: The delay for the process.
        :param container: The container to contain the new screeners.
        """

        screeners = []

        try:
            validate_intervals(intervals)

            valid = True

        except ValueError:
            valid = False
        # end try

        for exchange, symbols in self.structure().items():
            for symbol in symbols:
                if valid:
                    interval = intervals[exchange][symbol]
                # end if

                screeners.append(
                    self.create_ohlcv_screener(
                        symbol=symbol, exchange=exchange, delay=delay,
                        location=location, cancel=cancel,
                        container=container, interval=interval
                    )
                )
            # end for
        # end for

        return screeners
    # end create_ohlcv_screeners
# end MarketOHLCVRecorder

def ohlcv_market_recorder(
        data: Union[Intervals, Dict[str, Iterable[str]]],
        interval: Optional[str] = None
) -> OHLCVMarketRecorder:
    """
    Creates the market recorder object for the data.

    :param data: The market data.
    :param interval: The interval for the structure.

    :return: The market recorder object.
    """

    try:
        intervals = validate_ohlcv_market(data)

    except ValueError:
        validate_market(data)

        intervals = datasets_to_intervals_datasets(
            data=data, interval=interval
        )
    # end try

    return OHLCVMarketRecorder(intervals=intervals, market=data)
# end ohlcv_market_recorder

def ohlcv_market_screener(
        data: Union[Intervals, Dict[str, Iterable[str]]],
        intervals: Optional[Intervals] = None,
        market: Optional[Market] = None,
        ohlcv_market: Optional[OHLCVMarket] = None,
        location: Optional[str] = None,
        cancel: Optional[Union[float, dt.timedelta]] = None,
        delay: Optional[Union[float, dt.timedelta]] = None,
        limited: Optional[bool] = None,
        handler: Optional[FeedHandler] = None,
        amount: Optional[int] = None,
        refresh: Optional[Union[float, dt.timedelta, bool]] = None,
        recorder: Optional[OHLCVMarketRecorder] = None,
        fixed: Optional[bool] = True,
        separator: Optional[str] = None,
        parameters: Optional[Union[Dict[str, Dict[str, Any]], Dict[str, Any]]] = None
) -> OHLCVMarketScreener:
    """
    Creates the market screener object for the data.

    :param data: The market data.
    :param handler: The handler object for the market data.
    :param limited: The value to limit the screeners to active only.
    :param parameters: The parameters for the exchanges.
    :param market: The object to fill with the crypto feed record.
    :param intervals: The intervals for the datasets.
    :param ohlcv_market: The OHLCV market structure.
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

    try:
        intervals = validate_intervals(data)

    except ValueError:
        market = create_orderbook_market(data)
    # end try

    screener = OHLCVMarketScreener(
        recorder=recorder or OHLCVMarketRecorder(
            market=market, ohlcv_market=ohlcv_market, intervals=intervals
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