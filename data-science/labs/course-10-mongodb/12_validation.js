// Experiment 12 -- Implementing schema validation using JSON Schema.
//
// Run with MongoDB 8.3.7 and mongosh 2.12.0, on a fresh server: it is typed
// into mongosh line by line, as you would at the prompt. What each line printed
// is on the lab page, and tools/data-science/capture_lab_outputs.py runs it
// again. The query logic is also executed and asserted in 12_validation.py,
// through mongomock. (Until October 2026 mongod could not be installed where
// these labs are checked, and this file was desk-checked only.)
//
// Start mongosh in this folder: the line after `use collegeDB` loads the
// sample data, 00_sample_data.js.

// Step 1: Load the sample data
use collegeDB
load("00_sample_data.js")
db.validated.drop()

// Step 2: Write the schema
const schema = {
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
// Step 3: Create a collection that enforces it
db.createCollection("validated", {
  validator: { $jsonSchema: schema },
  validationLevel: "strict",
  validationAction: "error"
})

// Step 4: Insert a conforming document, and four that are not
db.validated.insertOne({ roll: NumberInt(21), name: "Asha", dept: "DS",
                         marks: { maths: NumberInt(88) } })     // OK

db.validated.insertOne({ name: "NoRoll", dept: "DS" })          // missing required
db.validated.insertOne({ roll: NumberInt(22), name: "Ab", dept: "DS" })  // too short
db.validated.insertOne({ roll: NumberInt(23), name: "Ravi", dept: "Physics" })  // enum
db.validated.insertOne({ roll: NumberInt(24), name: "Meena", dept: "DS",
                         marks: { maths: NumberInt(150) } })    // out of range

// Step 5: Add validation to data already there, in stages
// 1. Attach it in the SAFEST mode: log, do not block.
db.runCommand({ collMod: "students",
                validator: { $jsonSchema: schema },
                validationLevel: "moderate",
                validationAction: "warn" })

// 2. FIND the offenders -- $nor inverts a $jsonSchema match
db.students.find({ $nor: [ { $jsonSchema: schema } ] })
// [Corrected: these two read { $jsonSchema: { /* as above */ } }, an empty
// schema, which every document passes, so no offender could be found. The
// schema is now a const, defined once and used three times.]

// 3. Fix them, confirm the count is zero, then:
db.runCommand({ collMod: "students",
                validationLevel: "strict", validationAction: "error" })
