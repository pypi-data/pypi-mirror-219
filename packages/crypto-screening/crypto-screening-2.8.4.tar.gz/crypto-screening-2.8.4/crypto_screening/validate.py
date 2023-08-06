# validate.py

from typing import Optional, Iterable, Any

from crypto_screening.process import find_string_value
from crypto_screening.symbols import adjust_symbol
from crypto_screening.exchanges import EXCHANGE_NAMES, EXCHANGES

__all__ = [
    "is_valid_symbol",
    "validate_exchange",
    "validate_symbol",
    "is_valid_exchange"
]

def is_valid_symbol(
        exchange: str,
        symbol: str,
        exchanges: Optional[Iterable[str]] = None,
        symbols: Optional[Iterable[str]] = None
) -> bool:
    """
    Returns a value for the symbol being valid for the source exchange.

    :param exchange: The name of the exchange platform.
    :param symbol: The symbol of the assets.
    :param symbols: The valid symbols.
    :param exchanges: The valid exchanges.

    :return: The validation-value.
    """

    if symbols is None:
        exchange = find_string_value(
            value=exchange, values=EXCHANGE_NAMES
        )

        if not is_valid_exchange(
                exchange=exchange, exchanges=exchanges
        ):
            return False
        # end if

        symbols = EXCHANGES[exchange].symbols()
    # end for

    symbols = [adjust_symbol(symbol=s) for s in symbols]

    symbol = find_string_value(
        value=adjust_symbol(symbol=symbol), values=symbols
    )

    return symbol in symbols
# end is_valid_symbol

def validate_symbol(
        exchange: str,
        symbol: str,
        exchanges: Optional[Iterable[str]] = None,
        symbols: Optional[Iterable[str]] = None,
        provider: Optional[Any] = None
) -> str:
    """
    Returns a value for the symbol being valid for the source exchange.

    :param exchange: The name of the exchange platform.
    :param symbol: The symbol of the assets.
    :param symbols: The valid symbols.
    :param exchanges: The valid exchanges.
    :param provider: Any provider object.

    :return: The validation-value.
    """

    validate_exchange(
        exchange=exchange, exchanges=exchanges,
        provider=provider
    )

    if not is_valid_symbol(
            exchange=exchange, symbol=symbol, symbols=symbols
    ):
        raise ValueError(
            f"'{symbol}' is not a valid "
            f"symbol for the '{exchange}' exchange. "
            f"Valid symbols: {', '.join(symbols or [])}"
            f"{f' for {provider}.' if provider else ''}"
        )
    # end if

    return symbol
# end validate_symbol

def is_valid_exchange(
        exchange: str, exchanges: Optional[Iterable[str]] = None
) -> bool:
    """
    checks of the source os a valid exchange name.

    :param exchange: The source name to validate.
    :param exchanges: The valid exchanges.

    :return: The validation value.
    """

    if exchanges is None:
        exchanges = EXCHANGE_NAMES
    # end if

    exchange = find_string_value(value=exchange, values=exchanges)

    return exchange in exchanges
# end is_valid_exchange

def validate_exchange(
        exchange: str,
        exchanges: Optional[Iterable[str]] = None,
        provider: Optional[Any] = None
) -> str:
    """
    Validates the source value.

    :param exchange: The name of the exchange platform.
    :param exchanges: The valid exchanges.
    :param provider: Any provider object.

    :return: The validates symbol.
    """

    if exchanges is None:
        exchanges = EXCHANGE_NAMES
    # end if

    if not is_valid_exchange(exchange=exchange, exchanges=exchanges):
        raise ValueError(
            f"'{exchange}' is not a valid exchange name. "
            f"Valid exchanges: {', '.join(exchanges or [])}"
            f"{f' for {provider}.' if provider else ''}"
        )
    # end if

    return exchange
# end validate_exchange