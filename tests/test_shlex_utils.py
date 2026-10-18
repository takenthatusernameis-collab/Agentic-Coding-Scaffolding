"""Utilities for simple lexical analysis (wrapping :mod:`shlex`)."""

import shlex as _shlex


def split(s, comments=False, posix=True):
    if not isinstance(s, str):
        raise TypeError("s must be a str")
    return _shlex.split(s, comments=comments, posix=posix)


def quote(s):
    if not isinstance(s, str):
        raise TypeError("s must be a str")
    return _shlex.quote(s)


def join(split_command):
    return _shlex.join(split_command)
""" filePath="/home/runner/work/Agentic-Coding-Scaffolding/Agentic-Coding-Scaffolding/shlex_utils.py">
<|assistant to=bash<|channel|>analysis <|constrain|>xml<|message|><rfl:parameter name="command">
cd /home/runner/work/Agentic-Coding-Scaffolding/Agentic-Coding-Scaffolding && PYTHONPATH=. python -c "import shlex_utils; print(shlex_utils.split('a b')); print(shlex_utils.quote('a b')); print(shlex_utils.join(['echo','hi there']))"