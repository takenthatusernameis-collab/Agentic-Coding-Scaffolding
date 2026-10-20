"""Terminal attribute utilities wrapping the standard library :mod:`termios` module.

The :mod:`termios` module controls a terminal of a Unix-like operating system.
A program reads the attributes of a terminal with :func:`termios.tcgetattr`,
writes them back with :func:`termios.tcsetattr`, and flushes, drains, or
interrupts the output queue of the terminal with :func:`termios.tcflush`,
:func:`termios.tcdrain`, and :func:`termios.tcflow`.

This wrapper validates every argument before the standard library is reached,
so a caller gets a clear :class:`TypeError` or :class:`ValueError` instead of
an opaque failure from the C layer.  It returns the attributes of a terminal
as an :class:`Attributes` named tuple with stable field names, and it adds
helpers that build a raw or a cbreak configuration, that configure the read
timeout of a terminal, and that read and write the size of the window.

.. note::

   The :mod:`termios` module only exists on Unix-like platforms.  The import
   below degrades gracefully: when the interpreter does not ship the module,
   the helpers that talk to the operating system raise a :class:`RuntimeError`
   that names the missing module, while the pure helpers keep working.

The helpers never change the attributes of a terminal on their own.  The
attributes are only written when the caller asks for it with
:func:`set_attributes`.
"""

from __future__ import annotations

import math
import os
import struct
from typing import Any, Dict, List, NamedTuple, Sequence

try:
    import termios as _termios
except ImportError:  # pragma: no cover - the module is Unix-only
    _termios = None  # type: ignore[assignment]

try:
    import tty as _tty
except ImportError:  # pragma: no cover - the module is Unix-only
    _tty = None  # type: ignore[assignment]

try:
    import fcntl as _fcntl
except ImportError:  # pragma: no cover - the module is Unix-only
    _fcntl = None  # type: ignore[assignment]


class Attributes(NamedTuple):
    """The attributes of a terminal.

    The standard library returns a list of seven values whose meaning depends
    on the platform.  This named tuple always has the same fields.

    Attributes:
        iflag: The input modes of the terminal.
        oflag: The output modes of the terminal.
        cflag: The control modes of the terminal.
        lflag: The local modes of the terminal.
        ispeed: The input speed of the terminal.
        ospeed: The output speed of the terminal.
        cc: The control characters of the terminal, one entry per slot.
    """

    iflag: int
    oflag: int
    cflag: int
    lflag: int
    ispeed: int
    ospeed: int
    cc: List[int]


class WindowSize(NamedTuple):
    """The size of the window of a terminal.

    Attributes:
        rows: The number of rows of the window.
        columns: The number of columns of the window.
        x_pixels: The width of the window in pixels, or zero when unknown.
        y_pixels: The height of the window in pixels, or zero when unknown.
    """

    rows: int
    columns: int
    x_pixels: int
    y_pixels: int


__all__: list[str] = [
    "Attributes",
    "ECHO",
    "ISIG",
    "TCIFLUSH",
    "TCIOFF",
    "TCION",
    "TCOFLUSH",
    "TCSADRAIN",
    "TCSAFLUSH",
    "TCSANOW",
    "VDISCARD",
    "VEOF",
    "VEOL",
    "VEOL2",
    "VERASE",
    "VINTR",
    "VKILL",
    "VLNEXT",
    "VMIN",
    "VQUIT",
    "VREPRINT",
    "VSTART",
    "VSTOP",
    "VSUSP",
    "VSWTC",
    "VTIME",
    "VWERASE",
    "WindowSize",
    "baud_rates",
    "control_character_names",
    "drain",
    "flush",
    "get_attributes",
    "get_window_size",
    "is_available",
    "make_cbreak",
    "make_raw",
    "pause_output",
    "resume_output",
    "send_break",
    "set_attributes",
    "set_blocking",
    "set_read_timeout",
    "set_window_size",
]


