"""
Unit tests for the strings_algorithms module.
"""

import unittest
from strings_algorithms import (
    is_palindrome,
    is_pangram,
    are_anagrams,
    char_frequency,
    is_armstrong,
    armstrong_in_range,
    sieve_of_eratosthenes,
    word_frequency,
    reverse_words,
    is_valid_password,
    atoi,
    decimal_to_binary,
    decimal_to_hexadecimal,
)


class TestStringsAlgorithms(unittest.TestCase):
    """
    Test suite for the functions in strings_algorithms.py.
    """

    def test_is_palindrome(self):
        """
        Test the is_palindrome function with valid and invalid cases.
        """
        self.assertTrue(is_palindrome(121))
        self.assertFalse(is_palindrome(123))

    def test_is_pangram(self):
        """
        Test the is_pangram function with valid and invalid cases.
        """
        self.assertTrue(is_pangram("The quick brown fox jumps over the lazy dog"))
        self.assertFalse(is_pangram("Hello world"))

    def test_are_anagrams(self):
        """
        Test the are_anagrams function with valid and invalid cases.
        """
        self.assertTrue(are_anagrams("listen", "silent"))
        self.assertFalse(are_anagrams("hello", "world"))

    def test_char_frequency(self):
        """
        Test the char_frequency function with a sample string.
        """
        self.assertEqual(char_frequency("hello"), {"h": 1, "e": 1, "l": 2, "o": 1})

    def test_is_armstrong(self):
        """
        Test the is_armstrong function with valid and invalid cases.
        """
        self.assertTrue(is_armstrong(153))
        self.assertFalse(is_armstrong(123))

    def test_armstrong_in_range(self):
        """
        Test the armstrong_in_range function with a sample range.
        """
        self.assertEqual(armstrong_in_range(100, 999), [153, 370, 371, 407])

    def test_sieve_of_eratosthenes(self):
        """
        Test the sieve_of_eratosthenes function with a sample limit.
        """
        self.assertEqual(sieve_of_eratosthenes(10), [2, 3, 5, 7])
        self.assertEqual(sieve_of_eratosthenes(0), [])

    def test_word_frequency(self):
        """
        Test the word_frequency function with a sample sentence.
        """
        self.assertEqual(word_frequency("hello world hello"), {"hello": 2, "world": 1})

    def test_reverse_words(self):
        """
        Test the reverse_words function with a sample sentence.
        """
        self.assertEqual(reverse_words("hello world"), "olleh dlrow")

    def test_is_valid_password(self):
        """
        Test the is_valid_password function with valid and invalid cases.
        """
        self.assertTrue(is_valid_password("P@ssw0rd"))
        self.assertFalse(is_valid_password("password"))

    def test_atoi(self):
        """
        Test the atoi function with valid and invalid cases.
        """
        self.assertEqual(atoi("123"), 123)
        self.assertIsNone(atoi("abc"))

    def test_decimal_to_binary(self):
        """
        Test the decimal_to_binary function with a sample number.
        """
        self.assertEqual(decimal_to_binary(10), "1010")

    def test_decimal_to_hexadecimal(self):
        """
        Test the decimal_to_hexadecimal function with a sample number.
        """
        self.assertEqual(decimal_to_hexadecimal(255), "ff")


if __name__ == "__main__":
    unittest.main()
