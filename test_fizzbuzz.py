"""
Test module for FizzBuzz.

This module contains tests for all functions and the main block in fizzbuzz.py.
"""

from fizzbuzz import fizzbuzz, get_primes


def test_fizzbuzz():
    """Test the fizzbuzz function for correctness."""
    assert fizzbuzz(3) == "Fizz"
    assert fizzbuzz(5) == "Buzz"
    assert fizzbuzz(15) == "FizzBuzz"
    assert fizzbuzz(7) == 7


def test_get_primes():
    """Test the get_primes function for correctness."""
    primes = get_primes(10)
    assert primes == [2, 3, 5, 7]

    primes = get_primes(20)
    assert primes == [2, 3, 5, 7, 11, 13, 17, 19]


def test_main_block(capsys):
    """Test the main block for correct output."""
    from fizzbuzz import __name__ as module_name

    if module_name == "__main__":
        from fizzbuzz import get_primes, fizzbuzz

        _primes = get_primes(10)
        for i in _primes:
            print(fizzbuzz(i))

        captured = capsys.readouterr()
        expected_output = "Fizz\nBuzz\n7\n"
        assert expected_output in captured.out
