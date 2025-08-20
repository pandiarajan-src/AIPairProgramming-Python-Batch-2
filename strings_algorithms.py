"""
This module contains various string and number algorithms, including palindrome checks,
pangram detection, anagram checks, and more.

Prompt Given:

Create a new python program strings_algorithms.py featuring the following functionalites,
each bullet will be impletemented as a function
and finally call all the function with examples in the main function.

• What is a palindrome and find if the given number is a palindrome number
• What is a pangram and find if the given sentence is a pangram
• What is an anagram and find if the two given strings are anagrams of each other
• Print the frequency of each character in the given string
• Find if the given number is an Armstrong number
• Print all the Armstrong numbers in the given range
• Print all the primes in the given range using Sieve of Eratosthenes
• Improve the timing of the prime number printing program
• Find the frequency of the words in the given sentence
• Reverse each word separately in the given sentence
• Check if the password has at least 1 capital case letter,
    1 number, 1 small case letter and one special character
• Convert the given string to a number atoi
• Convert the given decimal number to binary
• Convert the given decimal number to hexadecimal
"""


def is_palindrome(number):
    """Check if a number is a palindrome."""
    str_num = str(number)
    return str_num == str_num[::-1]


def is_pangram(sentence):
    """Check if a sentence is a pangram."""
    alphabet = set("abcdefghijklmnopqrstuvwxyz")
    return alphabet <= set(sentence.lower())


def are_anagrams(str1, str2):
    """Check if two strings are anagrams."""
    return sorted(str1) == sorted(str2)


def char_frequency(string):
    """Print the frequency of each character in a string."""
    freq = {}
    for char in string:
        freq[char] = freq.get(char, 0) + 1
    return freq


def is_armstrong(number):
    """Check if a number is an Armstrong number."""
    digits = list(map(int, str(number)))
    power = len(digits)
    return number == sum(d**power for d in digits)


def armstrong_in_range(start, end):
    """Print all Armstrong numbers in a given range."""
    return [num for num in range(start, end + 1) if is_armstrong(num)]


def sieve_of_eratosthenes(limit):
    """Print all prime numbers in a range using Sieve of Eratosthenes."""
    primes = [True] * (limit + 1)
    primes[0] = primes[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if primes[i]:
            for j in range(i * i, limit + 1, i):
                primes[j] = False
    return [i for i, is_prime in enumerate(primes) if is_prime]


def word_frequency(sentence):
    """Find the frequency of words in a sentence."""
    words = sentence.split()
    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1
    return freq


def reverse_words(sentence):
    """Reverse each word in a sentence."""
    return " ".join(word[::-1] for word in sentence.split())


def is_valid_password(password):
    """
    Check if a password has at least one uppercase, one lowercase, one digit,
    and one special character.
    """
    has_upper = any(char.isupper() for char in password)
    has_lower = any(char.islower() for char in password)
    has_digit = any(char.isdigit() for char in password)
    has_special = any(not char.isalnum() for char in password)
    return has_upper and has_lower and has_digit and has_special


def atoi(string):
    """Convert a string to an integer."""
    try:
        return int(string)
    except ValueError:
        return None


def decimal_to_binary(number):
    """Convert a decimal number to binary."""
    return bin(number)[2:]


def decimal_to_hexadecimal(number):
    """Convert a decimal number to hexadecimal."""
    return hex(number)[2:]


def main():
    """
    Main function to demonstrate the usage of all implemented algorithms.
    """
    # Examples for each function
    print("Palindrome check for 121:", is_palindrome(121))
    print(
        "Pangram check for 'The quick brown fox jumps over the lazy dog':",
        is_pangram("The quick brown fox jumps over the lazy dog"),
    )
    print("Anagram check for 'listen' and 'silent':", are_anagrams("listen", "silent"))
    print("Character frequency in 'hello':", char_frequency("hello"))
    print("Armstrong check for 153:", is_armstrong(153))
    print("Armstrong numbers in range 100 to 999:", armstrong_in_range(100, 999))
    print("Prime numbers up to 50:", sieve_of_eratosthenes(50))
    print("Word frequency in 'hello world hello':", word_frequency("hello world hello"))
    print("Reversed words in 'hello world':", reverse_words("hello world"))
    print("Password validity for 'P@ssw0rd':", is_valid_password("P@ssw0rd"))
    print("String to integer conversion for '123':", atoi("123"))
    print("Decimal to binary for 10:", decimal_to_binary(10))
    print("Decimal to hexadecimal for 255:", decimal_to_hexadecimal(255))


if __name__ == "__main__":
    main()
