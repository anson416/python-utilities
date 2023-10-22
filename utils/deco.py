# -*- coding: utf-8 -*-
# File: deco.py

from typing import Any, Callable, Optional, Tuple

from .formatter import args2str, kwargs2str
from .types import StrDict

__all__ = [
    "timer_",
    "debugger",
]


def timer_(
    callback: Optional[Callable[[str, Tuple[Any], StrDict[Any], float], None]] = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A decorator for measuring a function's execution time using time.perf_counter().

    Args:
        callback (Optional[Callable[[str, Tuple[Any], StrDict[Any], float], None]], optional): A function that takes \
            the target function's name (str), positional (tuple) and keyword (dict) arguments passed to that function, \
            and execution time (float) as inputs, and returns nothing. Defaults to \
            `lambda f, a, k, t: print(f"{f}({args2str(a)}, {kwargs2str(k)}): {round(t, 3)} s")`.

    Returns:
        Callable[[Callable[..., Any]], Callable[..., Any]]: A function that behaves the same way as the target \
            function with added logging capability
    """

    import time

    def timer__(func: Callable[..., Any]) -> Callable[..., Any]:
        nonlocal callback

        if not callback:
            callback = lambda f, a, k, t: print(f"{f}({args2str(a)}, {kwargs2str(k)}): {round(t, 3)} s")

        def inner(*args: Any, **kwargs: Any) -> Any:
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            callback(func.__name__, args, kwargs, end_time - start_time)

            return result
        return inner
    return timer__


def debugger(
    call_callback: Optional[Callable[[str, Tuple[Any], StrDict[Any]], None]] = None,
    return_callback: Optional[Callable[[str, Tuple[Any], StrDict[Any], Any], None]] = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    A decorator for showing what arguments are passed to the target function (useful for debugging).

    Args:
        call_callback (Optional[Callable[[str, Tuple[Any], StrDict[Any]], None]], optional): A function that takes \
            the target function's name (str), and positional (tuple) and keyword (dict) arguments passed to that \
            function as inputs, and returns nothing. Defaults to \
            `lambda f, a, k: print(f"Calling {f}({args2str(a)}, {kwargs2str(k)})")`.
        return_callback (Optional[Callable[[str, Tuple[Any], StrDict[Any], Any], None]], optional): A function that \
            takes the target function's name (str), positional (tuple) and keyword (dict) arguments passed to that \
            function, and returned value from that function as inputs, and returns nothing. Defaults to \
            `lambda f, a, k, r: print(f"{f}({args2str(a)}, {kwargs2str(k)}): {r}")`.

    Returns:
        Callable[[Callable[..., Any]], Callable[..., Any]]: A function that behaves the same way as the target \
            function with added logging capability
    """

    def debugger_(func: Callable[..., Any]) -> Callable[..., Any]:
        nonlocal call_callback, return_callback

        if not call_callback:
            call_callback = lambda f, a, k: print(f"Calling {f}({args2str(a)}, {kwargs2str(k)})")
        if not return_callback:
            return_callback = lambda f, a, k, r: print(f"{f}({args2str(a)}, {kwargs2str(k)}): {r}")

        def inner(*args: Any, **kwargs: Any) -> Any:
            call_callback(func.__name__, args, kwargs)
            result = func(*args, **kwargs)
            return_callback(func.__name__, args, kwargs, result)

            return result
        return inner
    return debugger_
