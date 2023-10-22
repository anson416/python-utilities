# -*- coding: utf-8 -*-
# File: formatter.py

from typing import Any, Dict, Tuple, Union

from .types import Array, Number, StrDict

__all__ = [
    "arr2str",
    "args2str",
    "dict2str",
    "print_dict",
    "arr2dict",
    "convert_num",
    "convert_size",
    "trunc_str",
]


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


def args2str(args: Tuple[Any, ...]) -> str:
    """
    A special case of `arr2str()` that converts function positional arguments into formatted string.

    Args:
        args (Tuple[Any, ...]): Function positional arguments (maybe from *args)

    Returns:
        str: String formatted from function positional arguments
    """

    return arr2str(args, sep=", ")


def argparse2str(
    args: Any,
    sep: str = ", ",
    end: str = "",
) -> str:
    """
    Convert argparse arguments into formatted string.

    Args:
        args (Any): Arguments from argparse.ArgumentParser().parse_args()
        sep (str, optional): Separator between arguments. Defaults to ", ".
        end (str, optional): Ending string. Defaults to "".

    Returns:
        str: String formatted from argparse arguments

    Examples:
        argparse2str(Namespace(job='driver', age=47), sep=", ", end="??") -> job=driver, age=47??
    """
    
    return f"{sep.join([f'{key}={value}' for key, value in vars(args).items()])}{end}"


def dict2str(
    dic: Dict[Any, Any],
    kv_sep: str = " : ",
    item_sep: str = "\n",
    end: str = "",
) -> str:
    """
    Convert a dictionary into formatted string.

    Args:
        dic (Dict[Any, Any]): Target dictionary
        kv_sep (str, optional): Separator between key and value. Defaults to " : ".
        item_sep (str, optional): Separator between items. Defaults to "\\n".
        end (str, optional): Ending string. Defaults to "".

    Returns:
        str: String formatted from a dictionary

    Examples:
        dict2str({1: "a", 2: "b"}, kv_sep=" : ", item_sep="--", end="??") -> 1 : a--2 : b??
    """

    return f"{item_sep.join([f'{key}{kv_sep}{value}' for key, value in dic.items()])}{end}"


def kwargs2str(kwargs: StrDict[Any]) -> str:
    """
    A special case of `dict2str()` that converts function keyword arguments into formatted string.

    Args:
        args (StrDict[Any]): Function keyword arguments (maybe from **kwargs)

    Returns:
        str: String formatted from function keyword arguments
    """

    return dict2str(kwargs, kv_sep="=", item_sep=", ")


def print_dict(
    dic: Dict[Any, Any],
    indent: int = 4,
) -> None:
    """
    Print a dictionary nicely and return nothing.

    Args:
        dic (Dict[Any, Any]): Target dictionary
        indent (int, optional): Indent level. Defaults to 4.
    """

    assert indent >= 0, "indent must be non-negative integer"

    import json

    print(json.dumps(dic, indent=indent))


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
        key_to_str (bool, optional): Convert keys to string. Defaults to False.

    Returns:
        Dict[Union[int, str], Any]: Dictionary from an array

    Examples:
        arr2dict(["a", "b"], start=1, key_to_str=True) -> {"1": "a", "2": "b"}
    """

    return {(str(i) if key_to_str else i): item for i, item in enumerate(arr, start=start)}


def convert_num(
    num: Number,
    threshold: Number = 1000,
    div: Number = 1000,
) -> Tuple[Number, str]:
    """
    Format a number to smaller one with unit.

    Args:
        num (Number): Target number
        threshold (Number, optional): Keep dividing `num` until absolute of `num` is smaller than `threshold`. \
            Defaults to 1000.
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


def convert_size(
    size: int,
    threshold: Number = 1024,
    div: Number = 1024,
) -> Tuple[Number, str]:
    """
    Convert data size to smaller one with unit.

    Args:
        size (int): Data size (in bytes)
        threshold (Number, optional): Keep dividing `size` until `size` is smaller than `threshold`. Defaults to 1024.
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


def trunc_str(
    text: str,
    n: int,
    mode: int = 1,
    replacement: str = "...",
) -> str:
    """
    Truncate a string (if necessary) to certain length.

    Args:
        text (str): Target string
        n (int): Maximum length of substring from `text` in output string
        mode (int, optional): Mode of truncation. 1: Keeping the left part. 2: Keeping the left and right parts. 3: \
            Keeping the middle part. 4: Keeping the right part. Must be any one in {1, 2, 3, 4}. Defaults to 0.
        replacement (str, optional): String to replace the removed substring. Defaults to "...".

    Returns:
        str: Truncated `text`
    """

    assert mode in (1, 2, 3, 4), "mode must be any one in {1, 2, 3, 4}"

    from .num_ops import is_odd

    if len(text) <= n:
        return text
    
    if mode == 1:
        truncated = text[:n] + replacement
    elif mode == 2:
        left = n // 2
        right = left + is_odd(n)
        truncated = text[:left] + replacement + text[-right:]
    elif mode == 3:
        mid = (len(text) - n) // 2
        truncated = replacement + text[mid:mid+n] + replacement
    else:
        truncated = replacement + text[-n:]
    
    return truncated
