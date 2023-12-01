# -*- coding: utf-8 -*-
# File: array.py

from numbers import Real
from typing import Any, Iterator, Tuple

from .types_ import Array

__all__ = [
    "get_all_combs",
    "split_arr",
    "get_batches",
]


def get_all_combs(arr: Array[Any]) -> Iterator[Tuple[Any, ...]]:
    """
    Get all nC1 + nC2 + ... + nCn = 2^n - 1 combinations for an array of 
    length n.

    Args:
        arr (Array[Any]): Target array.

    Yields:
        Iterator[Tuple[Any, ...]]: All combinations from `arr`.
    """

    from itertools import combinations
    return (c
            for comb in map(lambda x: tuple(combinations(arr, x)), range(1, len(arr) + 1))
            for c in comb)


def split_arr(
    arr: Array[Any],
    weights: Array[Real],
) -> Iterator[Array[Any]]:
    """
    Split an array according to some given weights. The weights will be 
    normalized during runtime by dividing each weight by the total sum of all 
    weights.

    Args:
        arr (Array[Any]): Target array.
        weights (Array[Real]): Unnormalized weights based on which `arr` will 
            be split.

    Yields:
        Iterator[Array[Any]]: Split arrays.
    """

    assert len(weights) > 0, "`weights` must be non-empty."
    assert all(map(lambda x: x >= 0, weights)), "`weights` must contain only non-negative numbers."

    start_idx = 0
    for weight in map(lambda x: x / sum(weights), weights[:-1]):  # Last split is determined by previous splits
        yield arr[start_idx:(start_idx := start_idx + round(len(arr) * weight))]
    else:
        yield arr[start_idx:]


def get_batches(
    arr: Array[Any],
    batch_size: int,
) -> Iterator[Array[Any]]:
    """
    Get evenly split batches from an array.

    Args:
        arr (Array[Any]): Target array.
        batch_size (int): Size of each batch.

    Yields:
        Iterator[Array[Any]]: Batches from `arr`, each of which has length at 
            most `batch_size`.
    """

    assert batch_size > 0, f"{batch_size} <= 0. `batch_size` must be a positive integer."
    return (batch
            for batch in split_arr(arr, [batch_size] * (len(arr) // batch_size) + [len(arr) % batch_size])
            if len(batch) > 0)  # Filter out empty batch
