import unittest
import json
from keyvaluestore.api import update
from keyvaluestore.kvstore import create_entry
from keyvaluestore.models import KeyValueEntry


def gen_event(key, value):
    return {
        "pathParameters": {"key": key},
        "body": json.dumps({"key": key, "value": value})
    }


class TestApiUpdate(unittest.TestCase):

    def setUp(self):
        if not KeyValueEntry.exists():
            KeyValueEntry.create_table(wait=True, read_capacity_units=1, write_capacity_units=1)

    def tearDown(self):
        if KeyValueEntry.exists():
            KeyValueEntry.delete_table()

    def test_update(self):
        value = ["bar", "baz"]
        value2 = ["foo", "meh"]
        create_entry("foo", value)
        event = gen_event("foo", value2)
        res = update(event, None)

        self.assertEqual(200, res['statusCode'])
        data = json.loads(res["body"])
        self.assertEqual(sorted(value2), sorted(data["value"]))

    def test_update_no_value(self):
        key = "foo"
        create_entry(key, ["bar"])
        event = {"pathParameters": {"key": key}, "body": json.dumps({"key": key})}
        res = update(event, None)

        self.assertEquals(422, res['statusCode'])
        data = json.loads(res["body"])
        self.assertEqual(data["error_message"], "value: Invalid Request.  Missing 'value' field in json request.")