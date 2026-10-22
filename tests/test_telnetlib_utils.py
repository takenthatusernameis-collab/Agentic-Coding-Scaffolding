"""Tests for the :mod:`telnetlib_utils` wrapper."""

from __future__ import annotations

import socket
import threading
import time
import warnings
from typing import Callable, Iterator, List

import pytest

import telnetlib_utils

#: Marks the tests that need the standard library module.
requires_telnetlib = pytest.mark.skipif(
    not telnetlib_utils.is_available(), reason="telnetlib module not available"
)


class _FakeTelnetServer:
    """A local server that answers like a telnet peer.

    The server binds a port of the loopback interface, so the tests never
    reach the network.
    """

    def __init__(
        self,
        greeting: bytes = b"",
        echo: bool = True,
        close_after_greeting: bool = False,
    ) -> None:
        """Start the server.

        Args:
            greeting: The bytes the server sends when a client connects.
            echo: Whether the server sends the data it received back.
            close_after_greeting: Whether the server closes the connection
                right after the greeting.
        """
        self._greeting = greeting
        self._echo = echo
        self._close_after_greeting = close_after_greeting
        self._received = bytearray()
        self._stop = threading.Event()
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind(("127.0.0.1", 0))
        self._server.listen(1)
        self._server.settimeout(0.2)
        self.port = int(self._server.getsockname()[1])
        self._thread = threading.Thread(target=self._serve, daemon=True)
        self._thread.start()

    def _serve(self) -> None:
        """Accept one client and answer it."""
        try:
            connection, _ = self._server.accept()
        except OSError:
            return
        with connection:
            if self._greeting:
                try:
                    connection.sendall(self._greeting)
                except OSError:
                    return
            if self._close_after_greeting:
                return
            connection.settimeout(0.2)
            while not self._stop.is_set():
                try:
                    data = connection.recv(4096)
                except socket.timeout:
                    continue
                except OSError:
                    break
                if not data:
                    break
                self._received.extend(data)
                if self._echo:
                    try:
                        connection.sendall(data)
                    except OSError:
                        break

    @property
    def received(self) -> bytes:
        """Return the data the server received so far."""
        return bytes(self._received)

    def wait_for(self, size: int, timeout: float = 5.0) -> bytes:
        """Wait until the server received *size* bytes and return them.

        Args:
            size: The number of bytes to wait for.
            timeout: The number of seconds to wait at most.

        Returns:
            The data the server received.
        """
        deadline = time.monotonic() + timeout
        while len(self._received) < size and time.monotonic() < deadline:
            time.sleep(0.01)
        return self.received

    def close(self) -> None:
        """Stop the server and release its port."""
        self._stop.set()
        try:
            self._server.close()
        except OSError:
            pass
        self._thread.join(timeout=5.0)


@pytest.fixture
def telnet_server() -> Iterator[Callable[..., _FakeTelnetServer]]:
    """Yield a factory that starts servers and stops them at the end."""
    servers: List[_FakeTelnetServer] = []

    def start(
        greeting: bytes = b"",
        echo: bool = True,
        close_after_greeting: bool = False,
    ) -> _FakeTelnetServer:
        server = _FakeTelnetServer(greeting, echo, close_after_greeting)
        servers.append(server)
        return server

    try:
        yield start
    finally:
        for server in servers:
            server.close()


@pytest.fixture
def client() -> Iterator[object]:
    """Yield a telnet client that is not connected."""
    if not telnetlib_utils.is_available():
        pytest.skip("telnetlib module not available")
    connection = telnetlib_utils.create_telnet()
    try:
        yield connection
    finally:
        telnetlib_utils.close(connection)


def test_is_available() -> None:
    """``is_available`` reports whether the module ships."""
    result = telnetlib_utils.is_available()
    assert isinstance(result, bool)


