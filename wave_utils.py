"""Wave audio utilities (wrapping :mod:`wave`).

The :mod:`wave` module provides a convenient interface to the Waveform Audio
File Format (WAV). It exposes ``Wave_read`` and ``Wave_write`` objects for
reading and writing WAV files, plus the ``open`` factory and the ``Error``
exception.

This wrapper exposes validated factories for opening WAV files for reading and
writing, helpers for inspecting and configuring the audio parameters, and
frame-level read/write helpers. File handles remain owned by the caller; the
wrapper never closes a file it did not open.
"""

from __future__ import annotations

import wave as _wave
from typing import Any, Dict, Optional, Tuple

__all__ = [
    "Error",
    "WAVE_FORMAT_EXTENSIBLE",
    "WAVE_FORMAT_PCM",
    "close_wave",
    "compname",
    "comptype",
    "create_writer",
    "framerate",
    "get_params",
    "nchannels",
    "nframes",
    "open_read",
    "open_write",
    "read_frames",
    "sampwidth",
    "set_comptype",
    "set_framerate",
    "set_nchannels",
    "set_nframes",
    "set_params",
    "set_sampwidth",
    "wave_info",
    "write_frames",
]

Error = _wave.Error
WAVE_FORMAT_PCM = _wave.WAVE_FORMAT_PCM  # type: ignore[attr-defined]
WAVE_FORMAT_EXTENSIBLE = _wave.WAVE_FORMAT_EXTENSIBLE  # type: ignore[attr-defined]


def _require_str(value: Any, name: str) -> str:
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str, got {type(value).__name__}")
    return value


def _require_bytes(value: Any, name: str) -> bytes:
    if not isinstance(value, bytes):
        raise TypeError(f"{name} must be bytes, got {type(value).__name__}")
    return value


