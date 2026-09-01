"""Experiment 13: Create a class Student with attributes and methods to
display details.

Syllabus: Course 3, Unit 4 -- classes, objects, constructors, destructors,
encapsulation.
"""


class Student:
    """A single student record."""

    college = "Adikavi Nannaya University"   # CLASS attribute -- shared by all

    def __init__(self, roll, name, marks):
        """The constructor. Runs automatically when a Student is created."""
        self.roll = roll                     # INSTANCE attributes -- per object
        self.name = name
        self.marks = marks
        self.__fees_paid = 0                 # PRIVATE (name-mangled) attribute

    def total(self):
        return sum(self.marks.values())

    def average(self):
        return self.total() / len(self.marks)

    def grade(self):
        avg = self.average()
        if avg >= 85:
            return "A"
        if avg >= 70:
            return "B"
        if avg >= 50:
            return "C"
        return "F"

    # ENCAPSULATION: the private attribute is reached only through methods,
    # so the class controls what counts as a valid change.
    def pay_fees(self, amount):
        if amount <= 0:
            raise ValueError("payment must be positive")
        self.__fees_paid += amount

    def fees_paid(self):
        return self.__fees_paid

    def display(self):
        print(f"  Roll    : {self.roll}")
        print(f"  Name    : {self.name}")
        print(f"  College : {self.college}")
        for subject, mark in self.marks.items():
            print(f"    {subject:<12} {mark:3d}")
        print(f"  Total   : {self.total()}")
        print(f"  Average : {self.average():.2f}")
        print(f"  Grade   : {self.grade()}")
        print(f"  Fees    : {self.fees_paid()}")

    def __str__(self):
        """Controls what print(object) shows."""
        return f"Student({self.roll}, {self.name}, grade {self.grade()})"

    def __del__(self):
        """The destructor -- called when the object is garbage collected."""
        # Guarded because interpreter shutdown can clear globals first.
        try:
            print(f"  [destructor] Student object {self.roll} destroyed")
        except Exception:
            pass


print("CREATING OBJECTS")
s1 = Student(24001, "Ananya", {"Maths": 85, "Statistics": 78, "Python": 92})
s2 = Student(24002, "Bhavana", {"Maths": 62, "Statistics": 58, "Python": 71})

print("\nOBJECT 1")
s1.display()
print("\nOBJECT 2")
s2.display()

print("\n__str__ in action")
print(f"  {s1}")
print(f"  {s2}")

print("\nENCAPSULATION")
s1.pay_fees(15000)
print(f"  after pay_fees(15000): {s1.fees_paid()}")
try:
    s1.pay_fees(-500)
except ValueError as exc:
    print(f"  pay_fees(-500) rejected: {exc}")
print(f"  s1.__fees_paid is not directly reachable; "
      f"name-mangled to _Student__fees_paid = {s1._Student__fees_paid}")

print("\nCLASS vs INSTANCE ATTRIBUTES")
Student.college = "APSCHE Affiliated College"
print(f"  changing the class attribute affects every object:")
print(f"    s1.college = {s1.college}")
print(f"    s2.college = {s2.college}")

print("\nDESTRUCTOR")
del s2
