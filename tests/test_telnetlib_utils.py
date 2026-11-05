"""Tests for telnetlib_utils."""

import telnetlib_utils


def test_exports():
    for name in ["Telnet", "IAC", "create_telnet", "connect_telnet", "read_until",
                 "read_until_text", "read_all", "write", "send_line", "expect",
                 "expect_text", "close", "escape_iac", "strip_iac", "command_name",
                 "option_name", "is_available"]:
        assert hasattr(telnetlib_utils, name)
