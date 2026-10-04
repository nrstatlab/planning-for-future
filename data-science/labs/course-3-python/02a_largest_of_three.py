"""Experiment 2(a): Find the largest of three numbers using if-elif-else.

Syllabus: Course 3, Unit 2 -- control flow.
Sample input: 45 78 23
"""

# Step 1: Read three numbers
a = float(input("Enter the first number : "))
b = float(input("Enter the second number: "))
c = float(input("Enter the third number : "))

# Step 2: Compare them with if-elif-else
if a >= b and a >= c:
    largest = a
elif b >= a and b >= c:
    largest = b
else:
    largest = c

# Step 3: Print the largest, and check it with max()
print(f"The largest of {a}, {b}, {c} is {largest}")

# Built-in alternative -- correct, but the exam wants the if-elif-else version.
print(f"Cross-check with max(): {max(a, b, c)}")
