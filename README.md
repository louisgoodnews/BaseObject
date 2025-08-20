# BaseObject

A Python package providing flexible base classes for creating objects with type checking, immutability, and other useful features.

## Features

- **Type Checking**: Automatic type validation for class attributes
- **Mutable and Immutable Variants**: Choose between mutable and immutable object behavior
- **Dictionary-like Interface**: Access attributes using dot notation or dictionary-style access
- **Rich Comparison**: Built-in comparison operators (`==`, `!=`, `<`, `>`, etc.)
- **Serialization**: Easy conversion to and from dictionaries and JSON
- **Flexible Initialization**: Supports both annotated and non-annotated attributes

## Installation

```bash
pip install baseobject
```

## Usage

### Basic Usage

```python
from BaseObject.core import MutableBaseObject, ImmutableBaseObject

# Create a mutable object
person = MutableBaseObject(
    name="John Doe",
    age=30,
    email="john@example.com"
)

# Access attributes
print(person.name)  # John Doe
print(person["age"])  # 30

# Update attributes
person.name = "Jane Doe"
person["age"] = 31

# Convert to dictionary
person_dict = dict(person)
```

### Type Annotations

```python
class User(MutableBaseObject):
    name: str
    age: int
    email: str = None  # Optional field

# Type checking is enforced
user = User(name="Alice", age=25)  # Valid
user = User(name=123, age="25")     # Raises TypeError
```

### Immutable Objects

```python
class ImmutableUser(ImmutableBaseObject):
    name: str
    age: int

user = ImmutableUser(name="Bob", age=40)
user.name = "Robert"  # Raises AttributeError: Cannot modify immutable object

# Create a modified copy
new_user = user.copy()
new_user = new_user.set("name", "Robert")  # Returns a new instance
```

## API Reference

### MutableBaseObject

Base class for mutable objects with type checking.

**Methods:**
- `__getitem__`, `__setitem__`: Dictionary-style access
- `__delitem__`: Delete an attribute
- `__contains__`: Check if attribute exists
- `__iter__`: Iterate over attributes
- `__len__`: Number of attributes
- `copy()`: Create a shallow copy
- `to_dict()`: Convert to dictionary
- `to_json()`: Convert to JSON string
- `update(**kwargs)`: Update multiple attributes
- `get(key, default=None)`: Get attribute with default

### ImmutableBaseObject

Base class for immutable objects (inherits from MutableBaseObject).

**Additional Methods:**
- `set(key, value)`: Return a new instance with updated attribute
- `update(**kwargs)`: Return a new instance with multiple updates
- `copy(as_mutable=False)`: Create a copy (mutable or immutable)

## License

MIT

## Author

Louis Goodnews