@requires_telnetlib
def test_the_constants_match_the_standard_library() -> None:
    """The re-exported constants are the constants of the standard library."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        import telnetlib

    for name in (
        "IAC",
        "DONT",
        "DO",
        "WONT",
        "WILL",
        "SE",
        "NOP",
        "DM",
        "BRK",
        "IP",
        "AO",
        "AYT",
        "EC",
        "EL",
        "GA",
        "SB",
        "theNULL",
    ):
        assert getattr(telnetlib_utils, name) == getattr(telnetlib, name)
    assert telnetlib_utils.TELNET_PORT == telnetlib.TELNET_PORT


@requires_telnetlib
def test_the_command_names_match_the_standard_library() -> None:
    """Every command of the wrapper is a command of the standard library."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        import telnetlib

    for number, name in telnetlib_utils.COMMANDS.items():
        assert getattr(telnetlib, name) == bytes([number])
    for name in ("SE", "NOP", "DM", "BRK", "IP", "AO", "AYT", "EC", "EL", "GA", "SB"):
        assert name in telnetlib_utils.COMMANDS.values()


@requires_telnetlib
def test_the_option_names_match_the_standard_library() -> None:
    """Every option of the wrapper is an option of the standard library."""
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        import telnetlib

    for number, name in telnetlib_utils.OPTIONS.items():
        assert getattr(telnetlib, name) == bytes([number])


def test_command_name_reports_the_name_of_a_command() -> None:
    """``command_name`` reports the name of a command."""
    assert telnetlib_utils.command_name(251) == "WILL"
    assert telnetlib_utils.command_name(b"\xfd") == "DO"


def test_command_name_reports_no_name_for_an_unknown_value() -> None:
    """A value that is no command has no name."""
    assert telnetlib_utils.command_name(10) is None


def test_option_name_reports_the_name_of_an_option() -> None:
    """``option_name`` reports the name of an option."""
    assert telnetlib_utils.option_name(1) == "ECHO"
    assert telnetlib_utils.option_name(b"\x12") == "LOGOUT"


def test_option_name_reports_no_name_for_an_unknown_value() -> None:
    """A value that is no option has no name."""
    assert telnetlib_utils.option_name(100) is None


def test_command_name_validates_its_argument() -> None:
    """``command_name`` rejects a value that is no byte."""
    with pytest.raises(TypeError):
        telnetlib_utils.command_name("WILL")  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        telnetlib_utils.command_name(256)
    with pytest.raises(ValueError):
        telnetlib_utils.command_name(b"\xff\xff")


def test_option_name_validates_its_argument() -> None:
    """``option_name`` rejects a value that is no byte."""
    with pytest.raises(TypeError):
        telnetlib_utils.option_name("ECHO")  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        telnetlib_utils.option_name(-1)


def test_escape_iac_doubles_the_command_byte() -> None:
    """``escape_iac`` doubles every byte that introduces a command."""
    assert telnetlib_utils.escape_iac(b"a\xffb") == b"a\xff\xffb"
    assert telnetlib_utils.escape_iac(b"plain") == b"plain"


def test_escape_iac_validates_its_argument() -> None:
    """``escape_iac`` rejects data that is not bytes."""
    with pytest.raises(TypeError):
        telnetlib_utils.escape_iac("text")  # type: ignore[arg-type]


def test_strip_iac_removes_a_command() -> None:
    """``strip_iac`` removes the commands of the protocol."""
    assert telnetlib_utils.strip_iac(b"text\xff\xf1more") == b"textmore"


def test_strip_iac_restores_an_escaped_byte() -> None:
    """``strip_iac`` restores a payload byte that was escaped."""
    assert telnetlib_utils.strip_iac(b"a\xff\xffb") == b"a\xffb"


def test_strip_iac_removes_a_negotiation() -> None:
    """``strip_iac`` removes a negotiation with the option it names."""
    assert telnetlib_utils.strip_iac(b"x\xff\xfb\x01y") == b"xy"


def test_strip_iac_removes_a_subnegotiation() -> None:
    """``strip_iac`` removes a subnegotiation as a whole."""
    data = b"before\xff\xfa\x01\xff\xf0after"
    assert telnetlib_utils.strip_iac(data) == b"beforeafter"


def test_strip_iac_keeps_the_text_of_a_subnegotiation_out() -> None:
    """A subnegotiation ends at the sequence that ends it."""
    data = b"before\xff\xfa\x01\xff\xff\x02\xff\xf0after"
    assert telnetlib_utils.strip_iac(data) == b"beforeafter"


