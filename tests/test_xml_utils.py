"""Unit tests for xml_utils module."""

import tempfile
import unittest
import xml.etree.ElementTree as ET

from xml_utils import (
    add_child,
    build_xml,
    dict_to_element,
    element_to_dict,
    find_element,
    find_elements,
    get_attribute,
    get_element_text,
    parse_xml,
    parse_xml_string,
    set_attribute,
    set_element_text,
    validate_well_formed,
    xml_to_string,
)

SIMPLE_XML = '<root><child a="1">text</child><child a="2">more</child></root>'


class TestParseXmlString(unittest.TestCase):
    def test_parses_valid_xml(self):
        root = parse_xml_string(SIMPLE_XML)
        self.assertIsInstance(root, ET.Element)
        self.assertEqual(root.tag, "root")

    def test_child_attributes_and_text(self):
        root = parse_xml_string(SIMPLE_XML)
        first = root.find("child")
        self.assertIsNotNone(first)
        self.assertEqual(first.get("a"), "1")
        self.assertEqual(first.text, "text")

    def test_invalid_xml_raises(self):
        with self.assertRaises(ET.ParseError):
            parse_xml_string("<root>")

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            parse_xml_string(123)  # type: ignore[arg-type]


class TestParseXml(unittest.TestCase):
    def test_parses_file(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".xml", delete=False) as fh:
            fh.write(SIMPLE_XML)
            path = fh.name
        try:
            tree = parse_xml(path)
            self.assertIsInstance(tree, ET.ElementTree)
            self.assertEqual(tree.getroot().tag, "root")
        finally:
            import os

            os.remove(path)

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            parse_xml(123)  # type: ignore[arg-type]


