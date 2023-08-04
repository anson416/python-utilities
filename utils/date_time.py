# -*- coding: utf-8 -*-
# File: date_time.py

from datetime import datetime

from . import beartype

__all__ = [
    "get_date",
    "get_time",
    "get_datetime",
]


@beartype
def get_date(date_format: str = r"%Y-%m-%d") -> str:
    """
    Get today's date.

    Args:
        date_format (str, optional): Format string for date. Defaults to r"%Y-%m-%d".

    Returns:
        str: Today's date
    """

    assert date_format, "date_format cannot be empty"

    return datetime.now().strftime(date_format)


@beartype
def get_time(time_format: str = r"%H:%M:%S") -> str:
    """
    Get current time.

    Args:
        time_format (str, optional): Format string for time. Defaults to r"%H:%M:%S".

    Returns:
        str: Current time
    """

    assert time_format, "time_format cannot be empty"

    return datetime.now().strftime(time_format)


@beartype
def get_datetime(
    date_format: str = r"%Y-%m-%d",
    time_format: str = r"%H:%M:%S",
    sep: str = " ",
    date_first: bool = True,
) -> str:
    """
    Get current date and time.

    Args:
        date_format (str, optional): Format string for date. Defaults to r"%Y-%m-%d".
        time_format (str, optional): Format string for time. Defaults to r"%H:%M:%S".
        sep (str, optional): Separator between date and time. Defaults to " ".
        date_first (bool, optional): If True, put date before time. Otherwise, put time before date.

    Returns:
        str: Current date and time
    """
    
    return sep.join((get_date(date_format), get_time(time_format))[::(-1) ** (not date_first)])
