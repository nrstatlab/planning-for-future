"""Experiment 8: Create a dictionary of student roll numbers and marks, then
add, update, delete and traverse it.

Syllabus: Course 3, Unit 3 -- dictionaries.
"""

# Step 1: The dictionary
marks = {24001: 85, 24002: 72, 24003: 91, 24004: 64}
print(f"initial dictionary: {marks}")

# Step 2: Add
print("\nADD")
marks[24005] = 78
print(f"  marks[24005] = 78 -> {marks}")

# Step 3: Update
print("\nUPDATE")
marks[24002] = 80
print(f"  marks[24002] = 80 -> {marks}")
marks.update({24001: 88, 24006: 55})
print(f"  update({{...}})     -> {marks}")

# Step 4: Delete
print("\nDELETE")
removed = marks.pop(24006)
print(f"  pop(24006)        -> {marks}   returned {removed}")
del marks[24004]
print(f"  del marks[24004]  -> {marks}")

# Step 5: Access
print("\nACCESS")
print(f"  marks[24003]           = {marks[24003]}")
print(f"  marks.get(24003)       = {marks.get(24003)}")
print(f"  marks.get(99999)       = {marks.get(99999)}   <- None, no exception")
print(f"  marks.get(99999, 0)    = {marks.get(99999, 0)}      <- with a default")
try:
    marks[99999]
except KeyError as exc:
    print(f"  marks[99999] raises KeyError: {exc}")

# Step 6: Traversal
print("\nTRAVERSAL")
print("  keys  :", list(marks.keys()))
print("  values:", list(marks.values()))
print("  items :")
for roll, score in marks.items():
    grade = "A" if score >= 85 else "B" if score >= 70 else "C"
    print(f"    roll {roll}: {score:3d} -> grade {grade}")

# Step 7: Aggregates
print("\nAGGREGATES")
scores = list(marks.values())
print(f"  count   = {len(scores)}")
print(f"  total   = {sum(scores)}")
print(f"  average = {sum(scores) / len(scores):.2f}")
print(f"  highest = {max(marks, key=marks.get)} with {max(scores)}")
print(f"  lowest  = {min(marks, key=marks.get)} with {min(scores)}")

# Step 8: Dictionary comprehension
print("\nDICTIONARY COMPREHENSION")
print(f"  passed (>= 75): {dict((k, v) for k, v in marks.items() if v >= 75)}")
