// The sample data every experiment from 3 onwards starts from: the five students
// of Experiment 2, with the courses and enrollments that Experiment 16 joins.
// It is the data in fixtures.py, which the Python halves load, exactly;
// tools/data-science/run_mongo_labs.py checks that the two agree.
//
// Each script loads it in its second line, with load("00_sample_data.js"), so
// it can be run on its own, as often as you like: start mongosh in this folder.
// It drops and refills only these three collections.

// Step 1: Switch to collegeDB
db = db.getSiblingDB("collegeDB")

// Step 2: Refill the students
db.students.drop()
db.students.insertMany([
  {"_id": 21, "name": "Asha", "dept": "DS", "marks": {"maths": 88, "stats": 91}, "subjects": ["DS", "Stats", "Python"], "age": 20, "active": true},
  {"_id": 22, "name": "Ravi", "dept": "DS", "marks": {"maths": 65, "stats": 58}, "subjects": ["DS", "Python"], "age": 21, "active": true},
  {"_id": 23, "name": "Meena", "dept": "Stats", "marks": {"maths": 94, "stats": 89}, "subjects": ["Stats", "R"], "age": 20, "active": true},
  {"_id": 24, "name": "Kiran", "dept": "DS", "marks": {"maths": 71, "stats": 66}, "subjects": ["DS"], "age": 22, "active": false},
  {"_id": 25, "name": "Bhanu", "dept": "Stats", "marks": {"maths": 52, "stats": 47}, "subjects": ["Stats"], "age": 21, "active": true}
])

// Step 3: Refill the courses
db.courses.drop()
db.courses.insertMany([
  {"_id": "DSC301", "title": "Data Science with R", "credits": 4, "instructor": "Dr. Rao"},
  {"_id": "STA302", "title": "Statistical Foundations", "credits": 3, "instructor": "Dr. Devi"},
  {"_id": "WEB303", "title": "Web Technologies", "credits": 3, "instructor": "Dr. Kumar"}
])

// Step 4: Refill the enrollments
db.enrollments.drop()
db.enrollments.insertMany([
  {"student_id": 21, "course_id": "DSC301", "grade": "A"},
  {"student_id": 21, "course_id": "STA302", "grade": "B"},
  {"student_id": 22, "course_id": "DSC301", "grade": "C"},
  {"student_id": 23, "course_id": "STA302", "grade": "A"},
  {"student_id": 24, "course_id": "WEB303", "grade": "B"}
])

// Step 5: Say what was loaded
print("sample data loaded: " + db.students.countDocuments() + " students, " +
      db.courses.countDocuments() + " courses, " + db.enrollments.countDocuments() + " enrollments")
