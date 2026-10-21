"""Command line editing utilities wrapping the standard library :mod:`readline` module.

The :mod:`readline` module gives an interactive program the line editing of
GNU readline: a history of the lines that were entered, key bindings, and tab
completion.  The standard library offers the functions that drive the editor:
the history is read from a file and written to a file, entries are added,
read, removed, and replaced, a completer is registered, and the hooks of the
editor are set.

This wrapper validates every argument before the standard library is reached,
so a caller gets a clear :class:`TypeError` or :class:`ValueError` instead of
an opaque failure.  It adds the helpers the standard library leaves to the
caller: the history is returned as a list, the positions of the history are
numbered the same way everywhere, the helpers that touch a file always name
the file they touch, and a completer for a fixed list of words is offered.

.. note::

   The :mod:`readline` module only exists on Unix-like platforms.  The import
   below degrades gracefully: when the interpreter does not ship the module,
   the helpers raise a :class:`RuntimeError` that names the missing module,
   while :func:`is_available` keeps working.

The standard library numbers the history twice: :func:`readline.get_history_item`
reads an entry by its one-based position, while
:func:`readline.remove_history_item` and :func:`readline.replace_history_item`
work on a zero-based position.  The wrapper numbers every position the same
way, with the one-based number the standard library uses to read an entry, so
a position that can be read can also be removed and replaced.
"""

from __future__ import annotations

import os
from typing import Any, Callable, List, Optional, cast

try:
    import readline as _readline
except ImportError:  # pragma: no cover - the module is Unix-only
    _readline = None  # type: ignore[assignment]

__all__: List[str] = [
    "add_history",
    "append_history_file",
    "clear_history",
    "default_history_file",
    "get_begidx",
    "get_completer",
    "get_completer_delims",
    "get_completion_type",
    "get_current_history_length",
    "get_endidx",
    "get_history_item",
    "get_history_length",
    "get_line_buffer",
    "history_items",
    "insert_text",
    "is_available",
    "make_completer",
    "parse_and_bind",
    "read_history_file",
    "read_init_file",
    "redisplay",
    "remove_history_item",
    "replace_history_item",
    "search_history",
    "set_auto_history",
    "set_completer",
    "set_completer_delims",
    "set_completion_display_matches_hook",
    "set_history_length",
    "set_pre_input_hook",
    "set_startup_hook",
    "write_history_file",
]


def _readline_module() -> Any:
    """Return the standard library ``readline`` module.

    Returns:
        The imported :mod:`readline` module.

    Raises:
        RuntimeError: If the interpreter does not ship the ``readline``
            module.
    """
    if _readline is None:  # pragma: no cover - the module is Unix-only
        raise RuntimeError(
            "the standard library module 'readline' is not available on this interpreter"
        )
    return _readline


def _require_function(name: str) -> Any:
    """Return the standard library function *name*.

    Some functions of the standard library are only compiled into the module
    when the platform supports them, so a caller gets a clear message instead
    of an :class:`AttributeError`.

    Args:
        name: The name of the function of the standard library.

    Returns:
        The function of the standard library.

    Raises:
        RuntimeError: If the standard library does not provide the function.
    """
    function = getattr(_readline_module(), name, None)
    if function is None:  # pragma: no cover - a platform specific build
        raise RuntimeError(
            f"the standard library module 'readline' does not provide '{name}'"
        )
    return function


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


def _require_path(value: Any, name: str) -> str:
    """Return *value* as the path of a file.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The path as text.

    Raises:
        TypeError: If *value* is neither a string nor a path.
        ValueError: If *value* is an empty path.
    """
    if not isinstance(value, (str, os.PathLike)):
        raise TypeError(f"{name} must be a path, got {type(value).__name__}")
    text = os.fspath(value)
    if not isinstance(text, str):
        raise TypeError(f"{name} must be a text path, got {type(value).__name__}")
    if not text:
        raise ValueError(f"{name} must not be empty")
    return text


