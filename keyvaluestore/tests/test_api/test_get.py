import unittest
import json
from keyvaluestore.api import create, get
from keyvaluestore.kvstore import create_entry
from keyvaluestore.models import KeyValueEntry


def gen_event(key, value):
    return {
        "pathParameters": {"key": key},
        "body": ""
    }


class TestApiGet(unittest.TestCase):

    def setUp(self):
        if not KeyValueEntry.exists():
            KeyValueEntry.create_table(wait=True, read_capacity_units=1, write_capacity_units=1)

    def tearDown(self):
        if KeyValueEntry.exists():
            KeyValueEntry.delete_table()

    def test_get_entry(self):
        key = "foo"
        value = ["bar"]
        create_entry(key, value)
        event = gen_event(key, value)

        res = get(event, None)
        self.assertEquals(200, res['statusCode'])
        data = json.loads(res["body"])
        self.assertEquals(data, {"key": key, "value": value})

    def test_get_entry_missing(self):
        key = "foo"
        event = gen_event(key, None)
        res = get(event, None)
        self.assertEquals(404, res['statusCode'])


    def test_get_entry_multiple_values(self):
        key = "foo"
        value = ["bar", "baz"]
        create_entry(key, value)
        event = gen_event(key, None)

        res = get(event, None)
        self.assertEquals(200, res['statusCode'])
        data = json.loads(res["body"])
        data['value'] = sorted(data['value'])
        self.assertDictEqual(data, {"key": key, "value": sorted(value)})

    def test_get_entry_nonstring(self):
        key = 1
        event = gen_event(key, None)
        res = get(event, None)
        self.assertEquals(res["statusCode"], 422)
        data = json.loads(res["body"])
        self.assertEquals(data["error_message"], "key: 'key' must be a string.")



if __name__ == '__main__':
    import os

    os.environ["DYNAMODB_TABLE"] = "test_kv_store"
    os.environ["LOCAL"] = "1"
    unittest.main()
