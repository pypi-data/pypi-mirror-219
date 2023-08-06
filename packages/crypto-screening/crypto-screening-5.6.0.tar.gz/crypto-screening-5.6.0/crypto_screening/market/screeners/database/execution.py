# exchange.py

import os
import sys
from pathlib import Path
import subprocess
import threading
import time
from abc import ABCMeta
from typing import (
    Optional, Iterable, Dict, Union,
    List, TypeVar, Type
)
import argparse

from attr import define

from represent import represent

from crypto_screening.market.screeners.combined import (
    combined_market_screener
)
from crypto_screening.market.screeners.ohlcv import (
    OHLCVMarketScreener, OHLCVScreener
)
from crypto_screening.market.screeners.orders import (
    OrdersMarketScreener, OrdersScreener
)
from crypto_screening.market.screeners.trades import (
    TradesMarketScreener, TradesScreener
)
from crypto_screening.market.screeners.orderbook import (
    OrderbookMarketScreener, OrderbookScreener
)
from crypto_screening.market.screeners.combined import (
    CombinedMarketScreener
)

__all__ = [
    "exchange_service_parameters",
    "symbols_to_parameter",
    "arguments_parser",
    "parameter_to_symbols",
    "arguments_parser_parameters",
    "exchange_database_service_main",
    "ExchangeDatabaseServiceExecutionControllers",
    "ExchangeDatabaseService",
    "exchange_database_services",
    "activate_virtualenv_command"
]

EXCHANGE = "--exchange"
SYMBOLS = "--symbols"
ROOT = "--root"
DATABASES = "--databases"
SILENT = "--silent"
LOCATION = "--location"
REFRESH = "--refresh"
TIMEOUT = "--timeout"
WAIT = "--wait"
SAVE = "--save"
LOAD = "--load"
PID = "--pid"

def activate_virtualenv_command() -> Optional[str]:
    """
    Returns the command to activate the virtual env.

    :return: The command to activate the venv.
    """

    python_startup = (
        Path(os.path.split(sys.executable)[0]) /
        Path('activate')
    )

    if not python_startup.exists():
        return
    # end if

    return (
        f"{'' if 'win' in sys.platform else 'source '}"
        f"{python_startup}"
    )
# end activate_virtualenv_command

def symbols_to_parameter(symbols: Iterable[str]) -> str:
    """
    Returns the parameter for the symbols.

    :param symbols: The symbols to process.

    :return: The parameter string.
    """

    return f"[{','.join(symbols)}]"
# end symbols_to_parameter

def databases_to_parameter(databases: Iterable[str]) -> str:
    """
    Returns the parameter for the databases.

    :param databases: The databases to process.

    :return: The parameter string.
    """

    return f"[{','.join(databases)}]"
# end databases_to_parameter

def parameter_to_symbols(parameter: str) -> Iterable[str]:
    """
    Converts the parameterized symbols to the original symbols.

    :param parameter: The parameter to process.

    :return: The original symbols.
    """

    symbols_data = parameter

    for char in "[]{}()":
        symbols_data = symbols_data.strip(char)
    # end for

    symbols_data = symbols_data.strip(" ")
    return symbols_data.split(",")
# end parameter_to_symbols

def parameter_to_databases(parameter: str) -> Iterable[str]:
    """
    Converts the parameterized symbols to the original symbols.

    :param parameter: The parameter to process.

    :return: The original symbols.
    """

    databases_data = parameter

    for char in "[]{}()":
        databases_data = databases_data.strip(char)
    # end for

    databases_data = databases_data.strip(" ")
    return databases_data.split(",")
# end parameter_to_databases

