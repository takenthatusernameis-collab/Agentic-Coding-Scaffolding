"""Utilities for Python token constants (wrapping :mod:`token`)."""

import token as _token


def is_eof(tok):
    """Return ``True`` if *tok* is an end-of-file token."""
    return _token.ISEOF(tok)


def is_nonterminal(tok):
    """Return ``True`` if *tok* is a non-terminal token."""
    return _token.ISNONTERMINAL(tok)


def is_terminal(tok):
    """Return ``True`` if *tok* is a terminal token."""
    return _token.ISTERMINAL(tok)


def tok_name():
    """Return a copy of the token-name mapping."""
    return dict(_token.tok_name)


def exact_token_types():
    """Return a copy of the exact token type mapping."""
    return dict(_token.EXACT_TOKEN_TYPES)


def n_tokens():
    """Return the number of token types."""
    return _token.N_TOKENS


def nt_offset():
    """Return the non-terminal offset."""
    return _token.NT_OFFSET
