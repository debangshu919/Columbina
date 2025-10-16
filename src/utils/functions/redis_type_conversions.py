from typing import Any, Dict, Union


def serialize_for_redis(data: Dict[str, Any]) -> Dict[str, str]:
    """
    Convert Python data types to Redis-compatible string format.

    Args:
        data: Dictionary with mixed data types

    Returns:
        Dictionary with all values converted to strings
    """
    redis_data = {}
    for key, value in data.items():
        if isinstance(value, bool):
            redis_data[key] = str(value)
        elif isinstance(value, (int, float)):
            redis_data[key] = str(value)
        elif value is None:
            redis_data[key] = "None"
        else:
            redis_data[key] = str(value)
    return redis_data


def deserialize_from_redis(
    cache: Dict[Union[str, bytes], Union[str, bytes]],
) -> Dict[str, Any]:
    """
    Convert Redis string values back to proper Python types.

    Args:
        cache: Raw Redis hash data (keys and values may be bytes or strings)

    Returns:
        Dictionary with properly typed values
    """
    cache_data = {}
    for key, value in cache.items():
        # Convert bytes to strings if needed
        key = key.decode() if isinstance(key, bytes) else key
        value = value.decode() if isinstance(value, bytes) else value

        # Convert string values back to proper types
        if value in ("True", "False"):
            cache_data[key] = value == "True"
        elif value.isdigit() or (value.startswith("-") and value[1:].isdigit()):
            cache_data[key] = int(value)
        elif value == "None":
            cache_data[key] = None
        else:
            cache_data[key] = value

    return cache_data
