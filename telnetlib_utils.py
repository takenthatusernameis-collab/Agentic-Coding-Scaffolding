"""Telnet client utilities wrapping the standard library :mod:`telnetlib`."""

from __future__ import annotations

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
        def __init__(self, *args, **kwargs):
            raise RuntimeError("telnetlib module is not available")
    IAC = DONT = DO = WONT = WILL = SE = NOP = DM = BRK = IP = AO = AYT = EC = EL = GA = SB = theNULL = 255


def create_telnet(host: str | None = None, port: int = 23, timeout: float | None = None) -> Telnet:
    if not _TELNETLIB_AVAILABLE:
        raise RuntimeError("telnetlib module is not available")
    if host is not None and not isinstance(host, str):
        raise TypeError("host must be a str or None")
    if not isinstance(port, int) or isinstance(port, bool):
        raise TypeError("port must be an int")
    if timeout is not None and (not isinstance(timeout, (int, float)) or isinstance(timeout, bool)):
        raise TypeError("timeout must be a number or None")
    return Telnet(host, port, timeout)


def connect_telnet(host: str, port: int = 23, timeout: float | None = None) -> Telnet:
    tn = create_telnet(None, port, timeout)
    tn.open(host, port, timeout)
    return tn


def read_until(tn: Telnet, expected: bytes, timeout: float | None = None) -> bytes:
    if not isinstance(expected, (bytes, bytearray)):
        raise TypeError("expected must be bytes")
    return tn.read_until(bytes(expected), timeout)


def read_until_text(tn: Telnet, expected: str, timeout: float | None = None, encoding: str = "utf-8") -> str:
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


def expect(tn: Telnet, list_patterns, timeout: float | None = None):
    return tn.expect(list_patterns, timeout)


def expect_text(tn: Telnet, patterns: list[str], timeout: float | None = None, encoding: str = "utf-8"):
    pat = [p.encode(encoding) if isinstance(p, str) else p for p in patterns]
    return tn.expect(pat, timeout)


def close(tn: Telnet) -> None:
    tn.close()


def escape_iac(data: bytes) -> bytes:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes")
    b = bytes(data)
    return b.replace(bytes([IAC]), bytes([IAC, IAC]))


def strip_iac(data: bytes) -> bytes:
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("data must be bytes")
    b = bytes(data)
    result = bytearray()
    i = 0
    while i < len(b):
        if b[i] == IAC and i + 1 < len(b):
            cmd = b[i + 1]
            if cmd == IAC:
                result.append(IAC)
                i += 2
                continue
            if cmd in (DO, DONT, WILL, WONT):
                i += 3
                continue
            if cmd == SB:
                i += 2
                # skip until SE
                while i < len(b) and not (b[i] == IAC and i + 1 < len(b) and b[i + 1] == SE):
                    i += 1
                i += 2
                continue
            i += 2
            continue
        result.append(b[i])
        i += 1
    return bytes(result)


_COMMAND_NAMES = {
    IAC: "IAC", DONT: "DONT", DO: "DO", WONT: "WONT", WILL: "WILL",
    SE: "SE", NOP: "NOP", DM: "DM", BRK: "BRK", IP: "IP", AO: "AO",
    AYT: "AYT", EC: "EC", EL: "EL", GA: "GA", SB: "SB", theNULL: "NULL",
}


_OPTION_NAMES = {}


def command_name(cmd: int) -> str:
    if not isinstance(cmd, int) or isinstance(cmd, bool):
        raise TypeError("cmd must be an int")
    return _COMMAND_NAMES.get(cmd, str(cmd))


def option_name(opt: int) -> str:
    if not isinstance(opt, int) or isinstance(opt, bool):
        raise TypeError("opt must be an int")
    return _OPTION_NAMES.get(opt, str(opt))
