"""
FizzBuzz module.

This module contains a function to compute the FizzBuzz value for a given number.
"""
import time


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
        fizzbuzz(n)
        for n in range(2, n_max + 1)
        if all(n % d != 0 for d in range(2, int(n**0.5) + 1))
    ]


def sieve_of_eratosthenes(n_max):
    """Generate primes till n_max using the Sieve of Eratosthenes."""
    if n_max < 2:
        return []
    sieve = [True] * (n_max + 1)
    sieve[0] = sieve[1] = False
    for start in range(2, int(n_max**0.5) + 1):
        if sieve[start]:
            for multiple in range(start * start, n_max + 1, start):
                sieve[multiple] = False
    return [fizzbuzz(num) for num, is_prime in enumerate(sieve) if is_prime]


if __name__ == "__main__":
    # Task 1: Prime numbers from 1 to 100 and timing
    print("\nPrime numbers using list comprehension:")
    start_time = time.time()
    primes_list_comprehension = get_primes(100)
    end_time = time.time()
    print(primes_list_comprehension)
    print(f"Time taken: {end_time - start_time:.6f} seconds")

    # Task 2: Prime numbers using Sieve of Eratosthenes and timing
    print("\nPrime numbers using Sieve of Eratosthenes:")
    start_time = time.time()
    primes_sieve = sieve_of_eratosthenes(100)
    end_time = time.time()
    print(primes_sieve)
    print(f"Time taken: {end_time - start_time:.6f} seconds")
