"""Utilities for warning control (wrapping :mod:`warnings`)."""

import warnings
from typing import Literal, Optional, Type, Union, cast

Action = Literal["default", "error", "ignore", "always", "all", "module", "once"]


def warn(
    message: Union[Warning, str], category: Type[Warning] = UserWarning,
    stacklevel: int = 1,
) -> None:
    """Issue a warning."""
    if not isinstance(message, (str, Warning)):
        raise TypeError("message must be str or Warning instance")
    if not isinstance(category, type) or not issubclass(category, Warning):
        raise TypeError("category must be a Warning subclass")
    if not isinstance(stacklevel, int) or isinstance(stacklevel, bool):
        raise TypeError("stacklevel must be an integer")
    warnings.warn(message, category=category, stacklevel=stacklevel)


def simplefilter(
    action: str, category: Type[Warning] = Warning,
    lineno: int = 0, append: bool = False,
) -> None:
    """Insert a simple entry into the list of warnings filters."""
    if not isinstance(action, str):
        raise TypeError("action must be a string")
    if action not in ("error", "ignore", "always", "default", "module", "once"):
        raise ValueError("invalid action: {!r}".format(action))
    if not isinstance(category, type) or not issubclass(category, Warning):
        raise TypeError("category must be a Warning subclass")
    if not isinstance(lineno, int) or isinstance(lineno, bool):
        raise TypeError("lineno must be an integer")
    if not isinstance(append, bool):
        raise TypeError("append must be a bool")
    warnings.simplefilter(
        cast(Action, action), category=category, lineno=lineno, append=append
    )


def filterwarnings(
    action: str, message: str = "", category: Type[Warning] = Warning,
    module: str = "", lineno: int = 0, append: bool = False,
) -> None:
    """Insert an entry into the list of warnings filters."""
    if not isinstance(action, str):
        raise TypeError("action must be a string")
    if action not in ("error", "ignore", "always", "default", "module", "once"):
        raise ValueError("invalid action: {!r}".format(action))
    if not isinstance(message, str):
        raise TypeError("message must be a string")
    if not isinstance(category, type) or not issubclass(category, Warning):
        raise TypeError("category must be a Warning subclass")
    if not isinstance(module, str):
        raise TypeError("module must be a string")
    if not isinstance(lineno, int) or isinstance(lineno, bool):
        raise TypeError("lineno must be an integer")
    if not isinstance(append, bool):
        raise TypeError("append must be a bool")
    warnings.filterwarnings(
        cast(Action, action), message=message, category=category,
        module=module, lineno=lineno, append=append,
    )


def resetwarnings() -> None:
    """Clear the warnings filter."""
    warnings.resetwarnings()


def catch_warnings(record: bool = False, module=None):
    """Return a context manager that copies and restores the warnings filter."""
    if not isinstance(record, bool):
        raise TypeError("record must be a bool")
    return warnings.catch_warnings(record=record, module=module)


def showwarning(
    message: Warning, category: Type[Warning], filename: str, lineno: int,
    file=None, line: Optional[str] = None,
) -> None:
    """Call showwarning with arguments."""
    if not isinstance(message, Warning):
        raise TypeError("message must be a Warning instance")
    if not isinstance(category, type) or not issubclass(category, Warning):
        raise TypeError("category must be a Warning subclass")
    if not isinstance(filename, str):
        raise TypeError("filename must be a string")
    if not isinstance(lineno, int) or isinstance(lineno, bool):
        raise TypeError("lineno must be an integer")
    if line is not None and not isinstance(line, str):
        raise TypeError("line must be a string or None")
    warnings.showwarning(message, category, filename, lineno, file=file, line=line)


def formatwarning(
    message: Warning, category: Type[Warning], filename: str, lineno: int,
    line: Optional[str] = None,
) -> str:
    """Format a warning the standard way."""
    if not isinstance(message, Warning):
        raise TypeError("message must be a Warning instance")
    if not isinstance(category, type) or not issubclass(category, Warning):
        raise TypeError("category must be a Warning subclass")
    if not isinstance(filename, str):
        raise TypeError("filename must be a string")
    if not isinstance(lineno, int) or isinstance(lineno, bool):
        raise TypeError("lineno must be an integer")
    if line is not None and not isinstance(line, str):
        raise TypeError("line must be a string or None")
    return warnings.formatwarning(message, category, filename, lineno, line=line)
