"""
Author: Louis Goodnews
Date: 2025-08-20
"""

import copy
import json

from collections.abc import ItemsView, KeysView, ValuesView
from typing import (
    Any,
    Final,
    Iterator,
    Literal,
    Optional,
    override,
    Type,
    Union,
)


class MutableBaseObject:
    """
    A class representing a mutable base object.
    """

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the base object.

        This method iterates over the key-value pairs in the kwargs dictionary
        and sets the attributes on the object.

        :param kwargs: A dictionary of key-value pairs to set as attributes on the object.
        :type kwargs: dict[str, Any]

        :return: None
        :rtype: None
        """

        # Get the annotations of the object
        annotations: dict[str, Any] = getattr(
            self,
            "__annotations__",
            {},
        )

        def set_attr(
            name: str,
            value: Any,
            expected_type: Any,
        ) -> None:
            """
            Helper to set an attribute with type check and property creation.

            :param name: The name of the attribute to set.
            :type name: str
            :param value: The value to set the attribute to.
            :type value: Any
            :param expected_type: The expected type of the attribute.
            :type expected_type: Any

            :return: None
            :rtype: None
            """

            # Check if the value is not None and the expected type is not None and the value is not of the expected type
            if (
                value is not None
                and expected_type is not None
                and not isinstance(
                    value,
                    expected_type,
                )
            ):
                # Attempt to cast the value to the expected type
                try:
                    value = expected_type(value)
                except Exception:
                    # Raise a TypeError if the value is not of the expected type
                    raise TypeError(
                        f"Invalid type for field '{name}': expected {expected_type}, got {type(value)}"
                    )

            # Set the attribute on the object
            setattr(
                self,
                f"_{name}",
                value,
            )

            # Check if the property exists on the class
            if not hasattr(
                self.__class__,
                name,
            ):
                # Create the property
                self._create_property(name)

        # Check if the annotations are not empty
        if annotations:
            # Annotated attributes
            for (
                name,
                type_,
            ) in annotations.items():
                # Set the attribute on the object
                set_attr(
                    name,
                    kwargs.get(
                        name,
                        None,
                    ),
                    type_,
                )

            # Unexpected arguments
            for extra in set(
                kwargs.keys(),
            ) - set(
                annotations.keys(),
            ):
                # Raise a TypeError if the argument is unexpected
                raise TypeError(
                    f"Unexpected argument: '{extra}'",
                )
        else:
            # Non-annotated attributes
            for (
                name,
                value,
            ) in kwargs.items():
                # Set the attribute on the object
                set_attr(
                    name,
                    value,
                    None,
                )

        # Call __post_init__ if it exists
        if hasattr(self, "__post_init__"):
            self.__post_init__()

    def __add__(
        self,
        other: "MutableBaseObject",
    ) -> "MutableBaseObject":
        """
        Add two objects together.

        :param other: The other object to add to this object.
        :type other: MutableBaseObject

        :return: A new object created by adding the attributes of this object and the other object.
        :rtype: MutableBaseObject
        """

        # Check if the other object is an instance of the same class
        if not isinstance(
            other,
            self.__class__,
        ):
            # Return NotImplemented if the other object is not an instance of the same class
            return NotImplemented

        # Return a new object created by adding the attributes of this object and the other object
        return self.__class__(**dict(vars(self)) | dict(vars(other)))

    def __contains__(
        self,
        item: Any,
    ) -> bool:
        """
        Check if the object contains an attribute.

        :param item: The item to check.
        :type item: Any

        :return: True if the item exists on the object, False otherwise.
        :rtype: bool
        """

        # Check if the item exists on the object
        return item in vars(self).keys() or item in vars(self).values()

    def __copy__(self) -> "MutableBaseObject":
        """
        Return a copy of the object.

        :return: A copy of the object.
        :rtype: MutableBaseObject
        """

        attributes: dict[str, Any] = {
            key.lstrip("_"): value for key, value in vars(self).items() if not key.startswith("_")
        }

        # Return a copy of the object
        return self.__class__(**attributes)

    def __delitem__(
        self,
        key: str,
    ) -> None:
        """
        Delete an attribute from the object.

        :param key: The name of the attribute to delete.
        :type key: str

        :return: None
        :rtype: None
        """

        # Check if the attribute exists on the object
        if not hasattr(
            self,
            key,
        ):
            # Raise a KeyError if the attribute does not exist
            raise KeyError(
                f"{key!r} not found in {self.__class__.__name__}",
            )

        # Delete the attribute from the object
        delattr(
            self,
            key,
        )

    def __eq__(
        self,
        other: "MutableBaseObject",
    ) -> bool:
        """
        Check if the object is equal to another object.

        :param other: The object to compare to.
        :type other: MutableBaseObject

        :return: True if the objects are equal, False otherwise.
        :rtype: bool
        """

        # Check if the objects are equal
        return dict(vars(self)) == dict(vars(other))

    def __getitem__(
        self,
        key: str,
    ) -> Any:
        """
        Get an attribute from the object.

        :param key: The name of the attribute to get.
        :type key: str

        :return: The value of the attribute or None if the attribute does not exist.
        :rtype: Any
        """

        # Check if the attribute exists on the object
        if not hasattr(
            self,
            key,
        ):
            # Raise a KeyError if the attribute does not exist
            raise KeyError(
                f"{key!r} not found in {self.__class__.__name__}",
            )

        # Return the attribute from the object
        return getattr(
            self,
            key,
        )

    def __gt__(
        self,
        other: "MutableBaseObject",
    ) -> bool:
        """
        Check if the object is greater than another object.

        :param other: The object to compare to.
        :type other: MutableBaseObject

        :return: True if the object is greater than the other object, False otherwise.
        :rtype: bool
        """

        # Check if the object is greater than the other object
        return dict(vars(self)) > dict(vars(other))

    def __iter__(self) -> Iterator[tuple[str, Any]]:
        """
        Iterate over the attributes of the object.

        :return: An iterator over the attributes of the object.
        :rtype: Iterator[tuple[str, Any]]
        """

        # Iterate over the attributes of the object
        return iter(vars(self).items())

    def __len__(self) -> int:
        """
        Return the number of attributes on the object.

        :return: The number of attributes on the object.
        :rtype: int
        """

        # Return the number of attributes on the object
        return len(vars(self))

    def __lt__(
        self,
        other: "MutableBaseObject",
    ) -> bool:
        """
        Check if the object is less than another object.

        :param other: The object to compare to.
        :type other: MutableBaseObject

        :return: True if the object is less than the other object, False otherwise.
        :rtype: bool
        """

        # Check if the object is less than the other object
        return dict(vars(self)) < dict(vars(other))

    def __repr__(self) -> str:
        """
        Return a string representation of the object.

        :return: A string representation of the object.
        :rtype: str
        """

        # Return a string representation of the object
        return f"<{self.__class__.__name__} ({', '.join(f'{key}={value!r}' for (key, value,) in dict(vars(self)).items())})>"

    def __setitem__(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Set an attribute on the object.

        :param key: The name of the attribute to set.
        :type key: str
        :param value: The value to set the attribute to.
        :type value: Any

        :return: None
        :rtype: None
        """

        # Set the attribute on the object
        setattr(
            self,
            key,
            value,
        )

    def __str__(self) -> str:
        """
        Return a string representation of the object.

        :return: A string representation of the object.
        :rtype: str
        """

        # Return a string representation of the object
        return self.__repr__()

    def __subtract__(
        self,
        other: "MutableBaseObject",
    ) -> "MutableBaseObject":
        """
        Subtract another object from this object.

        :param other: The object to subtract from this object.
        :type other: MutableBaseObject

        :return: A new object created by subtracting the other object from this object.
        :rtype: MutableBaseObject
        """

        # Return a new object created by subtracting the other object from this object
        return self.__class__(
            **{k: v for k, v in vars(self).items() if k not in vars(other)},
        )

    @classmethod
    def _create_property(
        cls,
        name: str,
    ) -> None:
        """
        Dynamically create property and setter for a field.

        :param name: The name of the field to create a property for.
        :type name: str

        :return: None
        :rtype: None
        """

        def getter(self) -> Any:
            """
            Get the value of the field.

            :return: The value of the field.
            :rtype: Any
            """

            return getattr(self, f"_{name}")

        def setter(
            self,
            value: Any,
        ) -> None:
            """
            Set the value of the field.

            :param value: The value to set the field to.
            :type value: Any

            :return: None
            :rtype: None
            """

            setattr(self, f"_{name}", value)

        # Set the property on the class
        setattr(
            cls,
            name,
            property(
                getter,
                setter,
            ),
        )

    def copy(self) -> "MutableBaseObject":
        """
        Return a copy of the object.

        :return: A copy of the object.
        :rtype: MutableBaseObject
        """

        attributes: dict[str, Any] = {
            key.lstrip("_"): value for key, value in vars(self).items() if not key.startswith("_")
        }

        # Return a copy of the object
        return self.__class__(
            **attributes,
        )

    def deep_copy(
        self,
        as_mutable: bool = False,
    ) -> Union["MutableBaseObject", "ImmutableBaseObject"]:
        """
        Return a deep copy of the object, optionally as mutable.

        :param as_mutable: If True, returns a mutable copy. Defaults to False.
        :type as_mutable: bool

        :return: A deep copy of the object.
        :rtype: MutableBaseObject or ImmutableBaseObject
        """

        def _deep_copy_value(value) -> Any:
            """
            Recursively copy a value.

            :param value: The value to copy.
            :type value: Any

            :return: A deep copy of the value.
            :rtype: Any
            """

            # Check if the value is an ImmutableBaseObject or MutableBaseObject
            if isinstance(
                value,
                (
                    MutableBaseObject,
                    ImmutableBaseObject,
                ),
            ):
                # Return a deep copy of the value
                return value.deep_copy(as_mutable=as_mutable)
            elif isinstance(
                value,
                dict,
            ):
                # Return a deep copy of the value
                return {k: _deep_copy_value(v) for k, v in value.items()}
            elif isinstance(
                value,
                list,
            ):
                # Return a deep copy of the value
                return [_deep_copy_value(v) for v in value]
            elif isinstance(
                value,
                set,
            ):
                # Return a deep copy of the value
                return {_deep_copy_value(v) for v in value}
            elif isinstance(
                value,
                tuple,
            ):
                # Return a deep copy of the value
                return tuple(_deep_copy_value(v) for v in value)
            else:
                # Return a deep copy of the value
                return copy.deepcopy(value)

        # Copy all attributes of the object recursively
        copied_attributes: dict[str, Any] = {
            key.lstrip("_"): _deep_copy_value(value)
            for (
                key,
                value,
            ) in vars(self).items()
            if key.startswith("_") and key != "_locked_"
        }

        # Check if the object should be mutable
        if as_mutable:
            # Return a mutable copy of the object
            return MutableBaseObject(**copied_attributes)

        # Return an immutable copy of the object
        return self.__class__(**copied_attributes)

    def enumerate(self) -> list[tuple[int, tuple[str, Any]]]:
        """
        Return a list of attribute names and values on the object with their index.

        :return: A list of attribute names and values on the object with their index.
        :rtype: list[tuple[int, tuple[str, Any]]]
        """

        # Return a list of attribute names and values on the object with their index
        return list(enumerate(iterable=vars(self).items()))

    def equals(
        self,
        other: "MutableBaseObject",
        keys: Optional[list[str]] = None,
    ) -> bool:
        """
        Check if the object is equal to another object.

        :param other: The object to compare to.
        :type other: MutableBaseObject
        :param keys: A list of attribute names to compare.
        :type keys: Optional[list[str]]

        :return: True if the objects are equal, False otherwise.
        :rtype: bool
        """

        # Check if the objects are equal
        if keys is None:
            return vars(self) == vars(other)

        return all(
            [
                (
                    getattr(
                        self,
                        key,
                        None,
                    )
                    == getattr(
                        other,
                        key,
                        None,
                    )
                )
                for key in keys
            ],
        )

    def filter_by_type(
        self,
        type_: Type[Any],
    ) -> dict[str, Any]:
        """
        Return attributes of a specific type.

        :param type_: The type to filter attributes by.
        :type type_: Type[Any]

        :return: dictionary of attribute names and values matching the type.
        :rtype: dict[str, Any]
        """

        # Return a dictionary of attribute names and values matching the type
        return {k: v for k, v in vars(self).items() if isinstance(v, type_)}

    @classmethod
    def from_dict(
        cls,
        **kwargs,
    ) -> "MutableBaseObject":
        """
        Create a new object from a dictionary.

        :param kwargs: A dictionary of key-value pairs to set as attributes on the object.
        :type kwargs: dict[str, Any]

        :return: A new object created from the dictionary.
        :rtype: MutableBaseObject
        """

        attributes: dict[str, Any] = {
            key.lstrip("_"): value for key, value in kwargs.items() if not key.startswith("_")
        }

        # Return a new object created from the dictionary
        return cls(**attributes)

    @classmethod
    def from_json(
        cls,
        string: str,
    ) -> "MutableBaseObject":
        """
        Create a new object from a JSON string.

        :param string: A JSON string to create an object from.
        :type string: str

        :return: A new object created from the JSON string.
        :rtype: MutableBaseObject
        """

        # Return a new object created from the JSON string
        return cls.from_dict(
            **json.loads(string),
        )

    def get(
        self,
        key: str,
        default: Optional[Any] = None,
    ) -> Optional[Any]:
        """
        Get an attribute from the object.

        :param key: The name of the attribute to get.
        :type key: str
        :param default: The default value to return if the attribute does not exist.
        :type default: Optional[Any]

        :return: The value of the attribute or the default value if the attribute does not exist.
        :rtype: Optional[Any]
        """

        # Check if the attribute exists on the object
        if not hasattr(
            self,
            key,
        ):
            # Return the default value
            return default

        # Return the attribute from the object
        return getattr(
            self,
            key,
        )

    def get_or_default(
        self,
        key: str,
        default: Any,
    ) -> Any:
        """
        Get the value of an attribute, or return a default if it doesn't exist.

        :param key: Attribute name.
        :type key: str
        :param default: Default value if attribute is missing.
        :type default: Any

        :return: Value of the attribute or default.
        :rtype: Any
        """

        # Return the attribute from the object or the default value
        return getattr(
            self,
            key,
            default,
        )

    def has(
        self,
        key: Optional[str] = None,
        value: Optional[Any] = None,
    ) -> bool:
        """
        Check if the object has an attribute with the given name and value.

        :param key: The name of the attribute to check.
        :type key: Optional[str]
        :param value: The value of the attribute to check.
        :type value: Optional[Any]

        :return: True if the object has the attribute with the given name and value, False otherwise.
        :rtype: bool
        """

        # Add the underscore prefix to the key if it doesn't start with it
        if key is not None and not key.startswith("_"):
            # Add the underscore prefix to the key
            key = f"_{key}"

        # Get the dictionary of attributes
        attributes: dict[str, Any] = vars(self)

        # Check if both a key and value were passed
        if key is not None and value is not None:
            # Return True if the object has any matching attributes
            return key in attributes.keys() and value in attributes.values()

        # Check if a key was passed
        if key is not None:
            # Return True if the object has the attribute with the given name
            return key in attributes

        # Check if a value was passed
        if value is not None:
            # Return True if the object has the attribute with the given value
            return value in attributes.values()

        # Return False
        return False

    def items(self) -> ItemsView[str, Any]:
        """
        Return a list of attribute names and values on the object.

        :return: A list of attribute names and values on the object.
        :rtype: ItemsView[str, Any]
        """

        # Return a list of attribute names and values on the object
        return vars(self).items()

    def keys(self) -> KeysView[str]:
        """
        Return a list of attribute names on the object.

        :return: A list of attribute names on the object.
        :rtype: KeysView[str]
        """

        # Return a list of attribute names on the object
        return vars(self).keys()

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Set an attribute on the object.

        :param key: The name of the attribute to set.
        :type key: str
        :param value: The value to set the attribute to.
        :type value: Any

        :return: None
        :rtype: None
        """

        # Set the attribute on the object
        setattr(
            self,
            key,
            value,
        )

    def to_dict(
        self,
        allow_leading_underscores: bool = False,
        exclude: Optional[list[str]] = None,
        sort: Optional[Literal["ascending", "descending"]] = None,
    ) -> dict[str, Any]:
        """
        Convert the object to a dictionary.

        :param exclude: A list of attribute names to exclude from the dictionary.
        :type exclude: Optional[list[str]]
        :param sort: The sort order for the dictionary.
        :type sort: Optional[Literal["ascending", "descending"]]

        :return: A dictionary representation of the object.
        :rtype: dict[str, Any]
        """

        # Get the dictionary of attributes
        dictionary: dict[str, Any] = {
            key: value
            for (
                key,
                value,
            ) in sorted(
                dict(vars(self)).items(),
                reverse=sort == "ascending",
            )
        }

        # Check if keys with leading underscores are allowed
        if not allow_leading_underscores:
            # Update the dictionary to remove all keys with a underscore prefix
            dictionary = {
                key: value
                for (
                    key,
                    value,
                ) in dictionary.items()
                if not key.startswith("_")
            }

        # Check if an exclude list is provided
        if not exclude:
            # Return the full dictionary
            return dictionary

        # Iterate over the exclude list
        for key in exclude:
            # Remove the key from the dictionary
            dictionary.pop(
                key,
                None,
            )

        # Return the dictionary
        return dictionary

    def to_filtered_dict(
        self,
        keys: Optional[list[str]] = None,
        typ: Optional[type] = None,
    ) -> dict[str, Any]:
        """
        Return attributes as a dict, optionally filtered by keys or type.

        :param keys: Optional list of keys to include.
        :type keys: Optional[list[str]]
        :param typ: Optional type to filter attributes by.
        :type typ: Optional[type]

        :return: A dictionary of attributes.
        :rtype: dict[str, Any]
        """

        # Get the dictionary of attributes
        dictionary: dict[str, Any] = dict(vars(self))

        # Check if the keys parameter is provided
        if keys:
            # Filter the dictionary by keys
            dictionary = {k: v for k, v in dictionary.items() if k in keys}

        # Check if the type parameter is provided
        if typ:
            # Filter the dictionary by type
            dictionary = {k: v for k, v in dictionary.items() if isinstance(v, typ)}

        # Return the dictionary
        return dictionary

    def to_json(
        self,
        exclude: Optional[list[str]] = None,
        sort_keys: bool = False,
    ) -> str:
        """
        Convert the object to a JSON string.

        :param exclude: A list of attribute names to exclude from the JSON string.
        :type exclude: Optional[list[str]]
        :param sort_keys: Whether to sort the keys in the JSON string.
        :type sort_keys: bool

        :return: A JSON string representation of the object.
        :rtype: str
        """

        # Get the dictionary of attributes
        dictionary: dict[str, Any] = dict(vars(self))

        # Check if an exclude list is provided
        if not exclude:
            # Return the full dictionary
            return json.dumps(
                dictionary,
                sort_keys=sort_keys,
            )

        # Iterate over the exclude list
        for key in exclude:
            # Remove the key from the dictionary
            dictionary.pop(
                key,
                None,
            )

        # Return the dictionary
        return json.dumps(
            dictionary,
            sort_keys=sort_keys,
        )

    def update(
        self,
        **kwargs: Any,
    ) -> None:
        """
        Update the object with key-value pairs.

        :param kwargs: A dictionary of key-value pairs to update the object with.
        :type kwargs: dict[str, Any]

        :return: None
        :rtype: None
        """

        # Iterate over the key-value pairs in the kwargs dictionary
        for (
            name,
            value,
        ) in kwargs.items():
            # Set the attribute on the object
            setattr(
                self,
                name,
                value,
            )

    def update_defaults(
        self,
        **defaults: Any,
    ) -> None:
        """
        Update only attributes that are not yet set.

        :param defaults: Key-value pairs to update as defaults.
        :type defaults: dict[str, Any]

        :return: None
        :rtype: None
        """

        # Iterate over the key-value pairs in the defaults dictionary
        for (
            key,
            value,
        ) in defaults.items():
            # Check if the attribute is not yet set
            if hasattr(
                self,
                key,
            ):
                # Skip the attribute
                continue

            # Set the attribute on the object
            setattr(
                self,
                key,
                value,
            )

    def values(self) -> ValuesView[Any]:
        """
        Return a list of attribute values on the object.

        :return: A list of attribute values on the object.
        :rtype: ValuesView[Any]
        """

        # Return a list of attribute values on the object
        return vars(self).values()


class ImmutableBaseObject(MutableBaseObject):
    """
    A class representing an immutable base object.
    """

    def __init__(
        self,
        **kwargs: Any,
    ) -> None:
        """
        Initialize the base object.

        This method calls the parent class constructor to initialize the base object.

        :param kwargs: A dictionary of key-value pairs to set as attributes on the object.
        :type kwargs: dict[str, Any]

        :return: None
        :rtype: None
        """

        # Call the parent class constructor
        super().__init__(
            **kwargs,
        )

        # Initialize the lock dictionary instance variable
        self._locked_: Final[dict[str, bool]] = {}

        # Iterate over the keys of the kwargs dictionary
        for key in kwargs.keys():
            # Lock the attribute
            self._locked_[key] = True

    @override
    def __copy__(
        self,
        as_mutable: bool = False,
    ) -> Union["MutableBaseObject", "ImmutableBaseObject"]:
        """
        Return a shallow copy of the object.

        :param as_mutable: If True, returns a mutable copy. Defaults to False.
        :type as_mutable: bool

        :return: A shallow copy of the object.
        :rtype: MutableBaseObject or ImmutableBaseObject
        """

        # Get the attributes of the object
        attributes: dict[str, Any] = {
            key.lstrip("_"): value
            for (
                key,
                value,
            ) in vars(self).items()
            if not key.startswith("_")
        }

        # Check if the object should be mutable
        if as_mutable:
            # Return a mutable copy of the object
            return MutableBaseObject(**attributes)
        else:
            # Return an immutable copy of the object
            return self.__class__(**attributes)

    @override
    def __delattr__(
        self,
        name: str,
    ) -> None:
        """
        Delete an attribute from the object.

        :param name: The name of the attribute to delete.
        :type name: str

        :return: None
        :rtype: None

        Raises:
            AttributeError: If the object is immutable.
            AttributeError: If the attribute is locked.
        """

        # Check if the instance is locked
        self._check_locked(name=name)

        # Delete the attribute from the object
        super().__delattr__(
            name,
        )

        # Check, if the passed attribute is locked
        if name in self._locked_:
            # Release the attribute
            self._locked_.pop(name)

    @override
    def __delitem__(
        self,
        key: str,
    ) -> None:
        """
        Delete an attribute from the object.

        :param key: The name of the attribute to delete.
        :type key: str

        :return: None
        :rtype: None

        Raises:
            AttributeError: If the object is immutable.
            AttributeError: If the attribute is locked.
        """

        # Check if the instance is locked
        self._check_locked(name=key)

        # Delete the attribute from the object
        super().__delitem__(
            key,
        )

        # Check, if the passed attribute is locked
        if key in self._locked_:
            # Release the attribute
            self._locked_.pop(key)

    @override
    def __setattr__(
        self,
        name: str,
        value: Any,
    ) -> None:
        """
        Set an attribute on the object.

        :param name: The name of the attribute to set.
        :type name: str
        :param value: The value to set the attribute to.
        :type value: Any

        :return: None
        :rtype: None

        Raises:
            AttributeError: If the object is immutable.
            AttributeError: If the attribute is locked.
        """

        # Check if the instance is locked
        self._check_locked(name=name)

        # Set the attribute on the object
        super().__setattr__(
            name,
            value,
        )

    @override
    def __setitem__(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Set an attribute on the object.

        :param key: The name of the attribute to set.
        :type key: str
        :param value: The value to set the attribute to.
        :type value: Any

        :return: None
        :rtype: None

        Raises:
            AttributeError: If the object is immutable.
            AttributeError: If the attribute is locked.
        """

        # Check if the instance is locked
        self._check_locked(name=key)

        # Set the attribute on the object
        super().__setitem__(
            key,
            value,
        )

    def _check_locked(
        self,
        name: Optional[str] = None,
    ) -> None:
        """
        Raise an AttributeError if the object is locked and the attribute
        name does not start with '_'.

        :param name: Optional field name for error message
        :type name: Optional[str]

        :return: None
        :rtype: None

        Raises:
            AttributeError: If the object is immutable.
            AttributeError: If the attribute is locked.
        """

        # Check, if the passed name is None
        if name is None:
            # Raise an AttributeError if the object is immutable
            raise AttributeError(
                f"Cannot modify immutable object {self.__class__.__name__}",
            )

        # Check, if the passed name starts with '_', i.e. if is private
        if name.startswith("_"):
            # Skip the check
            return

        # Get the locked state
        locked: bool = self._locked_.get(name, False)

        # Check, if the attribute is locked
        if locked:
            # Raise an AttributeError if the attribute is not allowed to be modified
            raise AttributeError(
                f"Cannot modify immutable field '{name}' of object {self.__class__.__name__}",
            )

    @override
    def copy(
        self,
        as_mutable: bool = False,
    ) -> Union["MutableBaseObject", "ImmutableBaseObject"]:
        """
        Return a copy of the object.

        :param as_mutable: If True, returns a mutable copy. Defaults to False.
        :type as_mutable: bool

        :return: A copy of the object.
        :rtype: MutableBaseObject or ImmutableBaseObject
        """

        return self.__copy__(as_mutable)

    def is_locked(
        self,
        name: str,
    ) -> bool:
        """
        Check if an attribute is locked.

        :param name: The name of the attribute to check.
        :type name: str

        :return: True if the attribute is locked, False otherwise.
        :rtype: bool
        """

        return self._locked_.get(
            name,
            False,
        )

    def lock_attribute(
        self,
        name: str,
        allow_new: bool = False,
        value: Optional[Any] = None,
    ) -> None:
        """
        Lock a specific attribute, making it immutable.
        Optionally, enforce a specific value for it.

        :param allow_new: If True, allows to lock a new attribute.
        :type allow_new: bool
        :param name: The name of the attribute to lock.
        :type name: str
        :param value: Optional value to enforce for the attribute.
        :type value: Optional[Any]

        :return: None
        :rtype: None

        Raises:
            KeyError: If the attribute has not been registered.
            AttributeError: If the attribute is private.
            ValueError: If the attribute has not been registered and allow_new is False.
        """

        # Check, if the passed attribute has been registered
        if name not in self._locked_ and not allow_new:
            # Raise a KeyError exception if the attribute has not been registered
            raise KeyError(f"Attribute '{name}' has not been registered")

        # Check, if the attribute is private
        if name.startswith("_"):
            # Raise an AttributeError if the attribute is private
            raise AttributeError(f"Cannot lock private attribute '{name}'")

        # Check if the attribute should be set
        if value is not None:
            # Set the attribute on the object
            super().__setattr__(
                name,
                value,
            )

        # Check, if the attribute should be set
        elif allow_new and not hasattr(
            self,
            name,
        ):
            # Raise a ValueError exception if the attribute has not been registered
            raise ValueError(f"New attribute '{name}' must have a value when locking")

        # Lock the attribute
        self._locked_[name] = True

    @override
    def set(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Set an attribute on the object.

        :param key: The name of the attribute to set.
        :type key: str
        :param value: The value to set the attribute to.
        :type value: Any

        :return: None
        :rtype: None

        Raises:
            AttributeError: If the attribute is private.
        """

        # Check if the instance is locked
        self._check_locked(name=key)

        # Set the attribute on the object
        super().set(
            key,
            value,
        )

    def unlock_attribute(
        self,
        name: str,
    ) -> None:
        """
        Unlock a specific attribute, making it mutable.

        :param name: The name of the attribute to unlock.
        :type name: str

        :return: None
        :rtype: None

        Raises:
            KeyError: If the attribute has not been registered.
            AttributeError: If the attribute is private.
        """

        # Check, if the passed attribute has been registered
        if name not in self._locked_:
            # Raise a KeyError exception if the attribute has not been registered
            raise KeyError(f"Attribute '{name}' has not been registered")

        # Check, if the attribute is private
        if name.startswith("_"):
            # Raise an AttributeError if the attribute is private
            raise AttributeError(f"Cannot unlock private attribute '{name}'")

        # Unlock the attribute
        self._locked_[name] = False

    @override
    def update(
        self,
        **kwargs: Any,
    ) -> None:
        """
        Update the object with key-value pairs.

        :param kwargs: A dictionary of key-value pairs to update the object with.
        :type kwargs: dict[str, Any]

        :return: None
        :rtype: None

        Raises:
            AttributeError: If the attribute is private.
        """

        # Update the lock dictionary
        for key in kwargs.keys():
            # Check if the instance is locked
            self._check_locked(name=key)

        # Update the object with key-value pairs
        super().update(
            **kwargs,
        )

        # Update the lock dictionary
        for key in kwargs.keys():
            # Check, if the attribute is already locked
            if key in self._locked_:
                # Skip the current attribute
                continue

            # Lock the attribute
            self._locked_[key] = True


class BaseObjectBuilder(ImmutableBaseObject):
    """
    Base class for object builders.
    """

    def __init__(self) -> None:
        """
        Initialize the object builder.

        :return: None
        :rtype: None
        """

        # Call the parent class constructor
        super().__init__(**{"configuration": {}})

    @override
    def __contains__(
        self,
        item: Any,
    ) -> bool:
        """
        Check if the object contains an attribute.

        :param item: The item to check.
        :type item: Any

        :return: True if the item exists on the object, False otherwise.
        :rtype: bool
        """

        # Check if the item exists on the object
        return item in self.configuration

    @override
    def __delitem__(
        self,
        key: str,
    ) -> None:
        """
        Delete an attribute from the object.

        :param key: The key of the attribute to delete.
        :type key: str

        :return: None
        :rtype: None

        Raises:
            KeyError: If the attribute does not exist.
        """

        # Delete the attribute from the object
        del self.configuration[key]

    @override
    def __getitem__(
        self,
        key: str,
    ) -> Any:
        """
        Get an attribute from the object.

        :param key: The key of the attribute to get.
        :type key: str

        :return: The value of the attribute.
        :rtype: Any

        Raises:
            KeyError: If the attribute does not exist.
        """

        # Get the attribute from the object
        return self.configuration[key]

    @override
    def __setitem__(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Set an attribute on the object.

        :param key: The key of the attribute to set.
        :type key: str
        :param value: The value to set the attribute to.
        :type value: Any

        :return: None
        :rtype: None

        Raises:
            AttributeError: If the attribute is private.
        """

        # Set the attribute on the object
        self.configuration[key] = value

    @override
    def __str__(
        self,
    ) -> str:
        """
        Return a string representation of the object.

        :return: A string representation of the object.
        :rtype: str
        """

        # Return a string representation of the object
        return str(self.configuration)

    def build(self) -> Any:
        """
        Build the object.

        :return: The built object.
        :rtype: Any
        """

        raise NotImplementedError(f"{self.__class__.__name__}.build() is not implemented yet.")


# ---- Auto-Export -----

# Auto-export all non-rpivate symbols
__all__: Final[list[str]] = [name for name in globals() if not name.startswith("_")]
