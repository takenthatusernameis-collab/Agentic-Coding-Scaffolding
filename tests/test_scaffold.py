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
            "collections_utils.py",
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
            "tests/test_collections_utils.py",
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
             "list_utils.py",
             "tests/test_list_utils.py",
             "locale_utils.py",
             "tests/test_locale_utils.py",
             "env_utils.py",
             "tests/test_env_utils.py",
            "logging_utils.py",
            "tests/test_logging_utils.py",
            "cache_utils.py",
            "tests/test_cache_utils.py",
            "context_utils.py",
            "tests/test_context_utils.py",
            "timing_utils.py",
            "tests/test_timing_utils.py",
            "async_utils.py",
            "tests/test_async_utils.py",
            "bit_utils.py",
            "tests/test_bit_utils.py",
            "concurrent_utils.py",
            "tests/test_concurrent_utils.py",
            "priority_queue_utils.py",
            "tests/test_priority_queue_utils.py",
            "rate_limiter_utils.py",
            "tests/test_rate_limiter_utils.py",
            "retry_utils.py",
            "ring_buffer_utils.py",
            "tests/test_retry_utils.py",
            "tests/test_ring_buffer_utils.py",
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
            "operator_utils.py",
            "tests/test_operator_utils.py",
            "path_utils.py",
            "tests/test_path_utils.py",
            "color_utils.py",
            "tests/test_color_utils.py",
            "circuit_breaker_utils.py",
            "tests/test_circuit_breaker_utils.py",
            "pattern_utils.py",
            "tests/test_pattern_utils.py",
            "config_schema.py",
            "tests/test_config_schema.py",
            "copy_utils.py",
            "tests/test_copy_utils.py",
            "exceptions_utils.py",
            "tests/test_exceptions_utils.py",
            "exceptions_utils.py",
            "tests/test_exceptions_utils.py",
            "email_utils.py",
            "tests/test_email_utils.py",
            "enum_utils.py",
            "tests/test_enum_utils.py",
            "io_utils.py",
            "tests/test_io_utils.py",
            "ini_utils.py",
            "tests/test_ini_utils.py",
            "terminal_utils.py",
            "subprocess_utils.py",
            "tests/test_subprocess_utils.py",
            "tests/test_terminal_utils.py",
            "cli_utils.py",
            "tests/test_cli_utils.py",
            "hash_utils.py",
            "contextlib_utils.py",
            "hmac_utils.py",
            "tests/test_hash_utils.py",
            "tests/test_contextlib_utils.py",
            "tests/test_hmac_utils.py",
            "http_utils.py",
            "tests/test_http_utils.py",
            "inspect_utils.py",
            "tests/test_inspect_utils.py",
            "html_utils.py",
            "tests/test_html_utils.py",
            "deprecation_utils.py",
            "tests/test_deprecation_utils.py",
            "array_utils.py",
            "tests/test_array_utils.py",
            "base64_utils.py",
            "tests/test_base64_utils.py",
            "bisect_utils.py",
            "tests/test_bisect_utils.py",
            "calendar_utils.py",
            "colorsys_utils.py",
            "tests/test_calendar_utils.py",
            "call_once_utils.py",
            "tests/test_call_once_utils.py",
            "struct_utils.py",
            "tests/test_struct_utils.py",
            "duration_utils.py",
            "tests/test_duration_utils.py",
            "temp_utils.py",
            "tests/test_temp_utils.py",
            "xml_utils.py",
            "weakref_utils.py",
            "tests/test_xml_utils.py",
            "tests/test_weakref_utils.py",
            "argparse_utils.py",
            "tests/test_argparse_utils.py",
            "warnings_utils.py",
            "tests/test_warnings_utils.py",
            "seq_utils.py",
            "tests/test_seq_utils.py",
            "number_utils.py",
            "tests/test_number_utils.py",
            "os_utils.py",
            "tests/test_os_utils.py",
            "sort_utils.py",
            "tests/test_sort_utils.py",
            "graphlib_utils.py",
            "tests/test_graphlib_utils.py",
            "queue_utils.py",
            "tests/test_queue_utils.py",
            "version_utils.py",
            "tests/test_version_utils.py",
            "textwrap_utils.py",
            "tests/test_textwrap_utils.py",
            "bytes_utils.py",
            "tests/test_bytes_utils.py",
            "prime_utils.py",
            "tests/test_prime_utils.py",
            "sys_utils.py",
            "tests/test_sys_utils.py",
            "networking_utils.py",
            "tests/test_networking_utils.py",
            "decimal_utils.py",
            "tests/test_decimal_utils.py",
            "difflib_utils.py",
            "tests/test_difflib_utils.py",
            "fractions_utils.py",
            "tests/test_fractions_utils.py",
            "markdown_utils.py",
            "tests/test_markdown_utils.py",
            "heapq_utils.py",
            "tests/test_heapq_utils.py",
            "time_utils.py",
            "tests/test_time_utils.py",
            "timezone_utils.py",
            "tests/test_timezone_utils.py",
            "weakref_utils.py",
            "tests/test_weakref_utils.py",
            "argparse_utils.py",
            "tests/test_argparse_utils.py",
            "template_utils.py",
            "tests/test_template_utils.py",
            "semver_utils.py",
            "tests/test_semver_utils.py",
            "interval_utils.py",
            "tests/test_interval_utils.py",
            "threading_utils.py",
            "tests/test_threading_utils.py",
