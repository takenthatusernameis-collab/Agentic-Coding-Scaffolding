"""Terminal handling utilities wrapping the standard library :mod:`curses` module.

The :mod:`curses` module controls a text terminal: it initializes the screen,
changes the input mode of the terminal, paints text on windows, refreshes the
display, and handles colors and special keys.

This wrapper validates every argument before the standard library is reached, so
a caller gets a clear :class:`TypeError` or :class:`ValueError` instead of an
opaque failure from the C layer. It re-exports the constants and the functions
of :mod:`curses`, and it adds the helper :func:`is_available`, which reports
whether the interpreter ships the module.

.. note::

   The :mod:`curses` module only exists on Unix-like platforms.  The import
   below degrades gracefully: when the interpreter does not ship the module, the
   helpers raise a :class:`RuntimeError` that names the missing module, while the
   pure helpers keep working.
"""

from __future__ import annotations

from typing import Any, List, Optional, Tuple, Union, cast

try:
    import curses as _curses
except ImportError:  # pragma: no cover - the module is Unix-only
    _curses = None  # type: ignore[assignment]


def _curses_module() -> Any:
    """Return the standard library ``curses`` module.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    if _curses is None:
        raise RuntimeError("the standard library module 'curses' is not available")
    return _curses


def is_available() -> bool:
    """Return ``True`` if the ``curses`` module is available."""
    return _curses is not None


#: The window class of the standard library.
Window: Any = _curses.window if _curses is not None else Any  # type: ignore[assignment]

#: The result of an operation that failed.
ERR: int = _curses.ERR if _curses is not None else -1  # type: ignore[assignment]
#: The result of an operation that succeeded.
OK: int = _curses.OK if _curses is not None else 0  # type: ignore[assignment]

#: Attributes: standout mode.
A_STANDOUT: int = _curses.A_STANDOUT if _curses is not None else 0
#: Attributes: normal mode.
A_NORMAL: int = _curses.A_NORMAL if _curses is not None else 0
#: Attributes: reverse video.
A_REVERSE: int = _curses.A_REVERSE if _curses is not None else 0
#: Attributes: bold.
A_BOLD: int = _curses.A_BOLD if _curses is not None else 0
#: Attributes: dim.
A_DIM: int = _curses.A_DIM if _curses is not None else 0
#: Attributes: blinking.
A_BLINK: int = _curses.A_BLINK if _curses is not None else 0
#: Attributes: italic.
A_ITALIC: int = _curses.A_ITALIC if _curses is not None else 0
#: Attributes: underline.
A_UNDERLINE: int = _curses.A_UNDERLINE if _curses is not None else 0
#: Attributes: invisibility.
A_INVIS: int = _curses.A_INVIS if _curses is not None else 0
#: Attributes: protection.
A_PROTECT: int = _curses.A_PROTECT if _curses is not None else 0
#: Attributes: alternate character set.
A_ALTCHARSET: int = _curses.A_ALTCHARSET if _curses is not None else 0
#: Attributes: character text.
A_CHARTEXT: int = _curses.A_CHARTEXT if _curses is not None else 0
#: Attributes: color.
A_COLOR: int = _curses.A_COLOR if _curses is not None else 0
#: Attributes: all attributes.
A_ATTRIBUTES: int = _curses.A_ATTRIBUTES if _curses is not None else 0
#: Attributes: horizontal.
A_HORIZONTAL: int = _curses.A_HORIZONTAL if _curses is not None else 0
#: Attributes: left.
A_LEFT: int = _curses.A_LEFT if _curses is not None else 0
#: Attributes: low.
A_LOW: int = _curses.A_LOW if _curses is not None else 0
#: Attributes: right.
A_RIGHT: int = _curses.A_RIGHT if _curses is not None else 0
#: Attributes: top.
A_TOP: int = _curses.A_TOP if _curses is not None else 0
#: Attributes: vertical.
A_VERTICAL: int = _curses.A_VERTICAL if _curses is not None else 0

#: Colors.
COLOR_BLACK: int = _curses.COLOR_BLACK if _curses is not None else 0
COLOR_RED: int = _curses.COLOR_RED if _curses is not None else 0
COLOR_GREEN: int = _curses.COLOR_GREEN if _curses is not None else 0
COLOR_YELLOW: int = _curses.COLOR_YELLOW if _curses is not None else 0
COLOR_BLUE: int = _curses.COLOR_BLUE if _curses is not None else 0
COLOR_MAGENTA: int = _curses.COLOR_MAGENTA if _curses is not None else 0
COLOR_CYAN: int = _curses.COLOR_CYAN if _curses is not None else 0
COLOR_WHITE: int = _curses.COLOR_WHITE if _curses is not None else 0

#: Special keys.
KEY_UP: int = _curses.KEY_UP if _curses is not None else 0
KEY_DOWN: int = _curses.KEY_DOWN if _curses is not None else 0
KEY_LEFT: int = _curses.KEY_LEFT if _curses is not None else 0
KEY_RIGHT: int = _curses.KEY_RIGHT if _curses is not None else 0
KEY_HOME: int = _curses.KEY_HOME if _curses is not None else 0
KEY_END: int = _curses.KEY_END if _curses is not None else 0
KEY_BACKSPACE: int = _curses.KEY_BACKSPACE if _curses is not None else 0
KEY_ENTER: int = _curses.KEY_ENTER if _curses is not None else 0
KEY_RESIZE: int = _curses.KEY_RESIZE if _curses is not None else 0
KEY_MAX: int = _curses.KEY_MAX if _curses is not None else 0
KEY_MIN: int = _curses.KEY_MIN if _curses is not None else 0

__all__: List[str] = [
    "A_ALTCHARSET",
    "A_ATTRIBUTES",
    "A_BLINK",
    "A_BOLD",
    "A_CHARTEXT",
    "A_COLOR",
    "A_DIM",
    "A_HORIZONTAL",
    "A_INVIS",
    "A_ITALIC",
    "A_LEFT",
    "A_LOW",
    "A_NORMAL",
    "A_PROTECT",
    "A_REVERSE",
    "A_RIGHT",
    "A_STANDOUT",
    "A_TOP",
    "A_UNDERLINE",
    "A_VERTICAL",
    "COLOR_BLACK",
    "COLOR_BLUE",
    "COLOR_CYAN",
    "COLOR_GREEN",
    "COLOR_MAGENTA",
    "COLOR_RED",
    "COLOR_WHITE",
    "COLOR_YELLOW",
    "ERR",
    "KEY_BACKSPACE",
    "KEY_DOWN",
    "KEY_END",
    "KEY_ENTER",
    "KEY_HOME",
    "KEY_LEFT",
    "KEY_MAX",
    "KEY_MIN",
    "KEY_RESIZE",
    "KEY_RIGHT",
    "KEY_UP",
    "OK",
    "Window",
    "baudrate",
    "beep",
    "can_change_color",
    "cbreak",
    "color_content",
    "color_pair",
    "curs_set",
    "def_prog_mode",
    "def_shell_mode",
    "delay_output",
    "doupdate",
    "echo",
    "endwin",
    "erasechar",
    "filter",
    "flash",
    "flushinp",
    "get_escdelay",
    "get_tabsize",
    "getsyx",
    "has_colors",
    "has_ic",
    "has_il",
    "has_key",
    "is_available",
    "is_term_resized",
    "isendwin",
    "keyname",
    "killchar",
    "longname",
    "meta",
    "mouseinterval",
    "mousemask",
    "napms",
    "newwin",
    "nl",
    "nocbreak",
    "noecho",
    "nonl",
    "noqiflush",
    "noraw",
    "pair_content",
    "pair_number",
    "putp",
    "qiflush",
    "raw",
    "reset_prog_mode",
    "reset_shell_mode",
    "resetty",
    "resize_term",
    "resizeterm",
    "savetty",
    "set_escdelay",
    "set_tabsize",
    "setsyx",
    "start_color",
    "termattrs",
    "termname",
    "typeahead",
    "unget_wch",
    "ungetch",
    "use_default_colors",
    "use_env",
]


def _validate_int(value: int, name: str) -> int:
    """Return *value* when it is an integer.

    Args:
        value: The value to validate.
        name: The name of the argument, used in the error messages.

    Returns:
        The validated integer.

    Raises:
        TypeError: If *value* is not an int.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    return value


