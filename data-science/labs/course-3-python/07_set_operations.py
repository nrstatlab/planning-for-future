"""Experiment 7: Implement the set operations -- union, intersection,
difference, subset and superset.

Syllabus: Course 3, Unit 3 -- sets.
"""

A = {1, 2, 3, 4, 5}
B = {4, 5, 6, 7, 8}
print(f"A = {A}")
print(f"B = {B}")

print("\nMATHEMATICAL OPERATIONS  (operator and method forms are equivalent)")
print(f"  union            A | B  = {A | B}")
print(f"                   A.union(B) = {A.union(B)}")
print(f"  intersection     A & B  = {A & B}")
print(f"  difference       A - B  = {A - B}     in A but not in B")
print(f"                   B - A  = {B - A}     in B but not in A")
print(f"  symmetric diff   A ^ B  = {A ^ B}   in one or the other, not both")

print("\nSUBSET and SUPERSET")
C = {1, 2, 3}
print(f"  C = {C}")
print(f"  C.issubset(A)     = {C.issubset(A)}     C <= A is {C <= A}")
print(f"  A.issuperset(C)   = {A.issuperset(C)}     A >= C is {A >= C}")
print(f"  A.isdisjoint(B)   = {A.isdisjoint(B)}    they share 4 and 5")

print("\nMODIFYING A SET")
S = {10, 20}
S.add(30);            print(f"  add(30)        -> {S}")
S.update([40, 50]);   print(f"  update([40,50]) -> {S}")
S.discard(99);        print(f"  discard(99)    -> {S}   missing value is ignored")
S.remove(10);         print(f"  remove(10)     -> {S}")
try:
    S.remove(99)
except KeyError:
    print("  remove(99) raises KeyError -- unlike discard()")

print("\nDUPLICATES ARE DROPPED AUTOMATICALLY")
print(f"  set([1, 1, 2, 2, 3]) = {set([1, 1, 2, 2, 3])}")

print("\nFROZENSET -- the immutable version")
fs = frozenset([1, 2, 3])
print(f"  {fs}")
try:
    fs.add(4)
except AttributeError as exc:
    print(f"  fs.add(4) raises AttributeError: {exc}")

print("\nSET COMPREHENSION")
print(f"  {{n ** 2 for n in range(1, 6)}} = {{{', '.join(str(n**2) for n in range(1,6))}}}")
