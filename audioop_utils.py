"""Audio utilities wrapping the standard library :mod:`audioop` module.

The :mod:`audioop` module works on raw audio fragments: byte strings that hold
one sample per frame.  A frame is one, two, three, or four bytes wide, and the
width decides how a sample is read: eight bits, a signed sixteen bit number, a
signed twenty four bit number, or a signed thirty two bit number.

The standard library offers three groups of helpers: conversions between the
widths and between the linear, u-law, and a-law encodings; arithmetic on
fragments, such as adding a bias, adding two fragments, scaling a fragment, or
mixing the two channels of a stereo fragment into one; and measurements of a
fragment, such as its average, its root mean square, its peak, and the number
of frames it holds.  The module also resamples a fragment and codes it with
ADPCM.

This wrapper validates every argument before the standard library is reached,
so a caller gets a clear :class:`TypeError` or :class:`ValueError` instead of
an opaque failure.  It adds the helpers the standard library leaves to the
caller: the measurements of a fragment are reported together, the state of a
resampling is kept by a :class:`Resampler` instead of by the caller, the index
of a sample may be negative, and an empty fragment is rejected by the
measurements instead of being reported as silence.  The helper
:func:`is_available` reports whether the interpreter still ships the module.

.. note::

   The :mod:`audioop` module was deprecated in Python 3.11 and removed in
   Python 3.13 as part of :pep:`594`.  The import below degrades gracefully:
   when the interpreter no longer ships the module, the helpers raise a
   :class:`RuntimeError` that points at the ``audioop-lts`` package, which
   keeps the module available.

The helpers work on copies of their arguments and never write to the file
system, so the tests of the project need no audio device and no network.
"""

from __future__ import annotations

import math
import warnings
from typing import Any, Dict, List, Optional, Tuple, Type

try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        import audioop as _audioop
except ImportError:  # pragma: no cover - Python 3.13 removed the module
    _audioop = None  # type: ignore[assignment]

__all__ = [
    "AudioOpError",
    "Resampler",
    "SAMPLE_WIDTHS",
    "add_fragments",
    "average",
    "average_peak_to_peak",
    "convert_from_a_law",
    "convert_from_u_law",
    "convert_sample_width",
    "convert_to_a_law",
    "convert_to_u_law",
    "count_zero_crossings",
    "decode_adpcm",
    "describe_fragment",
    "duplicate_to_stereo",
    "encode_adpcm",
    "find_scale_factor",
    "frame_count",
    "is_available",
    "mix_to_mono",
    "peak_range",
    "peak_to_peak",
    "peak_value",
    "resample",
    "reverse_samples",
    "root_mean_square",
    "sample_at",
    "scale",
    "shift_bias",
    "swap_byte_order",
]

#: The widths of a sample the standard library understands, in bytes.
SAMPLE_WIDTHS = (1, 2, 3, 4)

#: The error the standard library raises for an invalid audio fragment.
AudioOpError: Type[Exception] = (
    _audioop.error if _audioop is not None else RuntimeError  # type: ignore[union-attr]
)

#: The calling convention of the ADPCM helpers of the standard library.
_ADPCM_CONVENTION: Optional[str] = None


def is_available() -> bool:
    """Return ``True`` when the interpreter ships the standard library module.

    Returns:
        ``True`` when the :mod:`audioop` module can be used, ``False`` when
        the interpreter removed it.
    """
    return _audioop is not None


def _require_available() -> None:
    """Raise ``RuntimeError`` when the interpreter no longer ships the module.

    Raises:
        RuntimeError: If the interpreter no longer ships the ``audioop``
            module.
    """
    if _audioop is None:  # pragma: no cover - Python 3.13 removed the module
        raise RuntimeError(
            "the standard library 'audioop' module was removed in Python 3.13; "
            "install the 'audioop-lts' package to keep using it"
        )


def _audioop_module() -> Any:
    """Return the standard library ``audioop`` module.

    Returns:
        The imported :mod:`audioop` module.

    Raises:
        RuntimeError: If the interpreter no longer ships the ``audioop``
            module.
    """
    _require_available()
    return _audioop


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
    raise TypeError(f"{name} must be bytes-like, got {type(value).__name__}")