def test_strip_iac_drops_an_unfinished_command() -> None:
    """A command byte at the end of the data is dropped."""
    assert telnetlib_utils.strip_iac(b"text\xff") == b"text"


def test_strip_iac_validates_its_argument() -> None:
    """``strip_iac`` rejects data that is not bytes."""
    with pytest.raises(TypeError):
        telnetlib_utils.strip_iac("text")  # type: ignore[arg-type]


def test_create_telnet_validates_its_arguments() -> None:
    """``create_telnet`` rejects arguments it cannot use."""
    with pytest.raises(TypeError):
        telnetlib_utils.create_telnet(123)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        telnetlib_utils.create_telnet("host", "port")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        telnetlib_utils.create_telnet("host", 23, "fast")  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        telnetlib_utils.create_telnet("host", 70000)


def test_connect_telnet_validates_its_arguments() -> None:
    """``connect_telnet`` rejects arguments it cannot use."""
    with pytest.raises(TypeError):
        telnetlib_utils.connect_telnet(123)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        telnetlib_utils.connect_telnet("host", "port")  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        telnetlib_utils.connect_telnet("host", -1)


def test_read_until_validates_its_arguments(client: object) -> None:
    """``read_until`` rejects a match that is not bytes."""
    with pytest.raises(TypeError):
        telnetlib_utils.read_until(client, "text")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        telnetlib_utils.read_until(client, b"text", "soon")  # type: ignore[arg-type]


def test_read_until_text_validates_its_arguments(client: object) -> None:
    """``read_until_text`` rejects a match that is not text."""
    with pytest.raises(TypeError):
        telnetlib_utils.read_until_text(client, b"text")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        telnetlib_utils.read_until_text(client, "text", encoding=123)  # type: ignore[arg-type]


def test_write_validates_its_arguments(client: object) -> None:
    """``write`` rejects data that is not bytes."""
    with pytest.raises(TypeError):
        telnetlib_utils.write(client, "text")  # type: ignore[arg-type]


def test_send_line_validates_its_arguments(client: object) -> None:
    """``send_line`` rejects a line that is not text."""
    with pytest.raises(TypeError):
        telnetlib_utils.send_line(client, 123)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        telnetlib_utils.send_line(client, "line", terminator=123)  # type: ignore[arg-type]


def test_expect_validates_its_arguments(client: object) -> None:
    """``expect`` rejects patterns that cannot match the data of a connection."""
    with pytest.raises(TypeError):
        telnetlib_utils.expect(client, "text")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        telnetlib_utils.expect(client, [b"ok", "text"])  # type: ignore[list-item]
    with pytest.raises(ValueError):
        telnetlib_utils.expect(client, [])
    with pytest.raises(TypeError):
        telnetlib_utils.expect(client, [b"ok"], "soon")  # type: ignore[arg-type]


def test_expect_text_validates_its_arguments(client: object) -> None:
    """``expect_text`` rejects patterns that are not text."""
    with pytest.raises(TypeError):
        telnetlib_utils.expect_text(client, [b"ok"])  # type: ignore[list-item]
    with pytest.raises(ValueError):
        telnetlib_utils.expect_text(client, [])


@requires_telnetlib
def test_the_readers_reject_a_client_that_is_not_a_client() -> None:
    """Every helper that needs a client rejects anything else."""
    with pytest.raises(TypeError):
        telnetlib_utils.read_until(object(), b"text")
    with pytest.raises(TypeError):
        telnetlib_utils.read_all(object())
    with pytest.raises(TypeError):
        telnetlib_utils.read_some(object())
    with pytest.raises(TypeError):
        telnetlib_utils.read_eager(object())
    with pytest.raises(TypeError):
        telnetlib_utils.read_lazy(object())
    with pytest.raises(TypeError):
        telnetlib_utils.read_very_eager(object())
    with pytest.raises(TypeError):
        telnetlib_utils.read_very_lazy(object())
    with pytest.raises(TypeError):
        telnetlib_utils.read_sb_data(object())
    with pytest.raises(TypeError):
        telnetlib_utils.write(object(), b"text")
    with pytest.raises(TypeError):
        telnetlib_utils.send_line(object(), "text")
    with pytest.raises(TypeError):
        telnetlib_utils.expect(object(), [b"text"])
    with pytest.raises(TypeError):
        telnetlib_utils.close(object())


