# -*- coding: utf-8 -*-
# File: formatter.py

from typing import Any, Dict, Union

from . import beartype
from .types import Array

__all__ = [
    "arr2str",
    "args2str",
    "dict2str",
    "arr2dict",
    "num2str",
    "datasize2str",
]


@beartype
def arr2str(
    arr: Array[Any],
    sep: str = "\n",
    end: str = "",
) -> str:
    """
    Convert an array into formatted string.

    Args:
        arr (Array[Any]): Target array
        sep (str, optional): Separator between elements in `arr`. Defaults to "\\n".
        end (str, optional): Ending string. Defaults to "".

    Returns:
        str: String formatted from an array

    Examples:
        arr2str([1, 2, 3], sep="---", end="!") -> 1---2---3!
    """

    return f"{sep.join(map(str, arr))}{end}"


@beartype
def args2str(
    args,
    sep: str = ", ",
    end: str = "",
) -> str:
    """
    Convert arguments into formatted string.

    Args:
        args (argparse.Namespace): Arguments from argparse.ArgumentParser().parse_args()
        sep (str, optional): Separator between arguments. Defaults to ", ".
        end (str, optional): Ending string. Defaults to "".

    Returns:
        str: String formatted from arguments

    Examples:
        args2str(Namespace(job='driver', age=47), sep=", ", end="??") -> job=driver, age=47??
    """

    @beartype
    def _args2str(
        args: argparse.Namespace,
        sep: str,
        end: str,
    ) -> str:
        return f"{sep.join([f'{key}={value}' for key, value in vars(args).items()])}{end}"

    import argparse
    
    return _args2str(args, sep, end)


@beartype
def dict2str(
    dic: Dict[Any, Any],
    kv_sep: str = " : ",
    item_sep: str = "\n",
    str_end: str = "",
) -> str:
    """
    Convert a dictionary into formatted string.

    Args:
        dic (Dict[Any, Any]): Target dictionary
        kv_sep (str, optional): Separator between key and value. Defaults to " : ".
        item_sep (str, optional): Separator between items. Defaults to "\\n".
        str_end (str, optional): Ending string. Defaults to "".

    Returns:
        str: String formatted from a dictionary

    Examples:
        dict2str({1: "a", 2: "b"}, kv_sep=" : ", item_sep="--", str_end="??") -> 1 : a--2 : b??
    """

    return f"{item_sep.join([f'{key}{kv_sep}{value}' for key, value in dic.items()])}{str_end}"


@beartype
def arr2dict(
    arr: Array[Any],
    start: int = 0,
    key_to_str: bool = False,
) -> Dict[Union[int, str], Any]:
    """
    Convert an array into dictionary.

    Args:
        arr (Array[Any]): Target array
        start (int, optional): Number from which key starts. Defaults to 0.
        key_to_str (bool, optional): If True, keys are converted into string. Defaults to False.

    Returns:
        Dict[Union[int, str], Any]: Dictionary from an array

    Examples:
        arr2dict(["a", "b"], start=1, key_to_str=True) -> {"1": "a", "2": "b"}
    """

    return {(str(i) if key_to_str else i): item for i, item in enumerate(arr, start=start)}


@beartype
def num2str(
    num: Union[float, int],
    prec: int = 2,
    dp: str = ".",
    sep: str = "",
) -> str:
    """
    Format a large number to string with unit.

    Args:
        num (Union[float, int]): Target number
        prec (int, optional): Number of digits after decimal point (i.e., precision). Defaults to 2.
        dp (str, optional): Separator between integer part and decimal part. Defaults to ".".
        sep (str, optional): Separator between number and unit. Defaults to "".

    Returns:
        str: Number with unit

    Examples:
        num2str(1234567, prec=1, dp="_", sep=" ") -> 1_2 M
    """

    UNITS = ["", "K", "M", "B", "T", "Q", "Qu", "S", "Sp", "O", "N"]

    assert prec >= 0, "prec must be non-negative integer"

    max_idx = len(UNITS) - 1
    i = 0
    while abs(num) >= 1000 and i < max_idx:
        num /= 1000
        i += 1

    return f"{num:.{prec}f}".replace(".", dp) + f"{sep}{UNITS[i]}"


@beartype
def datasize2str(
    size: int,
    div: Union[float, int] = 1024,
    prec: int = 0,
    dp: str = ".",
    sep: str = " ",
) -> str:
    """
    Format data size to string with unit.

    Args:
        size (int): Data size (in bytes)
        div (Union[float, int], optional): 1 KB equals `div` B. Defaults to 1024.
        prec (int, optional): Number of digits after decimal point (i.e., precision). Defaults to 0.
        dp (str, optional): Separator between integer part and decimal part. Defaults to ".".
        sep (str, optional): Separator between number and unit. Defaults to " ".

    Returns:
        str: Data size with unit

    Example:
        datasize2str(1298562, div=1000, prec=1, dp="_", sep="") -> 1_3MB
    """

    UNITS = ["", "K", "M", "G", "T", "P", "E", "Z", "Y", "R", "Q"]

    assert size >= 0, "size must be non-negative integer"
    assert div > 0, "div must be positive number"
    assert prec >= 0, "prec must be non-negative integer"

    max_idx = len(UNITS) - 1
    i = 0
    while size >= div and i < max_idx:
        size /= div
        i += 1

    return f"{size:.{prec}f}".replace(".", dp) + f"{sep}{UNITS[i]}B"