def _require_int(value: Any, name: str) -> int:
    """Return *value* as an integer, raising ``TypeError`` for other types.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The value as an integer.

    Raises:
        TypeError: If *value* is not an integer.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    return value


def _require_positive_int(value: Any, name: str) -> int:
    """Return *value* as an integer that is greater than zero.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The value as an integer.

    Raises:
        TypeError: If *value* is not an integer.
        ValueError: If *value* is not greater than zero.
    """
    number = _require_int(value, name)
    if number <= 0:
        raise ValueError(f"{name} must be greater than zero, got {number}")
    return number


def _require_width(value: Any, name: str = "width") -> int:
    """Return *value* as the width of a sample in bytes.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The width of a sample in bytes.

    Raises:
        TypeError: If *value* is not an integer.
        ValueError: If *value* is not one of :data:`SAMPLE_WIDTHS`.
    """
    width = _require_int(value, name)
    if width not in SAMPLE_WIDTHS:
        raise ValueError(f"{name} must be 1, 2, 3, or 4, got {width}")
    return width


def _require_factor(value: Any, name: str) -> float:
    """Return *value* as a factor, raising ``TypeError`` for other types.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The value as a factor.

    Raises:
        TypeError: If *value* is not a number.
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number, got {type(value).__name__}")
    return float(value)


def _require_frames(fragment: bytes, width: int, name: str = "fragment") -> None:
    """Raise ``ValueError`` when *fragment* does not hold whole frames.

    Args:
        fragment: The fragment to check.
        width: The width of a sample in bytes.
        name: The name of the argument, used in the error message.

    Raises:
        ValueError: If the length of *fragment* is not a multiple of *width*.
    """
    if len(fragment) % width:
        raise ValueError(
            f"{name} must hold a whole number of {width}-byte frames, "
            f"got {len(fragment)} bytes"
        )


def _require_non_empty(fragment: bytes, name: str = "fragment") -> bytes:
    """Return *fragment* when it holds a sample, raising ``ValueError`` otherwise.

    Args:
        fragment: The fragment to check.
        name: The name of the argument, used in the error message.

    Returns:
        The fragment.

    Raises:
        ValueError: If *fragment* is empty.
    """
    if not fragment:
        raise ValueError(f"{name} must not be empty")
    return fragment


def _samples(fragment: bytes, width: int) -> List[int]:
    """Return the samples of a fragment as signed integers.

    A sample is read the way the standard library reads it: the bytes of a
    frame are little endian and signed, so a frame of one byte holds a signed
    eight bit number, a frame of two bytes a signed sixteen bit number, a
    frame of three bytes a signed twenty four bit number, and a frame of four
    bytes a signed thirty two bit number.

    Args:
        fragment: The audio fragment.
        width: The width of a sample of *fragment* in bytes.

    Returns:
        The samples of the fragment.
    """
    return [
        int.from_bytes(fragment[offset : offset + width], "little", signed=True)
        for offset in range(0, len(fragment), width)
    ]


def _adpcm_convention() -> str:
    """Return the calling convention of the ADPCM helpers of the standard library.

    Python 3.12 changed the ADPCM helpers: they take the state of the
    conversion instead of the number of bits of a sample, and they return the
    state of the conversion next to the coded fragment.  The convention of the
    interpreter is detected once, so the wrapper offers the same interface on
    every version.

    Returns:
        Either ``"stateful"`` or ``"legacy"``.
    """
    global _ADPCM_CONVENTION
    if _ADPCM_CONVENTION is None:
        module = _audioop_module()
        try:
            module.lin2adpcm(b"", 2, None)
        except TypeError:
            _ADPCM_CONVENTION = "legacy"
        else:
            _ADPCM_CONVENTION = "stateful"
    return _ADPCM_CONVENTION


