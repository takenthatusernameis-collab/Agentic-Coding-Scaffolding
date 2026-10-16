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
