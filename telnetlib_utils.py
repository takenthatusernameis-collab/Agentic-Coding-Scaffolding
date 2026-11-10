"""Telnet client utilities wrapping the standard library :mod:`telnetlib`."""

from __future__ import annotations

from typing import Any

try:
    import telnetlib as _telnetlib
    _TELNETLIB_AVAILABLE = True
except Exception:
    _telnetlib = None  # type: ignore[assignment]
    _TELNETLIB_AVAILABLE = False

__all__: list[str] = [
    "Telnet",
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
    "create_telnet",
    "connect_telnet",
    "read_until",
    "read_until_text",
    "read_all",
    "read_some",
    "read_eager",
    "read_very_eager",
    "read_lazy",
    "read_very_lazy",
    "read_sb_data",
    "write",
    "send_line",
    "expect",
    "expect_text",
    "close",
    "escape_iac",
    "strip_iac",
    "command_name",
    "option_name",
    "is_available",
]


def is_available() -> bool:
    """Return True if the standard library :mod:`telnetlib` module is available."""
    return _TELNETLIB_AVAILABLE


if _TELNETLIB_AVAILABLE:
    Telnet = _telnetlib.Telnet
    IAC = _telnetlib.IAC
    DONT = _telnetlib.DONT
    DO = _telnetlib.DO
    WONT = _telnetlib.WONT
    WILL = _telnetlib.WILL
    SE = _telnetlib.SE
    NOP = _telnetlib.NOP
    DM = _telnetlib.DM
    BRK = _telnetlib.BRK
    IP = _telnetlib.IP
    AO = _telnetlib.AO
    AYT = _telnetlib.AYT
    EC = _telnetlib.EC
    EL = _telnetlib.EL
    GA = _telnetlib.GA
    SB = _telnetlib.SB
    theNULL = _telnetlib.theNULL
else:
    class Telnet:  # type: ignore[no-redef]
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            raise RuntimeError("telnetlib module is not available")

    _cmd = bytes([255])
    IAC = DONT = DO = WONT = WILL = SE = NOP = DM = BRK = IP = AO = AYT = EC = EL = GA = SB = theNULL = _cmd


def create_telnet(host: str | None = None, port: int = 23, timeout: float | None = None) -> Telnet:
    if not _TELNETLIB_AVAILABLE:
        raise RuntimeError("telnetlib module is not available")
    if host is not None and not isinstance(host, str):
        raise TypeError("host must be a str or None")
    if not isinstance(port, int) or isinstance(port, bool):
        raise TypeError("port must be an int")
    if timeout is not None and (not isinstance(timeout, (int, float)) or isinstance(timeout, bool)):
        raise TypeError("timeout must be a number or None")
    if host is None:
        return Telnet()
    if timeout is None:
        return Telnet(host, port)
    return Telnet(host, port, float(timeout))


def connect_telnet(host: str, port: int = 23, timeout: float | None = None) -> Telnet:
    tn = create_telnet(None, port, timeout)
    if timeout is None:
        tn.open(host, port)
    else:
        tn.open(host, port, float(timeout))
    return tn


def read_until(tn: Telnet, expected: bytes, timeout: float | None = None) -> bytes:
    if not isinstance(expected, (bytes, bytearray)):
        raise TypeError("expected must be bytes")
    return tn.read_until(bytes(expected), timeout)


def read_until_text(
    tn: Telnet,
    expected: str,
    timeout: float | None = None,
    encoding: str = "utf-8",
) -> str:
    if not isinstance(expected, str):
        raise TypeError("expected must be a str")
    data = read_until(tn, expected.encode(encoding), timeout)
    return data.decode(encoding, errors="replace")


def read_all(tn: Telnet) -> bytes:
    return tn.read_all()


def read_some(tn: Telnet) -> bytes:
    return tn.read_some()


def read_eager(tn: Telnet) -> bytes:
    return tn.read_eager()


def read_very_eager(tn: Telnet) -> bytes:
    return tn.read_very_eager()


def read_lazy(tn: Telnet) -> bytes:
    return tn.read_lazy()


def read_very_lazy(tn: Telnet) -> bytes:
    return tn.read_very_lazy()


def read_sb_data(tn: Telnet) -> bytes:
    return tn.read_sb_data()


def write(tn: Telnet, buffer: bytes) -> int:
    if not isinstance(buffer, (bytes, bytearray)):
        raise TypeError("buffer must be bytes")
    tn.write(bytes(buffer))
    return len(buffer)


def send_line(tn: Telnet, line: str | bytes, encoding: str = "utf-8") -> int:
    if isinstance(line, str):
        data = (line + "\r\n").encode(encoding)
    elif isinstance(line, (bytes, bytearray)):
        data = bytes(line) + b"\r\n"
    else:
        raise TypeError("line must be str or bytes")
    tn.write(data)
    return len(data)


def expect(tn: Telnet, list_patterns: Any, timeout: float | None = None) -> Any:
    return tn.expect(list_patterns, timeout)


def expect_text(
    tn: Telnet,
    patterns: list[str],
    timeout: float | None = None,
    encoding: str = "utf-8",
) -> Any:
    pat: list[Any] = [p.encode(encoding) if isinstance(p, str) else p for p in patterns]
    return tn.expect(pat, timeout)


def close(tn: Telnet) -> None:
    tn.close()


def escape_iac(data: bytes) -> bytes:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes")
    b = bytes(data)
    return b.replace(IAC, IAC + IAC)


def strip_iac(data: bytes) -> bytes:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes")
    b = bytes(data)
    iac = IAC[0]
    result = bytearray()
    i = 0
    while i < len(b):
        if b[i] == iac and i + 1 < len(b):
            cmd = b[i + 1]
            if cmd == iac:
                result.append(iac)
                i += 2
                continue
            if cmd in (DO[0], DONT[0], WILL[0], WONT[0]):
                i += 3
                continue
            if cmd == SB[0]:
                i += 2
                # skip until SE
                while i < len(b) and not (b[i] == iac and i + 1 < len(b) and b[i + 1] == SE[0]):
                    i += 1
                i += 2
                continue
            i += 2
            continue
        result.append(b[i])
        i += 1
    return bytes(result)


_COMMAND_NAMES: dict[int, str] = {
    IAC[0]: "IAC", DONT[0]: "DONT", DO[0]: "DO", WONT[0]: "WONT", WILL[0]: "WILL",
    SE[0]: "SE", NOP[0]: "NOP", DM[0]: "DM", BRK[0]: "BRK", IP[0]: "IP", AO[0]: "AO",
    AYT[0]: "AYT", EC[0]: "EC", EL[0]: "EL", GA[0]: "GA", SB[0]: "SB", theNULL[0]: "NULL",
}

_OPTION_NAMES: dict[int, str] = {}


def command_name(cmd: int) -> str:
    if not isinstance(cmd, int) or isinstance(cmd, bool):
        raise TypeError("cmd must be an int")
    return _COMMAND_NAMES.get(cmd, str(cmd))


def option_name(opt: int) -> str:
    if not isinstance(opt, int) or isinstance(opt, bool):
        raise TypeError("opt must be an int")
    return _OPTION_NAMES.get(opt, str(opt))
