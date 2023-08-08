# -*- coding: utf-8 -*-
# File: formatter.py

from . import beartype
from .types import Any, Array, Dict, Number, Tuple, Union

__all__ = [
    "arr2str",
    "args2str",
    "dict2str",
    "arr2dict",
    "convert_num",
    "convert_size",
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
def convert_num(
    num: Number,
    threshold: Number = 1000,
    div: Number = 1000,
) -> Tuple[Number, str]:
    """
    Format a number to smaller one with unit.

    Args:
        num (Number): Target number
        threshold (Number, optional): Keep dividing `num` until absolute of `num` < `threshold`. Defaults to 1000.
        div (Number, optional): Divide `num` by `div` in every iteration. Defaults to 1000.

    Returns:
        Tuple[Number, str]: Converted number and corresponding unit

    Examples:
        convert_num(1_234_567) -> (1.234567, "M")
    """

    assert threshold > 0, "threshold must be positive number"
    assert div > 0, "div must be positive number"

    UNITS = ["", "K", "M", "B", "T", "Q", "Qu", "S", "Sp", "O", "N"]

    max_idx = len(UNITS) - 1
    i = 0
    while abs(num) >= threshold and i < max_idx:
        num /= div
        i += 1

    return num, UNITS[i]


@beartype
def convert_size(
    size: int,
    threshold: Number = 1024,
    div: Number = 1024,
) -> Tuple[Number, str]:
    """
    Convert data size to smaller one with unit.

    Args:
        size (int): Data size (in bytes)
        threshold (Number, optional): Keep dividing `size` until `size` < `threshold`. Defaults to 1024.
        div (Number, optional): Divide `size` by `div` in every iteration. Defaults to 1024.

    Returns:
        Tuple[Number, str]: Converted size and corresponding unit

    Example:
        convert_size(1_298_562) -> (1.2384052276611328, "MB")
    """

    UNITS = ["", "K", "M", "G", "T", "P", "E", "Z", "Y", "R", "Q"]

    assert size >= 0, "size must be non-negative integer"
    assert threshold > 0, "threshold must be positive number"
    assert div > 0, "div must be positive number"

    max_idx = len(UNITS) - 1
    i = 0
    while size >= threshold and i < max_idx:
        size /= div
        i += 1

    return size, f"{UNITS[i]}B"
