"""Configuration utility functions for loading and managing INI configuration files.

This module provides utilities for working with INI-style configuration files
using Python's :mod:`configparser`, with section-aware get/set/merge operations.
"""

import configparser
from pathlib import Path
from typing import Any, Dict, Union


def _parser() -> configparser.ConfigParser:
    parser = _CasePreservingConfigParser()
    return parser


class _CasePreservingConfigParser(configparser.ConfigParser):
    """ConfigParser subclass that preserves the case of option keys."""

    def optionxform(self, option: str) -> str:
        return option


def load_config(file_path: Union[str, Path]) -> Dict[str, Dict[str, str]]:
    """Load configuration from an INI file.

    Args:
        file_path: Path to the INI configuration file.

    Returns:
        Dictionary mapping section names to dictionaries of key/value pairs.
        The ``DEFAULT`` section is excluded.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        configparser.Error: If the file contains invalid INI syntax.
        TypeError: If file_path is not a string or Path object.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {file_path}")

    parser = _parser()
    parser.read(path, encoding="utf-8")

    config: Dict[str, Dict[str, str]] = {}
    for section in parser.sections():
        config[section] = dict(parser.items(section))

    return config


def save_config(config: Dict[str, Dict[str, str]], file_path: Union[str, Path]) -> None:
    """Save configuration to an INI file.

    Args:
        config: Dictionary mapping section names to key/value dictionaries.
        file_path: Path where the INI configuration file should be saved.

    Raises:
        TypeError: If config is not a dictionary of dictionaries.
        OSError: If there is an issue writing to the file.
    """
    if not isinstance(config, dict):
        raise TypeError("config must be a dictionary")

    parser = _parser()
    for section, values in config.items():
        if not isinstance(values, dict):
            raise TypeError(f"Section '{section}' must be a dictionary")
        if not parser.has_section(section):
            parser.add_section(section)
        for key, value in values.items():
            parser.set(section, key, str(value))

    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        parser.write(f)


def get_config_value(
    config: Dict[str, Dict[str, Any]],
    key_path: str,
    default: Any = None,
    separator: str = ".",
) -> Any:
    """Get a value from a nested INI configuration using dot notation.

    The first path component names the section; the second names the key.
    Only one level of nesting (``section.key``) is supported.

    Args:
        config: Configuration dictionary mapping sections to key/value maps.
        key_path: Dot-separated path (e.g. ``"database.host"``).
        default: Value to return if the path is not found.
        separator: Separator character for the key path (default: ".").

    Returns:
        The value at the specified path, or default if not found.
    """
    if not isinstance(config, dict):
        return default

    keys = key_path.split(separator)
    if len(keys) != 2:
        return default

    section, key = keys
    values = config.get(section)
    if not isinstance(values, dict):
        return default

    return values.get(key, default)


def set_config_value(
    config: Dict[str, Dict[str, Any]],
    key_path: str,
    value: Any,
    separator: str = ".",
) -> None:
    """Set a value in a nested INI configuration using dot notation.

    Args:
        config: Configuration dictionary to modify.
        key_path: Dot-separated path (e.g. ``"database.host"``).
        value: Value to set at the specified location.
        separator: Separator character for the key path (default: ".").

    Raises:
        TypeError: If config is not a dictionary.
        ValueError: If key_path does not contain exactly one separator.
    """
    if not isinstance(config, dict):
        raise TypeError("config must be a dictionary")

    keys = key_path.split(separator)
    if len(keys) != 2:
        raise ValueError("key_path must be in 'section.key' format")

    section, key = keys
    if section not in config or not isinstance(config[section], dict):
        config[section] = {}

    config[section][key] = value


def merge_configs(
    base: Dict[str, Dict[str, Any]],
    override: Dict[str, Dict[str, Any]],
) -> Dict[str, Dict[str, Any]]:
    """Merge two INI configuration dictionaries, with override taking precedence.

    Args:
        base: Base configuration dictionary.
        override: Override configuration dictionary.

    Returns:
        New dictionary with merged configuration.

    Raises:
        TypeError: If either argument is not a dictionary of dictionaries.
    """
    if not isinstance(base, dict) or not isinstance(override, dict):
        raise TypeError("Both base and override must be dictionaries")

    result: Dict[str, Dict[str, Any]] = {}

    for section, values in base.items():
        if not isinstance(values, dict):
            raise TypeError(f"Section '{section}' in base must be a dictionary")
        result[section] = dict(values)

    for section, values in override.items():
        if not isinstance(values, dict):
            raise TypeError(f"Section '{section}' in override must be a dictionary")
        if section in result:
            result[section].update(values)
        else:
            result[section] = dict(values)

    return result


def list_sections(config: Dict[str, Dict[str, Any]]) -> list[str]:
    """Return the list of section names in a configuration dictionary."""
    return [section for section in config if isinstance(config[section], dict)]


def has_section(config: Dict[str, Dict[str, Any]], section: str) -> bool:
    """Return True if the configuration contains the given section."""
    return isinstance(config.get(section), dict)


def get_section(config: Dict[str, Dict[str, Any]], section: str) -> Dict[str, Any]:
    """Return the key/value dictionary for a section, or an empty dict if absent."""
    values = config.get(section)
    return dict(values) if isinstance(values, dict) else {}
