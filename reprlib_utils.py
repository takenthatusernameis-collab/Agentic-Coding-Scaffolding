"""Utilities for reprlib (wrapping :mod:`reprlib`)."""

import reprlib as _reprlib


def repr(obj):
    return _reprlib.repr(obj)


def get_ident():
    return _reprlib.get_ident()


class Repr(_reprlib.Repr):
    def __init__(
        self,
        *,
        maxlevel=6,
        maxtuple=6,
        maxlist=6,
        maxarray=5,
        maxdict=4,
        maxset=6,
        maxfrozenset=6,
        maxdeque=6,
        maxstring=30,
        maxlong=40,
        maxother=30,
        fillvalue="...",
        indent=None,
    ):
        if (
            maxlevel is not None
            and not isinstance(maxlevel, int)
            or (isinstance(maxlevel, int) and maxlevel < 0)
        ):
            raise TypeError("maxlevel must be a non-negative int or None")
        if not isinstance(maxtuple, int) or maxtuple < 0:
            raise TypeError("maxtuple must be a non-negative int")
        if not isinstance(maxlist, int) or maxlist < 0:
            raise TypeError("maxlist must be a non-negative int")
        if not isinstance(maxarray, int) or maxarray < 0:
            raise TypeError("maxarray must be a non-negative int")
        if not isinstance(maxdict, int) or maxdict < 0:
            raise TypeError("maxdict must be a non-negative int")
        if not isinstance(maxset, int) or maxset < 0:
            raise TypeError("maxset must be a non-negative int")
        if not isinstance(maxfrozenset, int) or maxfrozenset < 0:
            raise TypeError("maxfrozenset must be a non-negative int")
        if not isinstance(maxdeque, int) or maxdeque < 0:
            raise TypeError("maxdeque must be a non-negative int")
        if not isinstance(maxstring, int) or maxstring < 0:
            raise TypeError("maxstring must be a non-negative int")
        if not isinstance(maxlong, int) or maxlong < 0:
            raise TypeError("maxlong must be a non-negative int")
        if not isinstance(maxother, int) or maxother < 0:
            raise TypeError("maxother must be a non-negative int")
        if not isinstance(fillvalue, str):
            raise TypeError("fillvalue must be a string")
        if indent is not None and not isinstance(indent, (int, str)):
            raise TypeError("indent must be int, str, or None")
        if isinstance(indent, int) and indent < 0:
            raise ValueError("indent must be non-negative")
        super().__init__(
            maxlevel=maxlevel,
            maxtuple=maxtuple,
            maxlist=maxlist,
            maxarray=maxarray,
            maxdict=maxdict,
            maxset=maxset,
            maxfrozenset=maxfrozenset,
            maxdeque=maxdeque,
            maxstring=maxstring,
            maxlong=maxlong,
            maxother=maxother,
            fillvalue=fillvalue,
            indent=indent,
        )


aRepr = _reprlib.aRepr


def recursive_repr(fillvalue="..."):
    if not isinstance(fillvalue, str):
        raise TypeError("fillvalue must be a string")
    return _reprlib.recursive_repr(fillvalue=fillvalue)
