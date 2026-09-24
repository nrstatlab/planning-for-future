"""Experiment 3(a): Calculate the factorial of a number using recursion.

Syllabus: Course 3, Unit 2 -- recursive functions.
Sample input: 6
"""


def factorial(n):
    """Return n! computed recursively."""
    if n < 0:
        raise ValueError("factorial is undefined for negative numbers")
    if n in (0, 1):          # BASE CASE -- stops the recursion
        return 1
    return n * factorial(n - 1)   # RECURSIVE CASE


def factorial_traced(n, depth=0):
    """Same function, printing the call stack so you can trace it in a viva."""
    indent = "  " * depth
    print(f"{indent}factorial({n}) called")
    if n in (0, 1):
        print(f"{indent}  base case -> 1")
        return 1
    result = n * factorial_traced(n - 1, depth + 1)
    print(f"{indent}  returns {n} * factorial({n - 1}) = {result}")
    return result


if __name__ == "__main__":
    number = int(input("Enter a non-negative integer: "))
    print(f"\n{number}! = {factorial(number)}\n")
    print("Call trace:")
    factorial_traced(number)
