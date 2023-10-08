# -*- coding: utf-8 -*-
# File: num_ops.py

from .types import Number

__all__ = [
    "is_even",
    "is_odd",
    "rescale_num",
    "clamp",
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
    num: Number,
    a: Number,
    b: Number,
    c: Number,
    d: Number,
) -> float:
    """
    Map a number in [a, b] (a != b) to [c, d].

    Args:
        num (Number): Target number
        a (Number): Lower bound of original interval
        b (Number): Upper bound of original interval
        c (Number): Lower bound of new interval
        d (Number): Upper bound of new interval

    Returns:
        float: Rescaled number
    """

    assert a < b and a <= num <= b, "num must be in [a, b] where a != b"
    assert c <= d, "c must not be greater than d"

    return (num - a) * (d - c) / (b - a) + c


def clamp(
    num: Number,
    a: Number,
    b: Number,
) -> Number:
    """
    Restrict a number to a range [a, b].

    Args:
        num (Number): Target number
        a (Number): Lower bound of the range
        b (Number): Upper bound of the range

    Returns:
        Number: Clamped number
    """

    assert a <= b, "a must not be greater than b"

    return max(a, min(num, b))
