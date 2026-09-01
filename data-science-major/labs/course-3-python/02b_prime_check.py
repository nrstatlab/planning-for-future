"""Experiment 2(b): Check whether a number is prime using loops.

Only test divisors up to sqrt(n): if n has a factor larger than its square
root, the matching co-factor is smaller than the square root and would have
been found already.

Syllabus: Course 3, Unit 2 -- iterative statements.
Sample input: 29
"""

n = int(input("Enter a number: "))

if n < 2:
    print(f"{n} is not a prime number (primes start at 2)")
else:
    is_prime = True
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            is_prime = False
            print(f"{n} is divisible by {divisor}")
            break
        divisor += 1

    print(f"{n} is {'a prime' if is_prime else 'not a prime'} number")
