# -*- coding: utf-8 -*-
# File: __init__.py

from pathlib import Path
from typing import (Annotated, Any, Callable, Dict, Iterator, List, Optional,
                    Tuple, TypeVar, Union)

__all__ = [
    "Annotated",
    "Any",
    "Callable",
    "Dict",
    "Iterator",
    "List",
    "Optional",
    "Tuple",
    "Union",
    "Number",
    "Array",
    "Path",
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
