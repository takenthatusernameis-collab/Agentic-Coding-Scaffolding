"""Image format detection utilities wrapping the standard library :mod:`imghdr` module.

The :mod:`imghdr` module recognizes an image format from the first bytes of a
file or a byte stream.  It reads a small header, compares it against the magic
number of every format it knows, and returns the name of the first format that
matches.

This wrapper validates every argument before the standard library is reached, so
a caller gets a clear :class:`TypeError` or :class:`ValueError` instead of an
opaque failure from the standard library.  It adds the conveniences the
standard library leaves to the caller: a header can be inspected without a
file, every matching format can be listed instead of only the first one, the
formats the interpreter knows can be listed, and a detection function can be
registered and removed again.

.. note::

   The :mod:`imghdr` module was deprecated in Python 3.11 and removed in Python
   3.13 as part of :pep:`594`.  The import below degrades gracefully: when the
   interpreter no longer ships the module, the helpers raise a
   :class:`RuntimeError` that names the missing module, while the helpers that
   need no standard library keep working.

The wrapper only reads the file it is given and never writes to the filesystem.
"""

from __future__ import annotations

import inspect
import os
import warnings
from typing import Any, Callable, List, Optional, Union, cast

__all__ = [
    "DEFAULT_HEADER_SIZE",
    "detect",
    "is_available",
    "is_image",
    "matching_formats",
    "read_header",
    "register_test",
    "supported_formats",
    "unregister_test",
    "what",
]

#: The number of bytes the standard library reads to recognize an image.
DEFAULT_HEADER_SIZE = 32

#: The type of a detection function of the standard library.
DetectionFunction = Callable[[bytes, Any], Optional[str]]

PathLike = Union[str, "os.PathLike[str]"]

try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        import imghdr as _imghdr
except ImportError:  # pragma: no cover - Python 3.13 removed the module
    _imghdr = None  # type: ignore[assignment]


def _imghdr_module() -> Any:
    """Return the standard library ``imghdr`` module.

    Returns:
        The imported :mod:`imghdr` module.

    Raises:
        RuntimeError: If the interpreter no longer ships the ``imghdr`` module.
    """
    if _imghdr is None:  # pragma: no cover - Python 3.13 removed the module
        raise RuntimeError(
            "the standard library 'imghdr' module was removed in Python 3.13; "
            "recognize the format from the magic number of the file instead"
        )
    return _imghdr


def _require_bytes(value: Any, name: str) -> bytes:
    """Return *value* as bytes, raising ``TypeError`` for other types.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The value as bytes.

    Raises:
        TypeError: If *value* is not bytes-like.
    """
    if isinstance(value, bytes):
        return value
    if isinstance(value, (bytearray, memoryview)):
        return bytes(value)
    raise TypeError(f"{name} must be bytes, got {type(value).__name__}")


def _require_text(value: Any, name: str) -> str:
    """Return *value* as text, raising ``TypeError`` for other types.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The value as text.

    Raises:
        TypeError: If *value* is not a string.
    """
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str, got {type(value).__name__}")
    return value


