"""Experiment 14: Demonstrate single and multilevel inheritance.

The syllabus (Unit 4) also lists multiple inheritance and method overriding,
so both are included.

Syllabus: Course 3, Unit 4 -- inheritance.
"""

print("=" * 60)
print("SINGLE INHERITANCE -- one child, one parent")
print("=" * 60)


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def display(self):
        print(f"  Name: {self.name}, Age: {self.age}")

    def role(self):
        return "person"


class Student(Person):
    def __init__(self, name, age, roll):
        super().__init__(name, age)      # call the parent's constructor
        self.roll = roll

    def display(self):                   # METHOD OVERRIDING
        super().display()                # reuse the parent version, then add
        print(f"  Roll: {self.roll}")

    def role(self):
        return "student"


s = Student("Ananya", 19, 24001)
s.display()
print(f"  role() -> {s.role()}   (overrides Person.role)")
print(f"  isinstance(s, Person) = {isinstance(s, Person)}")

print()
print("=" * 60)
print("MULTILEVEL INHERITANCE -- a chain: Person -> Student -> ResearchScholar")
print("=" * 60)


class ResearchScholar(Student):
    def __init__(self, name, age, roll, topic):
        super().__init__(name, age, roll)
        self.topic = topic

    def display(self):
        super().display()
        print(f"  Research topic: {self.topic}")

    def role(self):
        return "research scholar"


r = ResearchScholar("Charan", 24, 21007, "Time Series Forecasting")
r.display()
print(f"  role() -> {r.role()}")
print("  Method Resolution Order:")
for cls in ResearchScholar.__mro__:
    print(f"    {cls.__name__}")

print()
print("=" * 60)
print("MULTIPLE INHERITANCE -- one child, two parents")
print("=" * 60)


class Teacher:
    def __init__(self, subject):
        self.subject = subject

    def teach(self):
        print(f"  teaches {self.subject}")


class TeachingAssistant(Student, Teacher):
    def __init__(self, name, age, roll, subject):
        Student.__init__(self, name, age, roll)
        Teacher.__init__(self, subject)

    def display(self):
        Student.display(self)
        self.teach()


ta = TeachingAssistant("Divya", 22, 22014, "Python Programming")
ta.display()
print("  MRO:", " -> ".join(c.__name__ for c in TeachingAssistant.__mro__))

print()
print("=" * 60)
print("POLYMORPHISM -- same call, different behaviour per class")
print("=" * 60)
for obj in (Person("Generic", 40), s, r, ta):
    print(f"  {type(obj).__name__:<20} role() = {obj.role()}")
