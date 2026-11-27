"""UUencode and UUdecode utilities wrapping the standard library :mod:`uu`."""

from __future__ import annotations

from typing import Any

try:
    import uu as _uu
    _UU_AVAILABLE = True
except Exception:  # pragma: no cover - exercised when uu is unavailable
    _uu = None  # type: ignore[assignment]
    _UU_AVAILABLE = False

__all__: list[str] = [
    "Error",
    "encode",
    "decode",
    "encode_file",
    "decode_file",
    "is_available",
]


def is_available() -> bool:
    """Return True if the standard library :mod:`uu` module is available."""
    return _UU_AVAILABLE


def _require_uu(name: str) -> None:
    if not _UU_AVAILABLE:
        raise RuntimeError(f"uu module is not available; {name} cannot be used")


if _UU_AVAILABLE:
    Error = _uu.Error
else:  # pragma: no cover - exercised when uu is unavailable
    class Error(Exception):  # type: ignore[no-redef]
        pass


def encode(
    in_file: Any,
    out_file: Any,
    name: str | None = None,
    mode: int | None = None,
    backtick: bool = False,
) -> None:
    """UUencode from *in_file* to *out_file*.

    Delegates to :func:`uu.encode`.

    Args:
        in_file: The input binary stream to read from.
        out_file: The output binary stream to write to.
        name: The file name to embed in the header (defaults to ``"-"``).
        mode: The file mode to embed in the header (defaults to ``0o666``).
        backtick: Use a backtick instead of a space for zero padding.

    Raises:
        RuntimeError: If the standard library :mod:`uu` module is unavailable.
        AttributeError: If *in_file* or *out_file* is not a file-like object.
            # audit-ignore: AttributeError
    """
    _require_uu("encode")
    if name is None:
        name = "-"
    if mode is None:
        mode = 0o666
    try:
        _uu.encode(in_file, out_file, name, mode, backtick=backtick)
    except TypeError:
        # Fallback for older Python versions where backtick kwarg is not supported
        _uu.encode(in_file, out_file, name, mode)


def decode(
    in_file: Any,
    out_file: Any | None = None,
    mode: int | None = None,
    quiet: int = 0,
) -> None:
    """UUdecode from *in_file* to *out_file*.

    Delegates to :func:`uu.decode`.

    Args:
        in_file: The input binary stream to read from.
        out_file: The output binary stream to write to, or ``None`` to discard.
        mode: The file mode to apply (defaults to ``0o666``).
        quiet: Suppress progress output when non-zero.

    Raises:
        RuntimeError: If the standard library :mod:`uu` module is unavailable.
        AttributeError: If *in_file* is not a file-like object.
            # audit-ignore: AttributeError
    """
    _require_uu("decode")
    if mode is None:
        mode = 0o666
    try:
        _uu.decode(in_file, out_file, mode, bool(quiet))
    except TypeError:
        # Fallback for older Python versions where quiet kwarg is not supported
        _uu.decode(in_file, out_file, mode, bool(quiet))


def encode_file(
    in_file: Any,
    out_file: Any,
    name: str = "-",
    mode: int = 0o666,
    backtick: bool = False,
) -> None:
    encode(in_file, out_file, name, mode, backtick)


def decode_file(
    in_file: Any,
    out_file: Any | None = None,
    mode: int = 0o666,
    quiet: int = 0,
) -> None:
    decode(in_file, out_file, mode, quiet)
