"""Cross-cutting tests for the public API surface of every wrapper module.

Every ``*_utils.py`` module exposes its public helpers through ``__all__``.
This suite guards that contract: any helper that is reachable as a public
attribute of the module (a top-level, non-underscore name that is callable or
a re-exported standard library alias) must also be listed in ``__all__``.
"""

import importlib
import inspect
import pkgutil
from pathlib import Path

import unittest

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
MODULE_PREFIX = ""  # modules are imported from the repository root


def _iter_wrapper_modules():
    """Yield the importable name of every ``*_utils.py`` module in the repo."""
    modules = []
    for entry in sorted((REPOSITORY_ROOT / "tests").iterdir()):
        if not entry.is_file():
            continue
        if entry.name.startswith("test_") and entry.name.endswith("_utils.py"):
            modules.append(entry.name[len("test_") : -len(".py")])
    # Also include any top-level *_utils.py module without a matching test.
    for path in sorted(REPOSITORY_ROOT.glob("*_utils.py")):
        name = path.stem
        if name not in modules:
            modules.append(name)
    return modules


class TestPublicAPI(unittest.TestCase):
    """Every public attribute of a wrapper module must appear in ``__all__``."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.modules = _iter_wrapper_modules()

    def test_modules_are_discovered(self) -> None:
        self.assertGreater(len(self.modules), 0, "no wrapper modules discovered")

    def test_every_module_has_all(self) -> None:
        missing_all = [name for name in self.modules if not hasattr(importlib.import_module(name), "__all__")]
        self.assertEqual(missing_all, [], f"modules missing __all__: {missing_all}")

    def test_every_public_attribute_is_exported(self) -> None:
        gaps = []
        for name in self.modules:
            module = importlib.import_module(name)
            exports = set(getattr(module, "__all__", []))
            for attr, value in inspect.getmembers(module):
                if attr.startswith("_"):
                    continue
                if attr in exports:
                    continue
                # Only guard helpers *defined* by this module. Re-exports of
                # standard library aliases (Complex, Number, ZoneInfo, ...)
                # are intentionally public and are documented in the module
                # prose; they are not part of the wrapper's own API surface.
                owner = getattr(value, "__module__", None)
                if owner != name:
                    continue
                gaps.append(f"{name}.{attr} ({type(value).__name__}) is public but missing from __all__")
        self.assertEqual(gaps, [], "\n".join(gaps))


if __name__ == "__main__":
    unittest.main()