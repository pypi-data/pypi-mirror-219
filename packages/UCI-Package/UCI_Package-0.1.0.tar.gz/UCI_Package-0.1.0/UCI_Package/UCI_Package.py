def count_vowels(string):
    return sum(1 for char in string.lower() if char in 'aeiou')

def reverse_string(string):
    return string[::-1]

def is_palindrome(string):
    return string.lower() == string.lower()[::-1]