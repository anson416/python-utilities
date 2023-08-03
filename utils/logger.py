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

__all__ = [
    "get_logger",
]

_LOG_LEVEL_DICT = {
    logging.DEBUG: ("DBG", "dark_grey"),
    logging.INFO: ("INF", "green"),
    logging.WARNING: ("WRN", "yellow"),
    logging.ERROR: ("ERR", "light_red"),
    logging.CRITICAL: ("CRT", "red"),
}
_UNKNOWN_LOG = ("UNK", "white")


class _ConsoleFormatter(logging.Formatter):
    """
    A formatter for logging to console.
    """

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
    """
    A formatter for logging to file (JSON Lines).
    """

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
    datetime_format: Optional[str] = None,
    log_dir: Optional[Pathlike] = None,
    max_bytes: int = 0,
    backup_count: int = 0,
) -> StrDict[Any]:
    """
    Construct a dict config for logging.config.dictConfig().

    Args:
        datetime_format (Optional[str], optional): Date and time format. Defaults to None.
        log_dir (Optional[Pathlike], optional): If not None, logs will be written to log_dir/log_<current_date_time>. \
            Defaults to None.
        max_bytes (int, optional): If max_bytes > 0 and backup_count > 0, each log file will store at most max_bytes \
            bytes. Used only if log_dir is not None. Defaults to 0.
        backup_count (int, optional): If backup_count > 0 and max_bytes > 0, the system will save at most backup_count \
            old log files. Used only if log_dir is not None. Defaults to 0.

    Returns:
        StrDict[Any]: Dict config
    """

    logger_config = {
        "version": 1,
        "formatters": {
            "console_formatter": {
                "()": _ConsoleFormatter,
                "datefmt": datetime_format,
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
        assert max_bytes >= 0, "max_bytes must be non-negative integer"
        assert backup_count >= 0, "backup_count must be non-negative integer"

        date_time = get_datetime(date_format=r'%Y%m%d', time_format=r'%H%M%S', sep='-')
        log_dir = os.path.join(log_dir, f"log_{date_time}")
        create_dir(log_dir)
        logger_config["handlers"]["file_handler"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "file_formatter",
            "level": "INFO",
            "filename": os.path.join(log_dir, "log.jsonl"),
            "maxBytes": max_bytes,
            "backupCount": backup_count,
        }
        logger_config["root"]["handlers"].append("file_handler")

    return logger_config


@beartype
def get_logger(
    logger_name: Optional[str] = __name__,
    datetime_format: Optional[str] = r"%Y-%m-%d %H:%M:%S",
    log_dir: Optional[Pathlike] = None,
    max_bytes: int = 10 * (1024 ** 2),
    backup_count: int = 10,
) -> logging.Logger:
    """
    Get custom logger.

    Args:
        logger_name (Optional[str], optional): Name of logger. Defaults to __name__.
        datetime_format (Optional[str], optional): Date and time format. Defaults to r"%Y-%m-%d %H:%M:%S".
        log_dir (Optional[Pathlike], optional): If not None, logs will be written to log_dir/log_<current_date_time>. \
            Defaults to None.
        max_bytes (int, optional): If max_bytes > 0 and backup_count > 0, each log file will store at most max_bytes \
            bytes. Used only if log_dir is not None. Defaults to 0.
        backup_count (int, optional): If backup_count > 0 and max_bytes > 0, the system will save at most backup_count \
            old log files. Used only if log_dir is not None. Defaults to 0.

    Returns:
        logging.Logger: Custom logger
    """

    logger_config = _get_logger_config(
        datetime_format=datetime_format,
        log_dir=log_dir,
        max_bytes=max_bytes,
        backup_count = backup_count,
    )
    logging.config.dictConfig(logger_config)
    logger = logging.getLogger(logger_name)

    return logger
