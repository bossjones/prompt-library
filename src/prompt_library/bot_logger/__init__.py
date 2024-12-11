#!/usr/bin/env python3

"""
Logging utilities for the SandboxAgent project.

This module provides functions and utilities for configuring and managing logging in the SandboxAgent project.
It includes functions for setting up the global logger, handling exceptions, and filtering log messages.

Functions:
    global_log_config(log_level: LOG_LEVEL, json: bool = False) -> None:
        Configure the global logger with the specified log level and format.

    get_logger(name: str = "prompt_library") -> Logger:
        Get a logger instance with the specified name.

    _log_exception(exc: BaseException, dev_mode: bool = False) -> None:
        Log an exception with the appropriate level based on the dev_mode setting.

    _log_warning(exc: BaseException, dev_mode: bool = False) -> None:
        Log a warning with the appropriate level based on the dev_mode setting.

    filter_out_serialization_errors(record: dict[str, Any]) -> bool:
        Filter out log messages related to serialization errors.

    filter_out_modules(record: dict[str, Any]) -> bool:
        Filter out log messages from the standard logging module.

Constants:
    LOGURU_FILE_FORMAT: str
        The log format string for file logging.

    NEW_LOGGER_FORMAT: str
        The new log format string for console logging.

    LOG_LEVEL: Literal
        The available log levels.

    MASKED: str
        A constant string used to mask sensitive data in logs.

Classes:
    Pii(str):
        A custom string class that masks sensitive data in logs based on the log_pii setting.
"""
# pylint: disable=no-member
# pylint: disable=consider-using-tuple
# pylint: disable=eval-used,no-member
# pyright: ignore[reportOperatorIssue]
# pyright: ignore[reportOptionalIterable]
# SOURCE: https://betterstack.com/community/guides/logging/loguru/

# FIXME: https://github.com/sweepai/sweep/blob/7d93c612568b8febd4aaf3c75810794bc10c09ae/sweepai/utils/event_logger.py#L7
# FIXME: https://github.com/sweepai/sweep/blob/7d93c612568b8febd4aaf3c75810794bc10c09ae/sweepai/utils/event_logger.py#L7
# FIXME: https://github.com/sweepai/sweep/blob/7d93c612568b8febd4aaf3c75810794bc10c09ae/sweepai/utils/event_logger.py#L7
# FIXME: https://github.com/sweepai/sweep/blob/7d93c612568b8febd4aaf3c75810794bc10c09ae/sweepai/utils/event_logger.py#L7
# FIXME: https://github.com/sweepai/sweep/blob/7d93c612568b8febd4aaf3c75810794bc10c09ae/sweepai/utils/event_logger.py#L7
# FIXME: https://github.com/sweepai/sweep/blob/7d93c612568b8febd4aaf3c75810794bc10c09ae/sweepai/utils/event_logger.py#L7
# FIXME: https://github.com/sweepai/sweep/blob/7d93c612568b8febd4aaf3c75810794bc10c09ae/sweepai/utils/event_logger.py#L7
# FIXME: https://github.com/sweepai/sweep/blob/7d93c612568b8febd4aaf3c75810794bc10c09ae/sweepai/utils/event_logger.py#L7
# FIXME: https://github.com/sweepai/sweep/blob/7d93c612568b8febd4aaf3c75810794bc10c09ae/sweepai/utils/event_logger.py#L7

from __future__ import annotations

import contextvars
import functools
import gc
import inspect
import logging
import os
import re
import sys
import time

from datetime import UTC, datetime, timezone
from logging import Logger, LogRecord
from pathlib import Path
from pprint import pformat
from sys import stdout
from time import process_time
from types import FrameType
from typing import TYPE_CHECKING, Any, Deque, Dict, Literal, Optional, Union, cast

import loguru
import pysnooper
import vcr

from loguru import logger
from loguru._defaults import LOGURU_FORMAT
from tqdm import tqdm

from prompt_library.models.loggers import LoggerModel, LoggerPatch


