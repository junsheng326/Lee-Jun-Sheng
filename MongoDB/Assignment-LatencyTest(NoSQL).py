#first install pymongo at terminal to allow mongoDB connection
# pip install pymongo


#--------------------------------------------------------------------------------


'''Testing through running the data one by one'''
# TESTING DBMS (10K DATA)
import pymongo 
from pymongo import MongoClient
import time

# 1. Connect to the local MongoDB instance managed by Compass
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["LatencyScalabilityTest"]
collection = db["DBMS"]

# 2. Example Latency Test (Timing a single update)
start_time = time.time()
collection.update_one({"Department": "Finance"}, {"$set": {"Traning Hours": "5"}})
latency = (time.time() - start_time) * 1000  # Convert to milliseconds

print(f"Update Latency: {latency:.2f} ms")

# TEST DBMS01 (100K DATA)
import pymongo 
from pymongo import MongoClient
import time

# 1. Connect to the local MongoDB instance managed by Compass
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["LatencyScalabilityTest"]
collection = db["DBMS01"]

# 2. Example Latency Test (Timing a single update)
start_time = time.time()
collection.update_one({"Department": "Finance"}, {"$set": {"Traning Hours": "5"}})
latency = (time.time() - start_time) * 1000  # Convert to milliseconds

print(f"Update Latency: {latency:.2f} ms")


# TEST DBMS02 (500K DATA)
import pymongo 
from pymongo import MongoClient
import time

# 1. Connect to the local MongoDB instance managed by Compass
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["JLatencyScalabilityTest"]
collection = db["DBMS02"]

# 2. Example Latency Test (Timing a single update)
start_time = time.time()
collection.update_one({"Department": "Finance"}, {"$set": {"Traning Hours": "5"}})
latency = (time.time() - start_time) * 1000  # Convert to milliseconds

print(f"Update Latency: {latency:.2f} ms")


'''Combined testing (running three datasets simultaneously)'''

import pymongo 
from pymongo import MongoClient
import time

# Connect to the local MongoDB instance managed by Compass
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["LatencyScalabilityTest"]

# Define collections to test
collections_to_test = [
    {"name": "DBMS01", "data_size": "10K"},
    {"name": "DBMS02", "data_size": "100K"},
    {"name": "DBMS03", "data_size": "500K"}
]

# Run latency test for each collection
print("=" * 50)
print("MongoDB Latency Test Results")
print("=" * 50)

for coll_info in collections_to_test:
    collection = db[coll_info["name"]]
    
    # Perform latency test (timing a single update)
    start_time = time.time()
    collection.update_one({"Department": "Finance"}, {"$set": {"Traning Hours": "5"}})
    latency = (time.time() - start_time) * 1000  # Convert to milliseconds
    
    print(f"\n{coll_info['name']} ({coll_info['data_size']} DATA)")
    print(f"Update Latency: {latency:.2f} ms")

print("\n" + "=" * 50)
print("Testing Complete")
print("=" * 50)


