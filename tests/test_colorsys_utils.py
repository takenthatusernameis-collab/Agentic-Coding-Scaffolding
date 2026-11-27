import colorsys

import pytest

import colorsys_utils


def test_rgb_to_hls():
    assert colorsys_utils.rgb_to_hls(1.0, 0.0, 0.0) == colorsys.rgb_to_hls(1.0, 0.0, 0.0)


def test_hls_to_rgb():
    assert colorsys_utils.hls_to_rgb(0.0, 0.5, 1.0) == colorsys.hls_to_rgb(0.0, 0.5, 1.0)


def test_rgb_to_hsv():
    assert colorsys_utils.rgb_to_hsv(1.0, 0.0, 0.0) == colorsys.rgb_to_hsv(1.0, 0.0, 0.0)


def test_hsv_to_rgb():
    assert colorsys_utils.hsv_to_rgb(0.0, 1.0, 1.0) == colorsys.hsv_to_rgb(0.0, 1.0, 1.0)


def test_rgb_to_yiq():
    assert colorsys_utils.rgb_to_yiq(1.0, 0.0, 0.0) == colorsys.rgb_to_yiq(1.0, 0.0, 0.0)


def test_yiq_to_rgb():
    a = (0.299, 0.596, 0.211)
    assert colorsys_utils.yiq_to_rgb(*a) == colorsys.yiq_to_rgb(*a)


def test_conversions_reject_non_numeric():
    """All conversions leak ``TypeError`` from stdlib ``colorsys`` on non-numeric input.

    Genuine stdlib delegation, documented with ``# audit-ignore: TypeError``.
    """
    for fn in (
        colorsys_utils.rgb_to_hls,
        colorsys_utils.hls_to_rgb,
        colorsys_utils.rgb_to_hsv,
        colorsys_utils.hsv_to_rgb,
        colorsys_utils.rgb_to_yiq,
        colorsys_utils.yiq_to_rgb,
    ):
        with pytest.raises(TypeError):
            fn("a", "b", "c")  # type: ignore[arg-type]
