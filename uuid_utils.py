"""UUID utility functions for generating and validating UUIDs."""

from __future__ import annotations

import uuid
from typing import List, Optional

__all__: List[str] = [
    "generate_uuid",
    "generate_uuid4",
    "generate_uuid1",
    "is_valid_uuid",
    "parse_uuid",
]


def generate_uuid(version: int = 4) -> str:
    """Generate a UUID string.

    Args:
        version: The UUID version to generate (1 or 4). Defaults to 4.

    Returns:
        A UUID string in standard format.

    Raises:
        ValueError: If version is not 1 or 4.

    Examples:
        >>> generate_uuid()
        'f47ac10b-58cc-4372-a567-0e02b2c3d479'
        >>> generate_uuid(version=4)
        'e3d55f30-d0aa-4c7c-b3a8-b2c7b1a6c0f1'
    """
    if version == 4:
        return str(uuid.uuid4())
    elif version == 1:
        return str(uuid.uuid1())
    else:
        raise ValueError("UUID version must be 1 or 4")


def generate_uuid4() -> str:
    """Generate a UUID4 string.

    Returns:
        A UUID4 string.

    Examples:
        >>> generate_uuid4()
        'f47ac10b-58cc-4372-a567-0e02b2c3d479'
    """
    return str(uuid.uuid4())


def generate_uuid1() -> str:
    """Generate a UUID1 string.

    Returns:
        A UUID1 string.

    Examples:
        >>> generate_uuid1()
        'e3d55f30-d0aa-4c7c-b3a8-b2c7b1a6c0f1'
    """
    return str(uuid.uuid1())


def is_valid_uuid(uuid_str: str, version: Optional[int] = None) -> bool:
    """Check if a string is a valid UUID.

    Args:
        uuid_str: The string to validate.
        version: Optional UUID version to check against.

    Returns:
        True if valid UUID, False otherwise.

    Examples:
        >>> is_valid_uuid('f47ac10b-58cc-4372-a567-0e02b2c3d479')
        True
        >>> is_valid_uuid('not-a-uuid')
        False
        >>> is_valid_uuid('f47ac10b-58cc-4372-a567-0e02b2c3d479', version=4)
        True
    """
    try:
        parsed = uuid.UUID(uuid_str)
        if version is not None:
            return parsed.version == version
        return True
    except (ValueError, AttributeError, TypeError):
        return False


def parse_uuid(uuid_str: str) -> uuid.UUID:
    """Parse a UUID string into a UUID object.

    Args:
        uuid_str: The UUID string to parse.

    Returns:
        A UUID object.

    Raises:
        ValueError: If the string is not a valid UUID.

    Examples:
        >>> u = parse_uuid('f47ac10b-58cc-4372-a567-0e02b2c3d479')
        >>> u.version
        4
    """
    return uuid.UUID(uuid_str)
