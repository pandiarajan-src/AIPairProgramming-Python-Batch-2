"""
FizzBuzz module.

This module contains a function to compute the FizzBuzz value for a given number.
"""


def fizzbuzz(n):
    """Return 'Fizz', 'Buzz', 'FizzBuzz', or the number based on divisibility."""
    if n % 3 == 0 and n % 5 == 0:
        return "FizzBuzz"
    if n % 3 == 0:
        return "Fizz"
    if n % 5 == 0:
        return "Buzz"
    return n


if __name__ == "__main__":
    for i in range(1, 101):
        print(fizzbuzz(i))