if TYPE_CHECKING:
    from better_exceptions.log import BetExcLogger
    from loguru._logger import Logger as _Logger


LOGLEVEL_MAPPING = {
    50: "CRITICAL",
    40: "ERROR",
    30: "WARNING",
    20: "INFO",
    10: "DEBUG",
    0: "NOTSET",
}

LOGURU_CONSOLE_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level}</level> | "
    "<cyan>{module}</cyan>:<cyan>{line}</cyan> | "
    "<level>{extra[room_id]}</level> - "
    "<level>{message}</level>"
)

LOGURU_FILE_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
    "<level>{extra[room_id]}</level> - "
    "<level>{message}</level>"
)

# NOTE: this is the default format for loguru
_LOGURU_FORMAT = (
    "LOGURU_FORMAT",
    str,
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
)

# NOTE: this is the new format for loguru
NEW_LOGGER_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan> - "
    "<magenta>{file}:{line}</magenta> | "
    "<level>{message}</level> | {extra}"
)


LOG_LEVEL = Literal[
    "TRACE",
    "DEBUG",
    "INFO",
    "SUCCESS",
    "WARNING",
    "ERROR",
    "CRITICAL",
]

# --------------------------------------------------------------------------
# SOURCE: https://github.com/ethyca/fides/blob/e9174b771155abc0ff3faf1fb7b8b76836788617/src/fides/api/util/logger.py#L116
MASKED = "MASKED"


class Pii(str):
    """Mask pii data"""

    def __format__(self, __format_spec: str) -> str:
        """
        Mask personally identifiable information (PII) in log messages.

        This class is a subclass of str and overrides the __format__ method to mask
        PII data in log messages. If the aiosettings.log_pii setting is True, the
        original string value is returned. Otherwise, the string "MASKED" is returned.

        Args:
            __format_spec (str): The format specification string.

        Returns:
            str: The masked or unmasked string value.
        """
        log_pii = True
        if log_pii:
            return super().__format__(__format_spec)
        return MASKED


def _log_exception(exc: BaseException, dev_mode: bool = False) -> None:
    """
    Log an exception with the appropriate level based on the dev_mode setting.

    If dev_mode is True, the entire traceback will be logged using logger.opt(exception=True).error().
    Otherwise, only the exception message will be logged using logger.error().

    Args:
        exc (BaseException): The exception to be logged.
        dev_mode (bool, optional): Whether to log the entire traceback or just the exception message.
            Defaults to False.

    Returns:
        None
    """
    if dev_mode:
        logger.opt(exception=True).error(exc)
    else:
        logger.error(exc)


def _log_warning(exc: BaseException, dev_mode: bool = False) -> None:
    """
    Log a warning with the appropriate level based on the dev_mode setting.

    If dev_mode is True, the entire traceback will be logged using logger.opt(exception=True).warning().
    Otherwise, only the warning message will be logged using logger.warning().

    Args:
        exc (BaseException): The exception or warning to be logged.
        dev_mode (bool, optional): Whether to log the entire traceback or just the warning message.
            Defaults to False.

    Returns:
        None
    """
    if dev_mode:
        logger.opt(exception=True).warning(exc)
    else:
        logger.warning(exc)


def filter_out_serialization_errors(record: dict[str, Any]):
    # Patterns to match the log messages you want to filter out
    patterns = [
        r"Orjson serialization failed:",
        r"Failed to serialize .* to JSON:",
        r"Object of type .* is not JSON serializable",
        # Failed to deepcopy input: TypeError("cannot pickle '_thread.RLock' object") | {}
        r".*Failed to deepcopy input:.*",
        r".*logging:callHandlers.*",
    ]

    # Check if the log message matches any of the patterns
    for pattern in patterns:
        if re.search(pattern, record["message"]):
            return False  # Filter out this message

    return True  # Keep all other messages


