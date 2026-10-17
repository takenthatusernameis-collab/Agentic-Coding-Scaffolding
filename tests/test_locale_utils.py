"""Tests for locale_utils module."""

import locale_utils


def test_normalize_locale():
    assert locale_utils.normalize_locale("en-us") == "en_US"
    assert locale_utils.normalize_locale("EN_us") == "en_US"
    assert locale_utils.normalize_locale("fr") == "fr"


def test_language_code():
    assert locale_utils.language_code("en-US") == "en"
    assert locale_utils.language_code("zh_Hans") == "zh"


def test_region_code():
    assert locale_utils.region_code("en-US") == "US"
    assert locale_utils.region_code("fr") == ""


def test_is_valid_locale():
    assert locale_utils.is_valid_locale("en-US") is True
    assert locale_utils.is_valid_locale("fr") is True
    assert locale_utils.is_valid_locale("123") is False


def test_type_errors():
    for fn in (locale_utils.normalize_locale, locale_utils.language_code, locale_utils.region_code):
        try:
            fn(123)
        except TypeError:
            pass
        else:
            raise AssertionError("expected TypeError")
    assert locale_utils.is_valid_locale(123) is False
