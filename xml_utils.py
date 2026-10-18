"""XML parsing and generation utilities.

Provides helpers for parsing XML documents and strings, building XML elements,
converting between elements and dictionaries, querying with XPath, and
serializing elements back to strings using the standard library
``xml.etree.ElementTree`` module. All functions validate their inputs and raise
``TypeError`` or ``ValueError`` on invalid arguments.
"""

from __future__ import annotations

import os
import xml.etree.ElementTree as ET
from typing import Any, Optional, Union

__all__: list[str] = [
    "parse_xml",
    "parse_xml_string",
    "build_xml",
    "add_child",
    "set_attribute",
    "get_attribute",
    "element_to_dict",
    "dict_to_element",
    "find_elements",
    "find_element",
    "get_element_text",
    "set_element_text",
    "xml_to_string",
    "validate_well_formed",
]


def parse_xml(path: Union[str, os.PathLike[str]]) -> ET.ElementTree[ET.Element]:
    """Parse an XML file and return its :class:`~xml.etree.ElementTree.ElementTree`.

    Args:
        path: Path to the XML file.

    Returns:
        The parsed :class:`~xml.etree.ElementTree.ElementTree`.

    Raises:
        TypeError: If ``path`` is not a string or path-like object.
        FileNotFoundError: If the file does not exist.
        xml.etree.ElementTree.ParseError: If the file is not well-formed XML.

    Examples:
        >>> import tempfile, os
        >>> path = tempfile.mktemp(suffix=".xml")
        >>> with open(path, "w") as fh:
        ...     _ = fh.write("<root><child>text</child></root>")
        >>> tree = parse_xml(path)
        >>> tree.getroot().tag
        'root'
        >>> os.remove(path)
    """
    if not isinstance(path, (str, os.PathLike)):
        raise TypeError("path must be a string or path-like object")
    return ET.parse(os.fspath(path))


