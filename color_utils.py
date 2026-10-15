"""Color manipulation utilities.

This module provides functions for converting between color representations
(hexadecimal, RGB, HSL), computing WCAG relative luminance and contrast ratios,
checking accessibility, and adjusting/blending colors.

Colors are accepted either as a hexadecimal string (``"#RRGGBB"`` or
``"RRGGBB"``) or as an RGB tuple ``(r, g, b)`` with integer channels in the
range ``0``-``255``.
"""

from typing import List, Tuple, Union

__all__: List[str] = [
    "validate_hex",
    "hex_to_rgb",
    "rgb_to_hex",
    "rgb_to_hsl",
    "hsl_to_rgb",
    "get_luminance",
    "get_contrast_ratio",
    "is_accessible",
    "adjust_brightness",
    "blend_colors",
]

_RGB = Tuple[int, int, int]
_Color = Union[str, _RGB]

_HEX_DIGITS = set("0123456789abcdefABCDEF")

_ACCESSIBILITY_THRESHOLDS = {
    ("AA", "normal"): 4.5,
    ("AA", "large"): 3.0,
    ("AAA", "normal"): 7.0,
    ("AAA", "large"): 4.5,
}


def _require_string(value: str, name: str) -> str:
    """Validate that ``value`` is a string, raising ``TypeError`` otherwise."""
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string")
    return value


def _require_int_range(value: int, name: str, minimum: int = 0, maximum: int = 255) -> int:
    """Validate that ``value`` is an int within ``[minimum, maximum]``."""
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an integer")
    if value < minimum or value > maximum:
        raise ValueError(f"{name} must be between {minimum} and {maximum}")
    return value


def _parse_color(color: _Color, name: str = "color") -> _RGB:
    """Normalize a hex string or RGB tuple to an ``(r, g, b)`` tuple."""
    if isinstance(color, str):
        return hex_to_rgb(color)
    if (
        isinstance(color, tuple)
        and len(color) == 3
        and all(isinstance(channel, int) and not isinstance(channel, bool) for channel in color)
    ):
        r, g, b = color
        return (
            _require_int_range(r, f"{name}[0]"),
            _require_int_range(g, f"{name}[1]"),
            _require_int_range(b, f"{name}[2]"),
        )
    raise TypeError(f"{name} must be a hex string or an (r, g, b) tuple of ints")


def validate_hex(hex_color: str) -> bool:
    """Return ``True`` if ``hex_color`` is a valid ``#RRGGBB`` or ``RRGGBB`` string.

    Args:
        hex_color: The hexadecimal color string to validate.

    Returns:
        ``True`` for a valid 6-digit hex color, ``False`` otherwise.

    Raises:
        TypeError: If ``hex_color`` is not a string.

    Examples:
        >>> validate_hex("#ff5733")
        True
        >>> validate_hex("ff5733")
        True
        >>> validate_hex("#gg5733")
        False
        >>> validate_hex("#ff57")
        False
    """
    _require_string(hex_color, "hex_color")
    value = hex_color.lstrip("#")
    if len(value) != 6:
        return False
    return all(ch in _HEX_DIGITS for ch in value)