def _require_position(value: Any, name: str = "position") -> int:
    """Return *value* as the position of a history entry.

    The positions of the wrapper start at one, the way the standard library
    numbers the entries it reads.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The position.

    Raises:
        TypeError: If *value* is not an integer.
        ValueError: If *value* is smaller than one.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    if value < 1:
        raise ValueError(f"{name} must be at least 1, got {value}")
    return value


def _require_count(value: Any, name: str = "count") -> int:
    """Return *value* as a number of history entries.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The number of entries.

    Raises:
        TypeError: If *value* is not an integer.
        ValueError: If *value* is negative.
    """
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    if value < 0:
        raise ValueError(f"{name} must not be negative, got {value}")
    return value


def _require_hook(value: Any, name: str) -> Optional[Callable[..., Any]]:
    """Return *value* as a hook of the editor.

    Args:
        value: The value to check.
        name: The name of the argument, used in the error message.

    Returns:
        The hook, or ``None`` when the hook is removed.

    Raises:
        TypeError: If *value* is neither ``None`` nor a callable.
    """
    if value is None:
        return None
    if not callable(value):
        raise TypeError(f"{name} must be callable or None, got {type(value).__name__}")
    return cast(Callable[..., Any], value)


def is_available() -> bool:
    """Report whether the interpreter ships the :mod:`readline` module.

    Returns:
        True when the standard library module is importable, False otherwise.
    """
    return _readline is not None


def default_history_file() -> str:
    """Return the history file the standard library uses by default.

    The standard library reads and writes the history of the user when no file
    is named.  The wrapper always names the file it touches, so this helper
    returns the path the standard library would use.

    Returns:
        The path of the history file of the user.
    """
    return os.path.expanduser("~/.history")


def parse_and_bind(key_sequence: Any) -> None:
    """Execute the key sequence *key_sequence*.

    The key sequence is the syntax of an init file of readline, for example
    ``"set editing-mode emacs"``.

    Args:
        key_sequence: The key sequence to execute.

    Raises:
        TypeError: If *key_sequence* is not a string.
        RuntimeError: If the interpreter does not ship the ``readline``
            module.
    """
    sequence = _require_text(key_sequence, "key_sequence")
    _require_function("parse_and_bind")(sequence)


def read_init_file(filename: Any) -> str:
    """Execute the init file *filename*.

    The file holds the key bindings and the settings of the editor.

    Args:
        filename: The path of the init file.

    Returns:
        The path of the file that was read.

    Raises:
        TypeError: If *filename* is not a path.
        ValueError: If *filename* is an empty path.
        RuntimeError: If the interpreter does not ship the ``readline``
            module.
        OSError: If the file cannot be read.
    """
    path = _require_path(filename, "filename")
    _require_function("read_init_file")(path)
    return path


def read_history_file(filename: Any) -> str:
    """Load the history of the file *filename*.

    The entries of the file are added to the history of the editor.

    Args:
        filename: The path of the history file.

    Returns:
        The path of the file that was read.

    Raises:
        TypeError: If *filename* is not a path.
        ValueError: If *filename* is an empty path.
        RuntimeError: If the interpreter does not ship the ``readline``
            module.
        OSError: If the file cannot be read.
    """
    path = _require_path(filename, "filename")
    _require_function("read_history_file")(path)
    return path


def write_history_file(filename: Any) -> str:
    """Write the history of the editor to the file *filename*.

    Args:
        filename: The path of the history file.

    Returns:
        The path of the file that was written.

    Raises:
        TypeError: If *filename* is not a path.
        ValueError: If *filename* is an empty path.
        RuntimeError: If the interpreter does not ship the ``readline``
            module.
        OSError: If the file cannot be written.
    """
    path = _require_path(filename, "filename")
    _require_function("write_history_file")(path)
    return path


def append_history_file(count: Any, filename: Any) -> str:
    """Append the last *count* entries of the history to the file *filename*.

    The file has to exist, the way the standard library expects it.

    Args:
        count: The number of entries that are appended.
        filename: The path of the history file.

    Returns:
        The path of the file the entries were appended to.

    Raises:
        TypeError: If *count* is not an integer or *filename* is not a path.
        ValueError: If *count* is negative or *filename* is an empty path.
        RuntimeError: If the interpreter does not ship the ``readline``
            module.
        OSError: If the file cannot be written.
    """
    number = _require_count(count)
    path = _require_path(filename, "filename")
    _require_function("append_history_file")(number, path)
    return path


def set_history_length(length: Any) -> None:
    """Set the maximal number of lines that are written to the history file.

    A negative length inhibits the truncation of the history file, which is
    what the standard library does by default.

    Args:
        length: The maximal number of lines.

    Raises:
        TypeError: If *length* is not an integer.
        RuntimeError: If the interpreter does not ship the ``readline``
            module.
    """
    if isinstance(length, bool) or not isinstance(length, int):
        raise TypeError(f"length must be an int, got {type(length).__name__}")
    _require_function("set_history_length")(length)


def get_history_length() -> int:
    """Return the maximal number of lines that are written to the history file.

    Returns:
        The maximal number of lines, or a negative number when the truncation
        of the history file is inhibited.

    Raises:
        RuntimeError: If the interpreter does not ship the ``readline``
            module.
    """
    return int(_require_function("get_history_length")())


def get_current_history_length() -> int:
    """Return the number of entries the history holds.

    Returns:
        The number of entries of the history.

    Raises:
        RuntimeError: If the interpreter does not ship the ``readline``
            module.
    """
    return int(_require_function("get_current_history_length")())


def add_history(line: Any) -> None:
    """Add the line *line* to the history.

    Args:
        line: The line that is added.

    Raises:
        TypeError: If *line* is not a string.
        RuntimeError: If the interpreter does not ship the ``readline``
            module.
    """
    text = _require_text(line, "line")
    _require_function("add_history")(text)


def clear_history() -> None:
    """Remove every entry from the history.

    Raises:
        RuntimeError: If the interpreter does not ship the ``readline``
            module.
    """
    _require_function("clear_history")()


def get_history_item(position: Any) -> Optional[str]:
    """Return the entry of the history at *position*.

    The positions start at one, the way the standard library numbers the
    entries it reads.

    Args:
        position: The position of the entry.

    Returns:
        The entry, or ``None`` when the history holds no entry at the
        position.

    Raises:
        TypeError: If *position* is not an integer.
        ValueError: If *position* is smaller than one.
        RuntimeError: If the interpreter does not ship the ``readline``
            module.
    """
    number = _require_position(position)
    item = _require_function("get_history_item")(number)
    return None if item is None else str(item)


def remove_history_item(position: Any) -> str:
    """Remove the entry of the history at *position* and return it.

    The positions start at one, the way the standard library numbers the
    entries it reads.  The standard library counts the entries it removes from
    zero, so the wrapper converts the position before it removes the entry.

    Args:
        position: The position of the entry.

    Returns:
        The entry that was removed.

    Raises:
        TypeError: If *position* is not an integer.
        ValueError: If *position* is smaller than one or the history holds no
            entry at the position.
        RuntimeError: If the interpreter does not ship the ``readline``
            module.
    """
    number = _require_position(position)
    module = _readline_module()
    entry = module.get_history_item(number)
    try:
        module.remove_history_item(number - 1)
    except ValueError as error:
        raise ValueError(f"the history holds no entry at position {number}") from error
    return "" if entry is None else str(entry)


def replace_history_item(position: Any, line: Any) -> str:
    """Replace the entry of the history at *position* and return it.

    The positions start at one, the way the standard library numbers the
    entries it reads.  The standard library counts the entries it replaces
    from zero, so the wrapper converts the position before it replaces the
    entry.

    Args:
        position: The position of the entry.
        line: The line that replaces the entry.

    Returns:
        The entry that was replaced.

    Raises:
        TypeError: If *position* is not an integer or *line* is not a string.
        ValueError: If *position* is smaller than one or the history holds no
            entry at the position.
        RuntimeError: If the interpreter does not ship the ``readline``
            module.
    """
    number = _require_position(position)
    text = _require_text(line, "line")
    module = _readline_module()
    entry = module.get_history_item(number)
    try:
        module.replace_history_item(number - 1, text)
    except ValueError as error:
        raise ValueError(f"the history holds no entry at position {number}") from error
    return "" if entry is None else str(entry)


def history_items() -> List[str]:
    """Return every entry of the history, the oldest one first.

    The standard library offers no way to read the history at once, so the
    wrapper reads the entries one by one.

    Returns:
        The entries of the history.

    Raises:
        RuntimeError: If the interpreter does not ship the ``readline``
            module.
    """
    module = _readline_module()
    length = int(module.get_current_history_length())
    items: List[str] = []
    for number in range(1, length + 1):
        entry = module.get_history_item(number)
        if entry is not None:
            items.append(str(entry))
    return items


def search_history(prefix: Any) -> List[str]:
    """Return the entries of the history that start with *prefix*.

    Args:
        prefix: The text the entries start with.

    Returns:
        The matching entries of the history, the oldest one first.

    Raises:
        TypeError: If *prefix* is not a string.
        RuntimeError: If the interpreter does not ship the ``readline``
            module.
    """
    text = _require_text(prefix, "prefix")
    return [entry for entry in history_items() if entry.startswith(text)]


def set_completer(function: Any) -> None:
    """Set the completer of the editor.

    The completer is called with the text that is completed and the number of
    the match that is wanted, and it returns the match or ``None`` when there
    is no further match.  Passing ``None`` removes the completer.

    Args:
        function: The completer, or ``None``.

    Raises:
        TypeError: If *function* is neither ``None`` nor a callable.
        RuntimeError: If the interpreter does not ship the ``readline``
            module.
    """
    completer = _require_hook(function, "function")
    _require_function("set_completer")(completer)


def get_completer() -> Optional[Callable[..., Any]]:
    """Return the completer of the editor.

    Returns:
        The completer, or ``None`` when no completer is set.

    Raises:
        RuntimeError: If the interpreter does not ship the ``readline``
            module.
    """
    completer = _require_function("get_completer")()
    return None if completer is None else completer


def set_completer_delims(delimiters: Any) -> None:
    """Set the delimiters the editor splits a word at.

    Args:
        delimiters: The delimiters as text.

    Raises:
        TypeError: If *delimiters* is not a string.
        RuntimeError: If the interpreter does not ship the ``readline``
            module.
    """
    text = _require_text(delimiters, "delimiters")
    _require_function("set_completer_delims")(text)


def get_completer_delims() -> str:
    """Return the delimiters the editor splits a word at.

    Returns:
        The delimiters as text.

    Raises:
        RuntimeError: If the interpreter does not ship the ``readline``
            module.
    """
    return str(_require_function("get_completer_delims")())


def set_startup_hook(function: Any) -> None:
    """Set the hook that runs before the first prompt is printed.

    The hook is called without arguments.  Passing ``None`` removes it.

    Args:
        function: The hook, or ``None``.

    Raises:
        TypeError: If *function* is neither ``None`` nor a callable.
        RuntimeError: If the interpreter does not ship the ``readline``
            module.
    """
    hook = _require_hook(function, "function")
    _require_function("set_startup_hook")(hook)


def set_pre_input_hook(function: Any) -> None:
    """Set the hook that runs before the editor reads a character.

    The hook is called without arguments.  Passing ``None`` removes it.

    Args:
        function: The hook, or ``None``.

    Raises:
        TypeError: If *function* is neither ``None`` nor a callable.
        RuntimeError: If the interpreter does not ship the ``readline``
            module.
    """
    hook = _require_hook(function, "function")
    _require_function("set_pre_input_hook")(hook)


def set_completion_display_matches_hook(function: Any) -> None:
    """Set the hook that displays the matches of a completion.

    The hook is called with the text that is completed, the list of the
    matches, and the length of the longest match.  Passing ``None`` removes
    it.

    Args:
        function: The hook, or ``None``.

    Raises:
        TypeError: If *function* is neither ``None`` nor a callable.
        RuntimeError: If the interpreter does not ship the ``readline``
            module.
    """
    hook = _require_hook(function, "function")
    _require_function("set_completion_display_matches_hook")(hook)


def get_completion_type() -> int:
    """Return the type of the completion that is attempted.

    Returns:
        Zero when no completion is attempted, one for a completion of a file
        name, and two for a completion of a host name.

    Raises:
        RuntimeError: If the interpreter does not ship the ``readline``
            module.
    """
    return int(_require_function("get_completion_type")())


def get_begidx() -> int:
    """Return the index the completion scope starts at.

    Returns:
        The index the completion scope starts at.

    Raises:
        RuntimeError: If the interpreter does not ship the ``readline``
            module.
    """
    return int(_require_function("get_begidx")())


def get_endidx() -> int:
    """Return the index the completion scope ends at.

    Returns:
        The index the completion scope ends at.

    Raises:
        RuntimeError: If the interpreter does not ship the ``readline``
            module.
    """
    return int(_require_function("get_endidx")())


def get_line_buffer() -> str:
    """Return the contents of the line buffer of the editor.

    Returns:
        The contents of the line buffer.

    Raises:
        RuntimeError: If the interpreter does not ship the ``readline``
            module.
    """
    return str(_require_function("get_line_buffer")())


def insert_text(text: Any) -> None:
    """Insert *text* into the line buffer at the cursor.

    Args:
        text: The text that is inserted.

    Raises:
        TypeError: If *text* is not a string.
        RuntimeError: If the interpreter does not ship the ``readline``
            module.
    """
    content = _require_text(text, "text")
    _require_function("insert_text")(content)


def redisplay() -> None:
    """Redraw the line buffer of the editor.

    Raises:
        RuntimeError: If the interpreter does not ship the ``readline``
            module.
    """
    _require_function("redisplay")()


def set_auto_history(enabled: Any) -> None:
    """Enable or disable the automatic history.

    When the automatic history is enabled, the line the user entered is added
    to the history by the editor itself.

    Args:
        enabled: Whether the automatic history is enabled.

    Raises:
        TypeError: If *enabled* is not a boolean.
        RuntimeError: If the interpreter does not ship the ``readline``
            module.
    """
    if not isinstance(enabled, bool):
        raise TypeError(f"enabled must be a bool, got {type(enabled).__name__}")
    _require_function("set_auto_history")(enabled)


def make_completer(words: Any) -> Callable[[str, int], Optional[str]]:
    """Return a completer for the words *words*.

    The completer follows the protocol of the standard library: it is called
    with the text that is completed and the number of the match that is
    wanted, and it returns the match or ``None`` when there is no further
    match.  The matches are sorted, so the completer offers the same match
    for the same text every time.

    Args:
        words: The words the completer offers.

    Returns:
        The completer.

    Raises:
        TypeError: If *words* is not an iterable of strings.
    """
    if isinstance(words, (str, bytes)):
        raise TypeError(f"words must be an iterable of strings, got {type(words).__name__}")
    try:
        candidates: List[str] = list(words)
    except TypeError as error:
        raise TypeError(
            f"words must be an iterable of strings, got {type(words).__name__}"
        ) from error
    for word in candidates:
        if not isinstance(word, str):
            raise TypeError(f"words must hold strings, got {type(word).__name__}")
    matches = sorted(set(candidates))

    def completer(text: str, state: int) -> Optional[str]:
        """Return the *state*-th match of *text*.

        Args:
            text: The text that is completed.
            state: The number of the match that is wanted.

        Returns:
            The match, or ``None`` when there is no further match.

        Raises:
            TypeError: If *text* is not a string or *state* is not an
                integer.
            ValueError: If *state* is negative.
        """
        prefix = _require_text(text, "text")
        if isinstance(state, bool) or not isinstance(state, int):
            raise TypeError(f"state must be an int, got {type(state).__name__}")
        if state < 0:
            raise ValueError(f"state must not be negative, got {state}")
        found = [word for word in matches if word.startswith(prefix)]
        if state >= len(found):
            return None
        return found[state]

    return completer
