import json
from typing import Any


def deep_equal(a: Any, b: Any):
    try:
        return json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
    except TypeError:
        return a == b
