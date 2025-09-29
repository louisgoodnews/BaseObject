"""
Author: Louis Goodnews
Date: 2025-08-20
"""

from typing import Final, List, Literal

from .core.core import (
    ImmutableBaseObject,
    MutableBaseObject,
)


__all__: Final[List[str]] = [
    "ImmutableBaseObject",
    "MutableBaseObject",
]

__version__: Final[Literal["0.1.0"]] = "0.1.0"
