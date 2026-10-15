"""URL and web utility functions."""

from typing import Dict, List, Optional, Union
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse


def is_valid_url(url: str, schemes: Optional[List[str]] = None) -> bool:
    """Validate a URL string.

    Args:
        url: The URL string to validate.
        schemes: Optional list of allowed schemes (e.g. ``['http', 'https']``).
            If ``None``, any non-empty scheme is accepted.

    Returns:
        ``True`` if the URL is valid and uses an allowed scheme, ``False`` otherwise.
    """
    try:
        parsed = urlparse(url)
    except (ValueError, TypeError):
        return False
    if not parsed.scheme:
        return False
    if not parsed.netloc:
        return False
    if schemes is not None and parsed.scheme not in schemes:
        return False
    return True


def extract_domain(url: str) -> str:
    """Extract the hostname from a URL.

    Args:
        url: The URL string to extract the domain from.

    Returns:
        The hostname portion of the URL.

    Raises:
        ValueError: If the URL has no valid hostname.
    """
    parsed = urlparse(url)
    if not parsed.hostname:
        raise ValueError(f"URL has no valid domain: {url}")
    return parsed.hostname


def get_query_params(url: str) -> Dict[str, str]:
    """Get all query parameters from a URL as a flat dict.

    When a parameter appears multiple times, the first value is used.

    Args:
        url: The URL string to parse.

    Returns:
        A dict mapping query parameter names to their first value.
    """
    parsed = urlparse(url)
    params: Dict[str, str] = {}
    query_dict = parse_qs(parsed.query, keep_blank_values=True)
    for key, values in query_dict.items():
        params[key] = values[0]
    return params


def get_query_param(url: str, key: str) -> Optional[str]:
    """Get a single query parameter value from a URL.

    Args:
        url: The URL string to parse.
        key: The query parameter name to look up.

    Returns:
        The first value for the given key, or ``None`` if the key is absent.
    """
    params = get_query_params(url)
    return params.get(key)


def add_query_param(url: str, key: str, value: Union[str, int, float]) -> str:
    """Add or update a query parameter in a URL.

    Args:
        url: The URL string to modify.
        key: The query parameter name.
        value: The query parameter value (converted to string).

    Returns:
        The updated URL with the query parameter set.
    """
    parsed = urlparse(url)
    params = get_query_params(url)
    params[key] = str(value)
    new_query = urlencode(params)
    return urlunparse(parsed._replace(query=new_query))


def remove_query_param(url: str, key: str) -> str:
    """Remove a query parameter from a URL.

    If the parameter does not exist, the URL is returned unchanged.

    Args:
        url: The URL string to modify.
        key: The query parameter name to remove.

    Returns:
        The URL with the specified query parameter removed.
    """
    parsed = urlparse(url)
    params = get_query_params(url)
    params.pop(key, None)
    new_query = urlencode(params) if params else ""
    return urlunparse(parsed._replace(query=new_query))


def build_url(
    scheme: str = "https",
    domain: str = "",
    path: str = "",
    port: Optional[int] = None,
    params: Optional[Dict[str, Union[str, int, float]]] = None,
) -> str:
    """Build a URL from its individual components.

    Args:
        scheme: URL scheme (e.g. ``'http'``, ``'https'``).
        domain: The domain or host name.
        path: Path component (should start with ``'/'``).
        port: Optional port number appended to the domain.
        params: Optional query parameters dict.

    Returns:
        The constructed URL string.

    Raises:
        ValueError: If ``domain`` is empty.
    """
    if not domain:
        raise ValueError("domain is required")
    netloc = domain
    if port is not None:
        netloc = f"{domain}:{port}"
    query = ""
    if params:
        query = urlencode(params)
    return urlunparse((scheme, netloc, path, "", query, ""))
