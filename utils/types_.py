# -*- coding: utf-8 -*-
# File: utils/types_.py

from pathlib import Path
from typing import Dict, List, Tuple, TypeVar, Union

__all__ = [
    "Array",
    "PathLike",
    "StrDict",
]

T = TypeVar("T")

# Type for union of list and tuple
Array = Union[List[T], Tuple[T, ...]]

# Type for file or directory path
PathLike = Union[str, Path]

# Type for dictionary with string as key
StrDict = Dict[str, T]
