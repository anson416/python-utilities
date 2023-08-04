# -*- coding: utf-8 -*-
# File: __init__.py

from pathlib import Path
from typing import TypeVar, Union

__all__ = [
    "Array",
    "Path",
    "Pathlike",
    "StrDict",
]

T = TypeVar("T")

# Type for a union of list and tuple
Array = Union[list[T], tuple[T, ...]]

# Type for file or directory path
Pathlike = Union[str, Path]

# Type for dictionary with string as key
StrDict = dict[str, T]
