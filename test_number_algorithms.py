"""
Unit tests for number_algorithms.py

This module contains unit tests for all functions in number_algorithms.py.
"""

import unittest
from number_algorithms import (
    find_factors,
    compare_strings,
    character_frequency,
    count_vowels,
    divisible_numbers,
    factorial_recursive,
    factorial_iterative,
    fibonacci_recursive,
    fibonacci_iterative,
    check_name,
    is_prime,
    prime_numbers_in_range,
    is_perfect_number,
    perfect_numbers_in_range,
)


class TestNumberAlgorithms(unittest.TestCase):
    """Unit tests for the number_algorithms module."""

    def test_find_factors(self):
        """Test the find_factors function."""
        self.assertEqual(find_factors(28), [1, 2, 4, 7, 14, 28])
        self.assertEqual(find_factors(1), [1])

    def test_compare_strings(self):
        """Test the compare_strings function."""
        self.assertEqual(compare_strings("hello", "hello"), "Equal")
        self.assertEqual(compare_strings("hello", "world"), "Unequal")

    def test_character_frequency(self):
        """Test the character_frequency function."""
        self.assertEqual(character_frequency("hello", "l"), 2)
        self.assertEqual(character_frequency("hello", "z"), 0)

    def test_count_vowels(self):
        """Test the count_vowels function."""
        self.assertEqual(count_vowels("hello world"), 3)
        self.assertEqual(count_vowels("bcdfg"), 0)

    def test_divisible_numbers(self):
        """Test the divisible_numbers function."""
        self.assertEqual(divisible_numbers(1, 10, 3), [3, 6, 9])
        self.assertEqual(divisible_numbers(1, 5, 7), [])

    def test_factorial_recursive(self):
        """Test the factorial_recursive function."""
        self.assertEqual(factorial_recursive(5), 120)
        self.assertEqual(factorial_recursive(0), 1)

    def test_factorial_iterative(self):
        """Test the factorial_iterative function."""
        self.assertEqual(factorial_iterative(5), 120)
        self.assertEqual(factorial_iterative(0), 1)

    def test_fibonacci_recursive(self):
        """Test the fibonacci_recursive function."""
        self.assertEqual(fibonacci_recursive(5), [0, 1, 1, 2, 3])
        self.assertEqual(fibonacci_recursive(0), [])

    def test_fibonacci_iterative(self):
        """Test the fibonacci_iterative function."""
        self.assertEqual(fibonacci_iterative(5), [0, 1, 1, 2, 3])
        self.assertEqual(fibonacci_iterative(0), [])

    def test_check_name(self):
        """Test the check_name function."""
        self.assertEqual(check_name("Alice", ["Bob", "Alice", "Eve"]), "Welcome")
        self.assertEqual(
            check_name("John", ["Bob", "Alice", "Eve"]), "See you next time"
        )

    def test_is_prime(self):
        """Test the is_prime function."""
        self.assertTrue(is_prime(29))
        self.assertFalse(is_prime(1))

    def test_prime_numbers_in_range(self):
        """Test the prime_numbers_in_range function."""
        self.assertEqual(prime_numbers_in_range(10, 20), [11, 13, 17, 19])
        self.assertEqual(prime_numbers_in_range(1, 1), [])

    def test_is_perfect_number(self):
        """Test the is_perfect_number function."""
        self.assertTrue(is_perfect_number(28))
        self.assertFalse(is_perfect_number(27))

    def test_perfect_numbers_in_range(self):
        """Test the perfect_numbers_in_range function."""
        self.assertEqual(perfect_numbers_in_range(1, 1000), [6, 28, 496])
        self.assertEqual(perfect_numbers_in_range(1, 5), [])


if __name__ == "__main__":
    unittest.main()
