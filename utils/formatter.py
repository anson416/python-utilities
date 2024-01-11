# -*- coding: utf-8 -*-
# File: utils/formatter.py

from numbers import Real
from typing import Any, Dict, Literal, Tuple, Union

from .types_ import Array, StrDict

__all__ = [
    "arr2str",
    "args2str",
    "argparse2str",
    "dict2str",
    "kwargs2str",
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
        arr (Array[Any]): Target array.
        sep (str, optional): Separator between elements in `arr`. Defaults to
            "\\n".
        end (str, optional): Ending string. Defaults to "".

    Returns:
        str: String formatted from an array.

    Examples:
        arr2str([1, 2, 3], sep="---", end="!") -> 1---2---3!
    """

    return f"{sep.join(map(str, arr))}{end}"


def args2str(args: Tuple[Any, ...]) -> str:
    """
    A special case of `arr2str()` that converts function positional arguments
    into formatted string.

    Args:
        args (Tuple[Any, ...]): Positional arguments.

    Returns:
        str: String formatted from positional arguments.
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
        args (Any): Arguments from `argparse.ArgumentParser().parse_args()`.
        sep (str, optional): Separator between arguments. Defaults to ", ".
        end (str, optional): Ending string. Defaults to "".

    Returns:
        str: String formatted from argparse arguments.

    Examples:
        argparse2str(Namespace(job='driver', age=47), sep=", ", end="??") ->
            job=driver, age=47??
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
        dic (Dict[Any, Any]): Target dictionary.
        kv_sep (str, optional): Separator between key and value. Defaults to
            " : ".
        item_sep (str, optional): Separator between items. Defaults to "\\n".
        end (str, optional): Ending string. Defaults to "".

    Returns:
        str: String formatted from a dictionary.

    Examples:
        dict2str({1: "a", 2: "b"}, kv_sep=" : ", item_sep="--", end="??") ->
            1 : a--2 : b??
    """

    return (
        f"{item_sep.join([f'{key}{kv_sep}{value}' for key, value in dic.items()])}{end}"
    )


def kwargs2str(kwargs: StrDict[Any]) -> str:
    """
    A special case of `dict2str()` that converts function keyword arguments
    into formatted string.

    Args:
        args (StrDict[Any]): Keyword arguments.

    Returns:
        str: String formatted from keyword arguments.
    """

    return dict2str(kwargs, kv_sep="=", item_sep=", ")


def print_dict(
    dic: Dict[Any, Any],
    indent: int = 4,
) -> None:
    """
    Print a dictionary nicely and return nothing.

    Args:
        dic (Dict[Any, Any]): Target dictionary.
        indent (int, optional): Indent level. Defaults to 4.
    """

    assert indent >= 0, f"{indent} < 0. indent must be a non-negative integer."
    import json

    print(json.dumps(dic, indent=indent))


def arr2dict(
    arr: Array[Any],
    start: int = 0,
    str_key: bool = False,
) -> Dict[Union[int, str], Any]:
    """
    Convert an array into dictionary.

    Args:
        arr (Array[Any]): Target array.
        start (int, optional): Number from which key starts. Defaults to 0.
        str_key (bool, optional): Convert keys to string. Defaults to False.

    Returns:
        Dict[Union[int, str], Any]: Dictionary from an array.

    Examples:
        arr2dict(["a", "b"], start=1, str_key=True) -> {"1": "a", "2": "b"}
    """

    return {(str(i) if str_key else i): item for i, item in enumerate(arr, start=start)}


def convert_num(
    num: Real,
    threshold: Real = 1000,
    div: Real = 1000,
) -> Tuple[Real, str]:
    """
    Format a number to a smaller one with unit.

    Args:
        num (Real): Target number.
        threshold (Real, optional): Keep dividing `num` until absolute of
            `num` is smaller than `threshold`. Defaults to 1000.
        div (Real, optional): Divide `num` by `div` in every iteration.
            Defaults to 1000.

    Returns:
        Tuple[Real, str]: Converted number and corresponding unit.

    Examples:
        convert_num(1_234_567) -> (1.234567, "M")
    """

    assert threshold > 0, f"{threshold} <= 0. `threshold` must be a positive number."
    assert div > 0, f"{div} <= 0. `div` must be a positive number."

    UNITS = ["", "K", "M", "B", "T", "Q", "Qu", "S", "Sp", "O", "N"]
    max_idx = len(UNITS) - 1
    i = 0
    while abs(num) >= threshold and i < max_idx:
        num /= div
        i += 1
    return num, UNITS[i]


def convert_size(
    size: int,
    threshold: Real = 1024,
    div: Real = 1024,
) -> Tuple[Real, str]:
    """
    Convert data size to smaller one with unit.

    Args:
        size (int): Data size (in bytes).
        threshold (Real, optional): Keep dividing `size` until `size` is
            smaller than `threshold`. Defaults to 1024.
        div (Real, optional): Divide `size` by `div` in every iteration.
            Defaults to 1024.

    Returns:
        Tuple[Real, str]: Converted size and corresponding unit.

    Example:
        convert_size(1_298_562) -> (1.2384052276611328, "MB")
    """

    assert size >= 0, f"{size} < 0. `size` must be a non-negative integer."
    assert threshold > 0, f"{threshold} <= 0. `threshold` must be a positive number."
    assert div > 0, f"{div} <= 0. `div` must be a positive number."

    UNITS = ["", "K", "M", "G", "T", "P", "E", "Z", "Y", "R", "Q"]
    max_idx = len(UNITS) - 1
    i = 0
    while size >= threshold and i < max_idx:
        size /= div
        i += 1
    return size, f"{UNITS[i]}B"


def trunc_str(
    text: str,
    n: int,
    mode: Literal[1, 2, 3, 4] = 1,
    replacement: str = "...",
) -> str:
    """
    Truncate a string (if necessary) to certain length.

    Args:
        text (str): Target string.
        n (int): Maximum length of substring from `text` in output string.
        mode (int, optional): Mode of truncation. Must be any one in
            {1, 2, 3, 4}. Defaults to 1.
            1: Keeping the left part.
            2: Keeping the left and right parts.
            3: Keeping the middle part.
            4: Keeping the right part.
        replacement (str, optional): String to replace the removed substring.
            Defaults to "...".

    Returns:
        str: Truncated `text`.
    """

    assert mode in (
        mode_set := {1, 2, 3, 4}
    ), f"{mode} does not belong to {mode_set}. `mode` must be any one in {mode_set}."

    from .num_ops import is_odd

    # Return `text` itself if no truncation is needed
    if len(text := str(text)) <= n:
        return text

    # Switch statements can be used in Python 3.10
    if mode == 1:
        truncated = "".join((text[:n], replacement))
    elif mode == 2:
        truncated = "".join(
            (text[: (left := n // 2)], replacement, text[-(left + is_odd(n)) :])
        )
    elif mode == 3:
        truncated = "".join(
            (replacement, text[(mid := (len(text) - n) // 2) : mid + n], replacement)
        )
    else:
        truncated = "".join((replacement, text[-n:]))
    return truncated
