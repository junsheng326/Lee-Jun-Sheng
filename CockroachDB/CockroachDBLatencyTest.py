"""
SIMPLE CockroachDB Latency Test - UPDATED
Tests UPDATE speed on imported data
"""

import psycopg2
import time

# Connect to database (using lowercase name)
conn = psycopg2.connect("postgresql://root@localhost:26257/defaultdb?sslmode=disable")
conn.autocommit = True
cur = conn.cursor()

# Switch to the database
cur.execute("USE latencyscalabilitytest")

# Collections to test (using lowercase names)
collections_to_test = [
    {"name": "dbms", "data_size": "10K"},
    {"name": "dbms01", "data_size": "100K"},
    {"name": "dbms02", "data_size": "500K"}
]

print("=" * 50)
print("CockroachDB Latency Test Results")
print("=" * 50)

# Test each collection
for coll in collections_to_test:
    table_name = coll["name"]
    data_size = coll["data_size"]
    
    # Time the UPDATE operation
    start_time = time.time()
    
    cur.execute(f"""
        UPDATE {table_name} 
        SET traininghours = 5 
        WHERE department = 'Finance' 
        LIMIT 1
    """)
    
    # Calculate latency
    latency = (time.time() - start_time) * 1000  # Convert to milliseconds
    
    # Print result
    print(f"\n{table_name.upper()} ({data_size} DATA)")
    print(f"Update Latency: {latency:.2f} ms")

print("\n" + "=" * 50)
print("Testing Complete")
print("=" * 50)

cur.close()
conn.close()