"""Experiment 9: Read a text file and display the count of vowels, consonants,
digits and spaces.

Syllabus: Course 3, Unit 4 -- file handling.
Creates its own sample.txt so the program runs standalone.
"""

FILENAME = "sample.txt"

# Step 1: Write the sample file
with open(FILENAME, "w") as fh:
    fh.write("Data Science Major 2025\n")
    fh.write("Andhra Pradesh State Council of Higher Education\n")

vowels = consonants = digits = spaces = others = 0

# Step 2: Read it back
# `with` closes the file automatically, even if an exception is raised.
with open(FILENAME, "r") as fh:
    text = fh.read()

# Step 3: Classify each character
for ch in text:
    if ch.isalpha():
        if ch.lower() in "aeiou":
            vowels += 1
        else:
            consonants += 1
    elif ch.isdigit():
        digits += 1
    elif ch == " ":
        spaces += 1
    elif ch != "\n":
        others += 1

# Step 4: Print the counts
print(f"Contents of {FILENAME}:")
print(text)
print(f"Vowels     : {vowels}")
print(f"Consonants : {consonants}")
print(f"Digits     : {digits}")
print(f"Spaces     : {spaces}")
print(f"Others     : {others}")
print(f"Total characters (excluding newlines): "
      f"{vowels + consonants + digits + spaces + others}")
