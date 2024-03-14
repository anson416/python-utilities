# -*- coding: utf-8 -*-
# File: utils/date_time.py

__all__ = [
    "get_date",
    "get_time",
    "get_datetime",
    "get_etr",
]


def get_date(date_format: str = r"%Y-%m-%d") -> str:
    """
    Get today's date.

    Args:
        date_format (str, optional): Format string for date. Defaults to
            r"%Y-%m-%d".

    Returns:
        str: Today's date.
    """

    assert date_format != "", f'"{date_format}" is empty. `date_format` must not be empty.'

    from datetime import datetime

    return datetime.now().strftime(date_format)


def get_time(time_format: str = r"%H:%M:%S") -> str:
    """
    Get current time.

    Args:
        time_format (str, optional): Format string for time. Defaults to
            r"%H:%M:%S".

    Returns:
        str: Current time.
    """

    assert time_format != "", f'"{time_format}" is empty. `time_format` must not be empty.'

    from datetime import datetime

    return datetime.now().strftime(time_format)


def get_datetime(
    date_format: str = r"%Y%m%d",
    time_format: str = r"%H%M%S",
    sep: str = "-",
    date_first: bool = True,
) -> str:
    """
    Get current date and time.

    Args:
        date_format (str, optional): Format string for date. Defaults to
            r"%Y%m%d".
        time_format (str, optional): Format string for time. Defaults to
            r"%H%M%S".
        sep (str, optional): Separator between date and time. Defaults to "-".
        date_first (bool, optional): Put date before time. Defaults to True.

    Returns:
        str: Today's date and current time.
    """

    return sep.join((get_date(date_format), get_time(time_format))[:: (-1) ** (not date_first)])


def get_etr(
    progress: int,
    total: int,
    time_elapsed: float,
) -> float:
    """
    Get the estimated time remaining (ETR) of an iterative process.

    Args:
        progress (int): Current iteration.
        total (int): Number of iterations.
        time_elapsed (float): Time elapsed from the start of the process.
            `start_time` can be obtained by `time()` from `from time import
            time`. Time elapsed naturally equals `time() - start_time`.

    Returns:
        float: ETR of the process.
    """

    assert total > 0, f"{total} > 0. `total` must be a positive integer."
    assert (
        0 < progress <= total
    ), f"0 < {progress} <= {total}. `progress` must be a positive integer not greater than `total`."

    return time_elapsed * ((total / progress) - 1)