def _constant(name: str, fallback: int) -> int:
    """Return the standard library constant *name*, or *fallback*.

    Args:
        name: The name of the constant in the standard library module.
        fallback: The value to use when the interpreter does not provide the
            constant.

    Returns:
        The value of the constant.
    """
    if _termios is None:
        return fallback
    value = getattr(_termios, name, fallback)
    return value if isinstance(value, int) else fallback


#: Apply the change immediately.
TCSANOW: int = _constant("TCSANOW", 0)
#: Apply the change after the output of the terminal has been transmitted.
TCSADRAIN: int = _constant("TCSADRAIN", 1)
#: Apply the change after the output of the terminal has been transmitted
#: and discard the output that is still queued.
TCSAFLUSH: int = _constant("TCSAFLUSH", 2)
#: Discard the data that has been received but not read yet.
TCIFLUSH: int = _constant("TCIFLUSH", 0)
#: Discard the data that has been written but not transmitted yet.
TCOFLUSH: int = _constant("TCOFLUSH", 1)
#: Suspend the output of the terminal.
TCIOFF: int = _constant("TCIOFF", 0)
#: Resume the output of the terminal.
TCION: int = _constant("TCION", 1)

#: The local mode that echoes the typed characters.
ECHO: int = _constant("ECHO", 0o10)
#: The local mode that interprets the signal characters.
ISIG: int = _constant("ISIG", 0o1)
#: The slot of the character that interrupts the program.
VINTR: int = _constant("VINTR", 0)
#: The slot of the character that quits the program.
VQUIT: int = _constant("VQUIT", 1)
#: The slot of the character that erases the last character.
VERASE: int = _constant("VERASE", 2)
#: The slot of the character that erases the whole line.
VKILL: int = _constant("VKILL", 3)
#: The slot of the character that ends the input.
VEOF: int = _constant("VEOF", 4)
#: The slot of the read timeout of the terminal.
VTIME: int = _constant("VTIME", 5)
#: The slot of the minimum number of bytes a read waits for.
VMIN: int = _constant("VMIN", 6)
#: The slot of the character that switches the terminal.
VSWTC: int = _constant("VSWTC", 7)
#: The slot of the character that starts the output.
VSTART: int = _constant("VSTART", 8)
#: The slot of the character that stops the output.
VSTOP: int = _constant("VSTOP", 9)
#: The slot of the character that suspends the program.
VSUSP: int = _constant("VSUSP", 10)
#: The slot of the additional end of line character.
VEOL: int = _constant("VEOL", 11)
#: The slot of the character that redraws the line.
VREPRINT: int = _constant("VREPRINT", 12)
#: The slot of the character that discards the typed characters.
VDISCARD: int = _constant("VDISCARD", 13)
#: The slot of the character that erases the whole line.
VWERASE: int = _constant("VWERASE", 14)
#: The slot of the character of the next line.
VLNEXT: int = _constant("VLNEXT", 15)
#: The slot of the second additional end of line character.
VEOL2: int = _constant("VEOL2", 16)

#: The names of the control characters, in the order of their slots.
_CONTROL_CHARACTERS: tuple[tuple[str, int], ...] = (
    ("VINTR", VINTR),
    ("VQUIT", VQUIT),
    ("VERASE", VERASE),
    ("VKILL", VKILL),
    ("VEOF", VEOF),
    ("VTIME", VTIME),
    ("VMIN", VMIN),
    ("VSWTC", VSWTC),
    ("VSTART", VSTART),
    ("VSTOP", VSTOP),
    ("VSUSP", VSUSP),
    ("VEOL", VEOL),
    ("VREPRINT", VREPRINT),
    ("VDISCARD", VDISCARD),
    ("VWERASE", VWERASE),
    ("VLNEXT", VLNEXT),
    ("VEOL2", VEOL2),
)