def exchange_service_parameters(
        exchange: str,
        symbols: Iterable[str],
        root: Optional[str] = None,
        databases: Optional[Iterable[str]] = None,
        silent: Optional[bool] = None,
        location: Optional[str] = None,
        refresh: Optional[int] = None,
        wait: Optional[int] = None,
        timeout: Optional[int] = None,
        save: Optional[bool] = None,
        load: Optional[bool] = None,
        pid: Optional[int] = None
) -> str:
    """
    Defines the parameters for the service.

    :param exchange: The exchange to screen.
    :param symbols: The symbols of the exchange to screen.
    :param root: The root for serving the service.
    :param databases: The host for the service.
    :param silent: The value to silence the service.
    :param location: The saving location for the data.
    :param refresh: The value to refresh the screening.
    :param wait: The value to wait before initialization.
    :param timeout: The timeout value for the service.
    :param load :The value to load the dataset.
    :param save: The value to save the data.
    :param pid: The PID of the master process.

    :return: The string for the command to run the service.
    """

    return (
        (f"{EXCHANGE}={exchange} " if exchange is not None else '') +
        (f"{SYMBOLS}={symbols_to_parameter(symbols)} " if symbols is not None else '') +
        (f"{DATABASES}={databases_to_parameter(databases)} " if databases is not None else '') +
        (f"{ROOT}={root} " if root is not None else '') +
        (f"{SILENT}={silent} " if silent is not None else '') +
        (f"{LOCATION}={location} " if location is not None else '') +
        (f"{REFRESH}={refresh} " if refresh is not None else '') +
        (f"{WAIT}={wait} " if wait is not None else '') +
        (f"{TIMEOUT}={timeout} " if timeout is not None else '') +
        (f"{SAVE}={save} " if save is not None else '') +
        (f"{LOAD}={load} " if load is not None else '') +
        (f"{PID}={pid} " if pid is not None else '')
    )
# end exchange_service_parameters

MarketScreener = Union[
    OrderbookMarketScreener,
    OHLCVMarketScreener,
    OrdersMarketScreener,
    TradesMarketScreener,
    CombinedMarketScreener
]
Screener = Union[
    OrderbookScreener,
    OHLCVScreener,
    OrdersScreener,
    TradesScreener
]

@define(repr=False)
@represent
class ExchangeDatabaseServiceExecutionControllers:
    """A class to contain the execution objects."""

    market: Optional[MarketScreener] = None
    screeners: Optional[Iterable[Screener]] = None
# end ExchangeDatabaseServiceExecutionControllers