"selectors_utils.py",
             "tests/test_selectors_utils.py",
              "pprint_utils.py",
              "tests/test_pprint_utils.py",
"reprlib_utils.py",
"tests/test_reprlib_utils.py",
"traceback_utils.py",
"tests/test_traceback_utils.py",
"typing_utils.py",
"tests/test_typing_utils.py",
              "gzip_utils.py",
             "tests/test_gzip_utils.py",
             "plistlib_utils.py",
             "tests/test_plistlib_utils.py",
"glob_utils.py",
              "tests/test_glob_utils.py",
              "shlex_utils.py",
              "tests/test_shlex_utils.py",
              "keyword_utils.py",
              "tests/test_keyword_utils.py",
              "socketserver_utils.py",
              "tests/test_socketserver_utils.py",
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
            "circuit_breaker_utils.py",
            "deprecation_utils.py",
            "collections_utils.py",
            "locale_utils.py",
            "env_utils.py",
            "logging_utils.py",
            "cache_utils.py",
            "timing_utils.py",
            "concurrent_utils.py",
            "operator_utils.py",
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
            "operator_utils.py",
            "tests/test_operator_utils.py",
            "path_utils.py",
            "tests/test_path_utils.py",
            "config_schema.py",
            "tests/test_config_schema.py",
            "copy_utils.py",
            "tests/test_copy_utils.py",
            "exceptions_utils.py",
            "tests/test_exceptions_utils.py",
            "exceptions_utils.py",
            "tests/test_exceptions_utils.py",
            "email_utils.py",
            "tests/test_email_utils.py",
            "io_utils.py",
            "tests/test_io_utils.py",
            "ini_utils.py",
            "tests/test_ini_utils.py",
            "terminal_utils.py",
            "subprocess_utils.py",
            "tests/test_subprocess_utils.py",
            "tests/test_terminal_utils.py",
            "cli_utils.py",
            "tests/test_cli_utils.py",
            "hash_utils.py",
            "contextlib_utils.py",
            "hmac_utils.py",
            "tests/test_hash_utils.py",
            "tests/test_contextlib_utils.py",
            "tests/test_hmac_utils.py",
            "html_utils.py",
            "tests/test_html_utils.py",
            "deprecation_utils.py",
            "tests/test_deprecation_utils.py",
            "array_utils.py",
            "tests/test_array_utils.py",
            "base64_utils.py",
            "tests/test_base64_utils.py",
            "bisect_utils.py",
            "tests/test_bisect_utils.py",
            "calendar_utils.py",
            "cmath_utils.py",
            "tests/test_calendar_utils.py",
            "tests/test_cmath_utils.py",
            "threading_utils.py",
            "tests/test_threading_utils.py",
            "http_utils.py",
            "tests/test_http_utils.py",
            "inspect_utils.py",
            "tests/test_inspect_utils.py",
            "struct_utils.py",
            "tests/test_struct_utils.py",
            "duration_utils.py",
            "temp_utils.py",
            "xml_utils.py",
            "weakref_utils.py",
            "argparse_utils.py",
            "tests/test_argparse_utils.py",
            "warnings_utils.py",
            "tests/test_warnings_utils.py",
            "seq_utils.py",
            "graphlib_utils.py",
            "queue_utils.py",
            "version_utils.py",
            "textwrap_utils.py",
            "bytes_utils.py",
            "tests/test_bytes_utils.py",
            "prime_utils.py",
            "tests/test_prime_utils.py",
            "sys_utils.py",
            "networking_utils.py",
            "decimal_utils.py",