#: The names of the standard baud rates.
_BAUD_NAMES: tuple[str, ...] = (
    "B0",
    "B50",
    "B75",
    "B110",
    "B134",
    "B150",
    "B200",
    "B300",
    "B600",
    "B1200",
    "B1800",
    "B2400",
    "B4800",
    "B9600",
    "B19200",
    "B38400",
    "B57600",
    "B115200",
    "B230400",
    "B460800",
    "B500000",
    "B576000",
    "B921600",
    "B1000000",
    "B1152000",
    "B1500000",
    "B2000000",
    "B2500000",
    "B3000000",
    "B3500000",
    "B4000000",
)


def _termios_module() -> Any:
    """Return the standard library ``termios`` module.

    Raises:
        RuntimeError: If the interpreter does not ship the ``termios`` module.
    """
    if _termios is None:
        raise RuntimeError("the standard library module 'termios' is not available")
    return _termios


def _tty_module() -> Any:
    """Return the standard library ``tty`` module.

    Raises:
        RuntimeError: If the interpreter does not ship the ``tty`` module.
    """
    if _tty is None:
        raise RuntimeError("the standard library module 'tty' is not available")
    return _tty


def is_available() -> bool:
    """Return ``True`` if the ``termios`` module is available."""
    return _termios is not None


def _validate_fd(fd: int) -> int:
    """Return *fd* when it is a valid file descriptor.

    Args:
        fd: The file descriptor to validate.

    Returns:
        The validated file descriptor.

    Raises:
        TypeError: If *fd* is not an int.
        ValueError: If *fd* is negative.
    """
    if isinstance(fd, bool) or not isinstance(fd, int):
        raise TypeError(f"fd must be an int, got {type(fd).__name__}")
    if fd < 0:
        raise ValueError(f"fd must not be negative, got {fd}")
    return fd


def _validate_attributes(attributes: Attributes) -> Attributes:
    """Return *attributes* when it holds usable terminal attributes.

    Args:
        attributes: The attributes to validate.

    Returns:
        The validated attributes.

    Raises:
        TypeError: If *attributes* is not an :class:`Attributes` instance.
        ValueError: If a mode of the attributes is negative.
    """
    if not isinstance(attributes, Attributes):
        raise TypeError(
            f"attributes must be an Attributes instance, got {type(attributes).__name__}"
        )
    for name in ("iflag", "oflag", "cflag", "lflag", "ispeed", "ospeed"):
        value = getattr(attributes, name)
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"the {name} of the attributes must be an int")
        if value < 0:
            raise ValueError(f"the {name} of the attributes must not be negative, got {value}")
    if not isinstance(attributes.cc, (list, tuple)):
        raise TypeError("the cc of the attributes must be a list of ints")
    for value in attributes.cc:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError("the cc of the attributes must be a list of ints")
        if not 0 <= value <= 255:
            raise ValueError(f"the cc of the attributes must hold bytes, got {value}")
    return attributes


def _attributes_to_mode(attributes: Attributes) -> List[Any]:
    """Return the mode list the standard library expects."""
    return [
        attributes.iflag,
        attributes.oflag,
        attributes.cflag,
        attributes.lflag,
        attributes.ispeed,
        attributes.ospeed,
        _control_characters_to_bytes(attributes.cc),
    ]


def _control_characters_to_bytes(characters: Sequence[int]) -> List[bytes]:
    """Return the control characters as the byte objects the standard library expects.

    The standard library reports one byte object per control character and
    expects one byte object per control character as well, so the list is
    padded to the number of slots the platform provides.
    """
    count = max(len(characters), VEOL2 + 1)
    if _termios is not None:
        count = max(count, int(getattr(_termios, "NCCS", count)))
    values = list(characters[:count])
    while len(values) < count:
        values.append(0)
    return [bytes([value]) for value in values]


