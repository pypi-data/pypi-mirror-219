# ohlcv.py

import time
import asyncio
import warnings
import datetime as dt
from typing import (
    Optional, Union, Dict, Iterable, Any, List
)

import pandas as pd
import numpy as np

import ccxt
import ccxt.pro as ccxtpro
import ccxt.async_support as async_ccxt

from represent import Modifiers

from multithreading import Caller, multi_threaded_call

from crypto_screening.dataset import (
    OPEN, HIGH, LOW, CLOSE, VOLUME, BIDS, ASKS,
    DATE_TIME, OHLCV_COLUMNS, ASKS_VOLUME, BIDS_VOLUME
)
from crypto_screening.interval import interval_to_total_time
from crypto_screening.market.screeners.base import (
    BaseMultiScreener, structure_screener_datasets, BaseScreener
)
from crypto_screening.market.screeners.recorder import (
    MarketRecorder, create_market_dataframe
)

__all__ = [
    "OHLCVScreener",
    "MarketOHLCVScreener",
    "market_ohlcv_recorder",
    "MarketOHLCVRecorder",
    "market_ohlcv_screener",
    "create_ohlcv_market",
    "create_ohlcv_dataframe"
]

def configure_exchange(
        exchange: str,
        pro: Optional[bool] = True,
        options: Optional[Dict[str, Any]] = None
) -> async_ccxt.Exchange:
    """
    Validates the exchange source value.

    :param exchange: The name of the exchange platform.
    :param pro: The value for the pro interface.
    :param options: The ccxt options.

    :return: The validates source.
    """

    if exchange.lower() == "coinbase":
        exchange = "coinbasepro"
    # end if

    try:
        exchange_service = getattr(
            (ccxtpro if pro else async_ccxt), exchange
        )(options)

    except AttributeError:
        raise ValueError(f"Unrecognized exchange name: {exchange}.")
        # end try

    if not (
        hasattr(exchange_service, "watch_tickers") or
        hasattr(exchange_service, "fetch_tickers")
    ):
        raise ValueError(
            f"Exchange {exchange_service} must have at least one of the "
            f"methods 'fetch_tickers', or 'watch_tickers'."
        )
        # end if
    # end if

    return exchange_service
# end configure_exchange

