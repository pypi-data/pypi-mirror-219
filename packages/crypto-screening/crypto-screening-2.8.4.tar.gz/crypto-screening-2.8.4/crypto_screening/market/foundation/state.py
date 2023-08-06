# state.py

import datetime as dt
from typing import (
    Optional, Union, Iterable, ClassVar, TypeVar, Generic
)

from attrs import define

from represent import represent, Modifiers

from crypto_screening.market.foundation.protocols import (
    BaseScreenerProtocol, BaseMultiScreenerProtocol, DataCollectorProtocol
)

__all__ = [
    "WaitingState"
]


_BS = TypeVar("_BS")

@define(repr=False)
@represent
class WaitingState(Generic[_BS]):
    """A class to represent the waiting state of screener objects."""

    screeners: Iterable[
        Union[
            _BS,
            BaseScreenerProtocol,
            BaseMultiScreenerProtocol,
            DataCollectorProtocol
        ]
    ]
    start: dt.datetime
    end: dt.datetime
    stop: Optional[bool] = False
    delay: Optional[float] = 0
    count: Optional[int] = 0
    canceled: Optional[bool] = False
    cancel: Optional[Union[float, dt.timedelta, dt.datetime]] = None

    __modifiers__: ClassVar[Modifiers] = Modifiers(
        hidden=["screeners"], properties=["time"]
    )

    @property
    def time(self) -> dt.timedelta:
        """
        Returns the amount of waited time.

        :return: The waiting time.
        """

        return self.end - self.start
    # end time
# end WaitingState