def frame_count(fragment: Any, width: int) -> int:
    """Return the number of frames a fragment holds.

    Args:
        fragment: The audio fragment.
        width: The width of a sample in bytes.

    Returns:
        The number of frames of the fragment.

    Raises:
        TypeError: If *fragment* is not bytes-like or *width* is not an
            integer.
        ValueError: If *width* is not a sample width the standard library
            understands, or the fragment does not hold whole frames.
    """
    data = _require_bytes(fragment, "fragment")
    size = _require_width(width)
    _require_frames(data, size)
    return len(data) // size


def convert_sample_width(fragment: Any, width: int, new_width: int) -> bytes:
    """Return the samples of a fragment in another width.

    Args:
        fragment: The audio fragment.
        width: The width of a sample of *fragment* in bytes.
        new_width: The width of a sample of the result in bytes.

    Returns:
        The fragment with its samples converted.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If a width is not a sample width the standard library
            understands, or the fragment does not hold whole frames.
        RuntimeError: If the interpreter no longer ships the ``audioop``
            module.
    """
    data = _require_bytes(fragment, "fragment")
    size = _require_width(width)
    target = _require_width(new_width, "new_width")
    _require_frames(data, size)
    module = _audioop_module()
    result: bytes = module.lin2lin(data, size, target)
    return result


def convert_to_u_law(fragment: Any, width: int) -> bytes:
    """Return the u-law encoded form of a fragment.

    Args:
        fragment: The audio fragment.
        width: The width of a sample of *fragment* in bytes.

    Returns:
        The u-law encoded fragment.  Every sample occupies one byte.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *width* is not a sample width the standard library
            understands, or the fragment does not hold whole frames.
        RuntimeError: If the interpreter no longer ships the ``audioop``
            module.
    """
    data = _require_bytes(fragment, "fragment")
    size = _require_width(width)
    _require_frames(data, size)
    module = _audioop_module()
    result: bytes = module.lin2ulaw(data, size)
    return result


def convert_from_u_law(fragment: Any, width: int) -> bytes:
    """Return the linear form of a u-law encoded fragment.

    Args:
        fragment: The u-law encoded audio fragment.
        width: The width of a sample of the result in bytes.

    Returns:
        The linear fragment.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *width* is not a sample width the standard library
            understands, or the fragment does not hold whole frames.
        RuntimeError: If the interpreter no longer ships the ``audioop``
            module.
    """
    data = _require_bytes(fragment, "fragment")
    size = _require_width(width)
    _require_frames(data, size)
    module = _audioop_module()
    result: bytes = module.ulaw2lin(data, size)
    return result


def convert_to_a_law(fragment: Any, width: int) -> bytes:
    """Return the a-law encoded form of a fragment.

    Args:
        fragment: The audio fragment.
        width: The width of a sample of *fragment* in bytes.

    Returns:
        The a-law encoded fragment.  Every sample occupies one byte.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *width* is not a sample width the standard library
            understands, or the fragment does not hold whole frames.
        RuntimeError: If the interpreter no longer ships the ``audioop``
            module.
    """
    data = _require_bytes(fragment, "fragment")
    size = _require_width(width)
    _require_frames(data, size)
    module = _audioop_module()
    result: bytes = module.lin2alaw(data, size)
    return result


def convert_from_a_law(fragment: Any, width: int) -> bytes:
    """Return the linear form of an a-law encoded fragment.

    Args:
        fragment: The a-law encoded audio fragment.
        width: The width of a sample of the result in bytes.

    Returns:
        The linear fragment.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *width* is not a sample width the standard library
            understands, or the fragment does not hold whole frames.
        RuntimeError: If the interpreter no longer ships the ``audioop``
            module.
    """
    data = _require_bytes(fragment, "fragment")
    size = _require_width(width)
    _require_frames(data, size)
    module = _audioop_module()
    result: bytes = module.alaw2lin(data, size)
    return result


