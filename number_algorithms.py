"""
number_algorithms.py

This Python program implements various number and string algorithms as separate functions.

Prompt given:
Create a new number_algorithms.py Python program
featuring the following functionalities, each implemented as a separate function:

1. Determine and print all factors of a given number.
2. Compare two given strings and print whether they are equal or unequal.
3. Calculate and display the frequency of a specific character within a given string.
4. Count and print the total number of vowels present in a given string.
5. Identify and print all numbers divisible by a specified number within a given range.
6. Compute the factorial of a number using both recursive and iterative methods.
7. Generate and display the Fibonacci series using both recursive and iterative methods.
8. Check if a provided name is in a predefined list
    and print "Welcome" if present or "See you next time" if absent.
9. Determine if a given number is a prime number and print the result.
10. Generate and print a list of all prime numbers within a specified range.
11. Check if a given number is a perfect number and print the result.
12. Generate and print a list of all perfect numbers within a specified range.

"""


# 1. Determine and print all factors of a given number
def find_factors(number):
    """Determine and return all factors of a given number."""
    return [i for i in range(1, number + 1) if number % i == 0]


# 2. Compare two given strings and print whether they are equal or unequal
def compare_strings(string1, string2):
    """Compare two strings and return whether they are equal or unequal."""
    return "Equal" if string1 == string2 else "Unequal"


# 3. Calculate and display the frequency of a specific character within a given string
def character_frequency(string, char):
    """Calculate the frequency of a specific character in a string."""
    return string.count(char)


# 4. Count and print the total number of vowels present in a given string
def count_vowels(string):
    """Count the total number of vowels in a given string."""
    vowels = "aeiouAEIOU"
    return sum(1 for char in string if char in vowels)


# 5. Identify and print all numbers divisible by a specified number within a given range
def divisible_numbers(start, end, divisor):
    """Find all numbers divisible by a specified number within a range."""
    return [i for i in range(start, end + 1) if i % divisor == 0]


# 6. Compute the factorial of a number using both recursive and iterative methods
def factorial_recursive(n):
    """Compute the factorial of a number using recursion."""
    if n in (0, 1):
        return 1
    return n * factorial_recursive(n - 1)


def factorial_iterative(n):
    """Compute the factorial of a number using iteration."""
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


# 7. Generate and display the Fibonacci series using both recursive and iterative methods
def fibonacci_recursive(n):
    """Generate the Fibonacci series up to n terms using recursion."""
    if n <= 0:
        return []
    if n == 1:
        return [0]
    if n == 2:
        return [0, 1]
    series = fibonacci_recursive(n - 1)
    series.append(series[-1] + series[-2])
    return series


def fibonacci_iterative(n):
    """Generate the Fibonacci series up to n terms using iteration."""
    if n <= 0:
        return []
    series = [0, 1]
    for _ in range(2, n):
        series.append(series[-1] + series[-2])
    return series[:n]


# 8. Check if a provided name is in a predefined list and print "Welcome" if present or "See you next time" if absent
def check_name(name, name_list):
    """Check if a name is in a predefined list and return a message."""
    return "Welcome" if name in name_list else "See you next time"


# 9. Determine if a given number is a prime number and print the result
def is_prime(number):
    """Determine if a number is a prime number."""
    if number <= 1:
        return False
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return False
    return True


# 10. Generate and print a list of all prime numbers within a specified range
def prime_numbers_in_range(start, end):
    """Generate a list of all prime numbers within a specified range."""
    return [i for i in range(start, end + 1) if is_prime(i)]


# 11. Check if a given number is a perfect number and print the result
def is_perfect_number(number):
    """Check if a number is a perfect number."""
    return sum(i for i in range(1, number) if number % i == 0) == number


# 12. Generate and print a list of all perfect numbers within a specified range
def perfect_numbers_in_range(start, end):
    """Generate a list of all perfect numbers within a specified range."""
    return [i for i in range(start, end + 1) if is_perfect_number(i)]


if __name__ == "__main__":
    # Example calls to the functions
    print("Factors of 28:", find_factors(28))
    print("Compare 'hello' and 'world':", compare_strings("hello", "world"))
    print("Frequency of 'l' in 'hello':", character_frequency("hello", "l"))
    print("Number of vowels in 'hello world':", count_vowels("hello world"))
    print("Numbers divisible by 3 between 1 and 10:", divisible_numbers(1, 10, 3))
    print("Factorial of 5 (recursive):", factorial_recursive(5))
    print("Factorial of 5 (iterative):", factorial_iterative(5))
    print("Fibonacci series (recursive, 5 terms):", fibonacci_recursive(5))
    print("Fibonacci series (iterative, 5 terms):", fibonacci_iterative(5))
    print(
        "Check name 'Alice' in ['Bob', 'Alice', 'Eve']:",
        check_name("Alice", ["Bob", "Alice", "Eve"]),
    )
    print("Is 29 a prime number?:", is_prime(29))
    print("Prime numbers between 10 and 20:", prime_numbers_in_range(10, 20))
    print("Is 28 a perfect number?:", is_perfect_number(28))
    print("Perfect numbers between 1 and 1000:", perfect_numbers_in_range(1, 1000))
