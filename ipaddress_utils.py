"""IP address utilities wrapping the standard library :mod:`ipaddress` module.

The :mod:`ipaddress` module turns the text of an IPv4 or IPv6 address into an
object that compares, sorts, and computes with the address.  An address object
knows the network it belongs to, whether it is private or public, and how it
looks in its packed form.

This wrapper validates every argument before the standard library is reached,
so a caller gets a clear :class:`TypeError` or :class:`ValueError` instead of
an opaque failure.  It also adds the conveniences that the standard library
leaves to the caller: a validity check that never raises, the smallest set of
networks that still covers a list of networks, the length of the common
prefix of a list of addresses, the neighbour of an address, and a packed form
that can be read back.

The module is pure computation, so it works on every platform and never
touches the file system, the network, or a process.
"""

from __future__ import annotations

import ipaddress as _ipaddress
from typing import Iterable, Union

__all__: list[str] = [
    "AddressValueError",
    "IPv4Address",
    "IPv4Interface",
    "IPv4Network",
    "IPv6Address",
    "IPv6Interface",
    "IPv6Network",
    "NetmaskValueError",
    "address_version",
    "address_within",
    "common_prefix_length",
    "from_packed",
    "ip_address",
    "ip_interface",
    "ip_network",
    "is_valid_address",
    "is_valid_interface",
    "is_valid_network",
    "network_hosts",
    "network_overlaps",
    "next_address",
    "previous_address",
    "sort_addresses",
    "subnets",
    "summarize_addresses",
    "to_packed",
]

#: An address of either version.
Address = Union[_ipaddress.IPv4Address, _ipaddress.IPv6Address]

#: A network of either version.
Network = Union[_ipaddress.IPv4Network, _ipaddress.IPv6Network]

#: An interface of either version.
Interface = Union[_ipaddress.IPv4Interface, _ipaddress.IPv6Interface]

# The errors of the standard library are re-exported, so a caller can catch
# them without importing the standard library module.
AddressValueError = _ipaddress.AddressValueError
NetmaskValueError = _ipaddress.NetmaskValueError

# The address, network, and interface classes are re-exported, so a caller can
# build an object and check its type without importing the standard library.
IPv4Address = _ipaddress.IPv4Address
IPv6Address = _ipaddress.IPv6Address
IPv4Network = _ipaddress.IPv4Network
IPv6Network = _ipaddress.IPv6Network
IPv4Interface = _ipaddress.IPv4Interface
IPv6Interface = _ipaddress.IPv6Interface


def _check_address_like(value: object, name: str) -> None:
    """Raise when *value* is not a text, an integer, or a packed byte address.

    A boolean is rejected as well: it is an integer in Python, but it never
    names an address.
    """
    if isinstance(value, bool) or not isinstance(value, (str, int, bytes)):
        raise TypeError(
            f"{name} must be a str, an int, or bytes, got {type(value).__name__}"
        )


def _check_address_pair(value: object, name: str) -> None:
    """Raise when *value* is not an address or a pair of an address and a prefix length."""
    if not isinstance(value, tuple):
        _check_address_like(value, name)
        return
    if len(value) != 2:
        raise ValueError(f"{name} must hold two items, got {len(value)}")
    _check_address_like(value[0], name)
    if isinstance(value[1], bool) or not isinstance(value[1], int):
        raise TypeError(
            f"the prefix length must be an int, got {type(value[1]).__name__}"
        )


def _check_address(value: object, name: str) -> None:
    """Raise when *value* is not an address object of the standard library."""
    if not isinstance(value, (IPv4Address, IPv6Address)):
        raise TypeError(
            f"{name} must be an IPv4Address or an IPv6Address, got {type(value).__name__}"
        )


def _check_network(value: object, name: str) -> None:
    """Raise when *value* is not a network object of the standard library."""
    if not isinstance(value, (IPv4Network, IPv6Network)):
        raise TypeError(
            f"{name} must be an IPv4Network or an IPv6Network, got {type(value).__name__}"
        )


def _check_optional_count(value: object, name: str) -> None:
    """Raise when *value* is neither ``None`` nor a non-negative integer."""
    if value is None:
        return
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int or None, got {type(value).__name__}")
    if value < 0:
        raise ValueError(f"{name} must not be negative, got {value}")


