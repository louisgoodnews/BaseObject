"""
Author: lodego
Date: 2025-02-06
"""

from typing import *

from core.object import ImmutableBaseObject


__all__: List[str] = ["BaseObjectBuilder"]


class BaseObjectBuilder(ImmutableBaseObject):
    """
    A base class for builder classes that build an object using keyword arguments.

    This class is immutable and can be used as a base class for all builder classes.

    Attributes:
        configuration (Dict[str, Any]): The configuration dictionary for the builder.
    """

    def __init__(self) -> None:
        """
        Initializes a new instance of the BaseObjectBuilder class.

        Args:
            None

        Returns:
            None
        """

        # Call the parent class constructor
        super().__init__(configuration={})

    def build(self) -> Any:
        """
        A placeholder method for building an instance of the subclass.

        This method must be implemented by the subclass. It will raise a NotImplementedError if called.

        Args:
            None

        Returns:
            Any: An instance of the subclass.
        """
        raise NotImplementedError(
            f"Subclass '{self.__class__.__name__}' must implement the 'build' method."
        )

    def kwargs(
        self,
        **kwargs,
    ) -> None:
        """
        Updates the configuration dictionary with the given keyword arguments.

        Args:
            kwargs (Dict[str, Any]): The keyword arguments to be updated.

        Returns:
            None
        """

        # Update the configuration dictionary with the given keyword arguments
        self.configuration.update(kwargs)
