# -*- coding: utf-8 -*-
# File: num_ops.py

from . import beartype

__all__ = [
    "is_even",
    "is_odd",
    "rescale_num",
]


@beartype
def is_even(num: int) -> bool:
    """
    Return True if a number is even.

    Args:
        num (int): Target number

    Returns:
        bool: True iff `num` is even
    """

    return num % 2 == 0


@beartype
def is_odd(num: int) -> bool:
    """
    Return True if a number is old.

    Args:
        num (int): Target number

    Returns:
        bool: True iff `num` is old
    """

    return num % 2 != 0


@beartype
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
    assert c <= d, "c must not be greater than d"

    return (num - a) * (d - c) / (b - a) + c
