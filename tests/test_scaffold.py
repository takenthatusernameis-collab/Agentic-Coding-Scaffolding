"""Tests for the scaffold.sh generator.

These tests invoke the real scaffold.sh script in a temporary directory and
verify that the generated project configuration is complete and consistent.
"""

import json
import os
import re
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
            msg=(f"scaffold.sh failed:\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"),
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
            "abc_utils.py",
            "ast_utils.py",
            "pickle_utils.py",
            "marshal_utils.py",
            "importlib_utils.py",
            "atexit_utils.py",
            "multiprocessing_utils.py",
            "concurrent_futures_utils.py",
            "zipfile_utils.py",
            "bz2_utils.py",
            "lzma_utils.py",
            "signal_utils.py",
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
            "tests/test_abc_utils.py",
            "tests/test_ast_utils.py",
            "tests/test_pickle_utils.py",
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
            "dbm_utils.py",
            "tests/test_dbm_utils.py",
            "url_utils.py",
            "tests/test_url_utils.py",
            "uuid_utils.py",
            "tests/test_uuid_utils.py",
            "prompt_utils.py",
            "tests/test_prompt_utils.py",
            "random_utils.py",
            "re_utils.py",
            "rlcompleter_utils.py",
            "tempfile_utils.py",
            "tests/test_random_utils.py",
            "tests/test_re_utils.py",
            "tests/test_rlcompleter_utils.py",
            "tests/test_tempfile_utils.py",
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
            "tty_utils.py",
            "tests/test_tty_utils.py",
            "doctest_utils.py",
            "tests/test_doctest_utils.py",
            "tools/refresh_scaffold.py",
            "scaffold.sh",
            "async_utils.py",
            "tests/test_async_utils.py",
            "bit_utils.py",
            "tests/test_bit_utils.py",
            "concurrent_utils.py",
            "concurrent_futures_utils.py",
            "tests/test_concurrent_utils.py",
            "tests/test_concurrent_futures_utils.py",
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
            "genericpath_utils.py",
            "ntpath_utils.py",
            "nturl2path_utils.py",
            "curses_utils.py",
            "bdb_utils.py",
            "pdb_utils.py",
            "site_utils.py",
            "posixpath_utils.py",
            "tests/test_genericpath_utils.py",
            "tests/test_ntpath_utils.py",
            "tests/test_nturl2path_utils.py",
            "tests/test_curses_utils.py",
            "tests/test_bdb_utils.py",
            "tests/test_pdb_utils.py",
            "tests/test_site_utils.py",
            "tests/test_posixpath_utils.py",
            "set_utils.py",
            "tests/test_set_utils.py",
            "stat_utils.py",
            "tests/test_stat_utils.py",
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
            "concurrent_futures_utils.py",
            "tests/test_concurrent_futures_utils.py",
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
            "trace_utils.py",
            "pstats_utils.py",
            "select_utils.py",
            "imaplib_utils.py",
            "mailbox_utils.py",
            "mailcap_utils.py",
            "mailbox_utils.py",
            "mailcap_utils.py",
"wave_utils.py",
             "uu_utils.py",
             "zipapp_utils.py",
              "py_compile_utils.py",
              "pyclbr_utils.py",
              "xdrlib_utils.py",
              "smtplib_utils.py",
              "compileall_utils.py",
             "modulefinder_utils.py",
             "optparse_utils.py",
             "symtable_utils.py",
             "profile_utils.py",
             "tests/test_trace_utils.py",
             "tests/test_pstats_utils.py",
             "tests/test_select_utils.py",
             "tests/test_imaplib_utils.py",
             "tests/test_mailbox_utils.py",
             "tests/test_mailcap_utils.py",
             "tests/test_mailbox_utils.py",
             "tests/test_mailcap_utils.py",
             "tests/test_wave_utils.py",
             "tests/test_uu_utils.py",
             "tests/test_zipapp_utils.py",
              "tests/test_py_compile_utils.py",
              "tests/test_pyclbr_utils.py",
              "tests/test_xdrlib_utils.py",
              "tests/test_smtplib_utils.py",
              "tests/test_compileall_utils.py",
             "tests/test_modulefinder_utils.py",
             "tests/test_optparse_utils.py",
             "tests/test_symtable_utils.py",
             "tests/test_profile_utils.py",
             "calendar_utils.py",
            "colorsys_utils.py",
            "tests/test_calendar_utils.py",
             "cmath_utils.py",
             "tests/test_cmath_utils.py",
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
            "timeit_utils.py",
            "tests/test_timeit_utils.py",
            "timeit_utils.py",
            "tests/test_timeit_utils.py",
            "asyncio_utils.py",
            "tests/test_asyncio_utils.py",
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
            "codecs_utils.py",
            "tests/test_codecs_utils.py",
            "traceback_utils.py",
            "tests/test_traceback_utils.py",
            "typing_utils.py",
            "tests/test_typing_utils.py",
            "gzip_utils.py",
            "tests/test_gzip_utils.py",
            "plistlib_utils.py",
            "tests/test_plistlib_utils.py",
            "gettext_utils.py",
            "tests/test_gettext_utils.py",
            "glob_utils.py",
            "tests/test_glob_utils.py",
            "shlex_utils.py",
            "tests/test_shlex_utils.py",
            "keyword_utils.py",
            "tests/test_keyword_utils.py",
            "socketserver_utils.py",
            "tests/test_socketserver_utils.py",
            "sqlite3_utils.py",
            "tests/test_sqlite3_utils.py",
            "marshal_utils.py",
            "tests/test_marshal_utils.py",
            "pkgutil_utils.py",
            "tests/test_pkgutil_utils.py",
            "unicodedata_utils.py",
            "tests/test_unicodedata_utils.py",
            "unittest_utils.py",
            "tests/test_unittest_utils.py",
            "unittest_utils.py",
            "tests/test_unittest_utils.py",
            "tomllib_utils.py",
            "tests/test_tomllib_utils.py",
            "token_utils.py",
            "tests/test_token_utils.py",
            "sched_utils.py",
            "tests/test_sched_utils.py",
            "quopri_utils.py",
            "tests/test_quopri_utils.py",
            "numbers_utils.py",
            "tests/test_numbers_utils.py",
            "netrc_utils.py",
            "tests/test_netrc_utils.py",
            "getopt_utils.py",
            "tests/test_getopt_utils.py",
            "filecmp_utils.py",
            "tests/test_filecmp_utils.py",
            "errno_utils.py",
            "tests/test_errno_utils.py",
            "dis_utils.py",
            "tests/test_dis_utils.py",
            "contextvars_utils.py",
            "tests/test_contextvars_utils.py",
            "configparser_utils.py",
            "tests/test_configparser_utils.py",
            "shelve_utils.py",
            "tests/test_shelve_utils.py",
            "binascii_utils.py",
            "tests/test_binascii_utils.py",
            "importlib_utils.py",
            "atexit_utils.py",
            "multiprocessing_utils.py",
            "concurrent_futures_utils.py",
            "zipfile_utils.py",
            "tests/test_zipfile_utils.py",
            "tests/test_concurrent_futures_utils.py",
            "bz2_utils.py",
            "tests/test_bz2_utils.py",
            "lzma_utils.py",
            "tests/test_lzma_utils.py",
            "signal_utils.py",
            "tests/test_signal_utils.py",
