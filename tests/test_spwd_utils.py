"""Tests for spwd_utils."""

import spwd_utils


def test_exports():
    for name in ["getspnam", "getspall", "is_available"]:
        assert hasattr(spwd_utils, name)
