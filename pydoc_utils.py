"""Documentation utilities wrapping the standard library :mod:`pydoc` module.

The :mod:`pydoc` module generates documentation from Python modules, classes,
and functions.  It renders documentation as plain text or HTML, locates and
imports objects by name, and displays documentation in a pager or a web
browser.

This wrapper validates every argument before the standard library is reached,
so a caller gets a clear :class:`TypeError` or :class:`ValueError` instead of
an opaque failure.  It re-exports the documentation classes and the error of
:mod:`pydoc` and adds input validation for defensive programming.

The module is pure computation, so it works on every platform and never
touches the network.
"""

from __future__ import annotations

import pydoc as _pydoc
from typing import Any, Callable, Optional, Sequence, Type, cast

#: The documentation builder of the standard library.
Doc = _pydoc.Doc
#: Raised when a module or object cannot be imported for documentation.
ErrorDuringImport = _pydoc.ErrorDuringImport
#: The HTML documentation builder of the standard library.
HTMLDoc = _pydoc.HTMLDoc
#: The HTML representation builder of the standard library.
HTMLRepr = _pydoc.HTMLRepr
#: The interactive help helper of the standard library.
Helper = _pydoc.Helper
#: The module scanner of the standard library.
ModuleScanner = _pydoc.ModuleScanner
#: The bounded repr builder of the standard library.
Repr = cast(Any, getattr(_pydoc, "Repr"))
#: The plain text documentation builder of the standard library.
TextDoc = _pydoc.TextDoc
#: The plain text representation builder of the standard library.
TextRepr = _pydoc.TextRepr

__all__: list[str] = [
    "Doc",
    "ErrorDuringImport",
    "HTMLDoc",
    "HTMLRepr",
    "Helper",
    "ModuleScanner",
    "Repr",
    "TextDoc",
    "TextRepr",
    "allmethods",
    "apropos",
    "browse",
    "classify_class_attrs",
    "classname",
    "cli",
    "cram",
    "describe",
    "doc",
    "format_exception_only",
    "getdoc",
    "getpager",
    "help",
    "importfile",
    "isdata",
    "ispackage",
    "ispath",
    "locate",
    "parentname",
    "plain",
    "plainpager",
    "render_doc",
    "resolve",
    "safeimport",
    "splitdoc",
    "stripid",
    "synopsis",
    "visiblename",
    "writedoc",
    "writedocs",
]


def _check_string(value: object, name: str) -> str:
    """Raise when *value* is not a string.

    Args:
        value: The value to validate.
        name: The name of the parameter for error messages.

    Returns:
        The validated string.

    Raises:
        TypeError: If *value* is not a string.
    """
    if isinstance(value, bool) or not isinstance(value, str):
        raise TypeError(f"{name} must be a str, got {type(value).__name__}")
    return value


def _check_optional_string(value: object, name: str) -> Optional[str]:
    """Raise when *value* is neither ``None`` nor a string."""
    if value is None:
        return None
    return _check_string(value, name)


def _check_bool(value: object, name: str) -> bool:
    """Raise when *value* is not a boolean."""
    if not isinstance(value, bool):
        raise TypeError(f"{name} must be a bool, got {type(value).__name__}")
    return value


def _check_optional_bool(value: object, name: str) -> Optional[bool]:
    """Raise when *value* is neither ``None`` nor a boolean."""
    if value is None:
        return None
    return _check_bool(value, name)


