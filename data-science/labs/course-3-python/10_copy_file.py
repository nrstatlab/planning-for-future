"""Experiment 10: Copy the contents of one file into another file.

Syllabus: Course 3, Unit 4 -- file handling.
"""

SOURCE = "source.txt"
TARGET = "target.txt"

with open(SOURCE, "w") as fh:
    fh.write("Line 1: Python file handling\n")
    fh.write("Line 2: reading and writing\n")
    fh.write("Line 3: Data Science Major\n")

# Copy line by line so the program works on files too large to hold in memory.
lines_copied = 0
with open(SOURCE, "r") as src, open(TARGET, "w") as dst:
    for line in src:
        dst.write(line)
        lines_copied += 1

print(f"Copied {lines_copied} lines from {SOURCE} to {TARGET}\n")

with open(TARGET, "r") as fh:
    print(f"Contents of {TARGET}:")
    print(fh.read())

# Verify the two files now match.
with open(SOURCE) as a, open(TARGET) as b:
    print("Files are identical" if a.read() == b.read() else "Files DIFFER")
