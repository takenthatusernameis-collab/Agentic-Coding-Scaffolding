"""Configuration utility functions for loading and managing configuration files.

This module provides utilities for working with configuration files,
currently supporting JSON format with potential for extension to other formats.
"""

import json
from pathlib import Path
from typing import Any, Dict, Union


def load_config(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Load configuration from a JSON file.

    Args:
        file_path: Path to the JSON configuration file

    Returns:
        Dictionary containing the configuration data

    Raises:
        FileNotFoundError: If the configuration file does not exist
        json.JSONDecodeError: If the file contains invalid JSON
        TypeError: If file_path is not a string or Path object, or if the JSON
                   root is not a dictionary
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {file_path}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        raise TypeError(f"Configuration file must contain a JSON object, got {type(data).__name__}")

    return data


def save_config(config: Dict[str, Any], file_path: Union[str, Path], indent: int = 2) -> None:
    """Save configuration to a JSON file.

    Args:
        config: Dictionary containing configuration data to save
        file_path: Path where the JSON configuration file should be saved
        indent: Number of spaces for indentation in the JSON output (default: 2)

    Raises:
        TypeError: If config is not a dictionary or file_path is not a string/Path
        OSError: If there is an issue writing to the file
    """
    if not isinstance(config, dict):
        raise TypeError("config must be a dictionary")

    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=indent, ensure_ascii=False)


def get_config_value(
    config: Dict[str, Any], key_path: str, default: Any = None, separator: str = "."
) -> Any:
    """Get a value from a nested configuration dictionary using dot notation.

    Args:
        config: Configuration dictionary
        key_path: Dot-separated path to the desired value (e.g., "database.host")
        default: Value to return if the key path is not found (default: None)
        separator: Separator character for the key path (default: ".")

    Returns:
        The value at the specified key path, or default if not found

    Example:
        >>> config = {"database": {"host": "localhost", "port": 5432}}
        >>> get_config_value(config, "database.host")
        'localhost'
        >>> get_config_value(config, "database.username", "admin")
        'admin'
    """
    if not isinstance(config, dict):
        return default

    keys = key_path.split(separator)
    current = config

    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default

    return current


def set_config_value(
    config: Dict[str, Any], key_path: str, value: Any, separator: str = "."
) -> None:
    """Set a value in a nested configuration dictionary using dot notation.

    Args:
        config: Configuration dictionary to modify
        key_path: Dot-separated path where the value should be set (e.g., "database.host")
        value: Value to set at the specified location
        separator: Separator character for the key path (default: ".")

    Raises:
        TypeError: If config is not a dictionary

    Example:
        >>> config = {"database": {"host": "localhost"}}
        >>> set_config_value(config, "database.port", 5432)
        >>> config
        {'database': {'host': 'localhost', 'port': 5432}}
        >>> set_config_value(config, "database.username", "admin")
        >>> config
        {'database': {'host': 'localhost', 'port': 5432, 'username': 'admin'}}
    """
    if not isinstance(config, dict):
        raise TypeError("config must be a dictionary")

    keys = key_path.split(separator)
    current = config

    # Navigate to the parent of the target key
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        elif not isinstance(current[key], dict):
            # Overwrite non-dict value with dict to continue path
            current[key] = {}
        current = current[key]

    # Set the final key
    current[keys[-1]] = value


def merge_configs(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """Merge two configuration dictionaries, with override taking precedence.

    Args:
        base: Base configuration dictionary
        override: Override configuration dictionary

    Returns:
        New dictionary with merged configuration

    Note:
        This function performs a deep merge. Nested dictionaries are merged
        recursively rather than replaced.

    Example:
        >>> base = {"database": {"host": "localhost", "port": 5432}, "debug": False}
        >>> override = {"database": {"port": 5433}, "debug": True}
        >>> merge_configs(base, override)
        {'database': {'host': 'localhost', 'port': 5433}, 'debug': True}
    """
    if not isinstance(base, dict) or not isinstance(override, dict):
        raise TypeError("Both base and override must be dictionaries")

    result = base.copy()

    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_configs(result[key], value)
        else:
            result[key] = value

    return result