def _require_size(value: Any, name: str) -> int:
    """Return *value* as a positive number of bytes.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The value as an int.

    Raises:
        TypeError: If *value* is not an int (or is a bool).
        ValueError: If *value* is not positive.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")
    return value


def _require_source(value: Any, name: str) -> None:
    """Raise ``TypeError`` unless *value* is a path or a binary stream.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Raises:
        TypeError: If *value* is neither a path nor a readable stream.
    """
    if isinstance(value, (str, os.PathLike)):
        return
    if hasattr(value, "read"):
        return
    raise TypeError(
        f"{name} must be a path or a binary stream, got {type(value).__name__}"
    )


def _require_detection_function(value: Any, name: str) -> DetectionFunction:
    """Return *value* as a detection function of the standard library.

    A detection function receives the header of an image and the open file, and
    returns the name of the format it recognizes or ``None``.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The value as a detection function.

    Raises:
        TypeError: If *value* is not callable or does not accept the header and
            the file.
    """
    if not callable(value):
        raise TypeError(f"{name} must be callable, got {type(value).__name__}")
    try:
        signature = inspect.signature(value)
    except (TypeError, ValueError):  # pragma: no cover - builtins without a signature
        return cast(DetectionFunction, value)
    accepts_varargs = any(
        parameter.kind is inspect.Parameter.VAR_POSITIONAL
        for parameter in signature.parameters.values()
    )
    positional = [
        parameter
        for parameter in signature.parameters.values()
        if parameter.kind
        in (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        )
    ]
    if len(positional) < 2 and not accepts_varargs:
        raise TypeError(
            f"{name} must accept the header and the file, got {value!r}"
        )
    return cast(DetectionFunction, value)


def is_available() -> bool:
    """Return ``True`` if the interpreter ships the ``imghdr`` module.

    Returns:
        ``True`` when the standard library module could be imported.
    """
    return _imghdr is not None


def supported_formats() -> List[str]:
    """Return the names of the formats the interpreter can recognize.

    The detection functions of the standard library are named ``test_<format>``,
    so the prefix is removed to name the format a function recognizes.

    Returns:
        The names of the formats, in the order the functions are tried.

    Raises:
        RuntimeError: If the interpreter does not ship the ``imghdr`` module.
    """
    module = _imghdr_module()
    formats: List[str] = []
    for function in module.tests:
        name = getattr(function, "__name__", "")
        formats.append(name[len("test_") :] if name.startswith("test_") else name)
    return formats


def matching_formats(data: bytes) -> List[str]:
    """Return the names of every format the header matches.

    The standard library stops at the first format it recognizes, so this
    helper reports all of them.  The order is the order the detection functions
    are tried in.

    Args:
        data: The header bytes of an image.

    Returns:
        The names of the matching formats, empty when nothing matches.

    Raises:
        TypeError: If *data* is not bytes-like.
        RuntimeError: If the interpreter does not ship the ``imghdr`` module.
    """
    header = _require_bytes(data, "data")
    module = _imghdr_module()
    formats: List[str] = []
    for function in module.tests:
        result = function(header, None)
        if result:
            formats.append(str(result))
    return formats


def detect(data: bytes) -> Optional[str]:
    """Return the name of the format the header matches.

    Args:
        data: The header bytes of an image.

    Returns:
        The name of the first matching format, or ``None`` when nothing
        matches.

    Raises:
        TypeError: If *data* is not bytes-like.
        RuntimeError: If the interpreter does not ship the ``imghdr`` module.
    """
    formats = matching_formats(data)
    return formats[0] if formats else None


def what(file: Union[PathLike, Any], h: Optional[bytes] = None) -> Optional[str]:
    """Return the type of image contained in a file or byte stream.

    Args:
        file: The path of the image, or an open binary stream.
        h: The header bytes of the image.  When they are given, the file is not
            read.

    Returns:
        The name of the detected format, or ``None`` when no format matches.

    Raises:
        TypeError: If *file* is neither a path nor a binary stream, or if *h* is
            not bytes-like.
        RuntimeError: If the interpreter does not ship the ``imghdr`` module.
    """
    module = _imghdr_module()
    header = None if h is None else _require_bytes(h, "h")
    if header is None:
        _require_source(file, "file")
    return cast(Optional[str], module.what(file, h=header))


def is_image(file: Union[PathLike, Any]) -> bool:
    """Return ``True`` if the file holds an image the interpreter recognizes.

    Args:
        file: The path of the image, or an open binary stream.

    Returns:
        ``True`` when a format is recognized, ``False`` otherwise.

    Raises:
        TypeError: If *file* is neither a path nor a binary stream.
        RuntimeError: If the interpreter does not ship the ``imghdr`` module.
    """
    return what(file) is not None


def read_header(file: Union[PathLike, Any], size: int = DEFAULT_HEADER_SIZE) -> bytes:
    """Return the first bytes of a file or byte stream.

    The position of a stream is restored, so reading the header never changes
    what the caller reads next.

    Args:
        file: The path of the image, or an open binary stream.
        size: The number of bytes to read.

    Returns:
        The header bytes, shorter than *size* when the file is shorter.

    Raises:
        TypeError: If *file* is neither a path nor a binary stream, or if *size*
            is not an int.
        ValueError: If *size* is not positive.
    """
    _require_size(size, "size")
    _require_source(file, "file")
    if isinstance(file, (str, os.PathLike)):
        with open(cast(str, os.fspath(file)), "rb") as handle:
            return handle.read(size)
    stream = cast(Any, file)
    location = stream.tell()
    try:
        return cast(bytes, stream.read(size))
    finally:
        stream.seek(location)


def register_test(function: DetectionFunction) -> str:
    """Register a detection function and return the name it is registered under.

    The registered function is tried after the functions of the standard
    library, so it only recognizes a format no other function recognizes.

    Args:
        function: The detection function to register.  It receives the header of
            an image and the open file, and returns the name of the format it
            recognizes or ``None``.

    Returns:
        The name the function is registered under.

    Raises:
        TypeError: If *function* is not callable or does not accept the header
            and the file.
        RuntimeError: If the interpreter does not ship the ``imghdr`` module.
    """
    module = _imghdr_module()
    detection = _require_detection_function(function, "function")
    module.tests.append(detection)
    return str(getattr(detection, "__name__", repr(detection)))


def unregister_test(name: str) -> bool:
    """Remove a registered detection function.

    Args:
        name: The name of the detection function to remove.

    Returns:
        ``True`` when a function was removed, ``False`` when no function is
        registered under that name.

    Raises:
        TypeError: If *name* is not a string.
        RuntimeError: If the interpreter does not ship the ``imghdr`` module.
    """
    module = _imghdr_module()
    _require_text(name, "name")
    tests = module.tests
    for index, function in enumerate(tests):
        if getattr(function, "__name__", None) == name:
            del tests[index]
            return True
    return False
