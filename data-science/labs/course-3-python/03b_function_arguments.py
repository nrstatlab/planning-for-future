"""Experiment 3(b): Demonstrate the different types of function arguments --
default, positional, keyword and variable-length.

Syllabus: Course 3, Unit 2 -- function arguments.
"""


# Step 1: Required and default parameters
def student(name, course, year=1):
    """`name` and `course` are required; `year` has a default value."""
    return f"{name} studies {course}, year {year}"


# Step 2: Variable-length *args and **kwargs
def total(*numbers):
    """*args -- variable number of positional arguments, received as a tuple."""
    print(f"  received {len(numbers)} arguments as a tuple: {numbers}")
    return sum(numbers)


def profile(**details):
    """**kwargs -- variable keyword arguments, received as a dictionary."""
    print(f"  received a dict: {details}")
    return ", ".join(f"{k}={v}" for k, v in details.items())


# Step 3: All four kinds in their required order
def mixed(required, default="D", *args, **kwargs):
    """The mandatory ordering: required, default, *args, **kwargs."""
    return f"required={required}, default={default}, args={args}, kwargs={kwargs}"


# Step 4: Call with positional, keyword and default arguments
print("POSITIONAL arguments -- matched by position")
print(" ", student("Ananya", "Data Science"))

print("\nKEYWORD arguments -- matched by name, so order stops mattering")
print(" ", student(course="Statistics", name="Bhavana", year=2))

print("\nDEFAULT argument -- year falls back to 1 when omitted")
print(" ", student("Charan", "Python"))

# Step 5: Call with variable-length arguments
print("\nVARIABLE-LENGTH *args")
print(f"  total(1, 2, 3, 4, 5) = {total(1, 2, 3, 4, 5)}")

print("\nVARIABLE-LENGTH **kwargs")
print(f"  {profile(name='Divya', roll=24003, cgpa=9.1)}")

print("\nALL FOUR TOGETHER")
print(" ", mixed("R", "X", 1, 2, extra="yes"))