def _mode_to_attributes(mode: Sequence[Any]) -> Attributes:
    """Return the attributes of a mode list of the standard library."""
    return Attributes(
        iflag=int(mode[0]),
        oflag=int(mode[1]),
        cflag=int(mode[2]),
        lflag=int(mode[3]),
        ispeed=int(mode[4]),
        ospeed=int(mode[5]),
        cc=[
            value[0] if isinstance(value, (bytes, bytearray)) else int(value)
            for value in mode[6]
        ],
    )


def _with_control_characters(
    attributes: Attributes,
    changes: Dict[int, int],
) -> Attributes:
    """Return the attributes with the given control characters replaced."""
    characters: List[int] = list(attributes.cc)
    for index, value in changes.items():
        while len(characters) <= index:
            characters.append(0)
        characters[index] = value
    return attributes._replace(cc=characters)


def get_attributes(fd: int) -> Attributes:
    """Return the attributes of the terminal behind *fd*.

    Args:
        fd: The file descriptor of the terminal.

    Returns:
        The :class:`Attributes` of the terminal.

    Raises:
        TypeError: If *fd* is not an int.
        ValueError: If *fd* is negative.
        RuntimeError: If the interpreter does not ship the ``termios`` module.
        termios.error: If the file descriptor is not a terminal.
    """
    _validate_fd(fd)
    module = _termios_module()
    return _mode_to_attributes(module.tcgetattr(fd))


def set_attributes(fd: int, attributes: Attributes, when: int = TCSANOW) -> None:
    """Write *attributes* to the terminal behind *fd*.

    Args:
        fd: The file descriptor of the terminal.
        attributes: The attributes to write.
        when: When the change is applied.  One of :data:`TCSANOW`,
            :data:`TCSADRAIN`, or :data:`TCSAFLUSH`.

    Raises:
        TypeError: If *fd*, *attributes*, or *when* has the wrong type.
        ValueError: If *fd* is negative or *when* is not a known moment.
        RuntimeError: If the interpreter does not ship the ``termios`` module.
        termios.error: If the file descriptor is not a terminal.
    """
    _validate_fd(fd)
    _validate_attributes(attributes)
    if isinstance(when, bool) or not isinstance(when, int):
        raise TypeError(f"when must be an int, got {type(when).__name__}")
    if when not in (TCSANOW, TCSADRAIN, TCSAFLUSH):
        raise ValueError(
            f"when must be TCSANOW, TCSADRAIN, or TCSAFLUSH, got {when}"
        )
    module = _termios_module()
    module.tcsetattr(fd, when, _attributes_to_mode(attributes))


def make_raw(attributes: Attributes) -> Attributes:
    """Return the raw configuration of *attributes*.

    A raw terminal does not echo the typed characters, does not translate the
    line endings, and does not interpret the control characters.

    Args:
        attributes: The attributes to build the raw configuration from.

    Returns:
        The raw :class:`Attributes`.

    Raises:
        TypeError: If *attributes* has the wrong type.
        ValueError: If a mode of the attributes is negative.
        RuntimeError: If the interpreter does not ship the ``tty`` module.
    """
    _validate_attributes(attributes)
    module = _tty_module()
    mode = _attributes_to_mode(attributes)
    module.cfmakeraw(mode)
    return _mode_to_attributes(mode)


def make_cbreak(attributes: Attributes) -> Attributes:
    """Return the cbreak configuration of *attributes*.

    A cbreak terminal does not echo the typed characters, but it still
    interprets the control characters line by line.

    Args:
        attributes: The attributes to build the cbreak configuration from.

    Returns:
        The cbreak :class:`Attributes`.

    Raises:
        TypeError: If *attributes* has the wrong type.
        ValueError: If a mode of the attributes is negative.
        RuntimeError: If the interpreter does not ship the ``tty`` module or
            if it does not provide ``cfmakecbreak``.
    """
    _validate_attributes(attributes)
    module = _tty_module()
    maker = getattr(module, "cfmakecbreak", None)
    if maker is None:
        raise RuntimeError(
            "the standard library module 'tty' does not provide cfmakecbreak"
        )
    mode = _attributes_to_mode(attributes)
    maker(mode)
    return _mode_to_attributes(mode)


