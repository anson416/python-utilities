# -*- coding: utf-8 -*-
# File: error.py

from typing import Optional

from . import beartype

__all__ = [
    "get_err_type",
    "err2str",
    "raise_err",
]


@beartype
def get_err_type(
    err: Exception,
) -> str:
    """
    Get the type of error from an error.

    Args:
        err (Exception): Error from try-except

    Returns:
        str: Type of error
    """

    return type(err).__name__


@beartype
def err2str(
    err: Exception,
    sep: str = ": ",
) -> str:
    """
    Convert an error into formatted string.

    Args:
        err (Exception): Error from try-except
        sep (str, optional): Separator between error type and error message. Defaults to ": ".

    Returns:
        str: String formatted from an error
    """

    return f"{get_err_type(err)}{sep}{err}"


@beartype
def raise_err(
    err: Exception,
    msg: Optional[str] = None,
) -> None:
    """
    Raise error.

    Args:
        err (Exception): Error from try-except
        msg (Optional[str], optional): Error message. Defaults to None.

    Usage:
        try:
            ...
        except Exception as e:
            raise_err(e)
    """

    import builtins

    raise getattr(builtins, get_err_type(err), Exception)(msg if msg else err)
