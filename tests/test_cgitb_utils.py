"""Tests for cgitb_utils."""

import cgitb_utils


def test_exports():
    for name in ["enable", "disable", "reset", "lookup", "scanvars", "handler",
                 "text", "html", "small", "strong", "grey", "pink", "blue", "is_available"]:
        assert hasattr(cgitb_utils, name)
    assert cgitb_utils.is_available() is True