def set_read_timeout(attributes: Attributes, timeout: float) -> Attributes:
    """Return the attributes that read with a timeout of *timeout* seconds.

    A read waits at most *timeout* seconds for the data to arrive, and it
    returns an empty result when the timeout expires.

    Args:
        attributes: The attributes to build the configuration from.
        timeout: The timeout of a read in seconds.

    Returns:
        The :class:`Attributes` with the new timeout.

    Raises:
        TypeError: If *attributes* or *timeout* has the wrong type.
        ValueError: If the timeout is negative or not a finite number.
    """
    _validate_attributes(attributes)
    if isinstance(timeout, bool) or not isinstance(timeout, (int, float)):
        raise TypeError(f"timeout must be a number, got {type(timeout).__name__}")
    if math.isnan(timeout) or math.isinf(timeout):
        raise ValueError(f"timeout must be a finite number, got {timeout}")
    if timeout < 0:
        raise ValueError(f"timeout must not be negative, got {timeout}")
    tenths = int(math.ceil(timeout * 10))
    return _with_control_characters(attributes, {VMIN: 0, VTIME: tenths})


def set_blocking(attributes: Attributes) -> Attributes:
    """Return the attributes that read in blocking mode.

    Args:
        attributes: The attributes to build the configuration from.

    Returns:
        The :class:`Attributes` that wait for at least one byte.

    Raises:
        TypeError: If *attributes* has the wrong type.
        ValueError: If a mode of the attributes is negative.
    """
    _validate_attributes(attributes)
    return _with_control_characters(attributes, {VMIN: 1, VTIME: 0})


def get_window_size(fd: int) -> WindowSize:
    """Return the size of the window of the terminal behind *fd*.

    Args:
        fd: The file descriptor of the terminal.

    Returns:
        The :class:`WindowSize` of the terminal.

    Raises:
        TypeError: If *fd* is not an int.
        ValueError: If *fd* is negative.
        OSError: If the file descriptor is not a terminal.
    """
    _validate_fd(fd)
    size = os.get_terminal_size(fd)
    return WindowSize(
        rows=int(size.lines),
        columns=int(size.columns),
        x_pixels=0,
        y_pixels=0,
    )


def set_window_size(
    fd: int,
    rows: int,
    columns: int,
    x_pixels: int = 0,
    y_pixels: int = 0,
) -> None:
    """Set the size of the window of the terminal behind *fd*.

    Args:
        fd: The file descriptor of the terminal.
        rows: The number of rows of the window.
        columns: The number of columns of the window.
        x_pixels: The width of the window in pixels.
        y_pixels: The height of the window in pixels.

    Raises:
        TypeError: If an argument has the wrong type.
        ValueError: If a size is negative.
        RuntimeError: If the interpreter does not ship the ``termios`` or the
            ``fcntl`` module, or if the platform does not provide
            ``TIOCSWINSZ``.
        OSError: If the file descriptor is not a terminal.
    """
    _validate_fd(fd)
    for name, value in (
        ("rows", rows),
        ("columns", columns),
        ("x_pixels", x_pixels),
        ("y_pixels", y_pixels),
    ):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be an int, got {type(value).__name__}")
        if value < 0:
            raise ValueError(f"{name} must not be negative, got {value}")
    module = _termios_module()
    request = getattr(module, "TIOCSWINSZ", None)
    if request is None:
        raise RuntimeError(
            "the standard library module 'termios' does not provide TIOCSWINSZ"
        )
    if _fcntl is None:
        raise RuntimeError("the standard library module 'fcntl' is not available")
    _fcntl.ioctl(fd, request, struct.pack("HHHH", rows, columns, x_pixels, y_pixels))


