from __future__ import annotations

import datetime
import json
from uuid import uuid4

from iso8601 import iso8601, ParseError


def uid() -> str:
    return str(uuid4()).replace("-", "")


_uid = uid


def utcnow() -> datetime.datetime:
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)


def str_to_datetime_if_parseable(value: str) -> datetime.datetime | str:
    if len(value) < 8 or value.count('-') != 2:
        return value
    try:
        ret = iso8601.parse_date(value)
    except (ParseError, ValueError, TypeError):
        ret = value
    return ret


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()


class CustomJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.try_datetime, *args, **kwargs)

    @staticmethod
    def try_datetime(d):
        ret = {}
        for key, value in d.items():
            if isinstance(value, str):
                ret[key] = str_to_datetime_if_parseable(value)
            else:
                ret[key] = value
        return ret
