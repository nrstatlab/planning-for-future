// Experiment 12 -- Implementing schema validation using JSON Schema.
//
// *** NOT EXECUTED ***
// This is the mongosh script for the lab exam. mongod cannot be installed in
// the verification environment (the Debian repositories that host mongodb-org
// are blocked by the egress policy), so this file has never been run here.
// The query logic is executed and asserted in the matching .py file, through
// mongomock. See notes/sem-4/course-10-document-database/lab.md.

use collegeDB
db.validated.drop()

db.createCollection("validated", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["roll", "name", "dept"],
      properties: {
        roll: { bsonType: "int", minimum: 1,
                description: "required integer, at least 1" },
        name: { bsonType: "string", minLength: 3, maxLength: 80 },
        dept: { enum: ["DS", "Stats", "CS"],
                description: "must be DS, Stats or CS" },
        marks: {
          bsonType: "object",
          properties: {
            maths: { bsonType: "int", minimum: 0, maximum: 100 },
            stats: { bsonType: "int", minimum: 0, maximum: 100 }
          }
        },
        email: { bsonType: "string", pattern: "^[^\\s@]+@[^\\s@]+\\.[^\\s@]{2,}$" }
      }
    }
  },
  validationLevel: "strict",
  validationAction: "error"
})

db.validated.insertOne({ roll: NumberInt(21), name: "Asha", dept: "DS",
                         marks: { maths: NumberInt(88) } })     // OK

db.validated.insertOne({ name: "NoRoll", dept: "DS" })          // missing required
db.validated.insertOne({ roll: NumberInt(22), name: "Ab", dept: "DS" })  // too short
db.validated.insertOne({ roll: NumberInt(23), name: "Ravi", dept: "Physics" })  // enum
db.validated.insertOne({ roll: NumberInt(24), name: "Meena", dept: "DS",
                         marks: { maths: NumberInt(150) } })    // out of range

// --- adding validation to a collection that ALREADY holds messy data --------
// 1. Attach it in the SAFEST mode: log, do not block.
db.runCommand({ collMod: "students",
                validator: { $jsonSchema: { /* as above */ } },
                validationLevel: "moderate",
                validationAction: "warn" })

// 2. FIND the offenders -- $nor inverts a $jsonSchema match
db.students.find({ $nor: [ { $jsonSchema: { /* as above */ } } ] })

// 3. Fix them, confirm the count is zero, then:
db.runCommand({ collMod: "students",
                validationLevel: "strict", validationAction: "error" })
