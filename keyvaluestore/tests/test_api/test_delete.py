import unittest
import json
from keyvaluestore.api import create, delete
from keyvaluestore.kvstore import create_entry
from keyvaluestore.models import KeyValueEntry


def gen_event(key, value):
    return {
        "pathParameters": {"key": key},
        "body": json.dumps({"key": key, "value": value})
    }


class TestApiDelete(unittest.TestCase):

    def setUp(self):
        if not KeyValueEntry.exists():
            KeyValueEntry.create_table(wait=True, read_capacity_units=1, write_capacity_units=1)

    def tearDown(self):
        if KeyValueEntry.exists():
            KeyValueEntry.delete_table()

    def test_delete_entry(self):
        key = "foo"
        value = ["bar"]
        create_entry(key, value)
        event = gen_event(key, value)

        res = delete(event, None)
        self.assertEquals(204, res['statusCode'])


    def test_delete_nonexistent_entry(self):
        event = gen_event("meh", None)
        res = delete(event, None)
        self.assertEquals(404, res['statusCode'])

    def test_delete_nonstring_key(self):
        key = 1
        event = gen_event(key, None)

        res = delete(event, None)
        self.assertEquals(422, res['statusCode'])


if __name__ == '__main__':
    import os

    os.environ["DYNAMODB_TABLE"] = "test_kv_store"
    os.environ["LOCAL"] = "1"
    unittest.main()