def shift_bias(fragment: Any, width: int, bias: int) -> bytes:
    """Return a fragment with a bias added to every sample.

    Args:
        fragment: The audio fragment.
        width: The width of a sample of *fragment* in bytes.
        bias: The value added to every sample.

    Returns:
        The fragment with the bias applied.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *width* is not a sample width the standard library
            understands, or the fragment does not hold whole frames.
        RuntimeError: If the interpreter no longer ships the ``audioop``
            module.
    """
    data = _require_bytes(fragment, "fragment")
    size = _require_width(width)
    offset = _require_int(bias, "bias")
    _require_frames(data, size)
    module = _audioop_module()
    result: bytes = module.bias(data, size, offset)
    return result


def add_fragments(left: Any, right: Any, width: int) -> bytes:
    """Return the sum of two fragments.

    Args:
        left: The first audio fragment.
        right: The second audio fragment.
        width: The width of a sample of the fragments in bytes.

    Returns:
        The fragment that holds the sum of the samples of both fragments.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *width* is not a sample width the standard library
            understands, the fragments hold a different number of bytes, or a
            fragment does not hold whole frames.
        RuntimeError: If the interpreter no longer ships the ``audioop``
            module.
    """
    first = _require_bytes(left, "left")
    second = _require_bytes(right, "right")
    size = _require_width(width)
    _require_frames(first, size, "left")
    _require_frames(second, size, "right")
    module = _audioop_module()
    if len(first) != len(second):
        raise ValueError(
            f"both fragments must have the same length, got {len(first)} and {len(second)}"
        )
    result: bytes = module.add(first, second, size)
    return result


def scale(fragment: Any, width: int, factor: float) -> bytes:
    """Return a fragment with every sample multiplied by a factor.

    Args:
        fragment: The audio fragment.
        width: The width of a sample of *fragment* in bytes.
        factor: The factor every sample is multiplied by.

    Returns:
        The scaled fragment.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *width* is not a sample width the standard library
            understands, or the fragment does not hold whole frames.
        RuntimeError: If the interpreter no longer ships the ``audioop``
            module.
    """
    data = _require_bytes(fragment, "fragment")
    size = _require_width(width)
    multiplier = _require_factor(factor, "factor")
    _require_frames(data, size)
    module = _audioop_module()
    result: bytes = module.mul(data, size, multiplier)
    return result


def average(fragment: Any, width: int) -> float:
    """Return the average of the samples of a fragment.

    The standard library truncates the average to a whole number, so this
    wrapper reports the exact mean of the samples instead.

    Args:
        fragment: The audio fragment.
        width: The width of a sample of *fragment* in bytes.

    Returns:
        The average of the samples.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *width* is not a sample width the standard library
            understands, the fragment is empty, or the fragment does not hold
            whole frames.
        RuntimeError: If the interpreter no longer ships the ``audioop``
            module.
    """
    data = _require_bytes(fragment, "fragment")
    size = _require_width(width)
    _require_frames(data, size)
    _require_non_empty(data)
    values = _samples(data, size)
    return sum(values) / len(values)


def average_peak_to_peak(fragment: Any, width: int) -> float:
    """Return the average peak to peak value of the samples of a fragment.

    The peak to peak value of a fragment is the distance between two turning
    points of its waveform, so the value describes the shape of the waveform
    and not its offset.  The standard library reports the average as a whole
    number.

    Args:
        fragment: The audio fragment.
        width: The width of a sample of *fragment* in bytes.

    Returns:
        The average of the distances between the turning points of the
        waveform.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *width* is not a sample width the standard library
            understands, the fragment is empty, or the fragment does not hold
            whole frames.
        RuntimeError: If the interpreter no longer ships the ``audioop``
            module.
    """
    data = _require_bytes(fragment, "fragment")
    size = _require_width(width)
    _require_frames(data, size)
    _require_non_empty(data)
    module = _audioop_module()
    return float(module.avgpp(data, size))