@represent
class ExchangeDatabaseService(metaclass=ABCMeta):
    """A class to represent the exchange service."""

    def __init__(
            self,
            exchange: str,
            symbols: Iterable[str],
            market: Optional[MarketScreener] = None,
            screeners: Optional[Iterable[Screener]] = None,
            script: Optional[str] = None,
            command: Optional[str] = None,
            activation: Optional[Union[bool, str]] = None,
            block: Optional[bool] = None,
            root: Optional[str] = None,
            databases: Optional[Iterable[str]] = None,
            silent: Optional[bool] = None,
            location: Optional[str] = None,
            refresh: Optional[int] = None,
            wait: Optional[int] = None,
            timeout: Optional[int] = None,
            save: Optional[bool] = None,
            load: Optional[bool] = None,
            pid: Optional[int] = None
    ) -> None:
        """
        Defines the parameters for the service.

        :param exchange: The exchange to screen.
        :param symbols: The symbols of the exchange to screen.
        :param script: The script to run.
        :param activation: The activation command.
        :param block: The value to block the process.
        :param root: The root for serving the service.
        :param databases: The host for the service.
        :param silent: The value to silence the service.
        :param location: The saving location for the data.
        :param refresh: The value to refresh the screening.
        :param wait: The value to wait before initialization.
        :param timeout: The timeout value for the service.
        :param save: The value to save the data.
        :param load :The value to load the dataset.
        :param pid: The PID of the master process.
        """

        if activation is None:
            activation = True

        elif activation is True:
            activation = activate_virtualenv_command()
        # end if

        if block is None:
            block = True
        # end if

        self._running = False
        self._serving = False

        self.exchange = exchange
        self.symbols = list(symbols)
        self.root = root
        self.script = script
        self.activation = activation
        self.command = command
        self.silent = silent
        self.location = location
        self.refresh = refresh
        self.wait = wait
        self.timeout = timeout
        self.save = save
        self.pid = pid
        self.block = block
        self.market = market
        self.screeners = screeners
        self.load = load
        self.databases = databases or self.generate_databases()

        self.process: Optional[subprocess.Popen] = None
        self.controllers: Optional[ExchangeDatabaseServiceExecutionControllers] = None
    # end __init__

    @property
    def running(self) -> bool:
        """
        Returns the info of the process being active.

        :return: The activation value.
        """

        return self._running
    # end running

    @property
    def serving(self) -> bool:
        """
        Returns the info of the process being active.

        :return: The activation value.
        """

        return self._serving
    # end serving

    def generate_databases(self) -> List[str]:
        """
        Generates the list of databases.

        :return: The database paths.
        """

        return [f'sqlite:///{self.location or "databases"}/{self.exchange}.sqlite']
    # end generate_databases

    def create(
            self,
            market: Optional[MarketScreener] = None,
            screeners: Optional[Iterable[Screener]] = None
    ) -> None:
        """
        Runs the updating loop.

        :param market: The market object.
        :param screeners: The screeners for the service.
        """

        market = market or self.market
        screeners = screeners or self.screeners

        if screeners is None:
            market = market or combined_market_screener(
                data={self.exchange: self.symbols},
                location=self.location, databases=self.databases
            )

            screeners = market.screeners

            self.market = market
        # end if

        self.screeners = screeners
    # end create

    def start(self) -> None:
        """Starts the service."""

        if isinstance(self.pid, int) and (self.pid not in (True, False)):
            def check() -> None:
                """Checks for exiting."""

                while True:
                    try:
                        os.kill(self.pid, 0)

                    except OSError:
                        return quit()
                    # end try

                    time.sleep(1)
                # end while
            # end check

            threading.Thread(target=check).start()
        # end if

        self.market.run(
            save=False, block=self.block,
            timeout=self.timeout, wait=self.wait
        )
    # end start

    def run(
            self,
            market: Optional[MarketScreener] = None,
            screeners: Optional[Iterable[Screener]] = None
    ) -> ExchangeDatabaseServiceExecutionControllers:
        """
        Runs the service.

        :param market: The master screener.
        :param screeners: The screeners for the service.
        """

        self.create(market=market, screeners=screeners)

        self.start()

        self.controllers = ExchangeDatabaseServiceExecutionControllers(
            market=self.market, screeners=self.screeners
        )

        if self.load:
            self.market.load_datasets()
        # end if

        self._running = True

        return self.controllers
    # end run

    def terminate(self) -> None:
        """Deletes the object and cleans the program."""

        if self.serving:
            self.process.terminate()
        # end if

        if self.running:
            self.service.terminate()
        # end if
    # end terminate

    def serve(self) -> None:
        """Creates the service and runs it."""

        command = self.command or self.generate_command()

        self.process = subprocess.Popen(command, shell=True)

        self._serving = True
    # end serve

    def command_parameters(self) -> Dict[str, Union[None, str, int, float, str, List[str]]]:
        """
        Returns the parameters for the command to run the service.

        :return: The command parameters.
        """

        return dict(
            exchange=self.exchange, symbols=self.symbols,
            root=self.root, silent=self.silent, save=self.save,
            databases=self.databases, location=self.location,
            wait=self.wait, timeout=self.timeout,
            refresh=self.refresh, pid=self.pid, load=self.load
        )
    # end command_parameters

    def generate_command(self) -> str:
        """
        Generates an execution command for the service.

        :return: The generated command.
        """

        parameters_command = exchange_service_parameters(
            **self.command_parameters()
        )

        command = f"{self.script} {parameters_command}"
        return (
            (f"{self.activation} & " + command)
            if self.activation else command
        )
    # end generate_command
# end ExchangeDatabaseService

_E = TypeVar("_E")

