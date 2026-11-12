"""Tests for telnetlib_utils."""

import types

import telnetlib_utils


def test_exports():
    for name in ["Telnet", "IAC", "create_telnet", "connect_telnet", "read_until",
                 "read_until_text", "read_all", "read_some", "read_eager",
                 "read_very_eager", "read_lazy", "read_very_lazy", "read_sb_data",
                 "write", "send_line", "expect", "expect_text", "close",
                 "escape_iac", "strip_iac", "command_name", "option_name",
                 "is_available"]:
        assert hasattr(telnetlib_utils, name), name


def _fake_telnet():
    """Return an object exposing the read methods the wrappers delegate to."""
    return types.SimpleNamespace(
        read_some=lambda: b"some",
        read_eager=lambda: b"eager",
        read_very_eager=lambda: b"very-eager",
        read_lazy=lambda: b"lazy",
        read_very_lazy=lambda: b"very-lazy",
        read_sb_data=lambda: b"sb-data",
    )


def test_read_wrappers_delegate_to_the_telnet_object():
    tn = _fake_telnet()
    assert telnetlib_utils.read_some(tn) == b"some"
    assert telnetlib_utils.read_eager(tn) == b"eager"
    assert telnetlib_utils.read_very_eager(tn) == b"very-eager"
    assert telnetlib_utils.read_lazy(tn) == b"lazy"
    assert telnetlib_utils.read_very_lazy(tn) == b"very-lazy"
    assert telnetlib_utils.read_sb_data(tn) == b"sb-data"
