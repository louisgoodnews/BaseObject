#!/usr/bin/env python3
"""
BaseObject - A Python package providing flexible base classes for creating objects
with type checking, immutability, and other useful features.
"""

from setuptools import setup, find_packages
import pathlib

# Read the contents of README.md
current_dir = pathlib.Path(__file__).parent
long_description = (current_dir / "README.md").read_text(encoding="utf-8")

# Read requirements
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="baseobject-py",
    version="0.1.0",
    author="Louis Goodnews",
    author_email="louisgoodnews95@gmail.com",
    description="A Python package providing flexible base classes for creating objects with type checking and immutability",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/louisgoodnews/BaseObject",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Typing :: Typed",
    ],
    keywords="base class, type checking, immutability, dataclass alternative",
    project_urls={
        "Bug Reports": "https://github.com/louisgoodnews/BaseObject/issues",
        "Source": "https://github.com/louisgoodnews/BaseObject",
    },
)