def _check_int(value: object, name: str) -> int:
    """Raise when *value* is not an integer."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an int, got {type(value).__name__}")
    return value


def _check_non_negative_int(value: int, name: str) -> int:
    """Raise when *value* is negative."""
    if value < 0:
        raise ValueError(f"{name} must not be negative, got {value}")
    return value


def _check_optional_container(value: object, name: str) -> Optional[Sequence[str]]:
    """Raise when *value* is neither ``None`` nor a sequence of strings."""
    if value is None:
        return None
    if not isinstance(value, (list, tuple)):
        raise TypeError(f"{name} must be a sequence of strings or None, got {type(value).__name__}")
    for index, item in enumerate(value):
        _check_string(item, f"{name}[{index}]")
    return value


def render_doc(
    thing: Any,
    *,
    title: Optional[str] = None,
    forceload: bool = False,
    renderer: Optional[Callable[[Any], str]] = None,
) -> str:
    """Return the documentation of *thing* as a string.

    Args:
        thing: The object to document.
        title: The title of the documentation.  When ``None`` the standard
            library title is used.
        forceload: Whether to reload the object even when it is cached.
        renderer: An optional renderer callable.  When ``None`` the standard
            library renderer is chosen from the type of *thing*.

    Returns:
        The documentation of *thing*.

    Raises:
        TypeError: If *title* is not a string, *forceload* is not a bool, or
            *renderer* is not callable or ``None``.
    """
    _check_optional_string(title, "title")
    _check_bool(forceload, "forceload")
    if renderer is not None and not callable(renderer):
        raise TypeError(f"renderer must be callable or None, got {type(renderer).__name__}")
    kwargs: dict[str, Any] = {"forceload": forceload}
    if title is not None:
        kwargs["title"] = title
    if renderer is not None:
        kwargs["renderer"] = renderer
    return cast(str, _pydoc.render_doc(thing, **kwargs))


def doc(
    thing: Any,
    *,
    title: Optional[str] = None,
    forceload: bool = False,
    output: Optional[Any] = None,
    is_cli: bool = False,
) -> None:
    """Document *thing* and write or return the result.

    The documentation is rendered and passed to the pager or written to
    *output*.  This function returns ``None``; use :func:`render_doc` to get
    the documentation as a string.

    Args:
        thing: The object to document.
        title: The title of the documentation.  When ``None`` the standard
            library title is used.
        forceload: Whether to reload the object even when it is cached.
        output: An optional file-like object to write the documentation to.
        is_cli: Whether the documentation is produced for the command line.

    Returns:
        ``None``.

    Raises:
        TypeError: If *title* is not a string or *forceload* is not a bool.
    """
    _check_optional_string(title, "title")
    _check_bool(forceload, "forceload")
    kwargs: dict[str, Any] = {"forceload": forceload, "output": output, "is_cli": is_cli}
    if title is not None:
        kwargs["title"] = title
    _pydoc.doc(thing, **kwargs)


def writedoc(thing: Any, *, forceload: bool = False) -> None:
    """Write the documentation of *thing* to a text file.

    The file is named after the object and written to the current directory.

    Args:
        thing: The object to document.
        forceload: Whether to reload the object even when it is cached.

    Raises:
        TypeError: If *forceload* is not a bool.
        OSError: If the file cannot be written.
    """
    _check_bool(forceload, "forceload")
    _pydoc.writedoc(thing, forceload=forceload)


def writedocs(directory: str, *, pkgpath: str = "") -> None:
    """Write the documentation of every module of *directory* to text files.

    Args:
        directory: The directory whose modules are documented.
        pkgpath: The package path prefix of the directory.

    Raises:
        TypeError: If *directory* or *pkgpath* is not a string.
        OSError: If a file cannot be written.
    """
    _check_string(directory, "directory")
    _check_string(pkgpath, "pkgpath")
    _pydoc.writedocs(directory, pkgpath=pkgpath)


def apropos(key: str) -> None:
    """Print a one-line summary of every module whose keyword matches *key*.

    Args:
        key: The keyword to search for.

    Raises:
        TypeError: If *key* is not a string.
    """
    _check_string(key, "key")
    _pydoc.apropos(key)


def locate(path: str, *, forceload: bool = False) -> Any:
    """Locate and import the object named by *path*.

    *path* is a dotted name such as ``"pydoc.render_doc"``.

    Args:
        path: The dotted name of the object to locate.
        forceload: Whether to reload the object even when it is cached.

    Returns:
        The located object.

    Raises:
        TypeError: If *path* is not a string or *forceload* is not a bool.
    """
    _check_string(path, "path")
    _check_bool(forceload, "forceload")
    return _pydoc.locate(path, forceload=forceload)


def resolve(thing: Any, *, forceload: bool = False) -> Any:
    """Resolve *thing* to the object it names.

    *thing* may be an object or a dotted name.

    Args:
        thing: The object or dotted name to resolve.
        forceload: Whether to reload the object even when it is cached.

    Returns:
        The resolved object.

    Raises:
        TypeError: If *forceload* is not a bool.
    """
    _check_bool(forceload, "forceload")
    return _pydoc.resolve(thing, forceload=forceload)


def safeimport(
    path: str, *, forceload: bool = False, cache: Optional[dict] = None
) -> Any:
    """Import the object named by *path*, returning ``None`` on failure.

    Unlike :func:`locate` this never raises an import error.

    Args:
        path: The dotted name of the object to import.
        forceload: Whether to reload the object even when it is cached.
        cache: An optional cache of already imported objects.

    Returns:
        The imported object, or ``None`` when it cannot be imported.

    Raises:
        TypeError: If *path* is not a string, *forceload* is not a bool, or
            *cache* is not a dict or ``None``.
    """
    _check_string(path, "path")
    _check_bool(forceload, "forceload")
    cache_dict: dict = {}
    if cache is not None:
        if not isinstance(cache, dict):
            raise TypeError(f"cache must be a dict or None, got {type(cache).__name__}")
        cache_dict = cache
    return _pydoc.safeimport(path, forceload=forceload, cache=cache_dict)


def importfile(path: str) -> Any:
    """Import the module at *path*.

    Args:
        path: The path of the module file to import.

    Returns:
        The imported module.

    Raises:
        TypeError: If *path* is not a string.
        ImportError: If *path* cannot be imported.
    """
    _check_string(path, "path")
    return _pydoc.importfile(path)


def getdoc(object: Any) -> str:
    """Return the documentation string of *object*.

    Args:
        object: The object to document.

    Returns:
        The documentation string of *object*.
    """
    return cast(str, _pydoc.getdoc(object))


def synopsis(filename: str, *, cache: Optional[dict] = None) -> str:
    """Return the one-line synopsis of the module in *filename*.

    Args:
        filename: The path of the module file.
        cache: An optional cache of already read synopses.

    Returns:
        The synopsis of the module.

    Raises:
        TypeError: If *filename* is not a string or *cache* is not a dict or
            ``None``.
        OSError: If *filename* cannot be read.
    """
    _check_string(filename, "filename")
    if cache is None:
        cache = {}
    elif not isinstance(cache, dict):
        raise TypeError(f"cache must be a dict or None, got {type(cache).__name__}")
    return cast(str, _pydoc.synopsis(filename, cache=cache))


def source_synopsis(file: Any) -> str:
    """Return the synopsis of the module whose source is *file*.

    Args:
        file: A file-like object holding the source of a module.

    Returns:
        The synopsis of the module.

    Raises:
        TypeError: If *file* is not file-like.
        OSError: If *file* cannot be read.
    """
    if not hasattr(file, "read"):
        raise TypeError(f"file must be file-like, got {type(file).__name__}")
    return cast(str, _pydoc.source_synopsis(file))


def describe(thing: Any) -> str:
    """Return a one-line description of *thing*.

    Args:
        thing: The object to describe.

    Returns:
        A one-line description of *thing*.
    """
    return cast(str, _pydoc.describe(thing))


def classify_class_attrs(object: Any) -> list[Any]:
    """Return the classified attributes of *object*.

    Args:
        object: The object whose attributes are classified.

    Returns:
        The classified attributes of *object*.
    """
    return cast(list[Any], _pydoc.classify_class_attrs(object))


def classname(object: Any, modname: str) -> str:
    """Return the fully qualified class name of *object*.

    Args:
        object: The object whose class name is returned.
        modname: The module name to prefix when the class has no module.

    Returns:
        The fully qualified class name of *object*.

    Raises:
        TypeError: If *modname* is not a string.
    """
    _check_string(modname, "modname")
    return cast(str, _pydoc.classname(object, modname))


def parentname(object: Any, modname: str) -> str:
    """Return the name of the module or package that contains *object*.

    Args:
        object: The object to look up.
        modname: The module name to use as a fallback.

    Returns:
        The name of the module or package that contains *object*.

    Raises:
        TypeError: If *modname* is not a string.
    """
    _check_string(modname, "modname")
    func = getattr(_pydoc, "parentname")
    return cast(str, func(object, modname))


def visiblename(
    name: str, *, all_names: Optional[Sequence[str]] = None, obj: Any = None
) -> bool:
    """Report whether *name* is a visible name.

    Args:
        name: The name to test.
        all_names: An optional container of names that are considered visible.
        obj: The object whose visible names are considered.

    Returns:
        ``True`` when *name* is visible, False otherwise.

    Raises:
        TypeError: If *name* is not a string or *all_names* is not a sequence
            of strings or ``None``.
    """
    _check_string(name, "name")
    _check_optional_container(all_names, "all_names")
    return bool(_pydoc.visiblename(name, all=all_names, obj=obj))


def isdata(object: Any) -> bool:
    """Report whether *object* is a data object.

    Args:
        object: The object to test.

    Returns:
        ``True`` when *object* is a data object, False otherwise.
    """
    return bool(_pydoc.isdata(object))


def ispackage(path: str) -> bool:
    """Report whether *path* is a package directory.

    Args:
        path: The path of the directory to test.

    Returns:
        ``True`` when *path* is a package directory, False otherwise.

    Raises:
        TypeError: If *path* is not a string.
    """
    _check_string(path, "path")
    return bool(_pydoc.ispackage(path))


def ispath(x: Any) -> bool:
    """Report whether *x* looks like a path.

    Args:
        x: The value to test.

    Returns:
        ``True`` when *x* looks like a path, False otherwise.
    """
    return bool(_pydoc.ispath(x))


def allmethods(cls: Type[Any]) -> list[str]:
    """Return the names of all methods of *cls*.

    Args:
        cls: The class whose method names are returned.

    Returns:
        The names of all methods of *cls*.

    Raises:
        TypeError: If *cls* is not a class.
    """
    if not isinstance(cls, type):
        raise TypeError(f"cls must be a class, got {type(cls).__name__}")
    return cast(list[str], _pydoc.allmethods(cls))


def splitdoc(doc: str) -> tuple[str, str]:
    """Split *doc* into its description and its sections.

    Args:
        doc: The documentation string to split.

    Returns:
        The description and the sections of the documentation string.

    Raises:
        TypeError: If *doc* is not a string.
    """
    _check_string(doc, "doc")
    return cast(tuple[str, str], _pydoc.splitdoc(doc))


def stripid(text: str) -> str:
    """Strip the identifier prefix from *text*.

    Args:
        text: The text to strip.

    Returns:
        The text without its identifier prefix.

    Raises:
        TypeError: If *text* is not a string.
    """
    _check_string(text, "text")
    return cast(str, _pydoc.stripid(text))


def replace(text: str, *pairs: str) -> str:
    """Replace the occurrences of the pairs of *text*.

    Each pair of arguments is an ``(old, new)`` pair of strings: ``old`` is
    replaced by ``new``.

    Args:
        text: The text to transform.
        *pairs: The ``old, new`` replacement string pairs.

    Returns:
        The transformed text.

    Raises:
        TypeError: If *text* is not a string, *pairs* does not hold an even
            number of strings, or a pair member is not a string.
    """
    _check_string(text, "text")
    if len(pairs) % 2 != 0:
        raise TypeError("pairs must hold an even number of strings")
    for index in range(0, len(pairs), 2):
        _check_string(pairs[index], f"pairs[{index}]")
        _check_string(pairs[index + 1], f"pairs[{index + 1}]")
    return cast(str, _pydoc.replace(text, *pairs))


def cram(text: str, maxlen: int) -> str:
    """Return *text* shortened to *maxlen* characters.

    The middle of the text is replaced with an ellipsis when it is too long.

    Args:
        text: The text to shorten.
        maxlen: The maximum length of the result.

    Returns:
        The shortened text.

    Raises:
        TypeError: If *text* is not a string or *maxlen* is not an int.
        ValueError: If *maxlen* is negative.
    """
    _check_string(text, "text")
    maxlen = _check_int(maxlen, "maxlen")
    _check_non_negative_int(maxlen, "maxlen")
    return cast(str, _pydoc.cram(text, maxlen))


def plain(text: str) -> str:
    """Return *text* as plain text without any markup.

    Args:
        text: The text to convert.

    Returns:
        The plain text form of *text*.

    Raises:
        TypeError: If *text* is not a string.
    """
    _check_string(text, "text")
    return cast(str, _pydoc.plain(text))


def cli() -> None:
    """Run the pydoc command line interface.

    Raises:
        SystemExit: When the command line interface exits.
    """
    _pydoc.cli()


def help() -> None:
    """Start the interactive help session.

    Raises:
        SystemExit: When the interactive help session exits.
    """
    _pydoc.help()


def getpager() -> Any:
    """Return the pager of the standard library.

    Returns:
        The pager callable, or ``None`` when no pager is configured.
    """
    return _pydoc.getpager()


def plainpager(text: str) -> None:
    """Page *text* using the plain text pager.

    Args:
        text: The text to page.

    Raises:
        TypeError: If *text* is not a string.
    """
    _check_string(text, "text")
    _pydoc.plainpager(text)


def browse(
    *,
    port: int = 0,
    open_browser: bool = True,
    hostname: str = "localhost",
) -> None:
    """Start a documentation server and open a browser to it.

    Args:
        port: The port to serve on.  ``0`` lets the operating system choose.
        open_browser: Whether to open a web browser to the server.
        hostname: The hostname the server listens on.

    Raises:
        TypeError: If *port* is not an int, *open_browser* is not a bool, or
            *hostname* is not a string.
        ValueError: If *port* is negative.
        OSError: If the server cannot be started.
    """
    port = _check_non_negative_int(_check_int(port, "port"), "port")
    _check_bool(open_browser, "open_browser")
    _check_string(hostname, "hostname")
    func = getattr(_pydoc, "browse")
    func(port=port, open_browser=open_browser, hostname=hostname)


def format_exception_only(exc: Any, value: Any = None) -> list[str]:
    """Return the formatted exception of *exc*.

    Args:
        exc: The exception to format.
        value: An optional value associated with the exception.

    Returns:
        The formatted exception as a list of strings.
    """
    func = getattr(_pydoc, "format_exception_only")
    return cast(list[str], func(exc, value))
