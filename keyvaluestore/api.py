import json

from pynamodb.exceptions import DeleteError, DoesNotExist

from keyvaluestore.exc import HTTPError, create_exception_response
from keyvaluestore import kvstore
from keyvaluestore.validation import validate_fields_present


def _serialize_entry(entry):
    return {
        "key": entry.key,
        "value": [v for v in entry.value]
    }


def _get_key(event):
    try:
        key = event['pathParameters']['key']
    except KeyError:
        raise HTTPError(error_message="Internal Server Error - Key Not Provided")
    else:
        return key


def create(event, context):
    try:
        data = json.loads(event["body"])
        validate_fields_present(data, require_key=True, require_value=True)
    except HTTPError as exc:
        return exc.as_response()

    entry = kvstore.create_entry(data["key"], data["value"])
    return {"statusCode": 201,
            "body": json.dumps(_serialize_entry(entry))}


def get(event, context):
    try:
        key = _get_key(event)
        entry = kvstore.get_entry(key)
    except HTTPError as exc:
        return exc.as_response()
    except DoesNotExist:
        return create_exception_response(404, "Entry Not Found")

    return {"statusCode": 200,
            "body": json.dumps(_serialize_entry(entry))}


def list_entries(event, context):
    entries = kvstore.list_all_entries()
    return {"statusCode": 200,
            "body": json.dumps({'entries': [_serialize_entry(entry) for entry in entries]})}


def update(event, context):
    try:
        key = _get_key(event)
        data = json.loads(event["body"])
        validate_fields_present(data, require_value=True)
        entry = kvstore.update_entry(key, data["value"])
    except HTTPError as exc:
        return exc.as_response()

    return {'statusCode': 200,
            'body': json.dumps(_serialize_entry(entry))}


def delete(event, context):
    try:
        key = _get_key(event)
        kvstore.delete_entry(key)
    except HTTPError as exc:
        return exc.as_response()
    except DeleteError:
        return create_exception_response(400, f'Unable To Delete Entry With Key: {key}')
    except DoesNotExist:
        return create_exception_response(404, "Entry Not Found")

    return {'statusCode': 204}