class OHLCVScreener(BaseScreener):
    """
    A class to represent a live asset data builder.

    Using this class, you can create a screener object to
    screen the market ask and bid data for a specific asset in
    a specific exchange at real time.

    You can also use it to build real time datasets of Open
    High Low Close Volume, with Bids and Asks.

    Parameters:

    - symbol:
        The symbol of an asset to screen.

    - exchange:
        The name of the exchange platform to screen data from.

    - locaion:
        The saving location for the saved data of the screener.

    - interval:
        The interval for the time between data points in the dataset.

    - delay:
        The delay to wait between each data fetching.

    - screener:
        The screener object to connect to for creating the dataset.

    - length:
        An initial dataset length to start with.

    - pro:
        The value to use the pro interface.

    - options:
        The ccxt options for the backend screening process.

    - cencel:
        The time to cancel screening process after no new data is fetched.

    >>> from crypto_screening.market.screeners import OHLCVScreener
    >>>
    >>> screener = OHLCVScreener(
    >>>     symbol="BTC/USD", exchange="binance"
    >>> )
    >>>
    >>> screener.run(wait=True)
    >>>
    >>> print(screener.market.iloc[-1].splitlines()[0])
    >>>
    >>> while True:
    >>>     screener.wait_for_update()
    >>>
    >>>     print(screener.market.iloc[-1].splitlines()[-1])
    """

    __modifiers__ = Modifiers(**BaseScreener.__modifiers__)
    __modifiers__.excluded.append('task')

    __slots__ = "interval", "pro", "options", "task"

    INTERVAL = "1m"

    PRO = False

    OPTIONS = {}

    LENGTH = 0

    COLUMNS = (
        OPEN, HIGH, LOW, CLOSE, VOLUME,
        ASKS, BIDS, ASKS_VOLUME, BIDS_VOLUME
    )

    def __init__(
            self,
            symbol: str,
            exchange: str,
            interval: Optional[str] = None,
            pro: Optional[bool] = True,
            data: Optional[pd.DataFrame] = None,
            length: Optional[Union[bool, int]] = None,
            delay: Optional[Union[float, dt.timedelta]] = None,
            location: Optional[str] = None,
            options: Optional[Dict[str, Any]] = None,
            cancel: Optional[Union[float, dt.timedelta]] = None
    ) -> None:
        """
        Defines the class attributes.

        :param symbol: The symbol of the asset.
        :param exchange: The exchange to get source data from.
        :param interval: The interval for the data.
        :param data: The base dataset of the asset to add to.
        :param length: The length of the base dataset.
        :param location: The saving location for the data.
        :param delay: The delay for the process.
        :param pro: The value for the pro interface.
        :param options: The ccxt options.
        :param cancel: The time to cancel the waiting.
        """

        super().__init__(
            symbol=symbol, exchange=exchange, delay=delay,
            location=location, cancel=cancel
        )

        if pro is None:
            pro = self.PRO
        # end if

        if length is None:
            length = self.LENGTH
        # end if

        self.pro = pro
        self.interval = interval or self.INTERVAL
        self.options = options or {}

        self.task = None

        self.market = self.validate_data(data, length=length)
    # end __init__

    def __getstate__(self) -> Dict[str, Any]:
        """
        Returns the data of the object.

        :return: The state of the object.
        """

        data = super().__getstate__()

        data["task"] = None

        return data
    # end __getstate__

    def validate_data(self, data: Any, length: Optional[int]) -> pd.DataFrame:
        """
        Validates the asset data value.

        :param data: The asset data.
        :param length: The length of the data to add.

        :return: The validates source.
        """

        if not all(
            hasattr(self, name) for name in ["exchange", "interval"]
        ):
            raise AttributeError(
                "Source and interval attributes must be defined "
                "before attempting to validate the data parameter data."
            )
        # end if

        if (
            (data is None) and
            (
                (length is None) or
                (length == 0) or
                (length is False) or
                (
                    isinstance(length, int) and
                    not (0 < length <= 500)
                )
            )
        ):
            data = pd.DataFrame(
                {column: [] for column in self.COLUMNS},
                index=[]
            )

        elif (data is None) and (isinstance(length, int)):
            if 0 < length <= 500:
                try:
                    exchange = getattr(ccxt, self.exchange)(self.options)

                    data = self.data_to_dataset(
                        exchange.fetch_ohlcv(
                            symbol=self.symbol,
                            timeframe=self.interval,
                            limit=length
                        )
                    )

                except Exception as e:
                    warnings.warn(str(e))

                    data = pd.DataFrame(
                        {column: [] for column in self.COLUMNS},
                        index=[]
                    )
                # end try

            else:
                raise ValueError(
                    f"Length must be a positive int between "
                    f"{1} and {500} when data is not defined, "
                    f"not: {length}."
                )
            # end if
        # end if

        return data
    # end validate_data

    def data_to_dataset(self, data: Iterable[Iterable]) -> pd.DataFrame:
        """
        Adjusts the dataset to an asset Open, High, Low, Close, Bids, Asks, Volume dataset.

        :param data: The data to adjust.

        :return: The asset dataset.
        """

        data = pd.DataFrame(data)

        index_column_name = list(data.columns)[0]

        data.index = pd.to_datetime(data[index_column_name], unit="ms")
        del data[index_column_name]
        data.index.name = DATE_TIME
        data.columns = list(OHLCV_COLUMNS)

        if len(self.market) == 0:
            asks = [np.nan] * len(data)
            bids = [np.nan] * len(data)

        else:
            asks = (
                self.market[ASKS].iloc
                [-len(data):].values[:]
            )
            bids = (
                self.market[BIDS].iloc
                [-len(data):].values[:]
            )
        # end if

        if ASKS in data:
            data[ASKS].values[:] = asks

        else:
            data[ASKS] = asks
        # end if

        if BIDS in data:
            data[BIDS].values[:] = bids

        else:
            data[BIDS] = bids
        # end if

        return data[list(self.COLUMNS)]
    # end data_to_dataset

    def dataset_path(self, location: Optional[str] = None) -> str:
        """
        Creates the path to the saving file for the screener object.

        :param location: The saving location of the dataset.

        :return: The saving path for the dataset.
        """

        return super().dataset_path(location=location).replace(
            '.csv', f'_{self.interval}.csv'
        )
    # end dataset_path

    async def async_get_market(self) -> Dict[str, float]:
        """
        Gets the market data.

        :return: The bids and asks.
        """

        exchange = configure_exchange(
            exchange=self.exchange.lower(), pro=self.pro,
            options=self.options
        )

        method = None

        if hasattr(exchange, "fetch_tickers"):
            method = exchange.fetch_tickers

        elif hasattr(exchange, "watch_tickers"):
            method = exchange.watch_tickers
        # end if

        data = await method(symbols=[self.symbol])
        data: Dict[str, Union[float, Dict[str, float]]]

        if self.symbol in data:
            data = data[self.symbol]
        # end if

        data[ASKS.lower()] = data.get("ask")
        data[BIDS.lower()] = data.get("bid")
        data[ASKS_VOLUME.lower()] = data.get("askVolume")
        data[BIDS_VOLUME.lower()] = data.get("bidVolume")
        saved_volume = data.get("volume", data.get('baseVolume'))

        if 'info' in data and VOLUME.lower() in data['info']:
            saved_volume = float(data['info'][VOLUME.lower()])
        # end if

        data = {
            key: (
                float(data[key.lower()]) if
                isinstance(data[key.lower()], str) else
                data[key.lower()]
            ) for key in self.COLUMNS if key.lower() in data
        }

        try:
            ohlcv = await exchange.fetch_ohlcv(
                self.symbol, timeframe='1m', limit=1
            )

            ohlcv = {
                column: float(value) for column, value in
                zip(OHLCV_COLUMNS, ohlcv[0][1:])
            }

            data.update(ohlcv)

        except Exception as e:
            warnings.warn(f"{type(e).__name__}: {e}")
        # end try

        data.setdefault(VOLUME, saved_volume)

        await exchange.close()

        return data
    # end async_get_market

    async def async_update_market(self) -> None:
        """Updates the market data."""

        data = await self.async_get_market()

        self.market.loc[dt.datetime.now()] = data
    # end async_update_market

    def update_market(self) -> None:
        """Updates the market data."""

        asyncio.run(self.async_update_market())
    # end update_market

    def get_market(self) -> Dict[str, float]:
        """
        Gets the market data.

        :return: The market data.
        """

        return asyncio.run(self.async_get_market())
    # end get_market

    async def async_run_loop(self) -> None:
        """Runs the processes of price screening."""

        self._screening = True

        delay = interval_to_total_time(self.interval).seconds

        while self.screening:
            start = time.time()

            try:
                await self.async_update_market()

            except Exception as e:
                warnings.warn(f"{type(e).__name__}: {e}")
            # end try

            end = time.time()

            if delay:
                time.sleep(max([delay - (end - start), 0]))
            # end if
        # end while
    # end async_run

    def screening_loop(self) -> None:
        """Runs the process of the price screening."""

        task = self.async_run_loop()

        loop = asyncio.new_event_loop()

        self.task = loop.create_task(task)

        if not loop.is_running():
            loop.run_forever()
        # end if
    # end screening_loop

    def stop(self) -> None:
        """Stops the screening process."""

        super().stop()

        if self.task is not None:
            self.task.cancel()
        # end if
    # end stop
