"""Experiment 12 — Schema validation with JSON Schema.

*** mongomock does NOT enforce $jsonSchema. ***

Rather than pretend it does, this script implements the SAME rules in code and
asserts that a conforming document passes and each kind of violation is caught.
The mongosh half (12_validation.js) is what you run on a real server.
"""
import re
import mongomock

SCHEMA = {
    "bsonType": "object",
    "required": ["roll", "name", "dept"],
    "properties": {
        "roll":  {"bsonType": "int", "minimum": 1},
        "name":  {"bsonType": "string", "minLength": 3, "maxLength": 80},
        "dept":  {"enum": ["DS", "Stats", "CS"]},
        "marks": {"bsonType": "object", "properties": {
            "maths": {"bsonType": "int", "minimum": 0, "maximum": 100},
            "stats": {"bsonType": "int", "minimum": 0, "maximum": 100}}},
        "email": {"bsonType": "string",
                  "pattern": r"^[^\s@]+@[^\s@]+\.[^\s@]{2,}$"},
    },
}

BSON_TYPES = {"int": int, "string": str, "object": dict, "double": float,
              "bool": bool, "array": list}


def violations(doc, schema=SCHEMA, path=""):
    """Return the list of ways `doc` fails `schema`. Empty means it conforms."""
    out = []
    for field in schema.get("required", []):
        if field not in doc:
            out.append(f"{path}{field}: required field missing")

    for field, rule in schema.get("properties", {}).items():
        if field not in doc:
            continue
        value = doc[field]
        where = f"{path}{field}"

        want = rule.get("bsonType")
        if want and not isinstance(value, BSON_TYPES[want]):
            out.append(f"{where}: expected {want}, got {type(value).__name__}")
            continue
        if "enum" in rule and value not in rule["enum"]:
            out.append(f"{where}: {value!r} not in {rule['enum']}")
        if "minimum" in rule and value < rule["minimum"]:
            out.append(f"{where}: {value} below minimum {rule['minimum']}")
        if "maximum" in rule and value > rule["maximum"]:
            out.append(f"{where}: {value} above maximum {rule['maximum']}")
        if "minLength" in rule and len(value) < rule["minLength"]:
            out.append(f"{where}: shorter than {rule['minLength']}")
        if "maxLength" in rule and len(value) > rule["maxLength"]:
            out.append(f"{where}: longer than {rule['maxLength']}")
        if "pattern" in rule and not re.match(rule["pattern"], value):
            out.append(f"{where}: does not match {rule['pattern']}")
        if rule.get("bsonType") == "object" and "properties" in rule:
            out.extend(violations(value, rule, path=f"{where}."))
    return out


def conforming_document_passes():
    good = {"roll": 21, "name": "Asha", "dept": "DS", "marks": {"maths": 88},
            "email": "asha@nri.ac.in"}
    assert violations(good) == [], violations(good)
    print("  a conforming document produces no violations")


def each_violation_is_caught():
    cases = {
        "missing required": ({"name": "NoRoll", "dept": "DS"}, "required"),
        "name too short":   ({"roll": 22, "name": "Ab", "dept": "DS"}, "shorter"),
        "dept not in enum": ({"roll": 23, "name": "Ravi", "dept": "Physics"}, "not in"),
        "marks over 100":   ({"roll": 24, "name": "Meena", "dept": "DS",
                              "marks": {"maths": 150}}, "above maximum"),
        "roll below 1":     ({"roll": 0, "name": "Zero", "dept": "DS"}, "below minimum"),
        "roll wrong type":  ({"roll": "21", "name": "Str", "dept": "DS"}, "expected int"),
        "bad email":        ({"roll": 25, "name": "Bhanu", "dept": "DS",
                              "email": "not-an-email"}, "does not match"),
    }
    for label, (doc, expected) in cases.items():
        found = violations(doc)
        assert found, f"{label}: expected a violation, got none"
        assert any(expected in v for v in found), f"{label}: {found}"
        print(f"    {label:18s} -> {found[0]}")

    print("  every rule in the schema is enforced")


def find_the_offenders():
    """The migration step: find what does NOT conform, before tightening."""
    db = mongomock.MongoClient().collegeDB
    db.messy.insert_many([
        {"roll": 21, "name": "Asha", "dept": "DS"},          # ok
        {"roll": 22, "name": "Ab", "dept": "DS"},            # name too short
        {"name": "NoRoll", "dept": "Stats"},                 # missing roll
        {"roll": 24, "name": "Kiran", "dept": "Physics"},    # bad dept
    ])

    offenders = [(d.get("name"), violations(d)) for d in db.messy.find()
                 if violations(d)]
    assert len(offenders) == 3, offenders
    assert all(v for _, v in offenders)

    conforming = [d for d in db.messy.find() if not violations(d)]
    assert len(conforming) == 1 and conforming[0]["name"] == "Asha"

    print(f"  3 of 4 documents violate the schema:")
    for name, vs in offenders:
        print(f"    {str(name):10s} {vs[0]}")
    print("  on a real server: $nor: [ { $jsonSchema: ... } ] finds exactly these")


def the_migration_path():
    """Turning strict validation on over dirty data breaks the application."""
    levels = {
        "strict":   "applies to EVERY insert and update",
        "moderate": "applies to inserts, and to updates of documents that ALREADY conform",
        "off":      "applies to nothing",
    }
    actions = {"error": "REJECT the write", "warn": "LOG it and accept"}

    assert set(levels) == {"strict", "moderate", "off"}
    assert set(actions) == {"error", "warn"}

    print("  validationLevel:")
    for k, v in levels.items():
        print(f"    {k:9s} {v}")
    print("  validationAction:")
    for k, v in actions.items():
        print(f"    {k:9s} {v}")
    print("  migration: moderate+warn -> find offenders -> fix -> strict+error")
    print("       going straight to strict+error breaks every update to a")
    print("       non-conforming document, INCLUDING the one that would fix it")


def main():
    print("Experiment 12 -- Schema validation")
    print("  NOTE: mongomock does not enforce $jsonSchema, so the same rules")
    print("        are implemented in code here and asserted.")
    conforming_document_passes()
    each_violation_is_caught()
    find_the_offenders()
    the_migration_path()


if __name__ == "__main__":
    main()