def hex_to_rgb(hex_color: str) -> _RGB:
    """Convert a hexadecimal color string to an ``(r, g, b)`` tuple.

    Args:
        hex_color: A ``#RRGGBB`` or ``RRGGBB`` color string.

    Returns:
        A tuple of three integers ``(r, g, b)`` in the range ``0``-``255``.

    Raises:
        TypeError: If ``hex_color`` is not a string.
        ValueError: If ``hex_color`` is not a valid 6-digit hex color.

    Examples:
        >>> hex_to_rgb("#ff5733")
        (255, 87, 51)
        >>> hex_to_rgb("000000")
        (0, 0, 0)
        >>> hex_to_rgb("#FFFFFF")
        (255, 255, 255)
    """
    _require_string(hex_color, "hex_color")
    if not validate_hex(hex_color):
        raise ValueError(f"Invalid hex color: {hex_color!r}")
    value = hex_color.lstrip("#")
    return (
        int(value[0:2], 16),
        int(value[2:4], 16),
        int(value[4:6], 16),
    )


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Convert RGB channel values to a ``#RRGGBB`` hexadecimal string.

    Args:
        r: Red channel (0-255).
        g: Green channel (0-255).
        b: Blue channel (0-255).

    Returns:
        A lowercase ``#RRGGBB`` hexadecimal color string.

    Raises:
        TypeError: If any channel is not an integer.
        ValueError: If any channel is outside ``0``-``255``.

    Examples:
        >>> rgb_to_hex(255, 87, 51)
        '#ff5733'
        >>> rgb_to_hex(0, 0, 0)
        '#000000'
    """
    r = _require_int_range(r, "r")
    g = _require_int_range(g, "g")
    b = _require_int_range(b, "b")
    return f"#{r:02x}{g:02x}{b:02x}"


def _srgb_linear(channel: int) -> float:
    """Linearize an sRGB 8-bit channel per the WCAG 2.1 relative luminance formula."""
    c = channel / 255.0
    if c <= 0.03928:
        return float(c / 12.92)
    return float(((c + 0.055) / 1.055) ** 2.4)


def get_luminance(color: _Color) -> float:
    """Return the WCAG 2.1 relative luminance of a color.

    The result is in the range ``0.0`` (black) to ``1.0`` (white).

    Args:
        color: A hex string or an ``(r, g, b)`` tuple.

    Returns:
        The relative luminance as a float.

    Raises:
        TypeError: If ``color`` is not a hex string or RGB tuple.
        ValueError: If an RGB channel is outside ``0``-``255``.

    Examples:
        >>> round(get_luminance("#ffffff"), 4)
        1.0
        >>> round(get_luminance("#000000"), 4)
        0.0
        >>> round(get_luminance((255, 255, 255)), 4)
        1.0
    """
    r, g, b = _parse_color(color, "color")
    return 0.2126 * _srgb_linear(r) + 0.7152 * _srgb_linear(g) + 0.0722 * _srgb_linear(b)


def rgb_to_hsl(r: int, g: int, b: int) -> Tuple[float, float, float]:
    """Convert RGB channel values to HSL ``(h, s, l)``.

    Hue is in degrees ``[0, 360)``; saturation and lightness are in ``[0, 1]``.

    Args:
        r: Red channel (0-255).
        g: Green channel (0-255).
        b: Blue channel (0-255).

    Returns:
        A tuple ``(h, s, l)`` with ``h`` in degrees and ``s``, ``l`` in ``[0, 1]``.

    Raises:
        TypeError: If any channel is not an integer.
        ValueError: If any channel is outside ``0``-``255``.

    Examples:
        >>> h, s, l = rgb_to_hsl(255, 0, 0)
        >>> round(h), round(s, 2), round(l, 2)
        (0, 1.0, 0.5)
    """
    rf = _require_int_range(r, "r") / 255.0
    gf = _require_int_range(g, "g") / 255.0
    bf = _require_int_range(b, "b") / 255.0
    max_c = max(rf, gf, bf)
    min_c = min(rf, gf, bf)
    lightness = (max_c + min_c) / 2.0
    if max_c == min_c:
        return 0.0, 0.0, lightness
    d = max_c - min_c
    s = d / (2.0 - max_c - min_c) if lightness > 0.5 else d / (max_c + min_c)
    if max_c == rf:
        h = (60.0 * ((gf - bf) / d) + 360.0) % 360.0
    elif max_c == gf:
        h = (60.0 * ((bf - rf) / d) + 120.0) % 360.0
    else:
        h = (60.0 * ((rf - gf) / d) + 240.0) % 360.0
    return h, s, lightness


def hsl_to_rgb(h: float, s: float, lightness: float) -> _RGB:
    """Convert HSL ``(h, s, l)`` to RGB ``(r, g, b)``.

    Hue ``h`` is in degrees; saturation ``s`` and lightness ``l`` are in ``[0, 1]``.

    Args:
        h: Hue in degrees.
        s: Saturation in ``[0, 1]``.
        l: Lightness in ``[0, 1]``.

    Returns:
        A tuple of three integers ``(r, g, b)`` in the range ``0``-``255``.

    Raises:
        TypeError: If any argument is not a number.
        ValueError: If ``s`` or ``l`` is outside ``[0, 1]``.

    Examples:
        >>> hsl_to_rgb(0, 1.0, 0.5)
        (255, 0, 0)
        >>> hsl_to_rgb(0, 0.0, 0.0)
        (0, 0, 0)
    """
    if not all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in (h, s, lightness)):
        raise TypeError("h, s, and lightness must be numbers")
    if not 0.0 <= s <= 1.0 or not 0.0 <= lightness <= 1.0:
        raise ValueError("s and lightness must be in the range [0, 1]")

    def _hue_to_rgb(p: float, q: float, t: float) -> float:
        t %= 1.0
        if t < 1.0 / 6.0:
            return p + (q - p) * 6.0 * t
        if t < 0.5:
            return q
        if t < 2.0 / 3.0:
            return p + (q - p) * (2.0 / 3.0 - t) * 6.0
        return p

    if s == 0.0:
        r = g = b = lightness
    else:
        q = lightness * (1.0 + s) if lightness < 0.5 else lightness + s - lightness * s
        p = 2.0 * lightness - q
        r = _hue_to_rgb(p, q, h / 360.0 + 1.0 / 3.0)
        g = _hue_to_rgb(p, q, h / 360.0)
        b = _hue_to_rgb(p, q, h / 360.0 - 1.0 / 3.0)
    return (
        _require_int_range(round(r * 255), "r"),
        _require_int_range(round(g * 255), "g"),
        _require_int_range(round(b * 255), "b"),
    )


def get_contrast_ratio(color1: _Color, color2: _Color) -> float:
    """Return the WCAG 2.1 contrast ratio between two colors.

    The ratio is in the range ``1.0`` (identical colors) to ``21.0`` (black vs
    white). The lighter color's luminance is used as the numerator.

    Args:
        color1: First color (hex string or ``(r, g, b)`` tuple).
        color2: Second color (hex string or ``(r, g, b)`` tuple).

    Returns:
        The contrast ratio as a float.

    Raises:
        TypeError: If either color is not a hex string or RGB tuple.
        ValueError: If an RGB channel is outside ``0``-``255``.

    Examples:
        >>> round(get_contrast_ratio("#ffffff", "#000000"), 2)
        21.0
        >>> round(get_contrast_ratio("#ffffff", "#ffffff"), 2)
        1.0
    """
    lum1 = get_luminance(color1)
    lum2 = get_luminance(color2)
    lighter = max(lum1, lum2)
    darker = min(lum1, lum2)
    return (lighter + 0.05) / (darker + 0.05)


def is_accessible(
    foreground: _Color,
    background: _Color,
    level: str = "AA",
    size: str = "normal",
) -> bool:
    """Return ``True`` if the color pair meets a WCAG contrast threshold.

    Args:
        foreground: Foreground color (hex string or ``(r, g, b)`` tuple).
        background: Background color (hex string or ``(r, g, b)`` tuple).
        level: Conformance level, either ``"AA"`` or ``"AAA"``.
        size: Text size, either ``"normal"`` or ``"large"``.

    Returns:
        ``True`` when the contrast ratio meets the threshold for the given
        level and size, ``False`` otherwise.

    Raises:
        TypeError: If ``level`` or ``size`` is not a string.
        ValueError: If ``level`` or ``size`` is not a recognized value.

    Examples:
        >>> is_accessible("#000000", "#ffffff")
        True
        >>> is_accessible("#ffffff", "#ffffff", level="AA")
        False
    """
    _require_string(level, "level")
    _require_string(size, "size")
    key = (level.upper(), size.lower())
    if key not in _ACCESSIBILITY_THRESHOLDS:
        raise ValueError(
            f"Unknown level/size combination: {level!r}/{size!r}; "
            "expected level in {'AA', 'AAA'} and size in {'normal', 'large'}"
        )
    return get_contrast_ratio(foreground, background) >= _ACCESSIBILITY_THRESHOLDS[key]


def adjust_brightness(hex_color: str, factor: float) -> str:
    """Scale each RGB channel of ``hex_color`` by ``factor`` and return a hex string.

    ``factor`` of ``1.0`` returns the color unchanged; ``0.0`` returns black;
    values above ``1.0`` brighten the color (channels are clamped to 255).

    Args:
        hex_color: A ``#RRGGBB`` or ``RRGGBB`` color string.
        factor: Brightness multiplier (must be non-negative).

    Returns:
        A lowercase ``#RRGGBB`` hexadecimal color string.

    Raises:
        TypeError: If ``hex_color`` is not a string or ``factor`` is not a number.
        ValueError: If ``hex_color`` is invalid or ``factor`` is negative.

    Examples:
        >>> adjust_brightness("#ff5733", 0.5)
        '#7f2b19'
        >>> adjust_brightness("#000000", 2.0)
        '#000000'
    """
    _require_string(hex_color, "hex_color")
    if not isinstance(factor, (int, float)) or isinstance(factor, bool):
        raise TypeError("factor must be a number")
    if factor < 0:
        raise ValueError("factor must be non-negative")
    if not validate_hex(hex_color):
        raise ValueError(f"Invalid hex color: {hex_color!r}")
    r, g, b = hex_to_rgb(hex_color)
    return rgb_to_hex(
        min(255, int(round(r * factor))),
        min(255, int(round(g * factor))),
        min(255, int(round(b * factor))),
    )


def blend_colors(color1: _Color, color2: _Color, weight: float = 0.5) -> str:
    """Linearly blend two colors and return the result as a hex string.

    ``weight`` of ``0.0`` returns ``color1``; ``1.0`` returns ``color2``;
    intermediate values interpolate between them.

    Args:
        color1: First color (hex string or ``(r, g, b)`` tuple).
        color2: Second color (hex string or ``(r, g, b)`` tuple).
        weight: Blend weight for ``color2`` in ``[0, 1]`` (default: 0.5).

    Returns:
        A lowercase ``#RRGGBB`` hexadecimal color string.

    Raises:
        TypeError: If either color is invalid or ``weight`` is not a number.
        ValueError: If ``weight`` is outside ``[0, 1]`` or an RGB channel is
            outside ``0``-``255``.

    Examples:
        >>> blend_colors("#000000", "#ffffff", 0.5)
        '#7f7f7f'
        >>> blend_colors("#ff0000", "#0000ff", 0.0)
        '#ff0000'
    """
    if not isinstance(weight, (int, float)) or isinstance(weight, bool):
        raise TypeError("weight must be a number")
    if not 0.0 <= weight <= 1.0:
        raise ValueError("weight must be in the range [0, 1]")
    r1, g1, b1 = _parse_color(color1, "color1")
    r2, g2, b2 = _parse_color(color2, "color2")
    return rgb_to_hex(
        int(round(r1 + (r2 - r1) * weight)),
        int(round(g1 + (g2 - g1) * weight)),
        int(round(b1 + (b2 - b1) * weight)),
    )
