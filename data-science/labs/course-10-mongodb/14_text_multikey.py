"""Experiment 14 — Text search and multikey indexes.

Two halves, and they run differently.

MULTIKEY is fully executed: mongomock matches array fields the way a real
server does, so every assertion here is a real one.

TEXT SEARCH is not. mongomock accepts createIndex([("x", "text")]) but raises
NotImplementedError on $text -- that is asserted below rather than glossed
over, and the ranking and stemming rules are then set out as data. The runnable
substitute is a regex scan, which is also the honest answer to "what do I do
when I have no text index?".
"""
import mongomock
from fixtures import fresh_db, names


# =============================================================================
# PART A -- multikey indexes: fully executed
# =============================================================================

def an_index_on_an_array_is_multikey_automatically():
    """You never ask for a multikey index. MongoDB decides."""
    db = fresh_db()
    db.students.create_index("subjects")

    # The index exists and looks like any other single-field index.
    assert "subjects_1" in {i["name"] for i in db.students.list_indexes()}

    # Matching is CONTAINS, not equals: no student's subjects field IS "DS".
    assert names(db.students.find({"subjects": "DS"})) == ["Asha", "Kiran", "Ravi"]
    assert names(db.students.find({"subjects": "R"})) == ["Meena"]

    # And the whole array still matches as a whole, if you give it exactly.
    assert names(db.students.find({"subjects": ["DS", "Python"]})) == ["Ravi"]
    assert names(db.students.find({"subjects": ["Python", "DS"]})) == [], \
        "the whole-array form is ORDER SENSITIVE; the contains form is not"

    print("  { subjects: 'DS' } matched Asha, Kiran, Ravi -- CONTAINS, not equals")
    print("  { subjects: ['Python','DS'] } matched nobody -- whole-array match")
    print("       is order sensitive, and Ravi's array is ['DS','Python']")


def one_index_entry_per_element():
    """The cost model: a document with n array values costs n index entries."""
    db = fresh_db()
    entries = sum(len(d["subjects"]) for d in db.students.find())
    docs = db.students.count_documents({})
    assert docs == 5
    assert entries == 9, entries          # 3 + 2 + 2 + 1 + 1

    print(f"  {docs} documents -> {entries} index entries "
          f"({entries / docs:.1f} per document)")
    print("       an array of 1,000 elements means 1,000 entries for ONE")
    print("       document -- multikey indexes are bigger than they look")


def all_and_size_and_positional():
    db = fresh_db()

    # $all -- contains ALL of these (order irrelevant)
    assert names(db.students.find({"subjects": {"$all": ["DS", "Python"]}})) \
        == ["Asha", "Ravi"]

    # bare {a: x, ...} on an array is OR-ish across elements; $all is AND
    assert names(db.students.find({"subjects": {"$all": ["Stats", "R"]}})) == ["Meena"]

    # $size -- exact length. NEVER served by an index.
    assert names(db.students.find({"subjects": {"$size": 3}})) == ["Asha"]
    assert names(db.students.find({"subjects": {"$size": 1}})) == ["Bhanu", "Kiran"]

    # positional: the FIRST element specifically
    assert names(db.students.find({"subjects.0": "DS"})) == ["Asha", "Kiran", "Ravi"]
    assert names(db.students.find({"subjects.0": "Stats"})) == ["Bhanu", "Meena"]

    print("  $all ['DS','Python'] -> Asha, Ravi        (contains BOTH)")
    print("  $size 3              -> Asha              (never uses the index)")
    print("  subjects.0 'Stats'   -> Bhanu, Meena      (FIRST element only)")


def store_the_length_if_you_query_it():
    """The fix for $size's collection scan: a field you CAN index."""
    db = fresh_db()
    for d in db.students.find():
        db.students.update_one({"_id": d["_id"]},
                               {"$set": {"nSubjects": len(d["subjects"])}})
    db.students.create_index("nSubjects")

    assert names(db.students.find({"nSubjects": 3})) == ["Asha"]
    assert names(db.students.find({"nSubjects": {"$gte": 2}})) \
        == ["Asha", "Meena", "Ravi"]

    print("  nSubjects >= 2 -> Asha, Meena, Ravi -- and unlike $size this one is")
    print("       indexable, and supports RANGES, which $size cannot express")


def the_elemmatch_trap_again():
    """Two conditions on an array of sub-documents. The classic wrong answer."""
    db = fresh_db()
    db.students.update_one(
        {"_id": 21},
        {"$set": {"enrollments": [{"course": "DSC301", "grade": "B"},
                                  {"course": "STA302", "grade": "A"}]}})
    db.students.create_index("enrollments.grade")

    # WRONG: satisfied by two DIFFERENT elements -- Asha got B in DSC301.
    wrong = names(db.students.find({"enrollments.course": "DSC301",
                                   "enrollments.grade": "A"}))
    assert wrong == ["Asha"], wrong

    # RIGHT: both conditions on the SAME element.
    right = names(db.students.find(
        {"enrollments": {"$elemMatch": {"course": "DSC301", "grade": "A"}}}))
    assert right == [], right

    print("  Asha: DSC301->B, STA302->A")
    print("    without $elemMatch -> ['Asha']   WRONG (two different elements)")
    print("    with    $elemMatch -> []         RIGHT")