"fractions_utils.py",
             "heapq_utils.py",
             "time_utils.py",
             "selectors_utils.py",
             "gzip_utils.py",
             "plistlib_utils.py",
             "glob_utils.py",
             "shlex_utils.py",
             "keyword_utils.py",
              "socketserver_utils.py",
"pprint_utils.py",
"traceback_utils.py",
"typing_utils.py",
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
            "tests/test_path_utils.py",
            "tests/test_crypto_utils.py",
            "tests/test_config_utils.py",
            "tests/test_circuit_breaker_utils.py",
            "tests/test_deprecation_utils.py",
            "tests/test_collections_utils.py",
            "tests/test_env_utils.py",
            "tests/test_logging_utils.py",
            "tests/test_cache_utils.py",
            "tests/test_timing_utils.py",
            "tests/test_concurrent_utils.py",
            "tests/test_operator_utils.py",
            "tests/test_priority_queue_utils.py",
            "tests/test_type_utils.py",
            "tests/test_config_schema.py",
            "tests/test_copy_utils.py",
            "tests/test_email_utils.py",
            "tests/test_io_utils.py",
            "tests/test_terminal_utils.py",
            "tests/test_seq_utils.py",
            "tests/test_graphlib_utils.py",
            "tests/test_sys_utils.py",
            "tests/test_prime_utils.py",
            "tests/test_decimal_utils.py",
            "tests/test_heapq_utils.py",
            "tests/test_time_utils.py",
            "weakref_utils.py",
            "tests/test_weakref_utils.py",
            "argparse_utils.py",
            "tests/test_argparse_utils.py",
            "warnings_utils.py",
            "tests/test_warnings_utils.py",
            "template_utils.py",
            "tests/test_template_utils.py",
            "semver_utils.py",
            "tests/test_semver_utils.py",
            "interval_utils.py",
            "tests/test_interval_utils.py",
"tests/test_selectors_utils.py",
             "tests/test_gzip_utils.py",
             "tests/test_plistlib_utils.py",
             "tests/test_glob_utils.py",
             "tests/test_shlex_utils.py",
              "tests/test_keyword_utils.py",
              "tests/test_socketserver_utils.py",
