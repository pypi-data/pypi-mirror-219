__all__ = [
    "configure_new_logger",
    "configure_existing_logger",
    "configure_existing_loggers",
    "logger",
]

import logging
import os
from datetime import datetime, timezone
from typing import Union

from pythonjsonlogger import jsonlogger

from rcplus_alloy_common.constants import (
    LOGGING_DATETIME_FORMAT,
    LOGGING_FORMAT,
    LOG_LEVEL,
    LOG_MODE,
    LOG_NAME,
)


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def formatTime(self, record, datefmt=None):
        return f"{datetime.fromtimestamp(record.created, tz=timezone.utc).strftime(LOGGING_DATETIME_FORMAT)[:-3]}Z"

    def process_log_record(self, log_record):
        dag_id = os.getenv("DAG_ID")
        if dag_id is not None:
            log_record["dag_id"] = dag_id
        dag_run_id = os.getenv("DAG_RUN_ID")
        if dag_run_id is not None:
            log_record["dag_run_id"] = dag_run_id
        return super().process_log_record(log_record)


class CustomLoggingFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        return f"{datetime.fromtimestamp(record.created, tz=timezone.utc).strftime(LOGGING_DATETIME_FORMAT)[:-3]}Z"


def configure_new_logger(
        log_name: str = LOG_NAME,
        log_mode: str = LOG_MODE,
        log_level: Union[str, int] = LOG_LEVEL,
        capture_warnings: bool = True,
) -> logging.Logger:
    """
    Configure a new logger.
    """
    logging.captureWarnings(capture_warnings)

    if log_mode == "JSON":
        handler = logging.StreamHandler()
        handler.setFormatter(
            CustomJsonFormatter(LOGGING_FORMAT, rename_fields={"levelname": "level", "asctime": "time"})
        )
    else:
        handler = logging.StreamHandler()
        handler.setFormatter(CustomLoggingFormatter(LOGGING_FORMAT))

    new_logger = logging.getLogger(log_name)
    new_logger.handlers.clear()
    new_logger.setLevel(log_level)
    new_logger.addHandler(handler)

    return new_logger


def create_handler(log_mode: str = LOG_MODE) -> logging.Handler:
    if log_mode == "JSON":
        handler = logging.StreamHandler()
        handler.setFormatter(
            CustomJsonFormatter(LOGGING_FORMAT, rename_fields={"levelname": "level", "asctime": "time"})
        )
    else:
        handler = logging.StreamHandler()
        handler.setFormatter(CustomLoggingFormatter(LOGGING_FORMAT))
    return handler


def configure_existing_loggers(
        log_mode: str = LOG_MODE,
        log_level: Union[str, int] = LOG_LEVEL,
        log_name_filter: str | None = None,
        capture_warnings: bool = True,
) -> None:
    """
    Configure all existing loggers to be the same (output as text/json, level) or
    configure only some specific 3rd party loggers (like urllib3 etc.) using log_name_filter.
    """
    logging.captureWarnings(capture_warnings)

    handler = create_handler(log_mode)

    for log_name in logging.root.manager.loggerDict:
        if log_name_filter is not None and log_name_filter not in log_name:
            continue
        existing_logger = logging.getLogger(log_name)
        existing_logger.handlers.clear()
        existing_logger.setLevel(log_level)
        existing_logger.addHandler(handler)


def configure_existing_logger(
        existing_logger: logging.Logger,
        log_mode: str = LOG_MODE,
        log_level: Union[str, int] = LOG_LEVEL,
        append_handler: bool = False,
        capture_warnings: bool = True,
) -> None:
    """
    (Re-)Configure an existing logger.
    """
    logging.captureWarnings(capture_warnings)

    handler = create_handler(log_mode)

    if not append_handler:
        existing_logger.handlers.clear()

    existing_logger.setLevel(log_level)
    existing_logger.addHandler(handler)


# The default utility logger.
logger = configure_new_logger(log_name=str(os.path.basename(__file__).split(".")[0]))
