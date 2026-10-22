"""Tests for pipes_utils module."""

import os
import tempfile
import unittest
from unittest import mock

import pipes_utils


class TestIsAvailable(unittest.TestCase):
    def test_is_available_reports_true_when_module_is_shipped(self):
        self.assertTrue(pipes_utils.is_available())

    def test_is_available_reports_false_when_module_is_missing(self):
        with mock.patch.object(pipes_utils, "_pipes", None):
            self.assertFalse(pipes_utils.is_available())


class TestCreateTemplate(unittest.TestCase):
    def test_create_template_returns_template(self):
        template = pipes_utils.create_template()
        self.assertIsInstance(template, pipes_utils.Template)

    def test_create_template_has_no_steps(self):
        template = pipes_utils.create_template()
        self.assertEqual(template.steps, [])

    def test_create_template_raises_when_module_is_missing(self):
        with mock.patch.object(pipes_utils, "_pipes", None):
            with self.assertRaises(RuntimeError):
                pipes_utils.create_template()


class TestResetTemplate(unittest.TestCase):
    def test_reset_template_clears_steps(self):
        template = pipes_utils.create_template()
        pipes_utils.append_step(template, "cat", "-f")
        pipes_utils.reset_template(template)
        self.assertEqual(template.steps, [])

    def test_reset_template_rejects_bad_template(self):
        with self.assertRaises(TypeError):
            pipes_utils.reset_template("not a template")  # type: ignore[arg-type]

    def test_reset_template_raises_when_module_is_missing(self):
        with mock.patch.object(pipes_utils, "_pipes", None):
            with self.assertRaises(RuntimeError):
                pipes_utils.reset_template(pipes_utils.create_template())


class TestCloneTemplate(unittest.TestCase):
    def test_clone_template_copies_steps(self):
        template = pipes_utils.create_template()
        pipes_utils.append_step(template, "cat", "-f")
        clone = pipes_utils.clone_template(template)
        self.assertEqual(clone.steps, template.steps)
        self.assertIsNot(clone, template)

    def test_clone_template_rejects_bad_template(self):
        with self.assertRaises(TypeError):
            pipes_utils.clone_template("not a template")  # type: ignore[arg-type]

    def test_clone_template_raises_when_module_is_missing(self):
        with mock.patch.object(pipes_utils, "_pipes", None):
            with self.assertRaises(RuntimeError):
                pipes_utils.clone_template(pipes_utils.create_template())


class TestSetDebug(unittest.TestCase):
    def test_set_debug_turns_debugging_on_and_off(self):
        template = pipes_utils.create_template()
        pipes_utils.set_debug(template, True)
        self.assertEqual(template.debugging, 1)
        pipes_utils.set_debug(template, False)
        self.assertEqual(template.debugging, 0)

    def test_set_debug_rejects_bad_template(self):
        with self.assertRaises(TypeError):
            pipes_utils.set_debug("not a template", True)  # type: ignore[arg-type]

    def test_set_debug_rejects_non_bool_flag(self):
        template = pipes_utils.create_template()
        with self.assertRaises(TypeError):
            pipes_utils.set_debug(template, 1)  # type: ignore[arg-type]

    def test_update_debug_is_an_alias(self):
        self.assertIs(pipes_utils.update_debug, pipes_utils.set_debug)


class TestAppendStep(unittest.TestCase):
    def test_append_step_adds_step_at_end(self):
        template = pipes_utils.create_template()
        pipes_utils.append_step(template, "cat $IN > $OUT", "-f")
        self.assertEqual(template.steps, [("cat $IN > $OUT", "-f")])

    def test_append_step_validates_cmd_and_kind(self):
        template = pipes_utils.create_template()
        with self.assertRaises(TypeError):
            pipes_utils.append_step(template, 5, "-f")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            pipes_utils.append_step(template, "cat $IN", 5)  # type: ignore[arg-type]

    def test_append_step_rejects_unknown_kind(self):
        template = pipes_utils.create_template()
        with self.assertRaises(ValueError):
            pipes_utils.append_step(template, "cat $IN", "xx")

    def test_append_step_rejects_source(self):
        template = pipes_utils.create_template()
        with self.assertRaises(ValueError):
            pipes_utils.append_step(template, "cat", ".")

    def test_append_step_rejects_after_sink(self):
        template = pipes_utils.create_template()
        pipes_utils.append_step(template, "cat", "-.")
        with self.assertRaises(ValueError):
            pipes_utils.append_step(template, "cat", "-f")

    def test_append_step_requires_dollar_in_for_file_input(self):
        template = pipes_utils.create_template()
        with self.assertRaises(ValueError):
            pipes_utils.append_step(template, "cat", "ff")

    def test_append_step_requires_dollar_out_for_file_output(self):
        template = pipes_utils.create_template()
        with self.assertRaises(ValueError):
            pipes_utils.append_step(template, "cat $IN", "ff")

    def test_append_step_raises_when_module_is_missing(self):
        with mock.patch.object(pipes_utils, "_pipes", None):
            with self.assertRaises(RuntimeError):
                pipes_utils.append_step(pipes_utils.create_template(), "cat", "-f")