def ip_address(address: str | int | bytes) -> Address:
    """Return the address object of *address*.

    Args:
        address: The address as text, such as ``"192.0.2.1"`` or ``"::1"``, as
            an integer, or as the packed bytes of the address.

    Returns:
        An :class:`IPv4Address` or an :class:`IPv6Address`.

    Raises:
        TypeError: If *address* is not a string, an integer, or bytes.
        ValueError: If *address* does not name a valid address.
    """
    _check_address_like(address, "address")
    return _ipaddress.ip_address(address)


def ip_network(
    address: str | int | bytes | tuple[str | int | bytes, int],
    strict: bool = True,
) -> Network:
    """Return the network object of *address*.

    Args:
        address: The network as text, such as ``"192.0.2.0/24"``, as an
            integer, as the packed bytes of the address, or as a pair of an
            address and a prefix length.
        strict: When ``True`` (the default) a network whose address holds
            bits outside of its prefix length is rejected.  When ``False``
            the address is masked with the prefix length instead.

    Returns:
        An :class:`IPv4Network` or an :class:`IPv6Network`.

    Raises:
        TypeError: If *address* has an unsupported type, or if *strict* is
            not a boolean.
        ValueError: If *address* does not name a valid network.
    """
    if not isinstance(strict, bool):
        raise TypeError(f"strict must be a bool, got {type(strict).__name__}")
    _check_address_pair(address, "address")
    return _ipaddress.ip_network(address, strict)


def ip_interface(address: str | int | bytes | tuple[str | int | bytes, int]) -> Interface:
    """Return the interface object of *address*.

    An interface is an address together with the prefix length of the network
    it belongs to, so ``"192.0.2.1/24"`` names the address ``192.0.2.1`` in
    the network ``192.0.2.0/24``.

    Args:
        address: The interface as text, as an integer, as the packed bytes of
            the address, or as a pair of an address and a prefix length.

    Returns:
        An :class:`IPv4Interface` or an :class:`IPv6Interface`.

    Raises:
        TypeError: If *address* has an unsupported type.
        ValueError: If *address* does not name a valid interface.
    """
    _check_address_pair(address, "address")
    return _ipaddress.ip_interface(address)


def is_valid_address(address: object) -> bool:
    """Report whether *address* names a valid address.

    Unlike :func:`ip_address` this check never raises, so it can be used on
    a value that comes from the outside without a guard around the call.

    Args:
        address: The value to check.

    Returns:
        ``True`` when *address* names a valid IPv4 or IPv6 address.
    """
    if isinstance(address, bool) or not isinstance(address, (str, int, bytes)):
        return False
    try:
        _ipaddress.ip_address(address)
    except ValueError:
        return False
    return True


def is_valid_network(address: object) -> bool:
    """Report whether *address* names a valid network.

    The check follows the strict rule of the standard library, so a network
    whose address holds bits outside of its prefix length is rejected.

    Args:
        address: The value to check.

    Returns:
        ``True`` when *address* names a valid IPv4 or IPv6 network.
    """
    if isinstance(address, bool) or not isinstance(address, (str, int, bytes)):
        return False
    try:
        _ipaddress.ip_network(address)
    except ValueError:
        return False
    return True


def is_valid_interface(address: object) -> bool:
    """Report whether *address* names a valid interface.

    Args:
        address: The value to check.

    Returns:
        ``True`` when *address* names a valid IPv4 or IPv6 interface.
    """
    if isinstance(address, bool) or not isinstance(address, (str, int, bytes)):
        return False
    try:
        _ipaddress.ip_interface(address)
    except ValueError:
        return False
    return True


def address_version(address: str | int | bytes) -> int:
    """Return the version of *address*.

    Args:
        address: The address as text, as an integer, or as packed bytes.

    Returns:
        ``4`` for an IPv4 address and ``6`` for an IPv6 address.

    Raises:
        TypeError: If *address* is not a string, an integer, or bytes.
        ValueError: If *address* does not name a valid address.
    """
    return ip_address(address).version


def to_packed(address: str | int | bytes) -> bytes:
    """Return the packed form of *address*.

    The packed form of an IPv4 address holds four bytes and the packed form of
    an IPv6 address holds sixteen bytes, in the network byte order.

    Args:
        address: The address as text, as an integer, or as packed bytes.

    Returns:
        The packed bytes of the address.

    Raises:
        TypeError: If *address* is not a string, an integer, or bytes.
        ValueError: If *address* does not name a valid address.
    """
    return ip_address(address).packed


