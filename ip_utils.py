"""IP address utility functions."""

import ipaddress


def is_valid_ip(ip_str: str) -> bool:
    """Check if a string is a valid IP address (IPv4 or IPv6)."""
    try:
        ipaddress.ip_address(ip_str)
        return True
    except (ValueError, TypeError):
        return False


def is_valid_ipv4(ip_str: str) -> bool:
    """Check if a string is a valid IPv4 address."""
    try:
        ipaddress.IPv4Address(ip_str)
        return True
    except (ValueError, TypeError):
        return False


def is_valid_ipv6(ip_str: str) -> bool:
    """Check if a string is a valid IPv6 address."""
    try:
        ipaddress.IPv6Address(ip_str)
        return True
    except (ValueError, TypeError):
        return False


def get_ip_version(ip_str: str) -> int:
    """Get the IP version (4 or 6) of an IP address."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.version
    except (ValueError, TypeError):
        raise ValueError(f"Invalid IP address: {ip_str}")


def ip_to_int(ip_str: str) -> int:
    """Convert an IP address string to an integer."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return int(ip)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid IP address: {ip_str}")


def int_to_ip(num: int, version: int = 4) -> str:
    """Convert an integer to an IP address string."""
    try:
        if version == 4:
            return str(ipaddress.IPv4Address(num))
        elif version == 6:
            return str(ipaddress.IPv6Address(num))
        else:
            raise ValueError("Version must be 4 or 6")
    except (ValueError, TypeError):
        raise ValueError(f"Invalid integer for IP {version}: {num}")


def is_private_ip(ip_str: str) -> bool:
    """Check if an IP address is private."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private
    except (ValueError, TypeError):
        raise ValueError(f"Invalid IP address: {ip_str}")


def is_loopback_ip(ip_str: str) -> bool:
    """Check if an IP address is loopback."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_loopback
    except (ValueError, TypeError):
        raise ValueError(f"Invalid IP address: {ip_str}")


def is_multicast_ip(ip_str: str) -> bool:
    """Check if an IP address is multicast."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_multicast
    except (ValueError, TypeError):
        raise ValueError(f"Invalid IP address: {ip_str}")


def is_link_local_ip(ip_str: str) -> bool:
    """Check if an IP address is link-local."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_link_local
    except (ValueError, TypeError):
        raise ValueError(f"Invalid IP address: {ip_str}")


def is_reserved_ip(ip_str: str) -> bool:
    """Check if an IP address is reserved."""
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_reserved
    except (ValueError, TypeError):
        raise ValueError(f"Invalid IP address: {ip_str}")


def normalize_ip(ip_str: str) -> str:
    """Normalize an IP address to its canonical form."""
    try:
        if isinstance(ip_str, str):
            # Handle IPv4 with leading zeros
            if '.' in ip_str and ':' not in ip_str:
                # IPv4
                parts = ip_str.split('.')
                if all(part.isdigit() for part in parts):
                    parts = [str(int(p)) for p in parts if p]
                    ip_str_clean = '.'.join(parts)
                else:
                    ip_str_clean = ip_str
            else:
                ip_str_clean = ip_str
        else:
            ip_str_clean = ip_str
        ip = ipaddress.ip_address(ip_str_clean)
        # For IPv4-mapped IPv6, return the IPv4 form if that's more readable
        if ip.version == 6:
            try:
                if ip.ipv4_mapped:
                    return str(ip.ipv4_mapped)
            except AttributeError:
                pass
        return str(ip)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid IP address: {ip_str}")


def in_subnet(ip_str: str, network: str) -> bool:
    """Check if an IP address is in a subnet."""
    try:
        ip = ipaddress.ip_address(ip_str)
        net = ipaddress.ip_network(network, strict=False)
        return ip in net
    except (ValueError, TypeError):
        raise ValueError("Invalid IP address or network")


__all__ = [
    "is_valid_ip",
    "is_valid_ipv4",
    "is_valid_ipv6",
    "get_ip_version",
    "ip_to_int",
    "int_to_ip",
    "is_private_ip",
    "is_loopback_ip",
    "is_multicast_ip",
    "is_link_local_ip",
    "is_reserved_ip",
    "normalize_ip",
    "in_subnet",
]
