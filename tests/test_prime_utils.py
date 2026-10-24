import unittest

from prime_utils import is_coprime, nth_prime, prime_factors, primes_up_to


class TestPrimesUpTo(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(primes_up_to(10), [2, 3, 5, 7])
        self.assertEqual(primes_up_to(1), [])
        self.assertEqual(primes_up_to(2), [2])


class TestNthPrime(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(nth_prime(1), 2)
        self.assertEqual(nth_prime(5), 11)
        self.assertEqual(nth_prime(10), 29)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            nth_prime(0)


class TestPrimeFactors(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(prime_factors(12), [2, 2, 3])
        self.assertEqual(prime_factors(13), [13])
        self.assertEqual(prime_factors(100), [2, 2, 5, 5])

    def test_invalid(self):
        with self.assertRaises(ValueError):
            prime_factors(1)


class TestIsCoprime(unittest.TestCase):
    def test_basic(self):
        self.assertTrue(is_coprime(8, 15))
        self.assertFalse(is_coprime(12, 18))
        self.assertTrue(is_coprime(7, 7) is False)


if __name__ == "__main__":
    unittest.main()