"tests/test_pprint_utils.py",
"tests/test_traceback_utils.py",
"tests/test_typing_utils.py",
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
            "collections_utils.py",
            "locale_utils.py",
            "env_utils.py",
            "logging_utils.py",
            "cache_utils.py",
            "timing_utils.py",
            "concurrent_utils.py",
            "operator_utils.py",
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
            "operator_utils.py",
            "tests/test_operator_utils.py",
            "path_utils.py",
            "tests/test_path_utils.py",
            "config_schema.py",
            "tests/test_config_schema.py",
            "copy_utils.py",
            "tests/test_copy_utils.py",
            "exceptions_utils.py",
            "tests/test_exceptions_utils.py",
            "exceptions_utils.py",
            "tests/test_exceptions_utils.py",
            "email_utils.py",
            "tests/test_email_utils.py",
            "io_utils.py",
            "tests/test_io_utils.py",
            "ini_utils.py",
            "tests/test_ini_utils.py",
            "terminal_utils.py",
            "subprocess_utils.py",
            "tests/test_subprocess_utils.py",
            "tests/test_terminal_utils.py",
            "cli_utils.py",
            "tests/test_cli_utils.py",
            "hash_utils.py",
            "contextlib_utils.py",
            "hmac_utils.py",
            "tests/test_hash_utils.py",
            "tests/test_contextlib_utils.py",
            "tests/test_hmac_utils.py",
            "html_utils.py",
            "tests/test_html_utils.py",
            "deprecation_utils.py",
            "tests/test_deprecation_utils.py",
            "array_utils.py",
            "tests/test_array_utils.py",
            "base64_utils.py",
            "tests/test_base64_utils.py",
            "bisect_utils.py",
            "tests/test_bisect_utils.py",
            "calendar_utils.py",
            "cmath_utils.py",
            "tests/test_calendar_utils.py",
            "tests/test_cmath_utils.py",
            "threading_utils.py",
            "tests/test_threading_utils.py",
            "http_utils.py",
            "tests/test_http_utils.py",
            "inspect_utils.py",
            "tests/test_inspect_utils.py",
            "struct_utils.py",
            "tests/test_struct_utils.py",
            "duration_utils.py",
            "temp_utils.py",
            "xml_utils.py",
            "weakref_utils.py",
            "argparse_utils.py",
            "tests/test_argparse_utils.py",
            "warnings_utils.py",
            "tests/test_warnings_utils.py",
            "seq_utils.py",
            "graphlib_utils.py",
            "queue_utils.py",
            "version_utils.py",
            "textwrap_utils.py",
            "tests/test_textwrap_utils.py",
            "bytes_utils.py",
            "tests/test_bytes_utils.py",
            "prime_utils.py",
            "tests/test_prime_utils.py",
            "sys_utils.py",
            "tests/test_sys_utils.py",
            "networking_utils.py",
            "tests/test_networking_utils.py",
            "decimal_utils.py",
            "tests/test_decimal_utils.py",
            "fractions_utils.py",
            "tests/test_fractions_utils.py",
            "heapq_utils.py",
            "tests/test_heapq_utils.py",
            "time_utils.py",
            "tests/test_time_utils.py",
            "weakref_utils.py",
            "tests/test_weakref_utils.py",
            "argparse_utils.py",
            "tests/test_argparse_utils.py",
            "template_utils.py",
            "tests/test_template_utils.py",
            "semver_utils.py",
            "tests/test_semver_utils.py",
            "interval_utils.py",
            "tests/test_interval_utils.py",
"selectors_utils.py",
             "tests/test_selectors_utils.py",
             "socketserver_utils.py",
             "tests/test_socketserver_utils.py",
             "glob_utils.py",
             "shlex_utils.py",
             "keyword_utils.py",
             "linecache_utils.py",
              "pprint_utils.py",
              "tests/test_pprint_utils.py",
