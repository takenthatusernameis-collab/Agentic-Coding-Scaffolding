"""Typed configuration schema utilities.

This module provides declarative, typed configuration schemas for
validating, parsing, and serializing configuration dictionaries. A
:class:`SchemaField` describes a single typed configuration field, and a
:class:`ConfigSchema` composes fields into a schema that validates raw
configuration dictionaries, coerces values to declared types, applies
defaults, enforces required fields, and serializes back to plain
dictionaries.

Example:
    >>> schema = ConfigSchema(
    ...     [
    ...         SchemaField("host", str, default="localhost"),
    ...         SchemaField("port", int, default=8080, validator=range_validator(1, 65535)),
    ...         SchemaField("debug", bool, default=False),
    ...     ]
    ... )
    >>> config = schema.validate({"host": "example.com", "port": "9000"})
    >>> config["port"]
    9000
    >>> schema.validate({})["host"]
    'localhost'
"""

from __future__ import annotations

import re
from typing import Any, Callable, Dict, Iterable, List, Optional, TypeVar, Union
from urllib.parse import urlparse

T = TypeVar("T")

_UNSET: Any = object()

# A validator coerces and validates a raw value, returning the converted
# value or raising TypeError/ValueError when the value is invalid.
Validator = Callable[[Any], Any]


class ConfigValidationError(ValueError):
    """Raised when a configuration value fails schema validation."""


def int_validator(value: Any) -> int:
    """Validate and coerce *value* to an ``int``.

    Args:
        value: The value to validate.

    Returns:
        The value converted to an int.

    Raises:
        TypeError: If *value* is a bool or otherwise non-numeric.
        ValueError: If *value* is a float that is not a whole number or a
            string that cannot be parsed as an int.

    Examples:
        >>> int_validator("42")
        42
        >>> int_validator(7)
        7
    """
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise TypeError(f"cannot coerce {value!r} to int")
    if isinstance(value, float) and not value.is_integer():
        raise ValueError(f"float value {value!r} is not a whole number")
    try:
        return int(value)
    except (ValueError, TypeError) as exc:
        raise ValueError(f"cannot coerce {value!r} to int") from exc


def float_validator(value: Any) -> float:
    """Validate and coerce *value* to a ``float``.

    Args:
        value: The value to validate.

    Returns:
        The value converted to a float.

    Raises:
        TypeError: If *value* is a bool or otherwise non-numeric.
        ValueError: If *value* is a string that cannot be parsed as a float.

    Examples:
        >>> float_validator("3.14")
        3.14
        >>> float_validator(7)
        7.0
    """
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise TypeError(f"cannot coerce {value!r} to float")
    try:
        return float(value)
    except (ValueError, TypeError) as exc:
        raise ValueError(f"cannot coerce {value!r} to float") from exc


def str_validator(value: Any) -> str:
    """Validate that *value* is a ``str`` and return it unchanged.

    Args:
        value: The value to validate.

    Returns:
        The input string.

    Raises:
        TypeError: If *value* is not a string.

    Examples:
        >>> str_validator("hello")
        'hello'
    """
    if not isinstance(value, str):
        raise TypeError(f"expected a string, got {type(value).__name__}")
    return value


