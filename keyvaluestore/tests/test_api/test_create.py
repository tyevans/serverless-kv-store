import unittest
import json
from keyvaluestore.api import create
from keyvaluestore.models import KeyValueEntry


def gen_event(key, value):
    return {
        "pathParameters": {"key": key},
        "body": json.dumps({"key": key, "value": value})
    }


class TestApiCreate(unittest.TestCase):
    """ Tests handler methods """

    def setUp(self):
        if not KeyValueEntry.exists():
            KeyValueEntry.create_table(wait=True, read_capacity_units=1, write_capacity_units=1)

    def tearDown(self):
        if KeyValueEntry.exists():
            KeyValueEntry.delete_table()

    def test_create_entry(self):
        """ Tests entry creation """
        key = "foo"
        value = "bar"
        """ Tests entry creation """
        event = gen_event(key, [value])
        res = create(event, None)
        self.assertEquals(201, res['statusCode'])
        data = json.loads(res["body"])
        self.assertEquals(data, {"key": key, "value": [value]})

    def test_create_duplicate_entry(self):
        """ Tests entry creation """
        key = "foo"
        value = "bar"
        event = gen_event(key, [value])
        res = create(event, None)
        self.assertEquals(201, res['statusCode'])
        data = json.loads(res["body"])
        self.assertEquals(data, {"key": key, "value": [value]})

        res2 = create(event, None)
        self.assertEquals(201, res2['statusCode'])
        data2 = json.loads(res["body"])
        self.assertEquals(data2, {"key": key, "value": [value]})

    def test_create_nonstring_key(self):
        key = 1
        value = ["bar"]
        event = gen_event(key, value)

        res = create(event, None)
        self.assertEquals(res["statusCode"], 422)
        data = json.loads(res["body"])
        self.assertEquals(data["error_message"], "key: Key must be a string")

    def test_create_nonstring_value(self):
        key = "foo"
        value = [1]
        event = gen_event(key, value)

        res = create(event, None)
        self.assertEquals(res["statusCode"], 422)
        data = json.loads(res["body"])
        self.assertEquals(data["error_message"], "value: 'value' must be a list of strings")

    def test_create_nonlist_value(self):
        key = "foo"
        value = "bar"
        event = gen_event(key, value)

        res = create(event, None)
        self.assertEquals(res["statusCode"], 422)
        data = json.loads(res["body"])
        self.assertEquals(data["error_message"], "value: 'value' must be a list of strings")


if __name__ == '__main__':
    import os

    os.environ["DYNAMODB_TABLE"] = "test_kv_store"
    os.environ["LOCAL"] = "1"
    unittest.main()
