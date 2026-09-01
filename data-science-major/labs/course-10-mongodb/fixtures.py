"""Shared sample data for the Course 10 practicals.

One definition, used by every script, so the labs cannot drift from each other
or from the worked examples in the notes. This is the same collection the
notes use throughout Units 3 to 5.
"""
import mongomock

STUDENTS = [
    {"_id": 21, "name": "Asha",  "dept": "DS",
     "marks": {"maths": 88, "stats": 91},
     "subjects": ["DS", "Stats", "Python"], "age": 20, "active": True},
    {"_id": 22, "name": "Ravi",  "dept": "DS",
     "marks": {"maths": 65, "stats": 58},
     "subjects": ["DS", "Python"], "age": 21, "active": True},
    {"_id": 23, "name": "Meena", "dept": "Stats",
     "marks": {"maths": 94, "stats": 89},
     "subjects": ["Stats", "R"], "age": 20, "active": True},
    {"_id": 24, "name": "Kiran", "dept": "DS",
     "marks": {"maths": 71, "stats": 66},
     "subjects": ["DS"], "age": 22, "active": False},
    {"_id": 25, "name": "Bhanu", "dept": "Stats",
     "marks": {"maths": 52, "stats": 47},
     "subjects": ["Stats"], "age": 21, "active": True},
]

COURSES = [
    {"_id": "DSC301", "title": "Data Science with R", "credits": 4,
     "instructor": "Dr. Rao"},
    {"_id": "STA302", "title": "Statistical Foundations", "credits": 3,
     "instructor": "Dr. Devi"},
    {"_id": "WEB303", "title": "Web Technologies", "credits": 3,
     "instructor": "Dr. Kumar"},
]

ENROLLMENTS = [
    {"student_id": 21, "course_id": "DSC301", "grade": "A"},
    {"student_id": 21, "course_id": "STA302", "grade": "B"},
    {"student_id": 22, "course_id": "DSC301", "grade": "C"},
    {"student_id": 23, "course_id": "STA302", "grade": "A"},
    {"student_id": 24, "course_id": "WEB303", "grade": "B"},
]


def fresh_db():
    """A clean in-memory database with the sample data loaded."""
    db = mongomock.MongoClient().collegeDB
    db.students.insert_many([dict(d) for d in STUDENTS])
    db.courses.insert_many([dict(d) for d in COURSES])
    db.enrollments.insert_many([dict(d) for d in ENROLLMENTS])
    return db


def names(cursor):
    """Sorted names from a cursor -- what most assertions compare."""
    return sorted(d["name"] for d in cursor)
