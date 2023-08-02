# -*- coding: utf-8 -*-
# File: logger.py

import logging
import logging.config
from typing import Any, Optional

from . import beartype
from .color import colored
from .types import Pathlike, StrDict

_LOG_DIR: Optional[Pathlike] = None
_LOGGER_NAME: Optional[str] = None
_DATETIME_FORMAT: str = r"%Y-%m-%d %H:%M:%S"


class _ConsoleFormatter(logging.Formatter):
    @beartype
    def __init__(self, datefmt: Optional[str] = None) -> None:
        super().__init__(datefmt=datefmt)

    @beartype
    def format(self, record: logging.LogRecord) -> str:
        info = "[%(asctime)s @%(name)s/%(filename)s:%(lineno)d]"
        # info = colored("[%(asctime)s @%(name)s/%(filename)s:%(lineno)d]", "GREEN")
        msg = colored("%(message)s", "RESET")
        print(record.levelno)

        if record.levelno == logging.DEBUG:
            fmt = colored(f"{info} [DBG]", "WHITE")
        elif record.levelno == logging.INFO:
            fmt = colored(f"{info} [DBG]", "GREEN")
        elif record.levelno == logging.WARNING:
            fmt = colored(f"{info} [DBG]", "YELLOW")
        elif record.levelno == logging.ERROR:
            fmt = colored(f"{info} [DBG]", "RED")
        elif record.levelno == logging.CRITICAL:
            fmt = colored(f"{info} [DBG]", "MAGENTA")
        else:
            fmt = f"{info} {msg}"
        fmt += f" {msg}"
        self._style._fmt = fmt  # pylint: disable=W0212
        # self._fmt = fmt
        return super().format(record)


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
def get_logger(logger_name: Optional[str] = None, datetime_format: Optional[str] = r"%Y%m%d-%H%M%S") -> logging.Logger:
    if not logger_name:
        logger_name = __name__

    logging.config.dictConfig(_get_logger_config(datefmt=datetime_format))
    logger = logging.getLogger(logger_name)

    return logger