def filter_out_modules(record: dict[str, Any]) -> bool:
    """
    Filter out log messages from the standard logging module.

    Args:
        record: The log record to check.

    Returns:
        bool: True if the message should be kept, False if it should be filtered out.
    """
    # Check if the log message originates from the logging module
    if record["name"].startswith("logging"):
        return False  # Filter out this message

    return True  # Keep all other messages


def catch_all_filter(record: dict[str, Any]) -> bool:
    """
    Filter out log messages that match certain patterns or originate from specific modules.

    This function combines the `filter_out_serialization_errors` and `filter_out_modules` filters
    to create a single filter that removes log messages that match certain patterns (related to
    serialization errors) or originate from the standard logging module.

    Args:
        record (dict[str, Any]): The log record to check.

    Returns:
        bool: True if the message should be kept, False if it should be filtered out.
    """

    return filter_out_serialization_errors(record) and filter_out_modules(record)


class TqdmOutputStream:
    """
    A custom output stream that writes to sys.stderr and supports tqdm progress bars.

    This class provides a write method that writes strings to sys.stderr using tqdm.write,
    which allows tqdm progress bars to be displayed correctly. It also provides an isatty
    method that returns whether sys.stderr is a terminal.

    This class is useful when you want to use tqdm progress bars in your application while
    still being able to write to the standard error stream.
    """

    def write(self, string: str = "") -> None:
        """
        Write the given string to sys.stderr using tqdm.write.

        Args:
            string (str): The string to write.
        """
        tqdm.write(string, file=sys.stderr, end="")

    def isatty(self) -> bool:
        """
        Return whether sys.stderr is a terminal.

        Returns:
            bool: True if sys.stderr is a terminal, False otherwise.
        """
        return sys.stderr.isatty()


_console_handler_id: int | None = None
_file_handler_id: int | None = None

_old_log_dir: str | None = None
_old_console_log_level: LOG_LEVEL | None = None
_old_backup_count: int | None = None

# ###################################################################################################
# # NOTE: Make sure we don't log secrets
# # SOURCE: https://github.com/Delgan/loguru/issues/537#issuecomment-986259036
# def obfuscate_message(message: str):
#     """Obfuscate sensitive information."""
#     result = re.sub(r"pass: .*", "pass: xxx", s)
#     return result
#
# def formatter(record):
#     record["extra"]["obfuscated_message"] = obfuscate_message(record["message"])
#     return "[{level}] {extra[obfuscated_message]}\n{exception}"
#
# logger.add(sys.stderr, format=formatter)
# ###################################################################################################


# SOURCE: https://github.com/bossjones/sandbox/blob/8ad412d9726e8ffc76ea8822f32e18a0cb5fc84f/dancedetector/dancedetector/dbx_logger/__init__.py
# References
# Solution comes from:
#   https://pawamoy.github.io/posts/unify-logging-for-a-gunicorn-uvicorn-app/
#   https://github.com/pahntanapat/Unified-FastAPI-Gunicorn-Log
#   https://github.com/Delgan/loguru/issues/365
#   https://loguru.readthedocs.io/en/stable/api/logger.html#sink

# request_id_contextvar is a context variable that will store the request id
# ContextVar works with asyncio out of the box.
# see https://docs.python.org/3/library/contextvars.html
REQUEST_ID_CONTEXTVAR = contextvars.ContextVar("request_id", default=None)

# initialize the context variable with a default value
REQUEST_ID_CONTEXTVAR.set("notset")


def set_log_extras(record: dict[str, Any]) -> None:
    """Set extra log fields in the log record.

    Args:
        record: The log record to modify.
    """
    record["extra"]["datetime"] = datetime.now(UTC)


