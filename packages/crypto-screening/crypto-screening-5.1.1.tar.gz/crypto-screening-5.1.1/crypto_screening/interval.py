# interval.py

from typing import Tuple, Union, Iterable
import datetime as dt

from attrs import define

from represent import represent, Modifiers


__all__ = [
    "interval_to_duration",
    "interval_to_time",
    "interval_to_total_time",
    "parts_to_interval",
    "INTERVALS",
    "MINUTES",
    "MONTHS",
    "HOURS",
    "DAYS",
    "YEARS",
    "WEEKS",
    "Interval"
]

MINUTES = "m"
MONTHS = "mo"
HOURS = "h"
DAYS = "d"
YEARS = "y"
WEEKS = "w"

INTERVALS = {
    MINUTES: dt.timedelta(minutes=1),
    HOURS: dt.timedelta(hours=1),
    DAYS: dt.timedelta(days=1),
    WEEKS: dt.timedelta(days=7),
    MONTHS: dt.timedelta(days=30),
    YEARS: dt.timedelta(days=365)
}

@define(slots=False, init=False, repr=False)
@represent
class Interval:
    """
    A class to represent a trading pair.

    This object represents a pair of assets that can be traded.

    attributes:

    - base:
        The asset to buy or sell.

    - quote:
        The asset to use to buy or sell.

    >>> from crypto_screening.interval import Interval
    >>>
    >>> interval = Interval(1, "d")
    """

    __slots__ = "periods", "duration", "parts"

    __modifiers__ = Modifiers(excluded=["parts"])

    def __init__(self, periods: int, duration: str) -> None:
        """
        Defines the class attributes.

        :param periods: The amount of periods for the interval.
        :param duration: The duration type for the interval.
        """

        self.periods = periods
        self.duration = duration

        self.parts = (self.periods, self.duration)
    # end __init__

    def __getitem__(self, item: Union[slice, int]) -> Union[int, str, Tuple[int, str]]:
        """
        Returns the items.

        :param item: The slice item.

        :return: The items in the object to get with the slice.
        """

        data = self.parts[item]

        if isinstance(data, list):
            # noinspection PyTypeChecker
            return type(self)(*data)
        # end if

        return data
    # end __getitem__

    def __len__(self) -> int:
        """
        The length of the assets.

        :return: The length of the assets.
        """

        return len(self.parts)
    # end __len__

    def __iter__(self) -> Tuple[int, str]:
        """
        Returns the object as an iterable.

        :return: The iterable object.
        """

        yield from self.parts
    # end __iter__

    @staticmethod
    def load(parts: Iterable[Union[str, int]]):
        """
        Creates a pair of assets from the data.

        :param parts: The pair data.

        :return: The pair object.
        """

        if not (
            (len(tuple(parts)) == 2) and
            all(isinstance(part, str) for part in parts)
        ):
            raise ValueError(
                f"Pair data must be an iterable of base asset and "
                f"quote asset of type str, in that order, not {parts}."
            )
        # end if

        return Interval(*parts)
    # end load

    def interval(self) -> str:
        """
        Returns the string for the interval.

        :return: The string.
        """

        return f"{self.periods}{self.duration}"
    # end __str__

    def json(self) -> Tuple[int, str]:
        """
        Converts the data into a json format.

        :return: The chain of assets.
        """

        return tuple(self.parts)
    # end json
# end Interval

def interval_to_duration(interval: str) -> int:
    """
    Extracts the number from the interval.

    :param interval: The interval to extract.

    :return: The number from the interval.
    """

    for kind in tuple(INTERVALS.keys()):
        try:
            return int(interval.replace(kind, ""))

        except (TypeError, EOFError):
            pass
        # end try
    # end for

    raise ValueError(f"Invalid interval value: {interval}.")
# end interval_to_duration

def interval_to_time(interval: str) -> dt.timedelta:
    """
    Extracts the type from the interval.

    :param interval: The interval to extract.

    :return: The type from the interval.
    """

    number = interval_to_duration(interval)

    try:
        return INTERVALS[interval.replace(str(number), "")]

    except KeyError:
        raise ValueError(f"Invalid interval structure: {interval}.")
    # end try
# end interval_to_time

def interval_to_total_time(interval: str) -> dt.timedelta:
    """
    Extracts the type from the interval.

    :param interval: The interval to extract.

    :return: The type from the interval.
    """

    return interval_to_duration(interval) * interval_to_time(interval)
# end interval_to_total_time

def parts_to_interval(increment: str, duration: int) -> str:
    """
    Creates a valid interval from the parameters.

    :param increment: The increment type for the interval.
    :param duration: The duration of the interval.

    :return: The interval.
    """

    if increment not in INTERVALS:
        raise ValueError(
            f"Interval increment must be one of "
            f"{', '.join(INTERVALS.keys())}, not {increment}."
        )
    # end if

    return f"{duration}{increment}"
# end parts_to_interval