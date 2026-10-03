# NOT EXECUTED -- PyMongo needs a running mongod, which these pages are not
# built against.  Every call here is mirrored by the pure-Python listing
# below, which WAS run and produces the output shown there.
from pymongo import MongoClient, ASCENDING

client = MongoClient("mongodb://localhost:27017/")
db = client["etl"]
col = db["customers"]

col.insert_many([
    {"_id": 1, "name": "Asha Rao", "address": {"city": "Vizag"},
     "income": 40, "tags": ["retail", "west"],
     "orders": [{"amt": 1240.50}, {"amt": 480.00}, {"amt": 75.25}]},
    {"_id": 2, "name": "Biju Menon", "address": {"city": "Kochi"},
     "income": 57, "tags": ["wholesale"], "orders": [{"amt": 99.00}]},
])

# find: a dotted path reaches inside a sub-document; an array field matches
# if ANY element matches; the second argument is the projection
list(col.find({"address.city": "Kochi"}, {"name": 1, "_id": 0}))
list(col.find({"income": {"$gt": 40}}))
list(col.find({"tags": "retail"}))

# update_one adds a field to ONE document and leaves every other alone
col.update_one({"_id": 1}, {"$set": {"status": "gold"}, "$inc": {"income": 5}})

# replace_one keeps the _id and DISCARDS every other field
col.replace_one({"_id": 4}, {"name": "Devan Iyer", "income": 70})

col.delete_many({"income": {"$lt": 40}})

# an aggregation pipeline: one stage at a time, in order
list(col.aggregate([
    {"$unwind": "$orders"},
    {"$group": {"_id": "$name", "n": {"$sum": 1},
                "total": {"$sum": "$orders.amt"}}},
    {"$sort": {"total": -1}},
]))

col.create_index([("address.city", ASCENDING)], name="ix_city")
col.create_index([("name", "text")], name="tx_name")
print(col.find({"_id": 2}).explain()["executionStats"]["totalDocsExamined"])

client.close()
