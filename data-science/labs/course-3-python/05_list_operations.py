"""Experiment 5: Create a list of numbers and perform insertion, deletion,
searching, sorting and list comprehension.

Syllabus: Course 3, Unit 3 -- lists.
"""

numbers = [45, 12, 78, 3, 56, 23]
print(f"original list: {numbers}")

print("\nINSERTION")
numbers.append(99)
print(f"  append(99)      -> {numbers}")
numbers.insert(2, 50)
print(f"  insert(2, 50)   -> {numbers}")
numbers.extend([7, 8])
print(f"  extend([7, 8])  -> {numbers}")

print("\nDELETION")
numbers.remove(3)
print(f"  remove(3)       -> {numbers}      removes the first matching value")
popped = numbers.pop()
print(f"  pop()           -> {numbers}   returned {popped}")
del numbers[0]
print(f"  del numbers[0]  -> {numbers}")

print("\nSEARCHING")
print(f"  56 in numbers      = {56 in numbers}")
print(f"  numbers.index(56)  = {numbers.index(56)}")
print(f"  numbers.count(12)  = {numbers.count(12)}")

print("\nSORTING")
print(f"  sorted(numbers)              = {sorted(numbers)}   returns a new list")
print(f"  sorted(numbers, reverse=True) = {sorted(numbers, reverse=True)}")
numbers.sort()
print(f"  numbers.sort()               -> {numbers}   sorts in place")

print("\nLIST COMPREHENSION")
print(f"  squares       = {[n ** 2 for n in numbers]}")
print(f"  evens only    = {[n for n in numbers if n % 2 == 0]}")
print(f"  labelled      = {['even' if n % 2 == 0 else 'odd' for n in numbers]}")
matrix = [[row * col for col in range(1, 4)] for row in range(1, 4)]
print(f"  nested (3x3)  = {matrix}")

print("\nMUTABILITY -- lists are mutable, unlike strings and tuples")
alias = numbers          # same object
copy = numbers.copy()    # independent object
numbers[0] = 999
print(f"  after numbers[0] = 999:")
print(f"    alias = {alias}   <- changed too, it is the same list")
print(f"    copy  = {copy}   <- unchanged, it is a separate list")
