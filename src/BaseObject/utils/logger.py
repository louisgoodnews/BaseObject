"""
Author: lodego
Date: 2024-01-24
"""

from datetime import datetime

from typing import *

from utils.logger.level import *


__all__: List[str] = ["Logger"]


class Logger:
    """
    A class for logging messages.

    Attributes:
        level (Level): The level of the logger (Defaults to INFO).
        name (str): The name of the logger.
    """

    # A dictionary of ANSI color codes
    __COLORISATION__: Dict[str, str] = {
        "CRITICAL": "\033[91m",  # Red color code for critical messages
        "DEBUG": "\033[94m",  # Blue color code for debug messages
        "ERROR": "\033[93m",  # Yellow color code for error messages
        "INFO": "\033[92m",  # Green color code for info messages
        "RESET": "\033[0m",  # Reset color code
        "SILENT": "\033[90m",  # Grey color code for silent messages
        "WARNING": "\033[95m",  # Magenta color code for warning messages
    }

    def __init__(
        self,
        name: str,
        level=Level.INFO,
    ) -> None:
        """
        Initializes a new instance of the Logger class.

        :param name: The name of the logger.
        :type name: str

        :param level: The level of the logger (Defaults to INFO).
        :type level: Level

        :return: None
        :rtype: None
        """

        # Store the level of the logger in an instance variable
        self._level: Level = level

        # Store the name of the logger in an instance variable
        self._name: str = name

    @property
    def level(self) -> Level:
        """
        Returns the level of the logger.

        :return: The level of the logger.
        :rtype: Level
        """

        # Return the level of the logger
        return self._level

    @level.setter
    def level(
        self,
        value: Level,
    ) -> None:
        """
        Sets the level of the logger.

        :param value: The level to set.
        :type value: Level

        :return: None
        :rtype: None
        """

        # Set the level of the logger
        self._level = value

    @property
    def name(self) -> str:
        """
        Returns the name of the logger.

        :return: The name of the logger.
        :rtype: str
        """

        # Return the name of the logger
        return self._name

    @name.setter
    def name(
        self,
        value: str,
    ) -> None:
        """
        Sets the name of the logger.

        :param value: The name to set.
        :type value: str

        :return: None
        :rtype: None
        """

        # Set the name of the logger
        self._name = value

    def critical(
        self,
        message: Any,
        *args,
        **kwargs,
    ) -> None:
        """
        Logs a message with the CRITICAL level.

        :param message: The message to log.
        :type message: Any

        :param args: Additional positional arguments.
        :type args: tuple

        :param kwargs: Additional keyword arguments.
        :type kwargs: dict

        :return: None
        :rtype: None
        """

        # Log the message with the CRITICAL level
        self.log(
            message=message,
            level=Level.CRITICAL,
            *args,
            **kwargs,
        )

    def debug(
        self,
        message: Any,
        *args,
        **kwargs,
    ) -> None:
        """
        Logs a message with the DEBUG level.

        :param message: The message to log.
        :type message: Any

        :param args: Additional positional arguments.
        :type args: tuple

        :param kwargs: Additional keyword arguments.
        :type kwargs: dict

        :return: None
        :rtype: None
        """

        # Log the message with the DEBUG level
        self.log(
            message=message,
            level=Level.DEBUG,
            *args,
            **kwargs,
        )

    def error(
        self,
        message: Any,
        *args,
        **kwargs,
    ) -> None:
        """
        Logs a message with the ERROR level.

        :param message: The message to log.
        :type message: Any

        :param args: Additional positional arguments.
        :type args: tuple

        :param kwargs: Additional keyword arguments.
        :type kwargs: Dict[str, Any]

        :return: None
        :rtype: None
        """

        # Log the message
        self.log(
            message=message,
            level=Level.ERROR,
            *args,
            **kwargs,
        )

    @classmethod
    def get_logger(
        cls,
        name: str,
        level=Level.INFO,
    ) -> "Logger":
        """
        Returns a logger instance with the given name and level (Defaults to INFO).

        :param name: The name of the logger.
        :type name: str

        :param level: The level of the logger.
        :type level: Level

        :return: A logger instance.
        :rtype: Logger
        """

        # Return a new logger instance with the given name and level
        return cls(
            level=level,
            name=name,
        )

    def info(
        self,
        message: Any,
        *args,
        **kwargs,
    ) -> None:
        """
        Logs a message with the INFO level.

        :param message: The message to log.
        :type message: Any

        :param args: Additional positional arguments.
        :type args: tuple

        :param kwargs: Additional keyword arguments.
        :type kwargs: Dict[str, Any]

        :return: None
        :rtype: None
        """

        # Log the message with the INFO level
        self.log(
            message=message,
            level=Level.INFO,
            *args,
            **kwargs,
        )

    def log(
        self,
        message: Any,
        level=Level.INFO,
        *args,
        **kwargs,
    ) -> None:
        """
        Logs a message with the given level (Defaults to INFO).

        Colorises the message based on the level:
        - Red for CRITICAL
        - Blue for DEBUG
        - Yellow for ERROR
        - Green for INFO
        - Grey for SILENT
        - Magenta for WARNING

        :param message: The message to log.
        :type message: Any

        :param level: The level of the message.
        :type level: Level

        :param args: Additional positional arguments.
        :type args: tuple

        :param kwargs: Additional keyword arguments.
        :type kwargs: dict

        :return: None
        :rtype: None
        """

        # Print the message to the console
        print(
            f"{self.__COLORISATION__[level.name]}[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] - [{level.name}] - [{self.name}] - {message}{", ".join(args) if args else ""}{", ".join([f"{key}={value}" for key, value, in kwargs.items()]) if kwargs else ""}{self.__COLORISATION__["RESET"]}"
        )

    def silent(
        self,
        message: Any,
        *args,
        **kwargs,
    ) -> None:
        """
        Logs a message with the SILENT level.

        The SILENT level is a custom level that is visible in the console as grey text.

        :param message: The message to log.
        :type message: Any

        :param args: Additional positional arguments.
        :type args: tuple

        :param kwargs: Additional keyword arguments.
        :type kwargs: dict

        :return: None
        :rtype: None
        """

        # Log the message with the SILENT level
        self.log(
            message=message,
            level=Level.SILENT,
            *args,
            **kwargs,
        )

    def warning(
        self,
        message: Any,
        *args,
        **kwargs,
    ) -> None:
        """
        Logs a message with the WARNING level.

        The WARNING level is a custom level that is visible in the console as yellow text.

        :param message: The message to log.
        :type message: Any

        :param args: Additional positional arguments.
        :type args: tuple

        :param kwargs: Additional keyword arguments.
        :type kwargs: dict

        :return: None
        :rtype: None
        """

        # Log the message with the WARNING level
        self.log(
            message=message,
            level=Level.WARNING,
            *args,
            **kwargs,
        )