def the_compound_restriction():
    """At most ONE array field in a compound index. Stated, not executed."""
    rules = [
        ("{ subjects: 1 }",            "OK", "one array field"),
        ("{ subjects: 1, dept: 1 }",   "OK", "one array, one scalar"),
        ("{ dept: 1, subjects: 1 }",   "OK", "order does not change the rule"),
        ("{ subjects: 1, tags: 1 }",   "ERROR",
         "two array fields -- cannot compute the cross product"),
    ]
    assert sum(1 for _, v, _ in rules if v == "ERROR") == 1

    print("  compound indexes containing arrays:")
    for spec, verdict, why in rules:
        print(f"    {spec:28s} {verdict:6s} {why}")
    print("       the reason: indexing both would need EVERY pair, so a")
    print("       document with 10 and 10 would need 100 index entries")


# =============================================================================
# PART B -- text search: mongomock cannot run it, so say so and prove it
# =============================================================================

ARTICLES = [
    {"_id": 1, "title": "Introduction to MongoDB",
     "body": "MongoDB is a document database that stores data in BSON."},
    {"_id": 2, "title": "Aggregation pipelines explained",
     "body": "The aggregation framework processes documents through stages."},
    {"_id": 3, "title": "Indexing strategy in MongoDB",
     "body": "An index is a B-tree. Aggregation queries benefit from indexes too."},
    {"_id": 4, "title": "Relational databases",
     "body": "SQL databases use tables, rows and joins."},
]


def text_search_is_not_implemented_here():
    """Asserted, so this file can never quietly start claiming to test $text."""
    db = mongomock.MongoClient().collegeDB
    db.articles.insert_many([dict(a) for a in ARTICLES])
    db.articles.create_index([("title", "text"), ("body", "text")])

    try:
        list(db.articles.find({"$text": {"$search": "mongodb"}}))
        raise SystemExit("mongomock now implements $text -- rewrite this file "
                         "to assert results instead of documenting them")
    except NotImplementedError as exc:
        message = str(exc)
    assert "$text" in message, message

    print("  mongomock accepted the text INDEX and then raised")
    print(f"    NotImplementedError: {message}")
    print("       so nothing below is a test result -- it is documentation")


def what_a_real_server_would_return():
    """The expected results, worked out by hand from the four articles."""
    expected = [
        ('"mongodb"',                  [1, 3],       "the word, in title or body"),
        ('"mongodb aggregation"',      [1, 2, 3],    "OR of the two terms, NOT and"),
        ('"\\"aggregation framework\\""', [2],       "a PHRASE -- adjacent words"),
        ('"mongodb -relational"',      [1, 3],       "- excludes; 4 never matched anyway"),
        ('"mongo"',                    [],           "WORDS, not substrings"),
        ('"stores"',                   [1],          "stemming: matches 'stores'/'storing'"),
        ('"the"',                      [],           "a stop word -- ignored entirely"),
    ]
    print("  on a real server, $text: { $search: ... } would return:")
    for term, ids, why in expected:
        print(f"    {term:32s} -> {str(ids):10s} {why}")
    print("       'mongo' returning NOTHING is the one that catches people:")
    print("       a text index stores WORDS. For prefixes use a regex anchored")
    print("       with ^, or Atlas Search; a bare /mongo/ scans the collection")


def regex_is_the_runnable_substitute():
    """What you actually do without a text index -- and it IS executed."""
    db = mongomock.MongoClient().collegeDB
    db.articles.insert_many([dict(a) for a in ARTICLES])

    hits = sorted(d["_id"] for d in
                  db.articles.find({"title": {"$regex": "mongo", "$options": "i"}}))
    assert hits == [1, 3], hits

    # And here is where regex BEATS $text: substrings.
    sub = sorted(d["_id"] for d in
                 db.articles.find({"body": {"$regex": "aggregat", "$options": "i"}}))
    assert sub == [2, 3], sub

    # And where it loses: no stemming, no ranking.
    stem = sorted(d["_id"] for d in
                  db.articles.find({"body": {"$regex": "store$", "$options": "i"}}))
    assert stem == [], "regex has no stemming -- 'stores' does not match 'store$'"

    print("  regex /mongo/i on title  -> [1, 3]   (substring: $text would miss)")
    print("  regex /aggregat/i on body-> [2, 3]   (substring again)")
    print("  regex /store$/i on body  -> []       (no stemming, no ranking,")
    print("       and an unanchored regex cannot use an index -- COLLSCAN)")


def the_text_index_rules():
    rules = [
        ("How many per collection?", "ONE",
         "it may span many fields, but you cannot have two"),
        ("Every field?", '{ "$**": "text" }',
         "a wildcard text index -- convenient, and large"),
        ("Weights", "{ title: 10, body: 1 }",
         "a title hit scores ten times a body hit"),
        ("Getting the score", '{ $meta: "textScore" }',
         "must be PROJECTED to exist"),
        ("Ordering by it", '.sort({ score: { $meta: "textScore" } })',
         "$text does NOT sort by relevance on its own"),
        ("Case / accents", "insensitive by default", "both, unless configured"),
        ("Inside $or", "not with a non-text clause", "one $text per query"),
    ]
    assert len(rules) == 7
    print("  text index rules:")
    for q, a, why in rules:
        print(f"    {q:24s} {a:34s} {why}")


def main():
    print("Experiment 14 -- Text search and multikey indexes")
    print("  PART A -- multikey: EXECUTED and asserted")
    an_index_on_an_array_is_multikey_automatically()
    one_index_entry_per_element()
    all_and_size_and_positional()
    store_the_length_if_you_query_it()
    the_elemmatch_trap_again()
    the_compound_restriction()
    print("  PART B -- text search: NOT executable here")
    text_search_is_not_implemented_here()
    what_a_real_server_would_return()
    regex_is_the_runnable_substitute()
    the_text_index_rules()


if __name__ == "__main__":
    main()
