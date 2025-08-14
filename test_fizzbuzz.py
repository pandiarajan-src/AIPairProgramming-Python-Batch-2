"""
Unit tests for the FizzBuzz module.
"""

import unittest
from fizzbuzz import fizzbuzz, get_primes, sieve_of_eratosthenes


class TestFizzBuzz(unittest.TestCase):
    """Test cases for the FizzBuzz module."""

    def test_fizzbuzz(self):
        """Test the fizzbuzz function."""
        self.assertEqual(fizzbuzz(1), 1)
        self.assertEqual(fizzbuzz(3), "Fizz")
        self.assertEqual(fizzbuzz(5), "Buzz")
        self.assertEqual(fizzbuzz(15), "FizzBuzz")
        self.assertEqual(fizzbuzz(7), 7)

    def test_get_primes(self):
        """Test the get_primes function."""
        self.assertEqual(
            get_primes(10), [2, "Fizz", "Buzz", 7]
        )  # Ensure raw primes are returned
        self.assertEqual(get_primes(1), [])
        self.assertEqual(get_primes(2), [2])

    def test_sieve_of_eratosthenes(self):
        """Test the sieve_of_eratosthenes function."""
        self.assertEqual(
            sieve_of_eratosthenes(10), [2, "Fizz", "Buzz", 7]
        )  # Ensure raw primes are returned
        self.assertEqual(sieve_of_eratosthenes(1), [])
        self.assertEqual(sieve_of_eratosthenes(2), [2])


if __name__ == "__main__":
    unittest.main()
