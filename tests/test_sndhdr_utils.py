"""Tests for sndhdr_utils."""

import sndhdr_utils


def test_exports():
    for name in ["what", "whathdr", "tests", "is_available"]:
        assert hasattr(sndhdr_utils, name)
