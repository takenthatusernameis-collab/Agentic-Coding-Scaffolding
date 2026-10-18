import datetime

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
