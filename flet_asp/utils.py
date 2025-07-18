import ujson
from typing import Any


def deep_equal(a: Any, b: Any) -> bool:
    """
    Performs a deep comparison between two values.

    This function serializes both values using `ujson.dumps()` with sorted keys
    to ensure structural equality, especially for nested dictionaries and lists.

    If the values are unserializable (e.g., contain functions), it falls back to `a == b`.

    Args:
        a (Any): First value to compare.
        b (Any): Second value to compare.

    Returns:
        bool: True if values are deeply equal, False otherwise.
    """

    try:
        return ujson.dumps(a, sort_keys=True) == ujson.dumps(b, sort_keys=True)
    except (TypeError, OverflowError):
        return a == b
