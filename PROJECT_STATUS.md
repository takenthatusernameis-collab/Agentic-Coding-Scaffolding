"""Tests for unicodedata_utils."""

from unicodedata_utils import (
    unicodedata_bidirectional,
    unicodedata_category,
    unicodedata_combining,
    unicodedata_decimal,
    unicodedata_digit,
    unicodedata_east_asian_width,
    unicodedata_lookup,
    unicodedata_mirrored,
    unicodedata_name,
    unicodedata_normalize,
    unicodedata_numeric,
)


def test_unicodedata_lookup():
    assert unicodedata_lookup("LATIN SMALL LETTER A") == "a"


def test_unicodedata_name():
    assert unicodedata_name("a") == "LATIN SMALL LETTER A"


def test_unicodedata_normalize():
    assert unicodedata_normalize("NFC", "a\u0301") == "\u00e1"


def test_unicodedata_category():
    assert unicodedata_category("a") == "Ll"


def test_unicodedata_bidirectional():
    assert unicodedata_bidirectional("a") == "L"


def test_unicodedata_combining():
    assert unicodedata_combining("\u0301") == 230


def test_unicodedata_east_asian_width():
    assert unicodedata_east_asian_width("a") == "Na"


def test_unicodedata_mirrored():
    assert unicodedata_mirrored("(") == 1


def test_unicodedata_decimal():
    assert unicodedata_decimal("\u0660") == 0


def test_unicodedata_digit():
    assert unicodedata_digit("\u0669") == 9


def test_unicodedata_numeric():
    assert unicodedata_numeric("\u00bd") == 0.5
""" filePath="/home/runner/work/Agentic-Coding-Scaffolding/Agentic-Coding-Scaffolding/tests/test_unicodedata_utils.py- Added `unicodedata_utils.py` wrapping stdlib `unicodedata` with `tests/test_unicodedata_utils.py`.
