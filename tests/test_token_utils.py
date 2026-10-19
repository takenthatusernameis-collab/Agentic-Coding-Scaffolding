"""Tests for token_utils."""

import token

from token_utils import (
    exact_token_types,
    is_eof,
    is_nonterminal,
    is_terminal,
    n_tokens,
    nt_offset,
    tok_name,
)


def test_is_eof():
    assert is_eof(token.ENDMARKER) is True
    assert is_eof(token.NAME) is False


def test_is_terminal():
    assert is_terminal(token.NAME) is True
    assert is_terminal(token.NT_OFFSET) is False


def test_is_nonterminal():
    assert is_nonterminal(token.NT_OFFSET) is True
    assert is_nonterminal(token.NAME) is False


def test_tok_name():
    assert tok_name()[token.NAME] == "NAME"


def test_exact_token_types():
    assert isinstance(exact_token_types(), dict)


def test_n_tokens():
    assert n_tokens() == token.N_TOKENS


def test_nt_offset():
    assert nt_offset() == token.NT_OFFSET
