# -*- coding: utf-8 -*-
# File: __init__.py

"""
Utilities that can be used anywhere.
"""

try:
    from beartype import beartype
except ImportError:
    raise ImportError("Could not import beartype. Try `pip3 install -U beartype`.")

__version__ = "0.1.0"
