# -*- coding: utf-8 -*-
# File: color.py

try:
    from colorama import just_fix_windows_console
except ImportError:
    raise ImportError("Could not import colorama. Try `pip install -U colorama`.")
try:
    from termcolor import colored
except ImportError:
    raise ImportError("Could not import termcolor. Try `pip install -U termcolor`.")

__all__ = ["colored"]

just_fix_windows_console()
