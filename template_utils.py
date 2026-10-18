"""String template utilities.

This module provides functions for simple string template rendering and
variable substitution. It supports both ``str.format()``-style templates
and ``string.Template``-style substitution.
"""

from __future__ import annotations

import re
from string import Template
from typing import Any, Mapping


def render_template(template: str, *args: Any, **kwargs: Any) -> str:
    """Render a template string using ``str.format()``.

    Args:
        template: The template string containing ``{placeholder}`` style
            placeholders.
        *args: Positional arguments to substitute into the template.
        **kwargs: Keyword arguments to substitute into the template.

    Returns:
        The rendered template string.

    Raises:
        TypeError: If ``template`` is not a string.
        KeyError: If a required placeholder is missing.
    """
    if not isinstance(template, str):
        raise TypeError("template must be a string")
    return template.format(*args, **kwargs)


def substitute(
    template: str,
    mapping: Mapping[str, Any] | None = None,
    **kwargs: Any,
) -> str:
    """Substitute variables into a template using ``string.Template``.

    This is the standard substitution that raises an error if a placeholder
    is missing from the mapping.

    Args:
        template: The template string containing ``$placeholder`` or
            ``${placeholder}`` style placeholders.
        mapping: Optional mapping of placeholder names to values.
        **kwargs: Additional keyword arguments to substitute.

    Returns:
        The substituted template string.

    Raises:
        TypeError: If ``template`` is not a string.
        KeyError: If a required placeholder is missing.
    """
    if not isinstance(template, str):
        raise TypeError("template must be a string")
    if mapping is None:
        mapping = {}
    full_mapping: dict[str, Any] = dict(mapping)
    full_mapping.update(kwargs)
    return Template(template).substitute(full_mapping)


def safe_substitute(
    template: str,
    mapping: Mapping[str, Any] | None = None,
    **kwargs: Any,
) -> str:
    """Safely substitute variables into a template using ``string.Template``.

    This leaves missing placeholders unchanged instead of raising an error.

    Args:
        template: The template string containing ``$placeholder`` or
            ``${placeholder}`` style placeholders.
        mapping: Optional mapping of placeholder names to values.
        **kwargs: Additional keyword arguments to substitute.

    Returns:
        The substituted template string.

    Raises:
        TypeError: If ``template`` is not a string.
    """
    if not isinstance(template, str):
        raise TypeError("template must be a string")
    if mapping is None:
        mapping = {}
    full_mapping: dict[str, Any] = dict(mapping)
    full_mapping.update(kwargs)
    return Template(template).safe_substitute(full_mapping)


def render_from_dict(
    template: str,
    context: Mapping[str, Any] | None = None,
    default: str = "",
) -> str:
    """Render a template by substituting values from a context dictionary.

    Uses ``str.format()`` style placeholders. For missing keys, the provided
    default value is used.

    Args:
        template: The template string containing ``{placeholder}`` style
            placeholders.
        context: Dictionary containing values to substitute.
        default: Default value to use for missing placeholders.

    Returns:
        The rendered template string.

    Raises:
        TypeError: If ``template`` is not a string or if ``context`` is
            provided but not a mapping.
    """
    if not isinstance(template, str):
        raise TypeError("template must be a string")
    if context is None:
        context = {}
    if not isinstance(context, Mapping):
        raise TypeError("context must be a mapping or None")

    class DefaultFormatter(dict):
        def __missing__(self, key: str) -> str:
            return default

    try:
        return template.format_map(DefaultFormatter(context))
    except Exception:
        result = template
        for key in extract_placeholders(template):
            pattern = re.compile(r"\{" + re.escape(key) + r"(:[^}]*)?\}")
            if key in context:
                result = pattern.sub(str(context[key]), result)
            else:
                result = pattern.sub(default, result)
        return result


def has_placeholders(template: str) -> bool:
    """Check if the template contains any placeholders.

    Checks for both ``str.format()`` style (``{name}``) and
    ``string.Template`` style (``$name``, ``${name}``) placeholders.

    Args:
        template: The template string to check.

    Returns:
        ``True`` if the template contains placeholders, ``False`` otherwise.

    Raises:
        TypeError: If ``template`` is not a string.
    """
    if not isinstance(template, str):
        raise TypeError("template must be a string")
    format_pattern = re.compile(r"\{[^}]+\}")
    if format_pattern.search(template):
        return True
    template_pattern = re.compile(r"\$[A-Za-z_][A-Za-z0-9_]*|\$\{[^}]+\}")
    if template_pattern.search(template):
        return True
    return False


def extract_placeholders(template: str) -> list[str]:
    """Extract placeholder names from a template string.

    Extracts names from both ``str.format()`` style (``{name}`` or
    ``{name:format}``) and ``string.Template`` style (``$name`` or
    ``${name}``) placeholders.

    Args:
        template: The template string to analyze.

    Returns:
        A list of placeholder names.

    Raises:
        TypeError: If ``template`` is not a string.
    """
    if not isinstance(template, str):
        raise TypeError("template must be a string")
    placeholders: list[str] = []
    format_pattern = re.compile(r"\{([^}:]+)(?::[^}]*)?\}")
    for match in format_pattern.finditer(template):
        name = match.group(1)
        if name.isdigit():
            continue
        if name not in placeholders:
            placeholders.append(name)
    template_pattern = re.compile(r"\$\{([^}]+)\}|\$([A-Za-z_][A-Za-z0-9_]*)")
    for match in template_pattern.finditer(template):
        name = match.group(1) if match.group(1) else match.group(2)
        if name and name not in placeholders:
            placeholders.append(name)
    return placeholders
