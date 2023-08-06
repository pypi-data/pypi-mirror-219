# data.py

import os
import time
import datetime as dt
from typing import (
    Optional, Dict, Any, List,
    Iterable, Union, Tuple
)

import pandas as pd

from sqlalchemy import create_engine, Engine, inspect, text

from multithreading import Caller, multi_threaded_call

from crypto_screening.dataset import DATE_TIME
from crypto_screening.symbols import (
    symbol_to_parts, adjust_symbol, parts_to_symbol
)
from crypto_screening.market.screeners.base import BaseScreener

__all__ = [
    "insert_database_record",
    "extract_database_record",
    "validate_database_engines",
    "parts_database_table_name",
    "database_table_name_to_parts",
    "extract_database_tables",
    "database_file_path",
    "await_database_creation",
    "await_all_databases_creation",
    "extract_data_into_screener_dataset",
    "extract_database_length"
]

def parts_database_table_name(
        name: str, exchange: str, symbol: str, interval: Optional[str] = None
) -> str:
    """
    Creates the database table name.

    :param name: The name for the data.
    :param exchange: The exchange name of the data.
    :param symbol: The symbol of the data.
    :param interval: The interval.

    :return: The table name.
    """

    return (
        f"{name}__"
        f"{exchange}__"
        f"{'_'.join(symbol_to_parts(adjust_symbol(symbol)))}__"
        f"{interval or ''}"
    )
# end parts_database_table_name

def database_table_name_to_parts(table: str) -> Tuple[str, str, str, Optional[str]]:
    """
    Converts the table name to the naming parts.

    :param table: The table name.

    :return: The name parts.
    """

    values = table.split("__")

    symbol = parts_to_symbol(*values[-2].split("_"))

    values.remove(values[-2])
    interval = values[-1] or None
    name = values[0]
    exchange = values[1]

    return name, exchange, symbol, interval
# end database_table_name_to_parts

def database_file_path(path: str) -> str:
    """
    Finds the name of the database file.

    :param path: The path to the database.

    :return: The file path to the database.
    """

    path = path[path.find("://") + 3:]

    if path.startswith("/"):
        path = path[1:]
    # end if

    return path
# end database_file_path

def await_database_creation(path: str) -> None:
    """
    Waits for the database to be created.

    :param path: The path to the database.
    """

    path = database_file_path(path)

    while not os.path.exists(path):
        time.sleep(0.001)
    # end while
# end await_database_creation

def await_all_databases_creation(paths: Iterable[str]) -> None:
    """
    Waits for the databases to be created.

    :param paths: The paths to the databases.
    """

    callers = [
        Caller(target=lambda: await_database_creation(path))
        for path in paths
    ]

    multi_threaded_call(callers)
# end await_all_databases_creation

def insert_database_record(
        name: str,
        exchange: str,
        symbol: str,
        dataset: pd.DataFrame,
        databases: Dict[str, Engine],
        interval: Optional[str] = None
) -> None:
    """
    Inserts the data into the databases.

    :param name: The name for the data.
    :param exchange: The exchange name of the data.
    :param symbol: The symbol of the data.
    :param dataset: The dataframe of the symbol.
    :param databases: The database engines.
    :param interval: The interval.
    """

    table = parts_database_table_name(
        name=name, exchange=exchange, symbol=symbol, interval=interval
    )

    for path, engine in databases.items():
        location = os.path.split(database_file_path(path))[0]

        if location:
            os.makedirs(location, exist_ok=True)
        # end if

        dataset.to_sql(table, engine, if_exists='append', index=True)
    # end for
# end insert_database_record