def from_packed(packed: bytes) -> Address:
    """Return the address that *packed* holds.

    Args:
        packed: The packed bytes of the address, four bytes for IPv4 and
            sixteen bytes for IPv6.

    Returns:
        An :class:`IPv4Address` or an :class:`IPv6Address`.

    Raises:
        TypeError: If *packed* is not a bytes-like object.
        ValueError: If *packed* does not hold four or sixteen bytes.
    """
    if not isinstance(packed, (bytes, bytearray)):
        raise TypeError(f"packed must be bytes, got {type(packed).__name__}")
    if len(packed) == 4:
        return IPv4Address(bytes(packed))
    if len(packed) == 16:
        return IPv6Address(bytes(packed))
    raise ValueError(f"a packed address holds 4 or 16 bytes, got {len(packed)}")


def network_hosts(network: Network, limit: int | None = None) -> list[Address]:
    """Return the usable hosts of *network*.

    The network address and the broadcast address of an IPv4 network are not
    usable hosts.  A network of a single address and a network of two
    addresses hold no address that may be excluded, so every address of such a
    network is returned.

    Args:
        network: The network whose hosts are returned.
        limit: The largest number of hosts to return.  ``None`` (the default)
            returns every host, which materializes the whole range of a large
            network.

    Returns:
        The addresses of the hosts of the network, in ascending order.

    Raises:
        TypeError: If *network* is not a network object, or if *limit* is
            neither an integer nor ``None``.
        ValueError: If *limit* is negative.
    """
    _check_network(network, "network")
    _check_optional_count(limit, "limit")
    hosts: list[Address] = []
    for host in network.hosts():
        if limit is not None and len(hosts) >= limit:
            break
        hosts.append(host)
    return hosts


def subnets(
    network: Network,
    prefixlen_diff: int = 1,
    new_prefix: int | None = None,
) -> list[Network]:
    """Return the subnets of *network*.

    Args:
        network: The network that is split.
        prefixlen_diff: The number of bits the prefix length of the subnets
            grows by.  It must not be combined with *new_prefix*.
        new_prefix: The prefix length that every subnet of the network has.
            It must not be combined with *prefixlen_diff*.

    Returns:
        The subnets of the network, in ascending order.

    Raises:
        TypeError: If *network* is not a network object, or if one of the
            prefix lengths is neither an integer nor ``None``.
        ValueError: If *new_prefix* is shorter than the prefix length of the
            network, or if both prefix lengths are given.
    """
    _check_network(network, "network")
    if isinstance(prefixlen_diff, bool) or not isinstance(prefixlen_diff, int):
        raise TypeError(
            f"prefixlen_diff must be an int, got {type(prefixlen_diff).__name__}"
        )
    if new_prefix is not None and (
        isinstance(new_prefix, bool) or not isinstance(new_prefix, int)
    ):
        raise TypeError(f"new_prefix must be an int or None, got {type(new_prefix).__name__}")
    if new_prefix is not None and prefixlen_diff != 1:
        raise ValueError("prefixlen_diff and new_prefix must not be set together")
    if isinstance(network, IPv4Network):
        return list(network.subnets(prefixlen_diff=prefixlen_diff, new_prefix=new_prefix))
    return list(network.subnets(prefixlen_diff=prefixlen_diff, new_prefix=new_prefix))


def summarize_addresses(addresses: Iterable[Address | Network]) -> list[Network]:
    """Return the smallest set of networks that still covers *addresses*.

    A network that holds another network of the list is replaced by the
    larger one, and two networks that are the halves of a common network are
    replaced by that network.  An address is turned into the network that
    holds it alone.

    Args:
        addresses: The addresses and networks to summarize.

    Returns:
        The networks that cover the input, in ascending order.

    Raises:
        TypeError: If the list holds a value that is neither an address nor a
            network.
        ValueError: If the list holds addresses of different versions.
    """
    collected = list(addresses)
    if not collected:
        return []
    versions: set[int] = set()
    networks: list[Network] = []
    for item in collected:
        if isinstance(item, (IPv4Network, IPv6Network)):
            versions.add(item.version)
            networks.append(item)
        elif isinstance(item, (IPv4Address, IPv6Address)):
            versions.add(item.version)
            networks.append(_ipaddress.ip_network(f"{item}/{item.max_prefixlen}"))
        else:
            raise TypeError(
                f"addresses must hold addresses or networks, got {type(item).__name__}"
            )
    if len(versions) > 1:
        raise ValueError("addresses of different versions cannot be summarized together")
    summarized: list[Network] = []
    if versions == {4}:
        summarized.extend(
            _ipaddress.collapse_addresses(
                [item for item in networks if isinstance(item, IPv4Network)]
            )
        )
    else:
        summarized.extend(
            _ipaddress.collapse_addresses(
                [item for item in networks if isinstance(item, IPv6Network)]
            )
        )
    return summarized


