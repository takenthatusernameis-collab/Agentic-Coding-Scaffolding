"""Symbol table utilities (wrapping :mod:`symtable`).

The :mod:`symtable` module exposes the compiler's view of a program: the
nested scope structure of a module, function, or class, together with the
symbols each scope binds and how they are used. This wrapper offers a small,
validated surface over that information so callers can inspect scopes, resolve
symbols, and collect free variables or globals without handling the raw
standard library objects.
"""

from __future__ import annotations

import importlib.util
import symtable as _symtable
from pathlib import Path
from typing import Any, Callable, Dict, Iterator, List, Optional, Tuple

__all__ = [
    "COMPILE_TYPES",
    "assigned_names",
    "build_symbol_table",
    "child_scopes",
    "describe_scope",
    "find_scope",
    "free_variables",
    "global_names",
    "imported_names",
    "iter_scopes",
    "local_names",
    "lookup_symbol_table",
    "namespace_names",
    "nonlocal_names",
    "parameter_names",
    "referenced_names",
    "scope_identifiers",
    "scope_type",
    "symbol_flags",
    "symbol_info",
]

COMPILE_TYPES = ("exec", "eval", "single")

_SYMBOL_FLAGS = (
    "is_global",
    "is_local",
    "is_free",
    "is_nonlocal",
    "is_parameter",
    "is_imported",
    "is_assigned",
    "is_referenced",
    "is_namespace",
    "is_declared_global",
    "is_declared_nonlocal",
)


def _require_text(value: object, name: str) -> str:
    """Return *value* when it is a string, otherwise raise ``TypeError``."""
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a str, got {type(value).__name__}")
    return value


def _require_table(table: object) -> _symtable.SymbolTable:
    """Return *table* when it is a symbol table, otherwise raise ``TypeError``."""
    if not isinstance(table, _symtable.SymbolTable):
        raise TypeError(
            f"table must be a symtable.SymbolTable, got {type(table).__name__}"
        )
    return table


def _require_symbol(symbol: object) -> _symtable.Symbol:
    """Return *symbol* when it is a symbol, otherwise raise ``TypeError``."""
    if not isinstance(symbol, _symtable.Symbol):
        raise TypeError(
            f"symbol must be a symtable.Symbol, got {type(symbol).__name__}"
        )
    return symbol


def _collect(
    table: _symtable.SymbolTable, predicate: Callable[[_symtable.Symbol], bool]
) -> List[str]:
    """Return the names of the symbols in *table* matching *predicate*."""
    return [symbol.get_name() for symbol in table.get_symbols() if predicate(symbol)]


def build_symbol_table(
    code: str,
    filename: str = "<string>",
    compile_type: str = "exec",
) -> _symtable.SymbolTable:
    """Build the symbol table for a block of source code.

    Args:
        code: The Python source to analyse.
        filename: The name reported for the source in tracebacks and scopes.
        compile_type: One of ``"exec"``, ``"eval"``, or ``"single"``.

    Returns:
        The root :class:`symtable.SymbolTable` for the source.

    Raises:
        TypeError: If *code* or *filename* is not a string, or if
            *compile_type* is not a string.
        ValueError: If *compile_type* is not one of :data:`COMPILE_TYPES`.
        SyntaxError: If *code* cannot be parsed.

    Examples:
        >>> table = build_symbol_table("value = 1")
        >>> table.get_type()
        'module'
        >>> scope_identifiers(table)
        ['value']
    """
    source = _require_text(code, "code")
    source_name = _require_text(filename, "filename")
    mode = _require_text(compile_type, "compile_type")
    if mode not in COMPILE_TYPES:
        raise ValueError(
            f"compile_type must be one of {', '.join(COMPILE_TYPES)}, got {mode!r}"
        )
    return _symtable.symtable(source, source_name, mode)


def _module_source(name: str) -> str:
    """Return the path of the Python source file of the module *name*."""
    try:
        spec = importlib.util.find_spec(name)
    except (ImportError, ValueError) as exc:
        raise ImportError(f"cannot find the source of module {name!r}") from exc
    if spec is None or spec.origin is None:
        raise ImportError(f"cannot find the source of module {name!r}")
    origin = spec.origin
    if not origin.endswith(".py"):
        raise ImportError(f"module {name!r} has no Python source file")
    return origin