"bz2_utils.py",
             "tests/test_bz2_utils.py",
             "bz2_utils.py",
             "tests/test_bz2_utils.py",
             "cmd_utils.py",
             "tests/test_cmd_utils.py",
             "this_utils.py",
             "tokenize_utils.py",
             "tests/test_this_utils.py",
             "tests/test_tokenize_utils.py",
             "socket_utils.py",
             "tests/test_socket_utils.py",
             "sysconfig_utils.py",
             "tests/test_sysconfig_utils.py",
             "mimetypes_utils.py",
             "tests/test_mimetypes_utils.py",
             "doctest_utils.py",
             "tests/test_doctest_utils.py",
             "tools/refresh_scaffold.py",
"code_utils.py",
            "tests/test_code_utils.py",
            "codeop_utils.py",
            "tests/test_codeop_utils.py",
            "copyreg_utils.py",
            "tests/test_copyreg_utils.py",
            "fileinput_utils.py",
            "tests/test_fileinput_utils.py",
            "fnmatch_utils.py",
              "ftplib_utils.py",
            "tests/test_fnmatch_utils.py",
              "tests/test_ftplib_utils.py",
            "getpass_utils.py",
            "tests/test_getpass_utils.py",
            "id_utils.py",
            "tests/test_id_utils.py",
            "memoize_utils.py",
            "tests/test_memoize_utils.py",
            "pathlib_utils.py",
              "poplib_utils.py",
            "tests/test_pathlib_utils.py",
              "tests/test_poplib_utils.py",
            "webbrowser_utils.py",
            "tests/test_webbrowser_utils.py",
            "xmlrpc_utils.py",
            "tests/test_xmlrpc_utils.py",
            "syslog_utils.py",
            "faulthandler_utils.py",
            "tests/test_syslog_utils.py",
            "tests/test_faulthandler_utils.py",
            "resource_utils.py",
            "tests/test_resource_utils.py",
            "pwd_utils.py",
            "tests/test_pwd_utils.py",
            "grp_utils.py",
            "tests/test_grp_utils.py",
            "termios_utils.py",
            "tests/test_termios_utils.py",
            "fcntl_utils.py",
            "pty_utils.py",
            "stringprep_utils.py",
            "tabnanny_utils.py",
            "encodings_utils.py",
            "zipimport_utils.py",
            "ipaddress_utils.py",
            "pydoc_utils.py",
            "pydoc_data_utils.py",
            "wsgiref_utils.py",
            "antigravity_utils.py",
            "tests/test_fcntl_utils.py",
            "tests/test_pty_utils.py",
            "tests/test_stringprep_utils.py",
            "tests/test_tabnanny_utils.py",
            "tests/test_encodings_utils.py",
            "tests/test_zipimport_utils.py",
            "tests/test_ipaddress_utils.py",
            "tests/test_pydoc_utils.py",
            "tests/test_pydoc_data_utils.py",
            "tests/test_wsgiref_utils.py",
            "runpy_utils.py",
            "tests/test_runpy_utils.py",
            "secrets_utils.py",
            "tests/test_secrets_utils.py",
            "ssl_utils.py",
            "tests/test_ssl_utils.py",
            "tarfile_utils.py",
            "tests/test_tarfile_utils.py",
            "types_utils.py",
            "tests/test_types_utils.py",
            "pickletools_utils.py",
            "tests/test_pickletools_utils.py",
            "zoneinfo_utils.py",
            "opcode_utils.py",
            "tests/test_zoneinfo_utils.py",
            "tests/test_opcode_utils.py",
            "opcode_utils.py",
            "tests/test_opcode_utils.py",
            "tests/test_atexit_utils.py",
            "tests/test_colorsys_utils.py",
            "compression_utils.py",
            "tests/test_compression_utils.py",
            "csv_utils.py",
            "tests/test_csv_utils.py",
            "ctypes_utils.py",
            "tests/test_ctypes_utils.py",
            "dataclasses_utils.py",
            "tests/test_dataclasses_utils.py",
            "functools_utils.py",
            "tests/test_functools_utils.py",
            "gc_utils.py",
            "tests/test_gc_utils.py",
            "greeting_utils.py",
            "tests/test_greeting_utils.py",
            "hashlib_utils.py",
            "tests/test_hashlib_utils.py",
            "tests/test_importlib_utils.py",
            "ip_utils.py",
            "tests/test_ip_utils.py",
            "itertools_utils.py",
            "tests/test_itertools_utils.py",
            "json_utils.py",
            "tests/test_json_utils.py",
            "tests/test_linecache_utils.py",
            "tests/test_multiprocessing_utils.py",
            "platform_utils.py",
            "tests/test_platform_utils.py",
            "regex_utils.py",
            "tests/test_regex_utils.py",
            "shutil_utils.py",
            "tests/test_shutil_utils.py",
            "zlib_utils.py",
            "tests/test_zlib_utils.py",
            "tracemalloc_utils.py",
            "tests/test_tracemalloc_utils.py",
            "mmap_utils.py",
            "tests/test_mmap_utils.py",
            "wsgiref_utils.py",
            "antigravity_utils.py",
            "tests/test_wsgiref_utils.py",
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

    def test_templated_documents_substitute_the_project_name(self) -> None:
        """The project name placeholder must be replaced in generated documents."""
        for relative in ("README.md", "AGENTS.md", "CHANGELOG.md"):
            with self.subTest(document=relative):
                content = (self.project_dir / relative).read_text()
                self.assertNotIn("${PROJECT_NAME}", content)
        readme = (self.project_dir / "README.md").read_text()
        self.assertTrue(readme.startswith("# My Project"))
        agents = (self.project_dir / "AGENTS.md").read_text()
        self.assertIn("Project: My Project", agents)

    def test_scaffold_project_doc_lists_shapes(self) -> None:
        """The scaffold-project command doc should list shapes.py and its tests."""
        content = (self.project_dir / ".kilo/command/scaffold-project.md").read_text()
        self.assertIn("shapes.py", content)
        self.assertIn("tests/test_shapes.py", content)

    def test_scaffold_project_doc_lists_all_modules(self) -> None:
        """The scaffold-project command doc should list all modules and tests."""
        content = (self.project_dir / ".kilo/command/scaffold-project.md").read_text()
        for module in [
            "abc_utils.py",
            "ast_utils.py",
            "pickle_utils.py",
            "marshal_utils.py",
            "tests/test_marshal_utils.py",
            "pkgutil_utils.py",
            "tests/test_pkgutil_utils.py",
            "unicodedata_utils.py",
            "tests/test_unicodedata_utils.py",
            "unittest_utils.py",
            "tests/test_unittest_utils.py",
            "unittest_utils.py",
            "tests/test_unittest_utils.py",
            "tomllib_utils.py",
            "tests/test_tomllib_utils.py",
            "token_utils.py",
            "tests/test_token_utils.py",
            "sched_utils.py",
            "tests/test_sched_utils.py",
            "quopri_utils.py",
            "tests/test_quopri_utils.py",
            "numbers_utils.py",
            "tests/test_numbers_utils.py",
            "netrc_utils.py",
            "tests/test_netrc_utils.py",
            "getopt_utils.py",
            "tests/test_getopt_utils.py",
            "filecmp_utils.py",
            "tests/test_filecmp_utils.py",
            "errno_utils.py",
            "tests/test_errno_utils.py",
            "dis_utils.py",
            "tests/test_dis_utils.py",
            "contextvars_utils.py",
            "tests/test_contextvars_utils.py",
            "configparser_utils.py",
            "tests/test_configparser_utils.py",
            "shelve_utils.py",
            "tests/test_shelve_utils.py",
            "binascii_utils.py",
            "tests/test_binascii_utils.py",
            "importlib_utils.py",
            "atexit_utils.py",
            "multiprocessing_utils.py",
            "concurrent_futures_utils.py",
            "zipfile_utils.py",
            "tests/test_zipfile_utils.py",
            "tests/test_concurrent_futures_utils.py",
            "bz2_utils.py",
            "tests/test_bz2_utils.py",
            "lzma_utils.py",
            "tests/test_lzma_utils.py",
            "signal_utils.py",
            "tests/test_signal_utils.py",
            "stats.py",
            "math_utils.py",
            "data_utils.py",
            "datetime_utils.py",
            "file_utils.py",
            "url_utils.py",
            "uuid_utils.py",
            "prompt_utils.py",
            "random_utils.py",
            "re_utils.py",
            "rlcompleter_utils.py",
            "tempfile_utils.py",
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
            "concurrent_futures_utils.py",
            "operator_utils.py",
            "priority_queue_utils.py",
            "rate_limiter_utils.py",
            "retry_utils.py",
            "dict_utils.py",
            "tests/test_rate_limiter_utils.py",
            "tests/test_retry_utils.py",
            "tests/test_dict_utils.py",
            "genericpath_utils.py",
            "ntpath_utils.py",
            "nturl2path_utils.py",
            "curses_utils.py",
            "bdb_utils.py",
            "pdb_utils.py",
            "site_utils.py",
            "posixpath_utils.py",
            "tests/test_genericpath_utils.py",
            "tests/test_ntpath_utils.py",
            "tests/test_nturl2path_utils.py",
            "tests/test_curses_utils.py",
            "tests/test_bdb_utils.py",
            "tests/test_pdb_utils.py",
            "tests/test_site_utils.py",
            "tests/test_posixpath_utils.py",
            "set_utils.py",
            "tests/test_set_utils.py",
            "stat_utils.py",
            "tests/test_stat_utils.py",
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
            "concurrent_futures_utils.py",
            "tests/test_concurrent_futures_utils.py",
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
            "trace_utils.py",
            "pstats_utils.py",
            "select_utils.py",
            "imaplib_utils.py",
            "mailbox_utils.py",
            "mailcap_utils.py",
            "mailbox_utils.py",
            "mailcap_utils.py",
            "wave_utils.py",
"uu_utils.py",
             "zipapp_utils.py",
              "py_compile_utils.py",
              "pyclbr_utils.py",
              "xdrlib_utils.py",
              "smtplib_utils.py",
              "compileall_utils.py",
             "modulefinder_utils.py",
             "optparse_utils.py",
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
            "gettext_utils.py",
            "tests/test_gettext_utils.py",
            "glob_utils.py",
            "shlex_utils.py",
            "keyword_utils.py",
            "socketserver_utils.py",
            "sqlite3_utils.py",
            "pprint_utils.py",
            "traceback_utils.py",
            "typing_utils.py",
            "pickle_utils.py",
            "marshal_utils.py",
            "importlib_utils.py",
            "atexit_utils.py",
            "multiprocessing_utils.py",
            "concurrent_futures_utils.py",
            "zipfile_utils.py",
            "tests/test_zipfile_utils.py",
            "tests/test_concurrent_futures_utils.py",
            "lzma_utils.py",
            "tests/test_lzma_utils.py",
            "signal_utils.py",
            "tests/test_signal_utils.py",
            "cmd_utils.py",
            "tests/test_cmd_utils.py",
            "this_utils.py",
            "tokenize_utils.py",
            "tests/test_this_utils.py",
            "tests/test_tokenize_utils.py",
            "socket_utils.py",
            "tests/test_socket_utils.py",
            "sysconfig_utils.py",
            "mimetypes_utils.py",
            "code_utils.py",
            "tests/test_code_utils.py",
            "copyreg_utils.py",
            "tests/test_copyreg_utils.py",
            "fileinput_utils.py",
            "tests/test_fileinput_utils.py",
            "fnmatch_utils.py",
              "ftplib_utils.py",
            "tests/test_fnmatch_utils.py",
              "tests/test_ftplib_utils.py",
            "getpass_utils.py",
            "tests/test_getpass_utils.py",
            "id_utils.py",
            "tests/test_id_utils.py",
            "memoize_utils.py",
            "tests/test_memoize_utils.py",
            "pathlib_utils.py",
              "poplib_utils.py",
            "tests/test_pathlib_utils.py",
              "tests/test_poplib_utils.py",
            "webbrowser_utils.py",
            "tests/test_webbrowser_utils.py",
            "xmlrpc_utils.py",
            "tests/test_xmlrpc_utils.py",
            "syslog_utils.py",
            "faulthandler_utils.py",
            "tests/test_syslog_utils.py",
            "tests/test_faulthandler_utils.py",
            "resource_utils.py",
            "tests/test_resource_utils.py",
            "pwd_utils.py",
            "tests/test_pwd_utils.py",
            "grp_utils.py",
            "tests/test_grp_utils.py",
            "termios_utils.py",
            "tests/test_termios_utils.py",
            "fcntl_utils.py",
            "pty_utils.py",
            "stringprep_utils.py",
            "tabnanny_utils.py",
            "encodings_utils.py",
            "zipimport_utils.py",
            "ipaddress_utils.py",
            "pydoc_utils.py",
            "pydoc_data_utils.py",
            "wsgiref_utils.py",
            "antigravity_utils.py",
            "tests/test_fcntl_utils.py",
            "tests/test_pty_utils.py",
            "tests/test_stringprep_utils.py",
            "tests/test_tabnanny_utils.py",
            "tests/test_encodings_utils.py",
            "tests/test_zipimport_utils.py",
            "tests/test_ipaddress_utils.py",
            "tests/test_pydoc_utils.py",
            "tests/test_pydoc_data_utils.py",
            "tests/test_wsgiref_utils.py",
            "runpy_utils.py",
            "tests/test_runpy_utils.py",
            "secrets_utils.py",
            "tests/test_secrets_utils.py",
            "ssl_utils.py",
            "tests/test_ssl_utils.py",
            "tarfile_utils.py",
            "tests/test_tarfile_utils.py",
            "types_utils.py",
            "tests/test_types_utils.py",
            "pickletools_utils.py",
            "tests/test_pickletools_utils.py",
            "zoneinfo_utils.py",
            "opcode_utils.py",
            "tests/test_zoneinfo_utils.py",
            "tests/test_opcode_utils.py",
            "opcode_utils.py",
            "tests/test_opcode_utils.py",
            "tests/test_atexit_utils.py",
            "tests/test_colorsys_utils.py",
            "compression_utils.py",
            "tests/test_compression_utils.py",
            "csv_utils.py",
            "tests/test_csv_utils.py",
            "ctypes_utils.py",
            "tests/test_ctypes_utils.py",
            "dataclasses_utils.py",
            "tests/test_dataclasses_utils.py",
            "functools_utils.py",
            "tests/test_functools_utils.py",
            "gc_utils.py",
            "tests/test_gc_utils.py",
            "greeting_utils.py",
            "tests/test_greeting_utils.py",
            "hashlib_utils.py",
            "tests/test_hashlib_utils.py",
            "tests/test_importlib_utils.py",
            "ip_utils.py",
            "tests/test_ip_utils.py",
            "itertools_utils.py",
            "tests/test_itertools_utils.py",
            "json_utils.py",
            "tests/test_json_utils.py",
            "tests/test_linecache_utils.py",
            "tests/test_multiprocessing_utils.py",
            "platform_utils.py",
            "tests/test_platform_utils.py",
            "regex_utils.py",
            "tests/test_regex_utils.py",
            "shutil_utils.py",
            "tests/test_shutil_utils.py",
            "zlib_utils.py",
            "tests/test_zlib_utils.py",
            "wsgiref_utils.py",
            "antigravity_utils.py",
            "tests/test_wsgiref_utils.py",
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
            "tests/test_re_utils.py",
            "tests/test_rlcompleter_utils.py",
            "tests/test_tempfile_utils.py",
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
            "tests/test_concurrent_futures_utils.py",
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
            "tests/test_sqlite3_utils.py",
            "tests/test_pprint_utils.py",
            "tests/test_traceback_utils.py",
            "tests/test_typing_utils.py",
            "tests/test_pickle_utils.py",
            "tests/test_marshal_utils.py",
            "tests/test_lzma_utils.py",
            "tests/test_pkgutil_utils.py",
            "tests/test_unicodedata_utils.py",
            "tests/test_tomllib_utils.py",
            "tests/test_token_utils.py",
            "tests/test_sched_utils.py",
            "tests/test_quopri_utils.py",
            "tests/test_numbers_utils.py",
            "tests/test_netrc_utils.py",
            "tests/test_getopt_utils.py",
            "tests/test_filecmp_utils.py",
            "tests/test_errno_utils.py",
            "tests/test_dis_utils.py",
            "tests/test_contextvars_utils.py",
            "tests/test_configparser_utils.py",
            "tests/test_shelve_utils.py",
            "tests/test_binascii_utils.py",
            "tests/test_cmd_utils.py",
            "tests/test_this_utils.py",
            "tests/test_tokenize_utils.py",
            "tests/test_socket_utils.py",
            "tests/test_sysconfig_utils.py",
            "tests/test_mimetypes_utils.py",
            "tests/test_code_utils.py",
            "tests/test_copyreg_utils.py",
            "tests/test_fileinput_utils.py",
            "tests/test_fnmatch_utils.py",
              "tests/test_ftplib_utils.py",
            "tests/test_getpass_utils.py",
            "tests/test_id_utils.py",
            "tests/test_memoize_utils.py",
            "tests/test_pathlib_utils.py",
              "tests/test_poplib_utils.py",
            "tests/test_webbrowser_utils.py",
            "tests/test_xmlrpc_utils.py",
            "tests/test_syslog_utils.py",
            "tests/test_resource_utils.py",
            "tests/test_pwd_utils.py",
            "tests/test_grp_utils.py",
            "tests/test_termios_utils.py",
            "tests/test_fcntl_utils.py",
            "tests/test_pty_utils.py",
            "tests/test_stringprep_utils.py",
            "tests/test_tabnanny_utils.py",
            "tests/test_encodings_utils.py",
            "tests/test_zipimport_utils.py",
            "tests/test_ipaddress_utils.py",
            "tests/test_pydoc_utils.py",
            "tests/test_pydoc_data_utils.py",
            "tests/test_wsgiref_utils.py",
            "tests/test_runpy_utils.py",
            "tests/test_secrets_utils.py",
            "tests/test_ssl_utils.py",
            "tests/test_tarfile_utils.py",
            "tests/test_types_utils.py",
            "tests/test_zoneinfo_utils.py",
            "tests/test_opcode_utils.py",
            "tests/test_atexit_utils.py",
            "tests/test_colorsys_utils.py",
            "tests/test_compression_utils.py",
            "tests/test_csv_utils.py",
            "tests/test_ctypes_utils.py",
            "tests/test_dataclasses_utils.py",
            "tests/test_functools_utils.py",
            "tests/test_gc_utils.py",
            "tests/test_greeting_utils.py",
            "tests/test_hashlib_utils.py",
            "tests/test_importlib_utils.py",
            "tests/test_ip_utils.py",
            "tests/test_itertools_utils.py",
            "tests/test_json_utils.py",
            "tests/test_linecache_utils.py",
            "tests/test_multiprocessing_utils.py",
            "tests/test_platform_utils.py",
            "tests/test_regex_utils.py",
            "tests/test_shutil_utils.py",
            "tests/test_zlib_utils.py",
             "cmath_utils.py",
             "tests/test_cmath_utils.py",
            "tests/test_wsgiref_utils.py",
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
            "re_utils.py",
            "rlcompleter_utils.py",
            "tests/test_rlcompleter_utils.py",
            "tempfile_utils.py",
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
            "concurrent_futures_utils.py",
            "operator_utils.py",
            "priority_queue_utils.py",
            "rate_limiter_utils.py",
            "retry_utils.py",
            "dict_utils.py",
            "tests/test_rate_limiter_utils.py",
            "tests/test_retry_utils.py",
            "tests/test_dict_utils.py",
            "genericpath_utils.py",
            "ntpath_utils.py",
            "nturl2path_utils.py",
            "curses_utils.py",
            "bdb_utils.py",
            "pdb_utils.py",
            "site_utils.py",
            "posixpath_utils.py",
            "tests/test_genericpath_utils.py",
            "tests/test_ntpath_utils.py",
            "tests/test_nturl2path_utils.py",
            "tests/test_curses_utils.py",
            "tests/test_bdb_utils.py",
            "tests/test_pdb_utils.py",
            "tests/test_site_utils.py",
            "tests/test_posixpath_utils.py",
            "set_utils.py",
            "tests/test_set_utils.py",
            "stat_utils.py",
            "tests/test_stat_utils.py",
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
            "concurrent_futures_utils.py",
            "tests/test_concurrent_futures_utils.py",
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
            "trace_utils.py",
            "pstats_utils.py",
            "select_utils.py",
            "imaplib_utils.py",
            "mailbox_utils.py",
            "mailcap_utils.py",
            "mailbox_utils.py",
            "mailcap_utils.py",
            "wave_utils.py",
"uu_utils.py",
             "zipapp_utils.py",
              "py_compile_utils.py",
              "pyclbr_utils.py",
              "xdrlib_utils.py",
              "smtplib_utils.py",
              "compileall_utils.py",
             "modulefinder_utils.py",
             "optparse_utils.py",
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
            "timeit_utils.py",
            "tests/test_timeit_utils.py",
            "timeit_utils.py",
            "tests/test_timeit_utils.py",
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
            "sqlite3_utils.py",
            "tests/test_socketserver_utils.py",
            "tests/test_sqlite3_utils.py",
            "gettext_utils.py",
            "tests/test_gettext_utils.py",
            "glob_utils.py",
            "shlex_utils.py",
            "keyword_utils.py",
            "linecache_utils.py",
            "pprint_utils.py",
            "tests/test_pprint_utils.py",
            "reprlib_utils.py",
            "tests/test_reprlib_utils.py",
            "codecs_utils.py",
            "tests/test_codecs_utils.py",
            "traceback_utils.py",
            "tests/test_traceback_utils.py",
            "typing_utils.py",
            "tests/test_typing_utils.py",
            "pickle_utils.py",
            "tests/test_pickle_utils.py",
            "marshal_utils.py",
            "tests/test_marshal_utils.py",
            "pkgutil_utils.py",
            "tests/test_pkgutil_utils.py",
            "unicodedata_utils.py",
            "tests/test_unicodedata_utils.py",
            "unittest_utils.py",
            "tests/test_unittest_utils.py",
            "unittest_utils.py",
            "tests/test_unittest_utils.py",
            "tomllib_utils.py",
            "tests/test_tomllib_utils.py",
            "token_utils.py",
            "tests/test_token_utils.py",
            "sched_utils.py",
            "tests/test_sched_utils.py",
            "quopri_utils.py",
            "tests/test_quopri_utils.py",
            "numbers_utils.py",
            "tests/test_numbers_utils.py",
            "netrc_utils.py",
            "tests/test_netrc_utils.py",
            "getopt_utils.py",
            "tests/test_getopt_utils.py",
            "filecmp_utils.py",
            "tests/test_filecmp_utils.py",
            "errno_utils.py",
            "tests/test_errno_utils.py",
            "dis_utils.py",
            "tests/test_dis_utils.py",
            "contextvars_utils.py",
            "tests/test_contextvars_utils.py",
            "configparser_utils.py",
            "tests/test_configparser_utils.py",
            "shelve_utils.py",
            "tests/test_shelve_utils.py",
            "binascii_utils.py",
            "tests/test_binascii_utils.py",
            "importlib_utils.py",
            "atexit_utils.py",
            "multiprocessing_utils.py",
            "concurrent_futures_utils.py",
            "zipfile_utils.py",
            "tests/test_zipfile_utils.py",
            "tests/test_concurrent_futures_utils.py",
            "lzma_utils.py",
            "tests/test_lzma_utils.py",
            "signal_utils.py",
            "tests/test_signal_utils.py",
            "cmd_utils.py",
            "tests/test_cmd_utils.py",
            "this_utils.py",
            "tokenize_utils.py",
            "tests/test_this_utils.py",
            "tests/test_tokenize_utils.py",
            "socket_utils.py",
            "tests/test_socket_utils.py",
            "sysconfig_utils.py",
            "mimetypes_utils.py",
            "doctest_utils.py",
            "tests/test_doctest_utils.py",
            "code_utils.py",
            "tests/test_code_utils.py",
            "copyreg_utils.py",
            "tests/test_copyreg_utils.py",
            "fileinput_utils.py",
            "tests/test_fileinput_utils.py",
            "fnmatch_utils.py",
              "ftplib_utils.py",
            "tests/test_fnmatch_utils.py",
              "tests/test_ftplib_utils.py",
            "getpass_utils.py",
            "tests/test_getpass_utils.py",
            "id_utils.py",
            "tests/test_id_utils.py",
            "memoize_utils.py",
            "tests/test_memoize_utils.py",
            "pathlib_utils.py",
              "poplib_utils.py",
            "tests/test_pathlib_utils.py",
              "tests/test_poplib_utils.py",
            "webbrowser_utils.py",
            "tests/test_webbrowser_utils.py",
            "xmlrpc_utils.py",
            "tests/test_xmlrpc_utils.py",
            "syslog_utils.py",
            "faulthandler_utils.py",
            "tests/test_syslog_utils.py",
            "tests/test_faulthandler_utils.py",
            "resource_utils.py",
            "tests/test_resource_utils.py",
            "pwd_utils.py",
            "tests/test_pwd_utils.py",
            "grp_utils.py",
            "tests/test_grp_utils.py",
            "termios_utils.py",
            "tests/test_termios_utils.py",
            "fcntl_utils.py",
            "pty_utils.py",
            "stringprep_utils.py",
            "tabnanny_utils.py",
            "encodings_utils.py",
            "zipimport_utils.py",
            "ipaddress_utils.py",
            "pydoc_utils.py",
            "pydoc_data_utils.py",
            "wsgiref_utils.py",
            "antigravity_utils.py",
            "tests/test_fcntl_utils.py",
            "tests/test_pty_utils.py",
            "tests/test_stringprep_utils.py",
            "tests/test_tabnanny_utils.py",
            "tests/test_encodings_utils.py",
            "tests/test_zipimport_utils.py",
            "tests/test_ipaddress_utils.py",
            "tests/test_pydoc_utils.py",
            "tests/test_pydoc_data_utils.py",
            "tests/test_wsgiref_utils.py",
            "runpy_utils.py",
            "tests/test_runpy_utils.py",
            "secrets_utils.py",
            "tests/test_secrets_utils.py",
            "ssl_utils.py",
            "tests/test_ssl_utils.py",
            "tarfile_utils.py",
            "tests/test_tarfile_utils.py",
            "types_utils.py",
            "tests/test_types_utils.py",
            "pickletools_utils.py",
            "tests/test_pickletools_utils.py",
            "zoneinfo_utils.py",
            "opcode_utils.py",
            "tests/test_zoneinfo_utils.py",
            "tests/test_opcode_utils.py",
            "opcode_utils.py",
            "tests/test_opcode_utils.py",
            "tests/test_atexit_utils.py",
            "tests/test_colorsys_utils.py",
            "compression_utils.py",
            "tests/test_compression_utils.py",
            "csv_utils.py",
            "tests/test_csv_utils.py",
            "cmath_utils.py",
            "tests/test_cmath_utils.py",
            "ctypes_utils.py",
            "tests/test_ctypes_utils.py",
            "dataclasses_utils.py",
            "tests/test_dataclasses_utils.py",
            "functools_utils.py",
            "tests/test_functools_utils.py",
            "gc_utils.py",
            "tests/test_gc_utils.py",
            "greeting_utils.py",
            "tests/test_greeting_utils.py",
            "hashlib_utils.py",
            "tests/test_hashlib_utils.py",
            "tests/test_importlib_utils.py",
            "ip_utils.py",
            "tests/test_ip_utils.py",
            "itertools_utils.py",
            "tests/test_itertools_utils.py",
            "json_utils.py",
            "tests/test_json_utils.py",
            "tests/test_linecache_utils.py",
            "tests/test_multiprocessing_utils.py",
            "platform_utils.py",
            "tests/test_platform_utils.py",
            "regex_utils.py",
            "tests/test_regex_utils.py",
            "shutil_utils.py",
            "tests/test_shutil_utils.py",
            "zlib_utils.py",
            "tests/test_zlib_utils.py",
            "wsgiref_utils.py",
            "antigravity_utils.py",
            "tests/test_wsgiref_utils.py",
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
        self.assertEqual(partition_by([1, 1, 2, 2, 3], lambda x: x), [[1, 1], [2, 2], [3]])

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

    def test_pickle_utils_functions_work(self):
        """Generated pickle_utils.py should have working functions."""
        import io
        import pickle

        from pickle_utils import (
            dump,
            dumps,
            is_valid_protocol,
            load,
            loads,
            pickler,
            unpickler,
            validate_protocol,
        )

        self.assertEqual(loads(dumps({"a": [1, 2, 3]})), {"a": [1, 2, 3]})

        for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
            self.assertEqual(loads(dumps("hello", protocol=protocol)), "hello")

        buffer = io.BytesIO()
        dump({"x": 1}, buffer)
        buffer.seek(0)
        self.assertEqual(load(buffer), {"x": 1})

        buffer = io.BytesIO()
        p = pickler(buffer)
        p.dump([1, 2, 3])
        buffer.seek(0)
        self.assertEqual(unpickler(buffer).load(), [1, 2, 3])

        self.assertEqual(validate_protocol(None), pickle.HIGHEST_PROTOCOL)
        self.assertEqual(validate_protocol(2), 2)
        with self.assertRaises(TypeError):
            validate_protocol("2")
        with self.assertRaises(ValueError):
            validate_protocol(99)
        self.assertTrue(is_valid_protocol(0))
        self.assertFalse(is_valid_protocol("nope"))

    def test_sqlite3_utils_functions_work(self):
        """Generated sqlite3_utils.py should have working functions."""
        from sqlite3_utils import (
            connect,
            create_table,
            fetch_all,
            fetch_one,
            insert_row,
            query,
            table_exists,
        )

        conn = connect(":memory:")
        try:
            create_table(conn, "users", "id INTEGER PRIMARY KEY, name TEXT")
            insert_row(conn, "users", ["name"], ["Ada"])
            insert_row(conn, "users", ["name"], ["Bob"])

            self.assertTrue(table_exists(conn, "users"))
            self.assertFalse(table_exists(conn, "missing"))

            row_a = fetch_one(conn, "SELECT name FROM users WHERE name = ?", ["Ada"])
            self.assertEqual(row_a, ("Ada",))
            rows = fetch_all(conn, "SELECT name FROM users ORDER BY name")
            self.assertEqual(rows, [("Ada",), ("Bob",)])
            named = query(conn, "SELECT name FROM users")
            self.assertEqual(named, [{"name": "Ada"}, {"name": "Bob"}])

            row_id = insert_row(conn, "users", ["name"], ["Cec"])
            self.assertEqual(row_id, 3)
            self.assertEqual(len(fetch_all(conn, "SELECT name FROM users")), 3)
        finally:
            conn.close()

    def test_zipfile_utils_functions_work(self):
        """Generated zipfile_utils.py should have working functions."""
        import os
        import tempfile

        from zipfile_utils import create_archive, extract_all, is_zipfile, list_names

        tmpdir = tempfile.mkdtemp(prefix="scaffold-zipfile-")
        try:
            src = os.path.join(tmpdir, "a.txt")
            with open(src, "w", encoding="utf-8") as handle:
                handle.write("hello")
            archive = os.path.join(tmpdir, "out.zip")

            path = create_archive(archive, [src])
            self.assertEqual(path, archive)
            self.assertTrue(is_zipfile(archive))
            self.assertFalse(is_zipfile(os.path.join(tmpdir, "missing.zip")))

            names = list_names(archive)
            self.assertEqual(len(names), 1)
            self.assertTrue(names[0].endswith("a.txt"))

            dest = os.path.join(tmpdir, "extracted")
            os.mkdir(dest)
            extract_all(archive, dest)
            found = False
            for root, _, files in os.walk(dest):
                if files:
                    found = True
            self.assertTrue(found)

            with self.assertRaises(TypeError):
                create_archive(123, [src])  # type: ignore[arg-type]
            with self.assertRaises(ValueError):
                create_archive("", [src])
            with self.assertRaises(ValueError):
                create_archive(archive, [])
        finally:
            import shutil

            shutil.rmtree(tmpdir, ignore_errors=True)


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

    def test_bz2_utils_functions_work(self):
        """Generated bz2_utils.py should have working functions."""
        import os
        import tempfile

        from bz2_utils import (
            bz2_compress,
            bz2_decompress,
            bz2_open,
            bz2_read,
            bz2_write,
        )

        data = b"hello world" * 10
        compressed = bz2_compress(data)
        self.assertEqual(bz2_decompress(compressed), data)

        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "test.bz2")
            bz2_write(p, data)
            self.assertEqual(bz2_read(p), data)
            with bz2_open(p, "rb") as f:
                self.assertEqual(f.read(), data)
            with bz2_open(p, "wb", compresslevel=1) as f:
                f.write(data)

    def test_lzma_utils_functions_work(self):
        """Generated lzma_utils.py should have working functions."""
        import os
        import tempfile

        from lzma_utils import (
            lzma_compress,
            lzma_decompress,
            lzma_open,
            lzma_read,
            lzma_write,
        )

        data = b"hello world" * 10
        compressed = lzma_compress(data)
        self.assertEqual(lzma_decompress(compressed), data)

        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "test.xz")
            lzma_write(p, data)
            self.assertEqual(lzma_read(p), data)
            with lzma_open(p, "rb") as f:
                self.assertEqual(f.read(), data)
            with lzma_open(p, "wb") as f:
                f.write(data)

    def test_signal_utils_functions_work(self):
        """Generated signal_utils.py should have working functions."""
        import signal

        from signal_utils import (
            alarm,
            get_handler,
            get_signal_name,
            interrupt_handler,
            is_valid_signal,
            pause,
            register_int_handler,
            register_term_handler,
            set_handler,
            signal_info,
            signal_names,
            suspend_handler,
            unregister_handler,
        )

        self.assertTrue(is_valid_signal(signal.SIGINT))
        self.assertFalse(is_valid_signal("SIGINT"))
        self.assertFalse(is_valid_signal(999999))
        self.assertEqual(get_signal_name(signal.SIGINT), "SIGINT")
        self.assertIn("SIGINT", signal_names())

        handler = get_handler(signal.SIGINT)
        self.assertIn(handler, (signal.SIG_DFL, signal.SIG_IGN, signal.default_int_handler))

        original = signal.getsignal(signal.SIGUSR1 if hasattr(signal, "SIGUSR1") else signal.SIGINT)
        sig = signal.SIGUSR1 if hasattr(signal, "SIGUSR1") else signal.SIGINT
        original_int = signal.getsignal(signal.SIGINT)
        original_term = signal.getsignal(signal.SIGTERM)
        try:
            set_handler(sig, suspend_handler)
            self.assertIs(signal.getsignal(sig), suspend_handler)
            register_int_handler(suspend_handler)
            self.assertIs(signal.getsignal(signal.SIGINT), suspend_handler)
            register_term_handler(suspend_handler)
            self.assertIs(signal.getsignal(signal.SIGTERM), suspend_handler)
            unregister_handler(sig)
            self.assertIs(signal.getsignal(sig), signal.SIG_DFL)
        finally:
            signal.signal(sig, original)
            signal.signal(signal.SIGINT, original_int)
            signal.signal(signal.SIGTERM, original_term)

        with self.assertRaises(KeyboardInterrupt):
            interrupt_handler(signal.SIGINT, None)
        self.assertIsNone(suspend_handler(signal.SIGINT, None))
        self.assertEqual(alarm(0), 0)
        self.assertTrue(callable(pause))

        info = signal_info()
        self.assertIsInstance(info, dict)
        self.assertIn("names", info)
        self.assertIn("sigint_handler", info)
        self.assertIn("alarm_available", info)

    def test_gc_utils_functions_work(self):
        """Generated gc_utils.py should have working functions."""
        import gc

        import gc_utils

        was_enabled = gc.isenabled()
        try:
            gc_utils.disable()
            self.assertFalse(gc_utils.isenabled())
            gc_utils.enable()
            self.assertTrue(gc_utils.isenabled())
        finally:
            if was_enabled:
                gc.enable()
            else:
                gc.disable()

        self.assertIsInstance(gc_utils.collect(), int)
        self.assertIsInstance(gc_utils.get_count(), tuple)
        self.assertIsInstance(gc_utils.get_threshold(), tuple)
        self.assertIsInstance(gc_utils.get_stats(), list)
        self.assertIsInstance(gc_utils.get_objects(), list)
        a = []
        self.assertIsInstance(gc_utils.get_referents(a), list)
        self.assertIsInstance(gc_utils.get_referrers([a]), list)
        orig = gc_utils.get_debug()
        try:
            gc_utils.set_debug(0)
            self.assertEqual(gc_utils.get_debug(), 0)
        finally:
            gc_utils.set_debug(orig)
        orig_t = gc_utils.get_threshold()
        try:
            gc_utils.set_threshold(700, 10, 10)
            gc_utils.set_threshold(1000)
        finally:
            gc_utils.set_threshold(*orig_t)


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


