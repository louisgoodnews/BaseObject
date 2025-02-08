"""
Author: lodego
Date: 2024-01-24
"""

from datetime import datetime, timedelta

from typing import *

from utils.logger import Logger


__all__: List[str] = ["BaseObjectManager"]


class BaseObjectManager:
    """
    A class for managing BaseObject instances.

    This class serves as a base class for manager classes that manage object instances.
    This class comes with a rudimentary cache system.

    Attributes:
        logger (Logger): The logger instance associated with the object.
        cache (List[Dict[str, Any]]): The cache for storing objects.
        timestamp (datetime): The timestamp of the last update.
        time_limit (int): The time limit for the cache.
    """

    def __init__(
        self,
        **kwargs,
    ) -> None:
        """
        Initializes a new instance of the BaseObjectManager class.

        :param kwargs: keyword arguments
        :type kwargs: dict

        :return: None
        :rtype: None
        """

        # Get an instance of the logger class and store it in the object
        self.logger = Logger.get_logger(name=self.__class__.__name__)

        # Initialize the cache as an empty list
        self._cache: List[Dict[str, Any]] = []

        # Store the time limit in an instance variable
        self._time_limit: int = 3600

        # Store the timestamp in an instance variable
        self._timestamp: datetime = datetime.now()

    @property
    def cache(self) -> List[Dict[str, Any]]:
        """
        Returns the cache.

        :return: The cache.
        :rtype: List[Dict[str, Any]]
        """

        # Return the cache
        return self._cache

    @property
    def time_limit(self) -> int:
        """
        Returns the time limit for the cache.

        :return: The time limit for the cache.
        :rtype: int
        """

        # Return the time limit
        return self._time_limit

    @time_limit.setter
    def time_limit(
        self,
        value: int,
    ) -> None:
        """
        Sets the time limit for the cache.

        :param value: The time limit to set.
        :type value: int

        :return: None
        :rtype: None
        """

        # Set the time limit
        self._time_limit = value

    def add_to_cache(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Adds an item to the cache.

        :param key: The key of the item.
        :type key: str

        :param value: The value of the item.
        :type value: Any

        :return: None
        :rtype: None
        """

        # Flush the cache, if needed
        self.flush_cache()

        # Check if the key already exists
        if key in [item["key"] for item in self._cache]:
            # Log a warning message
            self.logger.warning(message=f"Key '{key}' already exists. Overwriting...")

        # Add the key-value pair to the cache
        self._cache.append(
            {
                "key": key,
                "value": value,
            }
        )

        # Log the addition to the cache
        self.logger.info(message=f"Added to cache: {key}")

    def check_timestamp(self) -> bool:
        """
        Checks if the cache needs to be cleared.

        :return: True if the cache needs to be cleared, False otherwise.
        :rtype: bool
        """

        # Return True if the cache needs to be cleared, False otherwise
        return datetime.now() - self._timestamp >= timedelta(seconds=self._time_limit)

    def clear_cache(self) -> None:
        """
        Clears the cache and resets the timestamp.

        :return: None
        :rtype: None
        """

        # Clear the cache
        self.cache.clear()

        # Log the clear
        self.logger.info(message="Cache cleared.")

        # Update the timestamp
        self._timestamp = datetime.now()

    def flush_cache(
        self,
        force: bool = False,
    ) -> None:
        """
        Checks if the cache is valid and flushes if it is not.

        Otherwise if force is True it will flush the cache no matter what.

        :param force: Whether to flush the cache no matter what.
        :type force: bool

        :return: None
        :rtype: None
        """

        # Check if the cache is valid
        if not self.check_timestamp() or force:
            # Flush the cache
            self.cache.clear()

            # Update the timestamp
            self._timestamp = datetime.now()

            # Log updating the timestamp
            self.logger.info(message="Updated the timestamp to now.")

    def get_cache_keys(self) -> List[str]:
        """
        Returns the keys of the cache.

        :return: The keys of the cache.
        :rtype: List[str]
        """

        # Return the keys of the cache
        return [item["key"] for item in self._cache]

    def get_cache_values(self) -> List[Any]:
        """
        Returns the values of the cache.

        :return: The values of the cache.
        :rtype: List[Any]
        """

        # Return the values of the cache
        return [item["value"] for item in self._cache]

    def get_key_from_cache(
        self,
        value: Any,
    ) -> str:
        """
        Returns the key of the item with the given value from the cache.

        :param value: The value of the item.
        :type value: Any

        :return: The key of the item with the given value.
        :rtype: str
        """

        # Return the key of the item with the given value
        return [item["key"] for item in self._cache][
            [item["value"] for item in self._cache].index(value)
        ]

    def get_value_from_cache(
        self,
        key: str,
    ) -> Any:
        """
        Returns the value of the item with the given key from the cache.

        :param key: The key of the item.
        :type key: str

        :return: The value of the item with the given key.
        :rtype: Any
        """

        # Check if the key exists
        if key not in [item["key"] for item in self._cache]:
            # Log a warning message
            self.logger.warning(
                message=f"Key '{key}' does not exist. Returning None..."
            )

            # Return early since the key does not exist
            return

        # Return the value of the key
        return self._cache[[item["key"] for item in self._cache].index(key)]["value"]

    def is_cache_empty(self) -> bool:
        """
        Checks if the cache is empty.

        :return: True if the cache is empty, False otherwise.
        :rtype: bool
        """

        # Return True if the cache is empty, False otherwise
        return len(self._cache) == 0

    def is_cache_valid(self) -> bool:
        """
        Checks if the cache is valid.

        The cache is valid if the timestamp is less than the time limit and the cache is not empty.

        :return: True if the cache is valid, False otherwise.
        :rtype: bool
        """

        # Return True if the cache is valid, False otherwise
        return self.check_timestamp() and not self.is_cache_empty()

    def is_key_in_cache(
        self,
        key: str,
    ) -> bool:
        """
        Checks if a key exists in the cache.

        :param key: The key to check.
        :type key: str

        :return: True if the key exists, False otherwise.
        :rtype: bool
        """

        # Return True if the key exists, False otherwise
        return key in [item["key"] for item in self._cache]

    def is_value_in_cache(
        self,
        value: Any,
    ) -> bool:
        """
        Checks if a value exists in the cache.

        :param value: The value to check.
        :type value: Any

        :return: True if the value exists, False otherwise.
        :rtype: bool
        """

        # Return True if the value exists, False otherwise
        return value in [item["value"] for item in self._cache]

    def update_in_cache(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Updates the value of the item with the given key in the cache.

        :param key: The key of the item.
        :type key: str

        :param value: The new value of the item.
        :type value: Any

        :return: None
        :rtype: None

        :raises KeyError: If the key does not exist.
        """

        # Update the value of the item with the given key in the cache
        for item in self._cache:
            # Check if the key matches
            if item["key"] == key:
                # Update the value of the item
                item["value"] = value

                # Log an info message about the update
                self.logger.info(message=f"Updated in cache: {key}")

                # Return early since the key was found
                break
            else:
                # Raise a KeyError if the key was not found
                raise KeyError("Key not found")