def root_mean_square(fragment: Any, width: int) -> float:
    """Return the root mean square of the samples of a fragment.

    The standard library truncates the root mean square to a whole number, so
    this wrapper reports the exact value instead.

    Args:
        fragment: The audio fragment.
        width: The width of a sample of *fragment* in bytes.

    Returns:
        The root mean square of the samples.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *width* is not a sample width the standard library
            understands, the fragment is empty, or the fragment does not hold
            whole frames.
        RuntimeError: If the interpreter no longer ships the ``audioop``
            module.
    """
    data = _require_bytes(fragment, "fragment")
    size = _require_width(width)
    _require_frames(data, size)
    _require_non_empty(data)
    values = _samples(data, size)
    return math.sqrt(sum(value * value for value in values) / len(values))


def peak_value(fragment: Any, width: int) -> int:
    """Return the largest absolute value of the samples of a fragment.

    Args:
        fragment: The audio fragment.
        width: The width of a sample of *fragment* in bytes.

    Returns:
        The largest absolute value of the samples.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *width* is not a sample width the standard library
            understands, the fragment is empty, or the fragment does not hold
            whole frames.
        RuntimeError: If the interpreter no longer ships the ``audioop``
            module.
    """
    data = _require_bytes(fragment, "fragment")
    size = _require_width(width)
    _require_frames(data, size)
    _require_non_empty(data)
    module = _audioop_module()
    result: int = module.max(data, size)
    return result


def peak_range(fragment: Any, width: int) -> Tuple[int, int]:
    """Return the smallest and the largest sample of a fragment.

    Args:
        fragment: The audio fragment.
        width: The width of a sample of *fragment* in bytes.

    Returns:
        The smallest and the largest sample of the fragment.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *width* is not a sample width the standard library
            understands, the fragment is empty, or the fragment does not hold
            whole frames.
        RuntimeError: If the interpreter no longer ships the ``audioop``
            module.
    """
    data = _require_bytes(fragment, "fragment")
    size = _require_width(width)
    _require_frames(data, size)
    _require_non_empty(data)
    module = _audioop_module()
    result: Tuple[int, int] = module.minmax(data, size)
    return result


def peak_to_peak(fragment: Any, width: int) -> int:
    """Return the largest peak to peak value of the samples of a fragment.

    The peak to peak value of a fragment is the distance between two turning
    points of its waveform, so the value describes the shape of the waveform
    and not its offset.

    Args:
        fragment: The audio fragment.
        width: The width of a sample of *fragment* in bytes.

    Returns:
        The largest difference between two turning points of the fragment.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *width* is not a sample width the standard library
            understands, the fragment is empty, or the fragment does not hold
            whole frames.
        RuntimeError: If the interpreter no longer ships the ``audioop``
            module.
    """
    data = _require_bytes(fragment, "fragment")
    size = _require_width(width)
    _require_frames(data, size)
    _require_non_empty(data)
    module = _audioop_module()
    result: int = module.maxpp(data, size)
    return result


def count_zero_crossings(fragment: Any, width: int) -> int:
    """Return the number of times the samples of a fragment change sign.

    Args:
        fragment: The audio fragment.
        width: The width of a sample of *fragment* in bytes.

    Returns:
        The number of zero crossings of the fragment.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *width* is not a sample width the standard library
            understands, the fragment is empty, or the fragment does not hold
            whole frames.
        RuntimeError: If the interpreter no longer ships the ``audioop``
            module.
    """
    data = _require_bytes(fragment, "fragment")
    size = _require_width(width)
    _require_frames(data, size)
    _require_non_empty(data)
    module = _audioop_module()
    result: int = module.cross(data, size)
    return result


def find_scale_factor(fragment: Any, reference: Any) -> float:
    """Return the factor that fits a fragment to a reference best.

    The factor is the one that minimizes the root mean square of the sum of
    the fragment and the negated reference scaled by the factor.

    The standard library reads the two fragments as samples of sixteen bits, so
    both fragments have to hold an even number of bytes.

    Args:
        fragment: The audio fragment.
        reference: The reference audio fragment.

    Returns:
        The factor that fits the fragment to the reference best.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If the fragments hold a different number of bytes, or a
            fragment holds an odd number of bytes.
        RuntimeError: If the interpreter no longer ships the ``audioop``
            module.
    """
    data = _require_bytes(fragment, "fragment")
    other = _require_bytes(reference, "reference")
    if len(data) != len(other):
        raise ValueError(
            f"both fragments must have the same length, got {len(data)} and {len(other)}"
        )
    if len(data) % 2:
        raise ValueError(
            f"both fragments must hold a whole number of 16-bit samples, got {len(data)} bytes"
        )
    module = _audioop_module()
    result: float = module.findfactor(data, other)
    return result


