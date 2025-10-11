"""
Author: Louis Goodnews
Date: 2025-08-20
"""

from core.core import ImmutableBaseObject, MutableBaseObject


def main() -> None:
    """ """

    # Demo: MutableBaseObject
    print("=== MutableBaseObject Demo ===")

    class Person(MutableBaseObject):
        name: str
        age: int

    p = Person(name="Alice", age=30)

    print("Initial:", p)
    print("Keys:", p.keys())
    print("Values:", p.values())
    print("Has 'name'? ", p.has(key="name"))
    print("Has value 30? ", p.has(value=30))
    print("Has value 'Alice'? ", p.has(value="Alice"))
    print("Is 30 years old?", p.has(key="age", value=30))

    # Update attributes
    p.set("age", 31)
    p["name"] = "Bob"
    p.update(age=32)
    print("After updates:", p)

    # Copy
    p_copy = p.copy()
    print("Copy:", p_copy)

    # Deep copy
    p_deep = p.deep_copy()
    print("Deep copy (immutable):", p_deep)
    p_deep_mut = p.deep_copy(as_mutable=True)
    print("Deep copy (mutable):", p_deep_mut)

    # Iteration
    print("Iterating over attributes:")
    for key, value in p.items():
        print(f" {key} = {value}")

    # JSON conversion
    json_str = p.to_json()
    print("JSON:", json_str)
    p_from_json = Person.from_json(json_str)
    print("From JSON:", p_from_json)

    # Demo: ImmutableBaseObject
    print("\n=== ImmutableBaseObject Demo ===")

    class Point(ImmutableBaseObject):
        x: int
        y: int

    pt = Point(x=10, y=20)
    print("Initial:", pt)

    # Test immutability
    try:
        pt.x = 15
    except AttributeError as e:
        print("Cannot modify:", e)

    try:
        pt["y"] = 25
    except AttributeError as e:
        print("Cannot modify:", e)

    # Copy to mutable
    pt_mut = pt.copy(as_mutable=True)
    print("Mutable copy:", pt_mut)
    pt_mut.x = 15
    print("Modified mutable copy:", pt_mut)

    # Deep copy
    pt_deep = pt.deep_copy()
    print("Deep copy (immutable):", pt_deep)
    pt_deep_mut = pt.deep_copy(as_mutable=True)
    print("Deep copy (mutable):", pt_deep_mut)
    pt_deep_mut.y = 30
    print("Modified deep mutable copy:", pt_deep_mut)

    # Check has method
    print("Has key 'x'? ", pt.has(key="x"))
    print("Has value 20? ", pt.has(value=20))


if __name__ == "__main__":
    main()
