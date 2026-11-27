import datetime

import pytest

import email_utils


def test_formatdate_default():
    result = email_utils.email_formatdate()
    assert isinstance(result, str) and result


def test_formatdate_usegmt():
    result = email_utils.email_formatdate(usegmt=True)
    assert isinstance(result, str) and result


def test_formatdate_localtime():
    result = email_utils.email_formatdate(localtime=True)
    assert isinstance(result, str) and result


def test_parsedate():
    result = email_utils.email_parsedate("Wed, 21 Oct 2015 07:28:00 GMT")
    assert result is not None
    assert result[0] == 2015


def test_parsedate_invalid():
    assert email_utils.email_parsedate("not a date") is None


def test_parsedate_to_datetime():
    result = email_utils.email_parsedate_to_datetime("Wed, 21 Oct 2015 07:28:00 GMT")
    assert result is not None
    assert result.year == 2015


def test_parsedate_to_datetime_invalid():
    assert email_utils.email_parsedate_to_datetime("not a date") is None


def test_mktime_tz():
    t = (2015, 10, 21, 7, 28, 0, 0, 0, 0, 0)
    result = email_utils.email_mktime_tz(t)
    assert isinstance(result, float)


def test_parseaddr():
    name, addr = email_utils.email_parseaddr("User <user@example.com>")
    assert name == "User"
    assert addr == "user@example.com"


def test_parseaddr_strict_false():
    name, addr = email_utils.email_parseaddr("user@example.com", strict=False)
    assert addr == "user@example.com"


def test_formataddr():
    result = email_utils.email_formataddr(("User", "user@example.com"))
    assert "user@example.com" in result


def test_formataddr_charset():
    result = email_utils.email_formataddr(("User", "user@example.com"), charset="ascii")
    assert "user@example.com" in result


def test_getaddresses():
    result = email_utils.email_getaddresses(["User <user@example.com>"])
    assert result == [("User", "user@example.com")]


def test_make_msgid():
    result = email_utils.email_make_msgid()
    assert result.startswith("<")
    assert result.endswith(">")


def test_make_msgid_domain():
    result = email_utils.email_make_msgid(domain="example.com")
    assert "example.com" in result


def test_quote_unquote():
    quoted = email_utils.email_quote('hello "world"')
    assert isinstance(quoted, str)
    unquoted = email_utils.email_unquote(quoted)
    assert unquoted == 'hello "world"' or unquoted == 'hello \\"world\\"'


def test_format_datetime():
    dt = datetime.datetime(2015, 10, 21, 7, 28, 0, tzinfo=datetime.timezone.utc)
    result = email_utils.email_format_datetime(dt)
    assert "2015" in result
    assert "Oct" in result


def test_parsedate_rejects_non_string():
    with pytest.raises(AttributeError):
        email_utils.email_parsedate(42)  # type: ignore[arg-type]


def test_mktime_tz_rejects_short_tuple():
    with pytest.raises(IndexError):
        email_utils.email_mktime_tz((2015, 10, 21))  # type: ignore[arg-type]


def test_mktime_tz_rejects_empty_tuple():
    with pytest.raises(IndexError):
        email_utils.email_mktime_tz(())  # type: ignore[arg-type]


def test_mktime_tz_rejects_none():
    with pytest.raises(TypeError):
        email_utils.email_mktime_tz(None)  # type: ignore[arg-type]


def test_formataddr_rejects_none():
    with pytest.raises(TypeError):
        email_utils.email_formataddr(None)  # type: ignore[arg-type]


def test_formataddr_rejects_wrong_length_pair():
    with pytest.raises(ValueError):
        email_utils.email_formataddr(("User",))  # type: ignore[arg-type]


def test_formataddr_rejects_non_string_element():
    with pytest.raises(AttributeError):
        email_utils.email_formataddr(("User", 42))  # type: ignore[arg-type]


def test_make_msgid_rejects_non_string_idstring():
    with pytest.raises(TypeError):
        email_utils.email_make_msgid(idstring=42)  # type: ignore[arg-type]


def test_quote_rejects_non_string():
    with pytest.raises(AttributeError):
        email_utils.email_quote(None)  # type: ignore[arg-type]


def test_unquote_rejects_non_string():
    with pytest.raises(TypeError):
        email_utils.email_unquote(None)  # type: ignore[arg-type]


def test_getaddresses_rejects_non_iterable():
    with pytest.raises(TypeError):
        email_utils.email_getaddresses(None)  # type: ignore[arg-type]


def test_format_datetime_rejects_non_datetime():
    with pytest.raises(AttributeError):
        email_utils.email_format_datetime(None)  # type: ignore[arg-type]
    with pytest.raises(AttributeError):
        email_utils.email_format_datetime("not a datetime")  # type: ignore[arg-type]
    with pytest.raises(AttributeError):
        email_utils.email_format_datetime([])  # type: ignore[arg-type]


def test_parseaddr_rejects_empty_list():
    with pytest.raises(IndexError):
        email_utils.email_parseaddr([])  # type: ignore[arg-type]


def test_parseaddr_returns_empty_for_invalid_input():
    assert email_utils.email_parseaddr(None) == ("", "")
    assert email_utils.email_parseaddr(42) == ("", "")
    assert email_utils.email_parseaddr({}) == ("", "")
    assert email_utils.email_parseaddr(1.5) == ("", "")


def test_formataddr_accepts_non_string_charset():
    result = email_utils.email_formataddr(("User", "user@example.com"), charset=42)
    assert "user@example.com" in result


def test_getaddresses_iterates_string():
    result = email_utils.email_getaddresses("test")
    assert isinstance(result, list)


def test_make_msgid_accepts_non_string_domain():
    result = email_utils.email_make_msgid(domain=42)
    assert "42" in result


def test_parsedate_to_datetime_returns_none_for_errors():
    assert email_utils.email_parsedate_to_datetime(None) is None
    assert email_utils.email_parsedate_to_datetime(42) is None
    assert email_utils.email_parsedate_to_datetime("not a date") is None
