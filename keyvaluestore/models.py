import os
from pynamodb.attributes import UnicodeAttribute, UnicodeSetAttribute
from pynamodb.models import Model


class KeyValueEntry(Model):
    class Meta:
        table_name = os.environ["DYNAMODB_TABLE"]
        if "LOCAL" in os.environ:
            host = "http://localhost:8000"
        else:
            region = "us-west-1"
            host = "https://dynamodb.us-west-1.amazonaws.com"

    key = UnicodeAttribute(hash_key=True, null=False)
    value = UnicodeSetAttribute(null=False)