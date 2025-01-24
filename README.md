
# BaseObject

BaseObject is a Python library that provides a set of foundational classes for building robust, flexible, and structured Python applications. It introduces three key classes:

- **MutableBaseObject**: A customizable base class for creating mutable objects.
- **ImmutableBaseObject**: An extension of `MutableBaseObject` with enforced immutability.
- **BaseObjectManager**: A utility class for managing `BaseObject` instances with caching capabilities.

---

## Features

### 1. **MutableBaseObject**
- A flexible, mutable base class.
- Automatically integrates a logger for easy debugging and monitoring.
- Allows dynamic attribute assignment and management.
- Example methods:
  - `get(name)`: Retrieve an attribute.
  - `set(name, value)`: Set an attribute.
  - `to_dict(exclude=[])`: Export the object’s attributes as a dictionary.

---

### 2. **ImmutableBaseObject**
- Extends `MutableBaseObject` while enforcing immutability.
- Prevents modification or deletion of existing attributes after creation.
- Raises meaningful errors when attempting to alter attributes.
- Useful for scenarios where object state consistency is critical.

---

### 3. **BaseObjectManager**
- A manager for handling multiple `BaseObject` instances with a built-in caching system.
- Features:
  - Add objects to a cache (`add_to_cache(key, value)`).
  - Retrieve objects by key (`get_value_from_cache(key)`).
  - Clear or validate the cache (`clear_cache()`, `is_cache_valid()`).
  - Time-based cache invalidation with customizable time limits.

---

## Installation

Clone the repository and install the required dependencies.

```bash
git clone https://github.com/louisgoodnews/BaseObject.git
cd BaseObject
pip install -r requirements.txt
```

---

## Usage

### Creating a `MutableBaseObject`
```python
from core.base.object import MutableBaseObject

# Create a mutable object with dynamic attributes
obj = MutableBaseObject(name="Example", value=42)
print(obj.name)  # Output: Example

# Add a new attribute
obj.new_attr = "New"
print(obj.new_attr)  # Output: New
```

### Using an `ImmutableBaseObject`
```python
from core.base.object import ImmutableBaseObject

# Create an immutable object
obj = ImmutableBaseObject(name="Immutable Example")
print(obj.name)  # Output: Immutable Example

# Attempt to modify an attribute (will raise AttributeError)
obj.name = "New Name"  # Raises AttributeError
```

### Managing Objects with `BaseObjectManager`
```python
from core.base.manager import BaseObjectManager

# Create a manager instance
manager = BaseObjectManager()

# Add objects to the cache
manager.add_to_cache("example", {"key": "value"})

# Retrieve objects from the cache
data = manager.get_value_from_cache("example")
print(data)  # Output: {'key': 'value'}
```

---

## Project Structure

```
BaseObject/
├── assets
├── data
├── docs
├── src/
│   ├── __init__.py
│   ├── BaseObject/
│   │   ├── core/
│   │   │   ├──__init__.py
│   │   │   ├── base/
│   │   │   │   ├──__init__.py
│   │   │   │   ├── object.py         # Contains MutableBaseObject and ImmutableBaseObject
│   │   │   │   └── manager.py            # Contains BaseObjectManager
│   │   ├── utils/
│   │   │   ├── logger/
│   │   │   │   ├── logger.py         # Logger utilities
├── tests/     
│   ├── __init__.py                   # Unit tests
├── README.md                     # Project documentation
├── requirements.txt              # Python dependencies
└── setup.py                      # Setup script
```

---

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch: `git checkout -b feature/YourFeature`.
3. Commit your changes: `git commit -m 'Add YourFeature'`.
4. Push to the branch: `git push origin feature/YourFeature`.
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
