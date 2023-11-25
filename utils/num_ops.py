# -*- coding: utf-8 -*-
# File: num_ops.py

from numbers import Real
from typing import Optional

__all__ = [
    "is_even",
    "is_odd",
    "rescale_num",
    "clamp",
    "get_num_len",
    "round_",
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
    num: Real,
    a: Real,
    b: Real,
    c: Real,
    d: Real,
) -> float:
    """
    Map a number in [a, b] (a != b) to [c, d].

    Args:
        num (Real): Target number
        a (Real): Lower bound of original interval
        b (Real): Upper bound of original interval
        c (Real): Lower bound of new interval
        d (Real): Upper bound of new interval

    Returns:
        float: Rescaled number
    """

    assert a < b and a <= num <= b, "num must be in [a, b] where a != b"
    assert c <= d, f"{c} > {d}. c must not be greater than d."

    return (num - a) * (d - c) / (b - a) + c


def clamp(
    num: Real,
    a: Real,
    b: Real,
) -> Real:
    """
    Restrict a number to a specific range.

    Args:
        num (Real): Target number
        a (Real): Lower bound of the range
        b (Real): Upper bound of the range

    Returns:
        Real: `num` clamped between `a` and `b`. Equivalent to 

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


def get_num_len(num: Real) -> int:
    """
    Get the length of a number.

    Args:
        num (Real): Target number

    Returns:
        int: Length of `num`
    """

    return len(str(num))


def round_(
    num: Real,
    base: Real,
    prec: Optional[int] = None,
) -> Real:
    """
    Round a number to the nearest integral multiple of another number (base). 
    Credit: https://stackoverflow.com/a/18666678.

    Args:
        num (Real): Target number
        base (Real): Fundamental number of the integral multiple to which `num` will be rounded
        prec (Optional[int], optional): Precision of the rounded number. Defaults to the precision of `base`.

    Returns:
        Real: Rouneded number
    """

    assert base > 0, f"{base} <= 0. base must be a positive number."

    return round(
        base * round(num / base),
        get_num_len(base) - str(base).index(".") - 1 if prec is None and "." in str(base) else 0,
    )