def _validate_bool(value: bool, name: str) -> bool:
    """Return *value* when it is a boolean.

    Args:
        value: The value to validate.
        name: The name of the argument, used in the error messages.

    Returns:
        The validated boolean.

    Raises:
        TypeError: If *value* is not a bool.
    """
    if not isinstance(value, bool):
        raise TypeError(f"{name} must be a bool, got {type(value).__name__}")
    return value


def initscr() -> Window:
    """Initialize the standard screen and return it.

    Returns:
        The standard screen window.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    return cast(Window, module.initscr())


def endwin() -> None:
    """Restore the terminal to its previous state.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    module.endwin()


def isendwin() -> bool:
    """Report whether ``endwin`` has been called.

    Returns:
        True if the terminal has been restored, False otherwise.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    return cast(bool, module.isendwin())


def savetty() -> None:
    """Save the state of the terminal.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    module.savetty()


def resetty() -> None:
    """Restore the state of the terminal to the last saved state.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    module.resetty()


def def_prog_mode() -> None:
    """Save the current terminal modes as the program mode.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    module.def_prog_mode()


def def_shell_mode() -> None:
    """Save the current terminal modes as the shell mode.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    module.def_shell_mode()


def reset_prog_mode() -> None:
    """Restore the terminal modes to the saved program mode.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    module.reset_prog_mode()