def parse_xml_string(text: str) -> ET.Element:
    """Parse an XML string and return its root :class:`~xml.etree.ElementTree.Element`.

    Args:
        text: The XML document as a string.

    Returns:
        The root :class:`~xml.etree.ElementTree.Element`.

    Raises:
        TypeError: If ``text`` is not a string.
        xml.etree.ElementTree.ParseError: If ``text`` is not well-formed XML.

    Examples:
        >>> parse_xml_string('<root><child a="1">text</child></root>').tag
        'root'
        >>> parse_xml_string('<root><child a="1">text</child></root>').find("child").text
        'text'
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return ET.fromstring(text)


def build_xml(tag: str, text: Optional[str] = None, **attributes: str) -> ET.Element:
    """Build an XML element with the given tag, optional text, and attributes.

    Args:
        tag: The element tag name.
        text: Optional text content of the element.
        attributes: Element attributes as keyword arguments.

    Returns:
        A new :class:`~xml.etree.ElementTree.Element`.

    Raises:
        TypeError: If ``tag`` or ``text`` is not a string, or if any attribute
            name or value is not a string.

    Examples:
        >>> root = build_xml("root", attr="value")
        >>> root.tag
        'root'
        >>> root.get("attr")
        'value'
    """
    if not isinstance(tag, str):
        raise TypeError("tag must be a string")
    if text is not None and not isinstance(text, str):
        raise TypeError("text must be a string or None")
    for key, value in attributes.items():
        if not isinstance(key, str) or not isinstance(value, str):
            raise TypeError("attribute names and values must be strings")
    element = ET.Element(tag)
    if text is not None:
        element.text = text
    for key, value in attributes.items():
        element.set(key, value)
    return element


def add_child(parent: ET.Element, child: ET.Element) -> None:
    """Append ``child`` as a sub-element of ``parent``.

    Args:
        parent: The parent element.
        child: The child element to append.

    Raises:
        TypeError: If either argument is not an :class:`~xml.etree.ElementTree.Element`.
    """
    if not isinstance(parent, ET.Element):
        raise TypeError("parent must be an Element")
    if not isinstance(child, ET.Element):
        raise TypeError("child must be an Element")
    parent.append(child)


def set_attribute(element: ET.Element, key: str, value: str) -> None:
    """Set the attribute ``key`` on ``element`` to ``value``.

    Args:
        element: The target element.
        key: The attribute name.
        value: The attribute value.

    Raises:
        TypeError: If ``element`` is not an Element, or ``key``/``value`` are
            not strings.
    """
    if not isinstance(element, ET.Element):
        raise TypeError("element must be an Element")
    if not isinstance(key, str) or not isinstance(value, str):
        raise TypeError("key and value must be strings")
    element.set(key, value)


def get_attribute(element: ET.Element, key: str, default: Optional[str] = None) -> Optional[str]:
    """Return the value of attribute ``key`` on ``element``, or ``default``.

    Args:
        element: The target element.
        key: The attribute name.
        default: Value returned when the attribute is absent.

    Returns:
        The attribute value, or ``default`` if the attribute is not present.

    Raises:
        TypeError: If ``element`` is not an Element, or ``key``/``default``
            have invalid types.
    """
    if not isinstance(element, ET.Element):
        raise TypeError("element must be an Element")
    if not isinstance(key, str):
        raise TypeError("key must be a string")
    if default is not None and not isinstance(default, str):
        raise TypeError("default must be a string or None")
    return element.get(key, default)


def element_to_dict(element: ET.Element) -> dict[str, Any]:
    """Convert ``element`` and its descendants into a nested dictionary.

    The dictionary has keys ``tag``, ``attributes``, ``text``, and ``children``,
    where ``children`` is a list of dictionaries produced recursively.

    Args:
        element: The element to convert.

    Returns:
        A nested dictionary representation of ``element``.

    Raises:
        TypeError: If ``element`` is not an :class:`~xml.etree.ElementTree.Element`.

    Examples:
        >>> tree = parse_xml_string('<root><child a="1">text</child></root>')
        >>> d = element_to_dict(tree)
        >>> d["tag"]
        'root'
        >>> d["children"][0]["tag"]
        'child'
        >>> d["children"][0]["attributes"]
        {'a': '1'}
    """
    if not isinstance(element, ET.Element):
        raise TypeError("element must be an Element")
    return {
        "tag": element.tag,
        "attributes": dict(element.attrib),
        "text": element.text,
        "children": [element_to_dict(child) for child in element],
    }


def dict_to_element(tag: str, data: dict[str, Any]) -> ET.Element:
    """Build an :class:`~xml.etree.ElementTree.Element` from a nested dictionary.

    The dictionary may contain ``attributes`` (dict), ``text`` (str), and
    ``children`` (list of dicts) keys, matching the output of
    :func:`element_to_dict`.

    Args:
        tag: The element tag name.
        data: A nested dictionary describing the element.

    Returns:
        A new :class:`~xml.etree.ElementTree.Element`.

    Raises:
        TypeError: If ``tag`` is not a string or ``data`` has an invalid shape.
    """
    if not isinstance(tag, str):
        raise TypeError("tag must be a string")
    if not isinstance(data, dict):
        raise TypeError("data must be a dictionary")
    element = ET.Element(tag)
    attributes = data.get("attributes", {})
    if not isinstance(attributes, dict):
        raise TypeError("data['attributes'] must be a dictionary")
    for key, value in attributes.items():
        if not isinstance(key, str) or not isinstance(value, str):
            raise TypeError("attribute names and values must be strings")
        element.set(key, value)
    text = data.get("text")
    if text is not None:
        if not isinstance(text, str):
            raise TypeError("data['text'] must be a string or None")
        element.text = text
    children = data.get("children", [])
    if not isinstance(children, list):
        raise TypeError("data['children'] must be a list")
    for child in children:
        if not isinstance(child, dict):
            raise TypeError("each child must be a dictionary")
        child_tag = child.get("tag")
        if not isinstance(child_tag, str):
            raise TypeError("each child must have a string 'tag'")
        child_element = dict_to_element(child_tag, child)
        element.append(child_element)
    return element


def find_elements(element: ET.Element, xpath: str) -> list[ET.Element]:
    """Return all elements matching ``xpath`` relative to ``element``.

    Args:
        element: The element to search within.
        xpath: An XPath expression.

    Returns:
        A list of matching :class:`~xml.etree.ElementTree.Element` objects.

    Raises:
        TypeError: If ``element`` is not an Element or ``xpath`` is not a string.
    """
    if not isinstance(element, ET.Element):
        raise TypeError("element must be an Element")
    if not isinstance(xpath, str):
        raise TypeError("xpath must be a string")
    return element.findall(xpath)


def find_element(element: ET.Element, xpath: str) -> Optional[ET.Element]:
    """Return the first element matching ``xpath`` relative to ``element``.

    Args:
        element: The element to search within.
        xpath: An XPath expression.

    Returns:
        The first matching element, or ``None`` if no match is found.

    Raises:
        TypeError: If ``element`` is not an Element or ``xpath`` is not a string.
    """
    if not isinstance(element, ET.Element):
        raise TypeError("element must be an Element")
    if not isinstance(xpath, str):
        raise TypeError("xpath must be a string")
    return element.find(xpath)


def get_element_text(
    element: ET.Element, xpath: str, default: Optional[str] = None
) -> Optional[str]:
    """Return the text content of the first element matching ``xpath``.

    Args:
        element: The element to search within.
        xpath: An XPath expression locating the target element.
        default: Value returned when no matching element is found.

    Returns:
        The text content of the matched element, or ``default``.

    Raises:
        TypeError: If ``element`` is not an Element, ``xpath`` is not a string,
            or ``default`` is not a string or None.
    """
    if not isinstance(element, ET.Element):
        raise TypeError("element must be an Element")
    if not isinstance(xpath, str):
        raise TypeError("xpath must be a string")
    if default is not None and not isinstance(default, str):
        raise TypeError("default must be a string or None")
    found = element.find(xpath)
    if found is None:
        return default
    return found.text


def set_element_text(element: ET.Element, text: str) -> None:
    """Set the text content of ``element`` to ``text``.

    Args:
        element: The target element.
        text: The text content to set.

    Raises:
        TypeError: If ``element`` is not an Element or ``text`` is not a string.
    """
    if not isinstance(element, ET.Element):
        raise TypeError("element must be an Element")
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    element.text = text


def xml_to_string(element: ET.Element, xml_declaration: bool = True) -> str:
    """Serialize ``element`` and its descendants to an XML string.

    Args:
        element: The element to serialize.
        xml_declaration: Whether to include an XML declaration.

    Returns:
        The XML document as a string.

    Raises:
        TypeError: If ``element`` is not an Element or ``xml_declaration``
            is not a bool.
    """
    if not isinstance(element, ET.Element):
        raise TypeError("element must be an Element")
    if not isinstance(xml_declaration, bool):
        raise TypeError("xml_declaration must be a bool")
    return ET.tostring(element, encoding="unicode", xml_declaration=xml_declaration)


def validate_well_formed(text: str) -> bool:
    """Return ``True`` if ``text`` is well-formed XML, otherwise ``False``.

    Args:
        text: The candidate XML document as a string.

    Returns:
        ``True`` if ``text`` parses as well-formed XML, otherwise ``False``.

    Raises:
        TypeError: If ``text`` is not a string.

    Examples:
        >>> validate_well_formed("<root/>")
        True
        >>> validate_well_formed("<root>")
        False
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    try:
        ET.fromstring(text)
    except ET.ParseError:
        return False
    return True


if __name__ == "__main__":
    import doctest

    doctest.testmod()
