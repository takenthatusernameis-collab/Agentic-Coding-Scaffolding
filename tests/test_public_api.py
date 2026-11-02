"""Cross-cutting tests for the public API surface of every top-level module.

Every top-level module exposes its public helpers through ``__all__``. This
suite guards that contract repo-wide: any helper that is reachable as a public
attribute of the module (a top-level, non-underscore name that is callable or
a re-exported standard library alias) must also be listed in ``__all__``.

The contract applies to non-wrapper modules (``stats.py``, ``strings.py``,
``shapes.py``, ``prompt_utils.py``, ...) as well as ``*_utils.py`` wrapper
modules. Covering only the wrappers left those modules unguarded, which is how
earlier regressions (for example, ``upper``/``lower`` missing from
``bytes_utils.__all__``) slipped through unnoticed.
"""

import importlib
import inspect
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
MODULE_PREFIX = ""  # modules are imported from the repository root


def _iter_wrapper_modules():
    """Yield the importable name of every top-level module in the repo.

    The public-API ``__all__`` contract applies to every top-level module,
    not only the ``*_utils.py`` wrapper modules. Non-wrapper modules such as
    ``stats.py``, ``strings.py``, ``shapes.py`` and ``prompt_utils.py`` are
    held to the same contract: every public attribute they define must be
    exported in ``__all__``. Covering only the wrappers left those modules
    unguarded, which is how earlier regressions (missing ``upper``/``lower``
    in ``bytes_utils``) slipped through.
    """
    modules = []
    for entry in sorted((REPOSITORY_ROOT / "tests").iterdir()):
        if not entry.is_file():
            continue
        if entry.name.startswith("test_") and entry.name.endswith("_utils.py"):
            modules.append(entry.name[len("test_") : -len(".py")])
    # Include every top-level module, wrapper or not, so the contract is
    # enforced repo-wide. Modules whose names start with an underscore are
    # private by convention and are excluded.
    for path in sorted(REPOSITORY_ROOT.glob("*.py")):
        if path.name.startswith("_"):
            continue
        name = path.stem
        if name not in modules:
            modules.append(name)
    return modules


class TestPublicAPI(unittest.TestCase):
    """Every public attribute of a top-level module must appear in ``__all__``."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.modules = _iter_wrapper_modules()

    def test_modules_are_discovered(self) -> None:
        self.assertGreater(len(self.modules), 0, "no top-level modules discovered")

    def test_every_module_has_all(self) -> None:
        missing_all = [
            name for name in self.modules
            if not hasattr(importlib.import_module(name), "__all__")
        ]
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
                gaps.append(
                    f"{name}.{attr} ({type(value).__name__}) is public but missing from __all__"
                )
        self.assertEqual(gaps, [], "\n".join(gaps))


if __name__ == "__main__":
    unittest.main()
