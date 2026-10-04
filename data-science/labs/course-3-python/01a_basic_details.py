"""Experiment 1(a): Display basic details using print() and demonstrate the
different literal types (int, float, string, boolean, complex).

Syllabus: Course 3, Unit 1 -- literals, variables, built-in data types.
"""

# Step 1: Assign one literal of each type
name = "Raghav"           # str literal
roll_number = 24001       # int literal
department = "Data Science"
cgpa = 8.75               # float literal
is_enrolled = True        # bool literal
impedance = 3 + 4j        # complex literal

# Step 2: Print the details
print("STUDENT DETAILS")
print("-" * 40)
print(f"Name       : {name}")
print(f"Roll number: {roll_number}")
print(f"Department : {department}")
print(f"CGPA       : {cgpa}")
print(f"Enrolled   : {is_enrolled}")

# Step 3: Name the type of each value
print("\nLITERAL TYPES")
print("-" * 40)
for value in (roll_number, cgpa, name, is_enrolled, impedance):
    print(f"{str(value):<20} -> {type(value).__name__}")

# Step 4: The two parts of a complex number
# A complex number carries .real and .imag attributes.
print(f"\nreal part of {impedance} = {impedance.real}")
print(f"imag part of {impedance} = {impedance.imag}")
