"""Tests for pipes_utils."""

import pipes_utils


def test_exports():
    for name in [
        "Template", "quote", "quote_command", "create_template",
        "is_available", "make_pipeline", "step_kinds",
    ]:
        assert hasattr(pipes_utils, name)
    assert pipes_utils.is_available() is True
    assert isinstance(pipes_utils.quote("foo"), str)
