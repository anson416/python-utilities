# -*- coding: utf-8 -*-
# File: color.py

from typing import Optional

from colorama import Back, Fore, Style, just_fix_windows_console

from . import beartype

__all__ = ["Color",
           "colored"]

just_fix_windows_console()

from termcolor import colored

class Color:
    _FORE = Fore.__dict__
    _BACK = Back.__dict__

    @classmethod
    @beartype
    def colored(cls, text: str, fore_color: Optional[str] = None, back_color: Optional[str] = None) -> str:
        if fore_color:
            text = f"{cls._FORE[fore_color.upper()]}{text}"

        if back_color:
            text = f"{cls._BACK[back_color.upper()]}{text}"

        return f"{text}{Style.RESET_ALL}"
    
    @property
    @beartype
    def fore(self) -> list[str]:
        return list(self._FORE.keys())
    
    @property
    @beartype
    def back(self) -> list[str]:
        return list(self._BACK.keys())


# @beartype
# def colored(text: str, fore_color: Optional[str] = None, back_color: Optional[str] = None) -> str:
#     return Color.colored(text, fore_color=fore_color, back_color=back_color)