# SOURCE: https://github.com/joint-online-judge/fastapi-rest-framework/blob/b0e93f0c0085597fcea4bb79606b653422f16700/fastapi_rest_framework/logging.py#L43
def format_record(record: dict[str, Any]) -> str:
    """Custom format for loguru loggers.

    Uses pformat for log any data like request/response body during debug.
    Works with logging if loguru handler it.

    Args:
        record: The log record.

    Returns:
        The formatted log record.
    """
    # """
    # Custom format for loguru loggers.
    # Uses pformat for log any data like request/response body during debug.
    # Works with logging if loguru handler it.

    # Example:
    # -------
    # >>> payload = [{"users":[{"name": "Nick", "age": 87, "is_active": True},
    # >>>     {"name": "Alex", "age": 27, "is_active": True}], "count": 2}]
    # >>> logger.bind(payload=).debug("users payload")
    # >>> [   {   'count': 2,
    # >>>         'users': [   {'age': 87, 'is_active': True, 'name': 'Nick'},
    # >>>                      {'age': 27, 'is_active': True, 'name': 'Alex'}]}]

    # """
    format_string = NEW_LOGGER_FORMAT
    if record["extra"].get("payload") is not None:
        record["extra"]["payload"] = pformat(record["extra"]["payload"], indent=4, compact=True, width=88)
        format_string += "\n<level>{extra[payload]}</level>"

    format_string += "{exception}\n"
    return format_string


class InterceptHandler(logging.Handler):
    """
    Intercept all logging calls (with standard logging) into our Loguru Sink
    See: https://github.com/Delgan/loguru#entirely-compatible-with-standard-logging
    """

    loglevel_mapping = {
        logging.CRITICAL: "CRITICAL",
        logging.ERROR: "ERROR",
        logging.FATAL: "FATAL",
        logging.WARNING: "WARNING",
        logging.INFO: "INFO",
        logging.DEBUG: "DEBUG",
        1: "DUMMY",
        0: "NOTSET",
    }

    # from logging import DEBUG
    # from logging import ERROR
    # from logging import FATAL
    # from logging import INFO
    # from logging import WARN
    # https://issueexplorer.com/issue/tiangolo/fastapi/4026
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        """
        Intercept all logging calls (with standard logging) into our Loguru Sink.

        This method is called by the standard logging library whenever a log message
        is emitted. It converts the standard logging record into a Loguru log message
        and logs it using the Loguru logger.

        Args:
            record (logging.LogRecord): The standard logging record to be logged.

        Returns:
            None
        """
        # Get corresponding Loguru level if it exists.
        level: str | int
        try:
            level = loguru.logger.level(record.levelname).name
        except ValueError:
            # DISABLED 12/10/2021 # level = str(record.levelno)
            level = record.levelno

        # INFO: Find Caller Frame
        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            # DISABLED 12/10/2021 # frame = cast(FrameType, frame.f_back)
            depth += 1

        loguru.logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


class InterceptHandlerImproved(logging.Handler):
    """
    Intercept all logging calls (with standard logging) into our Loguru Sink
    """

    def emit(self, record: logging.LogRecord) -> None:
        """
        Intercept and redirect log messages from the standard logging module to Loguru.

        Args:
            record (logging.LogRecord): The standard logging record to be logged.
        """

        # Determine the corresponding Loguru log level.
        level: str | int
        try:
            # Attempt to get the Loguru level name using the record's level name.
            level = logger.level(record.levelname).name
        except ValueError:
            # If the level name is not found, fall back to using the numeric level.
            level = record.levelno

        # Find the stack frame from which the log message originated.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            # Traverse back through the stack frames.
            frame = frame.f_back
            # Increment the depth counter to track how far back we've gone.
            depth += 1

        # Log the message using Loguru, preserving the original context and exception info.
        logger.opt(depth=depth, exception=record.exc_info).log(
            level,  # Use the determined log level.
            record.getMessage(),  # Log the message content.
        )


def get_logger(
    name: str,
    provider: str | None = None,
    level: int = logging.INFO,
    logger: logging.Logger = logger,
) -> logging.Logger:
    """
    Get a logger instance with the specified name and configuration.

    Args:
        name (str): The name of the logger.
        provider (Optional[str], optional): The provider for the logger. Defaults to None.
        level (int, optional): The logging level. Defaults to logging.INFO.
        logger (logging.Logger, optional): The logger instance to use. Defaults to the root logger.

    Returns:
        logging.Logger: The configured logger instance.

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("This is an info message")
    """

    return logger