@requires_telnetlib
def test_connect_telnet_connects_to_the_server(
    telnet_server: Callable[..., _FakeTelnetServer],
) -> None:
    """``connect_telnet`` opens a connection to the server."""
    server = telnet_server()
    connection = telnetlib_utils.connect_telnet("127.0.0.1", server.port, timeout=5.0)
    try:
        assert connection.get_socket() is not None
    finally:
        telnetlib_utils.close(connection)


@requires_telnetlib
def test_read_until_returns_the_data_up_to_the_match(
    telnet_server: Callable[..., _FakeTelnetServer],
) -> None:
    """``read_until`` returns the data that arrived up to the match."""
    server = telnet_server(greeting=b"welcome\r\n")
    connection = telnetlib_utils.connect_telnet("127.0.0.1", server.port, timeout=5.0)
    try:
        data = telnetlib_utils.read_until(connection, b"\r\n", timeout=5.0)
    finally:
        telnetlib_utils.close(connection)
    assert data == b"welcome\r\n"


@requires_telnetlib
def test_read_until_text_returns_the_data_as_text(
    telnet_server: Callable[..., _FakeTelnetServer],
) -> None:
    """``read_until_text`` returns the data that arrived as text."""
    server = telnet_server(greeting=b"welcome\r\n")
    connection = telnetlib_utils.connect_telnet("127.0.0.1", server.port, timeout=5.0)
    try:
        data = telnetlib_utils.read_until_text(connection, "\r\n", timeout=5.0)
    finally:
        telnetlib_utils.close(connection)
    assert data == "welcome\r\n"


@requires_telnetlib
def test_send_line_writes_the_line(
    telnet_server: Callable[..., _FakeTelnetServer],
) -> None:
    """``send_line`` writes the line and ends it."""
    server = telnet_server()
    connection = telnetlib_utils.connect_telnet("127.0.0.1", server.port, timeout=5.0)
    try:
        sent = telnetlib_utils.send_line(connection, "hello")
    finally:
        telnetlib_utils.close(connection)
    assert sent == len("hello\r\n")
    assert server.wait_for(7) == b"hello\r\n"


@requires_telnetlib
def test_write_reports_the_number_of_bytes_that_were_sent(
    telnet_server: Callable[..., _FakeTelnetServer],
) -> None:
    """``write`` reports the bytes that reached the peer."""
    server = telnet_server()
    connection = telnetlib_utils.connect_telnet("127.0.0.1", server.port, timeout=5.0)
    try:
        sent = telnetlib_utils.write(connection, b"a\xffb")
    finally:
        telnetlib_utils.close(connection)
    assert sent == 4
    assert server.wait_for(4) == b"a\xff\xffb"


@requires_telnetlib
def test_expect_returns_the_pattern_that_matched(
    telnet_server: Callable[..., _FakeTelnetServer],
) -> None:
    """``expect`` reports the pattern that matched and the data up to it."""
    server = telnet_server(greeting=b"login: ")
    connection = telnetlib_utils.connect_telnet("127.0.0.1", server.port, timeout=5.0)
    try:
        index, match, data = telnetlib_utils.expect(connection, [b"denied", b"login"], 5.0)
    finally:
        telnetlib_utils.close(connection)
    assert index == 1
    assert match is not None
    assert data == b"login"


@requires_telnetlib
def test_expect_text_returns_the_data_as_text(
    telnet_server: Callable[..., _FakeTelnetServer],
) -> None:
    """``expect_text`` reports the pattern that matched and the data as text."""
    server = telnet_server(greeting=b"login: ")
    connection = telnetlib_utils.connect_telnet("127.0.0.1", server.port, timeout=5.0)
    try:
        index, match, data = telnetlib_utils.expect_text(connection, ["login"], 5.0)
    finally:
        telnetlib_utils.close(connection)
    assert index == 0
    assert match is not None
    assert data == "login"


