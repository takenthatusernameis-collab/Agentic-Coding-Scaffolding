"""Regular expression utility functions wrapping the :mod:`re` module.

Provides convenient helpers for common regex operations with type validation.
"""

import re
from typing import Callable, List, Optional, Tuple, Union


def find_all(pattern: Union[str, re.Pattern], text: str) -> List[str]:
    """Find all non-overlapping matches of a pattern in text."""
    if isinstance(pattern, str):
        compiled = re.compile(pattern)
    elif isinstance(pattern, re.Pattern):
        compiled = pattern
    else:
        raise TypeError("pattern must be str or re.Pattern")
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return compiled.findall(text)


def find_matches(pattern: Union[str, re.Pattern], text: str) -> List[re.Match]:
    """Find all matches returning Match objects."""
    if isinstance(pattern, str):
        compiled = re.compile(pattern)
    elif isinstance(pattern, re.Pattern):
        compiled = pattern
    else:
        raise TypeError("pattern must be str or re.Pattern")
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return list(compiled.finditer(text))


def search(pattern: Union[str, re.Pattern], text: str) -> Optional[re.Match]:
    """Search for a pattern in text."""
    if isinstance(pattern, str):
        compiled = re.compile(pattern)
    elif isinstance(pattern, re.Pattern):
        compiled = pattern
    else:
        raise TypeError("pattern must be str or re.Pattern")
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return compiled.search(text)


def match(pattern: Union[str, re.Pattern], text: str) -> Optional[re.Match]:
    """Match pattern at beginning of text."""
    if isinstance(pattern, str):
        compiled = re.compile(pattern)
    elif isinstance(pattern, re.Pattern):
        compiled = pattern
    else:
        raise TypeError("pattern must be str or re.Pattern")
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return compiled.match(text)


def full_match(pattern: Union[str, re.Pattern], text: str) -> Optional[re.Match]:
    """Match pattern against entire text."""
    if isinstance(pattern, str):
        compiled = re.compile(pattern)
    elif isinstance(pattern, re.Pattern):
        compiled = pattern
    else:
        raise TypeError("pattern must be str or re.Pattern")
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return compiled.fullmatch(text)


def split(
    pattern: Union[str, re.Pattern], text: str, maxsplit: int = 0
) -> List[str]:
    """Split text by pattern."""
    if isinstance(pattern, str):
        compiled = re.compile(pattern)
    elif isinstance(pattern, re.Pattern):
        compiled = pattern
    else:
        raise TypeError("pattern must be str or re.Pattern")
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(maxsplit, int) or isinstance(maxsplit, bool):
        raise TypeError("maxsplit must be an integer")
    return compiled.split(text, maxsplit=maxsplit)


def sub(
    pattern: Union[str, re.Pattern],
    repl: Union[str, Callable],
    text: str,
    count: int = 0,
) -> str:
    """Substitute pattern in text."""
    if isinstance(pattern, str):
        compiled = re.compile(pattern)
    elif isinstance(pattern, re.Pattern):
        compiled = pattern
    else:
        raise TypeError("pattern must be str or re.Pattern")
    if not (isinstance(repl, str) or callable(repl)):
        raise TypeError("repl must be str or callable")
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(count, int) or isinstance(count, bool):
        raise TypeError("count must be an integer")
    return compiled.sub(repl, text, count=count)


def subn(
    pattern: Union[str, re.Pattern],
    repl: Union[str, Callable],
    text: str,
    count: int = 0,
) -> Tuple[str, int]:
    """Substitute pattern returning (new_text, number_of_subs)."""
    if isinstance(pattern, str):
        compiled = re.compile(pattern)
    elif isinstance(pattern, re.Pattern):
        compiled = pattern
    else:
        raise TypeError("pattern must be str or re.Pattern")
    if not (isinstance(repl, str) or callable(repl)):
        raise TypeError("repl must be str or callable")
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    if not isinstance(count, int) or isinstance(count, bool):
        raise TypeError("count must be an integer")
    return compiled.subn(repl, text, count=count)


def compile_regex(pattern: str, flags: int = 0) -> re.Pattern:
    """Compile a regex pattern."""
    if not isinstance(pattern, str):
        raise TypeError("pattern must be a string")
    if not isinstance(flags, int) or isinstance(flags, bool):
        raise TypeError("flags must be an integer")
    return re.compile(pattern, flags=flags)


def escape(string: str) -> str:
    """Escape regex special characters in string."""
    if not isinstance(string, str):
        raise TypeError("string must be a string")
    return re.escape(string)
