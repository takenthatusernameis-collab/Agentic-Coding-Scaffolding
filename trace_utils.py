"""Trace utility functions wrapping the standard library trace module."""

from __future__ import annotations

import trace
from typing import Any

__all__: list[str] = [
    "Trace",
    "CoverageResults",
]

Trace = trace.Trace
CoverageResults = trace.CoverageResults
""" filePath">
/home/runner/work/Agentic-Coding-Scaffolding/Agentic-Coding-Scaffolding/trace_utils.py