def reset_shell_mode() -> None:
    """Restore the terminal modes to the saved shell mode.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    module.reset_shell_mode()


def cbreak() -> None:
    """Set cbreak mode: characters are available immediately.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    module.cbreak()


def nocbreak() -> None:
    """Leave cbreak mode and return to normal line-buffered input.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    module.nocbreak()


def echo() -> None:
    """Enable echoing of input characters.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    module.echo()


def noecho() -> None:
    """Disable echoing of input characters.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    module.noecho()


def raw() -> None:
    """Set raw mode: characters are available without processing.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    module.raw()


def noraw() -> None:
    """Leave raw mode.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    module.noraw()


def nl() -> None:
    """Enable the translation of newline into carriage return and line feed.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    module.nl()


def nonl() -> None:
    """Disable the translation of newline into carriage return and line feed.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    module.nonl()


def qiflush() -> None:
    """Flush the input and output queues on an interrupt or quit character.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    module.qiflush()


def noqiflush() -> None:
    """Disable flushing of the input and output queues.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    module.noqiflush()


def intrflush(flag: bool) -> None:
    """Set whether an interrupt or a quit flushes the input queue.

    Args:
        flag: Whether flushing is enabled.

    Raises:
        TypeError: If *flag* is not a bool.
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    _validate_bool(flag, "flag")
    module = _curses_module()
    module.intrflush(flag)


def meta(flag: bool) -> None:
    """Set whether the meta key returns eight-bit characters.

    Args:
        flag: Whether meta mode is enabled.

    Raises:
        TypeError: If *flag* is not a bool.
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    _validate_bool(flag, "flag")
    module = _curses_module()
    module.meta(flag)


def halfdelay(tenths: int) -> None:
    """Set half-delay mode: input blocks for *tenths* tenths of a second.

    Args:
        tenths: The delay in tenths of a second.

    Raises:
        TypeError: If *tenths* is not an int.
        ValueError: If *tenths* is negative.
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    _validate_int(tenths, "tenths")
    if tenths < 0:
        raise ValueError(f"tenths must not be negative, got {tenths}")
    module = _curses_module()
    module.halfdelay(tenths)


def get_escdelay() -> int:
    """Return the escape delay of the terminal in milliseconds.

    Returns:
        The escape delay in milliseconds.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    return cast(int, module.get_escdelay())


def set_escdelay(ms: int) -> None:
    """Set the escape delay of the terminal to *ms* milliseconds.

    Args:
        ms: The escape delay in milliseconds.

    Raises:
        TypeError: If *ms* is not an int.
        ValueError: If *ms* is negative.
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    _validate_int(ms, "ms")
    if ms < 0:
        raise ValueError(f"ms must not be negative, got {ms}")
    module = _curses_module()
    module.set_escdelay(ms)


def get_tabsize() -> int:
    """Return the tab size of the terminal.

    Returns:
        The tab size of the terminal.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    return cast(int, module.get_tabsize())


def set_tabsize(size: int) -> None:
    """Set the tab size of the terminal to *size*.

    Args:
        size: The tab size.

    Raises:
        TypeError: If *size* is not an int.
        ValueError: If *size* is negative.
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    _validate_int(size, "size")
    if size < 0:
        raise ValueError(f"size must not be negative, got {size}")
    module = _curses_module()
    module.set_tabsize(size)


