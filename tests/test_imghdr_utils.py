"""Tests for imghdr_utils."""

import imghdr_utils


def test_exports():
    for name in ["what", "tests", "detect", "is_available", "is_image", "matching_formats",
                 "read_header", "register_test", "supported_formats", "unregister_test"]:
        assert hasattr(imghdr_utils, name)