def lookup_symbol_table(
    name: str, filename: Optional[str] = None
) -> _symtable.SymbolTable:
    """Look up the symbol table of an importable module.

    The module is located with :func:`importlib.util.find_spec` and its
    source file is analysed without importing it.

    Args:
        name: The name of the module to inspect.
        filename: The path of the module source file, when it cannot be
            located automatically.

    Returns:
        The module's :class:`symtable.SymbolTable`.

    Raises:
        TypeError: If *name* or *filename* is not a string.
        ValueError: If *name* is empty.
        ImportError: If the module or its source file cannot be found.
        OSError: If the source file cannot be read.

    Examples:
        >>> table = lookup_symbol_table("json")
        >>> table.get_type()
        'module'
    """
    module_name = _require_text(name, "name")
    if not module_name:
        raise ValueError("name must not be empty")
    source_name = filename
    if source_name is None:
        source_name = _module_source(module_name)
    else:
        source_name = _require_text(filename, "filename")
    source = Path(source_name).read_text(encoding="utf-8")
    return build_symbol_table(source, source_name, "exec")


def scope_type(table: _symtable.SymbolTable) -> str:
    """Return the type of a scope.

    Args:
        table: The symbol table to inspect.

    Returns:
        One of ``"module"``, ``"function"``, ``"class"``, ``"annotation"``,
        or ``"comprehension"``.

    Raises:
        TypeError: If *table* is not a symbol table.
    """
    return _require_table(table).get_type()


def scope_identifiers(table: _symtable.SymbolTable) -> List[str]:
    """Return the names bound in a scope.

    Args:
        table: The symbol table to inspect.

    Returns:
        The identifiers of the scope, in source order.

    Raises:
        TypeError: If *table* is not a symbol table.
    """
    return list(_require_table(table).get_identifiers())


def child_scopes(table: _symtable.SymbolTable) -> List[_symtable.SymbolTable]:
    """Return the nested scopes of a scope.

    Args:
        table: The symbol table to inspect.

    Returns:
        The child symbol tables of *table*.

    Raises:
        TypeError: If *table* is not a symbol table.
    """
    return list(_require_table(table).get_children())


def iter_scopes(
    table: _symtable.SymbolTable,
) -> Iterator[Tuple[Tuple[str, ...], _symtable.SymbolTable]]:
    """Walk a scope tree depth first.

    Args:
        table: The root symbol table to walk.

    Yields:
        Tuples of ``(path, table)`` where *path* is the tuple of scope names
        leading to the yielded table.

    Raises:
        TypeError: If *table* is not a symbol table.

    Examples:
        >>> table = build_symbol_table("def outer():\\n    pass")
        >>> [path for path, _ in iter_scopes(table)]
        [(), ('outer',)]
    """
    root = _require_table(table)
    stack: List[Tuple[Tuple[str, ...], _symtable.SymbolTable]] = [((), root)]
    while stack:
        path, current = stack.pop()
        yield path, current
        for child in reversed(child_scopes(current)):
            stack.append((path + (child.get_name(),), child))


def find_scope(
    table: _symtable.SymbolTable, name: str
) -> Optional[_symtable.SymbolTable]:
    """Find a nested scope by name.

    Args:
        table: The root symbol table to search.
        name: The name of the scope to find.

    Returns:
        The matching symbol table, or ``None`` when no scope matches.

    Raises:
        TypeError: If *table* is not a symbol table or *name* is not a string.
    """
    root = _require_table(table)
    scope_name = _require_text(name, "name")
    for _, current in iter_scopes(root):
        if current.get_name() == scope_name:
            return current
    return None


def describe_scope(table: _symtable.SymbolTable) -> Dict[str, Any]:
    """Summarize a scope.

    Args:
        table: The symbol table to describe.

    Returns:
        A dictionary with the ``name``, ``type``, ``lineno``, ``id``,
        ``identifiers``, and ``children`` of the scope.

    Raises:
        TypeError: If *table* is not a symbol table.
    """
    scope = _require_table(table)
    return {
        "name": scope.get_name(),
        "type": scope.get_type(),
        "lineno": scope.get_lineno(),
        "id": scope.get_id(),
        "identifiers": scope_identifiers(scope),
        "children": [child.get_name() for child in child_scopes(scope)],
    }


def symbol_flags(symbol: _symtable.Symbol) -> Dict[str, bool]:
    """Return the usage flags of a symbol.

    Args:
        symbol: The symbol to inspect.

    Returns:
        A dictionary mapping each ``is_*`` predicate of the symbol to a
        boolean. Predicates that the running interpreter does not provide
        (such as ``is_declared_nonlocal`` before Python 3.13) report
        ``False``.

    Raises:
        TypeError: If *symbol* is not a symbol.
    """
    entry = _require_symbol(symbol)
    flags: Dict[str, bool] = {}
    for name in _SYMBOL_FLAGS:
        predicate = getattr(entry, name, None)
        flags[name] = bool(predicate()) if callable(predicate) else False
    return flags