def exchange_database_services(
        data: Dict[str, Iterable[str]],
        script: str,
        root: Optional[bool] = False,
        activation: Optional[Union[bool, str]] = None,
        databases: Optional[Iterable[str]] = None,
        silent: Optional[bool] = None,
        location: Optional[str] = None,
        refresh: Optional[int] = None,
        wait: Optional[int] = None,
        timeout: Optional[int] = None,
        load: Optional[bool] = None,
        save: Optional[bool] = None
) -> List[ExchangeDatabaseService]:
    """
    Runs the server of the data service.

    :param data: The exchanges and symbols data.
    :param script: The script to run.
    :param activation: The activation command.
    :param databases: The host for the service.
    :param silent: The value to silence the service.
    :param location: The saving location for the data.
    :param refresh: The value to refresh the screening.
    :param wait: The value to wait before initialization.
    :param timeout: The timeout value for the service.
    :param save: The value to save the data.
    :param load: The value to load the datasets.
    :param root: The value to add roots for the services.
    """

    base: Type[ExchangeDatabaseService]

    return [
        ExchangeDatabaseService(
            exchange=exchange, symbols=symbols, databases=databases,
            silent=silent, location=location, script=script,
            wait=wait, timeout=timeout, refresh=refresh, load=load,
            activation=activation, save=save, pid=os.getpid(),
            root=(exchange if root else None)
        ) for exchange, symbols in data.items()
    ]
# end exchange_database_services

def arguments_parser() -> argparse.ArgumentParser:
    """
    Creates the arguments' parser.

    :return: The arguments parser object.
    """

    parser = argparse.ArgumentParser(
        description=(
            'Multi-symbol multi-exchange crypto '
            'orderbook screening service.'
        )
    )

    parser.add_argument(
        EXCHANGE, help='exchange name to screen'
    )
    parser.add_argument(
        SYMBOLS, help='symbols for the exchange to screen'
    )
    parser.add_argument(
        ROOT, help="root path for the service endpoints",
        default=None, type=str
    )
    parser.add_argument(
        DATABASES, help="the paths to the databases",
        default=None, type=str
    )
    parser.add_argument(
        SILENT, help="silent the output",
        default=None, type=bool
    )
    parser.add_argument(
        LOCATION, help="saving location for the datasets",
        default=None, type=str
    )
    parser.add_argument(
        REFRESH, help="refreshing interval (int seconds)",
        default=None, type=int
    )
    parser.add_argument(
        TIMEOUT, help="timeout duration (int seconds)",
        default=None, type=int
    )
    parser.add_argument(
        WAIT, help="waiting time duration (int seconds)",
        default=None, type=int
    )
    parser.add_argument(
        SAVE, help="saving the collected data",
        default=None, type=bool
    )
    parser.add_argument(
        LOAD, help="load the data on start",
        default=None, type=bool
    )
    parser.add_argument(
        PID, help="the PID of the master process.",
        default=None, type=bool
    )

    return parser
# end arguments_parser

def arguments_parser_parameters(
        parser: argparse.ArgumentParser, crush: Optional[bool] = False
) -> Dict[str, Union[bool, int, str, Iterable[str]]]:
    """
    Extracts the parameters from the parser.

    :param parser: The parser object.
    :param crush: The value to crush for errors.

    :return: The parameters.
    """

    args = parser.parse_args()

    if (args.exchange, args.symbols) == (None, None):
        error = "Both exchange and symbols must be provided."

    elif args.exchange is None:
        error = "Exchange must be provided."
    # end if

    elif args.symbols is None:
        error = "Symbols must be provided."

    else:
        exchange = args.exchange
        symbols = parameter_to_symbols(args.symbols)
        databases = parameter_to_databases(args.databases)

        return dict(
            exchange=exchange, symbols=symbols, refresh=args.refresh or 0,
            databases=databases, silent=args.silent or False,
            root=args.root, timeout=args.timeout or 0, wait=args.wait or 0,
            save=args.save or False, pid=args.pid, load=args.load
        )
    # end if

    if all(value is None for value in args.__dict__.values()):
        parser.print_help()
        quit()

    elif crush:
        raise ValueError(error)

    else:
        print(error)
        quit()
    # end if
# end arguments_parser_parameters

def exchange_database_service_main() -> None:
    """Runs the main function for the service."""

    parser = arguments_parser()

    parameters = arguments_parser_parameters(parser)

    ExchangeDatabaseService(**parameters).run()
# end exchange_database_service_main