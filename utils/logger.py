# -*- coding: utf-8 -*-
# File: logger.py

import logging
import logging.config
from logging.handlers import RotatingFileHandler
from typing import Any, Optional

from . import beartype
from .color import colored
from .types import Pathlike, StrDict

__all__ = ["get_logger",
           "set_log_dir"]


class _ConsoleFormatter(logging.Formatter):
    @beartype
    def __init__(self, datefmt: Optional[str] = None) -> None:
        super().__init__(datefmt=datefmt)

    @beartype
    def format(self, record: logging.LogRecord) -> str:
        info = "[%(asctime)s @%(name)s/%(filename)s:%(lineno)d]"
        msg = colored("%(message)s", "white")
        level_no = record.levelno

        if level_no == logging.DEBUG:
            fmt = colored(f"{info} [DBG]", "dark_grey")
        elif level_no == logging.INFO:
            fmt = colored(f"{info} [INF]", "green")
        elif level_no == logging.WARNING:
            fmt = colored(f"{info} [WRN]", "yellow")
        elif level_no == logging.ERROR:
            fmt = colored(f"{info} [ERR]", "light_red")
        elif level_no == logging.CRITICAL:
            fmt = colored(f"{info} [CRT]", "red")
        else:
            fmt = f"{info} {msg}"
        fmt += f" {msg}"
        self._style._fmt = fmt
        
        return super().format(record)
    

class _FileFormatter(logging.Formatter):
    @beartype
    def __init__(self, datefmt: Optional[str] = None) -> None:
        super().__init__(datefmt=datefmt)

    @beartype
    def format(self, record: logging.LogRecord) -> str:
        info = "[%(asctime)s @%(name)s/%(filename)s/%(funcName)s:%(lineno)d]"
        level_no = record.levelno

        if level_no == logging.DEBUG:
            mode = " [DBG]"
        elif level_no == logging.INFO:
            mode = " [INF]"
        elif level_no == logging.WARNING:
            mode = " [WRN]"
        elif level_no == logging.ERROR:
            mode = " [ERR]"
        elif level_no == logging.CRITICAL:
            mode = " [CRT]"
        else:
            mode = ""

        return f"{info}{mode} %(message)s"


@beartype
def _get_logger_config(datefmt: Optional[str] = None) -> StrDict[Any]:
    logger_config = {
        "version": 1,
        "formatters": {
            "console_formatter": {
                "()": _ConsoleFormatter,
                "datefmt": datefmt
            }
        },
        "handlers": {
            "console_handler": {
                "class": "logging.StreamHandler",
                "formatter": "console_formatter",
                "level": "DEBUG"
            }
        },
        "root": {
            "handlers": ["console_handler"],
            "level": "DEBUG"
        }
    }

    return logger_config


@beartype
def get_logger(
    logger_name: Optional[str] = None,
    datetime_format: Optional[str] = r"%Y-%m-%d %H:%M:%S",
) -> logging.Logger:
    if not logger_name:
        logger_name = __name__

    logging.config.dictConfig(_get_logger_config(datefmt=datetime_format))
    logger = logging.getLogger(logger_name)

    file_handler = RotatingFileHandler("log.jsonl", maxBytes=2000)
    file_handler.setFormatter(_FileFormatter(datefmt=datetime_format))
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    return logger
