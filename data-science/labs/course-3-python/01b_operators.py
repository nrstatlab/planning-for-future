"""Experiment 1(b): Perform arithmetic, relational, logical, bitwise and
assignment operations on given inputs.

Syllabus: Course 3, Unit 1 -- classification of operators.
Sample input: 12 5
"""

# Step 1: Read two integers
a = int(input("Enter the first integer : "))
b = int(input("Enter the second integer: "))

# Step 2: Arithmetic
print(f"\nARITHMETIC   (a = {a}, b = {b})")
print(f"  a + b  = {a + b}")
print(f"  a - b  = {a - b}")
print(f"  a * b  = {a * b}")
print(f"  a / b  = {a / b}      <- true division, always a float")
print(f"  a // b = {a // b}      <- floor division")
print(f"  a % b  = {a % b}")
print(f"  a ** b = {a ** b}")

# Step 3: Relational
print("\nRELATIONAL")
for symbol, result in (("==", a == b), ("!=", a != b), (">", a > b),
                       ("<", a < b), (">=", a >= b), ("<=", a <= b)):
    print(f"  a {symbol:<2} b = {result}")

# Step 4: Logical
print("\nLOGICAL")
print(f"  (a > 0) and (b > 0) = {(a > 0) and (b > 0)}")
print(f"  (a > 0) or  (b < 0) = {(a > 0) or (b < 0)}")
print(f"  not (a > b)         = {not (a > b)}")

# Step 5: Bitwise
print("\nBITWISE")
print(f"  a = {a} = {a:b} in binary, b = {b} = {b:b} in binary")
print(f"  a &  b = {a & b}")
print(f"  a |  b = {a | b}")
print(f"  a ^  b = {a ^ b}")
print(f"  ~a     = {~a}")
print(f"  a << 1 = {a << 1}")
print(f"  a >> 1 = {a >> 1}")

# Step 6: Augmented assignment
print("\nASSIGNMENT (augmented)")
x = a
x += b; print(f"  x += b -> {x}")
x -= b; print(f"  x -= b -> {x}")
x *= b; print(f"  x *= b -> {x}")
x //= b; print(f"  x //= b -> {x}")

# Step 7: Identity and membership
print("\nIDENTITY and MEMBERSHIP")
print(f"  a is b     = {a is b}")
print(f"  a in [a, b] = {a in [a, b]}")
