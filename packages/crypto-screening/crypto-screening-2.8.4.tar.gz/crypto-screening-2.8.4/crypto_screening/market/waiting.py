# dynamic.py

import datetime as dt
from typing import (
    Optional, Union, Iterable
)

from crypto_screening.collect.screeners import gather_screeners
from crypto_screening.market.screeners import BaseScreener, BaseMultiScreener
from crypto_screening.market.foundation.state import WaitingState
from crypto_screening.market.foundation.waiting import (
    base_wait_for_update, base_wait_for_dynamic_initialization,
    base_wait_for_initialization, base_wait_for_dynamic_update
)

__all__ = [
    "wait_for_dynamic_initialization",
    "wait_for_update",
    "wait_for_initialization",
    "wait_for_dynamic_update",
    "WaitingState"
]

def wait_for_dynamic_initialization(
        screeners: Iterable[Union[BaseScreener, BaseMultiScreener]],
        stop: Optional[bool] = None,
        delay: Optional[Union[float, dt.timedelta]] = None,
        cancel: Optional[Union[float, dt.timedelta, dt.datetime]] = None
) -> WaitingState:
    """
    Waits for all the create_screeners to update.

    :param screeners: The create_screeners to wait for them to update.
    :param delay: The delay for the waiting.
    :param stop: The value to stop the screener objects.
    :param cancel: The time to cancel the waiting.

    :returns: The total delay.
    """

    return base_wait_for_dynamic_initialization(
        screeners=screeners, stop=stop, delay=delay,
        cancel=cancel, gatherer=gather_screeners
    )
# end wait_for_dynamic_initialization

def wait_for_initialization(
        *screeners: Union[BaseScreener, BaseMultiScreener],
        stop: Optional[bool] = False,
        delay: Optional[Union[float, dt.timedelta]] = None,
        cancel: Optional[Union[float, dt.timedelta, dt.datetime]] = None
) -> WaitingState:
    """
    Waits for all the create_screeners to update.

    :param screeners: The create_screeners to wait for them to update.
    :param delay: The delay for the waiting.
    :param stop: The value to stop the screener objects.
    :param cancel: The time to cancel the waiting.

    :returns: The total delay.
    """

    return base_wait_for_initialization(
        *screeners, stop=stop, delay=delay,
        cancel=cancel, gatherer=gather_screeners
    )
# end wait_for_initialization

def wait_for_dynamic_update(
        screeners: Iterable[Union[BaseScreener, BaseMultiScreener]],
        stop: Optional[bool] = False,
        delay: Optional[Union[float, dt.timedelta]] = None,
        cancel: Optional[Union[float, dt.timedelta, dt.datetime]] = None
) -> WaitingState:
    """
    Waits for all the create_screeners to update.

    :param screeners: The create_screeners to wait for them to update.
    :param delay: The delay for the waiting.
    :param stop: The value to stop the screener objects.
    :param cancel: The time to cancel the waiting.

    :returns: The total delay.
    """

    return base_wait_for_dynamic_update(
        screeners=screeners, stop=stop, delay=delay,
        cancel=cancel, gatherer=gather_screeners
    )
# end wait_for_dynamic_update

def wait_for_update(
        *screeners: Union[BaseScreener, BaseMultiScreener],
        stop: Optional[bool] = False,
        delay: Optional[Union[float, dt.timedelta]] = None,
        cancel: Optional[Union[float, dt.timedelta, dt.datetime]] = None
) -> WaitingState:
    """
    Waits for all the create_screeners to update.

    :param screeners: The create_screeners to wait for them to update.
    :param delay: The delay for the waiting.
    :param stop: The value to stop the screener objects.
    :param cancel: The time to cancel the waiting.

    :returns: The total delay.
    """

    return base_wait_for_update(
        *screeners, stop=stop, delay=delay,
        cancel=cancel, gatherer=gather_screeners
    )
# end wait_for_update
