"""
Test module for FizzBuzz.

This module contains tests for the fizzbuzz function.
"""

from fizzbuzz import fizzbuzz


def test_fizzbuzz():
    """Test the fizzbuzz function for correctness."""
    output = [fizzbuzz(i) for i in range(1, 101)]
    assert output[2] == "Fizz"  # 3rd element (3) should be "Fizz"
    assert output[4] == "Buzz"  # 5th element (5) should be "Buzz"
    assert output[14] == "FizzBuzz"  # 15th element (15) should be "FizzBuzz"
    assert output[0] == 1  # 1st element (1) should be 1
    assert output[99] == "Buzz"  # 100th element (100) should be "Buzz"