def extract_database_length(
        name: str,
        exchange: str,
        symbol: str,
        databases: Dict[str, Engine],
        interval: Optional[str] = None
) -> Dict[str, int]:
    """
    Extracts the length of the data from the databases.

    :param name: The name for the data.
    :param exchange: The exchange name of the data.
    :param symbol: The symbol of the data.
    :param databases: The database engines.
    :param interval: The interval.

    :return: The returned database lengths.
    """

    table = parts_database_table_name(
        name=name, exchange=exchange,
        symbol=symbol, interval=interval
    )

    query = 'SELECT COUNT(' + DATE_TIME + ') FROM ' + table

    return {
        path: engine.connect().execute(text(query)).all()[0][0]
        for path, engine in databases.items()
    }
# end extract_database_length

def extract_database_record(
        name: str,
        exchange: str,
        symbol: str,
        databases: Dict[str, Engine],
        interval: Optional[str] = None,
        length: Optional[int] = None,
        start: Optional[dt.datetime] = None
) -> Dict[str, pd.DataFrame]:
    """
    Extracts the data from the databases.

    :param name: The name for the data.
    :param exchange: The exchange name of the data.
    :param symbol: The symbol of the data.
    :param databases: The database engines.
    :param length: Yne length of the dataset to extract.
    :param interval: The interval.
    :param start: The starting row.

    :return: The returned databases.
    """

    table = parts_database_table_name(
        name=name, exchange=exchange,
        symbol=symbol, interval=interval
    )

    query = 'SELECT * FROM ' + table

    if length is not None:
        if isinstance(start, int) and (start > 0):
            length_query = f" WHERE DateTime > {start}"

        else:
            length_query = f'COUNT(*) - {length}'
        # end if

        query += (
                f' LIMIT {length} OFFSET '
                f'(SELECT {length_query} FROM  ' + table + ')'
        )

    elif isinstance(start, int) and (start > 0):
        query += f' WHERE DateTime > {start}'
    # end if

    return {
        path: pd.read_sql(query, engine)
        for path, engine in databases.items()
    }
# end extract_database_record

def extract_data_into_screener_dataset(
        screener: BaseScreener,
        path: str,
        engine: Engine,
        length: Optional[int] = None,
        start: Optional[dt.datetime] = None
) -> None:
    """
    Extracts the data and inserts it into the screener dataset.

    :param screener: The screener object.
    :param path: The path to the database.
    :param engine: The database engine.
    :param length: The length of data to extract.
    :param start: The start index.
    """

    interval = (
        screener.interval
        if (screener.NAME == "OHLCV") else
        None
    )

    data = extract_database_record(
        name=screener.NAME, exchange=screener.exchange,
        symbol=screener.symbol, interval=interval, start=start,
        length=length, databases={path: engine}
    )[path]

    for index, row in data.iterrows():
        row = row.to_dict()

        screener.market.loc[row.pop(DATE_TIME)] = row
    # end for
# end extract_data_into_screener_dataset

def extract_database_tables(
        databases: Dict[str, Engine]
) -> Dict[str, List[Tuple[str, str, str, Optional[str]]]]:
    """
    Extracts the databases table name.

    :param databases: The database engines.

    :return: The returned databases table name.
    """

    await_all_databases_creation(databases.keys())

    tables: Dict[str, List[Tuple[str, str, str, Optional[str]]]] = {}

    for path, engine in databases.items():
        database_tables = inspect(engine).get_table_names()

        tables[path] = [
            database_table_name_to_parts(table)
            for table in database_tables
        ]
    # end for

    return tables
# end extract_database_tables

Databases = Union[Iterable[str], Dict[str, Engine]]

def validate_database_engines(data: Any) -> Dict[str, Engine]:
    """
    Validates the databases.

    :param data: The databases to validate.

    :return: The database engines.
    """

    data = data or []

    if not isinstance(data, dict):
        data = {path: create_engine(path) for path in data}
    # end if

    if not all(
            isinstance(path, str) and isinstance(engine, Engine)
            for path, engine in data.items()
    ):
        raise ValueError(f"databases must be: {Databases}, not: {data}")
    # end if

    return data
# end validate_database_engines