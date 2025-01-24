"""
Author: lodego
Date: 2024-01-24
"""

from core.base.manager import *
from core.base.object import *

from utils.logger.logger import Logger


def main() -> None:
    # Get an instance of the logger class and store it in a variable
    logger: Logger = Logger.get_logger(name="main")

    # Log some messages in the console
    logger.critical(message="This is a critical message.")
    logger.debug(message="This is a debug message.")
    logger.error(message="This is an error message.")
    logger.info(message="This is an info message.")
    logger.silent(message="This is a silent message.")
    logger.warning(message="This is a warning message.")

    # Create a MutableBaseObject named "Steve"
    mutable: MutableBaseObject = MutableBaseObject(**{"name": "Steve"})

    # Change the name of the MutableBaseObject to "Jimmy"
    mutable.name = "Jimmy"

    # Print the name of the MutableBaseObject
    print(mutable.name)

    # Create an ImmutableBaseObject named "John"
    immutable: ImmutableBaseObject = ImmutableBaseObject(**{"name": "John"})

    try:
        # Try to change the name of the ImmutableBaseObject to "Karl"
        immutable.name = "Karl"
    except Exception as e:
        # Print the error message
        print(e)

    # Try to change the name of the ImmutableBaseObject to "Jimmy"
    print(immutable.name)

    # Create a BaseObjectManager and store it in a variable
    manager: BaseObjectManager = BaseObjectManager()

    # Print the manager
    print(manager)


if __name__ == "__main__":
    main()
