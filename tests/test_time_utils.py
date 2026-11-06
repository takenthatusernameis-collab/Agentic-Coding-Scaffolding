"""Tests for time_utils module."""

from datetime import datetime

import time_utils


def test_now_epoch_is_int():
    assert isinstance(time_utils.now_epoch(), int)


def test_now_iso_parseable():
    value = time_utils.now_iso()
    dt = datetime.fromisoformat(value)
    assert dt.tzinfo is not None


def test_epoch_roundtrip():
    ts = 1700000000
    iso = time_utils.epoch_to_iso(ts)
    assert time_utils.iso_to_epoch(iso) == ts


def test_iso_to_epoch_invalid():
    assert time_utils.iso_to_epoch("not-a-date") is None


def test_format_duration_zero():
    assert time_utils.format_duration(0) == "0s"


def test_format_duration_seconds():
    assert time_utils.format_duration(45) == "45s"


def test_format_duration_minutes():
    assert time_utils.format_duration(65) == "1m 5s"


def test_parse_duration_zero():
    assert time_utils.parse_duration("0s") == 0


def test_parse_duration_roundtrip():
    for s in [0, 45, 65, 3661, 7200]:
        assert time_utils.parse_duration(time_utils.format_duration(s)) == s


def test_parse_duration_type_error():
    try:
        time_utils.parse_duration(123)
    except TypeError:
        pass
    else:
        raise AssertionError("expected TypeError")


def test_parse_duration_value_error():
    try:
        time_utils.parse_duration("garbage")
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
    assert time_utils.format_duration(3661) == "1h 1m 1s"


def test_format_duration_type_error():
    try:
        time_utils.format_duration("x")
    except TypeError:
        return
    raise AssertionError("expected TypeError")


def test_format_duration_value_error():
    try:
        time_utils.format_duration(-1)
    except ValueError:
        return
    raise AssertionError("expected ValueError")
