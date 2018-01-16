import unittest
import json
from keyvaluestore.api import create, get, list_entries
from keyvaluestore.kvstore import create_entry
from keyvaluestore.models import KeyValueEntry


def gen_event(key, value):
    return {
        "pathParameters": {"key": key},
        "body": json.dumps({"key": key, "value": value})
    }


class TestApiGet(unittest.TestCase):

    def setUp(self):
        if not KeyValueEntry.exists():
            KeyValueEntry.create_table(wait=True, read_capacity_units=1, write_capacity_units=1)

    def tearDown(self):
        if KeyValueEntry.exists():
            KeyValueEntry.delete_table()

    def test_list_entries(self):
        value = ["bar", "baz"]
        create_entry("foo", value)
        create_entry("foo2", value)
        res = list_entries(None, None)

        self.assertEquals(200, res['statusCode'])
        data = json.loads(res["body"])
        self.assertEqual(2, len(data['entries']))


    def test_list_entries_empty(self):
        res = list_entries(None, None)

        self.assertEquals(200, res['statusCode'])
        data = json.loads(res["body"])
        self.assertEqual(0, len(data['entries']))
