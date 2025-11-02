import warnings
from typing import Any

try:
    from colorama import just_fix_windows_console  # type: ignore

    just_fix_windows_console()
except ImportError:
    pass
try:
    from termcolor import colored  # type: ignore
except ImportError:
    warnings.warn("termcolor is not installed")

    def colored(text: object, *args: Any, **kwargs: Any) -> str:
        return str(text)
