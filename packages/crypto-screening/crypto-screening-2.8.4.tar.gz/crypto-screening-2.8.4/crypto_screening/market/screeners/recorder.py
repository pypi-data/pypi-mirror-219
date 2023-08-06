# recorder.py

from typing import Optional, Dict, Any, List, Iterable

import pandas as pd

from represent import Modifiers, represent

from crypto_screening.validate import validate_exchange, validate_symbol
from crypto_screening.process import find_string_value
from crypto_screening.dataset import DATE_TIME

__all__ = [
    "create_market_dataframe",
    "validate_market",
    "MarketRecorder"
]

Market = Dict[str, Dict[str, pd.DataFrame]]

def create_market_dataframe(columns: Optional[Iterable[str]] = None) -> pd.DataFrame:
    """
    Creates a dataframe for the order book data.

    :param columns: The dataset columns.

    :return: The dataframe.
    """

    market = pd.DataFrame(
        {column: [] for column in columns or []}, index=[]
    )
    market.index.name = DATE_TIME

    return market
# end create_market_dataframe

def validate_market(data: Any) -> Market:
    """
    Validates the data.

    :param data: The data to validate.

    :return: The valid data.
    """

    if data is None:
        return {}
    # end if

    try:
        if not isinstance(data, dict):
            raise ValueError
        # end if

        for exchange, values in data.items():
            if not (
                isinstance(exchange, str) and
                (
                    (
                        isinstance(values, dict) and
                        all(
                            isinstance(symbol, str) and
                            isinstance(dataset, pd.DataFrame)
                            for symbol, dataset in values.items()
                        )
                    ) or (all(isinstance(value, str) for value in values))
                )
            ):
                raise ValueError
            # end if

            if not isinstance(values, dict):
                data[exchange] = {
                    symbol: create_market_dataframe()
                    for symbol in values
                }
            # end if
        # end for

    except (TypeError, ValueError):
        raise ValueError(
            f"Data must be of type {Market}, not: {data}."
        )
    # end try

    return data
# end validate_market

@represent
class MarketRecorder:
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

    >>> from crypto_screening.market.screeners.recorder import MarketRecorder
    >>>
    >>> market = {'binance': ['BTC/USDT'], 'bittrex': ['ETH/USDT']}
    >>>
    >>> recorder = MarketRecorder(data=market)

    """

    __modifiers__ = Modifiers()
    __modifiers__.hidden.append("market")

    __slots__ = "market",

    def __init__(self, market: Optional[Market] = None) -> None:
        """
        Defines the class attributes.

        :param market: The object to fill with the crypto feed record.
        """

        self.market = self.validate_market(data=market)
    # end __init__

    @staticmethod
    def validate_market(data: Any) -> Market:
        """
        Validates the data.

        :param data: The data to validate.

        :return: The valid data.
        """

        return validate_market(data=data)
    # end validate_market

    def structure(self) -> Dict[str, List[str]]:
        """
        Returns the structure of the market data.

        :return: The structure of the market.
        """

        return {
            exchange: list(symbols.keys())
            for exchange, symbols in self.market.items()
        }
    # end structure

    def data(self, exchange: str, symbol: str) -> pd.DataFrame:
        """
        Returns the market data of the symbol from the exchange.

        :param exchange: The source name of the exchange.
        :param symbol: The symbol of the pair.

        :return: The dataset of the spread data.
        """

        exchange = find_string_value(
            value=exchange, values=self.market.keys()
        )

        validate_exchange(
            exchange=exchange,
            exchanges=self.market.keys(),
            provider=self
        )

        validate_symbol(
            symbol=symbol,
            exchange=exchange,
            exchanges=self.market.keys(),
            symbols=self.market[exchange],
            provider=self
        )

        return self.market[exchange][symbol]
    # end data

    def in_market(self, exchange: str, symbol: str) -> bool:
        """
        Returns the market data of the symbol from the exchange.

        :param exchange: The source name of the exchange.
        :param symbol: The symbol of the pair.

        :return: The dataset of the spread data.
        """

        try:
            self.data(exchange=exchange, symbol=symbol)

            return True

        except ValueError:
            return False
        # end try
    # end in_market
# end MarketRecorder