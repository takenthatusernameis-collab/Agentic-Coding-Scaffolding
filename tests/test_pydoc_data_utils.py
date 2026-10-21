"""Tests for pydoc_data_utils."""

import unittest
from pydoc_data import topics as stdlib_topics
from typing import List

import pydoc_data_utils
from pydoc_data_utils import (
    count_topics,
    get_topic,
    get_topic_names,
    get_topic_section,
    get_topic_sections,
    get_topic_title,
    get_topics,
    get_topics_subset,
    has_topic,
    search_topics,
    wrap_topic,
)


def standard_topics() -> dict:
    """Return the topics of the standard library."""
    return stdlib_topics.topics


class TestModuleContract(unittest.TestCase):
    """Verify the contract of the module."""

    def test_all_is_sorted_and_unique(self):
        self.assertEqual(pydoc_data_utils.__all__, sorted(set(pydoc_data_utils.__all__)))

    def test_every_name_exists(self):
        for name in pydoc_data_utils.__all__:
            self.assertTrue(hasattr(pydoc_data_utils, name), name)

    def test_the_module_reads_the_standard_library(self):
        self.assertEqual(get_topics(), standard_topics())


class TestTopicCollection(unittest.TestCase):
    """Verify the helpers that report the topics of the standard library."""

    def test_count_topics_matches_the_standard_library(self):
        self.assertEqual(count_topics(), len(standard_topics()))

    def test_get_topic_names_matches_the_standard_library(self):
        self.assertEqual(get_topic_names(), sorted(standard_topics()))

    def test_get_topic_names_is_sorted(self):
        names = get_topic_names()
        self.assertEqual(names, sorted(names))

    def test_get_topics_holds_every_topic(self):
        topics = get_topics()
        self.assertEqual(len(topics), len(standard_topics()))
        for name, text in topics.items():
            self.assertEqual(text, standard_topics()[name])

    def test_get_topics_returns_a_copy(self):
        topics = get_topics()
        topics["lambda"] = "changed"
        self.assertNotEqual(standard_topics()["lambda"], "changed")
        self.assertEqual(get_topics()["lambda"], standard_topics()["lambda"])

    def test_get_topics_subset_returns_the_given_topics(self):
        subset = get_topics_subset(["lambda", "assert"])
        self.assertEqual(list(subset), ["lambda", "assert"])
        self.assertEqual(subset["lambda"], standard_topics()["lambda"])

    def test_get_topics_subset_accepts_a_tuple(self):
        subset = get_topics_subset(("lambda",))
        self.assertEqual(list(subset), ["lambda"])

    def test_get_topics_subset_rejects_a_single_string(self):
        with self.assertRaises(TypeError):
            get_topics_subset("lambda")

    def test_get_topics_subset_rejects_a_bad_container(self):
        with self.assertRaises(TypeError):
            get_topics_subset(42)

    def test_get_topics_subset_rejects_a_bad_entry(self):
        with self.assertRaises(TypeError):
            get_topics_subset([42])

    def test_get_topics_subset_rejects_an_unknown_topic(self):
        with self.assertRaises(ValueError):
            get_topics_subset(["lambda", "nowhere"])

    def test_get_topics_subset_rejects_an_empty_name(self):
        with self.assertRaises(ValueError):
            get_topics_subset([""])


class TestSingleTopic(unittest.TestCase):
    """Verify the helpers that work on a single topic."""

    def test_has_topic_reports_an_existing_topic(self):
        self.assertTrue(has_topic("lambda"))

    def test_has_topic_reports_an_unknown_topic(self):
        self.assertFalse(has_topic("nowhere"))

    def test_has_topic_rejects_a_bad_name(self):
        with self.assertRaises(TypeError):
            has_topic(42)
        with self.assertRaises(ValueError):
            has_topic("")

    def test_get_topic_matches_the_standard_library(self):
        self.assertEqual(get_topic("lambda"), standard_topics()["lambda"])

    def test_get_topic_rejects_an_unknown_topic(self):
        with self.assertRaises(ValueError):
            get_topic("nowhere")

    def test_get_topic_rejects_a_bad_name(self):
        with self.assertRaises(TypeError):
            get_topic(42)
        with self.assertRaises(ValueError):
            get_topic("")

    def test_get_topic_title_is_the_first_line(self):
        title = get_topic_title("lambda")
        self.assertEqual(title, standard_topics()["lambda"].split("\n", 1)[0])
        self.assertTrue(title)
        self.assertNotIn("\n", title)

    def test_get_topic_sections_returns_the_headings(self):
        sections = get_topic_sections("assignment")
        self.assertIn("Augmented assignment statements", sections)
        self.assertIn("Annotated assignment statements", sections)

    def test_get_topic_sections_is_empty_for_a_topic_without_sections(self):
        self.assertEqual(get_topic_sections("lambda"), [])

    def test_get_topic_sections_rejects_an_unknown_topic(self):
        with self.assertRaises(ValueError):
            get_topic_sections("nowhere")


