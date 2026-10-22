"""Utilities for CGI traceback reporting (wrapping :mod:`cgitb`)."""

import cgitb as _cgitb


def enable(display=1, logdir=None, context=5, format="html"):
    """Enable CGI traceback reporting (wrapping ``cgitb.enable``)."""
    return _cgitb.enable(display=display, logdir=logdir, context=context, format=format)


def handler(info=None):
    """Handle an exception (wrapping ``cgitb.handler``)."""
    return _cgitb.handler(info=info)


def html(info=None, context=5):
    """Return an HTML traceback (wrapping ``cgitb.html``)."""
    return _cgitb.html(info, context)


def text(info=None, context=5):
    """Return a text traceback (wrapping ``cgitb.text``)."""
    return _cgitb.text(info, context)


def reset():
    """Reset the handler (wrapping ``cgitb.reset``)."""
    return _cgitb.reset()


def hook_class():
    """Return the ``Hook`` class."""
    return _cgitb.Hook
