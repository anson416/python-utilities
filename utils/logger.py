# -*- coding: utf-8 -*-
# File: logger.py

import json
import logging
import logging.config
import os
from typing import Any, Optional

from . import beartype
from .color import colored
from .date_time import get_date, get_datetime, get_time
from .file_ops import create_dir
from .types import Pathlike, StrDict

__all__ = ["get_logger"]

_LOG_LEVEL_DICT = {
    logging.DEBUG: ("DBG", "dark_grey"),
    logging.INFO: ("INF", "green"),
    logging.WARNING: ("WRN", "yellow"),
    logging.ERROR: ("ERR", "light_red"),
    logging.CRITICAL: ("CRT", "red"),
}
_UNKNOWN_LOG = ("UNK", "white")


class _ConsoleFormatter(logging.Formatter):
    @beartype
    def format(self, record: logging.LogRecord) -> str:
        info = "[%(asctime)s @%(name)s/%(filename)s:%(lineno)d]"
        msg = colored("%(message)s", "white")
        abbrev, color = _LOG_LEVEL_DICT.get(record.levelno, _UNKNOWN_LOG)
        fmt = f"{colored(f'{info} [{abbrev}]', color)} {msg}"

        self._style._fmt = fmt
        self._fmt = fmt
        
        return super().format(record)
    

class _FileFormatter(logging.Formatter):
    @beartype
    def format(self, record: logging.LogRecord) -> str:
        log_dict = {
            "name": record.name,
            "level": _LOG_LEVEL_DICT.get(record.levelno, _UNKNOWN_LOG[:1])[0],
            "func": f"{record.filename}/{record.funcName}",
            "line": record.lineno,
            "date": get_date(),
            "time": get_time(),
            "msg": record.msg,
        }

        return json.dumps(log_dict)


@beartype
def _get_logger_config(
    datefmt: Optional[str] = None,
    log_dir: Optional[Pathlike] = None,
    maxBytes: int = 0,
    backupCount: int = 0,
) -> StrDict[Any]:
    logger_config = {
        "version": 1,
        "formatters": {
            "console_formatter": {
                "()": _ConsoleFormatter,
                "datefmt": datefmt,
            },
            "file_formatter": {
                "()": _FileFormatter,
            }
        },
        "handlers": {
            "console_handler": {
                "class": "logging.StreamHandler",
                "formatter": "console_formatter",
                "level": "DEBUG",
            }
        },
        "root": {
            "handlers": ["console_handler"],
            "level": "DEBUG",
        }
    }
    if log_dir:
        date_time = get_datetime(date_format=r'%Y%m%d', time_format=r'%H%M%S', sep='-')
        log_dir = os.path.join(log_dir, f"log_{date_time}")
        create_dir(log_dir)
        logger_config["handlers"]["file_handler"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "file_formatter",
            "level": "INFO",
            "filename": os.path.join(log_dir, "log.jsonl"),
            "maxBytes": maxBytes,
            "backupCount": backupCount,
        }
        logger_config["root"]["handlers"].append("file_handler")

    return logger_config


@beartype
def get_logger(
    logger_name: Optional[str] = None,
    datetime_format: Optional[str] = r"%Y-%m-%d %H:%M:%S",
    log_dir: Optional[Pathlike] = None,
    max_bytes: int = 50 * (1024 ** 3),
    backup_count: int = 100,
) -> logging.Logger:
    if not logger_name:
        logger_name = __name__

    logger_config = _get_logger_config(
        datefmt=datetime_format,
        log_dir=log_dir,
        maxBytes=max_bytes,
        backupCount = backup_count,
    )
    logging.config.dictConfig(logger_config)
    logger = logging.getLogger(logger_name)

    return logger
