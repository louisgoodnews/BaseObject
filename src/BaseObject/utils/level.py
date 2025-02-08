"""
Author: lodego
Date: 2024-01-24
"""

from enum import Enum


__all__: List[str] = ["Level"]


class Level(Enum):
    """
    A class representing log levels.

    Attributes:
        CRITICAL (str): The critical log level.
        DEBUG (str): The debug log level.
        ERROR (str): The error log level.
        INFO (str): The info log level.
        SILENT (str): The (custom) silent log level.
        WARNING (str): The warning log level.
    """

    CRITICAL = "CRITICAL"
    DEBUG = "DEBUG"
    ERROR = "ERROR"
    INFO = "INFO"
    SILENT = "SILENT"
    WARNING = "WARNING"