def curs_set(visibility: int) -> int:
    """Set the visibility of the cursor.

    Args:
        visibility: ``0`` hides the cursor, ``1`` shows it normally, and
            ``2`` makes it highly visible.

    Returns:
        The previous visibility of the cursor.

    Raises:
        TypeError: If *visibility* is not an int.
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    _validate_int(visibility, "visibility")
    module = _curses_module()
    return cast(int, module.curs_set(visibility))


def getsyx() -> Optional[Tuple[int, int]]:
    """Return the coordinates of the virtual cursor.

    Returns:
        The ``(y, x)`` coordinates of the cursor, or ``None`` when they are
        unknown.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    result = module.getsyx()
    if result is None:
        return None
    return cast(Tuple[int, int], result)


def setsyx(y: int, x: int) -> None:
    """Set the virtual cursor to the coordinates (*y*, *x*).

    Args:
        y: The row of the cursor.
        x: The column of the cursor.

    Raises:
        TypeError: If *y* or *x* is not an int.
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    _validate_int(y, "y")
    _validate_int(x, "x")
    module = _curses_module()
    module.setsyx(y, x)


def start_color() -> None:
    """Initialize color support.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    module.start_color()


def has_colors() -> bool:
    """Report whether the terminal supports colors.

    Returns:
        True if the terminal can change colors, False otherwise.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    return cast(bool, module.has_colors())


def can_change_color() -> bool:
    """Report whether colors can be redefined.

    Returns:
        True if colors can be redefined, False otherwise.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    return cast(bool, module.can_change_color())


def init_pair(pair: int, fg: int, bg: int) -> None:
    """Define the colors of the color pair *pair*.

    Args:
        pair: The number of the color pair.
        fg: The foreground color.
        bg: The background color.

    Raises:
        TypeError: If an argument is not an int.
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    _validate_int(pair, "pair")
    _validate_int(fg, "fg")
    _validate_int(bg, "bg")
    module = _curses_module()
    module.init_pair(pair, fg, bg)


def init_color(color: int, r: int, g: int, b: int) -> None:
    """Redefine a color.

    Args:
        color: The number of the color to redefine.
        r: The red component.
        g: The green component.
        b: The blue component.

    Raises:
        TypeError: If an argument is not an int.
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    _validate_int(color, "color")
    _validate_int(r, "r")
    _validate_int(g, "g")
    _validate_int(b, "b")
    module = _curses_module()
    module.init_color(color, r, g, b)


def color_content(color: int) -> Tuple[int, int, int]:
    """Return the red, green, and blue components of a color.

    Args:
        color: The number of the color.

    Returns:
        The ``(red, green, blue)`` components of the color.

    Raises:
        TypeError: If *color* is not an int.
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    _validate_int(color, "color")
    module = _curses_module()
    return cast(Tuple[int, int, int], module.color_content(color))


def pair_content(pair: int) -> Tuple[int, int, int]:
    """Return the foreground and background colors of a color pair.

    Args:
        pair: The number of the color pair.

    Returns:
        The ``(foreground, background)`` colors of the pair.

    Raises:
        TypeError: If *pair* is not an int.
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    _validate_int(pair, "pair")
    module = _curses_module()
    return cast(Tuple[int, int, int], module.pair_content(pair))


def color_pair(pair: int) -> int:
    """Return the attribute value of a color pair.

    Args:
        pair: The number of the color pair.

    Returns:
        The attribute value of the color pair.

    Raises:
        TypeError: If *pair* is not an int.
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    _validate_int(pair, "pair")
    module = _curses_module()
    return cast(int, module.color_pair(pair))


def pair_number(attrs: int) -> int:
    """Return the number of the color pair of an attribute.

    Args:
        attrs: The attribute value.

    Returns:
        The number of the color pair.

    Raises:
        TypeError: If *attrs* is not an int.
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    _validate_int(attrs, "attrs")
    module = _curses_module()
    return cast(int, module.pair_number(attrs))


