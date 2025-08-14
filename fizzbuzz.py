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


def get_primes(n_max):
    """Generate primes till n_max using a one-line list comprehension."""
    return [
        n
        for n in range(2, n_max + 1)
        if all(n % d != 0 for d in range(2, int(n**0.5) + 1))
    ]


if __name__ == "__main__":
    _primes = get_primes(100)
    for i in _primes:
        print(fizzbuzz(i))
