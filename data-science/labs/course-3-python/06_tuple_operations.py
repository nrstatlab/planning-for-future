"""Experiment 6: Demonstrate tuple packing, unpacking and immutability.

Syllabus: Course 3, Unit 3 -- tuples.
"""

print("PACKING -- several values collected into one tuple")
student = "Ananya", 24001, 8.75
print(f"  student = {student}  type {type(student).__name__}")

print("\nUNPACKING -- one tuple spread across several variables")
name, roll, cgpa = student
print(f"  name = {name}, roll = {roll}, cgpa = {cgpa}")

print("\nEXTENDED UNPACKING with *")
first, *rest = (10, 20, 30, 40)
print(f"  first = {first}, rest = {rest}   (rest is a list)")

print("\nSWAPPING via tuple assignment -- no temporary variable needed")
a, b = 5, 9
print(f"  before: a = {a}, b = {b}")
a, b = b, a
print(f"  after : a = {a}, b = {b}")

print("\nOPERATIONS")
t = (1, 2, 3, 2, 5)
print(f"  t = {t}")
print(f"  len(t)      = {len(t)}")
print(f"  t + (6, 7)  = {t + (6, 7)}")
print(f"  t * 2       = {t * 2}")
print(f"  t[1:4]      = {t[1:4]}")
print(f"  t.count(2)  = {t.count(2)}")
print(f"  t.index(3)  = {t.index(3)}")
print(f"  max(t)      = {max(t)}, min(t) = {min(t)}, sum(t) = {sum(t)}")

print("\nIMMUTABILITY")
try:
    t[0] = 99
except TypeError as exc:
    print(f"  t[0] = 99 raises TypeError: {exc}")

print("\nSINGLE-ELEMENT TUPLE -- the trailing comma is what makes it a tuple")
not_a_tuple = (5)
actual_tuple = (5,)
print(f"  (5)  -> {type(not_a_tuple).__name__}")
print(f"  (5,) -> {type(actual_tuple).__name__}")

print("\nWHY TUPLES: being immutable, they can be dictionary keys")
locations = {(17.68, 83.21): "Visakhapatnam", (16.99, 82.24): "Kakinada"}
print(f"  {locations}")
