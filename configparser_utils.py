"""Configuration file parsing utilities (wrapping :mod:`configparser`)."""

from __future__ import annotations

import configparser
from configparser import (
    BasicInterpolation,
    ConfigParser,
    ExtendedInterpolation,
    RawConfigParser,
)
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Union

__all__: list[str] = [
    "ConfigParser",
    "RawConfigParser",
    "BasicInterpolation",
    "ExtendedInterpolation",
    "DEFAULTSECT",
    "InterpolationMissingOptionError",
    "InterpolationSyntaxError",
    "InterpolationDepthError",
    "MissingSectionHeaderError",
    "ParsingError",
    "NoSectionError",
    "NoOptionError",
    "DuplicateSectionError",
    "DuplicateOptionError",
    "ConfigParserError",
    "Error",
]

# Re-export common exceptions for convenience
Error = configparser.Error
ConfigParserError = configparser.Error
NoSectionError = configparser.NoSectionError
NoOptionError = configparser.NoOptionError
InterpolationMissingOptionError = configparser.InterpolationMissingOptionError
InterpolationSyntaxError = configparser.InterpolationSyntaxError
InterpolationDepthError = configparser.InterpolationDepthError
ParsingError = configparser.ParsingError
MissingSectionHeaderError = configparser.MissingSectionHeaderError
DuplicateSectionError = configparser.DuplicateSectionError
DuplicateOptionError = configparser.DuplicateOptionError
DEFAULTSECT = getattr(configparser, "DEFAULTSECT", "DEFAULT")


def load_config(
    file_path: Union[str, Path], encoding: str = "utf-8"
) -> Dict[str, Dict[str, str]]:
    """Load configuration from an INI-style file.

    Args:
        file_path: Path to the configuration file.
        encoding: File encoding (default: "utf-8").

    Returns:
        Dictionary mapping section names to dictionaries of key/value pairs.
        The DEFAULT section is excluded.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        TypeError: If file_path is not a string or Path object.
        Error: If the file contains invalid INI syntax.
    """
    path = Path(file_path)
    if not isinstance(file_path, (str, Path)):
        raise TypeError("file_path must be a str or Path")
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {file_path}")

    parser = ConfigParser()
    parser.read(path, encoding=encoding)

    config: Dict[str, Dict[str, str]] = {}
    for section in parser.sections():
        config[section] = dict(parser.items(section))

    return config


def save_config(
    config: Mapping[str, Mapping[str, Any]],
    file_path: Union[str, Path],
    encoding: str = "utf-8",
) -> None:
    """Save configuration to an INI-style file.

    Args:
        config: Configuration dictionary mapping sections to key/value maps.
        file_path: Path where the configuration file should be saved.
        encoding: File encoding (default: "utf-8").

    Raises:
        TypeError: If config is not a mapping or file_path is invalid.
        OSError: If there is an issue writing to the file.
    """
    if not isinstance(config, Mapping):
        raise TypeError("config must be a mapping")

    path = Path(file_path)
    if not isinstance(file_path, (str, Path)):
        raise TypeError("file_path must be a str or Path")

    parser = ConfigParser()
    for section, values in config.items():
        if not isinstance(values, Mapping):
            raise TypeError(f"Section '{section}' must be a mapping")
        if not parser.has_section(section):
            parser.add_section(section)
        for key, value in values.items():
            parser.set(section, str(key), str(value))

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding=encoding) as f:
        parser.write(f)


def get_sections(parser: ConfigParser) -> List[str]:
    """Return a list of section names in the parser."""
    if not isinstance(parser, ConfigParser) and not isinstance(parser, RawConfigParser):
        raise TypeError("parser must be a ConfigParser")
    return parser.sections()


def get_options(parser: ConfigParser, section: str) -> List[str]:
    """Return a list of option names in the specified section."""
    if not isinstance(parser, (ConfigParser, RawConfigParser)):
        raise TypeError("parser must be a ConfigParser")
    return parser.options(section)


def read_files(filenames: Iterable[Union[str, Path]], encoding: str = "utf-8") -> List[str]:
    """Read and parse configuration files.

    Returns a list of successfully read filenames.
    """
    files = [str(f) for f in filenames]
    parser = ConfigParser()
    return parser.read(files, encoding=encoding)


def write_config(
    parser: ConfigParser, file_path: Union[str, Path], encoding: str = "utf-8"
) -> None:
    """Write the parser's configuration to a file."""
    if not isinstance(parser, (ConfigParser, RawConfigParser)):
        raise TypeError("parser must be a ConfigParser")
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding=encoding) as f:
        parser.write(f)
