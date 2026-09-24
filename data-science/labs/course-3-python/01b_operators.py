"""Experiment 1(b): Perform arithmetic, relational, logical, bitwise and
assignment operations on given inputs.

Syllabus: Course 3, Unit 1 -- classification of operators.
Sample input: 12 5
"""

a = int(input("Enter the first integer : "))
b = int(input("Enter the second integer: "))

print(f"\nARITHMETIC   (a = {a}, b = {b})")
print(f"  a + b  = {a + b}")
print(f"  a - b  = {a - b}")
print(f"  a * b  = {a * b}")
print(f"  a / b  = {a / b}      <- true division, always a float")
print(f"  a // b = {a // b}      <- floor division")
print(f"  a % b  = {a % b}")
print(f"  a ** b = {a ** b}")

print("\nRELATIONAL")
for symbol, result in (("==", a == b), ("!=", a != b), (">", a > b),
                       ("<", a < b), (">=", a >= b), ("<=", a <= b)):
    print(f"  a {symbol:<2} b = {result}")

print("\nLOGICAL")
print(f"  (a > 0) and (b > 0) = {(a > 0) and (b > 0)}")
print(f"  (a > 0) or  (b < 0) = {(a > 0) or (b < 0)}")
print(f"  not (a > b)         = {not (a > b)}")

print("\nBITWISE")
print(f"  a = {a} = {a:b} in binary, b = {b} = {b:b} in binary")
print(f"  a &  b = {a & b}")
print(f"  a |  b = {a | b}")
print(f"  a ^  b = {a ^ b}")
print(f"  ~a     = {~a}")
print(f"  a << 1 = {a << 1}")
print(f"  a >> 1 = {a >> 1}")

print("\nASSIGNMENT (augmented)")
x = a
x += b; print(f"  x += b -> {x}")
x -= b; print(f"  x -= b -> {x}")
x *= b; print(f"  x *= b -> {x}")
x //= b; print(f"  x //= b -> {x}")

print("\nIDENTITY and MEMBERSHIP")
print(f"  a is b     = {a is b}")
print(f"  a in [a, b] = {a in [a, b]}")
