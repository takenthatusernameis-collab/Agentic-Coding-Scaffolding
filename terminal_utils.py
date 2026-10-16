"""Terminal output utilities for colored text, progress bars, and prompts.

This module provides helpers for formatting terminal output using ANSI escape
sequences, rendering progress bars, clearing the screen, querying terminal
size, and reading user input. Output degrades gracefully when the stream is
not a terminal (for example, when piped to a file or captured in tests).
"""

from __future__ import annotations

import os
import shutil
import sys
from typing import Iterable, Iterator, Optional, TextIO, Tuple

_RESET = "\033[0m"
_BOLD = "\033[1m"

_COLOR_CODES: dict = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
}

_VALID_COLORS = frozenset(_COLOR_CODES)


def supports_color(stream: Optional[TextIO] = None) -> bool:
    """Return True if *stream* (default stdout) supports ANSI colors.

    Color is disabled when the stream is not a TTY, when the ``NO_COLOR``
    environment variable is set, or when the stream lacks an ``isatty``
    method.
    """
    if stream is None:
        stream = sys.stdout
    if "NO_COLOR" in os.environ:
        return False
    if not hasattr(stream, "isatty") or not stream.isatty():
        return False
    return True


def colorize(text: str, color: str = "white", bold: bool = False) -> str:
    """Wrap *text* in ANSI color escape codes.

    Args:
        text: The text to colorize.
        color: One of black, red, green, yellow, blue, magenta, cyan, white.
        bold: Whether to render the text in bold.

    Returns:
        The colorized text, or the original text unchanged when color is not
        supported on stdout.

    Raises:
        TypeError: If *text* or *color* is not a string.
        ValueError: If *color* is not a supported color name.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(color, str):
        raise TypeError("color must be a string")
    if color not in _VALID_COLORS:
        raise ValueError(
            f"unsupported color {color!r}; supported colors are "
            f"{sorted(_VALID_COLORS)!r}"
        )
    if not supports_color():
        return text
    codes = [_COLOR_CODES[color]]
    if bold:
        codes.insert(0, _BOLD)
    return f"\033[{';'.join(codes)}m{text}{_RESET}"


def print_colored(
    text: str,
    color: str = "white",
    bold: bool = False,
    stream: Optional[TextIO] = None,
) -> None:
    """Print colorized text to *stream* (default stdout).

    Args:
        text: The text to print.
        color: One of black, red, green, yellow, blue, magenta, cyan, white.
        bold: Whether to render the text in bold.
        stream: The output stream (defaults to sys.stdout).
    """
    if stream is None:
        stream = sys.stdout
    stream.write(colorize(text, color=color, bold=bold) + "\n")
    stream.flush()


def clear_screen() -> None:
    """Clear the terminal screen.

    Uses the ANSI clear-screen escape sequence when supported, falling back
    to printing newlines otherwise.
    """
    if supports_color(sys.stdout):
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()
    else:
        sys.stdout.write("\n" * 50)
        sys.stdout.flush()


def get_terminal_size() -> Tuple[int, int]:
    """Return the terminal size as ``(columns, lines)``.

    Falls back to ``(80, 24)`` when the size cannot be determined.
    """
    try:
        size = shutil.get_terminal_size(fallback=(80, 24))
    except Exception:
        return (80, 24)
    return (size.columns, size.lines)


class ProgressBar:
    """A simple terminal progress bar.

    Args:
        total: The total number of steps. Must be a positive integer.
        width: The character width of the bar (excluding labels). Defaults
            to a size derived from the terminal width.
        fill: The single character used for the completed portion.
        empty: The single character used for the remaining portion.
        stream: The output stream (defaults to sys.stdout).
    """

    def __init__(
        self,
        total: int,
        width: Optional[int] = None,
        fill: str = "#",
        empty: str = "-",
        stream: Optional[TextIO] = None,
    ) -> None:
        if isinstance(total, bool) or not isinstance(total, int) or total <= 0:
            raise ValueError("total must be a positive integer")
        if not isinstance(fill, str) or len(fill) != 1:
            raise ValueError("fill must be a single character")
        if not isinstance(empty, str) or len(empty) != 1:
            raise ValueError("empty must be a single character")
        if stream is None:
            stream = sys.stdout
        self.total = total
        if width is None:
            width = max(10, min(40, _term_width(stream) - 12))
        self.width = width
        self.fill = fill
        self.empty = empty
        self.stream = stream
        self._current = 0
        self._finished = False

    def update(self, current: Optional[int] = None, increment: int = 1) -> None:
        """Advance the progress bar to *current* or by *increment*.

        Args:
            current: The absolute step to advance to, within [0, total].
            increment: The number of steps to advance (default 1).

        Raises:
            TypeError: If *current* is not an integer.
            ValueError: If the resulting position is outside [0, total].
        """
        if self._finished:
            return
        if current is None:
            current = self._current + increment
        if isinstance(current, bool) or not isinstance(current, int):
            raise TypeError("current must be an integer")
        if current < 0 or current > self.total:
            raise ValueError(f"current {current} is outside [0, {self.total}]")
        self._current = current
        self._render()
        if self._current >= self.total:
            self._finished = True
            self.stream.write("\n")
            self.stream.flush()

    def finish(self) -> None:
        """Mark the progress bar as complete and print a final newline."""
        if not self._finished:
            self._current = self.total
            self._finished = True
            self.stream.write("\n")
            self.stream.flush()

    def _render(self) -> None:
        ratio = self._current / self.total
        filled = int(ratio * self.width)
        bar = self.fill * filled + self.empty * (self.width - filled)
        percent = int(ratio * 100)
        line = f"\r[{bar}] {percent}% ({self._current}/{self.total})"
        self.stream.write(line)
        self.stream.flush()

    def __enter__(self) -> "ProgressBar":
        return self

    def __exit__(self, *args) -> None:
        self.finish()


def progress_bar(
    iterable: Iterable,
    total: Optional[int] = None,
    width: Optional[int] = None,
    fill: str = "#",
    empty: str = "-",
    stream: Optional[TextIO] = None,
) -> Iterator:
    """Yield items from *iterable* while rendering a progress bar.

    Args:
        iterable: The iterable to wrap.
        total: The total number of items. Inferred from ``len`` when
            available; otherwise must be provided.
        width: The character width of the bar.
        fill: The character used for the completed portion.
        empty: The character used for the remaining portion.
        stream: The output stream (defaults to sys.stdout).

    Raises:
        ValueError: If *total* cannot be inferred and is not provided.
    """
    if total is None:
        try:
            total = len(iterable)  # type: ignore[arg-type]
        except TypeError as exc:
            raise ValueError(
                "total must be provided for iterables without len()"
            ) from exc
    bar = ProgressBar(total, width=width, fill=fill, empty=empty, stream=stream)
    with bar:
        for item in iterable:
            bar.update(increment=1)
            yield item


def prompt(message: str, default: Optional[str] = None) -> str:
    """Prompt the user for input and return the entered value.

    Args:
        message: The prompt message to display.
        default: The value returned when the user enters nothing.

    Returns:
        The user's input, or *default* when the input is empty.

    Raises:
        TypeError: If *message* or *default* is not a string/None.
        EOFError: If the input stream is closed.
    """
    if not isinstance(message, str):
        raise TypeError("message must be a string")
    if default is not None and not isinstance(default, str):
        raise TypeError("default must be a string or None")
    suffix = f" [{default}]" if default is not None else ""
    full_message = message + suffix + ": "
    if supports_color(sys.stdout):
        full_message = colorize(full_message, color="cyan")
    try:
        value = input(full_message)
    except EOFError as exc:
        raise EOFError("input stream closed") from exc
    if value == "":
        return default if default is not None else ""
    return value


def _term_width(stream: TextIO) -> int:
    try:
        return shutil.get_terminal_size(fallback=(80, 24)).columns
    except Exception:
        return 80
