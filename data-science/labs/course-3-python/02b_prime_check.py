"""Experiment 2(b): Check whether a number is prime using loops.

Only test divisors up to sqrt(n): if n has a factor larger than its square
root, the matching co-factor is smaller than the square root and would have
been found already.

Syllabus: Course 3, Unit 2 -- iterative statements.
Sample input: 29
"""

# Step 1: Read n
n = int(input("Enter a number: "))

# Step 2: A number below 2 is not prime
if n < 2:
    print(f"{n} is not a prime number (primes start at 2)")
else:
    is_prime = True
    divisor = 2
    # Step 3: Try each divisor up to the square root
    while divisor * divisor <= n:
        if n % divisor == 0:
            is_prime = False
            print(f"{n} is divisible by {divisor}")
            break
        divisor += 1

    # Step 4: Report the result
    print(f"{n} is {'a prime' if is_prime else 'not a prime'} number")
