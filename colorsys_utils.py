"""Utilities for color system conversions (wrapping :mod:`colorsys`)."""

from __future__ import annotations

import colorsys
from typing import Tuple

RGB = Tuple[float, float, float]
HLS = Tuple[float, float, float]
HSV = Tuple[float, float, float]
YIQ = Tuple[float, float, float]


def rgb_to_hls(r: float, g: float, b: float) -> HLS:
    return colorsys.rgb_to_hls(r, g, b)


def hls_to_rgb(h: float, lightness: float, s: float) -> RGB:
    return colorsys.hls_to_rgb(h, lightness, s)


def rgb_to_hsv(r: float, g: float, b: float) -> HSV:
    return colorsys.rgb_to_hsv(r, g, b)


def hsv_to_rgb(h: float, s: float, v: float) -> RGB:
    return colorsys.hsv_to_rgb(h, s, v)


def rgb_to_yiq(r: float, g: float, b: float) -> YIQ:
    return colorsys.rgb_to_yiq(r, g, b)


def yiq_to_rgb(y: float, i: float, q: float) -> RGB:
    return colorsys.yiq_to_rgb(y, i, q)