class TestPrependStep(unittest.TestCase):
    def test_prepend_step_adds_step_at_front(self):
        template = pipes_utils.create_template()
        pipes_utils.append_step(template, "cat $IN", "-f")
        pipes_utils.prepend_step(template, "head", "-f")
        self.assertEqual(template.steps[0], ("head", "-f"))

    def test_prepend_step_validates_cmd_and_kind(self):
        template = pipes_utils.create_template()
        with self.assertRaises(TypeError):
            pipes_utils.prepend_step(template, 5, "-f")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            pipes_utils.prepend_step(template, "cat $IN", 5)  # type: ignore[arg-type]

    def test_prepend_step_rejects_unknown_kind(self):
        template = pipes_utils.create_template()
        with self.assertRaises(ValueError):
            pipes_utils.prepend_step(template, "cat $IN", "xx")

    def test_prepend_step_rejects_sink(self):
        template = pipes_utils.create_template()
        with self.assertRaises(ValueError):
            pipes_utils.prepend_step(template, "cat", "-.")

    def test_prepend_step_rejects_after_source(self):
        template = pipes_utils.create_template()
        pipes_utils.prepend_step(template, "cat", ".-")
        with self.assertRaises(ValueError):
            pipes_utils.prepend_step(template, "cat", "-f")

    def test_prepend_step_raises_when_module_is_missing(self):
        with mock.patch.object(pipes_utils, "_pipes", None):
            with self.assertRaises(RuntimeError):
                pipes_utils.prepend_step(pipes_utils.create_template(), "cat", "-f")


class TestOpenTemplate(unittest.TestCase):
    def test_open_reading_with_no_steps_uses_builtin_open(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "notes.txt")
            with open(path, "w") as handle:
                handle.write("hello\n")
            template = pipes_utils.create_template()
            with pipes_utils.open_for_reading(template, path) as handle:
                self.assertEqual(handle.read(), "hello\n")

    def test_open_writing_with_no_steps_uses_builtin_open(self):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "notes.txt")
            template = pipes_utils.create_template()
            with pipes_utils.open_for_writing(template, path) as handle:
                handle.write("hello\n")
            with open(path) as handle:
                self.assertEqual(handle.read(), "hello\n")

    def test_open_rejects_bad_mode(self):
        template = pipes_utils.create_template()
        with self.assertRaises(ValueError):
            pipes_utils.open_template(template, "/tmp/x", "x")  # type: ignore[arg-type]

    def test_open_rejects_bad_template(self):
        with self.assertRaises(TypeError):
            pipes_utils.open_template("not a template", "/tmp/x", "r")  # type: ignore[arg-type]

    def test_open_raises_when_module_is_missing(self):
        with mock.patch.object(pipes_utils, "_pipes", None):
            with self.assertRaises(RuntimeError):
                pipes_utils.open_for_reading(pipes_utils.create_template(), "/tmp/x")


class TestCopyFile(unittest.TestCase):
    def test_copy_file_returns_exit_status(self):
        with tempfile.TemporaryDirectory() as directory:
            infile = os.path.join(directory, "in.txt")
            outfile = os.path.join(directory, "out.txt")
            with open(infile, "w") as handle:
                handle.write("data\n")
            template = pipes_utils.create_template()
            with mock.patch.object(pipes_utils._pipes_module().__class__, "copy", return_value=0):
                status = pipes_utils.copy_file(template, infile, outfile)
            self.assertEqual(status, 0)

    def test_copy_file_rejects_bad_template(self):
        with self.assertRaises(TypeError):
            pipes_utils.copy_file("not a template", "/tmp/in", "/tmp/out")  # type: ignore[arg-type]

    def test_copy_file_raises_when_module_is_missing(self):
        with mock.patch.object(pipes_utils, "_pipes", None):
            with self.assertRaises(RuntimeError):
                pipes_utils.copy_file(pipes_utils.create_template(), "/tmp/in", "/tmp/out")


class TestBuildPipeline(unittest.TestCase):
    def test_build_pipeline_returns_command_string(self):
        template = pipes_utils.create_template()
        pipes_utils.append_step(template, "cat $IN", "-f")
        command = pipes_utils.build_pipeline(template, "/tmp/in.txt", "/tmp/out.txt")
        self.assertIsInstance(command, str)
        self.assertIn("cat", command)

    def test_build_pipeline_rejects_bad_template(self):
        with self.assertRaises(TypeError):
            pipes_utils.build_pipeline("not a template", "/tmp/in", "/tmp/out")  # type: ignore[arg-type]

    def test_build_pipeline_raises_when_module_is_missing(self):
        with mock.patch.object(pipes_utils, "_pipes", None):
            with self.assertRaises(RuntimeError):
                pipes_utils.build_pipeline(
                    pipes_utils.create_template(), "/tmp/in", "/tmp/out"
                )


class TestQuoteCommand(unittest.TestCase):
    def test_quote_command_quotes_spaces(self):
        self.assertEqual(pipes_utils.quote_command("a b"), "'a b'")

    def test_quote_command_rejects_non_string(self):
        with self.assertRaises(TypeError):
            pipes_utils.quote_command(5)  # type: ignore[arg-type]

    def test_quote_command_raises_when_module_is_missing(self):
        with mock.patch.object(pipes_utils, "_pipes", None):
            with self.assertRaises(RuntimeError):
                pipes_utils.quote_command("a b")


class TestStepKindConstants(unittest.TestCase):
    def test_step_kind_constants_are_distinct(self):
        self.assertEqual(pipes_utils.FILEIN_FILEOUT, "ff")
        self.assertEqual(pipes_utils.STDIN_FILEOUT, "-f")
        self.assertEqual(pipes_utils.FILEIN_STDOUT, "f-")
        self.assertEqual(pipes_utils.STDIN_STDOUT, "--")
        self.assertEqual(pipes_utils.SOURCE, ".-")
        self.assertEqual(pipes_utils.SINK, "-.")
        self.assertEqual(len(set(pipes_utils.STEP_KINDS)), 6)


if __name__ == "__main__":
    unittest.main()