def request_id_filter(record: dict[str, Any]):
    """
    Inject the request id from the context var to the log record. The logging
    config format is defined in logger_config.yaml and has request_id as a field.
    """
    record["extra"]["request_id"] = REQUEST_ID_CONTEXTVAR.get()


def reset_logging(
    log_dir: str,
    *,
    console_log_level: LOG_LEVEL = "INFO",
    backup_count: int | None = None,
) -> None:
    """
    Reset the logging configuration.

    This function resets the logging configuration by removing any existing
    handlers and adding new handlers for console and file logging. The console
    log level and file backup count can be specified.

    Args:
        log_dir (str): The directory path for the log file.
        console_log_level (LOG_LEVEL, optional): The log level for the console
            handler. Defaults to "INFO".
        backup_count (Optional[int], optional): The number of backup log files
            to keep. If None, no backup files are kept. Defaults to None.

    Returns:
        None
    """
    global _console_handler_id, _file_handler_id
    global _old_log_dir, _old_console_log_level, _old_backup_count
    logger.configure(extra={"room_id": ""})

    if console_log_level != _old_console_log_level:
        if _console_handler_id is not None:
            logger.remove(_console_handler_id)
        else:
            logger.remove()  # remove the default stderr handler

        _console_handler_id = logger.add(
            sys.stderr,
            level=console_log_level,
            format=LOGURU_CONSOLE_FORMAT,
        )

        _old_console_log_level = console_log_level

    # Add file handler if log_dir is provided
    if log_dir:
        if _file_handler_id is not None:
            logger.remove(_file_handler_id)

        log_file = Path(log_dir) / "app.log"
        _file_handler_id = logger.add(
            log_file,
            rotation="1 MB",
            retention=backup_count,
            format=NEW_LOGGER_FORMAT,
            enqueue=True,
        )

        _old_log_dir = log_dir
        _old_backup_count = backup_count


# def reset_logging(log_dir: str, *, console_log_level: LOG_LEVEL = "INFO", backup_count: Optional[int] = None) -> None:

#     global _console_handler_id, _file_handler_id
#     global _old_log_dir, _old_console_log_level, _old_backup_count
#     logger.configure(extra={"room_id": ""})

#     if console_log_level != _old_console_log_level:
#         if _console_handler_id is not None:
#             logger.remove(_console_handler_id)
#         else:
#             logger.remove()  # remove the default stderr handler

#         _console_handler_id = logger.add(sys.stderr, level=console_log_level, format=LOGURU_CONSOLE_FORMAT)

#         _old_console_log_level = console_log_level


