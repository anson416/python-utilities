# -*- coding: utf-8 -*-
# File: logger.py

import gzip
import json
import logging
import logging.config
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Literal, Optional

from .color import colored
from .date_time import get_date, get_datetime, get_time
from .file_ops import create_dir, remove_file
from .types_ import PathLike, StrDict

__all__ = ["get_logger"]

_LOG_LEVEL_DICT = {
    logging.DEBUG:    ("DBG", "dark_grey"),
    logging.INFO:     ("INF", "green"),
    logging.WARNING:  ("WRN", "yellow"),
    logging.ERROR:    ("ERR", "light_red"),
    logging.CRITICAL: ("CRT", "red"),
}
_UNKNOWN_LOG = ("UNK", "white")


class _ConsoleFormatter(logging.Formatter):
    """
    A custom formatter for logging to console.
    """

    # Override
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
    A custom formatter for logging to file (JSON Lines).
    """

    # Override
    def format(self, record: logging.LogRecord) -> str:
        log_dict = {
            "name": record.name,
            "level": _LOG_LEVEL_DICT.get(record.levelno, _UNKNOWN_LOG[:1])[0],
            "file": record.filename,
            "func": record.funcName,
            "line": record.lineno,
            "date": get_date(),
            "time": get_time(),
            "msg": record.msg,
        }
        return json.dumps(log_dict)


class _InfiniteFileHandler(RotatingFileHandler):
    """
    A custom file handler for making infinitely many log backups.
    """

    def __init__(
        self,
        filename: PathLike,
        maxBytes: int = 0,
        compress: bool = False,
    ) -> None:
        super().__init__(filename, maxBytes=maxBytes)
        self._compress = compress
        self._backup_count = 0

    # Override
    def doRollover(self) -> None:
        if self.stream:
            self.stream.close()
            self.stream = None
        self._backup_count += 1
        date_time = get_datetime()
        backup_name = f"{self.baseFilename}.{date_time}.{self._backup_count}"
        self.rotate(self.baseFilename, backup_name)
        if self._compress:
            with open(backup_name, "rb") as f_in, \
                 gzip.open(f"{backup_name}.gz", "wb") as f_out:
                f_out.writelines(f_in)
            remove_file(backup_name)
        if not self.delay:
            self.stream = self._open()


def _get_logger_config(
    name: str = __name__,
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO",
    datetime_format: Optional[str] = r"%Y-%m-%d %H:%M:%S",
    log_dir: Optional[PathLike] = None,
    max_bytes: int = 0,
    compress: bool = False,
) -> StrDict[Any]:
    """
    Construct a configuration dictionary for logging.config.dictConfig().

    Args:
        name (str, optional): Name of logger. Defaults to __name__.
        level (str, optional): Level of logging. Must be any one in 
            {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}. Defaults to 
            "INFO".
        datetime_format (Optional[str], optional): Date and time format. 
            Defaults to r"%Y-%m-%d %H:%M:%S".
        log_dir (Optional[PathLike], optional): If not None, logs will be 
            written to "`log_dir`/log_<current_date_time>". Defaults to None.
        max_bytes (int, optional): If `max_bytes` > 0, each log file will 
            store at most `max_bytes` bytes (i.e., rollover). Used only if 
            `log_dir` is not None. Defaults to 0.
        compress (bool, optional): Compress backup (i.e., rotated) log files. 
            Used only if `log_dir` is not None. Defaults to False.

    Returns:
        StrDict[Any]: Configuration dictionary.
    """

    # Basic configuration dictionary
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
                "level": level,
            }
        },
        "loggers": {
            name: {
                "handlers": ["console_handler"],
                "level": logging.DEBUG,
                "propagate": False,
            },
        },
    }

    # Modify configuration to save logs to files
    if log_dir is not None:
        assert max_bytes >= 0, f"{max_bytes} < 0. `max_bytes` must be a non-negative integer."
        create_dir(log_dir := Path(log_dir) / f"log_{get_datetime()}", exist_ok=True)
        logger_config["handlers"]["file_handler"] = {
            "()": _InfiniteFileHandler,
            "formatter": "file_formatter",
            "level": logging.DEBUG,
            "filename": log_dir / "log.jsonl",
            "maxBytes": max_bytes,
            "compress": compress,
        }
        logger_config["loggers"][name]["handlers"].append("file_handler")

    return logger_config


def get_logger(
    name: str = __name__,
    datetime_format: Optional[str] = r"%Y-%m-%d %H:%M:%S",
    log_dir: Optional[PathLike] = None,
    max_bytes: int = 10 * (1024 ** 2),
    compress: bool = False,
) -> logging.Logger:
    """
    Get custom logger.

    Usage:

        ```python
        logger = get_logger()
        logger.debug("log debug message")
        logger.info("log info message")
        logger.warning("log warning message")
        logger.error("log error message")
        logger.critical("log critical message")
        ```

    Args:
        name (str, optional): Name of logger. Defaults to `__name__`.
        datetime_format (Optional[str], optional): Date and time format. 
            Defaults to r"%Y-%m-%d %H:%M:%S".
        log_dir (Optional[PathLike], optional): If not None, logs will be 
            written to "`log_dir`/log_<current_date_time>". Defaults to None.
        max_bytes (int, optional): If `max_bytes` > 0, each log file will 
            store at most `max_bytes` bytes. Used only if `log_dir` is not 
            None. Defaults to 10 * (1024 ** 2) = 10 MB.
        compress (bool, optional): Compress backup (i.e., rotated) log files. 
            Used only if `log_dir` is not None. Defaults to False.

    Returns:
        logging.Logger: Custom logger.
    """

    logger_config = _get_logger_config(
        name=name,
        datetime_format=datetime_format,
        log_dir=log_dir,
        max_bytes=max_bytes,
        compress=compress,
    )
    logging.config.dictConfig(logger_config)
    return logging.getLogger(name)
