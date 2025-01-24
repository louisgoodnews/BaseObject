import unittest

from BaseObject.core.base.object import MutableBaseObject, ImmutableBaseObject
from BaseObject.core.base.manager import BaseObjectManager


class TestMutableBaseObject(unittest.TestCase):
    def setUp(self):
        self.obj = MutableBaseObject(name="TestObject", value=42)

    def test_initialization(self):
        self.assertEqual(self.obj.name, "TestObject")
        self.assertEqual(self.obj.value, 42)

    def test_set_attribute(self):
        self.obj.new_attr = "New"
        self.assertEqual(self.obj.new_attr, "New")

    def test_get_nonexistent_attribute(self):
        self.assertIsNone(self.obj.get("nonexistent"))

    def test_to_dict(self):
        expected_dict = {"name": "TestObject", "value": 42}
        self.assertEqual(self.obj.to_dict(), expected_dict)


class TestImmutableBaseObject(unittest.TestCase):
    def setUp(self):
        self.obj = ImmutableBaseObject(name="ImmutableObject", value=99)

    def test_initialization(self):
        self.assertEqual(self.obj.name, "ImmutableObject")
        self.assertEqual(self.obj.value, 99)

    def test_set_attribute(self):
        with self.assertRaises(AttributeError):
            self.obj.name = "NewName"

    def test_delete_attribute(self):
        with self.assertRaises(AttributeError):
            del self.obj.name

    def test_to_dict(self):
        expected_dict = {"name": "ImmutableObject", "value": 99}
        self.assertEqual(self.obj.to_dict(), expected_dict)


class TestBaseObjectManager(unittest.TestCase):
    def setUp(self):
        self.manager = BaseObjectManager()

    def test_add_to_cache(self):
        self.manager.add_to_cache("key1", {"data": "value1"})
        self.assertTrue(self.manager.is_key_in_cache("key1_0"))

    def test_get_value_from_cache(self):
        self.manager.add_to_cache("key2", {"data": "value2"})
        value = self.manager.get_value_from_cache("key2_0")
        self.assertEqual(value, {"data": "value2"})

    def test_cache_flush(self):
        self.manager.add_to_cache("key3", {"data": "value3"})
        self.manager.flush_cache(force=True)
        self.assertTrue(self.manager.is_cache_empty())

    def test_cache_timestamp_expiry(self):
        self.manager.time_limit = 1  # Set time limit to 1 second
        self.manager.add_to_cache("key4", {"data": "value4"})
        import time

        time.sleep(2)
        self.assertFalse(self.manager.is_cache_valid())

    def test_cache_clear(self):
        self.manager.add_to_cache("key5", {"data": "value5"})
        self.manager.clear_cache()
        self.assertTrue(self.manager.is_cache_empty())


if __name__ == "__main__":
    unittest.main()