def symbol_info(table: _symtable.SymbolTable, name: str) -> Dict[str, Any]:
    """Describe a symbol bound in a scope.

    Args:
        table: The symbol table holding the symbol.
        name: The name of the symbol.

    Returns:
        A dictionary with the symbol ``name`` and its usage flags.

    Raises:
        TypeError: If *table* is not a symbol table or *name* is not a string.
        KeyError: If the scope does not bind *name*.
    """
    scope = _require_table(table)
    symbol_name = _require_text(name, "name")
    symbol = scope.lookup(symbol_name)
    if symbol is None:
        raise KeyError(f"{symbol_name!r} is not defined in scope {scope.get_name()!r}")
    info: Dict[str, Any] = {"name": symbol.get_name()}
    info.update(symbol_flags(symbol))
    return info


def free_variables(table: _symtable.SymbolTable) -> List[str]:
    """Return the free variables of a scope.

    Args:
        table: The symbol table to inspect.

    Returns:
        The names of the symbols bound in an enclosing scope.

    Raises:
        TypeError: If *table* is not a symbol table.
    """
    return _collect(_require_table(table), lambda symbol: symbol.is_free())


def global_names(table: _symtable.SymbolTable) -> List[str]:
    """Return the global names of a scope.

    Args:
        table: The symbol table to inspect.

    Returns:
        The names of the symbols that are global in the scope.

    Raises:
        TypeError: If *table* is not a symbol table.
    """
    return _collect(_require_table(table), lambda symbol: symbol.is_global())


def local_names(table: _symtable.SymbolTable) -> List[str]:
    """Return the local names of a scope.

    Args:
        table: The symbol table to inspect.

    Returns:
        The names of the symbols that are local to the scope.

    Raises:
        TypeError: If *table* is not a symbol table.
    """
    return _collect(_require_table(table), lambda symbol: symbol.is_local())


def parameter_names(table: _symtable.SymbolTable) -> List[str]:
    """Return the parameter names of a scope.

    Args:
        table: The symbol table to inspect.

    Returns:
        The names of the symbols that are parameters of the scope.

    Raises:
        TypeError: If *table* is not a symbol table.
    """
    return _collect(_require_table(table), lambda symbol: symbol.is_parameter())


def imported_names(table: _symtable.SymbolTable) -> List[str]:
    """Return the imported names of a scope.

    Args:
        table: The symbol table to inspect.

    Returns:
        The names of the symbols bound by an import statement.

    Raises:
        TypeError: If *table* is not a symbol table.
    """
    return _collect(_require_table(table), lambda symbol: symbol.is_imported())


def assigned_names(table: _symtable.SymbolTable) -> List[str]:
    """Return the assigned names of a scope.

    Args:
        table: The symbol table to inspect.

    Returns:
        The names of the symbols that are assigned in the scope.

    Raises:
        TypeError: If *table* is not a symbol table.
    """
    return _collect(_require_table(table), lambda symbol: symbol.is_assigned())


def referenced_names(table: _symtable.SymbolTable) -> List[str]:
    """Return the referenced names of a scope.

    Args:
        table: The symbol table to inspect.

    Returns:
        The names of the symbols that are referenced in the scope.

    Raises:
        TypeError: If *table* is not a symbol table.
    """
    return _collect(_require_table(table), lambda symbol: symbol.is_referenced())


def nonlocal_names(table: _symtable.SymbolTable) -> List[str]:
    """Return the nonlocal names of a scope.

    Args:
        table: The symbol table to inspect.

    Returns:
        The names of the symbols declared ``nonlocal`` in the scope.

    Raises:
        TypeError: If *table* is not a symbol table.
    """
    return _collect(_require_table(table), lambda symbol: symbol.is_nonlocal())


def namespace_names(symbol: _symtable.Symbol) -> List[str]:
    """Return the names bound in the namespace a symbol introduces.

    A symbol that is the target of a class or function statement introduces
    a namespace; this function reports the identifiers bound inside that
    namespace.

    Args:
        symbol: The symbol to inspect.

    Returns:
        The identifiers of the namespace, or an empty list when the symbol
        is not bound to exactly one namespace.

    Raises:
        TypeError: If *symbol* is not a symbol.
    """
    entry = _require_symbol(symbol)
    try:
        namespace = entry.get_namespace()
    except ValueError:
        return []
    return list(namespace.get_identifiers())