"reprlib_utils.py",
"tests/test_reprlib_utils.py",
"traceback_utils.py",
"tests/test_traceback_utils.py",
"typing_utils.py",
"tests/test_typing_utils.py",
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

    def test_collections_utils_functions_work(self) -> None:
        """Generated collections_utils.py should have working functions."""
        from collections_utils import (
            chunk,
            compact,
            deep_flatten,
            flatten,
            frequency,
            least_common,
            merge_dicts,
            most_common,
            partition_by,
            pluck,
            to_deque,
            uniq,
            uniq_by,
            windowed,
        )

        self.assertEqual(list(chunk([1, 2, 3, 4, 5], 2)), [[1, 2], [3, 4], [5]])
        self.assertEqual(flatten([1, [2, 3], [4], 5]), [1, 2, 3, 4, 5])
        self.assertEqual(deep_flatten([1, [2, [3, 4]], 5]), [1, 2, 3, 4, 5])
        self.assertEqual(list(windowed([1, 2, 3, 4], 2)), [(1, 2), (2, 3), (3, 4)])
        self.assertEqual(uniq([1, 2, 2, 3, 1]), [1, 2, 3])
        self.assertEqual(
            uniq_by([{"id": 1}, {"id": 2}, {"id": 1}], lambda x: x["id"]),
            [{"id": 1}, {"id": 2}],
        )
        self.assertEqual(frequency([1, 2, 2, 3])[2], 2)
        self.assertEqual(most_common([1, 2, 2, 3, 3, 3])[0], (3, 3))
        self.assertEqual(least_common([1, 2, 2, 3, 3, 3], n=1), [(1, 1)])
        self.assertEqual(merge_dicts({"a": 1}, {"b": 2}, {"a": 3}), {"a": 3, "b": 2})
        self.assertEqual(len(to_deque([1, 2, 3])), 3)
        self.assertEqual(pluck([{"a": 1}, {"a": 2}, {"b": 3}], "a"), [1, 2])
        self.assertEqual(compact([0, 1, False, 2, "", 3, None]), [1, 2, 3])
        self.assertEqual(
            partition_by([1, 1, 2, 2, 3], lambda x: x), [[1, 1], [2, 2], [3]]
        )

    def test_datetime_utils_functions_work(self) -> None:
        """Generated datetime_utils.py should have working functions."""
        from datetime import datetime

        from datetime_utils import add_days, days_between, is_leap_year, parse_datetime

        self.assertEqual(parse_datetime("2024-03-15 10:30:00"), datetime(2024, 3, 15, 10, 30, 0))
        self.assertEqual(days_between("2024-01-01", "2024-01-10"), 9)
        self.assertTrue(is_leap_year(2024))
        self.assertFalse(is_leap_year(2023))
        self.assertEqual(add_days("2024-01-01", 10), datetime(2024, 1, 11))

    def test_timezone_utils_functions_work(self) -> None:
        """Generated timezone_utils.py should have working functions."""
        import datetime

        from timezone_utils import (
            convert_datetime,
            format_datetime,
            get_timezone,
            get_utc_now,
            is_dst,
            is_valid_timezone,
            utc_offset,
        )

        self.assertTrue(is_valid_timezone("UTC"))
        self.assertFalse(is_valid_timezone("Not/AZone"))
        self.assertIsNone(get_timezone("Not/AZone"))
        self.assertIsNotNone(get_timezone("US/Eastern"))
        now = get_utc_now()
        self.assertIsNotNone(now.tzinfo)
        converted = convert_datetime(
            datetime.datetime(2024, 7, 15, 12, 0, 0, tzinfo=datetime.timezone.utc),
            "US/Eastern",
        )
        self.assertIsNotNone(converted)
        self.assertIsNotNone(format_datetime(now, "UTC"))
        self.assertIsNone(format_datetime(now, "Not/AZone"))
        self.assertEqual(utc_offset(now, "UTC"), "+00:00")
        self.assertFalse(is_dst(now, "UTC"))

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

    def test_locale_utils_functions_work(self) -> None:
        """Generated locale_utils.py should have working functions."""
        from locale_utils import (
            is_valid_locale,
            language_code,
            normalize_locale,
            region_code,
        )

        self.assertEqual(normalize_locale("en-us"), "en_US")
        self.assertEqual(normalize_locale("EN_us"), "en_US")
        self.assertEqual(normalize_locale("fr"), "fr")
        self.assertEqual(language_code("en-US"), "en")
        self.assertEqual(region_code("en-US"), "US")
        self.assertEqual(region_code("fr"), "")
        self.assertTrue(is_valid_locale("en-US"))
        self.assertTrue(is_valid_locale("fr"))
        self.assertFalse(is_valid_locale("123"))
        for fn in (normalize_locale, language_code, region_code):
            try:
                fn(123)  # type: ignore[arg-type]
            except TypeError:
                pass
            else:
                self.fail(f"expected TypeError from {fn.__name__}(123)")
        self.assertFalse(is_valid_locale(123))  # type: ignore[arg-type]

    def test_email_utils_functions_work(self) -> None:
        """Generated email_utils.py should have working functions."""
        import datetime

        from email_utils import (
            email_format_datetime,
            email_formataddr,
            email_formatdate,
            email_getaddresses,
            email_make_msgid,
            email_mktime_tz,
            email_parseaddr,
            email_parsedate,
            email_parsedate_to_datetime,
            email_quote,
            email_unquote,
        )

        self.assertTrue(email_formatdate())
        self.assertTrue(email_formatdate(usegmt=True))
        self.assertTrue(email_formatdate(localtime=True))
        self.assertEqual(email_parseaddr("User <user@example.com>"), ("User", "user@example.com"))
        self.assertEqual(email_formataddr(("User", "user@example.com")).count("@"), 1)
        addrs = email_getaddresses(["User <user@example.com>"])
        self.assertEqual(addrs, [("User", "user@example.com")])
        self.assertTrue(email_make_msgid().startswith("<") and email_make_msgid().endswith(">"))
        self.assertIsInstance(email_mktime_tz((2015, 10, 21, 7, 28, 0, 0, 0, 0, 0)), (int, float))
        parsed = email_parsedate("Wed, 21 Oct 2015 07:28:00 GMT")
        self.assertIsNotNone(parsed)
        assert parsed is not None
        self.assertEqual(parsed[0], 2015)
        self.assertEqual(email_parsedate_to_datetime("Wed, 21 Oct 2015 07:28:00 GMT").year, 2015)
        self.assertIsNone(email_parsedate("not a date"))
        self.assertIsInstance(email_quote('say "hi"'), str)
        self.assertIsInstance(email_unquote('say "hi"'), str)
        dt = datetime.datetime(2015, 10, 21, 7, 28, 0, tzinfo=datetime.timezone.utc)
        self.assertIn("Oct", email_format_datetime(dt))

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

    def test_color_utils_functions_work(self) -> None:
        """Generated color_utils.py should have working functions."""
        from color_utils import (
            adjust_brightness,
            blend_colors,
            get_contrast_ratio,
            get_luminance,
            hex_to_rgb,
            hsl_to_rgb,
            is_accessible,
            rgb_to_hex,
            validate_hex,
        )

        self.assertTrue(validate_hex("#ff5733"))
        self.assertFalse(validate_hex("#gg5733"))
        self.assertEqual(hex_to_rgb("#ff5733"), (255, 87, 51))
        self.assertEqual(rgb_to_hex(255, 87, 51), "#ff5733")
        self.assertAlmostEqual(get_luminance("#000000"), 0.0)
        self.assertAlmostEqual(get_luminance("#ffffff"), 1.0)
        self.assertAlmostEqual(get_contrast_ratio("#000000", "#ffffff"), 21.0)
        self.assertTrue(is_accessible("#000000", "#ffffff"))
        self.assertEqual(hsl_to_rgb(0, 1.0, 0.5), (255, 0, 0))
        self.assertEqual(adjust_brightness("#000000", 2.0), "#000000")
        self.assertEqual(blend_colors("#000000", "#ffffff", 0.5), "#808080")

    def test_pattern_utils_functions_work(self) -> None:
        """Generated pattern_utils.py should have working functions."""
        from pattern_utils import Factory, Observable, Observer, Singleton, Strategy

        class Service(metaclass=Singleton):
            pass

        self.assertIs(Service(), Service())

        factory = Factory()
        factory.register("greeter", lambda name: f"hi {name}")
        self.assertEqual(factory.create("greeter", "pat"), "hi pat")

        class MyObserver(Observer):
            def __init__(self) -> None:
                self.calls: list = []

            def update(self, subject, data=None):
                self.calls.append(data)

        subject = Observable()
        observer = MyObserver()
        subject.attach(observer)
        subject.notify("event")
        self.assertEqual(observer.calls, ["event"])

        class MyStrategy(Strategy):
            def execute(self, value: int) -> int:
                return value * 2

        self.assertEqual(MyStrategy().execute(21), 42)

    def test_bytes_utils_functions_work(self) -> None:
        """Generated bytes_utils.py should have working functions."""
        from bytes_utils import chunk, from_hex, to_hex, xor

        self.assertEqual(to_hex(b"abc"), "616263")
        self.assertEqual(from_hex("616263"), b"abc")
        self.assertEqual(xor(b"abc", b"\x01"), b"`cb")
        self.assertEqual(chunk(b"abcdef", 2), [b"ab", b"cd", b"ef"])

    def test_warnings_utils_functions_work(self) -> None:
        """Generated warnings_utils.py should have working functions."""
        import warnings

        from warnings_utils import catch_warnings, filterwarnings, resetwarnings, simplefilter, warn

        with catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            warn("hello")
            self.assertIsNotNone(caught)
            self.assertEqual(len(caught), 1)  # type: ignore[arg-type]
            self.assertEqual(str(caught[0].message), "hello")  # type: ignore[index]

        with self.assertRaises(TypeError):
            warn(123)  # type: ignore[arg-type]

        with self.assertRaises(ValueError):
            simplefilter("bogus")

        filterwarnings("ignore")
        resetwarnings()

    def test_cmath_utils_functions_work(self):
        """Generated cmath_utils.py should have working functions."""
        import math

        from cmath_utils import (
            acos,
            acosh,
            asin,
            asinh,
            atan,
            atanh,
            cos,
            cosh,
            exp,
            isclose,
            isfinite,
            isinf,
            isnan,
            log,
            log10,
            phase,
            polar,
            rect,
            sin,
            sinh,
            sqrt,
            tan,
            tanh,
        )

        self.assertEqual(phase(1), 0.0)
        self.assertEqual(phase(-1), math.pi)
        self.assertAlmostEqual(phase(1 + 1j), math.pi / 4)
        modulus, ph = polar(1 + 1j)
        self.assertAlmostEqual(modulus, math.sqrt(2))
        self.assertAlmostEqual(ph, math.pi / 4)
        self.assertEqual(exp(0), 1 + 0j)
        self.assertAlmostEqual(exp(1).real, math.e)
        self.assertEqual(log(1), 0j)
        self.assertAlmostEqual(log(math.e).real, 1.0)
        self.assertAlmostEqual(log(8, 2).real, 3.0)
        self.assertEqual(log10(1), 0j)
        self.assertAlmostEqual(log10(100).real, 2.0)
        self.assertEqual(sqrt(-1), 1j)
        self.assertEqual(sqrt(4), 2 + 0j)
        self.assertEqual(sin(0), 0j)
        self.assertAlmostEqual(sin(math.pi / 2).real, 1.0)
        self.assertEqual(cos(0), 1 + 0j)
        self.assertAlmostEqual(cos(math.pi).real, -1.0)
        self.assertEqual(tan(0), 0j)
        self.assertEqual(asin(0), 0j)
        self.assertAlmostEqual(asin(1).real, math.pi / 2)
        self.assertEqual(acos(1), 0j)
        self.assertEqual(atan(0), 0j)
        self.assertEqual(sinh(0), 0j)
        self.assertEqual(cosh(0), 1 + 0j)
        self.assertEqual(tanh(0), 0j)
        self.assertEqual(asinh(0), 0j)
        self.assertEqual(acosh(1), 0j)
        self.assertEqual(atanh(0), 0j)
        self.assertTrue(isfinite(1 + 2j))
        self.assertFalse(isfinite(complex(math.inf, 0)))
        self.assertTrue(isinf(complex(math.inf, 0)))
        self.assertFalse(isinf(1 + 2j))
        self.assertTrue(isnan(complex(math.nan, 0)))
        self.assertFalse(isnan(1 + 2j))
        self.assertTrue(isclose(1 + 1j, 1 + 1j))
        self.assertFalse(isclose(1 + 1j, 1 + 2j))

        # round-trip rect <-> polar
        r, phi = 2.0, math.pi / 3
        z = rect(r, phi)
        m2, p2 = polar(z)
        self.assertAlmostEqual(m2, r)
        self.assertAlmostEqual(p2 % (2 * math.pi), phi % (2 * math.pi))

        # input validation
        for fn in (
            phase,
            polar,
            exp,
            log,
            log10,
            sqrt,
            sin,
            cos,
            tan,
            asin,
            acos,
            atan,
            sinh,
            cosh,
            tanh,
            asinh,
            acosh,
            atanh,
            isfinite,
            isinf,
            isnan,
        ):
            with self.assertRaises(TypeError):
                fn("not-a-number")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            rect("2", 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            rect(2, "1")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            log("1", 2)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            log(1, "2")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            isclose(1, 1, rel_tol=-1)
        with self.assertRaises(ValueError):
            isclose(1, 1, abs_tol=-1)

    def test_threading_utils_functions_work(self):
        """Generated threading_utils.py should have working functions."""
        import threading

        from threading_utils import (
            active_count,
            create_bounded_semaphore,
            create_condition,
            create_event,
            create_lock,
            create_rlock,
            create_semaphore,
            create_thread,
            create_timer,
            current_thread,
            enumerate_threads,
            synchronized,
        )

        lock = create_lock()
        self.assertIsInstance(lock, type(threading.Lock()))

        rlock = create_rlock()
        self.assertIsInstance(rlock, type(threading.RLock()))

        sem = create_semaphore(2)
        self.assertTrue(sem.acquire())
        self.assertTrue(sem.acquire())
        self.assertFalse(sem.acquire(blocking=False))
        sem.release()
        sem.release()

        bsem = create_bounded_semaphore(1)
        self.assertIsInstance(bsem, threading.BoundedSemaphore)

        event = create_event()
        self.assertFalse(event.is_set())
        event.set()
        self.assertTrue(event.is_set())
        event.clear()
        self.assertFalse(event.is_set())

        cond = create_condition(lock)
        self.assertIsInstance(cond, threading.Condition)

        called = []

        def callback() -> None:
            called.append(True)

        timer = create_timer(0.01, callback)
        self.assertIsInstance(timer, threading.Timer)
        timer.cancel()

        results = []

        def worker(value: int) -> int:
            results.append(value)
            return value

        thread = create_thread(worker, args=(7,))
        thread.start()
        thread.join()
        self.assertEqual(results, [7])

        self.assertIsInstance(current_thread(), threading.Thread)
        self.assertGreaterEqual(active_count(), 1)
        threads = enumerate_threads()
        self.assertIsInstance(threads, list)
        self.assertIn(current_thread(), threads)

        @synchronized(lock)
        def guarded(value: int) -> int:
            return value

        self.assertEqual(guarded(42), 42)

    def test_typing_utils_functions_work(self):
        """Generated typing_utils.py should have working functions."""
        import typing
        from typing import List, Optional, TypedDict

        from typing_utils import (
            ClassVar,
            Final,
            Literal,
            get_args,
            get_origin,
            get_type_hints,
            is_typeddict,
            overload,
        )

        def greet(name: str) -> str:
            return f"hello {name}"

        hints = get_type_hints(greet)
        self.assertEqual(hints["name"], str)
        self.assertEqual(hints["return"], str)

        self.assertEqual(get_origin(List[int]), list)
        self.assertIsNone(get_origin(int))

        self.assertEqual(get_args(List[int]), (int,))
        self.assertEqual(get_args(dict), ())
        self.assertEqual(get_args(Optional[str]), (str, type(None)))

        class Point(TypedDict):
            x: int
            y: int

        self.assertTrue(is_typeddict(Point))
        self.assertFalse(is_typeddict(int))

        self.assertIs(overload, typing.overload)
        self.assertIs(Final, typing.Final)
        self.assertIs(Literal, typing.Literal)
        self.assertIs(ClassVar, typing.ClassVar)


    def test_traceback_utils_functions_work(self):
        """Generated traceback_utils.py should have working functions."""
        from traceback_utils import (
            extract_stack,
            format_exc,
            format_exception,
            format_exception_only,
            format_stack,
        )

        result = format_exception_only(ValueError, ValueError("boom"))
        self.assertIsInstance(result, list)
        self.assertTrue(any("boom" in line for line in result))

        try:
            raise RuntimeError("kaboom")
        except RuntimeError as exc:
            result = format_exception(exc)
        self.assertIsInstance(result, list)
        self.assertTrue(any("kaboom" in line for line in result))

        result = extract_stack()
        self.assertIsInstance(result, list)
        self.assertGreaterEqual(len(result), 1)

        result = format_stack()
        self.assertIsInstance(result, list)
        self.assertGreaterEqual(len(result), 1)

        result = format_exc()
        self.assertIsInstance(result, str)
        self.assertEqual(result, "")

        try:
            raise RuntimeError("traceback test")
        except RuntimeError:
            result = format_exc()
        self.assertIsInstance(result, str)
        self.assertIn("RuntimeError", result)


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