def use_default_colors() -> int:
    """Assign the default colors of the terminal to color pairs.

    Returns:
        :data:`OK` on success.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    return cast(int, module.use_default_colors())


def baudrate() -> int:
    """Return the speed of the terminal in bits per second.

    Returns:
        The baud rate of the terminal.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    return cast(int, module.baudrate())


def beep() -> None:
    """Produce a beep on the terminal.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    module.beep()


def flash() -> None:
    """Flash the screen.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    module.flash()


def delay_output(ms: int) -> None:
    """Delay the output for *ms* milliseconds.

    Args:
        ms: The delay in milliseconds.

    Raises:
        TypeError: If *ms* is not an int.
        ValueError: If *ms* is negative.
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    _validate_int(ms, "ms")
    if ms < 0:
        raise ValueError(f"ms must not be negative, got {ms}")
    module = _curses_module()
    module.delay_output(ms)


def flushinp() -> None:
    """Discard all input waiting in the input queue.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    module.flushinp()


def napms(ms: int) -> None:
    """Sleep for *ms* milliseconds.

    Args:
        ms: The delay in milliseconds.

    Raises:
        TypeError: If *ms* is not an int.
        ValueError: If *ms* is negative.
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    _validate_int(ms, "ms")
    if ms < 0:
        raise ValueError(f"ms must not be negative, got {ms}")
    module = _curses_module()
    module.napms(ms)


def ungetch(ch: int) -> None:
    """Push a character back onto the input queue.

    Args:
        ch: The character to push back.

    Raises:
        TypeError: If *ch* is not an int.
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    _validate_int(ch, "ch")
    module = _curses_module()
    module.ungetch(ch)


def unget_wch(ch: str) -> None:
    """Push a wide character back onto the input queue.

    Args:
        ch: The wide character to push back.

    Raises:
        TypeError: If *ch* is not a str.
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    if not isinstance(ch, str):
        raise TypeError(f"ch must be a str, got {type(ch).__name__}")
    module = _curses_module()
    module.unget_wch(ch)


def newwin(nlines: int, ncols: int, begin_y: int, begin_x: int) -> Window:
    """Create a new window.

    Args:
        nlines: The number of lines of the window.
        ncols: The number of columns of the window.
        begin_y: The row of the upper left corner.
        begin_x: The column of the upper left corner.

    Returns:
        The new window.

    Raises:
        TypeError: If an argument is not an int.
        ValueError: If an argument is negative.
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    _validate_int(nlines, "nlines")
    _validate_int(ncols, "ncols")
    _validate_int(begin_y, "begin_y")
    _validate_int(begin_x, "begin_x")
    if nlines < 0 or ncols < 0 or begin_y < 0 or begin_x < 0:
        raise ValueError("arguments must not be negative")
    module = _curses_module()
    return cast(Window, module.newwin(nlines, ncols, begin_y, begin_x))


def doupdate() -> None:
    """Update the physical screen to match the virtual screens.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    module.doupdate()


def erasechar() -> str:
    """Return the erase character of the terminal.

    Returns:
        The erase character.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    return cast(str, module.erasechar())


def killchar() -> str:
    """Return the kill character of the terminal.

    Returns:
        The kill character.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    return cast(str, module.killchar())


def keyname(c: Union[int, str]) -> Union[str, bytes]:
    """Return the name of the key *c*.

    Args:
        c: The key code or the character.

    Returns:
        The name of the key.

    Raises:
        TypeError: If *c* is not an int or a str.
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    if not isinstance(c, (int, str)):
        raise TypeError(f"c must be an int or a str, got {type(c).__name__}")
    module = _curses_module()
    return cast(Union[str, bytes], module.keyname(c))


def longname() -> str:
    """Return the long name of the terminal.

    Returns:
        The long name of the terminal.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    return cast(str, module.longname())


def termname() -> str:
    """Return the short name of the terminal.

    Returns:
        The short name of the terminal.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    return cast(str, module.termname())


def termattrs() -> int:
    """Return the video attributes supported by the terminal.

    Returns:
        The supported video attributes.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    return cast(int, module.termattrs())


def has_ic() -> bool:
    """Report whether the terminal supports insert and delete characters.

    Returns:
        True if the terminal supports them, False otherwise.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    return cast(bool, module.has_ic())


