import marshal
from typing import Any, Union


def dumps(obj: Any, version: int = marshal.version) -> bytes:
    """
    Serialize an object to a bytes string using the marshal module.

    Args:
        obj: The object to serialize.
        version: The marshal protocol version to use.

    Returns:
        Serialized bytes representation of obj.

    Raises:
        TypeError: If version is not an integer.
        ValueError: If version is out of range [0, marshal.version].
        ValueError: If the object cannot be marshaled by marshal.
    """
    if not isinstance(version, int):
        raise TypeError(f"version must be an int, got {type(version).__name__}")
    if version < 0 or version > marshal.version:
        raise ValueError(
            f"version must be between 0 and {marshal.version}, got {version}"
        )
    try:
        return marshal.dumps(obj, version)
    except Exception as e:
        raise ValueError(f"Failed to marshal object: {e}") from e


def loads(data: Union[bytes, bytearray, memoryview]) -> Any:
    """
    Deserialize bytes to an object using the marshal module.

    Args:
        data: Bytes data to deserialize.

    Returns:
        The deserialized object.

    Raises:
        TypeError: If data is not bytes-like.
        ValueError: If the data cannot be unmarshaled by marshal.
    """
    if not isinstance(data, (bytes, bytearray, memoryview)):
        raise TypeError(
            f"data must be bytes-like (bytes, bytearray, memoryview), "
            f"got {type(data).__name__}"
        )
    try:
        return marshal.loads(data)
    except Exception as e:
        raise ValueError(f"Failed to unmarshal data: {e}") from e


def dump(obj: Any, file: Any, version: int = marshal.version) -> None:
    """
    Serialize an object to a file-like object using the marshal module.

    Args:
        obj: The object to serialize.
        file: A file-like object with a write method that accepts bytes.
        version: The marshal protocol version to use.

    Returns:
        None.

    Raises:
        TypeError: If file is not writeable or version is not an integer.
        ValueError: If version is out of range or marshaling fails.
        AttributeError: If file lacks a write method.
    """
    if not hasattr(file, "write"):
        raise AttributeError("file must have a 'write' method")
    if not callable(file.write):
        raise TypeError("file.write must be callable")
    if not isinstance(version, int):
        raise TypeError(f"version must be an int, got {type(version).__name__}")
    if version < 0 or version > marshal.version:
        raise ValueError(
            f"version must be between 0 and {marshal.version}, got {version}"
        )
    try:
        marshal.dump(obj, file, version)
    except Exception as e:
        raise ValueError(f"Failed to marshal object to file: {e}") from e


def load(file: Any) -> Any:
    """
    Deserialize an object from a file-like object using the marshal module.

    Args:
        file: A file-like object with a read method that accepts bytes count.

    Returns:
        The deserialized object.

    Raises:
        TypeError: If file is not readable.
        ValueError: If unmarshaling fails.
        AttributeError: If file lacks a read method.
    """
    if not hasattr(file, "read"):
        raise AttributeError("file must have a 'read' method")
    if not callable(file.read):
        raise TypeError("file.read must be callable")
    try:
        return marshal.load(file)
    except Exception as e:
        raise ValueError(f"Failed to unmarshal data from file: {e}") from e


def get_version() -> int:
    """
    Get the current marshal version.

    Returns:
        The current marshal.version value.
    """
    return marshal.version