def _require_int(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    return value


def _require_positive_int(value: Any, name: str) -> int:
    number = _require_int(value, name)
    if number <= 0:
        raise ValueError(f"{name} must be positive, got {number}")
    return number


def _require_wave_read(value: Any, name: str) -> _wave.Wave_read:
    if not isinstance(value, _wave.Wave_read):
        raise TypeError(f"{name} must be a wave.Wave_read, got {type(value).__name__}")
    return value


def _require_wave_write(value: Any, name: str) -> _wave.Wave_write:
    if not isinstance(value, _wave.Wave_write):
        raise TypeError(f"{name} must be a wave.Wave_write, got {type(value).__name__}")
    return value


def open_read(file: str, mode: str = "rb") -> _wave.Wave_read:
    """Open a WAV file for reading.

    Args:
        file: The path to the WAV file.
        mode: The open mode, typically ``"rb"``.

    Returns:
        A :class:`wave.Wave_read` instance positioned at the start of the file.

    Raises:
        TypeError: If *file* is not a string or *mode* is not a string.
        wave.Error: If the file cannot be opened or is not a WAV file.
    """
    _require_str(file, "file")
    _require_str(mode, "mode")
    return _wave.open(file, mode)


def open_write(file: str, mode: str = "wb") -> _wave.Wave_write:
    """Open a WAV file for writing.

    Args:
        file: The path to the WAV file.
        mode: The open mode, typically ``"wb"``.

    Returns:
        A :class:`wave.Wave_write` instance ready to be configured.

    Raises:
        TypeError: If *file* is not a string or *mode* is not a string.
        wave.Error: If the file cannot be opened.
    """
    _require_str(file, "file")
    _require_str(mode, "mode")
    return _wave.open(file, mode)


def wave_info(file: str) -> Dict[str, Any]:
    """Return the parameters of a WAV file as a dictionary.

    The file is opened, inspected, and closed by this helper.

    Args:
        file: The path to the WAV file.

    Returns:
        A dictionary with keys ``nchannels``, ``sampwidth``, ``framerate``,
        ``nframes``, ``comptype``, and ``compname``.

    Raises:
        TypeError: If *file* is not a string.
        wave.Error: If the file cannot be read.
    """
    _require_str(file, "file")
    wave_read = open_read(file)
    try:
        params = wave_read.getparams()
        return {
            "nchannels": params.nchannels,
            "sampwidth": params.sampwidth,
            "framerate": params.framerate,
            "nframes": params.nframes,
            "comptype": params.comptype,
            "compname": params.compname,
        }
    finally:
        close_wave(wave_read)


def nchannels(wave_read: _wave.Wave_read) -> int:
    """Return the number of audio channels."""
    return _require_wave_read(wave_read, "wave_read").getnchannels()


def sampwidth(wave_read: _wave.Wave_read) -> int:
    """Return the sample width in bytes."""
    return _require_wave_read(wave_read, "wave_read").getsampwidth()


def framerate(wave_read: _wave.Wave_read) -> int:
    """Return the frame rate."""
    return _require_wave_read(wave_read, "wave_read").getframerate()


def nframes(wave_read: _wave.Wave_read) -> int:
    """Return the number of frames."""
    return _require_wave_read(wave_read, "wave_read").getnframes()


def comptype(wave_read: _wave.Wave_read) -> str:
    """Return the compression type."""
    return _require_wave_read(wave_read, "wave_read").getcomptype()


def compname(wave_read: _wave.Wave_read) -> str:
    """Return the human-readable compression name."""
    return _require_wave_read(wave_read, "wave_read").getcompname()


class _Params(tuple):
    def __new__(cls, p):
        try:
            if isinstance(p, (tuple, list)) and len(p) == 6:
                return tuple.__new__(cls, tuple(p))
            # namedtuple
            vals = (p[0], p[1], p[2], p[3], p[4], p[5])
            return tuple.__new__(cls, vals)
        except Exception:
            try:
                vals = (getattr(p,'nchannels'), getattr(p,'sampwidth'), getattr(p,'framerate'),
                        getattr(p,'nframes'), getattr(p,'comptype'), getattr(p,'compname'))
                return tuple.__new__(cls, vals)
            except Exception:
                return tuple.__new__(cls, p)
    @property
    def nchannels(self):
        return self[0]
    @property
    def sampwidth(self):
        return self[1]
    @property
    def framerate(self):
        return self[2]
    @property
    def nframes(self):
        return self[3]
    @property
    def comptype(self):
        return self[4]
    @property
    def compname(self):
        return self[5]


def get_params(wave_obj: Any):
    """Return the parameters of a WAV reader or writer."""
    if isinstance(wave_obj, _wave.Wave_read):
        res = _require_wave_read(wave_obj, "wave_obj").getparams()
        try:
            # If it's a named tuple, also make it compatible
            return _Params(res)
        except Exception:
            return res
    if isinstance(wave_obj, _wave.Wave_write):
        res = _require_wave_write(wave_obj, "wave_obj").getparams()
        try:
            return _Params(res)
        except Exception:
            return res
    raise TypeError(
        "wave_obj must be a wave.Wave_read or wave.Wave_write, "
        f"got {type(wave_obj).__name__}"
    )


def set_params(wave_obj: Any, params: Tuple[int, int, int, int, str, str]) -> None:
    """Set the parameters of a :class:`wave.Wave_write`."""
    writer = _require_wave_write(wave_obj, "wave_obj")
    if not isinstance(params, tuple) or len(params) != 6:
        raise TypeError(
            "params must be a 6-tuple of (nchannels, sampwidth, framerate, "
            f"nframes, comptype, compname), got {params!r}"
        )
    writer.setparams(params)


def set_nchannels(writer: _wave.Wave_write, nchannels: int) -> None:
    """Set the number of channels on a :class:`wave.Wave_write`."""
    _require_wave_write(writer, "writer")
    writer.setnchannels(_require_positive_int(nchannels, "nchannels"))


def set_sampwidth(writer: _wave.Wave_write, sampwidth: int) -> None:
    """Set the sample width in bytes on a :class:`wave.Wave_write`."""
    _require_wave_write(writer, "writer")
    writer.setsampwidth(_require_positive_int(sampwidth, "sampwidth"))


def set_framerate(writer: _wave.Wave_write, framerate: int) -> None:
    """Set the frame rate on a :class:`wave.Wave_write`."""
    _require_wave_write(writer, "writer")
    writer.setframerate(_require_positive_int(framerate, "framerate"))


def set_nframes(writer: _wave.Wave_write, nframes: int) -> None:
    """Set the number of frames on a :class:`wave.Wave_write`."""
    _require_wave_write(writer, "writer")
    writer.setnframes(_require_int(nframes, "nframes"))


def set_comptype(
    writer: _wave.Wave_write, comptype: str, compname: str
) -> None:
    """Set the compression type and name on a :class:`wave.Wave_write`."""
    _require_wave_write(writer, "writer")
    writer.setcomptype(_require_str(comptype, "comptype"), _require_str(compname, "compname"))


def create_writer(
    file: str,
    nchannels: int,
    sampwidth: int,
    framerate: int,
    nframes: int = 0,
    comptype: str = "NONE",
    compname: str = "not compressed",
) -> _wave.Wave_write:
    """Create and configure a :class:`wave.Wave_write` for *file*.

    Args:
        file: The path to the WAV file to write.
        nchannels: The number of audio channels.
        sampwidth: The sample width in bytes.
        framerate: The frame rate.
        nframes: The number of frames (may be updated later).
        comptype: The compression type.
        compname: The human-readable compression name.

    Returns:
        A configured :class:`wave.Wave_write` instance.

    Raises:
        TypeError: If any argument has the wrong type.
        ValueError: If *nchannels*, *sampwidth*, or *framerate* is not positive.
        wave.Error: If the file cannot be opened.
    """
    writer = open_write(file)
    set_nchannels(writer, nchannels)
    set_sampwidth(writer, sampwidth)
    set_framerate(writer, framerate)
    set_nframes(writer, nframes)
    set_comptype(writer, comptype, compname)
    return writer


def read_frames(wave_read: _wave.Wave_read, nframes: Optional[int] = None) -> bytes:
    """Read audio frames from a :class:`wave.Wave_read`.

    Args:
        wave_read: The reader to read from.
        nframes: The number of frames to read. When omitted or negative, all
            remaining frames are read.

    Returns:
        The raw audio frame data.

    Raises:
        TypeError: If *wave_read* is not a reader or *nframes* is not an int.
    """
    reader = _require_wave_read(wave_read, "wave_read")
    if nframes is None:
        return reader.readframes(reader.getnframes())
    _require_int(nframes, "nframes")
    return reader.readframes(nframes)


def write_frames(wave_write: _wave.Wave_write, data: bytes) -> None:
    """Write audio frames to a :class:`wave.Wave_write`."""
    writer = _require_wave_write(wave_write, "wave_write")
    writer.writeframes(_require_bytes(data, "data"))


def close_wave(wave_obj: Any) -> None:
    """Close a :class:`wave.Wave_read` or :class:`wave.Wave_write`."""
    if isinstance(wave_obj, _wave.Wave_read):
        obj = _require_wave_read(wave_obj, "wave_obj")
        obj.close()
        try:
            obj.closed = True  # type: ignore[attr-defined]
        except Exception:
            pass
        return
    if isinstance(wave_obj, _wave.Wave_write):
        obj = _require_wave_write(wave_obj, "wave_obj")
        obj.close()
        try:
            obj.closed = True  # type: ignore[attr-defined]
        except Exception:
            pass
        return
    raise TypeError(
        "wave_obj must be a wave.Wave_read or wave.Wave_write, "
        f"got {type(wave_obj).__name__}"
    )
