from keyvaluestore.exc import ValidationError


def validate_key(key):
    if not isinstance(key, str):
        raise ValidationError("key", "'key' must be a string.")


def validate_value(value):
    if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
        raise ValidationError("value", "'value' must be a list of strings")


def validate_fields_present(data, require_key=False, require_value=False):
    if require_key:
        if "key" not in data:
            raise ValidationError("key", "Invalid Request.  Missing 'key' field in json request.")
        if not isinstance(data["key"], str):
            raise ValidationError("key", "Key must be a string")

    if require_value:
        if "value" not in data:
            raise ValidationError("value", "Invalid Request.  Missing 'value' field in json request.")
        if not isinstance(data["value"], list):
            raise ValidationError("value", "'value' must be a list of strings")
        if not all(isinstance(v, str) for v in data["value"]):
            raise ValidationError("value", "'value' must be a list of strings")
