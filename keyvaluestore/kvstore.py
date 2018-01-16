from logging import getLogger

from pynamodb.exceptions import DoesNotExist, DeleteError

from keyvaluestore.exc import HTTPError
from keyvaluestore.models import KeyValueEntry
from keyvaluestore.validation import validate_key, validate_value

logger = getLogger(__name__)



def create_entry(key, value):
    validate_key(key)
    validate_value(value)
    entry = KeyValueEntry(key=key, value=value)
    entry.save()
    return entry


def get_entry(key):
    validate_key(key)
    entry = KeyValueEntry.get(hash_key=key)
    return entry


def list_all_entries():
    return KeyValueEntry.scan()


def update_entry(key, value):
    validate_key(key)
    validate_value(value)
    entry = get_entry(key)
    if value != entry.value:
        entry.update(actions=[KeyValueEntry.value.set(value)])
    else:
        logger.info('Nothing changed did not update')
    return entry


def delete_entry(key):
    validate_key(key)
    entry = get_entry(key)
    entry.delete() # May raise DeleteError. let it pass through