def timeit(func):
    def wrapped(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.debug("Function '{}' executed in {:f} s", func.__name__, end - start)
        return result

    return wrapped


def logger_wraps(*, entry=True, exit=True, level="DEBUG"):
    def wrapper(func):
        name = func.__name__

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            logger_ = logger.opt(depth=1)
            if entry:
                logger_.log(level, "Entering '{}' (args={}, kwargs={})", name, args, kwargs)
            result = func(*args, **kwargs)
            if exit:
                logger_.log(level, "Exiting '{}' (result={})", name, result)
            return result

        return wrapped

    return wrapper


# @pysnooper.snoop()
# @pysnooper.snoop(thread_info=True)
# FIXME: https://github.com/abnerjacobsen/fastapi-mvc-loguru-demo/blob/main/mvc_demo/core/loguru_logs.py
# SOURCE: https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger
def global_log_config(log_level: str | int = logging.DEBUG, json: bool = False) -> _Logger:
    """Configure global logging settings.

    Args:
        log_level: The log level to use. Defaults to logging.DEBUG.
        json: Whether to format logs as JSON. Defaults to False.

    Returns:
        The configured logger instance.
    """

    # The logger is pre-configured for convenience with a default handler which writes messages to |sys.stderr|. You should |remove| it first if you plan to |add| another handler logging messages to the console, otherwise you may end up with duplicated logs.
    # logger.remove()  # Remove all handlers added so far, including the default one.
    # logger.add(sys.stdout, level="DEBUG")

    # SOURCE: https://github.com/acgnhiki/blrec/blob/975fa2794a3843a883597acd5915a749a4e196c8/src/blrec/logging/configure_logging.py#L21
    global _console_handler_id, _file_handler_id
    global _old_log_dir, _old_console_log_level, _old_backup_count
    # SOURCE: https://github.com/acgnhiki/blrec/blob/975fa2794a3843a883597acd5915a749a4e196c8/src/blrec/logging/configure_logging.py#L21

    if isinstance(log_level, str) and (log_level in logging._nameToLevel):
        log_level = logging.DEBUG

    # NOTE: Original
    intercept_handler = InterceptHandler()
    # logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    # intercept_handler = InterceptHandlerImproved()
    # logging.basicConfig(handlers=[intercept_handler], level=log_level, force=True)

    # logging.basicConfig(handlers=[intercept_handler], level=LOG_LEVEL)
    # logging.root.handlers = [intercept_handler]
    logging.root.setLevel(log_level)

    seen = set()
    for name in [
        *logging.root.manager.loggerDict.keys(),  # pylint: disable=no-member
        "asyncio",
        "discord",
        "discord.client",
        "discord.gateway",
        "discord.http",
        "chromadb",
        "langchain_chroma",
        # "selenium",
        # "webdriver_manager",
        # "arsenic",
        # "aiohttp",
        # "tensorflow",
        # "keras",
        # "gunicorn",
        # "gunicorn.access",
        # "gunicorn.error",
        # "uvicorn",
        # "uvicorn.access",
        # "uvicorn.error",
        # "uvicorn.config",
    ]:
        if name not in seen:
            seen.add(name.split(".")[0])
            logging.getLogger(name).handlers = [intercept_handler]

    logger.configure(
        handlers=[
            {
                # sink (file-like object, str, pathlib.Path, callable, coroutine function or logging.Handler) - An object in charge of receiving formatted logging messages and propagating them to an appropriate endpoint.
                "sink": stdout,
                # serialize (bool, optional) - Whether the logged message and its records should be first converted to a JSON string before being sent to the sink.
                "serialize": False,
                # format (str or callable, optional) - The template used to format logged messages before being sent to the sink. If a callable is passed, it should take a logging.Record as its first argument and return a string.
                "format": format_record,
                # diagnose (bool, optional) - Whether the exception trace should display the variables values to eases the debugging. This should be set to False in production to avoid leaking sensitive
                "diagnose": True,
                # backtrace (bool, optional) - Whether the exception trace formatted should be extended upward, beyond the catching point, to show the full stacktrace which generated the error.
                "backtrace": True,
                # enqueue (bool, optional) - Whether the messages to be logged should first pass through a multiprocessing-safe queue before reaching the sink. This is useful while logging to a file through multiple processes. This also has the advantage of making logging calls non-blocking.
                "enqueue": True,
                # catch (bool, optional) - Whether errors occurring while sink handles logs messages should be automatically caught. If True, an exception message is displayed on sys.stderr but the exception is not propagated to the caller, preventing your app to crash.
                "catch": True,
                # filter (callable, optional) - A callable that takes a record and returns a boolean. If the callable returns False, the record is filtered out.
                "filter": filter_out_serialization_errors,
            }
        ],
        # extra={"request_id": REQUEST_ID_CONTEXTVAR.get()},
    )

    print(f"Logger set up with log level: {log_level}")

    setup_uvicorn_logger()
    setup_gunicorn_logger()

    # logger.disable("logging")

    return logger


def setup_uvicorn_logger():
    """
    Set up the uvicorn logger.

    This function configures the uvicorn logger to use the InterceptHandler,
    which allows for better handling and formatting of log messages from uvicorn.
    """
    loggers = (logging.getLogger(name) for name in logging.root.manager.loggerDict if name.startswith("uvicorn."))
    for uvicorn_logger in loggers:
        uvicorn_logger.handlers = []
    logging.getLogger("uvicorn").handlers = [InterceptHandler()]


def setup_gunicorn_logger():
    logging.getLogger("gunicorn.error").handlers = [InterceptHandler()]
    logging.getLogger("gunicorn.access").handlers = [InterceptHandler()]


def get_lm_from_tree(loggertree: LoggerModel, find_me: str) -> LoggerModel | None:
    """Recursively search for a logger model in the logger tree.

    Args:
        loggertree: The root logger model to search from.
        find_me: The name of the logger model to find.

    Returns:
        The found logger model, or None if not found.
    """
    if find_me == loggertree.name:
        print("Found")
        return loggertree
    else:
        for ch in loggertree.children:
            print(f"Looking in: {ch.name}")
            if i := get_lm_from_tree(ch, find_me):
                return i
    return None


def generate_tree() -> LoggerModel:
    """Generate a tree of logger models.

    Returns:
        The root logger model of the generated tree.
    """
    rootm = LoggerModel(name="root", level=logging.getLogger().getEffectiveLevel(), children=[])
    nodesm: dict[str, LoggerModel] = {}
    items = sorted(logging.root.manager.loggerDict.items())  # type: ignore
    for name, loggeritem in items:
        if isinstance(loggeritem, logging.PlaceHolder):
            nodesm[name] = nodem = LoggerModel(name=name, children=[])
        else:
            nodesm[name] = nodem = LoggerModel(name=name, level=loggeritem.getEffectiveLevel(), children=[])
        i = name.rfind(".", 0, len(name) - 1)
        parentm = rootm if i == -1 else nodesm[name[:i]]
        parentm.children.append(nodem)
    return rootm


def obfuscate_message(message: str) -> str:
    """Obfuscate sensitive information in a message.

    Args:
        message: The message to obfuscate.

    Returns:
        The obfuscated message.
    """
    obfuscation_patterns = [
        (r"email: .*", "email: ******"),
        (r"password: .*", "password: ******"),
        (r"newPassword: .*", "newPassword: ******"),
        (r"resetToken: .*", "resetToken: ******"),
        (r"authToken: .*", "authToken: ******"),
        (r"located at .*", "located at ******"),
        (r"#token=.*", "#token=******"),
    ]
    for pattern, replacement in obfuscation_patterns:
        message = re.sub(pattern, replacement, message)

    return message


def formatter(record: dict[str, Any]) -> str:
    """Format a log record.

    Args:
        record: The log record to format.

    Returns:
        The formatted log record.
    """
    record["extra"]["obfuscated_message"] = record["message"]
    return (
        "<green>[{time:YYYY-MM-DD HH:mm:ss}]</green> <level>[{level}]</level> - "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{extra[obfuscated_message]}</level>\n{exception}"
    )


def formatter_sensitive(record: dict[str, Any]) -> str:
    """Format a log record with sensitive information obfuscated.

    Args:
        record: The log record to format.

    Returns:
        The formatted log record with sensitive information obfuscated.
    """
    record["extra"]["obfuscated_message"] = obfuscate_message(record["message"])
    return (
        "<green>[{time:YYYY-MM-DD HH:mm:ss}]</green> <level>[{level}]</level> - "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{extra[obfuscated_message]}</level>\n{exception}"
    )


# SMOKE-TESTS
if __name__ == "__main__":
    from logging_tree import printout

    global_log_config(
        log_level=logging.getLevelName("DEBUG"),
        json=False,
    )
    LOGGER = logger

    def dump_logger_tree():
        rootm = generate_tree()
        LOGGER.debug(rootm)

    def dump_logger(logger_name: str):
        LOGGER.debug(f"getting logger {logger_name}")
        rootm = generate_tree()
        return get_lm_from_tree(rootm, logger_name)

    LOGGER.info("TESTING TESTING 1-2-3")
    printout()
