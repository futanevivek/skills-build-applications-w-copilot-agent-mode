from pymongo import MongoClient

# Connect to MongoDB
print("Connecting to MongoDB...")
client = MongoClient('localhost', 27017)
print("Database names:", client.list_database_names())
db = client['octofit_db']

# Test inserting a document
test_collection = db['test_collection']
test_document = {"test_key": "test_value"}
result = test_collection.insert_one(test_document)

# Verify the document was inserted
print("Inserted document ID:", result.inserted_id)
retrieved_document = test_collection.find_one({"_id": result.inserted_id})
print("Inserted Document:", retrieved_document)

# Clean up
test_collection.delete_one({"_id": result.inserted_id})
