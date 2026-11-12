"""Repo-wide enforcement of the doctest examples.

Every top-level module documents its helpers with doctest examples. Those
examples are the executable specification of the public API, but nothing ran
them, so a wrong expected value or an example that no longer parses could rot
silently. This suite runs the examples of every top-level module so such a
regression fails the build.

The examples are run with no option flags, so an expected value has to match
the real output exactly. A module that genuinely needs a wildcard opts in per
example with ``# doctest: +ELLIPSIS``. The environment is snapshotted and
restored around the run because a doctest may set an environment variable (for
example :func:`env_utils.ensure_env`) and the suite must not leak that state
into the tests that run after it.
"""

import doctest
import importlib
import io
import os
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent


def _iter_module_names():
    """Return the importable name of every top-level module in the repository.

    Modules whose names start with an underscore are private by convention and
    are excluded, matching the discovery of ``tests.test_public_api``.
    """
    return [
        path.stem
        for path in sorted(REPOSITORY_ROOT.glob("*.py"))
        if not path.name.startswith("_")
    ]


class TestDoctests(unittest.TestCase):
    """Every doctest example in every top-level module must pass."""

    modules: list[str]

    @classmethod
    def setUpClass(cls) -> None:
        cls.modules = _iter_module_names()

    def test_modules_are_discovered(self) -> None:
        self.assertGreater(len(self.modules), 0, "no top-level modules discovered")

    def test_every_doctest_example_passes(self) -> None:
        saved_env = os.environ.copy()
        failures: list[str] = []
        attempted = 0
        try:
            finder = doctest.DocTestFinder(recurse=True)
            for name in self.modules:
                try:
                    module = importlib.import_module(name)
                    tests = finder.find(module, name, globs=vars(module))
                except Exception as exc:  # pragma: no cover - defensive guard
                    failures.append(f"{name}: could not load doctests: {exc!r}")
                    continue
                for test in tests:
                    if not test.examples:
                        continue
                    attempted += 1
                    out = io.StringIO()
                    runner = doctest.DocTestRunner(optionflags=0, verbose=False)
                    runner.run(test, out=out.write)
                    if runner.failures:
                        failures.append(f"{test.name}:\n{out.getvalue().rstrip()}")
        finally:
            os.environ.clear()
            os.environ.update(saved_env)

        self.assertGreater(attempted, 0, "no doctest examples were executed")
        self.assertEqual(failures, [], "\n\n".join(failures))


if __name__ == "__main__":
    unittest.main()