def network_overlaps(first: Network, second: Network) -> bool:
    """Report whether two networks overlap.

    Two networks of different versions never overlap, because an IPv4 network
    and an IPv6 network hold disjoint addresses.

    Args:
        first: The first network.
        second: The second network.

    Returns:
        ``True`` when the networks hold at least one address in common.

    Raises:
        TypeError: If one of the networks is not a network object.
    """
    _check_network(first, "first")
    _check_network(second, "second")
    if first.version != second.version:
        return False
    return bool(first.overlaps(second))


def address_within(address: Address, network: Network) -> bool:
    """Report whether *address* lies inside *network*.

    An address of a different version never lies inside a network, because an
    IPv4 address and an IPv6 network hold disjoint addresses.

    Args:
        address: The address to look for.
        network: The network to look in.

    Returns:
        ``True`` when the network holds the address.

    Raises:
        TypeError: If *address* is not an address object, or if *network* is
            not a network object.
    """
    _check_address(address, "address")
    _check_network(network, "network")
    if address.version != network.version:
        return False
    return bool(address in network)


def common_prefix_length(addresses: Iterable[Address]) -> int:
    """Return the length of the common prefix of *addresses*.

    The common prefix is the longest sequence of leading bits that every
    address of the list shares.  Its length is the prefix length of the
    smallest network that holds every address of the list.

    Args:
        addresses: The addresses to compare.

    Returns:
        The number of leading bits the addresses share, which is 32 for IPv4
        and 128 for IPv6 at most.

    Raises:
        TypeError: If the list holds a value that is not an address object.
        ValueError: If the list is empty or holds addresses of different
            versions.
    """
    collected = list(addresses)
    if not collected:
        raise ValueError("at least one address is required")
    for item in collected:
        _check_address(item, "addresses")
    versions = {item.version for item in collected}
    if len(versions) > 1:
        raise ValueError("addresses of different versions have no common prefix")
    width = 32 if versions.pop() == 4 else 128
    base = int(collected[0])
    difference = 0
    for item in collected[1:]:
        difference |= base ^ int(item)
    return width - difference.bit_length()


def next_address(address: Address) -> Address:
    """Return the address that follows *address*.

    Args:
        address: The address to step from.

    Returns:
        The next address of the same version.

    Raises:
        TypeError: If *address* is not an address object.
        ValueError: If *address* is the last address of its version.
    """
    _check_address(address, "address")
    value = int(address) + 1
    if value >= 1 << address.max_prefixlen:
        raise ValueError(f"{address} is the last address of its version")
    if address.version == 4:
        return IPv4Address(value)
    return IPv6Address(value)


def previous_address(address: Address) -> Address:
    """Return the address that precedes *address*.

    Args:
        address: The address to step from.

    Returns:
        The previous address of the same version.

    Raises:
        TypeError: If *address* is not an address object.
        ValueError: If *address* is the first address of its version.
    """
    _check_address(address, "address")
    value = int(address) - 1
    if value < 0:
        raise ValueError(f"{address} is the first address of its version")
    if address.version == 4:
        return IPv4Address(value)
    return IPv6Address(value)


def sort_addresses(addresses: Iterable[Address]) -> list[Address]:
    """Return the addresses of *addresses* in ascending order.

    The addresses are sorted by their version first, so every IPv4 address
    comes before every IPv6 address, and by their numeric value afterwards.

    Args:
        addresses: The addresses to sort.

    Returns:
        The sorted addresses, as a new list.

    Raises:
        TypeError: If the list holds a value that is not an address object.
    """
    collected = list(addresses)
    for item in collected:
        _check_address(item, "addresses")
    return sorted(collected, key=lambda item: (item.version, int(item)))
