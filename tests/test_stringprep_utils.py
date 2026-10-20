"""Tests for stringprep_utils."""

import unittest

import stringprep_utils
from stringprep_utils import (
    MAP_TABLES,
    TABLES,
    find_problems,
    in_table,
    is_allowed,
    is_bidi_allowed,
    is_mapped_to_nothing,
    is_preparable,
    is_prohibited,
    is_unassigned,
    map_table,
    map_table_names,
    map_text,
    table_names,
)


class TestStringprepUtils(unittest.TestCase):
    """Verify the string preparation helpers of the wrapper."""

    def test_the_tables_are_read_only(self):
        with self.assertRaises(TypeError):
            TABLES["a2"] = lambda char: True  # type: ignore[index]
        with self.assertRaises(TypeError):
            MAP_TABLES["b4"] = lambda char: char  # type: ignore[index]

    def test_table_names(self):
        names = table_names()
        self.assertEqual(names, tuple(sorted(names)))
        self.assertIn("a1", names)
        self.assertIn("b1", names)
        self.assertIn("c21", names)
        self.assertIn("d1", names)
        self.assertEqual(len(names), len(TABLES))

    def test_map_table_names(self):
        names = map_table_names()
        self.assertEqual(names, ("b2", "b3"))
        self.assertEqual(len(names), len(MAP_TABLES))

    def test_in_table_finds_a_member(self):
        self.assertTrue(in_table("b1", "\u00ad"))
        self.assertFalse(in_table("b1", "a"))
        self.assertTrue(in_table("a1", "\u0378"))
        self.assertTrue(in_table("c21", "\n"))
        self.assertTrue(in_table("d1", "\u05d0"))

    def test_in_table_validates_its_arguments(self):
        with self.assertRaises(TypeError):
            in_table(1, "a")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            in_table("b1", 1)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            in_table("b1", "")
        with self.assertRaises(ValueError):
            in_table("b1", "ab")
        with self.assertRaises(ValueError):
            in_table("z9", "a")

    def test_map_table_maps_a_character(self):
        self.assertEqual(map_table("b3", "A"), "a")
        self.assertEqual(map_table("b2", "A"), "a")
        self.assertEqual(map_table("b2", "\u00df"), "ss")

    def test_map_table_validates_its_arguments(self):
        with self.assertRaises(TypeError):
            map_table(1, "a")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            map_table("b2", 1)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            map_table("b2", "")
        with self.assertRaises(ValueError):
            map_table("b2", "ab")
        with self.assertRaises(ValueError):
            map_table("b1", "a")

    def test_is_unassigned(self):
        self.assertTrue(is_unassigned("\u0378"))
        self.assertFalse(is_unassigned("a"))
        self.assertFalse(is_unassigned("\u00e9"))

    def test_is_mapped_to_nothing(self):
        self.assertTrue(is_mapped_to_nothing("\u00ad"))
        self.assertTrue(is_mapped_to_nothing("\u200b"))
        self.assertFalse(is_mapped_to_nothing("a"))

    def test_is_prohibited(self):
        self.assertTrue(is_prohibited("\n"))
        self.assertTrue(is_prohibited("\u0085"))
        self.assertTrue(is_prohibited("\u00a0"))
        self.assertTrue(is_prohibited("\ue000"))
        self.assertTrue(is_prohibited("\uffff"))
        self.assertTrue(is_prohibited("\ud800"))
        self.assertTrue(is_prohibited("\ufffd"))
        self.assertTrue(is_prohibited("\u2ff0"))
        self.assertTrue(is_prohibited("\u200e"))
        self.assertTrue(is_prohibited("\U000e0001"))

    def test_is_prohibited_keeps_the_plain_space(self):
        self.assertFalse(is_prohibited(" "))
        self.assertFalse(is_prohibited("a"))
        self.assertFalse(is_prohibited("1"))

    def test_is_allowed(self):
        self.assertTrue(is_allowed("a"))
        self.assertTrue(is_allowed(" "))
        self.assertTrue(is_allowed("1"))
        self.assertFalse(is_allowed("\u0378"))
        self.assertFalse(is_allowed("\n"))
        self.assertFalse(is_allowed("\ue000"))

    def test_is_bidi_allowed(self):
        self.assertTrue(is_bidi_allowed("a"))
        self.assertTrue(is_bidi_allowed("\u05d0"))
        self.assertFalse(is_bidi_allowed("1"))

    def test_map_text_removes_the_characters_mapped_to_nothing(self):
        self.assertEqual(map_text("a\u00adb"), "ab")
        self.assertEqual(map_text("a\u200bb"), "ab")

    def test_map_text_folds_the_case(self):
        self.assertEqual(map_text("ABC"), "abc")
        self.assertEqual(map_text(""), "")
        self.assertEqual(map_text("\u00df"), "ss")

    def test_find_problems_reports_the_offending_characters(self):
        self.assertEqual(find_problems("example.com"), [])
        problems = find_problems("a\u0378\n")
        self.assertEqual(len(problems), 2)
        self.assertIn("U+0378", problems[0])
        self.assertIn("unassigned", problems[0])
        self.assertIn("U+000A", problems[1])
        self.assertIn("prohibited", problems[1])

    def test_is_preparable(self):
        self.assertTrue(is_preparable("example.com"))
        self.assertTrue(is_preparable(""))
        self.assertFalse(is_preparable("a\nb"))
        self.assertFalse(is_preparable("a\u0378"))

    def test_the_helpers_validate_their_arguments(self):
        with self.assertRaises(TypeError):
            is_unassigned(1)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            is_unassigned("")
        with self.assertRaises(TypeError):
            is_mapped_to_nothing(1)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            is_mapped_to_nothing("ab")
        with self.assertRaises(TypeError):
            is_prohibited(1)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            is_prohibited("ab")
        with self.assertRaises(TypeError):
            is_allowed(1)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            is_allowed("")
        with self.assertRaises(TypeError):
            is_bidi_allowed(1)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            is_bidi_allowed("ab")
        with self.assertRaises(TypeError):
            map_text(1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            find_problems(1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            is_preparable(1)  # type: ignore[arg-type]

    def test_all_is_sorted_and_unique(self):
        self.assertIsNotNone(stringprep_utils.__all__)
        self.assertEqual(
            len(stringprep_utils.__all__), len(set(stringprep_utils.__all__))
        )
        self.assertEqual(stringprep_utils.__all__, sorted(stringprep_utils.__all__))
        for name in stringprep_utils.__all__:
            self.assertTrue(hasattr(stringprep_utils, name), name)


if __name__ == "__main__":
    unittest.main()
