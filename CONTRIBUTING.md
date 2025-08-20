# Contributing to BaseObject

Thank you for considering contributing to BaseObject! We appreciate your interest in making this project better. This document outlines the process for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)
- [Code Style](#code-style)
- [Testing](#testing)
- [Documentation](#documentation)
- [License](#license)

## Code of Conduct

By participating in this project, you are expected to uphold our [Code of Conduct](CODE_OF_CONDUCT.md). Please report any unacceptable behavior to the project maintainers.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Install the development dependencies
4. Create a feature branch for your changes

## Development Setup

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/BaseObject.git
   cd BaseObject
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e .[dev]
   ```

## Making Changes

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b bugfix/issue-number-short-description
   ```

2. Make your changes following the code style guidelines
3. Add tests for your changes
4. Update documentation as needed
5. Run tests and ensure they pass

## Pull Request Process

1. Push your changes to your fork
2. Open a pull request against the `main` branch
3. Ensure all CI checks pass
4. Request review from one or more maintainers
5. Address any review feedback
6. Once approved, a maintainer will merge your changes

## Reporting Issues

When reporting issues, please include:

- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Environment information (Python version, OS, etc.)
- Any relevant error messages or logs

## Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use type hints for all function/method signatures
- Keep lines under 100 characters
- Use `black` for code formatting
- Use `isort` for import sorting

## Testing

- Write tests for all new functionality
- Ensure all tests pass before submitting a PR
- Run tests using:
  ```bash
  pytest
  ```
- Generate coverage report:
  ```bash
  pytest --cov=BaseObject tests/
  ```

## Documentation

- Update documentation for any new features or changes
- Follow the existing documentation style
- Ensure docstrings follow [Google style](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)

## License

By contributing to BaseObject, you agree that your contributions will be licensed under its [MIT License](LICENSE).

---

Thank you for your contribution! We appreciate your help in making BaseObject better.