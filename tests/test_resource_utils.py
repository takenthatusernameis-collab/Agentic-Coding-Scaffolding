"""Tests for resource_utils."""

import unittest
from unittest.mock import patch

import resource_utils
from resource_utils import (
    Limit,
    Usage,
    get_page_size,
    get_rlimit,
    get_rusage,
    is_available,
    limit_name,
    limit_names,
    limit_value,
    prlimit,
    set_rlimit,
    usage_as_dict,
    usage_names,
)

#: The name of a limit every Unix-like platform provides.
LIMIT_NAME = "RLIMIT_NOFILE"


class TestResourceUtils(unittest.TestCase):
    def test_is_available(self):
        self.assertIsInstance(is_available(), bool)

    def test_constants_match_the_standard_library(self):
        self.assertEqual(resource_utils.RUSAGE_SELF, 0)
        self.assertEqual(resource_utils.RUSAGE_CHILDREN, -1)
        self.assertEqual(resource_utils.RUSAGE_THREAD, 1)
        if is_available():
            import resource

            self.assertEqual(resource_utils.RLIM_INFINITY, resource.RLIM_INFINITY)

    def test_limit_names(self):
        limits = limit_names()
        self.assertTrue(limits)
        self.assertIn(LIMIT_NAME, limits)
        self.assertNotIn("RLIM_INFINITY", limits)
        limits[LIMIT_NAME] = 99
        self.assertNotEqual(limit_names()[LIMIT_NAME], 99)

    def test_usage_names(self):
        usages = usage_names()
        self.assertEqual(usages["RUSAGE_SELF"], resource_utils.RUSAGE_SELF)
        self.assertEqual(usages["RUSAGE_CHILDREN"], resource_utils.RUSAGE_CHILDREN)

    def test_limit_value(self):
        self.assertEqual(limit_value(LIMIT_NAME), limit_names()[LIMIT_NAME])
        self.assertEqual(limit_value("nofile"), limit_names()[LIMIT_NAME])
        self.assertEqual(limit_value("RLIMIT-NOFILE"), limit_names()[LIMIT_NAME])

    def test_limit_value_validates_its_arguments(self):
        with self.assertRaises(TypeError):
            limit_value(7)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            limit_value("RLIMIT_DOES_NOT_EXIST")

    def test_limit_name(self):
        value = limit_value(LIMIT_NAME)
        self.assertEqual(limit_name(value), LIMIT_NAME)

    def test_limit_name_validates_its_arguments(self):
        with self.assertRaises(TypeError):
            limit_name("RLIMIT_NOFILE")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            limit_name(9999)

    def test_get_rlimit_reads_the_current_limits(self):
        limits = get_rlimit(LIMIT_NAME)
        self.assertIsInstance(limits, Limit)
        self.assertIsInstance(limits.soft, int)
        self.assertIsInstance(limits.hard, int)
        soft, hard = limits
        self.assertEqual((soft, hard), (limits.soft, limits.hard))

    def test_get_rlimit_accepts_a_name_and_a_value(self):
        self.assertEqual(
            get_rlimit(LIMIT_NAME),
            get_rlimit(limit_value(LIMIT_NAME)),
        )

    def test_get_rlimit_validates_its_arguments(self):
        with self.assertRaises(TypeError):
            get_rlimit(1.5)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            get_rlimit("RLIMIT_DOES_NOT_EXIST")
        with self.assertRaises(ValueError):
            get_rlimit(9999)

    def test_set_rlimit_calls_the_standard_library(self):
        limits = get_rlimit(LIMIT_NAME)
        with patch("resource_utils._resource.setrlimit") as mock_setrlimit:
            set_rlimit(LIMIT_NAME, (limits.soft, limits.hard))
        mock_setrlimit.assert_called_once_with(
            limit_value(LIMIT_NAME),
            (limits.soft, limits.hard),
        )

    def test_set_rlimit_validates_its_arguments(self):
        with patch("resource_utils._resource.setrlimit") as mock_setrlimit:
            with self.assertRaises(TypeError):
                set_rlimit(LIMIT_NAME, "unlimited")  # type: ignore[arg-type]
            with self.assertRaises(ValueError):
                set_rlimit(LIMIT_NAME, (1,))
            with self.assertRaises(TypeError):
                set_rlimit(LIMIT_NAME, (1, "two"))  # type: ignore[arg-type]
            with self.assertRaises(ValueError):
                set_rlimit("RLIMIT_DOES_NOT_EXIST", (1, 1))
            with self.assertRaises(TypeError):
                set_rlimit(1.5, (1, 1))  # type: ignore[arg-type]
        mock_setrlimit.assert_not_called()

    def test_set_rlimit_refuses_impossible_limits(self):
        limits = get_rlimit(LIMIT_NAME)
        if limits.hard == resource_utils.RLIM_INFINITY:
            self.skipTest("the platform does not limit the resource")
        with patch("resource_utils._resource.setrlimit") as mock_setrlimit:
            with self.assertRaises(ValueError):
                set_rlimit(LIMIT_NAME, (limits.hard + 1, limits.hard + 1))
            with self.assertRaises(ValueError):
                set_rlimit(LIMIT_NAME, (limits.hard + 1, limits.hard + 2))
        mock_setrlimit.assert_not_called()

    def test_prlimit_reads_the_limits_of_the_running_process(self):
        if not hasattr(resource_utils._resource, "prlimit"):
            self.skipTest("the platform does not provide prlimit")
        limits = prlimit(0, LIMIT_NAME)
        self.assertIsInstance(limits, Limit)
        self.assertEqual(limits, get_rlimit(LIMIT_NAME))

    def test_prlimit_validates_its_arguments(self):
        with self.assertRaises(TypeError):
            prlimit("0", LIMIT_NAME)  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            prlimit(-1, LIMIT_NAME)
        with self.assertRaises(ValueError):
            prlimit(0, "RLIMIT_DOES_NOT_EXIST")
        with self.assertRaises(TypeError):
            prlimit(0, LIMIT_NAME, "unlimited")  # type: ignore[arg-type]

    def test_prlimit_reports_a_platform_without_prlimit(self):
        with patch("resource_utils._resource", object()):
            with self.assertRaises(RuntimeError):
                prlimit(0, LIMIT_NAME)

    def test_get_rusage_reports_the_usage_of_the_process(self):
        usage = get_rusage()
        self.assertIsInstance(usage, Usage)
        self.assertGreaterEqual(usage.user_time, 0.0)
        self.assertGreaterEqual(usage.system_time, 0.0)
        self.assertGreaterEqual(usage.max_rss, 0)

    def test_get_rusage_reports_the_usage_of_the_children(self):
        usage = get_rusage(resource_utils.RUSAGE_CHILDREN)
        self.assertIsInstance(usage, Usage)

    def test_get_rusage_validates_its_arguments(self):
        with self.assertRaises(TypeError):
            get_rusage("self")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            get_rusage(9999)

    def test_usage_as_dict(self):
        usage = get_rusage()
        fields = usage_as_dict(usage)
        self.assertEqual(fields["user_time"], usage.user_time)
        self.assertIn("max_rss", fields)
        with self.assertRaises(TypeError):
            usage_as_dict((1, 2))  # type: ignore[arg-type]

    def test_get_page_size(self):
        size = get_page_size()
        self.assertIsInstance(size, int)
        self.assertGreater(size, 0)

    def test_helpers_report_a_missing_standard_library_module(self):
        with patch("resource_utils._resource", None):
            with self.assertRaises(RuntimeError):
                get_rlimit(LIMIT_NAME)
            with self.assertRaises(RuntimeError):
                set_rlimit(LIMIT_NAME, (1, 1))
            with self.assertRaises(RuntimeError):
                prlimit(0, LIMIT_NAME)
            with self.assertRaises(RuntimeError):
                get_rusage()
            with self.assertRaises(RuntimeError):
                get_page_size()
            self.assertFalse(is_available())

    def test_all_names_are_exported(self):
        self.assertIsNotNone(resource_utils.__all__)
        self.assertEqual(len(resource_utils.__all__), len(set(resource_utils.__all__)))
        for name in resource_utils.__all__:
            self.assertTrue(hasattr(resource_utils, name), name)


if __name__ == "__main__":
    unittest.main()
