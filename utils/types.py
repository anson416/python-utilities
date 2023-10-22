# -*- coding: utf-8 -*-
# File: __init__.py

from pathlib import Path
from typing import Dict, List, Tuple, TypeVar, Union

__all__ = [
    "Number",
    "Array",
    "Pathlike",
    "StrDict",
]

T = TypeVar("T")

# Type for any real number
Number = Union[float, int]

# Type for a union of list and tuple
Array = Union[List[T], Tuple[T, ...]]

# Type for file or directory path
Pathlike = Union[str, Path]

# Type for dictionary with string as key
StrDict = Dict[str, T]