def mix_to_mono(
    fragment: Any,
    width: int,
    left_factor: float = 1.0,
    right_factor: float = 1.0,
) -> bytes:
    """Return the mono form of a stereo fragment.

    Args:
        fragment: The stereo audio fragment.
        width: The width of a sample of *fragment* in bytes.
        left_factor: The factor the left channel is multiplied by.
        right_factor: The factor the right channel is multiplied by.

    Returns:
        The mono fragment.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *width* is not a sample width the standard library
            understands, the fragment does not hold whole frames, or the
            fragment does not hold an even number of frames.
        RuntimeError: If the interpreter no longer ships the ``audioop``
            module.
    """
    data = _require_bytes(fragment, "fragment")
    size = _require_width(width)
    left = _require_factor(left_factor, "left_factor")
    right = _require_factor(right_factor, "right_factor")
    _require_frames(data, size)
    module = _audioop_module()
    if (len(data) // size) % 2:
        raise ValueError("fragment must hold an even number of frames to be mixed down")
    result: bytes = module.tomono(data, size, left, right)
    return result


def duplicate_to_stereo(
    fragment: Any,
    width: int,
    left_factor: float = 1.0,
    right_factor: float = 1.0,
) -> bytes:
    """Return the stereo form of a mono fragment.

    Args:
        fragment: The mono audio fragment.
        width: The width of a sample of *fragment* in bytes.
        left_factor: The factor the left channel is multiplied by.
        right_factor: The factor the right channel is multiplied by.

    Returns:
        The stereo fragment.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *width* is not a sample width the standard library
            understands, or the fragment does not hold whole frames.
        RuntimeError: If the interpreter no longer ships the ``audioop``
            module.
    """
    data = _require_bytes(fragment, "fragment")
    size = _require_width(width)
    left = _require_factor(left_factor, "left_factor")
    right = _require_factor(right_factor, "right_factor")
    _require_frames(data, size)
    module = _audioop_module()
    result: bytes = module.tostereo(data, size, left, right)
    return result


def swap_byte_order(fragment: Any, width: int) -> bytes:
    """Return a fragment with the byte order of every sample reversed.

    Args:
        fragment: The audio fragment.
        width: The width of a sample of *fragment* in bytes.

    Returns:
        The fragment with the byte order of every sample reversed.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *width* is not a sample width the standard library
            understands, or the fragment does not hold whole frames.
        RuntimeError: If the interpreter no longer ships the ``audioop``
            module.
    """
    data = _require_bytes(fragment, "fragment")
    size = _require_width(width)
    _require_frames(data, size)
    module = _audioop_module()
    result: bytes = module.byteswap(data, size)
    return result


def reverse_samples(fragment: Any, width: int) -> bytes:
    """Return a fragment with its samples in reverse order.

    Args:
        fragment: The audio fragment.
        width: The width of a sample of *fragment* in bytes.

    Returns:
        The fragment with its samples in reverse order.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *width* is not a sample width the standard library
            understands, or the fragment does not hold whole frames.
        RuntimeError: If the interpreter no longer ships the ``audioop``
            module.
    """
    data = _require_bytes(fragment, "fragment")
    size = _require_width(width)
    _require_frames(data, size)
    module = _audioop_module()
    result: bytes = module.reverse(data, size)
    return result


def sample_at(fragment: Any, width: int, index: int) -> int:
    """Return the sample of a fragment at a position.

    A negative index counts from the end of the fragment, so ``-1`` is the
    last sample of the fragment.

    Args:
        fragment: The audio fragment.
        width: The width of a sample of *fragment* in bytes.
        index: The position of the sample.

    Returns:
        The sample at the position.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *width* is not a sample width the standard library
            understands, or the fragment does not hold whole frames.
        IndexError: If the position is outside the fragment.
        RuntimeError: If the interpreter no longer ships the ``audioop``
            module.
    """
    data = _require_bytes(fragment, "fragment")
    size = _require_width(width)
    position = _require_int(index, "index")
    _require_frames(data, size)
    module = _audioop_module()
    frames = len(data) // size
    if position < 0:
        position += frames
    if not 0 <= position < frames:
        raise IndexError(f"sample index {index} is out of range for {frames} frames")
    result: int = module.getsample(data, size, position)
    return result


def resample(
    fragment: Any,
    width: int,
    channels: int,
    input_rate: int,
    output_rate: int,
    state: Any = None,
) -> Tuple[bytes, Any]:
    """Return the resampled form of a fragment.

    The standard library resampler is stateful: it returns the state of the
    conversion next to the resampled fragment, and the state has to be handed
    back to the next call so that the conversion continues where it stopped.

    Args:
        fragment: The audio fragment.
        width: The width of a sample of *fragment* in bytes.
        channels: The number of channels of the fragment.
        input_rate: The frame rate of the fragment in frames per second.
        output_rate: The frame rate of the result in frames per second.
        state: The state of an earlier call.  The state of the first call is
            ``None``.

    Returns:
        The resampled fragment and the state of the conversion.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *width* is not a sample width the standard library
            understands, a rate is not greater than zero, the number of
            channels is not greater than zero, or the fragment does not hold
            whole frames.
        RuntimeError: If the interpreter no longer ships the ``audioop``
            module.
    """
    data = _require_bytes(fragment, "fragment")
    size = _require_width(width)
    channel_count = _require_positive_int(channels, "channels")
    source_rate = _require_positive_int(input_rate, "input_rate")
    target_rate = _require_positive_int(output_rate, "output_rate")
    _require_frames(data, size * channel_count)
    module = _audioop_module()
    result: Tuple[bytes, Any] = module.ratecv(
        data, size, channel_count, source_rate, target_rate, state
    )
    return result


def encode_adpcm(fragment: Any, width: int, state: Any = None, bits: int = 4) -> Tuple[bytes, Any]:
    """Return the ADPCM coded form of a fragment.

    Args:
        fragment: The audio fragment.
        width: The width of a sample of *fragment* in bytes.
        state: The state of an earlier call.  The state of the first call is
            ``None``.
        bits: The number of bits a coded sample occupies.  Only four bits are
            available on an interpreter that uses the stateful convention.

    Returns:
        The coded fragment and the state of the conversion.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *width* is not a sample width the standard library
            understands, the fragment does not hold whole frames, or the number
            of bits is not one the standard library understands.
        RuntimeError: If the interpreter no longer ships the ``audioop``
            module.
    """
    data = _require_bytes(fragment, "fragment")
    size = _require_width(width)
    bit_count = _require_int(bits, "bits")
    _require_frames(data, size)
    module = _audioop_module()
    if _adpcm_convention() == "stateful":
        if bit_count != 4:
            raise ValueError(f"bits must be 4 on this interpreter, got {bit_count}")
        result: Tuple[bytes, Any] = module.lin2adpcm(data, size, state)
        return result
    if bit_count not in (2, 3, 4, 5):
        raise ValueError(f"bits must be 2, 3, 4, or 5, got {bit_count}")
    coded: bytes = module.lin2adpcm(data, size, bit_count)
    return coded, None


def decode_adpcm(fragment: Any, width: int, state: Any = None, bits: int = 4) -> Tuple[bytes, Any]:
    """Return the linear form of an ADPCM coded fragment.

    Args:
        fragment: The ADPCM coded audio fragment.
        width: The width of a sample of the result in bytes.
        state: The state of an earlier call.  The state of the first call is
            ``None``.
        bits: The number of bits a coded sample occupies.  Only four bits are
            available on an interpreter that uses the stateful convention.

    Returns:
        The linear fragment and the state of the conversion.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *width* is not a sample width the standard library
            understands, the fragment does not hold whole frames, or the number
            of bits is not one the standard library understands.
        RuntimeError: If the interpreter no longer ships the ``audioop``
            module.
    """
    data = _require_bytes(fragment, "fragment")
    size = _require_width(width)
    bit_count = _require_int(bits, "bits")
    _require_frames(data, size)
    module = _audioop_module()
    if _adpcm_convention() == "stateful":
        if bit_count != 4:
            raise ValueError(f"bits must be 4 on this interpreter, got {bit_count}")
        result: Tuple[bytes, Any] = module.adpcm2lin(data, size, state)
        return result
    if bit_count not in (2, 3, 4, 5):
        raise ValueError(f"bits must be 2, 3, 4, or 5, got {bit_count}")
    decoded: bytes = module.adpcm2lin(data, size, bit_count)
    return decoded, None


def describe_fragment(fragment: Any, width: int) -> Dict[str, Any]:
    """Return a description of an audio fragment.

    The description holds the width of a sample, the number of frames, the
    smallest and the largest sample, the peak of the fragment, its peak to
    peak value, its average, its average peak to peak value, its root mean
    square, and the number of zero crossings.

    Args:
        fragment: The audio fragment.
        width: The width of a sample of *fragment* in bytes.

    Returns:
        A mapping that holds the measurements of the fragment.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If *width* is not a sample width the standard library
            understands, the fragment is empty, or the fragment does not hold
            whole frames.
        RuntimeError: If the interpreter no longer ships the ``audioop``
            module.
    """
    data = _require_bytes(fragment, "fragment")
    size = _require_width(width)
    _require_frames(data, size)
    _require_non_empty(data)
    module = _audioop_module()
    smallest, largest = module.minmax(data, size)
    return {
        "width": size,
        "frames": len(data) // size,
        "minimum": smallest,
        "maximum": largest,
        "peak": module.max(data, size),
        "peak_to_peak": module.maxpp(data, size),
        "average": average(data, size),
        "average_peak_to_peak": average_peak_to_peak(data, size),
        "root_mean_square": root_mean_square(data, size),
        "zero_crossings": module.cross(data, size),
    }


class Resampler:
    """Resample audio fragments and keep the state of the conversion.

    The standard library resampler returns the state of the conversion next to
    the resampled fragment, and the state has to be handed back to the next
    call so that the conversion continues where it stopped.  This class keeps
    the state, so a caller only hands over the fragments.

    Args:
        channels: The number of channels of the fragments.
        input_rate: The frame rate of the fragments in frames per second.
        output_rate: The frame rate of the results in frames per second.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If a rate is not greater than zero, or the number of
            channels is not greater than zero.
    """

    def __init__(self, channels: int, input_rate: int, output_rate: int) -> None:
        self._channels = _require_positive_int(channels, "channels")
        self._input_rate = _require_positive_int(input_rate, "input_rate")
        self._output_rate = _require_positive_int(output_rate, "output_rate")
        self._state: Any = None

    @property
    def channels(self) -> int:
        """Return the number of channels of the fragments."""
        return self._channels

    @property
    def input_rate(self) -> int:
        """Return the frame rate of the fragments."""
        return self._input_rate

    @property
    def output_rate(self) -> int:
        """Return the frame rate of the results."""
        return self._output_rate

    @property
    def state(self) -> Any:
        """Return the state of the conversion."""
        return self._state

    def reset(self) -> None:
        """Forget the state of the conversion."""
        self._state = None

    def resample(self, fragment: Any, width: int) -> bytes:
        """Return the resampled form of a fragment.

        Args:
            fragment: The audio fragment.
            width: The width of a sample of *fragment* in bytes.

        Returns:
            The resampled fragment.

        Raises:
            TypeError: If an argument has the wrong type.
            ValueError: If *width* is not a sample width the standard library
                understands, or the fragment does not hold whole frames.
            RuntimeError: If the interpreter no longer ships the ``audioop``
                module.
        """
        data, self._state = resample(
            fragment,
            width,
            self._channels,
            self._input_rate,
            self._output_rate,
            self._state,
        )
        return data
