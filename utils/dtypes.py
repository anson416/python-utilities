from pathlib import Path
from typing import Annotated, Union

from pydantic import StringConstraints

PathLike = Union[Path, str]
NonEmptyStr = Annotated[str, StringConstraints(strict=True, min_length=1)]
