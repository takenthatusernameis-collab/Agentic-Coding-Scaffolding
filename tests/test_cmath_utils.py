import math
import unittest

from cmath_utils import (
    acos,
    acosh,
    asin,
    asinh,
    atan,
    atanh,
    cos,
    cosh,
    exp,
    isclose,
    isfinite,
    isinf,
    isnan,
    log,
    log10,
    phase,
    polar,
    rect,
    sin,
    sinh,
    sqrt,
    tan,
    tanh,
)


class TestPhase(unittest.TestCase):
    def test_phase_positive_real(self):
        self.assertEqual(phase(1), 0.0)

    def test_phase_negative_real(self):
        self.assertEqual(phase(-1), math.pi)

    def test_phase_complex(self):
        self.assertAlmostEqual(phase(1 + 1j), math.pi / 4)

    def test_phase_invalid(self):
        with self.assertRaises(TypeError):
            phase("1+1j")  # type: ignore[arg-type]


class TestPolar(unittest.TestCase):
    def test_polar_one(self):
        self.assertEqual(polar(1), (1.0, 0.0))

    def test_polar_complex(self):
        modulus, ph = polar(1 + 1j)
        self.assertAlmostEqual(modulus, math.sqrt(2))
        self.assertAlmostEqual(ph, math.pi / 4)

    def test_polar_invalid(self):
        with self.assertRaises(TypeError):
            polar([1, 2])  # type: ignore[arg-type]


class TestRect(unittest.TestCase):
    def test_rect_roundtrip(self):
        r, phi = 2.0, math.pi / 3
        z = rect(r, phi)
        modulus, phase = polar(z)
        self.assertAlmostEqual(modulus, r)
        self.assertAlmostEqual(phase % (2 * math.pi), phi % (2 * math.pi))

    def test_rect_zero(self):
        self.assertEqual(rect(0, 5), 0j)

    def test_rect_invalid_r(self):
        with self.assertRaises(TypeError):
            rect("2", 1)  # type: ignore[arg-type]

    def test_rect_invalid_phi(self):
        with self.assertRaises(TypeError):
            rect(2, "1")  # type: ignore[arg-type]


class TestExp(unittest.TestCase):
    def test_exp_zero(self):
        self.assertEqual(exp(0), 1 + 0j)

    def test_exp_one(self):
        self.assertAlmostEqual(exp(1).real, math.e)
        self.assertAlmostEqual(exp(1).imag, 0.0)

    def test_exp_invalid(self):
        with self.assertRaises(TypeError):
            exp(None)  # type: ignore[arg-type]


class TestLog(unittest.TestCase):
    def test_log_one(self):
        self.assertEqual(log(1), 0j)

    def test_log_e(self):
        self.assertAlmostEqual(log(math.e).real, 1.0)
        self.assertAlmostEqual(log(math.e).imag, 0.0)

    def test_log_base(self):
        self.assertAlmostEqual(log(8, 2).real, 3.0)
        self.assertAlmostEqual(log(8, 2).imag, 0.0)

    def test_log_invalid(self):
        with self.assertRaises(TypeError):
            log("1")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            log(1, "2")  # type: ignore[arg-type]


class TestLog10(unittest.TestCase):
    def test_log10_one(self):
        self.assertEqual(log10(1), 0j)

    def test_log10_hundred(self):
        self.assertAlmostEqual(log10(100).real, 2.0)
        self.assertAlmostEqual(log10(100).imag, 0.0)

    def test_log10_invalid(self):
        with self.assertRaises(TypeError):
            log10([100])  # type: ignore[arg-type]


class TestSqrt(unittest.TestCase):
    def test_sqrt_negative(self):
        self.assertEqual(sqrt(-1), 1j)

    def test_sqrt_positive(self):
        self.assertEqual(sqrt(4), 2 + 0j)

    def test_sqrt_invalid(self):
        with self.assertRaises(TypeError):
            sqrt("4")  # type: ignore[arg-type]


class TestTrig(unittest.TestCase):
    def test_sin_cos(self):
        self.assertEqual(sin(0), 0j)
        self.assertAlmostEqual(sin(math.pi / 2).real, 1.0)
        self.assertAlmostEqual(cos(0).real, 1.0)
        self.assertAlmostEqual(cos(math.pi).real, -1.0)

    def test_tan(self):
        self.assertEqual(tan(0), 0j)

    def test_invalid(self):
        with self.assertRaises(TypeError):
            sin("x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            cos("x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            tan("x")  # type: ignore[arg-type]


class TestInverseTrig(unittest.TestCase):
    def test_asin_acos_atan(self):
        self.assertEqual(asin(0), 0j)
        self.assertAlmostEqual(asin(1).real, math.pi / 2)
        self.assertEqual(acos(1), 0j)
        self.assertAlmostEqual(acos(0).real, math.pi / 2)
        self.assertEqual(atan(0), 0j)
        self.assertAlmostEqual(atan(1).real, math.pi / 4)

    def test_invalid(self):
        with self.assertRaises(TypeError):
            asin("x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            acos("x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            atan("x")  # type: ignore[arg-type]


class TestHyperbolic(unittest.TestCase):
    def test_sinh_cosh_tanh(self):
        self.assertEqual(sinh(0), 0j)
        self.assertEqual(cosh(0), 1 + 0j)
        self.assertEqual(tanh(0), 0j)

    def test_inverse(self):
        self.assertEqual(asinh(0), 0j)
        self.assertEqual(acosh(1), 0j)
        self.assertEqual(atanh(0), 0j)

    def test_invalid(self):
        with self.assertRaises(TypeError):
            sinh("x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            cosh("x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            tanh("x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            asinh("x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            acosh("x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            atanh("x")  # type: ignore[arg-type]


class TestClassification(unittest.TestCase):
    def test_isfinite(self):
        self.assertTrue(isfinite(1 + 2j))
        self.assertFalse(isfinite(complex(math.inf, 0)))
        self.assertFalse(isfinite(complex(0, math.inf)))
        self.assertFalse(isfinite(complex(math.nan, 0)))

    def test_isinf(self):
        self.assertTrue(isinf(complex(math.inf, 0)))
        self.assertFalse(isinf(1 + 2j))

    def test_isnan(self):
        self.assertTrue(isnan(complex(math.nan, 0)))
        self.assertFalse(isnan(1 + 2j))

    def test_invalid(self):
        with self.assertRaises(TypeError):
            isfinite("x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            isinf("x")  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            isnan("x")  # type: ignore[arg-type]


class TestIsClose(unittest.TestCase):
    def test_isclose_same(self):
        self.assertTrue(isclose(1 + 1j, 1 + 1j))

    def test_isclose_different(self):
        self.assertFalse(isclose(1 + 1j, 1 + 2j))

    def test_isclose_tolerance(self):
        self.assertTrue(isclose(1 + 1j, 1 + 1.0000000001j))
        self.assertFalse(isclose(1 + 1j, 1 + 2j, abs_tol=0.5))

    def test_invalid(self):
        with self.assertRaises(TypeError):
            isclose("x", 1)  # type: ignore[arg-type]
        with self.assertRaises(TypeError):
            isclose(1, "x")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            isclose(1, 1, rel_tol=-1)
        with self.assertRaises(ValueError):
            isclose(1, 1, abs_tol=-1)


if __name__ == "__main__":
    unittest.main()