def bool_validator(value: Any) -> bool:
    """Validate and coerce *value* to a ``bool``.

    Accepts booleans, numeric values (zero is falsy), and the strings
    ``true``, ``false``, ``1``, ``0``, ``yes``, ``no``, ``on``, ``off``
    (case-insensitive).

    Args:
        value: The value to validate.

    Returns:
        The value converted to a bool.

    Raises:
        TypeError: If *value* cannot be interpreted as a bool.
        ValueError: If *value* is a string that does not represent a bool.

    Examples:
        >>> bool_validator("true")
        True
        >>> bool_validator(0)
        False
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in ("true", "1", "yes", "on"):
            return True
        if lowered in ("false", "0", "no", "off"):
            return False
        raise ValueError(f"cannot interpret string {value!r} as a bool")
    if isinstance(value, (int, float)):
        return bool(value)
    raise TypeError(f"cannot coerce {value!r} to bool")


_EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


def email_validator(value: Any) -> str:
    """Validate that *value* is a string resembling an email address.

    Args:
        value: The value to validate.

    Returns:
        The validated email string.

    Raises:
        TypeError: If *value* is not a string.
        ValueError: If *value* does not resemble an email address.

    Examples:
        >>> email_validator("user@example.com")
        'user@example.com'
    """
    text = str_validator(value)
    if not _EMAIL_PATTERN.match(text):
        raise ValueError(f"invalid email address: {text!r}")
    return text


_HOSTNAME_LABEL_PATTERN = re.compile(r"^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$")


def hostname_validator(value: Any) -> str:
    """Validate that *value* is a string resembling a hostname.

    Args:
        value: The value to validate.

    Returns:
        The validated hostname string.

    Raises:
        TypeError: If *value* is not a string.
        ValueError: If *value* is not a valid hostname.

    Examples:
        >>> hostname_validator("example.com")
        'example.com'
    """
    text = str_validator(value)
    if not text:
        raise ValueError("hostname must not be empty")
    if text.endswith(".") or text.startswith("-") or text.endswith("-"):
        raise ValueError(f"invalid hostname: {text!r}")
    if len(text) > 253:
        raise ValueError(f"hostname too long: {text!r}")
    for label in text.split("."):
        if not label or len(label) > 63 or not _HOSTNAME_LABEL_PATTERN.match(label):
            raise ValueError(f"invalid hostname: {text!r}")
    return text


def url_validator(value: Any) -> str:
    """Validate that *value* is a string with a scheme and a host.

    Args:
        value: The value to validate.

    Returns:
        The validated URL string.

    Raises:
        TypeError: If *value* is not a string.
        ValueError: If *value* has no scheme or no host.

    Examples:
        >>> url_validator("https://example.com/path")
        'https://example.com/path'
    """
    text = str_validator(value)
    parsed = urlparse(text)
    if not parsed.scheme:
        raise ValueError(f"URL has no scheme: {text!r}")
    if not parsed.hostname:
        raise ValueError(f"URL has no host: {text!r}")
    return text


def range_validator(min_value: Union[int, float], max_value: Union[int, float]) -> Validator:
    """Return a validator ensuring a numeric value lies within ``[min, max]``.

    Args:
        min_value: The inclusive lower bound.
        max_value: The inclusive upper bound.

    Returns:
        A validator callable.

    Raises:
        ValueError: If ``min_value`` is greater than ``max_value``.

    Examples:
        >>> validate = range_validator(1, 10)
        >>> validate(5)
        5
        >>> validate(15)  # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        ValueError: value 15 is outside the allowed range [1, 10]
    """
    if min_value > max_value:
        raise ValueError("min_value must be <= max_value")

    def validate(value: Any) -> Union[int, float]:
        number: Union[int, float]
        if isinstance(value, bool) or not isinstance(value, (int, float, str)):
            raise TypeError(f"cannot coerce {value!r} to a number")
        try:
            number = float(value) if isinstance(value, str) else value  # type: ignore[assignment]
        except (ValueError, TypeError) as exc:
            raise ValueError(f"cannot coerce {value!r} to a number") from exc
        if not (min_value <= number <= max_value):
            raise ValueError(
                f"value {value!r} is outside the allowed range [{min_value}, {max_value}]"
            )
        return number

    return validate


def choices_validator(*choices: Any) -> Validator:
    """Return a validator ensuring the value is one of ``choices``.

    Args:
        choices: The allowed values.

    Returns:
        A validator callable.

    Raises:
        ValueError: If no choices are provided.

    Examples:
        >>> validate = choices_validator("dev", "staging", "prod")
        >>> validate("staging")
        'staging'
    """
    if not choices:
        raise ValueError("at least one choice is required")
    choice_set = frozenset(choices)
    choice_list = list(choices)

    def validate(value: Any) -> Any:
        if value not in choice_set:
            raise ValueError(f"value {value!r} is not one of {choice_list!r}")
        return value

    return validate


def regex_validator(pattern: Union[str, re.Pattern], flags: int = 0) -> Validator:
    """Return a validator ensuring a string matches *pattern*.

    Args:
        pattern: A regex pattern string or compiled ``re.Pattern``.
        flags: Regex flags, used when *pattern* is a string.

    Returns:
        A validator callable.

    Raises:
        TypeError: If *pattern* is neither a string nor a compiled pattern.
        ValueError: If *pattern* is an invalid regex string.

    Examples:
        >>> validate = regex_validator(r"^[A-Z]+$")
        >>> validate("HELLO")
        'HELLO'
    """
    if isinstance(pattern, str):
        try:
            compiled = re.compile(pattern, flags)
        except re.error as exc:
            raise ValueError(f"invalid regex pattern: {pattern!r}") from exc
    elif isinstance(pattern, re.Pattern):
        compiled = pattern
    else:
        raise TypeError(f"pattern must be a string or re.Pattern, got {type(pattern).__name__}")

    def validate(value: Any) -> str:
        text = str_validator(value)
        if not compiled.match(text):
            raise ValueError(f"value {text!r} does not match pattern {pattern!r}")
        return text

    return validate


class SchemaField:
    """A single typed configuration field within a :class:`ConfigSchema`.

    Args:
        name: The configuration key name.
        type_: The expected type (``str``, ``int``, ``float``, or ``bool``).
        default: The default value used when the field is absent. Use
            :data:`schema_required` or omit to mark the field as required.
        required: Whether the field must be present in the config.
        validator: Optional extra validator applied after type coercion.
        description: Human-readable description of the field.

    Raises:
        TypeError: If ``type_`` is not one of the supported types, or if
            ``validator`` is not callable.
        ValueError: If both ``default`` is unset and ``required`` is False
            is contradictory usage (handled by the schema instead).
    """

    _SUPPORTED_TYPES: Dict[type, Validator] = {
        str: str_validator,
        int: int_validator,
        float: float_validator,
        bool: bool_validator,
    }

    def __init__(
        self,
        name: str,
        type_: type,
        default: Any = _UNSET,
        required: bool = False,
        validator: Optional[Validator] = None,
        description: str = "",
    ) -> None:
        if type_ not in self._SUPPORTED_TYPES:
            raise TypeError(
                f"unsupported type {type_!r}; supported types are "
                f"{sorted(self._SUPPORTED_TYPES, key=lambda t: t.__name__)!r}"
            )
        if not isinstance(name, str) or not name:
            raise ValueError("name must be a non-empty string")
        if validator is not None and not callable(validator):
            raise TypeError("validator must be callable")
        self.name: str = name
        self.type_: type = type_
        self.default: Any = default
        self.required: bool = required
        self.validator: Optional[Validator] = validator
        self.description: str = description

    @property
    def has_default(self) -> bool:
        """Return ``True`` if a default value was provided."""
        return self.default is not _UNSET

    def coerce(self, value: Any) -> Any:
        """Coerce *value* to the field's declared type.

        Args:
            value: The raw value to coerce.

        Returns:
            The value converted to the field's type.

        Raises:
            TypeError: If the value cannot be coerced.
            ValueError: If the value is invalid for the type.
        """
        return self._SUPPORTED_TYPES[self.type_](value)

    def validate(self, value: Any) -> Any:
        """Validate and coerce *value*, applying the field's validator.

        Args:
            value: The raw value to validate.

        Returns:
            The validated, coerced value.

        Raises:
            TypeError: If the value cannot be coerced to the field's type.
            ValueError: If the value fails the type check or validator.
        """
        coerced = self.coerce(value)
        if self.validator is not None:
            return self.validator(coerced)
        return coerced


class ConfigSchema:
    """A typed configuration schema composed of :class:`SchemaField` instances.

    Args:
        fields: An iterable of :class:`SchemaField` instances. Duplicate
            names are not allowed; later definitions win.

    Raises:
        ValueError: If a field name is duplicated.
        TypeError: If any item in ``fields`` is not a :class:`SchemaField`.
    """

    def __init__(self, fields: Iterable[SchemaField]) -> None:
        self._fields: Dict[str, SchemaField] = {}
        for field in fields:
            if not isinstance(field, SchemaField):
                raise TypeError(
                    f"all fields must be SchemaField instances, got {type(field).__name__}"
                )
            if field.name in self._fields:
                raise ValueError(f"duplicate field name: {field.name!r}")
            self._fields[field.name] = field

    @property
    def fields(self) -> Dict[str, SchemaField]:
        """Return a copy of the field name to :class:`SchemaField` mapping."""
        return dict(self._fields)

    def field_names(self) -> List[str]:
        """Return the list of declared field names."""
        return list(self._fields)

    def required_fields(self) -> List[str]:
        """Return the sorted list of required field names."""
        return sorted(name for name, field in self._fields.items() if field.required)

    def optional_fields(self) -> List[str]:
        """Return the sorted list of optional field names."""
        return sorted(name for name, field in self._fields.items() if not field.required)

    def validate(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and normalize *config* against this schema.

        Only declared fields are present in the returned dictionary.
        Required fields must be present; optional fields fall back to their
        defaults when absent. All values are coerced to the declared types
        and passed through any field-level validators.

        Args:
            config: The raw configuration dictionary.

        Returns:
            A new dictionary with validated, coerced values.

        Raises:
            TypeError: If *config* is not a dictionary.
            ConfigValidationError: If a required field is missing or a
                value fails validation.
        """
        if not isinstance(config, dict):
            raise TypeError("config must be a dictionary")
        result: Dict[str, Any] = {}
        for name, field in self._fields.items():
            if name not in config:
                if field.required:
                    raise ConfigValidationError(f"required field {name!r} is missing")
                if field.has_default:
                    result[name] = field.default
                continue
            try:
                result[name] = field.validate(config[name])
            except (TypeError, ValueError) as exc:
                raise ConfigValidationError(f"field {name!r}: {exc}") from exc
        return result

    def parse(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Alias for :meth:`validate`."""
        return self.validate(config)

    def get(self, config: Dict[str, Any], name: str, default: Any = None) -> Any:
        """Return the validated value for *name* from *config*.

        Args:
            config: The raw configuration dictionary.
            name: The field name to look up.
            default: Value returned if the field is absent or invalid.

        Returns:
            The validated value, or *default* if unavailable.
        """
        if name not in self._fields:
            return default
        try:
            validated = self.validate(config)
        except (TypeError, ValueError, ConfigValidationError):
            return default
        return validated.get(name, default)

    def merge(self, other: ConfigSchema) -> ConfigSchema:
        """Return a new schema merging *other* into this one.

        Fields from *other* override fields with the same name.

        Args:
            other: The schema to merge in.

        Returns:
            A new :class:`ConfigSchema` with the combined fields.
        """
        merged: Dict[str, SchemaField] = dict(self._fields)
        merged.update(other._fields)
        return ConfigSchema(list(merged.values()))
