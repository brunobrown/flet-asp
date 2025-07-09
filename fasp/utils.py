import ujson
from typing import Any


def deep_equal(a: Any, b: Any) -> bool:
    try:
        return ujson.dumps(a, sort_keys=True) == ujson.dumps(b, sort_keys=True)
    except (TypeError, OverflowError):
        return a == b