# end OHLCVScreener

class MarketOHLCVRecorder(MarketRecorder):
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

    >>> from crypto_screening.market.screeners import market_ohlcv_recorder
    >>>
    >>> market = {'binance': ['BTC/USDT'], 'bittrex': ['ETH/USDT']}
    >>>
    >>> recorder = market_ohlcv_recorder(data=market)
    """

    COLUMNS = OHLCVScreener.COLUMNS

    def ohlcv(self, exchange: str, symbol: str) -> pd.DataFrame:
        """
        Returns the market data of the symbol from the exchange.

        :param exchange: The source name of the exchange.
        :param symbol: The symbol of the pair.

        :return: The dataset of the spread data.
        """

        return self.data(exchange=exchange, symbol=symbol)
    # end ohlcv
# end MarketOHLCVRecorder

def create_ohlcv_dataframe() -> pd.DataFrame:
    """
    Creates a dataframe for the order book data.

    :return: The dataframe.
    """

    return create_market_dataframe(
        columns=MarketOHLCVRecorder.COLUMNS
    )
# end create_orderbook_dataframe

def create_ohlcv_market(data: Dict[str, Iterable[str]]) -> Dict[str, Dict[str, pd.DataFrame]]:
    """
    Creates the dataframes of the market data.

    :param data: The market data.

    :return: The dataframes of the market data.
    """

    return {
        exchange.lower(): {
            symbol.upper(): create_ohlcv_dataframe()
            for symbol in data[exchange]
        } for exchange in data
    }
# end create_ohlcv_market

def market_ohlcv_recorder(data: Dict[str, Iterable[str]]) -> MarketOHLCVRecorder:
    """
    Creates the market recorder object for the data.

    :param data: The market data.

    :return: The market recorder object.
    """

    return MarketOHLCVRecorder(
        market=create_ohlcv_market(data=data)
    )
# end market_ohlcv_recorder

class MarketOHLCVScreener(BaseMultiScreener):
    """
    A class to represent an asset price screener.

    Using this class, you can create a screener object to
    screen the market ask and bid data for a specific asset in
    a specific exchange at real time.

    Parameters:

    - exchanges:
        The data of exchanges and their symbols to screen.

    - interval:
        The interval for the time between data points in the dataset.

    - delay:
        The delay to wait between each data fetching.

    - length:
        An initial dataset length to start with.

    - locaion:
        The saving location for the saved data of the screener.

    - pro:
        The value to use the pro interface.

    - options:
        The ccxt options for the backend screening process.

    - cencel:
        The time to cancel screening process after no new data is fetched.

    >>> from crypto_screening.market.screeners import MarketOHLCVScreener
    >>>
    >>> screener = MarketOHLCVScreener(
    >>>     data={
    >>>         "binance": ["BTC/USDT", "AAVE/EUR"],
    >>>         "bittrex": ["GRT/USD", "BTC/USD"]
    >>>     }
    >>> )
    >>>
    >>> screener.run(wait=True)
    """

    __slots__ = "interval", "pro", "options", "task", "exchanges", "length"

    INTERVAL = OHLCVScreener.INTERVAL

    PRO = OHLCVScreener.PRO

    OPTIONS = OHLCVScreener.OPTIONS

    LENGTH = OHLCVScreener.LENGTH
    CANCEL = OHLCVScreener.CANCEL

    COLUMNS = OHLCVScreener.COLUMNS

    screeners: List[OHLCVScreener]

    def __init__(
            self,
            interval: Optional[str] = None,
            delay: Optional[Union[float, dt.timedelta]] = None,
            length: Optional[Union[int, bool]] = None,
            location: Optional[str] = None,
            pro: Optional[bool] = None,
            options: Optional[Dict[str, Any]] = None,
            cancel: Optional[Union[float, dt.timedelta]] = None,
            screeners: Optional[Iterable[OHLCVScreener]] = None,
            recorder: Optional[MarketRecorder] = None
    ) -> None:
        """
        Defines the class attributes.

        :param interval: The interval of the data to load.
        :param pro: The value to use the pro interface.
        :param location: The saving location for the data.
        :param delay: The delay between each data fetching request.
        :param length: The length of the data to get in each request.
        :param options: The ccxt options.
        :param cancel: The time it takes to cancel a non-updating screener.
        :param screeners: The create_screeners for the multi-screener object.
        :param recorder: The recorder object for recording the data.
        """

        super().__init__(
            delay=delay, cancel=cancel,
            location=location, recorder=recorder or MarketOHLCVRecorder(
                market=structure_screener_datasets(screeners=screeners)
            )
        )

        if pro is None:
            pro = self.PRO
        # end if

        if length is None:
            length = self.LENGTH
        # end if

        self.options = options or self.OPTIONS
        self.interval = interval or self.INTERVAL
        self.pro = pro
        self.length = length

        self.screeners[:] = list(screeners or []) or self.create_screeners()
    # end Screener

    def create_screener(
            self,
            symbol: str,
            exchange: str,
            pro: Optional[bool] = True,
            length: Optional[Union[bool, int]] = None,
            delay: Optional[Union[float, dt.timedelta]] = None,
            location: Optional[str] = None,
            options: Optional[Dict[str, Any]] = None,
            cancel: Optional[Union[float, dt.timedelta]] = None,
            container: Optional[Dict[str, Dict[str, OHLCVScreener]]] = None
    ) -> OHLCVScreener:
        """
        Creates the screener and inserts it into the container.

        :param container: The container to contain the new screener.
        :param symbol: The symbol of the screener.
        :param exchange: The source of the data.
        :param pro: The value to use the pro interface.
        :param location: The saving location for the data.
        :param delay: The delay between each data fetching request.
        :param length: The length of the data to get in each request.
        :param options: The ccxt options.
        :param cancel: The time it takes to cancel a non-updating screener.
        """

        if container is None:
            container = {}
        # end if

        if pro is None:
            pro = self.pro
        # end if

        if length is None:
            length = self.length
        # end if

        if cancel is None:
            cancel = self.cancel
        # end if

        if delay is None:
            delay = self.delay
        # end if

        container.setdefault(exchange, {})[symbol] = OHLCVScreener(
            symbol=symbol, exchange=exchange,
            options=options, interval=self.interval,
            pro=pro, delay=delay, length=length,
            location=location or self.location, cancel=cancel
        )

        return container[exchange][symbol]
    # end create_screener

    def _create_screener(
            self,
            symbol: str,
            exchange: str,
            pro: Optional[bool] = True,
            length: Optional[Union[bool, int]] = None,
            delay: Optional[Union[float, dt.timedelta]] = None,
            location: Optional[str] = None,
            options: Optional[Dict[str, Any]] = None,
            cancel: Optional[Union[float, dt.timedelta]] = None,
            container: Optional[Dict[str, Dict[str, Optional[OHLCVScreener]]]] = None,
    ) -> OHLCVScreener:
        """
        Creates the screener and inserts it into the container.

        :param container: The container to contain the new screener.
        :param symbol: The symbol of the screener.
        :param exchange: The source of the data.
        :param pro: The value to use the pro interface.
        :param location: The saving location for the data.
        :param delay: The delay between each data fetching request.
        :param length: The length of the data to get in each request.
        :param options: The ccxt options.
        :param cancel: The time it takes to cancel a non-updating screener.
        """

        if container is None:
            container = {}
        # end if

        try:
            return self.create_screener(
                symbol=symbol, exchange=exchange,
                container=container, pro=pro, length=length,
                delay=delay, location=location,
                options=options, cancel=cancel
            )

        except ValueError as e:
            warnings.warn(str(e))

            container[symbol] = None
        # end try
    # end _create_screener

    def _create_screeners(
            self,
            symbols: Iterable[str],
            exchange: str,
            pro: Optional[bool] = True,
            length: Optional[Union[bool, int]] = None,
            delay: Optional[Union[float, dt.timedelta]] = None,
            location: Optional[str] = None,
            options: Optional[Dict[str, Any]] = None,
            cancel: Optional[Union[float, dt.timedelta]] = None,
            container: Optional[Dict[str, Dict[str, Optional[OHLCVScreener]]]] = None,
            wait: Optional[bool] = True
    ) -> Dict[str, Optional[OHLCVScreener]]:
        """
        Creates the screener and inserts it into the container.

        :param container: The container to contain the new screener.
        :param symbols: The symbol of the screener.
        :param exchange: The source of the data.
        :param wait: The value to wait for the creation of the screeners.
        :param pro: The value to use the pro interface.
        :param location: The saving location for the data.
        :param delay: The delay between each data fetching request.
        :param length: The length of the data to get in each request.
        :param options: The ccxt options.
        :param cancel: The time it takes to cancel a non-updating screener.
        """

        if container is None:
            container = {}
        # end if

        symbols = list(symbols)

        callers = []

        for symbol in symbols:
            callers.append(
                Caller(
                    target=self._create_screener,
                    kwargs=dict(
                        container=container,
                        symbol=symbol, exchange=exchange,
                        pro=pro, length=length,
                        delay=delay, location=location,
                        options=options, cancel=cancel
                    )
                )
            )
        # end for

        multi_threaded_call(callers=callers, wait=wait)

        return container
    # end _create_screeners

    def create_screeners(
            self,
            pro: Optional[bool] = True,
            length: Optional[Union[bool, int]] = None,
            delay: Optional[Union[float, dt.timedelta]] = None,
            location: Optional[str] = None,
            options: Optional[Dict[str, Any]] = None,
            cancel: Optional[Union[float, dt.timedelta]] = None,
    ) -> List[OHLCVScreener]:
        """
        Initializes the create_screeners.

        :param pro: The value to use the pro interface.
        :param location: The saving location for the data.
        :param delay: The delay between each data fetching request.
        :param length: The length of the data to get in each request.
        :param options: The ccxt options.
        :param cancel: The time it takes to cancel a non-updating screener.

        :return: The created screener objects.
        """

        market: Dict[str, Dict[str, OHLCVScreener]] = {}

        callers = []

        for exchange, symbols in self.recorder.structure().items():
            market.setdefault(exchange, {})

            callers.append(
                Caller(
                    target=self._create_screeners,
                    kwargs=dict(
                        container=market, symbols=symbols,
                        exchange=exchange, wait=False,
                        pro=pro, length=length,
                        delay=delay, location=location,
                        options=options, cancel=cancel
                    )
                )
            )
        # end for

        multi_threaded_call(callers=callers)

        screeners = []

        for exchange in market.values():
            for symbol, screener in exchange.copy().items():
                if isinstance(screener, OHLCVScreener):
                    screeners.append(screener)

                else:
                    exchange.pop(symbol)
                # end if
            # end for
        # end for

        return screeners
    # end create_screeners

    def ohlcv(self, exchange: str, symbol: str) -> pd.DataFrame:
        """
        Returns the market data of the symbol from the exchange.

        :param exchange: The source name of the exchange.
        :param symbol: The symbol of the pair.

        :return: The dataset of the spread data.
        """

        return self.recorder.ohlcv(exchange=exchange, symbol=symbol)
    # end ohlcv

    async def async_get_market(self) -> Dict[str, Dict[str, Dict[str, float]]]:
        """
        Gets the market data.

        :return: The market data.
        """

        market = {exchange: {} for exchange in self.exchanges}

        for screener in self.screeners:
            market[screener.exchange][screener.symbol] = (
                await screener.async_get_market()
            )
        # end for

        return market
    # end async_get_market

    async def async_update_market(self) -> None:
        """Updates the market data."""

        for screener in self.screeners:
            await screener.async_update_market()
        # end for
    # end async_update_market

    def update_market(self) -> None:
        """Updates the market data."""

        asyncio.run(self.async_update_market())
    # end update_market

    def get_market(self) -> Dict[str, Dict[str, Dict[str, float]]]:
        """
        Gets the market data.

        :return: The market data.
        """

        return asyncio.run(self.async_get_market())
    # end get_market

    def stop(self) -> None:
        """Stops the screening process."""

        super().stop()

        for screener in self.screeners:
            screener.stop()
        # end for
    # end stop

    def terminate(self) -> None:
        """Stops the screening process."""

        super().terminate()

        for screener in self.screeners:
            screener.terminate()
        # end for
    # end terminate

    def start_screening(
            self,
            save: Optional[bool] = True,
            timeout: Optional[Union[float, dt.timedelta, dt.datetime]] = None
    ) -> None:
        """
        Starts the screening process.

        :param save: The value to save the data.
        :param timeout: The valur to add a timeout to the process.
        """

        if self.screening:
            warnings.warn(f"Screening process of {self} is already running.")

            return
        # end if

        for screener in self.screeners:
            screener.run(
                timeout=timeout, wait=False,
                block=False, save=save
            )
        # end for
    # end start_screening

    def run(
            self,
            screen: Optional[bool] = True,
            save: Optional[bool] = True,
            block: Optional[bool] = False,
            update: Optional[bool] = True,
            wait: Optional[Union[bool, float, dt.timedelta, dt.datetime]] = False,
            timeout: Optional[Union[float, dt.timedelta, dt.datetime]] = None
    ) -> None:
        """
        Runs the process of the price screening.

        :param screen: The value to start the screening.
        :param save: The value to save the data.
        :param wait: The value to wait after starting to run the process.
        :param block: The value to block the execution.
        :param update: The value to update the screeners.
        :param timeout: The valur to add a timeout to the process.
        """

        if screen:
            self.start_screening(save=save, timeout=timeout)
        # end if

        super().run(
            screen=False, save=False, block=block,
            update=update, wait=wait, timeout=timeout
        )
    # end run
# end MarketOHLCVScreener

Market = Dict[str, Dict[str, pd.DataFrame]]

def market_ohlcv_screener(
        data: Dict[str, Iterable[str]],
        interval: Optional[str] = None,
        delay: Optional[Union[float, dt.timedelta]] = None,
        length: Optional[Union[int, bool]] = None,
        location: Optional[str] = None,
        pro: Optional[bool] = None,
        options: Optional[Dict[str, Any]] = None,
        cancel: Optional[Union[float, dt.timedelta]] = None,
        market: Optional[Market] = None,
        recorder: Optional[MarketOHLCVRecorder] = None,
) -> MarketOHLCVScreener:
    """
    Creates the market screener object for the data.

    :param data: The market data.
    :param market: The object to fill with the crypto feed record.
    :param recorder: The recorder object for recording the data.
    :param interval: The interval of the data to load.
    :param pro: The value to use the pro interface.
    :param location: The saving location for the data.
    :param delay: The delay between each data fetching request.
    :param length: The length of the data to get in each request.
    :param options: The ccxt options.
    :param cancel: The time it takes to cancel a non-updating screener.

    :return: The market screener object.
    """

    screener = MarketOHLCVScreener(
        recorder=recorder or MarketOHLCVRecorder(
            market=market or create_ohlcv_market(data=data)
        ),
        location=location, cancel=cancel, delay=delay,
        options=options, pro=pro, interval=interval, length=length
    )

    return screener
# end market_orderbook_recorder