class TestScaffoldHeredocs(unittest.TestCase):
    """scaffold.sh heredocs must be balanced and must not nest generators.

    A heredoc that is opened before its file body is written swallows every
    following section into the generated file, which silently corrupts the
    scaffolded project.
    """

    HEREDOC_OPEN = re.compile(r"^cat > \"\$OUTPUT_DIR/(.+)\" <<'([A-Za-z0-9_]+)'$")

    def setUp(self) -> None:
        self.lines = SCAFFOLD.read_text().splitlines()

    def _heredocs(self) -> list[tuple[int, str, int]]:
        """Return (line number, delimiter, end line) for every heredoc."""
        found = []
        index = 0
        while index < len(self.lines):
            match = self.HEREDOC_OPEN.match(self.lines[index])
            if not match:
                index += 1
                continue
            delimiter = match.group(2)
            end = index + 1
            while end < len(self.lines) and self.lines[end].strip() != delimiter:
                end += 1
            found.append((index + 1, delimiter, end))
            index = end + 1
        return found

    def test_every_heredoc_has_a_terminator(self) -> None:
        for line_number, delimiter, end in self._heredocs():
            self.assertLess(
                end,
                len(self.lines),
                msg=f"heredoc {delimiter!r} opened at line {line_number} has no terminator",
            )

    def test_heredocs_do_not_contain_nested_generators(self) -> None:
        for line_number, delimiter, end in self._heredocs():
            nested = [line for line in self.lines[line_number:end] if line.startswith("cat >")]
            if nested:
                self.fail(
                    f"heredoc {delimiter!r} opened at line {line_number} contains {nested[0]!r}"
                )

    def test_generated_files_are_not_empty(self) -> None:
        """Every generated Python file must contain actual content."""
        for line_number, delimiter, end in self._heredocs():
            opener = self.HEREDOC_OPEN.match(self.lines[line_number - 1])
            if opener is None:
                continue
            target = opener.group(1)
            if not target.endswith(".py"):
                continue
            body = [line for line in self.lines[line_number:end] if line.strip()]
            self.assertTrue(
                body,
                msg=f"{target} is generated as an empty file (heredoc {delimiter!r})",
            )


if __name__ == "__main__":
    unittest.main()