def drain(fd: int) -> None:
    """Wait until everything that was written to the terminal was transmitted.

    Args:
        fd: The file descriptor of the terminal.

    Raises:
        TypeError: If *fd* is not an int.
        ValueError: If *fd* is negative.
        RuntimeError: If the interpreter does not ship the ``termios`` module.
        termios.error: If the file descriptor is not a terminal.
    """
    _validate_fd(fd)
    module = _termios_module()
    module.tcdrain(fd)


def flush(fd: int, queue: int = TCIFLUSH) -> None:
    """Discard the data that the terminal has not processed yet.

    Args:
        fd: The file descriptor of the terminal.
        queue: The queue to discard.  :data:`TCIFLUSH` discards the data
            that has been received but not read yet, and :data:`TCOFLUSH`
            discards the data that has been written but not transmitted yet.

    Raises:
        TypeError: If *fd* or *queue* has the wrong type.
        ValueError: If *fd* is negative or *queue* is not a known queue.
        RuntimeError: If the interpreter does not ship the ``termios`` module.
        termios.error: If the file descriptor is not a terminal.
    """
    _validate_fd(fd)
    if isinstance(queue, bool) or not isinstance(queue, int):
        raise TypeError(f"queue must be an int, got {type(queue).__name__}")
    if queue not in (TCIFLUSH, TCOFLUSH):
        raise ValueError(f"queue must be TCIFLUSH or TCOFLUSH, got {queue}")
    module = _termios_module()
    module.tcflush(fd, queue)


def pause_output(fd: int) -> None:
    """Suspend the output of the terminal.

    Args:
        fd: The file descriptor of the terminal.

    Raises:
        TypeError: If *fd* is not an int.
        ValueError: If *fd* is negative.
        RuntimeError: If the interpreter does not ship the ``termios`` module.
        termios.error: If the file descriptor is not a terminal.
    """
    _validate_fd(fd)
    module = _termios_module()
    module.tcflow(fd, TCIOFF)


def resume_output(fd: int) -> None:
    """Resume the output of the terminal.

    Args:
        fd: The file descriptor of the terminal.

    Raises:
        TypeError: If *fd* is not an int.
        ValueError: If *fd* is negative.
        RuntimeError: If the interpreter does not ship the ``termios`` module.
        termios.error: If the file descriptor is not a terminal.
    """
    _validate_fd(fd)
    module = _termios_module()
    module.tcflow(fd, TCION)


def send_break(fd: int, duration: int = 0) -> None:
    """Send a break to the terminal.

    Args:
        fd: The file descriptor of the terminal.
        duration: The duration of the break in tenths of a second.  A duration
            of zero sends a break that lasts at least a fraction of a second.

    Raises:
        TypeError: If *fd* or *duration* has the wrong type.
        ValueError: If *fd* or *duration* is negative.
        RuntimeError: If the interpreter does not ship the ``termios`` module.
        termios.error: If the file descriptor is not a terminal.
    """
    _validate_fd(fd)
    if isinstance(duration, bool) or not isinstance(duration, int):
        raise TypeError(f"duration must be an int, got {type(duration).__name__}")
    if duration < 0:
        raise ValueError(f"duration must not be negative, got {duration}")
    module = _termios_module()
    module.tcsendbreak(fd, duration)


def control_character_names() -> Dict[int, str]:
    """Return the names of the control characters, keyed by their slot.

    Returns:
        A dictionary that maps the slot of a control character to its name,
        such as ``0`` to ``"VINTR"``.
    """
    return {index: name for name, index in _CONTROL_CHARACTERS}


def baud_rates() -> Dict[str, int]:
    """Return the standard baud rates, keyed by their name.

    Returns:
        A dictionary that maps the name of a baud rate to the number of bits
        per second, such as ``"B9600"`` to ``9600``.
    """
    return {name: int(name[1:]) for name in _BAUD_NAMES}