class TestTopicSection(unittest.TestCase):
    """Verify the helper that returns the text of a section."""

    def test_get_topic_section_returns_the_body(self):
        body = get_topic_section("assignment", "Augmented assignment statements")
        self.assertTrue(body.startswith("Augmented assignment is the combination"))
        self.assertNotIn("Augmented assignment statements\n", body)

    def test_get_topic_section_stops_at_the_next_section(self):
        body = get_topic_section("assignment", "Augmented assignment statements")
        self.assertNotIn("Annotated assignment statements", body)

    def test_get_topic_section_rejects_an_unknown_section(self):
        with self.assertRaises(ValueError):
            get_topic_section("assignment", "Nowhere")

    def test_get_topic_section_rejects_the_title_of_the_topic(self):
        with self.assertRaises(ValueError):
            get_topic_section("lambda", "Lambdas")

    def test_get_topic_section_rejects_an_unknown_topic(self):
        with self.assertRaises(ValueError):
            get_topic_section("nowhere", "Overview")

    def test_get_topic_section_rejects_a_bad_section(self):
        with self.assertRaises(TypeError):
            get_topic_section("assignment", 42)
        with self.assertRaises(ValueError):
            get_topic_section("assignment", "")


class TestSearch(unittest.TestCase):
    """Verify the helper that searches the topics."""

    def test_search_topics_finds_a_topic_by_name(self):
        self.assertIn("lambda", search_topics("lambda"))

    def test_search_topics_finds_a_topic_by_text(self):
        names = search_topics("augmented assignment")
        self.assertIn("assignment", names)

    def test_search_topics_ignores_the_case(self):
        self.assertEqual(search_topics("LAMBDA"), search_topics("lambda"))

    def test_search_topics_is_sorted(self):
        names = search_topics("a")
        self.assertEqual(names, sorted(names))

    def test_search_topics_returns_nothing_for_an_unknown_text(self):
        self.assertEqual(search_topics("nowhere-at-all"), [])

    def test_search_topics_rejects_a_bad_query(self):
        with self.assertRaises(TypeError):
            search_topics(42)
        with self.assertRaises(ValueError):
            search_topics("")


class TestWrapTopic(unittest.TestCase):
    """Verify the helper that wraps the text of a topic."""

    def test_wrap_topic_wraps_the_prose(self):
        wrapped = wrap_topic("lambda", 40)
        for line in wrapped.split("\n"):
            if line[:1].isspace():
                continue
            self.assertLessEqual(len(line), 40)

    def test_wrap_topic_keeps_the_indented_parts(self):
        wrapped = wrap_topic("lambda", 40)
        self.assertIn("   lambda_expr ::= \"lambda\" [parameter_list] \":\" expression", wrapped)

    def test_wrap_topic_keeps_the_title(self):
        wrapped = wrap_topic("lambda", 40)
        self.assertTrue(wrapped.startswith(get_topic_title("lambda")))

    def test_wrap_topic_keeps_every_word_of_the_prose(self):
        wrapped = wrap_topic("lambda", 40)
        words = [word for word in get_topic("lambda").split() if word.isalnum()]
        for word in set(words):
            self.assertIn(word, wrapped)

    def test_wrap_topic_rejects_a_bad_width(self):
        with self.assertRaises(TypeError):
            wrap_topic("lambda", "wide")
        with self.assertRaises(ValueError):
            wrap_topic("lambda", 0)

    def test_wrap_topic_rejects_an_unknown_topic(self):
        with self.assertRaises(ValueError):
            wrap_topic("nowhere", 40)


class TestHeadingDetection(unittest.TestCase):
    """Verify that the headings of a topic are found in the text of the topic."""

    def headings(self, name: str) -> List[str]:
        """Return the headings of a topic of the standard library."""
        return pydoc_data_utils._headings(standard_topics()[name].split("\n"))

    def test_the_title_of_a_topic_is_not_a_heading(self):
        self.assertEqual(self.headings("lambda"), [])

    def test_the_headings_of_a_topic_are_found(self):
        self.assertIn("Overview", self.headings("compound"))

    def test_every_heading_is_part_of_the_text(self):
        text = standard_topics()["assignment"]
        for heading in pydoc_data_utils.get_topic_sections("assignment"):
            self.assertIn(heading, text)


if __name__ == "__main__":
    unittest.main()
