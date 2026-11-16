import unittest
from unittest import mock

import profile_utils


class TestProfileUtils(unittest.TestCase):
    def test_new_profiler(self):
        p = profile_utils.new_profiler()
        self.assertIsInstance(p, profile_utils.Profile)

    def test_run(self):
        profile_utils.run("x = 1 + 2")

    def test_runctx(self):
        ns = {}
        profile_utils.runctx("x = 1 + 2", ns, ns)
        self.assertEqual(ns["x"], 3)

    def test_run_rejects_a_non_string(self):
        with self.assertRaises(TypeError):
            profile_utils.run(123)  # type: ignore[arg-type]

    def test_runctx_rejects_a_non_string(self):
        with self.assertRaises(TypeError):
            profile_utils.runctx(123, {}, {})  # type: ignore[arg-type]

    def test_main_delegates_to_the_standard_library(self):
        with mock.patch.object(profile_utils._profile, "main") as main:
            profile_utils.main()
            main.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