@requires_telnetlib
def test_expect_reports_no_pattern_when_none_matched(
    telnet_server: Callable[..., _FakeTelnetServer],
) -> None:
    """``expect`` reports that no pattern matched when the data never did."""
    server = telnet_server()
    connection = telnetlib_utils.connect_telnet("127.0.0.1", server.port, timeout=5.0)
    try:
        index, match, data = telnetlib_utils.expect(connection, [b"never"], 0.2)
    finally:
        telnetlib_utils.close(connection)
    assert index == -1
    assert match is None
    assert data == b""


@requires_telnetlib
def test_read_all_reads_until_the_connection_is_closed(
    telnet_server: Callable[..., _FakeTelnetServer],
) -> None:
    """``read_all`` reads the data until the peer closes the connection."""
    server = telnet_server(greeting=b"the end", close_after_greeting=True)
    connection = telnetlib_utils.connect_telnet("127.0.0.1", server.port, timeout=5.0)
    try:
        data = telnetlib_utils.read_all(connection)
    finally:
        telnetlib_utils.close(connection)
    assert data == b"the end"


@requires_telnetlib
def test_the_client_answers_a_negotiation(
    telnet_server: Callable[..., _FakeTelnetServer],
) -> None:
    """The client of the standard library refuses the options it cannot do."""
    server = telnet_server(greeting=b"\xff\xfd\x01hello", echo=False)
    connection = telnetlib_utils.connect_telnet("127.0.0.1", server.port, timeout=5.0)
    try:
        data = telnetlib_utils.read_until(connection, b"hello", timeout=5.0)
    finally:
        telnetlib_utils.close(connection)
    received = server.wait_for(3)
    assert data == b"hello"
    assert received == b"\xff\xfc\x01"


@requires_telnetlib
def test_close_closes_the_connection(
    telnet_server: Callable[..., _FakeTelnetServer],
) -> None:
    """``close`` releases the connection of the client."""
    server = telnet_server()
    connection = telnetlib_utils.connect_telnet("127.0.0.1", server.port, timeout=5.0)
    telnetlib_utils.close(connection)
    assert connection.get_socket() is None


def test_degradation_without_module() -> None:
    """The helpers raise ``RuntimeError`` when the module is missing."""
    original = telnetlib_utils._telnetlib
    try:
        telnetlib_utils._telnetlib = None  # type: ignore[assignment]
        with pytest.raises(RuntimeError, match="telnetlib"):
            telnetlib_utils.create_telnet()
        with pytest.raises(RuntimeError, match="telnetlib"):
            telnetlib_utils.connect_telnet("host")
        with pytest.raises(RuntimeError, match="telnetlib"):
            telnetlib_utils.read_until(object(), b"text")
        with pytest.raises(RuntimeError, match="telnetlib"):
            telnetlib_utils.read_all(object())
        with pytest.raises(RuntimeError, match="telnetlib"):
            telnetlib_utils.write(object(), b"text")
        with pytest.raises(RuntimeError, match="telnetlib"):
            telnetlib_utils.close(object())
    finally:
        telnetlib_utils._telnetlib = original


def test_the_helpers_of_the_protocol_work_without_the_module() -> None:
    """The helpers that only work on the protocol keep working."""
    original = telnetlib_utils._telnetlib
    try:
        telnetlib_utils._telnetlib = None  # type: ignore[assignment]
        assert not telnetlib_utils.is_available()
        assert telnetlib_utils.escape_iac(b"\xff") == b"\xff\xff"
        assert telnetlib_utils.strip_iac(b"a\xff\xf1b") == b"ab"
        assert telnetlib_utils.command_name(255) == "IAC"
        assert telnetlib_utils.option_name(1) == "ECHO"
        assert telnetlib_utils.TELNET_PORT == 23
    finally:
        telnetlib_utils._telnetlib = original


def test_exports() -> None:
    """The module exports its public names."""
    for name in telnetlib_utils.__all__:
        assert hasattr(telnetlib_utils, name), name
