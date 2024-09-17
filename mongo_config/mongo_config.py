from pymongo import MongoClient

client = MongoClient('mongodb://bdp-mongo-container:27017/')

db_name = 'bdp-database'
db = client[db_name]

if 'processed_data' not in db.list_collection_names():
    db.create_collection('processed_data')
if 'raw_data' not in db.list_collection_names():
    db.create_collection('raw_data')

print("Database and collections are ready!")