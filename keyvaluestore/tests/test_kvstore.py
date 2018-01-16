import unittest
import json

from pynamodb.exceptions import DoesNotExist

from keyvaluestore.exc import HTTPError, ValidationError
from keyvaluestore.kvstore import create_entry, get_entry, list_all_entries, update_entry, delete_entry
from keyvaluestore.models import KeyValueEntry


class TestHandler(unittest.TestCase):
    """ Tests handler methods """

    def setUp(self):
        if not KeyValueEntry.exists():
            KeyValueEntry.create_table(wait=True, read_capacity_units=1, write_capacity_units=1)

    def tearDown(self):
        if KeyValueEntry.exists():
            KeyValueEntry.delete_table()

    def test_create_entry(self):
        key = "foo"
        value = ["bar"]
        entry = create_entry(key, value)
        self.assertEqual(key, entry.key)
        self.assertListEqual(value, entry.value)

    def test_create_entry_nonstring_key(self):
        key = 1
        value = ["bar"]
        with self.assertRaises(ValidationError) as exc:
            entry = create_entry(key, value)
        self.assertEqual(exc.exception.field, "key")
        self.assertEqual(exc.exception.message, "'key' must be a string.")

    def test_create_entry_nonstring_value(self):
        key = "foo"
        value = [1]
        with self.assertRaises(ValidationError) as exc:
            entry = create_entry(key, value)
        self.assertEqual(exc.exception.field, "value")
        self.assertEqual(exc.exception.message, "'value' must be a list of strings")


    def test_create_entry_nonlist_value(self):
        key = "foo"
        value = [1]
        with self.assertRaises(ValidationError) as exc:
            entry = create_entry(key, value)
        self.assertEqual(exc.exception.field, "value")
        self.assertEqual(exc.exception.message, "'value' must be a list of strings")

    def test_get_entry_by_key(self):
        key = "foo"
        value = ["bar"]
        create_entry(key, value)
        entry = get_entry(key)
        self.assertEqual(key, entry.key)
        self.assertListEqual(value, list(entry.value))

    def test_get_entry_key_missing(self):
        key = "Hello"
        with self.assertRaises(DoesNotExist) as exc:
            entry = get_entry(key)

    def test_get_entry_by_key_multiple_values(self):
        key = "foo"
        value = ["bar", "baz"]
        create_entry(key, value)
        entry = get_entry(key)
        self.assertEqual(key, entry.key)
        self.assertListEqual(sorted(value), sorted(entry.value))

    def test_get_entry_key_nonstring(self):
        key = 1
        with self.assertRaises(ValidationError) as exc:
            entry = get_entry(key)
        self.assertEqual(exc.exception.field, "key")
        self.assertEqual(exc.exception.message, "'key' must be a string.")

    def test_list_all_entries(self):
        value = ["bar", "baz"]
        create_entry("foo", value)
        create_entry("foo2", value)
        entries = list(list_all_entries())
        self.assertEqual(2, len(entries))
        for entry in entries:
            if entry.key in ["foo", "foo2"]:
                self.assertListEqual(sorted(entry.value), sorted(value))

    def test_list_all_entries_empty(self):
        entries = list(list_all_entries())
        self.assertEqual(0, len(entries))

    def test_update_entry(self):
        value1 = ['foo', 'bar']
        value2 = ['bar', 'baz']
        entry = create_entry("foo", value1)
        self.assertListEqual(sorted(value1), sorted(entry.value))

        updated_entry = update_entry('foo', value2)
        self.assertListEqual(sorted(value2), sorted(updated_entry.value))

        entry.refresh()
        self.assertListEqual(sorted(value2), sorted(entry.value))

    def test_update_entry_invalid_key(self):
        value = ['foo', 'bar']
        with self.assertRaises(DoesNotExist):
            update_entry("foo", value)

    def test_update_entry_nonstring_value(self):
        value = ["bar", "baz"]
        value2 = [1]
        create_entry("foo", value)

        with self.assertRaises(ValidationError) as exc:
            update_entry("foo", value2)
        self.assertEqual(exc.exception.field, "value")
        self.assertEqual(exc.exception.message, "'value' must be a list of strings")

    def test_update_entry_nonlist_value(self):
        value = ["bar", "baz"]
        value2 = "hello"
        create_entry("foo", value)

        with self.assertRaises(ValidationError) as exc:
            update_entry("foo", value2)
        self.assertEqual(exc.exception.field, "value")
        self.assertEqual(exc.exception.message, "'value' must be a list of strings")

    def test_delete_entry(self):
        value = ["bar", "baz"]
        create_entry("foo", value)
        delete_entry("foo")
        with self.assertRaises(DoesNotExist):
            get_entry("foo")


    def test_delete_nonexistent_entry(self):
        with self.assertRaises(DoesNotExist):
            delete_entry("foo")

    def test_delete_nonstring_key(self):
        with self.assertRaises(ValidationError) as exc:
            delete_entry(1)
        self.assertEqual(exc.exception.field, "key")
        self.assertEqual(exc.exception.message, "'key' must be a string.")


if __name__ == '__main__':
    import os

    os.environ["DYNAMODB_TABLE"] = "test_kv_store"
    os.environ["LOCAL"] = "1"
    unittest.main()