def has_il() -> bool:
    """Report whether the terminal supports insert and delete lines.

    Returns:
        True if the terminal supports them, False otherwise.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    return cast(bool, module.has_il())


def has_key(key: int) -> bool:
    """Report whether the terminal recognizes the key *key*.

    Args:
        key: The key code to test.

    Returns:
        True if the terminal recognizes the key, False otherwise.

    Raises:
        TypeError: If *key* is not an int.
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    _validate_int(key, "key")
    module = _curses_module()
    return cast(bool, module.has_key(key))


def filter() -> None:
    """Restrict the terminal to the current line.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    module.filter()


def typeahead(fd: int) -> None:
    """Set the file descriptor used for typeahead checking.

    Args:
        fd: The file descriptor.

    Raises:
        TypeError: If *fd* is not an int.
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    _validate_int(fd, "fd")
    module = _curses_module()
    module.typeahead(fd)


def resize_term(nlines: int, ncols: int) -> None:
    """Resize the standard screen and the windows.

    Args:
        nlines: The new number of lines.
        ncols: The new number of columns.

    Raises:
        TypeError: If an argument is not an int.
        ValueError: If an argument is negative.
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    _validate_int(nlines, "nlines")
    _validate_int(ncols, "ncols")
    if nlines < 0 or ncols < 0:
        raise ValueError("arguments must not be negative")
    module = _curses_module()
    module.resize_term(nlines, ncols)


def resizeterm(nlines: int, ncols: int) -> None:
    """Alias of :func:`resize_term`.

    Args:
        nlines: The new number of lines.
        ncols: The new number of columns.

    Raises:
        TypeError: If an argument is not an int.
        ValueError: If an argument is negative.
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    _validate_int(nlines, "nlines")
    _validate_int(ncols, "ncols")
    if nlines < 0 or ncols < 0:
        raise ValueError("arguments must not be negative")
    module = _curses_module()
    module.resizeterm(nlines, ncols)


def is_term_resized(nlines: int, ncols: int) -> bool:
    """Report whether the terminal was resized to (*nlines*, *ncols*).

    Args:
        nlines: The number of lines.
        ncols: The number of columns.

    Returns:
        True if the terminal was resized, False otherwise.

    Raises:
        TypeError: If an argument is not an int.
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    _validate_int(nlines, "nlines")
    _validate_int(ncols, "ncols")
    module = _curses_module()
    return cast(bool, module.is_term_resized(nlines, ncols))


def update_lines_cols() -> None:
    """Update the number of lines and columns of the standard screen.

    Raises:
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    module = _curses_module()
    module.update_lines_cols()


def setupterm(term: str) -> None:
    """Read the terminal capabilities of *term*.

    Args:
        term: The name of the terminal type.

    Raises:
        TypeError: If *term* is not a str.
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    if not isinstance(term, str):
        raise TypeError(f"term must be a str, got {type(term).__name__}")
    module = _curses_module()
    module.setupterm(term)


def mouseinterval(interval: int) -> int:
    """Set the maximum interval in milliseconds between mouse clicks.

    Args:
        interval: The interval in milliseconds.

    Returns:
        The previous interval.

    Raises:
        TypeError: If *interval* is not an int.
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    _validate_int(interval, "interval")
    module = _curses_module()
    return cast(int, module.mouseinterval(interval))


def mousemask(newmask: int) -> int:
    """Set the mouse events to be reported.

    Args:
        newmask: The mask of the mouse events.

    Returns:
        The mask of the mouse events that can be reported.

    Raises:
        TypeError: If *newmask* is not an int.
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    _validate_int(newmask, "newmask")
    module = _curses_module()
    return cast(int, module.mousemask(newmask))


def putp(string: str) -> None:
    """Write the string *string* to the terminal.

    Args:
        string: The string to write.

    Raises:
        TypeError: If *string* is not a str.
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    if not isinstance(string, str):
        raise TypeError(f"string must be a str, got {type(string).__name__}")
    module = _curses_module()
    module.putp(string)


def use_env(flag: bool) -> None:
    """Set whether the environment determines the terminal size.

    Args:
        flag: Whether the environment is used.

    Raises:
        TypeError: If *flag* is not a bool.
        RuntimeError: If the interpreter does not ship the ``curses`` module.
    """
    _validate_bool(flag, "flag")
    module = _curses_module()
    module.use_env(flag)
