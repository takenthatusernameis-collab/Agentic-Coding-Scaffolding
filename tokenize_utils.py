"""Utilities for Python source tokenization (wrapping :mod:`tokenize`).

The :mod:`tokenize` module turns Python source code into a stream of tokens.
This wrapper exposes a small, validated surface over that functionality so
callers can tokenize in-memory sources or files, look token types up by name,
and rebuild source text from a token stream.
"""

from __future__ import annotations

import io
import keyword
import token as _token
import tokenize as _tokenize
from collections.abc import Iterable
from pathlib import Path
from typing import Any, Callable, List, Tuple, Union

__all__ = [
    "TokenInfo",
    "tokenize_source",
    "tokenize_file",
    "generate_tokens",
    "untokenize",
    "token_name",
    "token_type",
    "detect_encoding",
    "significant_tokens",
    "is_comment",
    "is_string",
    "is_number",
    "is_name",
    "is_keyword",
]

# The token record produced by the standard library tokenizer.
TokenInfo = _tokenize.TokenInfo

# Token types that carry no meaning for Python code itself.
_IGNORED_TOKEN_TYPES = frozenset(
    {
        _tokenize.COMMENT,
        _tokenize.NL,
        _tokenize.ENCODING,
        _tokenize.INDENT,
        _tokenize.DEDENT,
        _tokenize.ENDMARKER,
    }
)


def _require_text(value: object, name: str = "source") -> str:
    """Return *value* when it is a string, otherwise raise ``TypeError``."""
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string, got {type(value).__name__}")
    return value


def _require_callable(value: object, name: str) -> Callable[..., Any]:
    """Return *value* when it is callable, otherwise raise ``TypeError``."""
    if not callable(value):
        raise TypeError(f"{name} must be callable, got {type(value).__name__}")
    return value


def tokenize_source(source: str) -> List[TokenInfo]:
    """Tokenize *source* text and return the resulting token list.

    Args:
        source: Python source code to tokenize.

    Returns:
        The tokens produced by :func:`tokenize.generate_tokens`.

    Raises:
        TypeError: If *source* is not a string.
    """
    text = _require_text(source)
    return list(_tokenize.generate_tokens(io.StringIO(text).readline))


def tokenize_file(path: Union[str, Path]) -> List[TokenInfo]:
    """Tokenize the Python source file at *path*.

    The file is decoded using the encoding declared by its cookie or by the
    PEP 263 default, exactly as the standard library tokenizer does.

    Args:
        path: Path of the file to tokenize.

    Returns:
        The tokens produced by :func:`tokenize.generate_tokens`.

    Raises:
        TypeError: If *path* is neither a string nor a path-like object.
        FileNotFoundError: If *path* does not exist.
    """
    if not isinstance(path, (str, Path)):
        raise TypeError(f"path must be a string or Path, got {type(path).__name__}")
    file_path = Path(path)
    with _tokenize.open(file_path) as handle:
        text = handle.read()
    return tokenize_source(text)


def generate_tokens(readline: Callable[[], str]) -> Iterable[TokenInfo]:
    """Yield tokens from a *readline* callable.

    Args:
        readline: Callable returning one line of source at a time.

    Returns:
        An iterator of tokens.

    Raises:
        TypeError: If *readline* is not callable.
    """
    reader = _require_callable(readline, "readline")
    return _tokenize.generate_tokens(reader)


def untokenize(tokens: Iterable[Any]) -> str:
    """Rebuild source text from a stream of tokens.

    Args:
        tokens: Tokens produced by :func:`tokenize_source` or
            :func:`generate_tokens`.

    Returns:
        The reconstructed source text.

    Raises:
        TypeError: If *tokens* is not iterable.
    """
    if not isinstance(tokens, Iterable):
        raise TypeError(f"tokens must be iterable, got {type(tokens).__name__}")
    return _tokenize.untokenize(list(tokens))


def token_name(token_type: int) -> str:
    """Return the human readable name of *token_type*.

    Args:
        token_type: Numeric token type, such as ``token.NAME``.

    Returns:
        The token name, or ``"UNKNOWN"`` when the type is not registered.

    Raises:
        TypeError: If *token_type* is not an integer.
    """
    if isinstance(token_type, bool) or not isinstance(token_type, int):
        raise TypeError(f"token_type must be an int, got {type(token_type).__name__}")
    return _token.tok_name.get(token_type, "UNKNOWN")


def token_type(name: str) -> int:
    """Return the numeric token type registered under *name*.

    Args:
        name: Token name, such as ``"NAME"``.

    Returns:
        The numeric token type.

    Raises:
        TypeError: If *name* is not a string.
        KeyError: If *name* is not a known token name.
    """
    text = _require_text(name, "name")
    exact = _token.EXACT_TOKEN_TYPES.get(text)
    if exact is not None:
        return exact
    for value, known in _token.tok_name.items():
        if known == text:
            return value
    raise KeyError(f"unknown token name: {text!r}")


def detect_encoding(readline: Callable[[], bytes]) -> Tuple[str, List[bytes]]:
    """Detect the source encoding declared by a byte stream.

    Args:
        readline: Callable returning one line of bytes at a time.

    Returns:
        A tuple of the detected encoding and the lines that were read.

    Raises:
        TypeError: If *readline* is not callable.
    """
    reader = _require_callable(readline, "readline")
    encoding, lines = _tokenize.detect_encoding(reader)
    return encoding, list(lines)


def significant_tokens(tokens: Iterable[TokenInfo]) -> List[TokenInfo]:
    """Return the tokens of *tokens* that carry meaning for Python code.

    Comments, blank lines, encoding markers, indentation markers and the end
    marker are removed from the stream.

    Args:
        tokens: Tokens to filter.

    Returns:
        The filtered token list.

    Raises:
        TypeError: If *tokens* is not iterable.
    """
    if not isinstance(tokens, Iterable):
        raise TypeError(f"tokens must be iterable, got {type(tokens).__name__}")
    return [tok for tok in tokens if tok.type not in _IGNORED_TOKEN_TYPES]


def is_comment(token: TokenInfo) -> bool:
    """Return ``True`` when *token* is a comment token."""
    return token.type == _tokenize.COMMENT


def is_string(token: TokenInfo) -> bool:
    """Return ``True`` when *token* is a string literal token."""
    return token.type == _tokenize.STRING


def is_number(token: TokenInfo) -> bool:
    """Return ``True`` when *token* is a numeric literal token."""
    return token.type == _tokenize.NUMBER


def is_name(token: TokenInfo) -> bool:
    """Return ``True`` when *token* is a name token."""
    return token.type == _tokenize.NAME


def is_keyword(token: TokenInfo) -> bool:
    """Return ``True`` when *token* is a name token holding a Python keyword."""
    return token.type == _tokenize.NAME and keyword.iskeyword(token.string)
