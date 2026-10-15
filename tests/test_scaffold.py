"""Tests for the scaffold.sh generator.

These tests invoke the real scaffold.sh script in a temporary directory and
verify that the generated project configuration is complete and consistent.
"""

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
SCAFFOLD = ROOT / "scaffold.sh"


class TestScaffoldKiloJson(unittest.TestCase):
    """Verify scaffold.sh emits a complete, valid kilo.json."""

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="scaffold-test-"))
        self.project_dir = self.tmp / "my-project"
        # --no-test keeps the run fast and hermetic.
        result = subprocess.run(
            ["bash", str(SCAFFOLD), "My Project", str(self.project_dir), "--no-test"],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        self.assertEqual(
            result.returncode,
            0,
            msg=(
                f"scaffold.sh failed:\nstdout:\n{result.stdout}\n"
                f"stderr:\n{result.stderr}"
            ),
        )

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_kilo_json_is_valid(self) -> None:
        kilo_json = self.project_dir / "kilo.json"
        self.assertTrue(kilo_json.is_file(), "kilo.json was not generated")
        data = json.loads(kilo_json.read_text())
        self.assertIsInstance(data, dict)

    def test_kilo_json_has_scaffolder_subagent(self) -> None:
        """Scaffolded projects must define the scaffolder subagent.

        The scaffolding system depends on this subagent being present so that
        scaffolded repositories can themselves scaffold further projects.
        """
        data = json.loads((self.project_dir / "kilo.json").read_text())
        agents = data.get("agent", {})
        self.assertIn(
            "scaffolder",
            agents,
            msg="kilo.json is missing the 'scaffolder' subagent",
        )
        scaffolder = agents["scaffolder"]
        self.assertEqual(scaffolder.get("mode"), "subagent")
        self.assertEqual(scaffolder.get("model"), "kilo/kilo-auto/free")
        self.assertIsInstance(scaffolder.get("description"), str)
        self.assertTrue(scaffolder["description"].strip())

    def test_kilo_json_permission_is_allow(self) -> None:
        data = json.loads((self.project_dir / "kilo.json").read_text())
        self.assertEqual(data.get("permission"), "allow")

    def test_required_files_generated(self) -> None:
        expected = [
            "AGENTS.md",
            "README.md",
            "CHANGELOG.md",
            "Makefile",
            "pyproject.toml",
            "hello.py",
            "calculator.py",
            "config_utils.py",
            "shapes.py",
            "strings.py",
            "utils.py",
            "stats.py",
            "math_utils.py",
            "data_utils.py",
            ".gitignore",
            "LICENSE",
            ".pre-commit-config.yaml",
            ".kilo/.gitignore",
            ".kilo/agent/scaffolder.md",
            ".kilo/command/handover.md",
            ".kilo/command/scaffold-project.md",
            ".kilo/skill/scaffolding-helper.md",
            ".github/workflows/main.yml",
            "tests/test_hello.py",
            "tests/test_calculator.py",
            "tests/test_config_utils.py",
            "tests/test_shapes.py",
            "tests/test_strings.py",
            "tests/test_utils.py",
            "tests/test_stats.py",
            "tests/test_math_utils.py",
            "tests/test_data_utils.py",
            "file_utils.py",
            "tests/test_file_utils.py",
            "datetime_utils.py",
            "tests/test_datetime_utils.py",
            "url_utils.py",
            "tests/test_url_utils.py",
            "uuid_utils.py",
            "tests/test_uuid_utils.py",
            "prompt_utils.py",
            "tests/test_prompt_utils.py",
            "random_utils.py",
            "tests/test_random_utils.py",
            "validation_utils.py",
            "tests/test_validation_utils.py",
            "crypto_utils.py",
            "tests/test_crypto_utils.py",
            "env_utils.py",
            "tests/test_env_utils.py",
            "logging_utils.py",
            "tests/test_logging_utils.py",
            "cache_utils.py",
            "tests/test_cache_utils.py",
            "timing_utils.py",
            "tests/test_timing_utils.py",
            "concurrent_utils.py",
            "tests/test_concurrent_utils.py",
            "priority_queue_utils.py",
            "tests/test_priority_queue_utils.py",
            "rate_limiter_utils.py",
            "tests/test_rate_limiter_utils.py",
            "retry_utils.py",
            "tests/test_retry_utils.py",
            "dict_utils.py",
            "tests/test_dict_utils.py",
            "set_utils.py",
            "tests/test_set_utils.py",
            "statistics_utils.py",
            "tests/test_statistics_utils.py",
            "string_utils.py",
            "tests/test_string_utils.py",
            "tree_utils.py",
            "tests/test_tree_utils.py",
            "uuid_utils.py",
            "tests/test_uuid_utils.py",
            "prompt_utils.py",
            "tests/test_prompt_utils.py",
            "type_utils.py",
            "tests/test_type_utils.py",
        ]
        for rel in expected:
            path = self.project_dir / rel
            self.assertTrue(path.is_file(), f"Expected generated file missing: {rel}")

    def test_pyproject_has_ruff_config(self) -> None:
        content = (self.project_dir / "pyproject.toml").read_text()
        self.assertIn("[tool.ruff]", content)
        self.assertIn("[tool.ruff.lint]", content)
        self.assertIn('select = ["E", "F", "I", "W"]', content)

    def test_makefile_has_typecheck_and_pre_commit_targets(self) -> None:
        content = (self.project_dir / "Makefile").read_text()
        self.assertIn("typecheck:", content)
        self.assertIn("pre-commit-install:", content)
        self.assertIn("pre-commit-run:", content)

    def test_pre_commit_config_is_valid(self) -> None:
        content = (self.project_dir / ".pre-commit-config.yaml").read_text()
        self.assertIn("ruff", content)
        self.assertIn("mypy", content)
        self.assertIn("unittest", content)
        self.assertIn("scaffold-test", content)

    def test_calculator_has_all_operations(self) -> None:
        content = (self.project_dir / "calculator.py").read_text()
        self.assertIn("def add(", content)
        self.assertIn("def subtract(", content)
        self.assertIn("def multiply(", content)
        self.assertIn("def divide(", content)

    def test_shapes_has_all_functions(self) -> None:
        content = (self.project_dir / "shapes.py").read_text()
        self.assertIn("def circle_area(", content)
        self.assertIn("def circle_perimeter(", content)
        self.assertIn("def rectangle_area(", content)
        self.assertIn("def rectangle_perimeter(", content)
        self.assertIn("def triangle_area(", content)
        self.assertIn("def triangle_perimeter(", content)

    def test_readme_contains_calculator_and_new_files(self) -> None:
        """README.md should document all generated modules and config files."""
        content = (self.project_dir / "README.md").read_text()
        self.assertIn("calculator.py", content)
        self.assertIn("shapes.py", content)
        self.assertIn("test_shapes.py", content)
        self.assertIn("CHANGELOG.md", content)
        self.assertIn(".pre-commit-config.yaml", content)
        self.assertIn("Ignore patterns for .kilo directory", content)
        self.assertIn("test_calculator.py", content)

    def test_scaffold_project_doc_lists_shapes(self) -> None:
        """The scaffold-project command doc should list shapes.py and its tests."""
        content = (self.project_dir / ".kilo/command/scaffold-project.md").read_text()
        self.assertIn("shapes.py", content)
        self.assertIn("tests/test_shapes.py", content)

    def test_scaffold_project_doc_lists_all_modules(self) -> None:
        """The scaffold-project command doc should list all modules and tests."""
        content = (self.project_dir / ".kilo/command/scaffold-project.md").read_text()
        for module in [
            "stats.py",
            "math_utils.py",
            "data_utils.py",
            "datetime_utils.py",
            "file_utils.py",
            "url_utils.py",
            "uuid_utils.py",
            "prompt_utils.py",
            "random_utils.py",
            "validation_utils.py",
            "crypto_utils.py",
            "config_utils.py",
            "env_utils.py",
            "logging_utils.py",
            "cache_utils.py",
            "timing_utils.py",
            "concurrent_utils.py",
            "priority_queue_utils.py",
            "rate_limiter_utils.py",
            "retry_utils.py",
            "dict_utils.py",
            "tests/test_rate_limiter_utils.py",
            "tests/test_retry_utils.py",
            "tests/test_dict_utils.py",
            "set_utils.py",
            "tests/test_set_utils.py",
            "statistics_utils.py",
            "tests/test_statistics_utils.py",
            "string_utils.py",
            "tests/test_string_utils.py",
            "tree_utils.py",
            "tests/test_tree_utils.py",
            "uuid_utils.py",
            "tests/test_uuid_utils.py",
            "prompt_utils.py",
            "tests/test_prompt_utils.py",
            "type_utils.py",
            "tests/test_type_utils.py",
        ]:
            self.assertIn(module, content, f"scaffold-project.md missing {module}")
        for test in [
            "tests/test_stats.py",
            "tests/test_math_utils.py",
            "tests/test_data_utils.py",
            "tests/test_datetime_utils.py",
            "tests/test_file_utils.py",
            "tests/test_url_utils.py",
            "tests/test_uuid_utils.py",
            "tests/test_prompt_utils.py",
            "tests/test_random_utils.py",
            "tests/test_validation_utils.py",
            "tests/test_crypto_utils.py",
            "tests/test_config_utils.py",
            "tests/test_env_utils.py",
            "tests/test_logging_utils.py",
            "tests/test_cache_utils.py",
            "tests/test_timing_utils.py",
            "tests/test_concurrent_utils.py",
            "tests/test_priority_queue_utils.py",
            "tests/test_type_utils.py",
        ]:
            self.assertIn(test, content, f"scaffold-project.md missing {test}")

    def test_scaffold_project_doc_no_inconsistent_indent(self) -> None:
        """scaffold-project.md list items should not have extra leading spaces."""
        content = (self.project_dir / ".kilo/command/scaffold-project.md").read_text()
        for line in content.splitlines():
            self.assertFalse(
                line.startswith("  - "),
                msg=f"Line has inconsistent indentation: {line!r}",
            )

    def test_changelog_lists_all_modules(self) -> None:
        """Generated CHANGELOG.md should list all modules and their tests."""
        content = (self.project_dir / "CHANGELOG.md").read_text()
        for module in [
            "stats.py",
            "math_utils.py",
            "data_utils.py",
            "datetime_utils.py",
            "file_utils.py",
            "url_utils.py",
            "uuid_utils.py",
            "prompt_utils.py",
            "random_utils.py",
            "validation_utils.py",
            "crypto_utils.py",
            "config_utils.py",
            "env_utils.py",
            "logging_utils.py",
            "cache_utils.py",
            "timing_utils.py",
            "concurrent_utils.py",
            "priority_queue_utils.py",
            "rate_limiter_utils.py",
            "retry_utils.py",
            "dict_utils.py",
            "tests/test_rate_limiter_utils.py",
            "tests/test_retry_utils.py",
            "tests/test_dict_utils.py",
            "set_utils.py",
            "tests/test_set_utils.py",
            "statistics_utils.py",
            "tests/test_statistics_utils.py",
            "string_utils.py",
            "tests/test_string_utils.py",
            "tree_utils.py",
            "tests/test_tree_utils.py",
            "uuid_utils.py",
            "tests/test_uuid_utils.py",
            "prompt_utils.py",
            "tests/test_prompt_utils.py",
        ]:
            self.assertIn(module, content, f"CHANGELOG.md missing {module}")

    def test_file_utils_no_unused_os_import(self) -> None:
        """Generated file_utils.py should not import the unused `os` module."""
        content = (self.project_dir / "file_utils.py").read_text()
        self.assertNotIn("import os", content)

    def test_readme_makefile_table_includes_all_targets(self) -> None:
        """README Makefile table must include typecheck and pre-commit targets."""
        content = (self.project_dir / "README.md").read_text()
        self.assertIn("make typecheck", content)
        self.assertIn("make pre-commit-install", content)
        self.assertIn("make pre-commit-run", content)

    def test_changelog_lists_new_files(self) -> None:
        """Generated CHANGELOG.md should mention the new modules and config."""
        content = (self.project_dir / "CHANGELOG.md").read_text()
        self.assertIn("calculator.py", content)
        self.assertIn(".pre-commit-config.yaml", content)
        self.assertIn("CHANGELOG.md", content)
        self.assertIn(".kilo/.gitignore", content)
        self.assertIn("strings.py", content)
        self.assertIn("utils.py", content)
        self.assertIn("stats.py", content)
        self.assertIn("tests/test_strings.py", content)
        self.assertIn("tests/test_utils.py", content)
        self.assertIn("tests/test_stats.py", content)

    def test_stats_functions_work(self) -> None:
        """Generated stats.py should have working functions."""
        from stats import mean, median, mode, stddev, variance

        self.assertEqual(mean([1, 2, 3]), 2.0)
        self.assertEqual(median([1, 2, 3]), 2.0)
        self.assertEqual(median([1, 2, 3, 4]), 2.5)
        self.assertEqual(mode([1, 1, 2]), 1)
        self.assertAlmostEqual(variance([1, 2, 3]), 0.6666666667, places=5)
        self.assertAlmostEqual(stddev([1, 2, 3]), 0.8164965809, places=5)
    def test_math_utils_functions_work(self) -> None:
        """Generated math_utils.py should have working functions."""
        from math_utils import clamp, factorial, fibonacci, gcd, is_prime, lcm

        self.assertEqual(factorial(5), 120)
        self.assertEqual(fibonacci(5), 5)
        self.assertEqual(gcd(48, 18), 6)
        self.assertEqual(lcm(4, 6), 12)
        self.assertTrue(is_prime(17))
        self.assertFalse(is_prime(9))
        self.assertEqual(clamp(5, 0, 10), 5)

    def test_datetime_utils_functions_work(self) -> None:
        """Generated datetime_utils.py should have working functions."""
        from datetime import datetime

        from datetime_utils import add_days, days_between, is_leap_year, parse_datetime

        self.assertEqual(parse_datetime("2024-03-15 10:30:00"), datetime(2024, 3, 15, 10, 30, 0))
        self.assertEqual(days_between("2024-01-01", "2024-01-10"), 9)
        self.assertTrue(is_leap_year(2024))
        self.assertFalse(is_leap_year(2023))
        self.assertEqual(add_days("2024-01-01", 10), datetime(2024, 1, 11))

    def test_url_utils_functions_work(self) -> None:
        """Generated url_utils.py should have working functions."""
        from url_utils import add_query_param, build_url, extract_domain, is_valid_url

        self.assertTrue(is_valid_url("https://example.com"))
        self.assertFalse(is_valid_url("not-a-url"))
        self.assertEqual(extract_domain("https://api.example.com:8080"), "api.example.com")
        result = add_query_param("https://example.com", "q", "test")
        self.assertIn("q=test", result)
        url = build_url(scheme="https", domain="example.com", path="/api", params={"k": "v"})
        self.assertIn("/api", url)
        self.assertIn("k=v", url)

    def test_crypto_utils_functions_work(self) -> None:
        """Generated crypto_utils.py should have working functions."""
        from crypto_utils import base64_decode, base64_encode, generate_token, hash_string

        self.assertEqual(len(hash_string("hello")), 64)
        self.assertEqual(len(hash_string("hello", algorithm="md5")), 32)
        self.assertEqual(base64_decode(base64_encode("hello")), "hello")
        self.assertEqual(len(generate_token(16)), 32)

    def test_env_utils_functions_work(self) -> None:
        """Generated env_utils.py should have working functions."""
        from env_utils import (
            ensure_env,
            get_env,
            get_env_bool,
            get_env_int,
            set_env,
            unset_env,
        )

        with mock.patch.dict(os.environ, {}, clear=True):
            set_env("TEST_ENV_INT", 42)
            self.assertEqual(get_env("TEST_ENV_INT"), "42")
            self.assertEqual(get_env_int("TEST_ENV_INT"), 42)
            set_env("TEST_ENV_BOOL", "true")
            self.assertIs(get_env_bool("TEST_ENV_BOOL"), True)
            self.assertEqual(ensure_env("NEW_VAR", "default"), "default")
            self.assertEqual(os.environ["NEW_VAR"], "default")
            self.assertTrue(unset_env("NEW_VAR"))
            self.assertFalse(unset_env("NEW_VAR"))

    def test_logging_utils_functions_work(self) -> None:
        """Generated logging_utils.py should have working functions."""
        import logging as _logging

        from logging_utils import configure_logging, get_logger, log_calls

        logger = get_logger("test_logging")
        self.assertIsInstance(logger, _logging.Logger)
        self.assertEqual(logger.name, "test_logging")
        self.assertIs(logger, _logging.getLogger("test_logging"))

        root = configure_logging(level=_logging.INFO, force=True)
        try:
            self.assertIs(root, _logging.getLogger())
            self.assertEqual(_logging.getLogger().level, _logging.INFO)

            @log_calls(level=_logging.DEBUG)
            def add(a: int, b: int) -> int:
                return a + b

            with self.assertLogs("logging_utils", level="DEBUG") as cm:
                result = add(2, 3)
            self.assertEqual(result, 5)
            self.assertEqual(len(cm.records), 2)
            self.assertIn("Calling", cm.records[0].getMessage())
            self.assertIn("returned", cm.records[1].getMessage())
        finally:
            _logging.getLogger().setLevel(_logging.WARNING)

    def test_cache_utils_functions_work(self) -> None:
        """Generated cache_utils.py should have working functions."""
        from cache_utils import cache_info, clear_cache, memoize

        calls = [0]

        @memoize()
        def square(n: int) -> int:
            calls[0] += 1
            return n * n

        self.assertEqual(square(4), 16)
        self.assertEqual(square(4), 16)
        self.assertEqual(calls[0], 1)

        info = square.cache_info()  # type: ignore[attr-defined]
        self.assertEqual(info["hits"], 1)
        self.assertEqual(info["misses"], 1)

        square.clear_cache()  # type: ignore[attr-defined]
        info = square.cache_info()  # type: ignore[attr-defined]
        self.assertEqual(info["currsize"], 0)

        clear_cache(square)
        self.assertEqual(square(4), 16)
        self.assertEqual(calls[0], 2)

        info = cache_info(square)
        self.assertEqual(info["misses"], 1)

    def test_timing_utils_functions_work(self) -> None:
        """Generated timing_utils.py should have working functions."""
        import time

        from timing_utils import benchmark, elapsed_time, timer

        with timer("Test") as t:
            pass
        self.assertGreaterEqual(t.elapsed, 0.0)

        start = time.perf_counter()
        elapsed = elapsed_time(start)
        self.assertGreaterEqual(elapsed, 0.0)
        self.assertIsInstance(elapsed, float)

        call_count = 0

        @benchmark(iterations=2)
        def test_func():
            nonlocal call_count
            call_count += 1
            return "success"

        result = test_func()
        self.assertEqual(result, "success")
        self.assertEqual(call_count, 2)

    def test_concurrent_utils_functions_work(self) -> None:
        """Generated concurrent_utils.py should have working functions."""
        import asyncio

        from concurrent_utils import ProcessPool, ThreadPool, _inc, run_async, to_async

        with ThreadPool(max_workers=2) as thread_pool:
            results = list(thread_pool.map(lambda x: x * 2, [1, 2, 3]))
        self.assertEqual(results, [2, 4, 6])

        with ProcessPool(max_workers=2) as process_pool:
            results = list(process_pool.map(_inc, [1, 2, 3]))
        self.assertEqual(results, [2, 3, 4])

        async def async_add(a: int, b: int) -> int:
            await asyncio.sleep(0.001)
            return a + b

        result = run_async(async_add(1, 2))
        self.assertEqual(result, 3)

        def sync_mul(a: int, b: int) -> int:
            return a * b

        async_mul = to_async(sync_mul)
        result = run_async(async_mul(3, 4))
        self.assertEqual(result, 12)

    def test_priority_queue_utils_functions_work(self) -> None:
        """Generated priority_queue_utils.py should have working functions."""
        from priority_queue_utils import (
            PriorityQueue,
            create_priority_queue,
            merge_queues,
            pop_priority,
            push_priority,
        )

        pq: PriorityQueue[str] = PriorityQueue()
        push_priority(pq, "low", priority=10)
        push_priority(pq, "high", priority=1)
        push_priority(pq, "medium", priority=5)
        self.assertEqual(pop_priority(pq), "high")
        self.assertEqual(pop_priority(pq), "medium")
        self.assertEqual(pop_priority(pq), "low")

        pq2: PriorityQueue[str] = create_priority_queue([(1.0, "a"), (2.0, "b")])
        self.assertEqual(pq2.pop(), "a")
        self.assertEqual(pq2.pop(), "b")

        pq3: PriorityQueue[str] = PriorityQueue()
        push_priority(pq3, "x", priority=3)
        pq4: PriorityQueue[str] = PriorityQueue()
        push_priority(pq4, "y", priority=1)
        merged = merge_queues(pq3, pq4)
        self.assertEqual(merged.pop(), "y")
        self.assertEqual(merged.pop(), "x")

    def test_statistics_utils_functions_work(self) -> None:
        """Generated statistics_utils.py should have working functions."""
        from statistics_utils import (
            correlation,
            covariance,
            geometric_mean,
            harmonic_mean,
            normalize,
            percentile,
            z_score,
        )

        self.assertAlmostEqual(harmonic_mean([1, 2, 4]), 1.7142857142857142)
        self.assertAlmostEqual(geometric_mean([1, 2, 3, 4, 5]), 2.605171084697352)
        self.assertEqual(percentile([1, 2, 3, 4, 5], 50), 3.0)
        self.assertAlmostEqual(covariance([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]), -2.5)
        self.assertAlmostEqual(correlation([1, 2, 3, 4, 5], [5, 4, 3, 2, 1]), -1.0)
        z = z_score([1, 2, 3, 4, 5])
        self.assertAlmostEqual(z[0], -1.414213562373095)
        self.assertAlmostEqual(z[4], 1.414213562373095)
        self.assertEqual(normalize([1, 2, 3, 4, 5]), [0.0, 0.25, 0.5, 0.75, 1.0])


class TestScaffoldProjectNameNormalization(unittest.TestCase):
    """Verify project names are normalized into safe identifiers."""

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="scaffold-name-"))

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def _scaffold(self, name: str) -> Path:
        out = self.tmp / "out"
        result = subprocess.run(
            ["bash", str(SCAFFOLD), name, str(out), "--no-test"],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
        self.assertEqual(
            result.returncode,
            0,
            msg=f"scaffold.sh failed for name '{name}':\n{result.stderr}",
        )
        return out

    def test_spaces_and_mixed_case_normalized(self) -> None:
        out = self._scaffold("My Cool Tool")
        # Directory name should be normalized to lowercase hyphenated form.
        self.assertTrue((out / "pyproject.toml").is_file())
        content = (out / "pyproject.toml").read_text()
        self.assertIn('name = "my-cool-tool"', content)

    def test_special_chars_stripped(self) -> None:
        out = self._scaffold("Awesome!!! Project @#$ 123")
        content = (out / "pyproject.toml").read_text()
        # Only lowercase letters, digits, and hyphens should remain.
        for line in content.splitlines():
            if line.startswith("name = "):
                self.assertRegex(line, r'name = "[a-z0-9-]+"')




class TestScaffoldNoTestFlag(unittest.TestCase):
    """Verify the --no-test flag is parsed correctly in various positions."""

    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="scaffold-notest-"))

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_no_test_as_third_arg_skips_smoke_test(self) -> None:
        out = self.tmp / "project"
        result = subprocess.run(
            ["bash", str(SCAFFOLD), "My Project", str(out), "--no-test"],
            capture_output=True,
            text=True,
            timeout=120,
            check=True,
        )
        self.assertIn("Smoke test skipped", result.stdout)

    def test_no_test_without_output_dir_skips_smoke_test(self) -> None:
        out = self.tmp / "my-project"
        result = subprocess.run(
            ["bash", str(SCAFFOLD), "My Project", "--no-test"],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(self.tmp),
            check=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Smoke test skipped", result.stdout)
        # Output dir defaults to ./<project-id> relative to cwd.
        self.assertTrue((out / "pyproject.toml").is_file())

    def test_no_test_as_third_arg_does_not_set_output_dir(self) -> None:
        out = self.tmp / "project"
        subprocess.run(
            ["bash", str(SCAFFOLD), "My Project", str(out), "--no-test"],
            capture_output=True,
            text=True,
            timeout=120,
            check=True,
        )
        # The output dir should be the real path, not "--no-test".
        self.assertTrue((out / "pyproject.toml").is_file())


if __name__ == "__main__":
    unittest.main()