class TestBuildXml(unittest.TestCase):
    def test_builds_element_with_tag_and_text(self):
        element = build_xml("greeting", text="hello")
        self.assertEqual(element.tag, "greeting")
        self.assertEqual(element.text, "hello")

    def test_builds_element_with_attributes(self):
        element = build_xml("node", id="42", active="true")
        self.assertEqual(element.get("id"), "42")
        self.assertEqual(element.get("active"), "true")

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            build_xml(123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            build_xml("node", text=123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            build_xml("node", id=123)  # type: ignore[arg-type]


class TestAddChild(unittest.TestCase):
    def test_appends_child(self):
        parent = build_xml("parent")
        child = build_xml("child")
        add_child(parent, child)
        self.assertEqual(len(parent), 1)
        self.assertEqual(parent[0].tag, "child")

    def test_type_errors(self):
        parent = build_xml("parent")
        with self.assertRaises(TypeError):
            add_child(parent, "not an element")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            add_child("not an element", build_xml("child"))  # type: ignore[arg-type]


class TestSetGetAttribute(unittest.TestCase):
    def test_set_and_get_attribute(self):
        element = build_xml("node")
        set_attribute(element, "key", "value")
        self.assertEqual(get_attribute(element, "key"), "value")

    def test_get_attribute_default(self):
        element = build_xml("node")
        self.assertIsNone(get_attribute(element, "missing"))
        self.assertEqual(get_attribute(element, "missing", default="n/a"), "n/a")

    def test_type_errors(self):
        element = build_xml("node")
        with self.assertRaises(TypeError):
            set_attribute(element, "k", 123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            get_attribute(element, 123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            get_attribute(element, "k", default=123)  # type: ignore[arg-type]


class TestElementToDict(unittest.TestCase):
    def test_converts_element_to_dict(self):
        root = parse_xml_string(SIMPLE_XML)
        d = element_to_dict(root)
        self.assertEqual(d["tag"], "root")
        self.assertEqual(d["attributes"], {})
        self.assertEqual(len(d["children"]), 2)
        self.assertEqual(d["children"][0]["tag"], "child")
        self.assertEqual(d["children"][0]["attributes"], {"a": "1"})
        self.assertEqual(d["children"][0]["text"], "text")

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            element_to_dict("not an element")  # type: ignore[arg-type]


class TestDictToElement(unittest.TestCase):
    def test_rebuilds_element_from_dict(self):
        root = parse_xml_string(SIMPLE_XML)
        d = element_to_dict(root)
        rebuilt = dict_to_element("root", d)
        self.assertEqual(rebuilt.tag, "root")
        self.assertEqual(len(rebuilt), 2)
        self.assertEqual(rebuilt[0].get("a"), "1")
        self.assertEqual(rebuilt[0].text, "text")

    def test_roundtrip_preserves_structure(self):
        root = parse_xml_string("<outer><inner>value</inner></outer>")
        d = element_to_dict(root)
        rebuilt = dict_to_element(d["tag"], d)
        self.assertEqual(xml_to_string(rebuilt), xml_to_string(root))

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            dict_to_element(123, {})  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            dict_to_element("tag", "not a dict")  # type: ignore[arg-type]


class TestFindElements(unittest.TestCase):
    def test_finds_matching_elements(self):
        root = parse_xml_string(SIMPLE_XML)
        children = find_elements(root, "child")
        self.assertEqual(len(children), 2)
        self.assertEqual([c.get("a") for c in children], ["1", "2"])

    def test_type_errors(self):
        root = build_xml("root")
        with self.assertRaises(TypeError):
            find_elements(root, 123)  # type: ignore[arg-type]


class TestFindElement(unittest.TestCase):
    def test_finds_first_matching_element(self):
        root = parse_xml_string(SIMPLE_XML)
        child = find_element(root, "child")
        self.assertIsNotNone(child)
        self.assertEqual(child.get("a"), "1")

    def test_returns_none_when_missing(self):
        root = build_xml("root")
        self.assertIsNone(find_element(root, "missing"))

    def test_type_errors(self):
        root = build_xml("root")
        with self.assertRaises(TypeError):
            find_element(root, 123)  # type: ignore[arg-type]


class TestGetSetElementText(unittest.TestCase):
    def test_get_element_text(self):
        root = parse_xml_string(SIMPLE_XML)
        self.assertEqual(get_element_text(root, "child"), "text")

    def test_get_element_text_default(self):
        root = build_xml("root")
        self.assertIsNone(get_element_text(root, "missing"))
        self.assertEqual(get_element_text(root, "missing", default="n/a"), "n/a")

    def test_set_element_text(self):
        element = build_xml("node")
        set_element_text(element, "new text")
        self.assertEqual(element.text, "new text")

    def test_type_errors(self):
        root = build_xml("root")
        with self.assertRaises(TypeError):
            get_element_text(root, 123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            get_element_text(root, "child", default=123)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            set_element_text(root, 123)  # type: ignore[arg-type]


class TestXmlToString(unittest.TestCase):
    def test_serializes_element(self):
        element = build_xml("empty")
        self.assertEqual(xml_to_string(element, xml_declaration=False), "<empty />")

    def test_serializes_with_children(self):
        parent = build_xml("parent")
        add_child(parent, build_xml("child", text="hi"))
        result = xml_to_string(parent, xml_declaration=False)
        self.assertIn("<child>hi</child>", result)

    def test_type_errors(self):
        element = build_xml("node")
        with self.assertRaises(TypeError):
            xml_to_string(element, xml_declaration="yes")  # type: ignore[arg-type]


class TestValidateWellFormed(unittest.TestCase):
    def test_valid_xml_returns_true(self):
        self.assertTrue(validate_well_formed("<root/>"))
        self.assertTrue(validate_well_formed(SIMPLE_XML))

    def test_invalid_xml_returns_false(self):
        self.assertFalse(validate_well_formed("<root>"))
        self.assertFalse(validate_well_formed("not xml at all"))

    def test_type_errors(self):
        with self.assertRaises(TypeError):
            validate_well_formed(123)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
