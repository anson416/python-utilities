# -*- coding: utf-8 -*-
# File: num_ops.py

__all__ = [
    "is_even",
    "is_odd",
    "rescale_num",
    "clamp",
    "get_num_len",
]


def is_even(num: int) -> bool:
    """
    Return True if a number is even.

    Args:
        num (int): Target number

    Returns:
        bool: True if `num` is even
    """

    return num % 2 == 0


def is_odd(num: int) -> bool:
    """
    Return True if a number is old.

    Args:
        num (int): Target number

    Returns:
        bool: True if `num` is old
    """

    return num % 2 != 0


def rescale_num(
    num: float,
    a: float,
    b: float,
    c: float,
    d: float,
) -> float:
    """
    Map a number in [a, b] (a != b) to [c, d].

    Args:
        num (float): Target number
        a (float): Lower bound of original interval
        b (float): Upper bound of original interval
        c (float): Lower bound of new interval
        d (float): Upper bound of new interval

    Returns:
        float: Rescaled number
    """

    assert a < b and a <= num <= b, "num must be in [a, b] where a != b"
    assert c <= d, f"{c} > {d}. c must not be greater than d."

    return (num - a) * (d - c) / (b - a) + c


def clamp(
    num: float,
    a: float,
    b: float,
) -> float:
    """
    Restrict a number to a specific range.

    Args:
        num (float): Target number
        a (float): Lower bound of the range
        b (float): Upper bound of the range

    Returns:
        float: `num` clamped between `a` and `b`. Equivalent to 

        ```python
        if a <= num <= b:
            return num
        elif num < a:
            return a
        else:
            return b
        ```
    """

    assert a <= b, f"{a} > {b}. a must not be greater than b."

    return max(a, min(num, b))


def get_num_len(num: float) -> int:
    """
    Get the length of a number.

    Args:
        num (float): Target number

    Returns:
        int: Length of `num`
    """

    return len(str(num))
